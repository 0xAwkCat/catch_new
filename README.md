# HackerNews 聚合 API

从 HackerNews 拉取热门文章，按关键词过滤后存入 SQLite，通过 FastAPI 提供 REST 接口，每 30 分钟自动更新。

## 本地运行

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## 接口文档

| 方法 | 路径 | 参数 | 说明 |
|------|------|------|------|
| GET | `/health` | — | 健康检查 |
| GET | `/items` | `keyword`（可选） | 查询条目，支持关键词过滤 |
| GET | `/items/{id}` | — | 查询单条详情 |

示例：

```
GET /items?keyword=AI
GET /items/47603737
GET /health
```

## 关键词配置

在 `config.py` 中修改 `KEYWORDS` 列表，控制哪些文章会被存入数据库。

## 目录结构

```
├── main.py          # FastAPI 入口 + 定时任务
├── fetcher.py       # HackerNews 数据拉取
├── database.py      # SQLite 初始化与增删查
├── config.py        # 关键词、路径等配置
├── requirements.txt
└── railway.toml     # Railway 部署配置
```
