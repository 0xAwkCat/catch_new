import sqlite3
from config import DB_PATH, KEYWORDS


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id      INTEGER PRIMARY KEY,
                title   TEXT,
                url     TEXT,
                score   INTEGER,
                time    INTEGER
            )
        """)


def matches_keyword(title: str) -> bool:
    if not title:
        return False
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in KEYWORDS)


def save_stories(stories: list[dict]):
    saved = 0
    with get_conn() as conn:
        for s in stories:
            if not matches_keyword(s.get("title", "")):
                continue
            conn.execute("""
                INSERT OR IGNORE INTO items (id, title, url, score, time)
                VALUES (:id, :title, :url, :score, :time)
            """, s)
            saved += 1
    return saved


def query_items(keyword: str = None) -> list[dict]:
    with get_conn() as conn:
        if keyword:
            rows = conn.execute(
                "SELECT * FROM items WHERE LOWER(title) LIKE ? ORDER BY score DESC",
                (f"%{keyword.lower()}%",)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM items ORDER BY score DESC"
            ).fetchall()
    return [dict(r) for r in rows]


def get_item(item_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    return dict(row) if row else None


if __name__ == "__main__":
    from fetcher import fetch_top_stories

    init_db()
    print("数据库初始化完成")

    stories = fetch_top_stories()
    saved = save_stories(stories)
    print(f"拉取 {len(stories)} 条，关键词匹配后存入 {saved} 条")

    items = query_items()
    print(f"\ndata.db 当前共 {len(items)} 条记录：")
    for item in items:
        print(f"  [{item['score']:>4}] {item['title']}")
