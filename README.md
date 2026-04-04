---
title: Vision AI Engine
emoji: 👁️‍🗨️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Vision AI Engine

Vision AI is a high-performance facial biometrics and analysis dashboard. It uses deep neural networks to provide real-time gender identification, age estimation, emotional spectrum analysis, and ethnicity classification directly from a webcam or image upload.

![Biometric Evaluation](image.png)

## Core Features
*   **Live Facial Scanning**: Real-time biometric HUD with neural stabilization for consistent tracking.
*   **Identity Verification**: High-precision face matching using deep similarity metrics (VGG-Face, ArcFace).
*   **Occlusion Handling**: Optimized performance for subjects with headgear (hijab), eyewear, or varying lighting conditions.
*   **Detailed Analytics**: Sub-model level breakdowns of emotions and demographic clusters.

## Installation and Setup

1.  **Environment Configuration**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Model Configuration**:
    The system requires pre-trained weights for the DeepFace engine. Download them using the following script:
    ```bash
    python scripts/download_weights.py
    ```

3.  **Launch the System**:
    ```bash
    python run.py
    ```
    View the dashboard locally at `http://localhost:5000`.

---
*Developed by hodfa840*
