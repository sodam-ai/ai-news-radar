"""카드 뉴스 이미지 생성기 — Pillow 기반

뉴스 데이터를 시각적 카드 이미지(1080x1080 PNG)로 변환합니다.
SNS 업로드 및 미리보기에 사용됩니다.
"""
import os
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config import DATA_DIR, CATEGORIES

CARD_DIR = DATA_DIR / "cards"

# 카테고리별 테마 색상
CAT_COLORS = {
    "ai_tool": ("#2196F3", "#1565C0"),
    "ai_research": ("#9C27B0", "#6A1B9A"),
    "ai_trend": ("#FF9800", "#E65100"),
    "ai_tutorial": ("#4CAF50", "#2E7D32"),
    "ai_business": ("#E91E63", "#AD1457"),
    "ai_image_video": ("#FF4081", "#C51162"),
    "ai_coding": ("#00E676", "#00C853"),
    "ai_ontology": ("#7C4DFF", "#6200EA"),
    "ai_other": ("#78909C", "#455A64"),
}

SENTIMENT_ICONS = {"positive": "😊", "negative": "😠", "neutral": "😐"}

# 폰트 경로 (Windows → macOS → Linux fallback)
_FONT_PATHS = [
    "C:/Windows/Fonts/malgunbd.ttf",      # Windows 맑은 고딕 Bold
    "C:/Windows/Fonts/malgun.ttf",         # Windows 맑은 고딕
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS
    "/usr/share/fonts/truetype/noto/NotoSansKR-Bold.ttf",  # Linux
]

_FONT_REGULAR_PATHS = [
    "C:/Windows/Fonts/malgun.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansKR-Regular.ttf",
]


def _find_font(paths: list[str]) -> str:
    for p in paths:
        if os.path.exists(p):
            return p
    return ""


def _ensure_card_dir():
    CARD_DIR.mkdir(parents=True, exist_ok=True)


def generate_single_card(article: dict, size: tuple = (1080, 1080)) -> str | None:
    """단일 기사를 카드 뉴스 이미지로 변환. PNG 경로 반환."""
    _ensure_card_dir()

    w, h = size
    category = article.get("category", "ai_other")
    accent, accent_dark = CAT_COLORS.get(category, ("#78909C", "#455A64"))
    sentiment = article.get("sentiment", "neutral")

    # 이미지 생성
    img = Image.new("RGB", (w, h), color="#0D1117")
    draw = ImageDraw.Draw(img)

    # 폰트 로드
    bold_path = _find_font(_FONT_PATHS)
    regular_path = _find_font(_FONT_REGULAR_PATHS)

    try:
        font_title = ImageFont.truetype(bold_path, 42) if bold_path else ImageFont.load_default()
        font_body = ImageFont.truetype(regular_path, 28) if regular_path else ImageFont.load_default()
        font_meta = ImageFont.truetype(regular_path, 22) if regular_path else ImageFont.load_default()
        font_tag = ImageFont.truetype(bold_path, 20) if bold_path else ImageFont.load_default()
        font_brand = ImageFont.truetype(bold_path, 24) if bold_path else ImageFont.load_default()
    except Exception:
        font_title = font_body = font_meta = font_tag = font_brand = ImageFont.load_default()

    padding = 60

    # ── 상단 그라데이션 바 ──
    for i in range(8):
        alpha = int(255 * (1 - i / 8))
        r, g, b = int(accent[1:3], 16), int(accent[3:5], 16), int(accent[5:7], 16)
        draw.rectangle([0, i, w, i + 1], fill=(r, g, b))

    # ── 카테고리 배지 ──
    cat_name = CATEGORIES.get(category, "기타")
    cat_y = 40
    cat_text = f"  {cat_name}  "
    bbox = draw.textbbox((0, 0), cat_text, font=font_tag)
    cat_w = bbox[2] - bbox[0] + 20
    draw.rounded_rectangle([padding, cat_y, padding + cat_w, cat_y + 36], radius=18, fill=accent)
    draw.text((padding + 10, cat_y + 4), cat_text, fill="white", font=font_tag)

    # ── 감성 + 중요도 (우측 상단) ──
    importance = article.get("importance", 0)
    stars = "⭐" * importance
    sentiment_text = f"{SENTIMENT_ICONS.get(sentiment, '')} {stars}"
    draw.text((w - padding - 200, cat_y + 4), sentiment_text, fill="#B0BEC5", font=font_meta)

    # ── 제목 (줄바꿈) ──
    title = article.get("title", "")
    title_y = 110
    wrapped_title = textwrap.fill(title, width=22)
    title_lines = wrapped_title.split("\n")[:4]  # 최대 4줄

    for i, line in enumerate(title_lines):
        draw.text((padding, title_y + i * 56), line, fill="white", font=font_title)

    # ── 구분선 ──
    line_y = title_y + len(title_lines) * 56 + 30
    draw.rectangle([padding, line_y, w - padding, line_y + 3], fill=accent)

    # ── 요약 (줄바꿈) ──
    summary = article.get("summary_text", "")
    summary_y = line_y + 30
    wrapped_summary = textwrap.fill(summary, width=32)
    summary_lines = wrapped_summary.split("\n")[:8]  # 최대 8줄

    for i, line in enumerate(summary_lines):
        draw.text((padding, summary_y + i * 40), line, fill="#CFD8DC", font=font_body)

    # ── 태그 ──
    tags = article.get("tags", [])[:5]
    if tags:
        tag_y = h - 200
        tag_text = "  ".join([f"#{t}" for t in tags])
        draw.text((padding, tag_y), tag_text, fill=accent, font=font_tag)

    # ── 팩트체크 배지 ──
    related = article.get("related_articles", [])
    fc_count = len(related) + 1
    if fc_count >= 3:
        fc_text = f"✅ {fc_count}개 매체 확인"
    elif fc_count == 2:
        fc_text = f"🔍 {fc_count}개 매체 보도"
    else:
        fc_text = "⚠️ 단독 보도"
    draw.text((padding, h - 150), fc_text, fill="#90A4AE", font=font_meta)

    # ── 하단 브랜드 + 날짜 ──
    draw.rectangle([0, h - 80, w, h], fill="#161B22")
    draw.text((padding, h - 65), "📡 AI News Radar", fill=accent, font=font_brand)

    pub = article.get("published_at", "")[:10]
    if pub:
        draw.text((w - padding - 150, h - 60), pub, fill="#546E7A", font=font_meta)

    # 저장
    safe_title = "".join(c for c in title[:30] if c.isalnum() or c in (" ", "-", "_")).strip()
    filename = f"card_{article.get('id', 'unknown')}_{safe_title[:20]}.png"
    output_path = str(CARD_DIR / filename)
    img.save(output_path, "PNG", quality=95)

    return output_path


