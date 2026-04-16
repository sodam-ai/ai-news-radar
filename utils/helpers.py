"""JSON/ë¡œê¹…, ê³µí†µ ë„ì›€ í•¨ìˆ˜."""
import json
import sys
import tempfile
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path


def log(msg: str):
    """Windows CP949 ì½˜ì†”ì—ì„œë„ ì¶œë ¥ê°€ ëŠê¸°ì§€ ì•Šë„ë¡ ë³´ìˆ˜ì ìœ¼ë¡œ ë¡œê¹…. """
    try:
        print(msg)
    except (UnicodeEncodeError, UnicodeDecodeError):
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


_JSON_LOCKS: dict[str, threading.RLock] = {}
_JSON_LOCKS_GUARD = threading.Lock()


def _json_lock(path: Path) -> threading.RLock:
    key = str(path.resolve())
    with _JSON_LOCKS_GUARD:
        if key not in _JSON_LOCKS:
            _JSON_LOCKS[key] = threading.RLock()
        return _JSON_LOCKS[key]


def safe_write_json(path: Path, data):
    """ë™ì¼ íŒŒì¼ ì— ëŒ€í•œ ë™ì‹œ ì 쓰ê¸°ë¥¼ ì™„í™”í•˜ê³  ì›ìžì ìœ¼ë¡œ êµì²´."""
    with _json_lock(path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f"{path.stem}_",
            suffix=".tmp",
            delete=False,
        ) as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            tmp_path = Path(f.name)
        tmp_path.replace(path)


def safe_update_json(path: Path, updater, default=None):
    """ìµœì‹ ì— ë€í•œ read-modify-write ë¥¼ í•˜ë‚˜ì˜ ë½ìœ¼ë¡œ ë¬¶ëŠ” í—¬í¼."""
    with _json_lock(path):
        current = safe_read_json(path, default)
        updated = updater(current)
        if updated is None:
            updated = current
        safe_write_json(path, updated)
        return updated
