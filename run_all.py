import subprocess
import sys
import time
import os
import signal

# Paths to backend and frontend
BACKEND_PATH = os.path.join(os.getcwd(), "backend")
FRONTEND_PATH = os.path.join(os.getcwd(), "frontend")

# Start FastAPI backend
backend_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--reload"],
    cwd=BACKEND_PATH
)
print("Starting FastAPI backend...")

# Wait a few seconds for backend to start
time.sleep(3)

# Start Streamlit frontend
frontend_process = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "app.py"],
    cwd=FRONTEND_PATH
)
print("Starting Streamlit frontend...")

try:
    # Wait for both processes
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    print("\nStopping both backend and frontend...")
    backend_process.send_signal(signal.SIGINT)
    frontend_process.send_signal(signal.SIGINT)
