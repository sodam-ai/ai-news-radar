"""CLI 수집 스크립트 — GitHub Actions / 로컬 cron 용

사용법:
  python scripts/collect.py             # 전체 수집+처리+브리핑
  python scripts/collect.py --crawl     # 수집만
  python scripts/collect.py --process   # AI 처리만
  python scripts/collect.py --briefing  # 브리핑 생성만
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
from utils.helpers import log


def main():
    parser = argparse.ArgumentParser(description="AI News Radar — CLI 수집 스크립트")
    parser.add_argument("--crawl", action="store_true", help="RSS 수집만")
    parser.add_argument("--process", action="store_true", help="AI 처리만")
    parser.add_argument("--briefing", action="store_true", help="브리핑 생성만")
    args = parser.parse_args()

    # 아무 플래그도 없으면 전체 실행
    run_all = not (args.crawl or args.process or args.briefing)

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

    print("\n🏁 완료!")


if __name__ == "__main__":
    main()
