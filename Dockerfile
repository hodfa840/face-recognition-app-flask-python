# VISION.AI - Hugging Face Spaces (Optimized)
FROM python:3.10-slim

# Set environment variables for non-root user
ENV DEEPFACE_HOME=/home/user
ENV MPLCONFIGDIR=/home/user/.matplotlib
ENV HF_HOME=/home/user/.cache/huggingface
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Install system dependencies for OpenCV and DeepFace
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Setup non-root user (Standard for Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
WORKDIR /home/user/app

# Set PATH for the new user
ENV PATH="/home/user/.local/bin:${PATH}"

# Prepare directories with correct permissions (Hugging Face /home/user is writable)
RUN mkdir -p /home/user/.deepface/weights \
    && mkdir -p /home/user/app/static/uploads

# Install core dependencies first (TensorFlow is the largest)
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir tensorflow-cpu==2.15.1 \
    && pip install --no-cache-dir -r requirements.txt

# Pre-download models during BUILD phase (Ensures runtime stability)
COPY --chown=user:user scripts/build_models.py scripts/build_models.py
RUN python scripts/build_models.py

# Copy the rest of the application
COPY --chown=user:user . .

# Ensure the upload folder is definitely writable by the app
RUN chmod 777 /home/user/app/static/uploads

EXPOSE 7860

# CMD to start the Gunicorn server
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:7860", "--timeout", "300", "run:app"]
