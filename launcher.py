"""AI News Radar — EXE 런처
PyInstaller로 빌드된 exe에서 Streamlit 서버를 직접 실행합니다.
"""
import sys
import os
import time
import threading
import socket
import multiprocessing

# PyInstaller 번들 경로 처리
if getattr(sys, 'frozen', False):
    # exe로 실행 중
    BUNDLE_DIR = sys._MEIPASS
    APP_DIR = os.path.dirname(sys.executable)
else:
    # 일반 Python으로 실행 중
    BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DIR = BUNDLE_DIR

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, BUNDLE_DIR)
sys.path.insert(0, APP_DIR)

# 환경변수 로드
from dotenv import load_dotenv
env_path = os.path.join(APP_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

APP_NAME = "AI News Radar"


def _find_free_port(preferred: int = 6601) -> int:
    """사용 가능한 포트 찾기"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", preferred))
        sock.close()
        return preferred
    except OSError:
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()
        return port


def _wait_for_server(port: int, timeout: int = 60) -> bool:
    """서버가 준비될 때까지 대기"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect(("127.0.0.1", port))
            sock.close()
            return True
        except (ConnectionRefusedError, OSError):
            time.sleep(0.5)
    return False


def _run_streamlit(port: int, app_script: str):
    """Streamlit 서버를 현재 프로세스에서 직접 실행"""
    # Streamlit 설정 덮어쓰기
    os.environ["STREAMLIT_SERVER_PORT"] = str(port)
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "127.0.0.1"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
    os.environ["STREAMLIT_THEME_BASE"] = "dark"
    os.environ["STREAMLIT_THEME_PRIMARY_COLOR"] = "#6366f1"
    os.environ["STREAMLIT_THEME_BACKGROUND_COLOR"] = "#09090b"
    os.environ["STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR"] = "#17171c"
    os.environ["STREAMLIT_THEME_TEXT_COLOR"] = "#ececef"

    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", app_script,
                "--server.port", str(port),
                "--server.headless", "true",
                "--server.address", "127.0.0.1"]
    stcli.main()


def _show_notification(message: str, title: str = APP_NAME):
    """Windows 네이티브 알림"""
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name=APP_NAME,
            timeout=5,
        )
    except Exception:
        pass


def _create_tray_icon(port: int, window_ref: list, stop_event: threading.Event):
    """시스템 트레이 아이콘 생성"""
    try:
        import pystray
        from PIL import Image, ImageDraw
    except ImportError:
        return None

    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=(79, 195, 247, 255))
    draw.ellipse([20, 20, 44, 44], fill=(13, 71, 161, 255))
    draw.ellipse([28, 28, 36, 36], fill=(255, 255, 255, 255))

    def on_open(icon, item):
        if window_ref and window_ref[0]:
            try:
                window_ref[0].show()
                window_ref[0].restore()
            except Exception:
                pass

    def on_quit(icon, item):
        icon.stop()
        stop_event.set()
        if window_ref and window_ref[0]:
            try:
                window_ref[0].destroy()
            except Exception:
                pass
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem(f"📡 {APP_NAME}", on_open, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("❌ 종료", on_quit),
    )

    icon = pystray.Icon(APP_NAME, img, APP_NAME, menu)
    return icon


def main():
    multiprocessing.freeze_support()

    port = _find_free_port(6601)

    # app.py 경로 결정
    app_script = os.path.join(APP_DIR, "app.py")
    if not os.path.exists(app_script):
        # 번들 내부에서 찾기
        app_script = os.path.join(BUNDLE_DIR, "app.py")

    if not os.path.exists(app_script):
        print(f"[Error] app.py를 찾을 수 없습니다: {app_script}")
        input("Press Enter to exit...")
        sys.exit(1)

    # data 디렉토리 확인/생성
    data_dir = os.path.join(APP_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)

    # preset_sources.json 복사 (번들에서 앱 디렉토리로)
    preset_src = os.path.join(BUNDLE_DIR, "data", "preset_sources.json")
    preset_dst = os.path.join(data_dir, "preset_sources.json")
    if os.path.exists(preset_src) and not os.path.exists(preset_dst):
        import shutil
        shutil.copy2(preset_src, preset_dst)

    print(f"[AI News Radar] 시작 중... (포트 {port})")
    print(f"[AI News Radar] app.py: {app_script}")

    # Streamlit 서버를 별도 스레드에서 실행
    st_thread = threading.Thread(
        target=_run_streamlit,
        args=(port, app_script),
        daemon=True
    )
    st_thread.start()

    print(f"[AI News Radar] 서버 대기 중... (http://127.0.0.1:{port})")
    if not _wait_for_server(port, timeout=60):
        print("[AI News Radar] 서버 시작 실패!")
        input("Press Enter to exit...")
        sys.exit(1)
    print("[AI News Radar] 서버 준비 완료!")

    # 트레이 + 윈도우
    stop_event = threading.Event()
    window_ref = [None]

    tray_icon = _create_tray_icon(port, window_ref, stop_event)
    if tray_icon:
        tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
        tray_thread.start()

    # pywebview 윈도우
    try:
        import webview

        def on_closing():
            if tray_icon:
                window_ref[0].hide()
                _show_notification("트레이로 최소화됨", APP_NAME)
                return False
            return True

        url = f"http://127.0.0.1:{port}"
        window = webview.create_window(
            APP_NAME,
            url,
            width=1400,
            height=900,
            min_size=(800, 600),
            confirm_close=True if tray_icon else False,
            text_select=True,
        )
        window_ref[0] = window

        if tray_icon:
            window.events.closing += on_closing

        _show_notification("AI News Radar 시작!", APP_NAME)
        webview.start(debug=False)

    except ImportError:
        print("[AI News Radar] pywebview 미설치 — 브라우저에서 열기")
        import webbrowser
        url = f"http://127.0.0.1:{port}"
        webbrowser.open(url)
        print(f"\n  📡 AI News Radar: {url}")
        print("  종료하려면 Ctrl+C를 누르세요.\n")
        try:
            while not stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    finally:
        if tray_icon:
            try:
                tray_icon.stop()
            except Exception:
                pass
        print("[AI News Radar] 종료")


if __name__ == "__main__":
    main()
