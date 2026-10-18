# Traffic Analytics – PipeGen Physical AI System

**Track A – Perception (CraftifAI PipeGen)**
**Theme:** Building Physical AI Systems That See, Decide and Act

> Official suggested problem: **Traffic and Crosswalk Analytics**
> Detection + line-crossing counts per class, ready for MQTT / Closed-Loop.

---

## Quick Links

| Document | Purpose |
|----------|---------|
| **[docs/STEP_BY_STEP_GUIDE.md](docs/STEP_BY_STEP_GUIDE.md)** | **Full path: setup → PipeGen → GitHub → both forms** |
| [PROJECT_DESCRIPTION.md](PROJECT_DESCRIPTION.md) | Full problem + solution write-up for judges |
| [PIPEGEN_REQUIREMENT.md](PIPEGEN_REQUIREMENT.md) | Exact text to paste into PipeGen |
| [SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md) | Official mandatory checklist |
| [docs/HOW_TO_RUN.md](docs/HOW_TO_RUN.md) | How to run the reference analytics layer |

---

## What This Repository Contains

This repository currently contains a CPU-compatible traffic analytics reference pipeline and a Streamlit dashboard. The PipeGen-generated TensorRT/DeepStream pipeline, export, and benchmark evidence are still pending; this is not yet a complete PipeGen submission.

1. **PipeGen integration — pending**
   The intended final system uses CraftifAI PipeGen to generate a TensorRT + DeepStream application. The current working implementation is the CPU-compatible Python reference pipeline; PipeGen compilation, export, and TensorRT benchmarking have not yet been verified.

2. **Actionable outputs**
   - Live annotated display
   - Saved annotated video
   - JSON counts file
   - MQTT topic `traffic/counts` (ready for FirmGen Closed-Loop bonus)

3. **Reference / fallback analytics layer** (`src/` + `main.py`)
   A clean Python implementation of the same counting logic that can be used for rapid prototyping or as a post-processing node. It is **not** a substitute for the PipeGen pipeline.

4. **Evidence folder**
   Placeholders for the two mandatory screenshots judges expect:
   - Pipeline IR node graph
   - TensorRT speed report from PipeGen

---

## How to Use This Repo for Submission

### Step 1 – Install PipeGen (mandatory)

Follow the official **PipeGen Installation Guide** (v0.5.x):

- NVIDIA GPU + driver ≥ 560.35
- Docker + NVIDIA Container Toolkit
- socat
- User in `docker` group
- Graphical X session

Then install PipeGen itself from the CraftifAI developer portal and confirm:

```bash
pipegen --version
# should print 0.5.1 (or the version required by the organizers)
```

### Step 2 – Create the pipeline inside PipeGen

1. Sign in at https://developer.craftifai.com
2. Start a new PipeGen project
3. Paste the full requirement from **`PIPEGEN_REQUIREMENT.md`**
4. Complete all five stages
5. Compile at least one model to TensorRT (FP16 or INT8)
6. Run live on a video file / USB camera / RTSP
7. Export the entire project folder → copy it into `pipegen_export/`

### Step 3 – Capture evidence

Take screenshots of:

- The Pipeline IR node graph → save as `evidence/pipeline_ir.png`
- The TensorRT speed / power / accuracy report → save as `evidence/tensorrt_speed_report.png`

### Step 4 – Push and submit

```bash
git add .
git commit -m "Track A PipeGen submission – Traffic Analytics"
git push
```

Then fill the official form:
https://forms.gle/eJyeCKCG2UH757QZ8

---

## Repository Layout

```
traffic-analytics-pipegen/
├── README.md
├── PROJECT_DESCRIPTION.md      ← for judges
├── PIPEGEN_REQUIREMENT.md      ← paste this into PipeGen
├── SUBMISSION_CHECKLIST.md
├── requirements.txt
├── config.yaml
├── main.py                     ← reference counting layer
├── src/
│   ├── counter.py
│   └── visualizer.py
├── evidence/                   ← mandatory screenshots go here
├── pipegen_export/             ← full PipeGen export goes here
├── output/
├── assets/
└── docs/
```

---

## Mapping to Official Judging Criteria

| Criterion                        | How we address it                                      |
|----------------------------------|--------------------------------------------------------|
| Tool is load-bearing             | PipeGen generates the actual TensorRT + DeepStream app |
| Works live on hardware           | USB / CSI / RTSP / video on NVIDIA GPU or Jetson       |
| Actionable output                | JSON + MQTT counts                                     |
| Evidence of full flow            | Pipeline IR + TensorRT report in `evidence/`           |
| Edge Optimization (bonus)        | INT8 / Jetson path prepared in the requirement         |
| Closed Loop readiness (bonus)    | MQTT topic designed for FirmGen consumption            |

---

## Author

Zaheer Rachakula
CraftifAI Physical AI Hackathon – Track A