def generate_briefing_card(briefing: dict, size: tuple = (1080, 1350)) -> str | None:
    """브리핑 전체를 하나의 카드 이미지로 변환"""
    _ensure_card_dir()

    w, h = size
    img = Image.new("RGB", (w, h), color="#0D1117")
    draw = ImageDraw.Draw(img)

    bold_path = _find_font(_FONT_PATHS)
    regular_path = _find_font(_FONT_REGULAR_PATHS)

    try:
        font_title = ImageFont.truetype(bold_path, 48) if bold_path else ImageFont.load_default()
        font_item = ImageFont.truetype(bold_path, 30) if bold_path else ImageFont.load_default()
        font_body = ImageFont.truetype(regular_path, 24) if regular_path else ImageFont.load_default()
        font_brand = ImageFont.truetype(bold_path, 24) if bold_path else ImageFont.load_default()
    except Exception:
        font_title = font_item = font_body = font_brand = ImageFont.load_default()

    padding = 60

    # 상단 그라데이션
    for i in range(10):
        draw.rectangle([0, i, w, i + 1], fill=(79, 195, 247))

    # 제목
    date = briefing.get("date", "")
    draw.text((padding, 40), f"📡 오늘의 AI 브리핑", fill="white", font=font_title)
    draw.text((padding, 100), date, fill="#4FC3F7", font=font_body)

    # 총평
    summary = briefing.get("summary", "")
    if summary:
        wrapped = textwrap.fill(summary, width=34)
        for i, line in enumerate(wrapped.split("\n")[:3]):
            draw.text((padding, 150 + i * 35), line, fill="#B0BEC5", font=font_body)

    # TOP 기사
    top = briefing.get("top_articles", [])
    y_offset = 290
    for i, item in enumerate(top[:5]):
        if not isinstance(item, dict):
            continue
        headline = item.get("headline", item.get("title", ""))
        why = item.get("why_important", item.get("summary", ""))

        # 번호 원
        draw.ellipse([padding, y_offset, padding + 44, y_offset + 44], fill="#4FC3F7")
        draw.text((padding + 14, y_offset + 6), str(i + 1), fill="white", font=font_item)

        # 헤드라인
        wrapped_h = textwrap.fill(headline, width=28)
        h_lines = wrapped_h.split("\n")[:2]
        for j, line in enumerate(h_lines):
            draw.text((padding + 60, y_offset + j * 38), line, fill="white", font=font_item)

        # 이유
        if why:
            why_wrapped = textwrap.fill(why, width=36)
            why_lines = why_wrapped.split("\n")[:2]
            why_y = y_offset + len(h_lines) * 38 + 5
            for j, line in enumerate(why_lines):
                draw.text((padding + 60, why_y + j * 30), line, fill="#78909C", font=font_body)
            y_offset = why_y + len(why_lines) * 30 + 30
        else:
            y_offset += len(h_lines) * 38 + 30

    # 하단 브랜드
    draw.rectangle([0, h - 80, w, h], fill="#161B22")
    draw.text((padding, h - 65), "📡 AI News Radar — SoDam AI Studio", fill="#4FC3F7", font=font_brand)

    filename = f"briefing_card_{date}.png"
    output_path = str(CARD_DIR / filename)
    img.save(output_path, "PNG", quality=95)

    return output_path


def generate_category_cards(articles: list[dict], category: str, max_cards: int = 5) -> list[str]:
    """특정 카테고리의 기사들을 카드 이미지로 생성"""
    filtered = [a for a in articles if a.get("category") == category and a.get("ai_processed")]
    filtered.sort(key=lambda x: x.get("importance", 0), reverse=True)

    paths = []
    for a in filtered[:max_cards]:
        path = generate_single_card(a)
        if path:
            paths.append(path)
    return paths
