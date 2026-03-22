"""유틸리티 함수"""
import sys
import json
import uuid
import tempfile
from pathlib import Path
from datetime import datetime, timezone


def log(msg: str):
    """Windows CP949 콘솔에서도 안전한 로그 출력"""
    try:
        print(msg)
    except (UnicodeEncodeError, UnicodeDecodeError):
        # 유니코드 문자를 ASCII 대체 문자로 변환하여 출력
        safe = msg.encode("ascii", errors="replace").decode("ascii")
        print(safe)


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def safe_read_json(path: Path, default=None):
    if default is None:
        default = []
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_write_json(path: Path, data):
    """임시 파일 → rename 패턴으로 파일 깨짐 방지"""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(path)
