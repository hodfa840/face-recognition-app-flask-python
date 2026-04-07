---
title: Vision AI Engine
emoji: 👁️‍🗨️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# 👁️ Vision AI Engine

**A professional-grade facial biometrics and analysis platform powered by deep learning.**

Vision AI is a high-performance facial biometrics dashboard delivering real-time analysis of gender identification, age estimation, emotional spectrum analysis, and ethnicity classification. Built with state-of-the-art neural networks, it processes both live webcam feeds and uploaded images with exceptional accuracy.

![Biometric Evaluation](https://raw.githubusercontent.com/hodfa840/face-recognition-app-flask-python/main/image.png)

### 🎯 [Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/Hodfa71/vision-ai-engine)
*Try the Vision AI Engine in action with real-time facial analysis — no installation required.*

## ✨ Core Features

- **🎬 Live Facial Scanning** — Real-time biometric HUD with neural stabilization for consistent tracking across all poses and lighting conditions.
- **🔐 Identity Verification** — High-precision face matching using deep similarity metrics (VGG-Face, ArcFace) with sub-second response times.
- **🛡️ Occlusion Handling** — Optimized performance for subjects with headgear (hijab), eyewear, masks, or varying lighting conditions.
- **📊 Detailed Analytics** — Sub-model level breakdowns with demographic clustering, emotion spectrum analysis, and confidence metrics.

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Webcam or image input capability
- 4GB+ RAM (8GB+ recommended for optimal performance)

### Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/hodfa840/face-recognition-app-flask-python.git
   cd face-recognition-app-flask-python
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Pre-trained Models**
   ```bash
   python scripts/download_weights.py
   ```

5. **Launch the Application**
   ```bash
   python run.py
   ```
   Access the dashboard at **`http://localhost:5000`**

---

## 👤 Contributors

**Developed and maintained by:** [hodfa840](https://github.com/hodfa840)  
**Contact:** hodfa840@student.liu.se

---

*Vision AI Engine — Professional Facial Biometrics Platform*
