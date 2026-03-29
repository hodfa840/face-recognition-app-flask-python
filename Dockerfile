# VISION.AI - Hugging Face Spaces
# Use tensorflow base image - tensorflow pre-installed, no 300MB download
FROM tensorflow/tensorflow:2.15.0

ENV DEEPFACE_HOME=/home/user
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# System dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Setup non-root user
RUN useradd -m -u 1000 user
USER user
WORKDIR /home/user/app
ENV PATH="/home/user/.local/bin:${PATH}"

RUN mkdir -p /home/user/.deepface/weights \
    && mkdir -p /home/user/app/static/uploads

# Install remaining dependencies (no tensorflow here - already in base image)
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download model weights from HF Hub
COPY --chown=user:user scripts/build_models.py scripts/build_models.py
RUN python scripts/build_models.py

# Copy application
COPY --chown=user:user . .

EXPOSE 7860
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:7860", "--timeout", "300", "--access-logfile", "-", "--error-logfile", "-", "run:app"]
