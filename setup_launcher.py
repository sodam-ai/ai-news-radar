"""AI News Radar — Setup & Launch EXE
This lightweight exe:
1. Finds Python on the system
2. Creates a .venv and installs dependencies
3. Launches Streamlit via subprocess
4. Opens the browser automatically

Does NOT bundle Streamlit — runs it natively for 100% stability.
"""
import sys
import os
import subprocess
import time
import socket
import webbrowser
import shutil
import ctypes

APP_NAME = "AI News Radar"
PORT = 6601
VENV_DIR = ".venv"
REQ_FILE = "requirements.txt"
ENV_FILE = ".env"
ENV_EXAMPLE = ".env.example"
APP_SCRIPT = "app.py"


def get_app_dir():
    """Get the directory where the exe/script is located."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def log(msg):
    print(f"  {msg}")


def set_console_title(title):
    try:
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    except Exception:
        pass


def find_python():
    """Find a usable Python 3 interpreter."""
    candidates = ["py -3", "python3", "python"]
    for cmd in candidates:
        try:
            parts = cmd.split()
            result = subprocess.run(
                parts + ["--version"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and "Python 3" in result.stdout:
                return cmd
        except Exception:
            continue
    return None


def find_free_port(preferred=6601):
    """Find an available port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", preferred))
        sock.close()
        return preferred
    except OSError:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()
        return port


def wait_for_server(port, timeout=120):
    """Wait until the server is responding."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect(("127.0.0.1", port))
            sock.close()
            return True
        except (ConnectionRefusedError, OSError, TimeoutError):
            time.sleep(1)
    return False


def run_cmd(cmd_str, cwd=None, show_output=False):
    """Run a shell command and return success status."""
    try:
        if show_output:
            result = subprocess.run(
                cmd_str, shell=True, cwd=cwd, timeout=600
            )
        else:
            result = subprocess.run(
                cmd_str, shell=True, cwd=cwd,
                capture_output=True, text=True, timeout=600
            )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def main():
    set_console_title(APP_NAME)
    app_dir = get_app_dir()
    os.chdir(app_dir)

    print()
    print("  =============================================")
    print(f"       {APP_NAME}")
    print("  =============================================")
    print()

    # --- Step 1: Find Python ---
    log("[1/5] Checking Python...")
    python_cmd = find_python()
    if not python_cmd:
        print()
        log("[ERROR] Python 3 is not installed!")
        print()
        log("Please install Python first:")
        log("  1. Go to https://python.org/downloads")
        log("  2. Download and install Python")
        log("  3. CHECK 'Add Python to PATH' during install!")
        log("  4. Then run this program again.")
        print()
        try:
            webbrowser.open("https://www.python.org/downloads/")
        except Exception:
            pass
        input("  Press Enter to exit...")
        sys.exit(1)
    log(f"  [OK] Python found")

    # --- Step 2: Create venv ---
    venv_python = os.path.join(VENV_DIR, "Scripts", "python.exe")
    venv_streamlit = os.path.join(VENV_DIR, "Scripts", "streamlit.exe")
    venv_pip = os.path.join(VENV_DIR, "Scripts", "pip.exe")

    if not os.path.exists(venv_python):
        log("[2/5] Creating virtual environment...")
        log("       (This is a one-time setup)")
        ok = run_cmd(f"{python_cmd} -m venv {VENV_DIR}")
        if not ok or not os.path.exists(venv_python):
            log("[ERROR] Failed to create virtual environment.")
            input("  Press Enter to exit...")
            sys.exit(1)
        log("       [OK] Virtual environment created!")
    else:
        log("[2/5] Virtual environment ready.")

    # --- Step 3: Install dependencies ---
    if not os.path.exists(venv_streamlit):
        log("[3/5] Installing dependencies...")
        log("       This takes 2-5 minutes on first run.")
        log("       Please wait...")
        print()
        ok = run_cmd(
            f'"{venv_pip}" install -r {REQ_FILE}',
            show_output=True
        )
        if not ok:
            log("[ERROR] Failed to install dependencies.")
            log("  Try deleting the .venv folder and running again.")
            input("  Press Enter to exit...")
            sys.exit(1)
        print()
        log("       [OK] All dependencies installed!")
    else:
        log("[3/5] Dependencies ready.")

    # --- Step 4: Setup .env ---
    if not os.path.exists(ENV_FILE):
        log("[4/5] Setting up API key...")
        if os.path.exists(ENV_EXAMPLE):
            shutil.copy2(ENV_EXAMPLE, ENV_FILE)
        else:
            with open(ENV_FILE, "w", encoding="utf-8") as f:
                f.write("GEMINI_API_KEY=your_api_key_here\n")
        print()
        log("  !! You need a free API key to use AI features !!")
        log("")
        log("  1. Get your key at: https://aistudio.google.com/apikey")
        log("  2. A text editor will open with the .env file")
        log("  3. Replace 'your_gemini_api_key_here' with your key")
        log("  4. Save the file (Ctrl+S) and close the editor")
        print()
        try:
            webbrowser.open("https://aistudio.google.com/apikey")
            time.sleep(2)
        except Exception:
            pass
        try:
            os.startfile(os.path.join(app_dir, ENV_FILE))
        except Exception:
            try:
                subprocess.run(["notepad.exe", ENV_FILE])
            except Exception:
                pass
        input("  After saving your API key, press Enter to continue...")
    else:
        log("[4/5] API key file ready.")

    # --- Step 5: Launch ---
    log("[5/5] Launching AI News Radar...")

    port = find_free_port(PORT)

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Start Streamlit as subprocess
    streamlit_cmd = [
        venv_python, "-m", "streamlit", "run", APP_SCRIPT,
        "--server.port", str(port),
        "--server.headless", "true",
        "--server.address", "127.0.0.1",
        "--theme.base", "dark",
        "--browser.gatherUsageStats", "false",
    ]

    try:
        proc = subprocess.Popen(
            streamlit_cmd,
            cwd=app_dir,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
    except Exception as e:
        log(f"[ERROR] Failed to start: {e}")
        input("  Press Enter to exit...")
        sys.exit(1)

    print()
    log(f"  Starting server on port {port}...")
    log("  Please wait...")

    if wait_for_server(port, timeout=120):
        url = f"http://localhost:{port}"
        print()
        print("  =============================================")
        print(f"   AI News Radar is running!")
        print(f"   Open: {url}")
        print("  =============================================")
        print()
        log("  Opening browser...")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        print()
        log("  Close this window to stop the app.")
        log("  Or press Ctrl+C.")
        print()

        try:
            proc.wait()
        except KeyboardInterrupt:
            log("  Shutting down...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
    else:
        log("[ERROR] Server failed to start within 2 minutes.")
        log("  Check if port 6601 is already in use.")
        proc.terminate()
        input("  Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    main()
