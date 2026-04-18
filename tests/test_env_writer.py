"""utils/env_writer.py — `.env` 원자적 R/W 회귀 테스트."""
from __future__ import annotations

from pathlib import Path

import pytest

from utils.env_writer import (
    EnvWriterError,
    apply_runtime,
    read_env,
    update_env,
)


@pytest.fixture
def tmp_env(tmp_path) -> Path:
    """빈 .env 파일 경로 (아직 생성 안 됨)."""
    return tmp_path / ".env"


class TestReadEnv:
    def test_file_not_found_returns_empty(self, tmp_env):
        assert read_env(tmp_env) == {}

    def test_basic_parse(self, tmp_env):
        tmp_env.write_text("A=1\nB=hello\n", encoding="utf-8")
        assert read_env(tmp_env) == {"A": "1", "B": "hello"}

    def test_comments_and_blank_lines_ignored(self, tmp_env):
        tmp_env.write_text(
            "# this is a comment\n"
            "\n"
            "KEY=value\n"
            "# inline comment below\n"
            "ANOTHER=2\n",
            encoding="utf-8",
        )
        assert read_env(tmp_env) == {"KEY": "value", "ANOTHER": "2"}

    def test_quoted_values_stripped(self, tmp_env):
        tmp_env.write_text(
            'A="double"\n'
            "B='single'\n"
            'C=no_quotes\n',
            encoding="utf-8",
        )
        env = read_env(tmp_env)
        assert env == {"A": "double", "B": "single", "C": "no_quotes"}

    def test_whitespace_around_equals(self, tmp_env):
        tmp_env.write_text("A = spaces\nB=  trimmed  \n", encoding="utf-8")
        env = read_env(tmp_env)
        assert env["A"] == "spaces"
        assert env["B"] == "trimmed"


class TestUpdateEnv:
    def test_creates_new_file_if_missing(self, tmp_env):
        update_env({"NEW_KEY": "v1"}, path=tmp_env)
        assert tmp_env.exists()
        assert read_env(tmp_env) == {"NEW_KEY": "v1"}

    def test_updates_existing_key_in_place(self, tmp_env):
        tmp_env.write_text("A=old\nB=other\n", encoding="utf-8")
        update_env({"A": "new"}, path=tmp_env)
        env = read_env(tmp_env)
        assert env == {"A": "new", "B": "other"}

    def test_adds_new_key_at_end(self, tmp_env):
        tmp_env.write_text("A=1\n", encoding="utf-8")
        update_env({"NEW": "added"}, path=tmp_env)
        env = read_env(tmp_env)
        assert env == {"A": "1", "NEW": "added"}

    def test_preserves_comments_and_order(self, tmp_env):
        tmp_env.write_text(
            "# top comment\n"
            "A=1\n"
            "# middle comment\n"
            "B=2\n",
            encoding="utf-8",
        )
        update_env({"A": "updated"}, path=tmp_env)
        content = tmp_env.read_text(encoding="utf-8")
        assert "# top comment" in content
        assert "# middle comment" in content
        assert "A=updated" in content
        assert "B=2" in content
        assert content.index("# top comment") < content.index("A=updated")
        assert content.index("A=updated") < content.index("# middle comment")

    def test_multiple_updates_atomic(self, tmp_env):
        tmp_env.write_text("A=1\nB=2\n", encoding="utf-8")
        update_env({"A": "aa", "B": "bb", "C": "cc"}, path=tmp_env)
        assert read_env(tmp_env) == {"A": "aa", "B": "bb", "C": "cc"}

    def test_empty_value_rejected(self, tmp_env):
        with pytest.raises(EnvWriterError):
            update_env({"KEY": ""}, path=tmp_env)
        with pytest.raises(EnvWriterError):
            update_env({"KEY": "   "}, path=tmp_env)

    def test_invalid_key_rejected(self, tmp_env):
        with pytest.raises(EnvWriterError):
            update_env({"1INVALID": "v"}, path=tmp_env)
        with pytest.raises(EnvWriterError):
            update_env({"INVALID-KEY": "v"}, path=tmp_env)
        with pytest.raises(EnvWriterError):
            update_env({"": "v"}, path=tmp_env)

    def test_too_long_value_rejected(self, tmp_env):
        with pytest.raises(EnvWriterError):
            update_env({"KEY": "x" * 2001}, path=tmp_env)

    def test_empty_updates_rejected(self, tmp_env):
        with pytest.raises(EnvWriterError):
            update_env({}, path=tmp_env)

    def test_no_tempfile_leftover(self, tmp_env):
        tmp_env.write_text("A=1\n", encoding="utf-8")
        update_env({"A": "2"}, path=tmp_env)
        leftovers = list(tmp_env.parent.glob(".env.*.tmp"))
        assert leftovers == [], f"leftover tempfiles: {leftovers}"

    def test_existing_file_preserved_on_reject(self, tmp_env):
        tmp_env.write_text("A=keep\n", encoding="utf-8")
        with pytest.raises(EnvWriterError):
            update_env({"KEY": ""}, path=tmp_env)
        assert read_env(tmp_env) == {"A": "keep"}


class TestApplyRuntime:
    def test_sets_os_environ(self, monkeypatch):
        import os
        monkeypatch.delenv("TEST_RUNTIME_KEY_X", raising=False)
        apply_runtime({"TEST_RUNTIME_KEY_X": "runtime_val"})
        assert os.getenv("TEST_RUNTIME_KEY_X") == "runtime_val"

    def test_ignores_empty_values(self, monkeypatch):
        import os
        monkeypatch.delenv("TEST_EMPTY_RUNTIME", raising=False)
        apply_runtime({"TEST_EMPTY_RUNTIME": ""})
        assert os.getenv("TEST_EMPTY_RUNTIME") is None
