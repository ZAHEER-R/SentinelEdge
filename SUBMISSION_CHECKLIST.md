# Official Submission Checklist – Track A (PipeGen)

Use this checklist before you fill the Google Form.

## Mandatory Requirements (from Problem Statement)

- [ ] **Full PipeGen Flow**
  Project went through all five stages: Requirement → Pipeline IR → Model → Compiler → Run.
  Not just a notebook or pure Python script.

- [ ] **TensorRT Engine**
  At least one model compiled to a TensorRT engine inside PipeGen.
  Speed report from PipeGen is captured and placed in `evidence/`.

- [ ] **Live Run**
  Pipeline runs live on a video file, USB camera, CSI camera or RTSP stream on an NVIDIA GPU machine or Jetson.

- [ ] **Actionable Output**
  Pipeline produces more than boxes on a screen: JSON file and/or MQTT feed with the counts.

- [ ] **Deep Integration**
  PipeGen is the load-bearing core of the product (the DeepStream / TensorRT pipeline is what actually runs).

## What to Submit (from Problem Statement)

- [ ] **Working Prototype**
  Live demo ready on hardware at the venue (or screen recording if remote).

- [ ] **Source Code**
  This GitHub repository, including the PipeGen export folder under `pipegen_export/`.

- [ ] **Project Description**
  `PROJECT_DESCRIPTION.md` (problem, track, pipeline details, bonuses).

- [ ] **Evidence (Track A)**
  - Screenshot of the Pipeline IR node graph → `evidence/pipeline_ir.png`
  - TensorRT speed report from PipeGen → `evidence/tensorrt_speed_report.png`
  - Live run proof (screenshot or short video) → `evidence/`

- [ ] **Pitch Deck / Video** (optional but recommended)

## Bonus Items (if you are going for them)

- [ ] **Edge Optimization**
  INT8 engine or Jetson deployment + speed/power/accuracy numbers from PipeGen reports.

- [ ] **Closed Loop**
  MQTT counts are consumed by a FirmGen board that performs a physical action.

## Final Submission Links

- PipeGen form: https://forms.gle/eJyeCKCG2UH757QZ8
- Sign-up / downloads: https://developer.craftifai.com/dashboard?tab=downloads
- Questions: #community-support on Discord

## Files that must exist in the repository before you push

```
traffic-analytics-pipegen/
├── README.md
├── PROJECT_DESCRIPTION.md
├── PIPEGEN_REQUIREMENT.md
├── SUBMISSION_CHECKLIST.md
├── requirements.txt
├── config.yaml
├── main.py                    # reference / fallback analytics layer
├── src/
├── evidence/                  # ← put the two mandatory screenshots here
│   ├── pipeline_ir.png
│   └── tensorrt_speed_report.png
├── pipegen_export/            # ← copy the entire folder PipeGen generates here
├── output/
└── docs/
```
