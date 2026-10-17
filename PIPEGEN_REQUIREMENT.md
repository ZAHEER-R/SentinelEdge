# PipeGen Natural Language Requirement (Paste this into PipeGen)

**Use this exact text (or very close) when you start a new project inside PipeGen.**

---

## Requirement Text for PipeGen

```
Build a real-time traffic analytics vision pipeline that runs on an NVIDIA GPU or Jetson.

Input: USB camera, CSI camera, video file, or RTSP stream of a road / highway.

Tasks:
1. Detect vehicles of classes: car, truck, bus, motorcycle, bicycle.
2. Track each vehicle across frames with unique IDs.
3. Draw a virtual horizontal counting line across the middle of the frame.
4. Count vehicles that cross the line in both directions (UP and DOWN) separately for each class.
5. Overlay on every frame:
   - Green bounding boxes with class name + track ID
   - Blue counting line
   - Top-left live count panel showing:
     UP Cars, DOWN Cars, UP Trucks, DOWN Trucks, UP Buses, DOWN Buses, UP Motorcycles, DOWN Motorcycles

Outputs (actionable):
- Live annotated display
- Annotated MP4 video saved to disk
- JSON metadata file written every N frames with the current UP/DOWN counts
- MQTT topic "traffic/counts" publishing the same JSON so another system (or FirmGen board) can act on it

Precision: Compile at least one model to TensorRT (FP16 preferred, INT8 if possible for Edge Optimization bonus).
Target platform: x86_64 NVIDIA GPU or Jetson with JetPack 6.
```

---

## Why this requirement satisfies the mandatory checklist

| Mandatory Item              | How this requirement covers it                          |
|-----------------------------|---------------------------------------------------------|
| Full PipeGen 5-stage flow   | You will go through Requirement → IR → Model → Compiler → Run |
| TensorRT engine             | Explicitly requests TensorRT compilation + speed report |
| Live Run                    | USB / CSI / RTSP / video file                           |
| Actionable Output           | JSON file + MQTT topic (not just boxes on screen)       |
| Edge Optimization (bonus)   | Requests INT8 / Jetson                                  |
| Closed Loop (bonus)         | MQTT topic ready for FirmGen to consume                 |

---

## After PipeGen generates the project

1. Keep the generated DeepStream app / run.sh as the core perception engine.
2. The Python counting logic in `src/` can be used as reference or as a post-processing node if PipeGen does not emit directional counts natively.
3. Export the full PipeGen project folder into `pipegen_export/` before submission.
4. Take screenshots of:
   - Pipeline IR node graph
   - TensorRT speed / power / accuracy report
   and place them in the `evidence/` folder.
