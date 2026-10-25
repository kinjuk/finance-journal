# Optimization Lab
Portfolio optimizer: React + TypeScript frontend, FastAPI + SciPy backend. Sharpe, Sortino and min-volatility objectives, efficient frontier, constraint-binding diagnostics, any Yahoo ticker.

Live: https://opt-lab.vercel.app/
 
    backend/   FastAPI + SciPy SLSQP engine, validated endpoint, pytest suite
    frontend/  Vite + React + TypeScript, Recharts, design tokens, dark/light, vitest
 
## Run locally
    cd backend  && pip install -r requirements-dev.txt && uvicorn main:app --reload      # :8000
    cd frontend && cp .env.example .env && npm install && npm run dev                     # :5173
 
## Deploy (free tiers)
1. **Backend → Render** (New Web Service, root `backend`, Docker). Set `ALLOWED_ORIGINS` to your frontend URL.
2. **Frontend → Vercel** (root `frontend`). Set `VITE_API_URL` to the Render URL.
Free Render instances sleep when idle; the UI shows a "waking the server" note after 4 s.
## Design decisions
- One endpoint, one JSON contract (`frontend/src/types.ts` mirrors it); objectives are interchangeable.
- Constraints validated server-side (feasibility, ticker format, date order) and surfaced as readable errors.
- Return estimator is switchable: arithmetic (consistent with covariance) or the legacy compounded log-mean.
- Results are historical, in-sample estimates, not forecasts.
## Roadmap
Risk tab (correlation, drawdown), projection fan, diagnostics/export, sensitivity-to-cap chart.
