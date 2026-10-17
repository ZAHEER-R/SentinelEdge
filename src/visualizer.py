"""OpenCV overlay renderer for traffic analytics."""
import cv2


class Visualizer:
    def __init__(
        self,
        line_y,
        line_color=(255, 0, 0),
        line_thickness=3,
        box_thickness=2,
        font_scale=0.55,
        text_bg_color=(0, 0, 0),
        show_ids=True,
        show_centroids=True,
        show_counts=True,
    ):
        self.line_y = int(line_y)
        self.line_color = tuple(line_color)
        self.line_thickness = int(line_thickness)
        self.box_thickness = int(box_thickness)
        self.font_scale = float(font_scale)
        self.text_bg_color = tuple(text_bg_color)
        self.show_ids = bool(show_ids)
        self.show_centroids = bool(show_centroids)
        self.show_counts = bool(show_counts)

    def draw_line(self, frame):
        cv2.line(
            frame, (0, self.line_y),
            (frame.shape[1] - 1, self.line_y),
            self.line_color, self.line_thickness,
        )

    def draw_tracks(self, frame, tracks):
        for track_id, box, class_name in tracks:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(
                frame, (x1, y1), (x2, y2),
                (0, 255, 0), self.box_thickness,
            )

            if self.show_ids:
                label = f"{class_name} ID:{track_id}"
                text_y = max(18, y1 - 7)
                cv2.putText(
                    frame, label, (x1, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, self.font_scale,
                    (0, 255, 0), 2, cv2.LINE_AA,
                )

            if self.show_centroids:
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                cv2.circle(frame, (cx, cy), 4, (0, 255, 255), -1)

    def draw_counts(self, frame, overlay_lines):
        if not self.show_counts:
            return

        font = cv2.FONT_HERSHEY_SIMPLEX
        line_height = max(20, int(24 * self.font_scale / 0.55))
        padding = 8
        panel_width = min(
            frame.shape[1] - 8,
            max(
                (cv2.getTextSize(s, font, self.font_scale, 1)[0][0]
                 for s in overlay_lines),
                default=120,
            ) + 2 * padding,
        )
        panel_height = len(overlay_lines) * line_height + 2 * padding

        overlay = frame.copy()
        cv2.rectangle(
            overlay, (5, 5),
            (5 + panel_width, 5 + panel_height),
            self.text_bg_color, -1,
        )
        cv2.addWeighted(overlay, 0.72, frame, 0.28, 0, frame)

        y = 5 + padding + line_height - 5
        for line in overlay_lines:
            cv2.putText(
                frame, line, (5 + padding, y),
                font, self.font_scale, (255, 255, 255),
                1, cv2.LINE_AA,
            )
            y += line_height

    def annotate(self, frame, tracks, overlay_lines):
        output = frame.copy()
        self.draw_line(output)
        self.draw_tracks(output, tracks)
        self.draw_counts(output, overlay_lines)
        return output
