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

# Tell DeepFace where to store models (baked into the image at /app/.deepface/weights)
ENV DEEPFACE_HOME=/app
ENV PORT=7860

# Install Python dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy only the build script, then download models
# (kept in a separate layer so code changes don't re-download models)
COPY scripts/build_models.py scripts/build_models.py
RUN python scripts/build_models.py

# Copy the rest of the application
COPY . .

EXPOSE 7860

# 1 worker = 1 copy of models in RAM, no OOM
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:7860", "--timeout", "300", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
