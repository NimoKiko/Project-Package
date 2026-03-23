# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal utility platform with a Vue 3 frontend (`tools/`) and a Python FastAPI backend (`toolsbackend/`). The two services are developed and run independently — no shared monorepo tooling.

Current tools:
- **Audio conversion** — converts audio files between formats via `pydub`
- **PDF operations** — alternating-page merge of two PDFs, and page-reversal of a single PDF via `PyPDF2`

A User CRUD module exists but the database (Tortoise-ORM/MySQL) integration is currently commented out in `main.py`.

---

## Frontend (`tools/`)

**Stack:** Vue 3 + TypeScript 5.8 + Vite 7 + Element Plus + Pinia + Vue Router + Axios + SCSS

```bash
cd tools
npm install
npm run dev        # dev server (http://localhost:5173)
npm run build      # vue-tsc type-check + vite build
npm run preview    # preview production build
```

**Path alias:** `@` maps to `src/`.

**Backend URL config:** At startup, `main.ts` fetches `public/config.json` and stores `BASE_URL` in localStorage. For local dev the default is `http://127.0.0.1:8000`. Edit `tools/public/config.json` to change it.

**Architecture:**
- `src/main.ts` — app entry: registers ElementPlus (zh-CN locale), Pinia, Router, loads config
- `src/App.vue` — root component, just a `<router-view>`
- `src/views/home.vue` — main layout shell (Header + Side sidebar + nested `<router-view>`)
- `src/views/modules/` — one sub-folder per tool feature
- `src/api/` — Axios API call modules (one file per backend router)
- `src/stores/modules/` — Pinia store modules (one per feature)
- `src/utils/request.ts` — Axios instance with request/response interceptors
- `src/utils/URL.ts` — helpers to read/write `BASE_URL` from localStorage
- `src/router/index.ts` — Vue Router config (HTML5 history mode, lazy-loaded routes)

---

## Backend (`toolsbackend/`)

**Stack:** Python + FastAPI 0.116 + Uvicorn + Pydantic v2 + PyPDF2 + pydub

```bash
cd toolsbackend

# First-time setup
python -m venv toolkitenv
source toolkitenv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt

# Run dev server (port 8000, auto-reload)
python main.py
# or: uvicorn main:app --reload --port 8000
```

**Architecture:**
- `main.py` — FastAPI app entry: CORS (fully open), registers routers at `/user`, `/audio`, `/pdf`
- `api/<Feature>/routes.py` — router per feature
- `api/Pdf/Services/pdfOperate.py` — PDF business logic extracted into a service layer
- `models/User.py` — Tortoise-ORM User model (DB integration currently disabled)
- `settings.py` — Tortoise-ORM MySQL config (`localhost:3306`, db `templateProject`, user `root/root`)

**To re-enable the database:** uncomment the Tortoise-ORM `register_tortoise` block in `main.py` and ensure MySQL is running.

**Aerich migrations** (when DB is active):
```bash
aerich init -t settings.TORTOISE_ORM
aerich init-db
aerich migrate
aerich upgrade
```