# F1 Driver Stats

A Streamlit app that displays Formula 1 driver statistics and standings, powered by manually maintained flat files.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Repository Structure](#repository-structure)
3. [Technology Stack](#technology-stack)
4. [Environment Strategy](#environment-strategy)
5. [Pre-Flight Checklist](#pre-flight-checklist)
6. [Implementation Stories](#implementation-stories)
7. [Secrets & Config Management](#secrets--config-management)
8. [Definition of Done](#definition-of-done)

---

## Architecture Overview

```
Browser
  │
  ▼
Fly.io Machine (scale to zero)
  │
  ▼
Streamlit App (Python)
  │
  ├── Season selector (sidebar)
  ├── Driver standings table
  ├── Driver stat charts (plotly)
  └── Data (CSV/JSON flat files — no DB needed)
```

### Key Design Decisions

- **Flat files as the data layer** — F1 data is manually maintained and season-scoped. A versioned CSV/JSON file per season in the repo is simple, auditable, and requires no database.
- **Scale to zero** — hosted on a Fly.io Machine with `min_machines_running = 0`. Costs nothing when idle, wakes in ~2-3 seconds.
- **Streamlit only** — no reverse proxy needed. Fly.io handles TLS. Personal site embeds via iframe using the Fly.io URL.
- **Extensibility** — adding a new season means adding a new data file. No code change required.

---

## Repository Structure

```
f1-driver-stats/
├── README.md
├── fly.toml                    ← Fly.io machine config (scale to zero)
├── Dockerfile
├── requirements.txt
├── .streamlit/
│   └── config.toml             ← disable toolbar for clean iframe embed
├── app/
│   ├── main.py                 ← Streamlit entry point
│   ├── charts.py               ← Plotly chart rendering
│   ├── standings.py            ← standings table logic
│   ├── data.py                 ← data loading + season filtering
│   └── components/
│       ├── season_selector.py
│       └── driver_card.py
└── data/
    ├── 2024.csv                ← one file per season
    ├── 2025.csv
    └── schema.md               ← documents columns and data format
```

---

## Technology Stack

| Layer | Technology | Reason |
|---|---|---|
| App framework | Streamlit | Already in use; rapid iteration |
| Charts | Plotly | Interactive charts, native Streamlit support |
| Data | json files (one per season) | Manual maintenance, no DB overhead, version controlled |
| Hosting | Fly.io (scale to zero) | $0 when idle, Docker-native, fast cold start |
| CI/CD | GitHub Actions | Auto-deploy on push to `main` |

---

## Environment Strategy

| | Local | Production (Fly.io) |
|---|---|---|
| Run command | `streamlit run app/main.py` | Docker via Fly Machine |
| URL | `http://localhost:8501` | `https://f1.brandonlocke.xyz` |
| Data | `data/*.csv` | Same files, baked into image |
| Secrets | None needed | None needed |

---

## Pre-Flight Checklist

```bash
# Python env set up
python --version   # 3.12+
pip install -r requirements.txt

# App runs locally
streamlit run app/main.py

# Docker builds
docker build -t f1-driver-stats .
docker run -p 8501:8501 f1-driver-stats

# Fly CLI installed and authenticated
fly version
fly auth whoami
```

---

## Implementation Stories

---

### EPIC 1 — Code Cleanup & Structure

**Epic Goal:** Existing local Streamlit app is refactored into a clean module structure, ready for Dockerization. Behavior is identical to before.

---

#### Story 1.1 — Refactor Into Module Structure

**Context:** App is fairly complete locally as a single script (or loose files). Need clean module structure before deploying.

**Assumptions:**
- Existing app runs locally via `streamlit run`
- All data is in flat files already
- No Docker setup exists yet

**Tasks:**
- Create directory structure per [Repository Structure](#repository-structure)
- Move chart logic → `app/charts.py`
- Move standings/table logic → `app/standings.py`
- Move data loading → `app/data.py`:
  - `load_season(year: int) -> pd.DataFrame`
  - `available_seasons() -> list[int]` — scans `data/` for CSV files
- Move season selector UI → `app/components/season_selector.py`
- Move driver detail UI → `app/components/driver_card.py`
- `app/main.py` — entry point only, composes components
- Standardize all data files to match `data/schema.md`
- Write `data/schema.md` documenting all columns, types, and valid values
- Pin all deps in `requirements.txt`

**Out of Scope:** Any new features, Docker, deployment.

**Acceptance Criteria:**
- [ ] `streamlit run app/main.py` — identical behavior to original app
- [ ] No business logic in `main.py` — composes only
- [ ] `available_seasons()` correctly detects all CSV files in `data/`
- [ ] `pip install -r requirements.txt` installs cleanly in a fresh venv
- [ ] All existing data files pass schema validation (no missing columns)

---

#### Story 1.2 — Streamlit Config for Iframe Embed

**Context:** Story 1.1 complete. App runs locally in modular form.

**Assumptions:**
- App will be embedded via iframe on the personal site
- Should match the aesthetic established by the Bobiverse tracker

**Tasks:**
- Create `.streamlit/config.toml`:
  ```toml
  [server]
  headless = true
  address = "0.0.0.0"
  port = 8501

  [client]
  toolbarMode = "minimal"
  showSidebarNavigation = false

  [theme]
  base = "dark"
  primaryColor = "#e10600"       # F1 red
  backgroundColor = "#1a1a1a"
  secondaryBackgroundColor = "#2d2d2d"
  textColor = "#ffffff"
  ```
- Verify toolbar hidden at 800px wide viewport
- Verify theme renders cleanly on dark background

**Acceptance Criteria:**
- [ ] `streamlit run app/main.py` — no Streamlit toolbar visible
- [ ] App renders cleanly at 800px wide
- [ ] F1 red theme applied consistently across charts and UI elements

---

### EPIC 1 Integration Gate

- [ ] `streamlit run app/main.py` — app loads, standings render, charts work
- [ ] Season selector populates from available CSV files automatically
- [ ] Switching seasons updates all views correctly
- [ ] No visible Streamlit toolbar
- [ ] App usable at 800px wide viewport

---

### EPIC 2 — Feature Polish

**Epic Goal:** App is visually polished and data is easy to navigate. Ready to be a public-facing project on the personal site.

---

#### Story 2.1 — Season Selector & Data Navigation

**Context:** Epic 1 complete. App is structured and styled.

**Assumptions:**
- Multiple season CSV files exist in `data/`
- Season selector currently works but may be basic

**Tasks:**
- Sidebar: season dropdown populated from `available_seasons()`
- Default to the most recent season on load
- Show season summary stats at top: total races, champion, dominant team
- "Compare seasons" toggle — side-by-side stat comparison of two seasons (optional stretch goal, clearly marked as stretch)

**Acceptance Criteria:**
- [ ] Season dropdown shows all available seasons, sorted descending
- [ ] Defaults to latest season on load
- [ ] Season summary bar visible at top of page
- [ ] Switching seasons updates all charts and tables without error

---

#### Story 2.2 — Standings Table Polish

**Context:** Story 2.1 complete.

**Tasks:**
- Standings table columns: Position, Driver, Team, Points, Wins, Podiums, Poles
- Team color coded — each constructor has a distinct color accent
- Sortable by any column
- Highlight championship leader row
- Mobile-friendly: table scrolls horizontally on narrow viewports

**Acceptance Criteria:**
- [ ] Table renders all columns from schema
- [ ] Clicking a column header sorts correctly
- [ ] Championship leader row visually distinct
- [ ] Table scrolls horizontally at 400px width without breaking layout

---

#### Story 2.3 — Driver Detail & Charts

**Context:** Story 2.2 complete.

**Tasks:**
- Clicking a driver row opens a detail panel (or expander) showing:
  - Points progression chart (if race-by-race data available; otherwise season totals)
  - Wins / Podiums / Poles breakdown (bar chart)
  - DNF count and percentage
  - Head-to-head vs teammate (points delta)
- Charts use F1 red theme from `config.toml`
- If race-by-race data not available, show season aggregate charts only (no error)

**Acceptance Criteria:**
- [ ] Clicking any driver opens detail panel
- [ ] All charts render without console errors
- [ ] Detail panel closes/collapses cleanly
- [ ] Graceful fallback if race-by-race data is absent

---

### EPIC 2 Integration Gate

- [ ] Full user journey: load app → select season → click driver → detail charts render
- [ ] All seasons in `data/` load without errors
- [ ] No Python exceptions during normal navigation
- [ ] App usable on mobile viewport (600px)

---

### EPIC 3 — Dockerization

**Epic Goal:** App runs identically in Docker as locally. Image is lean and healthy.

---

#### Story 3.1 — Dockerfile

**Context:** Epic 2 complete. App fully functional locally.

**Assumptions:**
- Python 3.12
- All deps in `requirements.txt`
- Data files baked into image (no external volume)

**Tasks:**
- Multi-stage Dockerfile:
  - Builder: `python:3.12-slim`, install deps
  - Runner: copy app + data, run Streamlit
- `HEALTHCHECK` via `curl http://localhost:8501/_stcore/health`
- Non-root user
- `.dockerignore` — exclude `.git`, `__pycache__`, venv, local `.streamlit` overrides

**Acceptance Criteria:**
- [ ] `docker build -t f1-driver-stats .` succeeds
- [ ] `docker run -p 8501:8501 f1-driver-stats` — app accessible at `http://localhost:8501`
- [ ] Healthcheck passes after 30 seconds
- [ ] Image under 500MB
- [ ] App behavior identical to `streamlit run`

---

### EPIC 3 Integration Gate

- [ ] `docker build` succeeds cleanly
- [ ] `docker run` — full app works, standings render, charts work
- [ ] Healthcheck healthy after 30 seconds
- [ ] `docker stop` — exits within 10 seconds

---

### EPIC 4 — Fly.io Deployment

**Epic Goal:** App live at `https://f1.brandonlocke.xyz`, scales to zero, auto-deploys on push to `main`.

---

#### Story 4.1 — Fly.io App Setup

**Context:** Story 3.1 complete. Docker image works locally.

**Assumptions:**
- `fly` CLI installed and authenticated
- Bobiverse tracker already deployed — follow the same pattern
- Cloudflare DNS available for `brandonlocke.xyz`

**Tasks:**
- `fly launch` — app name `f1-driver-stats`, nearest region
- Write `fly.toml` (mirror Bobiverse pattern):
  ```toml
  [build]

  [[services]]
    internal_port = 8501
    protocol = "tcp"

    [[services.ports]]
      handlers = ["http"]
      port = 80

    [[services.ports]]
      handlers = ["tls", "http"]
      port = 443

    [services.concurrency]
      type = "connections"
      hard_limit = 10
      soft_limit = 5

  [[services.http_checks]]
    path = "/_stcore/health"
    interval = "15s"
    timeout = "5s"

  [machines]
    min_machines_running = 0
  ```
- `fly deploy`
- `fly certs add f1.brandonlocke.xyz`
- Cloudflare DNS CNAME: `f1` → `f1-driver-stats.fly.dev`

**Acceptance Criteria:**
- [ ] `fly deploy` succeeds
- [ ] `https://f1-driver-stats.fly.dev` — app loads
- [ ] `https://f1.brandonlocke.xyz` — app loads after DNS propagation
- [ ] `fly scale show` — `min_machines_running = 0` confirmed
- [ ] Cold start test: scale to zero → visit URL → app wakes within 5 seconds

---

#### Story 4.2 — GitHub Actions CI/CD

**Context:** Story 4.1 complete.

**Tasks:**
- `.github/workflows/deploy.yml` — lint + deploy on push to `main`
- `.github/workflows/pr-check.yml` — lint on PRs only
- `FLY_API_TOKEN` in GitHub repository secrets

**Acceptance Criteria:**
- [ ] Push to `main` → deploy within 5 minutes
- [ ] Lint failure → deploy blocked
- [ ] PR → lint only, no deploy

---

### EPIC 4 Integration Gate

- [ ] Cold start: scale to zero → visit URL → app loads within 5 seconds
- [ ] Push a change → GitHub Actions deploys → visible on site within 5 minutes
- [ ] `fly logs` — no errors during normal use
- [ ] Monthly cost near $0 confirmed in Fly.io dashboard

---

## Secrets & Config Management

No secrets required — all data is static and baked into the Docker image.

If a future data source (e.g. a live F1 API) requires a key:
```bash
fly secrets set API_KEY=value
```
Access in Python via `os.environ.get("API_KEY")`.

---

## Adding a New Season

1. Create `data/YYYY.csv` following `data/schema.md`
2. Commit and push to `main`
3. GitHub Actions deploys automatically
4. New season appears in the season selector on next app load

No code changes required.

---

## Definition of Done

- [ ] All acceptance criteria pass
- [ ] `streamlit run app/main.py` works
- [ ] `docker run` works identically
- [ ] No secrets committed
- [ ] `data/schema.md` updated if columns changed
- [ ] Epic integration gate passes before moving to next epic
