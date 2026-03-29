"""
Called during Docker build to pre-download DeepFace AI models.
Models are baked into the image so no runtime download is needed.
"""
import os
import sys

os.environ["DEEPFACE_HOME"] = "/app"

try:
    from deepface import DeepFace

    for model_name in ["Age", "Gender", "Emotion", "Race"]:
        print(f"Downloading {model_name} model...", flush=True)
        DeepFace.build_model(model_name)
        print(f"  {model_name} ready.", flush=True)

    print("All models downloaded successfully.", flush=True)

except Exception as e:
    print(f"WARNING: Model download failed during build: {e}", flush=True)
    print("Models will be downloaded at first request.", flush=True)
    sys.exit(0)   # don't fail the build — app can still start
