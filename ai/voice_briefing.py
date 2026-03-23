"""음성 브리핑 — edge-tts로 브리핑 텍스트를 한국어 음성으로 변환"""
import asyncio
import os
from pathlib import Path

from config import DATA_DIR
from utils.helpers import safe_read_json, today_str, log

BRIEFINGS_PATH = DATA_DIR / "briefings.json"
AUDIO_DIR = DATA_DIR / "audio"

# 한국어 음성 (edge-tts Microsoft 무료 TTS)
VOICE_FEMALE = "ko-KR-SunHiNeural"   # 여성 (자연스러운 톤)
VOICE_MALE = "ko-KR-InJoonNeural"    # 남성

DEFAULT_VOICE = VOICE_FEMALE


def _ensure_audio_dir():
    """오디오 저장 폴더 생성"""
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def _briefing_to_text(briefing: dict) -> str:
    """브리핑 dict를 읽기 좋은 텍스트로 변환"""
    date = briefing.get("date", today_str())
    lines = [f"{date} AI 뉴스 브리핑입니다."]

    # 총평
    summary = briefing.get("summary", "")
    if summary:
        lines.append(summary)

    # TOP 기사
    top = briefing.get("top_articles", [])
    if isinstance(top, list):
        lines.append(f"오늘의 주요 뉴스 {len(top)}건입니다.")
        for i, item in enumerate(top, 1):
            if isinstance(item, dict):
                headline = item.get("headline", item.get("title", ""))
                why = item.get("why_important", item.get("summary", ""))
                lines.append(f"{i}번째 뉴스. {headline}.")
                if why:
                    lines.append(why)

    lines.append("이상 AI 뉴스 레이더 브리핑이었습니다.")
    return "\n".join(lines)


async def _generate_audio_async(text: str, output_path: str, voice: str = DEFAULT_VOICE):
    """edge-tts로 텍스트를 MP3 오디오로 변환 (비동기)"""
    import edge_tts

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def generate_voice_briefing(briefing: dict = None, voice: str = DEFAULT_VOICE) -> str | None:
    """브리핑을 음성 파일로 변환. MP3 파일 경로 반환.

    Args:
        briefing: 브리핑 dict. None이면 오늘의 브리핑 자동 로드.
        voice: edge-tts 음성 ID.

    Returns:
        생성된 MP3 파일 경로 또는 None.
    """
    _ensure_audio_dir()

    # 브리핑 로드
    if briefing is None:
        briefings = safe_read_json(BRIEFINGS_PATH, [])
        briefing = next((b for b in briefings if b.get("date") == today_str()), None)

    if not briefing:
        log("[음성 브리핑] 브리핑 데이터 없음")
        return None

    # 텍스트 생성
    text = _briefing_to_text(briefing)
    if not text.strip():
        return None

    # 파일명: audio/briefing_2026-03-23.mp3
    date = briefing.get("date", today_str())
    output_path = str(AUDIO_DIR / f"briefing_{date}.mp3")

    # 이미 생성된 파일이 있으면 재사용
    if os.path.exists(output_path):
        log(f"[음성 브리핑] 캐시 사용: {output_path}")
        return output_path

    try:
        asyncio.run(_generate_audio_async(text, output_path, voice))
        log(f"[음성 브리핑] 생성 완료: {output_path}")
        return output_path
    except Exception as e:
        log(f"[음성 브리핑 오류] {e}")
        return None


def get_available_voices() -> list[dict]:
    """사용 가능한 한국어 음성 목록"""
    return [
        {"id": VOICE_FEMALE, "name": "선히 (여성)", "gender": "female"},
        {"id": VOICE_MALE, "name": "인준 (남성)", "gender": "male"},
    ]
