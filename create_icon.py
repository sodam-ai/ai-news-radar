"""AI News Radar — 아이콘 생성 스크립트
레이더 + 뉴스 모티프의 프로그램 아이콘을 생성합니다.
"""
import math
from PIL import Image, ImageDraw, ImageFont

SIZES = [16, 32, 48, 64, 128, 256]


def create_icon(size: int = 256) -> Image.Image:
    """레이더 + 신호 모티프 아이콘 생성"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    r = size // 2

    # 배경: 진한 남색 원
    draw.ellipse([0, 0, size - 1, size - 1], fill=(15, 23, 42, 255))

    # 외곽 링: 얇은 파란 테두리
    draw.ellipse([1, 1, size - 2, size - 2], outline=(59, 130, 246, 180), width=max(1, size // 64))

    # 레이더 동심원 (3개)
    for i, ratio in enumerate([0.7, 0.5, 0.3]):
        cr = int(r * ratio)
        alpha = 60 - i * 15
        draw.ellipse(
            [cx - cr, cy - cr, cx + cr, cy + cr],
            outline=(96, 165, 250, alpha), width=max(1, size // 128)
        )

    # 레이더 스캔 라인 (부채꼴 효과)
    line_len = int(r * 0.75)
    for angle_deg in [30, 150, 270]:
        angle = math.radians(angle_deg)
        ex = cx + int(line_len * math.cos(angle))
        ey = cy + int(line_len * math.sin(angle))
        draw.line([cx, cy, ex, ey], fill=(59, 130, 246, 50), width=max(1, size // 128))

    # 메인 스캔 라인 (밝은 파란)
    main_angle = math.radians(-45)
    mx = cx + int(line_len * math.cos(main_angle))
    my = cy + int(line_len * math.sin(main_angle))
    draw.line([cx, cy, mx, my], fill=(96, 165, 250, 200), width=max(1, size // 64))

    # 신호 도트 3개 (감지된 뉴스 포인트)
    dots = [
        (0.30, -60, (52, 211, 153, 255)),   # 녹색 — 긍정
        (0.55, -20, (251, 191, 36, 255)),    # 황색 — 중립
        (0.45, -70, (96, 165, 250, 255)),    # 파란 — 메인
    ]
    for dist_ratio, deg, color in dots:
        rad = math.radians(deg)
        dx = cx + int(r * dist_ratio * math.cos(rad))
        dy = cy + int(r * dist_ratio * math.sin(rad))
        dot_r = max(2, size // 32)
        # 글로우
        glow_r = dot_r * 3
        for gr in range(glow_r, dot_r, -1):
            alpha = int(color[3] * 0.15 * (1 - gr / glow_r))
            draw.ellipse([dx - gr, dy - gr, dx + gr, dy + gr], fill=(*color[:3], alpha))
        draw.ellipse([dx - dot_r, dy - dot_r, dx + dot_r, dy + dot_r], fill=color)

    # 중심 점
    center_r = max(2, size // 40)
    draw.ellipse(
        [cx - center_r, cy - center_r, cx + center_r, cy + center_r],
        fill=(255, 255, 255, 230)
    )

    # 우측 하단: 작은 "N" 텍스트 (News)
    if size >= 64:
        try:
            font_size = max(10, size // 6)
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()
        tx = cx + int(r * 0.25)
        ty = cy + int(r * 0.25)
        # 텍스트 배경 원
        tr = font_size // 2 + 4
        draw.ellipse([tx - tr, ty - tr, tx + tr, ty + tr], fill=(59, 130, 246, 220))
        # "N" 글자
        bbox = draw.textbbox((0, 0), "N", font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((tx - tw // 2, ty - th // 2 - 2), "N", fill=(255, 255, 255, 255), font=font)

    return img


def main():
    # 멀티사이즈 ICO 생성
    images = [create_icon(s) for s in SIZES]
    ico_path = "assets/icon.ico"

    import os
    os.makedirs("assets", exist_ok=True)

    # ICO 저장 (멀티사이즈)
    images[0].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in SIZES],
        append_images=images[1:],
    )
    print(f"[OK] {ico_path}")

    # PNG도 저장 (256x256)
    png_path = "assets/icon.png"
    images[-1].save(png_path, format="PNG")
    print(f"[OK] {png_path}")


if __name__ == "__main__":
    main()
