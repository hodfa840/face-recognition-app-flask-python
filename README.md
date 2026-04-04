---
title: Vision AI Engine
emoji: 👁️‍🗨️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Vision AI Engine

A real-time facial biometrics analysis and verification system powered by deep learning models.

![Biometric Match Evaluation](image.png)

## Key Features
- **Real-time Live View**: Direct webcam integration with real-time biometric tracking (Age, Gender, Emotion, Ethnicity).
- **Occlusion-Resistant Matching**: Face verification system that matches identities across headgear, glasses, and viewpoint changes.
- **High-Precision Analysis**: Multi-model backend using RetinaFace, VGG-Face, and ArcFace for depth analysis.

## Local Installation
1. **Clone & Setup**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. **Download Weights**:
   ```bash
   python scripts/download_weights.py
   ```
3. **Launch Engine**:
   ```bash
   python scripts/start_project.py
   ```
