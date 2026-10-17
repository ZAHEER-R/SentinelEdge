# Step-by-Step Guide: From This Folder → Working Pipeline → GitHub → Form Submission

This guide is written so you can follow it in order and also answer the official **PipeGen Feedback Form** honestly.

---

## PHASE 0 – What you already have (this repository)

You are starting from:

```
traffic-analytics-pipegen/
├── README.md
├── PROJECT_DESCRIPTION.md
├── PIPEGEN_REQUIREMENT.md          ← you will paste this into PipeGen
├── SUBMISSION_CHECKLIST.md
├── main.py + src/                  ← reference counting layer only
├── evidence/                       ← put screenshots here later
├── pipegen_export/                 ← put PipeGen export here later
└── docs/
```

**Important:**
The Python code in `main.py` is **only a reference**.
Judges require the real pipeline to be built **inside PipeGen**.

---

## PHASE 1 – Machine Setup (answers form question: “What did you run PipeGen on?”)

### 1.1 Choose your machine

Preferred answers on the form:

- **An x86-64 Linux PC with an NVIDIA GPU** (best)
- **An NVIDIA Jetson** (also accepted)

You need:

- NVIDIA GPU + driver **560.35.03 or newer**
- Docker
- NVIDIA Container Toolkit
- socat
- Your user in the `docker` group
- Graphical X session
- Free disk space (~50 GB on x86_64)

### 1.2 Install prerequisites (Ubuntu x86_64 example)

```bash
# If the organizers gave you the script:
chmod +x pipegen_prerequisites_ubuntu_x86.sh
./pipegen_prerequisites_ubuntu_x86.sh

# Then log out and log back in (or run):
newgrp docker
```

Manual alternative (if no script):

```bash
# Docker
# follow https://docs.docker.com/engine/install/

# NVIDIA Container Toolkit
# follow https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

sudo apt install socat
sudo usermod -aG docker $USER
newgrp docker
```

### 1.3 Install PipeGen itself

1. Go to: https://developer.craftifai.com/dashboard?tab=downloads
2. Sign in with your CraftifAI account (the one you registered for the hackathon).
3. Download and install **PipeGen v0.5.1** (or the version the organizers specify).
4. Verify:

```bash
pipegen --version
# expected: 0.5.1 (or the required version)
```

**Form tip:**
If this step fails → you will later tick “Could not get PipeGen running” or “Installation and first start”.

---

## PHASE 2 – Create the pipeline inside PipeGen (core of Track A)

### 2.1 Start PipeGen and sign in

```bash
pipegen
```

Sign in with the same CraftifAI account.

### 2.2 Paste the Requirement (answers “Where did your model or code come from?”)

Open the file in this repo:

```
PIPEGEN_REQUIREMENT.md
```

Copy the entire requirement text (the block starting with “Build a real-time traffic analytics vision pipeline…”) and paste it into the **Requirement** stage cards in PipeGen.

Then click **Generate PIR** (or the equivalent button).

**Form answers you can use later:**

- Model/code source: **Catalog** (and/or Deep Search if PipeGen pulls a model that way)
- Input you plan to use: Sample video **or** My own video **or** USB camera **or** RTSP

### 2.3 Go through all five stages

You must complete:

1. **Requirement** → Generate Pipeline IR
2. **Pipeline IR** → node graph (source → detect → track → count → outputs)
3. **Model** → inspect, compile to TensorRT, look at the speed report
4. **Compiler** → Compile Pipeline
5. **Run** → get video on screen with results

**Target on the form:**
“Video on screen with results, and I built on top of it”

### 2.4 Capture mandatory evidence while it is fresh

While the pipeline is running or after it compiles:

1. Screenshot the **Pipeline IR node graph**
   → save as `evidence/pipeline_ir.png`

2. Screenshot the **TensorRT speed / power / accuracy report**
   → save as `evidence/tensorrt_speed_report.png`

3. (Optional but strong) Record a short screen video of the live run.

