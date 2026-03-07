## 專案簡介

這個專案會實作一個與 `simple-alias-87695966.figma.site` 1:1 的「鮮採市集」商店網站：

- **前端**：Vue 3（JavaScript）+ SCSS（Vite）
- **後端**：FastAPI（提供商品/分類 API 與假資料）

## 開發方式

### 後端（FastAPI）

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 前端（Vue）

```bash
cd frontend
npm install
npm run dev
```

預設：
- 前端：`http://localhost:5173`
- 後端：`http://localhost:8000`

