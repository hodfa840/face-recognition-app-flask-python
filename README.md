---
title: Vision AI Engine
emoji: 👁️‍🗨️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

## 📊 Biometric Case Study: Neural Occlusion Bypass
![Match Proof](app/static/demo/cv_match.png)
*Identity Confirmed across Hijab occlusion using clinical-grade pre-processing.*

A professional-grade, Flask-powered facial biometric engine capable of real-time clinical demographics analysis and cross-occlusion identity verification (e.g., matching across hijabs, glasses, and ages). 🚀✨

## 🔗 Live Deployment
**[▶ Launch Vision.AI Engine](https://hodfa71-vision-ai-engine.hf.space)**

> **Note:** Hosted on Hugging Face Spaces free tier. The first request may be slow (10–30 seconds) as the app wakes from sleep and loads AI model weights into memory. Subsequent requests are fast.

## 🌟 Key Features
- **Neural Vision HUD (Live Mode)**: Real-time 640x600 biometric scanner with clinical-grade sharpening and stabilization.
- **Occlusion-Resistant Matcher**: Proven to match identities even with significant changes in headgear (Hijab), eyewear, or lighting.
- **Deep Biometric Extraction**: Accurate gender, age range, ethnicity, and emotional state predictions.
- **Neural Stabilization Buffer**: Weighted voting system to eliminate AI 'flicker' in real-time feeds.
- **Privacy-First**: No images are stored permanently; all analysis is performed in volatile RAM/temp memory.


## 🛠️ Technology Stack
- **Engine**: [DeepFace](https://github.com/serengil/deepface) (VGG-Face, ArcFace, RetinaFace detector)
- **Backend**: Flask 3.0, TensorFlow 2.13+, OpenCV (Headless)
- **Frontend**: Vanilla HTML5/CSS3 (Glassmorphism), Font-Awesome 6
- **Stability**: Neural stabilization buffer with weighted voting across live frames

## 🎨 Local Setup & Launch
1. **Initialize Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Download ML Weights**:
   ```bash
   python scripts/download_weights.py
   ```
   This downloads all model weights into `~/.deepface/weights/`. **The app will not work without this step.**

   | Model | Size | Purpose |
   |-------|------|---------|
   | `vgg_face_weights.h5` | ~580 MB | Face recognition |
   | `age_model_weights.h5` | ~514 MB | Age estimation |
   | `gender_model_weights.h5` | ~514 MB | Gender classification |
   | `facial_expression_model_weights.h5` | ~5 MB | Emotion detection |
   | `race_model_single_batch.h5` | ~150 MB | Ethnicity classification |
   | `retinaface.h5` | ~145 MB | Face detection (accuracy-critical) |

   > **RetinaFace** is the face detector used by this app. It is significantly more accurate than basic OpenCV detection, especially for gender and age predictions. Downloaded from the [official DeepFace models repo](https://github.com/serengil/deepface_models/releases/tag/v1.0).

3. **Run Command Center**:
   ```bash
   python scripts/start_project.py
   ```
   *Visit: http://localhost:5000/analysis/live*

## 🚀 Live Hosting Options
DeepFace is a heavy-weight engine (~2.5GB RAM for weights). For recruiters to see this live, I recommend:
1. **[Hugging Face Spaces](https://huggingface.co/spaces)** (Free + Hardware accelerated): The gold standard for ML demos.
2. **[Render.com](https://render.com)** (Standard Instance): Good for standard web apps.
3. **Docker Deployment**: Each environment is containerized for seamless scaling.

---
*Created for a world-class Machine Learning Portfolio. Licensed under MIT.*
