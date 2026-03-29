#!/usr/bin/env bash
# Hugging Face Spaces startup script
# Models are pre-baked into the Docker image — no download needed here.
exec gunicorn -w 1 -b 0.0.0.0:7860 --timeout 300 --access-logfile - --error-logfile - run:app
