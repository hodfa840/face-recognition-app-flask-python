import os
import subprocess
import sys

def main():
    print("--- Vision.AI Standard Setup & Launch ---")
    
    # 1. Detect environment
    project_root = os.getcwd()
    venv_python = os.path.join(project_root, "venv", "Scripts", "python.exe")
    
    if os.path.exists(venv_python):
        print(f"Detected Virtual Environment: {venv_python}")
        python_exe = venv_python
    else:
        print("Warning: No virtual environment detected. Using system Python.")
        python_exe = sys.executable
        
    # 2. Ensure basic requirements (checking if deepface exists first)
    try:
        subprocess.run([python_exe, "-c", "import deepface"], check=True, capture_output=True)
        print("Required packages (deepface) already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing dependencies from requirements.txt...")
        # Note: We use --no-deps or specific install if global pip is broken, 
        # but here we just try standard install first
        subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # 3. Check for weights
    print("\nChecking for ML weights...")
    scripts_dir = os.path.join(project_root, "scripts")
    download_script = os.path.join(scripts_dir, "download_weights.py")
    
    if os.path.exists(download_script):
        subprocess.run([python_exe, download_script])
    else:
        print(f"[ERROR] Found no download script at {download_script}")
    
    # 4. Launch the app
    print("\nLaunching Vision.AI Dashboard...")
    print("Point your browser to http://127.0.0.1:5000")
    print("Press CTRL+C to stop.")
    
    try:
        subprocess.run([python_exe, "run.py"])
    except KeyboardInterrupt:
        print("\nStopping...")

if __name__ == "__main__":
    main()
