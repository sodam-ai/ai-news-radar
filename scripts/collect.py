"""CLI 수집 스크립트 — GitHub Actions / 로컬 cron 용

사용법:
  python scripts/collect.py             # 전체 수집+처리+브리핑
  python scripts/collect.py --crawl     # 수집만
  python scripts/collect.py --process   # AI 처리만
  python scripts/collect.py --briefing  # 브리핑 생성만
  python scripts/collect.py --sns       # SNS 카드 뉴스 자동 게시 (설정된 플랫폼)
  python scripts/collect.py --all       # 전체 + SNS 게시
"""
import sys
import os
import argparse

# 프로젝트 루트를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from crawler.rss_crawler import crawl_all
from ai.batch_processor import process_unprocessed
from ai.deduplicator import deduplicate
from ai.briefing import generate_daily_briefing
from ai.model_router import get_active_provider, PROVIDERS
from ai.smart_alert import check_and_alert
from utils.helpers import log


def _run_sns_posting():
    """설정된 SNS 플랫폼에 카드 뉴스 자동 게시"""
    from sns.poster import get_available_platforms, post_article
    from sns.card_generator import generate_single_card
    from config import DATA_DIR
    from utils.helpers import safe_read_json

    platforms = get_available_platforms()
    configured = [p["id"] for p in platforms if p["configured"]]

    if not configured:
        print("⚠️ 설정된 SNS 플랫폼이 없습니다. .env에 SNS 키를 추가하세요.")
        return

    print(f"📢 SNS 게시 시작 ({len(configured)}개 플랫폼: {', '.join(configured)})...")

    # 오늘 수집된 기사 중 중요도 상위 3개
    articles = safe_read_json(DATA_DIR / "articles.json", [])
    from utils.helpers import today_str
    today = today_str()
    today_arts = [
        a for a in articles
        if a.get("ai_processed") and a.get("is_primary", True)
        and a.get("crawled_at", "").startswith(today)
    ]
    today_arts.sort(key=lambda x: x.get("importance", 0), reverse=True)
    target = today_arts[:3]

    if not target:
        # 오늘 기사 없으면 최근 중요 기사
        all_primary = [a for a in articles if a.get("ai_processed") and a.get("is_primary", True)]
        all_primary.sort(key=lambda x: x.get("importance", 0), reverse=True)
        target = all_primary[:3]

    if not target:
        print("⚠️ 게시할 기사가 없습니다.")
        return

    posted = 0
    for a in target:
        try:
            card_path = generate_single_card(a)
            results = post_article(a, configured, card_path)
            success = sum(1 for r in results if r.get("success"))
            posted += success
            title_short = a.get("title", "")[:40]
            print(f"  ✅ {title_short}... → {success}/{len(configured)} 플랫폼")
        except Exception as e:
            print(f"  ❌ 게시 오류: {e}")

    print(f"📢 SNS 게시 완료: {posted}건")
    log(f"[CLI] SNS 게시: {posted}건")


def main():
    parser = argparse.ArgumentParser(description="AI News Radar — CLI 수집 스크립트")
    parser.add_argument("--crawl", action="store_true", help="RSS 수집만")
    parser.add_argument("--process", action="store_true", help="AI 처리만")
    parser.add_argument("--briefing", action="store_true", help="브리핑 생성만")
    parser.add_argument("--sns", action="store_true", help="SNS 카드 뉴스 자동 게시")
    parser.add_argument("--all", action="store_true", help="전체 + SNS 게시")
    args = parser.parse_args()

    # 아무 플래그도 없거나 --all이면 전체 실행
    run_all = not (args.crawl or args.process or args.briefing or args.sns) or args.all
    run_sns = args.sns or args.all

    # 1. RSS 수집
    if run_all or args.crawl:
        print("📡 RSS 수집 시작...")
        try:
            count = crawl_all()
            print(f"✅ {count}개 새 글 수집 완료")
            log(f"[CLI] RSS 수집: {count}개")
        except Exception as e:
            print(f"❌ 수집 오류: {e}")
            log(f"[CLI 오류] RSS 수집: {e}")

    # 2. AI 처리
    if run_all or args.process:
        provider = get_active_provider()
        if not provider:
            print("⚠️ LLM API 키가 설정되지 않았습니다. AI 처리를 건너뜁니다.")
        else:
            print(f"🤖 AI 처리 시작 ({PROVIDERS[provider]['name']})...")
            try:
                processed = process_unprocessed()
                clusters = deduplicate()
                print(f"✅ AI 처리 {processed}개 완료, 중복 {clusters}개 그룹 병합")
                log(f"[CLI] AI 처리: {processed}개, 중복: {clusters}그룹")

                # 스마트 알림
                alerted = check_and_alert()
                if alerted:
                    print(f"🔔 {len(alerted)}건 키워드 알림 발생")
            except Exception as e:
                print(f"❌ AI 처리 오류: {e}")
                log(f"[CLI 오류] AI 처리: {e}")

    # 3. 브리핑 생성
    if run_all or args.briefing:
        provider = get_active_provider()
        if not provider:
            print("⚠️ LLM API 키가 설정되지 않았습니다. 브리핑 생성을 건너뜁니다.")
        else:
            print("📋 브리핑 생성 중...")
            try:
                briefing = generate_daily_briefing()
                if briefing:
                    top_count = len(briefing.get("top_articles", []))
                    print(f"✅ 브리핑 생성 완료 (TOP {top_count})")
                    log(f"[CLI] 브리핑 생성: TOP {top_count}")
                else:
                    print("⚠️ 브리핑 생성에 필요한 기사가 부족합니다.")
            except Exception as e:
                print(f"❌ 브리핑 오류: {e}")
                log(f"[CLI 오류] 브리핑: {e}")

    # 4. SNS 게시
    if run_sns:
        _run_sns_posting()

    print("\n🏁 완료!")


if __name__ == "__main__":
    main()
