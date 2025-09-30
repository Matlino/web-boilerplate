# Web Boilerplate

### Backend 
- Run dev server: `uvicorn web_boilerplate.main:app --reload`
- Default route: `GET /` returns `{ "status": "ok" }`
- DB health: `GET /health/db`


### Front end 
- `cd frontend && pnpm run dev`
- (`nvm use node` if needed before)


### PostgreSQL (local)

1. Start Postgres:
   - `docker compose up -d postgres`
2. Connection URL (default):
   - `postgresql+asyncpg://postgres:postgres@localhost:5432/app_db`
3. App configuration:
   - Create `.env` in repo root (optional):
     - `DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/app_db`
4. Test DB health endpoint:
   - `curl http://localhost:8000/health/db`
