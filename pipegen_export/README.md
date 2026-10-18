# PipeGen Export Folder

**Project:** SentinelEdge – Smart Traffic Analytics
**Team:** ZexTech team – 6e656f84
**Author:** Zaheer Rachakula
**Event:** CraftifAI Physical AI Hackathon, Track A (Perception)

This folder is reserved for the **PipeGen Export Project** output of SentinelEdge.

## Current status

| Item | Status |
|------|--------|
| PipeGen requirement text | Ready: [`../PIPEGEN_REQUIREMENT.md`](../PIPEGEN_REQUIREMENT.md) |
| PipeGen run on NVIDIA GPU | **Not done yet** |
| Pipeline IR graph | **Not available yet** |
| TensorRT compile / speed report | **Not available yet** |
| Exported PipeGen project | **Not available yet** |

### Why the export is not here yet

PipeGen could not run on the author's laptop. The machine does not meet the PipeGen prerequisites:

- NVIDIA GPU with driver 560.35 or higher
- Docker with NVIDIA Container Toolkit
- `socat`
- About 50 GB of free disk
- A graphical session

The PipeGen compatibility screenshot is in [`../deliverables/`](../deliverables/).

Rather than leave the project empty, the same pipeline was built and deployed on the **CPU path** (YOLOv8 + ByteTrack + line counting + MQTT + Streamlit dashboard). The files in this folder will not be filled with guessed or fake output.

## What the pipeline does (for PipeGen)

The requirement in `PIPEGEN_REQUIREMENT.md` describes this flow:

1. **Input:** video file, USB webcam or RTSP stream
2. **Detect** vehicles with YOLOv8 (car, truck, bus, motorcycle, bicycle)
3. **Track** each vehicle across frames with ByteTrack (stable IDs)
4. **Count** UP / DOWN crossings of a horizontal line, once per track ID, per class
5. **Output:** live display with boxes, IDs, line and count panel; annotated video; JSON counts; MQTT on `traffic/counts`

## How to produce the export (on a compatible GPU machine)

1. Check the driver:
   ```bash
   nvidia-smi
   ```
2. Install Docker, NVIDIA Container Toolkit and `socat`, then add your user to the `docker` group.
3. Download PipeGen v0.5.x from https://developer.craftifai.com/dashboard?tab=downloads and check it:
   ```bash
   pipegen --version
   ```
4. Run `pipegen`, sign in and create a new project.
5. Paste the full contents of `PIPEGEN_REQUIREMENT.md` into the **Requirement** stage.
6. Complete the stages: **Requirement → Pipeline IR → Model (TensorRT FP16/INT8) → Compiler → Run**.
7. Use **Export Project** and copy the exported folder into this directory.
8. Save screenshots to `../evidence/`:
   - `pipeline_ir.png` (Pipeline IR node graph)
   - `tensorrt_speed_report.png` (TensorRT speed report)
9. Commit and push:
   ```bash
   git add pipegen_export/ evidence/
   git commit -m "Add PipeGen export and TensorRT evidence"
   git push origin main
   ```

## Where to see the working system today

| What | Where |
|------|-------|
| Live demo (CPU path) | https://zaheer-traffic-analyzer.streamlit.app/ |
| Source code | https://github.com/ZAHEER-R/CraftifAIHackathon_CRA002 |
| Main README (setup, usage, previews) | [`../README.md`](../README.md) |
| CLI pipeline | [`../main.py`](../main.py) |
| Streamlit dashboard | [`../app.py`](../app.py) |
| Settings | [`../config.yaml`](../config.yaml) |

## How to run the working CPU version

```bash
python -m venv venv
# Windows: .\venv\Scripts\Activate.ps1      Linux/WSL: source venv/bin/activate
pip install -r requirements.txt
python main.py            # CLI (video / webcam / RTSP)
streamlit run app.py      # dashboard
```

Outputs are saved in `../output/` (`annotated_*.mp4`, `counts_*.json`).

---

*This folder will be updated with the real PipeGen export once a compatible NVIDIA GPU machine is available.*