### 2.5 Export the project

In PipeGen use **Export Project**.
Copy the entire exported folder into:

```
pipegen_export/
```

This is what proves PipeGen was the load-bearing tool.

---

## PHASE 3 – Make the actionable outputs clear (JSON + MQTT)

PipeGen should already produce live display + saved video.
Make sure the requirement you pasted also asked for:

- JSON metadata with UP/DOWN counts
- MQTT topic `traffic/counts`

If PipeGen did not emit MQTT automatically, you can note in the project description that the JSON counts are the actionable feed and that MQTT is prepared for Closed-Loop.

The reference Python code in `main.py` already writes a JSON file — you can show it as the analytics layer sitting on top of the PipeGen pipeline.

---

## PHASE 4 – Push everything to GitHub

### 4.1 Initialise and push

```bash
cd traffic-analytics-pipegen

git init
git add .
git commit -m "Track A PipeGen submission – Traffic Analytics with directional counts"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your real values.

### 4.2 Final check of the repository

Your GitHub repo should contain at minimum:

- `README.md`
- `PROJECT_DESCRIPTION.md`
- `PIPEGEN_REQUIREMENT.md`
- `SUBMISSION_CHECKLIST.md`
- `evidence/pipeline_ir.png`
- `evidence/tensorrt_speed_report.png`
- `pipegen_export/` (the real export from PipeGen)
- `src/` and `main.py` (reference layer)

---

## PHASE 5 – Submit the official forms

### 5.1 Project submission form (this one scores you)

- PipeGen track form: https://forms.gle/eJyeCKCG2UH757QZ8
- Paste your GitHub repository link
- Mention Track A – PipeGen
- Mention any bonus you are going for (Edge Optimization / Closed Loop readiness)

### 5.2 Feedback form (does **not** affect score, but is required)

The form you attached says:

> “Your project is only scored if this form has been submitted.”

Fill it while the session is still fresh. Suggested honest answers based on a successful run:

| Form question | Suggested answer if everything worked |
|---------------|---------------------------------------|
| How much edge AI pipeline work before? | This is my first time **or** I have built a few |
| What did you run PipeGen on? | An x86-64 Linux PC with an NVIDIA GPU |
| Where did your model or code come from? | Catalog (and Deep Search if used) |
| What input did you use? | Sample video / My own video / USB camera / RTSP |
| How far did you get? | Video on screen with results, and I built on top of it |
| About how long to video on screen? | 30–60 minutes or 1–2 hours (be honest) |
| Did you have to work outside PipeGen? | Tick what is true (terminal commands, editing files, etc.) |
| Overall rating | Your real opinion (1–5) |
| Would you use PipeGen again? | Yes / Probably / No |

Be blunt — the form explicitly says judges never see it.

---

## PHASE 6 – After both forms are submitted

1. Keep the live demo ready (video file or camera) for the venue.
2. Have the two evidence screenshots and the GitHub link open.
3. If you also want the Closed-Loop bonus later, a FirmGen board can subscribe to `traffic/counts`.

---

## Quick Reference – Order of Operations

```
1. Install prerequisites + PipeGen
2. pipegen --version   (confirm it works)
3. Paste PIPEGEN_REQUIREMENT.md into PipeGen
4. Complete all 5 stages → get video on screen
5. Take Pipeline IR + TensorRT screenshots → evidence/
6. Export project → pipegen_export/
7. git push to GitHub
8. Submit project form (forms.gle/...)
9. Submit feedback form (the one you attached)
10. Demo at the venue
```

---

## If something fails

- Note the exact stage (Requirement / Pipeline IR / Model / Compiler / Run)
- Note the version: `pipegen --version`
- Take a screenshot of the error
- You can still answer the feedback form honestly (“Stuck in the Model stage”, etc.)
- Ask in `#community-support` on Discord or at the hardware desk

You now have a complete, form-aligned path from this root folder all the way to a valid Track A submission.
