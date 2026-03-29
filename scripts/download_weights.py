"""
Download DeepFace model weights from Hugging Face Hub.
Runs at container startup so models are ready before the app serves requests.
"""
import os
import sys

# ── CONFIG ───────────────────────────────────────────────────────────────────
HF_REPO_ID = "Hodfa71/deepface-weights"   # your HF model repo

# DeepFace looks for weights in $DEEPFACE_HOME/.deepface/weights
# In Docker we set DEEPFACE_HOME=/tmp → /tmp/.deepface/weights
DEEPFACE_HOME = os.environ.get("DEEPFACE_HOME", os.path.expanduser("~"))
WEIGHTS_DIR = os.path.join(DEEPFACE_HOME, ".deepface", "weights")

WEIGHT_FILES = [
    "age_model_weights.h5",
    "gender_model_weights.h5",
    "facial_expression_model_weights.h5",
    "race_model_single_batch.h5",
    "retinaface.h5",
    "vgg_face_weights.h5",
]

# Minimum file sizes to detect corrupted/incomplete downloads
MIN_SIZES = {
    "facial_expression_model_weights.h5": 5 * 1024 * 1024,   # ~5 MB
}
DEFAULT_MIN_SIZE = 40 * 1024 * 1024  # 40 MB for the rest
# ─────────────────────────────────────────────────────────────────────────────


def main():
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("Installing huggingface_hub...")
        os.system(f"{sys.executable} -m pip install huggingface_hub")
        from huggingface_hub import hf_hub_download

    os.makedirs(WEIGHTS_DIR, exist_ok=True)
    print(f"--- Vision.AI Weight Downloader (HF Hub) ---")
    print(f"Repo  : {HF_REPO_ID}")
    print(f"Target: {WEIGHTS_DIR}\n")

    token = os.environ.get("HF_TOKEN")  # optional for public repos

    for filename in WEIGHT_FILES:
        dest = os.path.join(WEIGHTS_DIR, filename)
        min_size = MIN_SIZES.get(filename, DEFAULT_MIN_SIZE)

        if os.path.exists(dest):
            if os.path.getsize(dest) >= min_size:
                print(f"[SKIP] {filename} already present "
                      f"({os.path.getsize(dest)/1024/1024:.1f} MB)")
                continue
            print(f"[RE-DOWNLOAD] {filename} looks incomplete, re-fetching...")

        print(f"[DOWNLOADING] {filename} from {HF_REPO_ID}...")
        try:
            hf_hub_download(
                repo_id=HF_REPO_ID,
                filename=filename,
                local_dir=WEIGHTS_DIR,
                token=token,
            )
            actual_size = os.path.getsize(dest) / 1024 / 1024
            print(f"[OK] {filename} saved ({actual_size:.1f} MB)")
        except Exception as exc:
            print(f"[ERROR] {filename}: {exc}")

    print("\nAll weights ready. Starting app...\n")


if __name__ == "__main__":
    main()
