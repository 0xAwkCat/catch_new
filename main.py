from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
from database import init_db, query_items, get_item, save_stories
from fetcher import fetch_top_stories
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="HackerNews 聚合 API")
scheduler = BackgroundScheduler()


def fetch_and_save():
    logger.info("定时任务：开始拉取 HackerNews 数据...")
    stories = fetch_top_stories()
    saved = save_stories(stories)
    logger.info(f"定时任务：拉取 {len(stories)} 条，新增 {saved} 条")


@app.on_event("startup")
def startup():
    init_db()
    fetch_and_save()
    scheduler.add_job(fetch_and_save, "interval", minutes=30)
    scheduler.start()
    logger.info("定时任务已启动，每 30 分钟自动拉取一次")


@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def list_items(keyword: str = None):
    return query_items(keyword)


@app.get("/items/{item_id}")
def item_detail(item_id: int):
    item = get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="未找到该条目")
    return item
