import httpx

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
FETCH_LIMIT = 30


def fetch_top_stories(limit: int = FETCH_LIMIT) -> list[dict]:
    with httpx.Client(timeout=10) as client:
        resp = client.get(HN_TOP_STORIES_URL)
        resp.raise_for_status()
        story_ids = resp.json()[:limit]

        stories = []
        for story_id in story_ids:
            item_resp = client.get(HN_ITEM_URL.format(id=story_id))
            item_resp.raise_for_status()
            item = item_resp.json()
            if item and item.get("type") == "story":
                stories.append({
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "score": item.get("score"),
                    "time": item.get("time"),
                })
        return stories


if __name__ == "__main__":
    print(f"Fetching top {FETCH_LIMIT} stories from HackerNews...\n")
    stories = fetch_top_stories()
    for s in stories:
        print(f"[{s['score']:>4}] {s['title']}")
        print(f"       id={s['id']}  url={s['url']}  time={s['time']}")
        print()
    print(f"Total: {len(stories)} stories fetched.")
