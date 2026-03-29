"""
Called during Docker build to pre-download DeepFace AI models.
Tries Hugging Face Hub first (fast & reliable within HF infrastructure),
then falls back to DeepFace's built-in downloader (GitHub releases).
Models are baked into the image so no runtime download is needed.
"""
import os
import sys
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

# Use DEEPFACE_HOME from env (set in Dockerfile) or fallback to user home
DEEPFACE_HOME = os.environ.get("DEEPFACE_HOME", os.path.expanduser("~"))
WEIGHTS_DIR = os.path.join(DEEPFACE_HOME, ".deepface", "weights")
os.makedirs(WEIGHTS_DIR, exist_ok=True)

HF_REPO = "Hodfa71/deepface-weights"
MODEL_FILES = [
    "age_model_weights.h5",
    "gender_model_weights.h5",
    "facial_expression_model_weights.h5",
    "race_model_single_batch.h5",
    "retinaface.h5",
]


def try_hf_hub():
    """Download weights from Hodfa71/deepface-weights on Hugging Face Hub."""
    try:
        from huggingface_hub import hf_hub_download, list_repo_files
        # Check the repo exists and has files
        files = list(list_repo_files(HF_REPO))
        if not files:
            print(f"  HF repo {HF_REPO} is empty or not found.", flush=True)
            return False

        for filename in MODEL_FILES:
            dest = os.path.join(WEIGHTS_DIR, filename)
            if os.path.exists(dest):
                print(f"  {filename} already present, skipping.", flush=True)
                continue
            if filename not in files:
                print(f"  {filename} not in HF repo, skipping.", flush=True)
                continue
            print(f"  Downloading {filename} from HF Hub...", flush=True)
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    hf_hub_download,
                    repo_id=HF_REPO,
                    filename=filename,
                    local_dir=WEIGHTS_DIR,
                    local_dir_use_symlinks=False,
                )
                future.result(timeout=300)  # 5 minute cap per file
            print(f"  {filename} ready.", flush=True)
        return True
    except Exception as exc:
        print(f"  HF Hub download failed: {exc}", flush=True)
        return False


def try_deepface_build():
    """Download weights via DeepFace (from GitHub releases)."""
    try:
        from deepface import DeepFace
        for model_name in ["Age", "Gender", "Emotion", "Race"]:
            print(f"  Building {model_name} via DeepFace (GitHub)...", flush=True)
            DeepFace.build_model(model_name)
            print(f"  {model_name} ready.", flush=True)
        return True
    except Exception as exc:
        print(f"  DeepFace build failed: {exc}", flush=True)
        return False


print("=== Downloading AI model weights ===", flush=True)
print(f"Trying HF Hub ({HF_REPO})...", flush=True)
if try_hf_hub():
    print("=== HF Hub download successful ===", flush=True)
elif try_deepface_build():
    print("=== GitHub download successful ===", flush=True)
else:
    print("WARNING: All download attempts failed.", flush=True)
    print("Models will attempt to download on first request.", flush=True)
    sys.exit(0)
