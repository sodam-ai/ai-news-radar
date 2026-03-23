"""AI News Radar — 데스크톱 앱 (pywebview + 시스템 트레이)

사용법:
  python desktop.py             # 데스크톱 앱 실행
  python desktop.py --port 7429 # 포트 지정
  python desktop.py --no-tray   # 트레이 아이콘 없이

웹 모드와의 차이:
  - 네이티브 윈도우에서 실행 (브라우저 불필요)
  - 시스템 트레이 아이콘 (백그라운드 실행, 우클릭 메뉴)
  - 새 뉴스 수집 시 Windows 네이티브 알림
  - 창 닫기 → 트레이로 최소화 (완전 종료 = 트레이 우클릭 → 종료)
"""
import sys
import os
import time
import argparse
import subprocess
import threading
import socket

# 프로젝트 루트
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT_DIR, ".env"))

APP_NAME = "AI News Radar"
APP_ICON = None  # 아이콘 파일 경로 (없으면 기본)

# ── Streamlit 서버 관리 ──

def _find_free_port(preferred: int = 7429) -> int:
    """사용 가능한 포트 찾기"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", preferred))
        sock.close()
        return preferred
    except OSError:
        sock.close()
        # 자동 할당
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()
        return port


def _wait_for_server(port: int, timeout: int = 30) -> bool:
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


class StreamlitServer:
    """Streamlit 서버 프로세스 관리"""

    def __init__(self, port: int):
        self.port = port
        self.process = None

    def start(self):
        """서버 시작"""
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            os.path.join(ROOT_DIR, "app.py"),
            "--server.port", str(self.port),
            "--server.headless", "true",
            "--server.address", "127.0.0.1",
            "--browser.gatherUsageStats", "false",
            "--global.developmentMode", "false",
        ]
        self.process = subprocess.Popen(
            cmd,
            cwd=ROOT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        print(f"[Desktop] Streamlit 서버 시작 (포트 {self.port}, PID {self.process.pid})")

    def stop(self):
        """서버 종료"""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print("[Desktop] Streamlit 서버 종료")

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"


# ── 시스템 트레이 ──

def _create_tray_icon(server: StreamlitServer, window_ref: list):
    """시스템 트레이 아이콘 생성"""
    try:
        import pystray
        from PIL import Image, ImageDraw
    except ImportError:
        print("[Desktop] pystray/Pillow 미설치 — 트레이 아이콘 비활성화")
        return None

    # 간단한 📡 아이콘 생성 (16x16 파란 원)
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=(79, 195, 247, 255))
    draw.ellipse([20, 20, 44, 44], fill=(13, 71, 161, 255))
    draw.ellipse([28, 28, 36, 36], fill=(255, 255, 255, 255))

    def on_open(icon, item):
        """창 열기/복원"""
        if window_ref and window_ref[0]:
            try:
                window_ref[0].show()
                window_ref[0].restore()
            except Exception:
                pass

    def on_collect(icon, item):
        """수동 수집 트리거"""
        try:
            from crawler.rss_crawler import crawl_all
            threading.Thread(target=_collect_with_notification, daemon=True).start()
        except Exception as e:
            print(f"[Desktop] 수집 오류: {e}")

    def on_quit(icon, item):
        """완전 종료"""
        icon.stop()
        server.stop()
        if window_ref and window_ref[0]:
            try:
                window_ref[0].destroy()
            except Exception:
                pass
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem(f"📡 {APP_NAME}", on_open, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("🔄 뉴스 수집", on_collect),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("❌ 종료", on_quit),
    )

    icon = pystray.Icon(APP_NAME, img, APP_NAME, menu)
    return icon


def _collect_with_notification():
    """수집 + 데스크톱 알림"""
    try:
        from crawler.rss_crawler import crawl_all
        count = crawl_all()
        if count > 0:
            _show_notification(f"📡 {count}개 새 뉴스 수집!", "AI News Radar")
    except Exception as e:
        print(f"[Desktop] 수집 오류: {e}")


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
        pass  # 알림 실패 무시


# ── 데스크톱 알림 감시 (백그라운드) ──

def _watch_new_articles(interval: int = 300):
    """5분마다 새 기사 확인 → 알림"""
    from utils.helpers import safe_read_json
    from config import DATA_DIR

    articles_path = DATA_DIR / "articles.json"
    last_count = len(safe_read_json(articles_path, []))

    while True:
        time.sleep(interval)
        try:
            current = safe_read_json(articles_path, [])
            current_count = len(current)
            if current_count > last_count:
                new = current_count - last_count
                _show_notification(f"📡 새 뉴스 {new}개 수집됨!")
                last_count = current_count
            else:
                last_count = current_count
        except Exception:
            pass


# ── 메인 실행 ──

def main():
    parser = argparse.ArgumentParser(description=f"{APP_NAME} — 데스크톱 앱")
    parser.add_argument("--port", type=int, default=7429, help="서버 포트 (기본: 7429)")
    parser.add_argument("--no-tray", action="store_true", help="시스템 트레이 비활성화")
    parser.add_argument("--width", type=int, default=1400, help="창 너비")
    parser.add_argument("--height", type=int, default=900, help="창 높이")
    args = parser.parse_args()

    port = _find_free_port(args.port)

    # 1. Streamlit 서버 시작
    server = StreamlitServer(port)
    server.start()

    print(f"[Desktop] 서버 대기 중... ({server.url})")
    if not _wait_for_server(port, timeout=30):
        print("[Desktop] 서버 시작 실패!")
        server.stop()
        sys.exit(1)
    print("[Desktop] 서버 준비 완료!")

    # 2. 백그라운드 알림 감시
    watcher = threading.Thread(target=_watch_new_articles, daemon=True)
    watcher.start()

    # 3. 시스템 트레이 아이콘
    window_ref = [None]
    tray_icon = None

    if not args.no_tray:
        tray_icon = _create_tray_icon(server, window_ref)
        if tray_icon:
            tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
            tray_thread.start()

    # 4. pywebview 윈도우
    try:
        import webview

        def on_closing():
            """창 닫기 → 트레이로 최소화 (트레이 있을 때)"""
            if tray_icon:
                window_ref[0].hide()
                _show_notification("트레이로 최소화됨", APP_NAME)
                return False  # 창 닫기 취소
            return True  # 트레이 없으면 진짜 닫기

        window = webview.create_window(
            APP_NAME,
            server.url,
            width=args.width,
            height=args.height,
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
        print("[Desktop] pywebview 미설치 — 브라우저에서 열기")
        import webbrowser
        webbrowser.open(server.url)
        try:
            server.process.wait()
        except KeyboardInterrupt:
            pass
    finally:
        if tray_icon:
            try:
                tray_icon.stop()
            except Exception:
                pass
        server.stop()


if __name__ == "__main__":
    main()
