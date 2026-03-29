# VISION.AI - Hugging Face Spaces
FROM python:3.10-slim

# System dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV DEEPFACE_HOME=/app
ENV PORT=7860

COPY requirements.txt .

# Step 1: upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Step 2: install tensorflow-cpu first (largest package, isolated for visibility)
RUN pip install --no-cache-dir --timeout 180 --retries 5 tensorflow-cpu==2.13.0

# Step 3: install tf-keras (depends on tensorflow)
RUN pip install --no-cache-dir --timeout 60 tf-keras

# Step 4: install everything else
RUN pip install --no-cache-dir --timeout 120 --retries 3 \
    flask>=3.0.0 \
    flask-cors>=4.0.0 \
    opencv-python-headless>=4.8.0 \
    deepface>=0.0.86 \
    "numpy>=1.24.0,<2.0" \
    pillow>=10.0.0 \
    python-dotenv>=1.0.0 \
    gunicorn>=21.2.0 \
    "werkzeug>=3.0.0" \
    "huggingface_hub>=0.20.0"

# Copy only the build script, then download models
COPY scripts/build_models.py scripts/build_models.py
RUN python scripts/build_models.py

# Copy the rest of the application
COPY . .

EXPOSE 7860

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:7860", "--timeout", "300", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
