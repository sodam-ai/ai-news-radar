"""`.env` 파일 원자적 R/W 유틸.

목적:
- Streamlit UI에서 API 키를 받아 `.env`에 안전하게 기록
- 기존 주석·빈 줄·미변경 키를 보존
- 저장 실패 시 기존 파일 유지 (atomic write)
- 저장 직후 `os.environ` + `load_dotenv(override=True)` 재반영
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
import threading
from pathlib import Path
from typing import Optional

_DEFAULT_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
_WRITE_LOCK = threading.RLock()

_KV_PATTERN = re.compile(
    r"""^(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<val>.*)$"""
)


class EnvWriterError(Exception):
    """env 파일 조작 실패."""


def _resolve(path: Optional[Path]) -> Path:
    return Path(path) if path else _DEFAULT_ENV_PATH


def read_env(path: Optional[Path] = None) -> dict[str, str]:
    """`.env` 파싱 → {KEY: VALUE} (주석/빈 줄 무시, 양끝 따옴표 제거)."""
    env_path = _resolve(path)
    if not env_path.exists():
        return {}
    result: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = _KV_PATTERN.match(stripped)
        if not m:
            continue
        key = m.group("key")
        val = m.group("val").strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
            val = val[1:-1]
        result[key] = val
    return result


def update_env(
    updates: dict[str, str],
    path: Optional[Path] = None,
) -> None:
    """`.env`에 updates 반영. 주석·빈 줄·미변경 키 보존, atomic write.

    - 빈 값(strip 후 empty)은 거부 (`EnvWriterError`)
    - 기존 키는 같은 위치에서 업데이트
    - 신규 키는 파일 끝에 추가
    - tempfile → os.replace로 원자적 교체
    """
    if not updates:
        raise EnvWriterError("updates는 비어 있을 수 없습니다")

    for k, v in updates.items():
        if not isinstance(k, str) or not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", k):
            raise EnvWriterError(f"키 이름이 잘못됨: {k!r}")
        if not isinstance(v, str) or not v.strip():
            raise EnvWriterError(f"값이 비어 있음: {k}")
        if len(v) > 2000:
            raise EnvWriterError(f"값이 너무 김(>2000): {k}")

    env_path = _resolve(path)

    with _WRITE_LOCK:
        if env_path.exists():
            original = env_path.read_text(encoding="utf-8").splitlines()
        else:
            original = []

        remaining = dict(updates)
        new_lines: list[str] = []
        for line in original:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                new_lines.append(line)
                continue
            m = _KV_PATTERN.match(stripped)
            if not m:
                new_lines.append(line)
                continue
            key = m.group("key")
            if key in remaining:
                new_lines.append(f"{key}={remaining[key]}")
                del remaining[key]
            else:
                new_lines.append(line)

        if remaining:
            if new_lines and new_lines[-1].strip():
                new_lines.append("")
            for key, val in remaining.items():
                new_lines.append(f"{key}={val}")

        env_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=env_path.parent,
            prefix=".env.",
            suffix=".tmp",
            delete=False,
        ) as tf:
            tf.write("\n".join(new_lines))
            if new_lines and new_lines[-1] != "":
                tf.write("\n")
            tmp_path = Path(tf.name)

        if sys.platform != "win32":
            try:
                os.chmod(tmp_path, 0o600)
            except OSError:
                pass

        os.replace(tmp_path, env_path)


def apply_runtime(updates: dict[str, str]) -> None:
    """os.environ 즉시 반영 + .env 재로드 (override=True)."""
    from dotenv import load_dotenv

    for k, v in updates.items():
        if isinstance(k, str) and isinstance(v, str) and v.strip():
            os.environ[k] = v

    env_path = _resolve(None)
    if env_path.exists():
        load_dotenv(dotenv_path=str(env_path), override=True)
