"""
Upload local DeepFace model weights to your Hugging Face model repo.

Usage:
    pip install huggingface_hub
    python scripts/upload_weights_to_hf.py

You need to be logged in:
    huggingface-cli login
  OR set env var:
    set HF_TOKEN=hf_xxxxxxxxxxxx
"""
import os
import sys

try:
    from huggingface_hub import HfApi, create_repo
except ImportError:
    print("Installing huggingface_hub...")
    os.system(f"{sys.executable} -m pip install huggingface_hub")
    from huggingface_hub import HfApi, create_repo

# ── CONFIG ──────────────────────────────────────────────────────────────────
HF_REPO_ID = "Hodfa71/deepface-weights"   # your model repo on HF Hub
HF_REPO_TYPE = "model"

# Local weights directory (where DeepFace saves them)
LOCAL_WEIGHTS_DIR = os.path.join(os.path.expanduser("~"), ".deepface", "weights")

# The weight files to upload (must exist in LOCAL_WEIGHTS_DIR)
WEIGHT_FILES = [
    "age_model_weights.h5",
    "gender_model_weights.h5",
    "facial_expression_model_weights.h5",
    "race_model_single_batch.h5",
    "retinaface.h5",
    "vgg_face_weights.h5",
]
# ────────────────────────────────────────────────────────────────────────────


def main():
    token = os.environ.get("HF_TOKEN")

    api = HfApi(token=token)

    # Create the repo if it doesn't exist yet
    print(f"Creating/checking repo: {HF_REPO_ID}")
    try:
        create_repo(HF_REPO_ID, repo_type=HF_REPO_TYPE, exist_ok=True, token=token)
        print(f"  Repo ready: https://huggingface.co/{HF_REPO_ID}")
    except Exception as exc:
        print(f"  Warning: {exc}")

    # Upload each weight file
    for filename in WEIGHT_FILES:
        local_path = os.path.join(LOCAL_WEIGHTS_DIR, filename)
        if not os.path.exists(local_path):
            print(f"[SKIP] {filename} — not found at {local_path}")
            continue

        size_mb = os.path.getsize(local_path) / (1024 * 1024)
        print(f"[UPLOADING] {filename} ({size_mb:.1f} MB)...")
        try:
            api.upload_file(
                path_or_fileobj=local_path,
                path_in_repo=filename,
                repo_id=HF_REPO_ID,
                repo_type=HF_REPO_TYPE,
            )
            print(f"  [OK] {filename} uploaded.")
        except Exception as exc:
            print(f"  [ERROR] {filename}: {exc}")

    print("\nDone. Weights are at:")
    print(f"  https://huggingface.co/{HF_REPO_ID}")


if __name__ == "__main__":
    main()
