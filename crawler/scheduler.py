"""크롤링 스케줄러"""
from apscheduler.schedulers.background import BackgroundScheduler

from config import CRAWL_INTERVAL_MINUTES
from crawler.rss_crawler import crawl_all
from utils.helpers import log

_scheduler = None


def start_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        return

    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        crawl_all,
        "interval",
        minutes=CRAWL_INTERVAL_MINUTES,
        id="crawl_job",
        replace_existing=True,
    )
    _scheduler.start()
    log(f"[스케줄러] {CRAWL_INTERVAL_MINUTES}분 간격 자동 수집 시작")


def stop_scheduler():
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        _scheduler = None
