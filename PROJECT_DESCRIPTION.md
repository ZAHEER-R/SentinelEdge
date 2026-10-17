# Project Description – Traffic Analytics Physical AI System

**Track:** A – PipeGen (Perception)
**Optional Bonuses targeted:** Edge Optimization + Closed Loop readiness
**Team / Author:** Zaheer Rachakula
**Hackathon:** CraftifAI Physical AI Hackathon – Embedded SF

---

## 1. Problem Statement

Cities and traffic authorities lack live, per-class vehicle counts at key road sections. Manual counting is slow and inaccurate. Existing camera systems usually only show video; they do not produce structured, actionable analytics that another system can act on in real time.

## 2. Chosen Track & Tool

- **Primary tool:** CraftifAI PipeGen (mandatory load-bearing component)
- **Track:** A – Perception
- We deliberately do **not** treat PipeGen as an afterthought. The entire vision pipeline (detection → tracking → counting line → actionable outputs) is defined and compiled through PipeGen’s five stages.

## 3. Solution Summary

A GPU-accelerated edge vision pipeline that:

1. Ingests a live camera or video stream.
2. Detects and tracks vehicles (car, truck, bus, motorcycle, bicycle).
3. Maintains a virtual counting line and produces directional (UP / DOWN) counts per class.
4. Emits three actionable outputs:
   - Live annotated display
   - Saved annotated video
   - JSON + MQTT feed of the current counts

This maps directly to the official suggested track:

> **4. Traffic and Crosswalk Analytics**
> Detection and line-crossing counts per class, with INT8 on a Jetson for a pole-mounted unit.

## 4. PipeGen Pipeline Overview

| Stage            | Content                                                                 |
|------------------|-------------------------------------------------------------------------|
| Requirement      | Natural-language description (see `PIPEGEN_REQUIREMENT.md`)             |
| Pipeline IR      | Node graph: source → detector → tracker → counting line → outputs       |
| Model            | YOLOv8 (or equivalent from CraftifAI catalog / Deep Search)             |
| Compiler         | TensorRT FP16 (and INT8 for Edge Optimization bonus)                    |
| Run              | DeepStream app with `run.sh`, live display + JSON + MQTT                |

## 5. Actionable Outputs

- **JSON file** written periodically with current counts
- **MQTT topic** `traffic/counts` – ready for a FirmGen ESP32/STM32 board to subscribe and trigger physical actions (Closed Loop bonus)
- Annotated RTSP / display stream

## 6. Hardware Target

- Primary: x86_64 Linux PC with NVIDIA GPU (driver ≥ 560.35)
- Edge Optimization bonus: NVIDIA Jetson (JetPack 6) with INT8 engine

## 7. Evidence Provided in This Repository

| Evidence                                      | Location                          |
|-----------------------------------------------|-----------------------------------|
| PipeGen natural-language requirement          | `PIPEGEN_REQUIREMENT.md`          |
| Pipeline IR node-graph screenshot             | `evidence/pipeline_ir.png`        |
| TensorRT speed / power report                 | `evidence/tensorrt_speed_report.png` |
| Live run screenshots / short demo video       | `evidence/`                       |
| Annotated output examples                     | `output/`                         |
| Source / reference counting logic             | `src/`                            |
| Full PipeGen export folder                    | `pipegen_export/` (after you run PipeGen) |

## 8. How to Reproduce

1. Install PipeGen v0.5.1 following the official Installation Guide.
2. Sign in with your CraftifAI account.
3. Create a new project and paste the requirement from `PIPEGEN_REQUIREMENT.md`.
4. Complete all five stages and export the project into `pipegen_export/`.
5. Run the generated `run.sh` on a supported NVIDIA machine.
6. Place the required screenshots into `evidence/`.

## 9. Closed-Loop Readiness (Bonus)

The MQTT topic `traffic/counts` is intentionally designed so a FirmGen firmware project can subscribe and drive LEDs, relays or motors when a count threshold is crossed.
