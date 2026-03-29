"""AI News Radar — 빌드 스크립트
exe 빌드 + ZIP 패키징을 한 번에 실행합니다.

사용법:
  python build_installer.py          # exe 빌드 + ZIP 생성
  python build_installer.py --zip    # ZIP만 생성 (이미 빌드된 경우)
  python build_installer.py --inno   # Inno Setup 인스톨러 빌드 (Inno Setup 필요)
"""
import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
DIST_DIR = PROJECT_ROOT / "dist" / "AI_News_Radar"
OUTPUT_DIR = PROJECT_ROOT / "installer_output"
VERSION = "1.0.0"


def build_exe():
    """PyInstaller로 exe 빌드"""
    print("=" * 50)
    print("  Step 1: PyInstaller 빌드")
    print("=" * 50)

    spec_file = PROJECT_ROOT / "ai_news_radar.spec"
    if not spec_file.exists():
        print(f"[ERROR] spec 파일 없음: {spec_file}")
        return False

    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm", str(spec_file)]
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))

    if result.returncode != 0:
        print("[ERROR] PyInstaller 빌드 실패!")
        return False

    if not (DIST_DIR / "AI_News_Radar.exe").exists():
        print("[ERROR] exe 파일이 생성되지 않았습니다!")
        return False

    print("[OK] exe 빌드 완료!")
    return True


def create_zip():
    """Portable ZIP 생성"""
    print("=" * 50)
    print("  Step 2: Portable ZIP 생성")
    print("=" * 50)

    if not DIST_DIR.exists():
        print(f"[ERROR] 빌드 폴더 없음: {DIST_DIR}")
        print("  먼저 --build로 exe를 빌드하세요.")
        return False

    OUTPUT_DIR.mkdir(exist_ok=True)
    zip_name = f"AI_News_Radar_v{VERSION}_Portable_Win64"
    zip_path = OUTPUT_DIR / f"{zip_name}.zip"

    # 기존 ZIP 삭제
    if zip_path.exists():
        zip_path.unlink()

    print(f"  ZIP 생성 중: {zip_path}")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for root, dirs, files in os.walk(DIST_DIR):
            # __pycache__ 제외
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for file in files:
                file_path = Path(root) / file
                arcname = f"{zip_name}/{file_path.relative_to(DIST_DIR)}"
                zf.write(file_path, arcname)

        # .env.example 추가
        env_example = PROJECT_ROOT / ".env.example"
        if env_example.exists():
            zf.write(env_example, f"{zip_name}/.env.example")

        # 간단한 사용 설명서
        readme_content = f"""AI News Radar v{VERSION} — Portable Edition
=============================================

사용법:
  1. 이 폴더를 원하는 곳에 압축 해제
  2. .env.example을 .env로 복사
  3. .env 파일에 GEMINI_API_KEY 입력
  4. AI_News_Radar.exe 실행

포트: http://localhost:6601

문제 해결:
  - Windows Defender가 차단하면: "추가 정보" → "실행" 클릭
  - .env 파일이 없으면 API 기능이 작동하지 않습니다
  - 방화벽에서 6601 포트 허용 필요할 수 있습니다

GitHub: https://github.com/sodam-ai/ai-news-radar
"""
        zf.writestr(f"{zip_name}/사용법.txt", readme_content.encode('utf-8'))

    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"[OK] ZIP 생성 완료: {zip_path} ({zip_size_mb:.1f} MB)")
    return True


def build_inno():
    """Inno Setup 인스톨러 빌드"""
    print("=" * 50)
    print("  Step 3: Inno Setup 인스톨러 빌드")
    print("=" * 50)

    iss_file = PROJECT_ROOT / "installer.iss"
    iscc_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]

    iscc = None
    for p in iscc_paths:
        if os.path.exists(p):
            iscc = p
            break

    if not iscc:
        print("[SKIP] Inno Setup이 설치되어 있지 않습니다.")
        print("  다운로드: https://jrsoftware.org/isdl.php")
        print(f"  설치 후 '{iss_file}'을 Inno Setup에서 열어 컴파일하세요.")
        return False

    OUTPUT_DIR.mkdir(exist_ok=True)
    cmd = [iscc, str(iss_file)]
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))

    if result.returncode != 0:
        print("[ERROR] Inno Setup 빌드 실패!")
        return False

    print("[OK] 인스톨러 생성 완료!")
    return True


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--zip" in args:
        create_zip()
    elif "--inno" in args:
        build_inno()
    else:
        # 전체 빌드
        if build_exe():
            create_zip()
            build_inno()
        else:
            print("\n[FAILED] 빌드 실패. 로그를 확인하세요.")
            sys.exit(1)
