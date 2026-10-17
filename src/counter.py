"""Directional vehicle line-crossing counter."""
from collections import defaultdict
from typing import Dict, List, Tuple


class VehicleCounter:
    VEHICLE_CLASSES = ("car", "truck", "bus", "motorcycle", "bicycle")

    def __init__(
        self,
        line_y: int,
        vehicle_classes=None,
        direction_up: str = "UP",
        direction_down: str = "DOWN",
    ):
        self.line_y = int(line_y)
        self.vehicle_classes = list(vehicle_classes or self.VEHICLE_CLASSES)
        self.direction_up = direction_up
        self.direction_down = direction_down

        self.counts = {
            direction: {name: 0 for name in self.vehicle_classes}
            for direction in (direction_up, direction_down)
        }
        self.previous_y = {}
        self.track_class = {}
        self.counted_ids = set()
        self.total_crossings = 0

    def update(self, tracks: List[Tuple[int, tuple, str]]) -> None:
        for track_id, box, class_name in tracks:
            if class_name not in self.vehicle_classes:
                continue

            x1, y1, x2, y2 = box
            center_y = (int(y1) + int(y2)) // 2
            track_id = int(track_id)

            # Keep the first recognized class for a track to avoid
            # class flicker causing inconsistent attribution.
            self.track_class.setdefault(track_id, class_name)

            previous = self.previous_y.get(track_id)
            self.previous_y[track_id] = center_y

            if previous is None or track_id in self.counted_ids:
                continue

            direction = None
            if previous > self.line_y and center_y <= self.line_y:
                direction = self.direction_up
            elif previous < self.line_y and center_y >= self.line_y:
                direction = self.direction_down

            if direction is not None:
                stable_class = self.track_class[track_id]
                self.counts[direction][stable_class] += 1
                self.counted_ids.add(track_id)
                self.total_crossings += 1

    def get_summary(self) -> Dict:
        result = {
            direction: dict(class_counts)
            for direction, class_counts in self.counts.items()
        }
        result["total_crossings"] = self.total_crossings
        return result

    def get_overlay_text(self) -> List[str]:
        lines = []
        for class_name in self.vehicle_classes:
            label = class_name.title() + "s"
            if class_name == "bus":
                label = "Buses"
            elif class_name == "bicycle":
                label = "Bicycles"
            elif class_name == "motorcycle":
                label = "Motorcycles"

            lines.append(
                f"{self.direction_up} {label}: "
                f"{self.counts[self.direction_up][class_name]}"
            )
            lines.append(
                f"{self.direction_down} {label}: "
                f"{self.counts[self.direction_down][class_name]}"
            )
        return lines
