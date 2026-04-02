# 公开数据聚合 API — 项目任务与目录结构

## 项目目标

从 HackerNews 拉取公开数据，按关键词过滤后落库，通过 FastAPI 暴露 REST 接口，最终部署上线。

---

## 任务清单

### Stage 1 — 数据拉取
- [ ] 安装依赖：`pip install httpx`
- [ ] 编写 `fetcher.py`，从 HackerNews API 拉取 Top Stories
- [ ] 打印原始数据，确认字段结构（id / title / url / score / time）

### Stage 2 — 数据清洗与存储
- [ ] 安装依赖：`pip install sqlite3`（内置，无需安装）
- [ ] 编写 `database.py`，初始化 SQLite 数据库和表结构
- [ ] 编写关键词过滤逻辑，只存入匹配的条目
- [ ] 验证：查看 `data.db` 中是否有数据

### Stage 3 — API 接口
- [ ] 安装依赖：`pip install fastapi uvicorn`
- [ ] 编写 `main.py`，实现 `/items?keyword=xxx` 接口
- [ ] 本地运行：`uvicorn main:app --reload`
- [ ] 验证：浏览器访问 `http://localhost:8000/items?keyword=AI`

### Stage 4 — 定时任务
- [ ] 安装依赖：`pip install apscheduler`
- [ ] 在 `main.py` 中集成定时拉取（每 30 分钟执行一次）
- [ ] 验证：等待一个周期，确认数据库自动更新

### Stage 5 — 部署上线
- [ ] 编写 `requirements.txt`
- [ ] 编写 `Procfile` 或 `railway.toml`
- [ ] 推送代码到 GitHub
- [ ] 在 Railway / Render 上一键部署
- [ ] 验证：用公网 URL 访问接口

---

## 目录结构

```
hn-api/
│
├── main.py              # FastAPI 入口，路由 + 定时任务
├── fetcher.py           # 数据拉取逻辑（HackerNews API）
├── database.py          # 数据库初始化 + 增删查操作
├── config.py            # 配置项（关键词列表、拉取数量等）
│
├── data.db              # SQLite 数据库（本地运行生成，不提交 git）
│
├── requirements.txt     # 依赖列表
├── .gitignore           # 忽略 data.db、__pycache__ 等
└── README.md            # 项目说明 + 接口文档
```

---

## 接口设计

| 方法 | 路径 | 参数 | 说明 |
|------|------|------|------|
| GET | `/items` | `keyword`（可选） | 查询所有条目，支持关键词过滤 |
| GET | `/items/{id}` | — | 查询单条详情 |
| GET | `/health` | — | 服务健康检查 |

---

## 依赖清单（requirements.txt）

```
httpx
fastapi
uvicorn
apscheduler
```

---

## 里程碑

| 天数 | 目标 | 验收标准 |
|------|------|---------|
| Day 1 | Stage 1 完成 | 终端打印出 HN 数据 |
| Day 2-3 | Stage 2 完成 | data.db 中有记录 |
| Day 4-5 | Stage 3 完成 | 本地接口返回 JSON |
| Day 6 | Stage 4 完成 | 数据自动刷新 |
| Day 7-10 | Stage 5 完成 | 公网可访问 |