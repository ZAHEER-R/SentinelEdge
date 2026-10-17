#!/usr/bin/env python3
"""Reference analytics layer; not a substitute for PipeGen/DeepStream."""
import argparse
import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

import cv2
import numpy as np
import yaml
import torch
from ultralytics import YOLO

from src.counter import VehicleCounter
from src.visualizer import Visualizer
from src.mqtt_publisher import MqttPublisher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)
LOG = logging.getLogger("traffic-analytics")


def load_config(path="config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle) or {}
    for key in ("model", "classes", "tracking", "counting", "display", "output"):
        if key not in config:
            raise ValueError(f"Missing required config section: {key}")
    return config


def choose_source_interactive() -> Tuple[str, str]:
    print("\nTRAFFIC ANALYTICS — INPUT SOURCE")
    print("1. Video file")
    print("2. USB webcam")
    print("3. RTSP stream")
    while True:
        choice = input("Choose 1/2/3: ").strip()
        if choice == "1":
            path = input("Video file path: ").strip().strip('"').strip("'")
            if Path(path).is_file():
                return "video", path
            print(f"File not found: {path}")
        elif choice == "2":
            return "webcam", input("Camera index [0]: ").strip() or "0"
        elif choice == "3":
            url = input("RTSP URL: ").strip()
            if url:
                return "rtsp", url
        else:
            print("Invalid choice.")


def open_capture(mode: str, source: str):
    if mode == "video":
        cap = cv2.VideoCapture(source)
    elif mode == "webcam":
        cap = cv2.VideoCapture(int(source))
    else:
        os.environ.setdefault(
            "OPENCV_FFMPEG_CAPTURE_OPTIONS", "rtsp_transport;tcp"
        )
        cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        cap.release()
        raise RuntimeError(f"Cannot open input source: {source}")
    return cap


def atomic_json_write(path: Path, payload: dict) -> None:
    """Write JSON through a temporary file to avoid partial snapshots."""
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    os.replace(temp_path, path)


def process(
    mode: str,
    source: str,
    config: dict,
    output_dir="output",
    display_override: Optional[bool] = None,
) -> None:
    model_cfg = config["model"]
    count_cfg = config["counting"]
    display_cfg = config["display"]
    output_cfg = config["output"]
    mqtt_cfg = config.get("mqtt", {})

    display_enabled = (
        display_override
        if display_override is not None
        else bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    )
    if display_override is True and not (
        os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
    ):
        raise RuntimeError(
            "--display was requested, but DISPLAY/WAYLAND_DISPLAY is unset. "
            "Run inside a graphical session or use --no-display."
        )

    device = model_cfg.get("device", "auto")
    if device == "auto":
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

    LOG.info("Loading model %s", model_cfg["name"])
    LOG.info("Inference device: %s", device)
    model = YOLO(model_cfg["name"])

    cap = open_capture(mode, source)
    writer = None
    mqtt = None
    preview_created = False
    frame_idx = 0
    start = time.time()

    try:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if width <= 0 or height <= 0:
            ok, first_frame = cap.read()
            if not ok:
                raise RuntimeError("Input opened but returned no valid frames.")
            height, width = first_frame.shape[:2]
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        reported_fps = cap.get(cv2.CAP_PROP_FPS)
        fps = reported_fps if reported_fps and reported_fps > 0 else float(
            output_cfg.get("fps_fallback", 25.0)
        )
        line_y = int(height * float(count_cfg.get("line_position", 0.55)))
        classes = list(config["classes"]["vehicle"])
        counter = VehicleCounter(
            line_y,
            classes,
            direction_up=count_cfg.get("direction_up", "UP"),
            direction_down=count_cfg.get("direction_down", "DOWN"),
        )
        visualizer = Visualizer(
            line_y,
            line_color=tuple(display_cfg.get("line_color", [255, 0, 0])),
            line_thickness=display_cfg.get("line_thickness", 3),
            box_thickness=display_cfg.get("box_thickness", 2),
            font_scale=display_cfg.get("font_scale", 0.55),
            text_bg_color=tuple(display_cfg.get("text_bg_color", [0, 0, 0])),
            show_ids=display_cfg.get("show_ids", True),
            show_centroids=display_cfg.get("show_centroids", True),
            show_counts=display_cfg.get("show_counts", True),
        )

        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        base = Path(source).stem if mode == "video" else mode
        video_path = out_dir / f"annotated_{base}_{timestamp}.mp4"
        json_path = out_dir / f"counts_{base}_{timestamp}.json"

        if output_cfg.get("save_annotated", True):
            codec = output_cfg.get("codec", "mp4v")
            if len(codec) != 4:
                raise ValueError("output.codec must contain exactly 4 characters.")
            fourcc = cv2.VideoWriter_fourcc(*codec)
            writer = cv2.VideoWriter(str(video_path), fourcc, fps, (width, height))
            if not writer.isOpened():
                writer.release()
                writer = None
                raise RuntimeError(
                    f"Cannot create output video: {video_path}. "
                    "Check the codec and OpenCV video-writer support."
                )
            LOG.info("Annotated video: %s", video_path)

        interval = max(1, int(output_cfg.get("json_every_n_frames", 30)))
        mqtt = MqttPublisher(
            enabled=mqtt_cfg.get("enabled", False),
            host=mqtt_cfg.get("host", "127.0.0.1"),
            port=mqtt_cfg.get("port", 1883),
            topic=mqtt_cfg.get("topic", output_cfg.get("mqtt_topic", "traffic/counts")),
            qos=mqtt_cfg.get("qos", 0),
            keepalive=mqtt_cfg.get("keepalive", 30),
        )

        LOG.info("Input: %s (%dx%d, %.2f FPS)", source, width, height, fps)
        if display_enabled:
            LOG.info("Preview enabled; press q to stop.")
        else:
            LOG.info("Headless mode: preview disabled.")

        names = model.names
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame_idx += 1

            results = model.track(
                frame,
                conf=float(model_cfg.get("confidence", 0.35)),
                iou=float(model_cfg.get("iou", 0.45)),
                persist=bool(config["tracking"].get("persist", True)),
                tracker=config["tracking"].get("tracker", "bytetrack.yaml"),
                verbose=False,
                device=device,
            )

            tracks = []
            if results and results[0].boxes is not None:
                boxes_obj = results[0].boxes
                if boxes_obj.id is not None:
                    boxes = boxes_obj.xyxy.cpu().numpy().astype(int)
                    ids = boxes_obj.id.cpu().numpy().astype(int)
                    class_ids = boxes_obj.cls.cpu().numpy().astype(int)
                    for box, track_id, class_id in zip(boxes, ids, class_ids):
                        class_name = names.get(int(class_id), str(class_id))
                        if class_name in classes:
                            tracks.append(
                                (int(track_id), tuple(box.tolist()), class_name)
                            )

            counter.update(tracks)
            annotated = visualizer.annotate(
                frame, tracks, counter.get_overlay_text()
            )

            if writer is not None:
                writer.write(annotated)

            if display_enabled:
                cv2.imshow("Traffic Analytics — press q to stop", annotated)
                preview_created = True
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            if frame_idx % interval == 0:
                snapshot = {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "frame": frame_idx,
                    "source": source,
                    "counts": counter.get_summary(),
                }
                atomic_json_write(json_path, snapshot)
                mqtt.publish(snapshot)

            if frame_idx % 50 == 0:
                elapsed = max(time.time() - start, 1e-6)
                LOG.info("Frames: %d | Processing FPS: %.2f", frame_idx, frame_idx / elapsed)

        final = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "source": source,
            "total_frames": frame_idx,
            "elapsed_seconds": round(time.time() - start, 3),
            "counts": counter.get_summary(),
        }
        atomic_json_write(json_path, final)
        mqtt.publish(final)

        LOG.info("Final counts:\n%s", json.dumps(final, indent=2))
        LOG.info("Final JSON: %s", json_path)
        if writer is not None:
            LOG.info("Annotated video: %s", video_path)
        LOG.info("Reminder: the official load-bearing pipeline must be generated by PipeGen.")

    finally:
        cap.release()
        if writer is not None:
            writer.release()
        if mqtt is not None:
            mqtt.close()
        if preview_created:
            cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(
        description="Traffic Analytics — reference analytics layer"
    )
    parser.add_argument("--source", type=str)
    parser.add_argument("--mode", choices=["video", "webcam", "rtsp"])
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--output-dir", default="output")
    display = parser.add_mutually_exclusive_group()
    display.add_argument("--display", action="store_true", help="Force GUI preview")
    display.add_argument("--no-display", action="store_true", help="Disable GUI preview")
    args = parser.parse_args()

    project_dir = Path(__file__).resolve().parent
    os.chdir(project_dir)
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = project_dir / config_path
    config = load_config(str(config_path))

    if args.source:
        source = args.source
        if args.mode:
            mode = args.mode
        elif Path(source).is_file():
            mode = "video"
        elif source.isdigit():
            mode = "webcam"
        else:
            mode = "rtsp"
    else:
        mode, source = choose_source_interactive()

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = project_dir / output_dir

    display_override = True if args.display else False if args.no_display else None
    process(mode, source, config, str(output_dir), display_override)


if __name__ == "__main__":
    main()
