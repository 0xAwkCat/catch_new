from fastapi import FastAPI, HTTPException
from database import init_db, query_items, get_item

app = FastAPI(title="HackerNews 聚合 API")


@app.on_event("startup")
def startup():
    init_db()


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
