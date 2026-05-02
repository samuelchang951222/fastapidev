# 鮮採市集 — Fresh Market Online Store

一個具有完整購物車、會員系統、商品分類的線上蔬果市集網站。

- **前端**：Vue 3 (Composition API) + Vue Router + Pinia + SCSS + Vite
- **後端**：FastAPI (Python) + Supabase (資料庫/認證)
- **部署**：前後端分離開發，可合併靜態檔後由 FastAPI 統一 serve

---

## 目錄

- [系統需求](#系統需求)
- [快速開始](#快速開始)
  - [1. 後端設定](#1-後端設定)
  - [2. 前端設定](#2-前端設定)
  - [3. 啟動開發伺服器](#3-啟動開發伺服器)
- [正式上線](#正式上線)
- [常見問題](#常見問題)
- [專案結構](#專案結構)

---

## 系統需求

| 工具 | 建議版本 | 最低版本 |
|------|---------|---------|
| Python | 3.11+ | 3.10 |
| Node.js | 20+ | 18 |
| npm | 10+ | 9 |

> ⚠️ **Python 版本注意**：Raspberry Pi OS / Debian 舊版可能內建 Python 3.9，
> 請先用 `python3 --version` 確認。若版本低於 3.10，需先升級：
> ```bash
> sudo apt update && sudo apt install python3.11 python3.11-venv -y
> ```

---

## 快速開始

### 1. 後端設定

```bash
cd backend

# 建立虛擬環境
python3 -m venv .venv

# 啟動虛擬環境（Linux / macOS）
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

# 安裝依賴
pip install -r requirements.txt

# 啟動後端（開發模式，hot-reload）
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

後端 API 預設在 `http://localhost:8000`

- 測試是否正常：`curl http://localhost:8000/health`
- API 文件：`http://localhost:8000/docs`（Swagger UI）

### 2. 前端設定

**另開一個終端機視窗：**

```bash
cd frontend

# 安裝依賴
npm install

# 啟動開發伺服器（hot-reload）
npm run dev
```

前端開發伺服器在 `http://localhost:5173`

> 開發模式下，前端會把 `/api/*` 請求自動代理到後端 `localhost:8000`。

### 3. 啟動開發伺服器

同時跑兩個 terminal：

| Terminal | 指令 | 網址 |
|----------|------|------|
| 1 (後端) | `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000` | `http://localhost:8000` |
| 2 (前端) | `cd frontend && npm run dev` | `http://localhost:5173` |

---

## 正式上線

前端 build 後，FastAPI 會直接 serve 靜態檔：

```bash
cd frontend
npm run build                    # 產生 dist/ 資料夾

cd ..
uvicorn main:app --host 0.0.0.0 --port 8000
```

這樣只需開一個 port（8000），前後端都從同一個位址提供服務。

---

## 常見問題

### Python 版本太低

```bash
# 檢查目前版本
python3 --version

# Debian / Ubuntu 安裝 Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv -y

# 建立虛擬環境時指定版本
python3.11 -m venv .venv
```

### `pip install` 失敗

```bash
# 確保 pip 是最新版
python3 -m pip install --upgrade pip

# 如果缺少系統套件
sudo apt install build-essential python3-dev -y
```

### 前端 `npm install` 失敗

```bash
# 確保 Node.js 版本足夠新
node --version   # 需要 18+

# 清除快取後重試
rm -rf node_modules package-lock.json
npm install
```

### 開發時前端打不到後端 API

Vite 設定已自動 proxy `/api` 到 `localhost:8000`。
確認後端有在 8000 port 執行，且無 CORS 錯誤。

如果仍出問題，可直接設定環境變數：

```bash
# frontend/.env
VITE_API_BASE=http://localhost:8000
```

### Supabase 連線問題

後端使用 Supabase 作為資料庫。若需要更換為自己的 Supabase 專案，
編輯 `backend/app/supabase_config.py`，換上自己的 URL 和 service_role key：

```python
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-service-role-key"
```

---

## 專案結構

```
fastapidev/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI 應用入口
│       ├── schemas.py           # Pydantic 資料模型
│       ├── supabase_config.py   # Supabase 連線設定
│       └── routers/             # API 路由
│           ├── auth.py          # 註冊/登入/登出
│           ├── products.py      # 商品
│           ├── categories.py    # 分類
│           ├── flash_sales.py   # 限時搶購
│           └── orders.py        # 訂單
├── frontend/
│   ├── index.html               # 入口 HTML（含手機漢堡選單）
│   └── src/
│       ├── main.js              # Vue 應用啟動
│       ├── App.vue              # 根元件
│       ├── router/index.js      # Vue Router 路由設定
│       ├── stores/              # Pinia 狀態管理
│       │   ├── auth.js          # 認證
│       │   ├── cart.js          # 購物車
│       │   ├── catalog.js       # 商品目錄
│       │   ├── ui.js            # UI 狀態
│       │   └── toast.js         # 提示訊息
│       ├── components/          # 共用元件
│       │   ├── layout/          # HeaderNav, AppLayout, SearchPanel
│       │   ├── cart/            # 購物車抽屜
│       │   ├── product/         # 商品卡片
│       │   └── ui/              # BaseButton, ToastHost
│       ├── views/               # 頁面元件
│       │   ├── HomePage.vue     # 首頁（hero + 分類 + 精選）
│       │   ├── ShopPage.vue     # 商品列表（含篩選/排序）
│       │   ├── ProductPage.vue  # 商品詳情
│       │   ├── CheckoutPage.vue # 結帳
│       │   ├── LoginPage.vue    # 登入
│       │   ├── RegisterPage.vue # 註冊
│       │   ├── AboutPage.vue    # 關於我們
│       │   └── ContactPage.vue  # 聯絡我們
│       └── styles/
│           ├── main.scss        # 全域樣式
│           └── _tokens.scss     # 設計 token（顏色、間距）
├── main.py                      # 整合入口（正式上線用）
├── README.md
└── .gitignore
```

---

## 技術選型

| 層級 | 技術 | 用途 |
|------|------|------|
| 前端框架 | Vue 3 (Composition API) | SPA 頁面 |
| 狀態管理 | Pinia | 購物車、認證、UI |
| 路由 | Vue Router 4 | 頁面切換 |
| 建置工具 | Vite 7 | 開發伺服器 + 打包 |
| CSS | SCSS + 設計 token | 響應式樣式 |
| 後端 | FastAPI | RESTful API |
| 資料庫 | Supabase (PostgreSQL) | 商品/使用者/訂單 |
| 認證 | JWT (自製) | 註冊 / 登入 |

---

Made with 🦀 by Samuel
