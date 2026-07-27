# GenXSOP — Next-Generation Sales & Operations Planning Platform

A full-stack S&OP platform built with **FastAPI** (Python) + **React** (TypeScript), applying **SOLID principles** and **GoF Design Patterns** throughout.

## 📚 Architecture Documentation

If you’re new to the codebase, start here:

- **Architecture index:** [`docs/architecture/README.md`](docs/architecture/README.md)
- **System Context (C4 L1):** [`docs/architecture/system-context.md`](docs/architecture/system-context.md)
- **Container Diagram (C4 L2):** [`docs/architecture/container.md`](docs/architecture/container.md)
- **Backend Architecture:** [`docs/architecture/backend.md`](docs/architecture/backend.md)
- **Frontend Architecture:** [`docs/architecture/frontend.md`](docs/architecture/frontend.md)
- **Data Model:** [`docs/architecture/data-model.md`](docs/architecture/data-model.md)
- **Runtime & Deployment:** [`docs/architecture/runtime-deployment.md`](docs/architecture/runtime-deployment.md)
- **Cross-cutting Concerns:** [`docs/architecture/cross-cutting.md`](docs/architecture/cross-cutting.md)
- **ADRs:** [`docs/adr/README.md`](docs/adr/README.md)
- **C4 L3 Components (Forecasting):** [`docs/architecture/components-forecasting.md`](docs/architecture/components-forecasting.md)

## 🧭 How to use GenXSOP

- **User Guide (UI walkthrough):** [`docs/user-guide.md`](docs/user-guide.md)
- **Developer / API Guide:** [`docs/api-guide.md`](docs/api-guide.md)
- **Docs index:** [`docs/README.md`](docs/README.md)
- **Forecasting GenXAI enhancements:** [`docs/forecasting-genxai-enhancements.md`](docs/forecasting-genxai-enhancements.md)

## 🧰 API tooling

- **Postman collection:** [`docs/postman/GenXSOP.postman_collection.json`](docs/postman/GenXSOP.postman_collection.json)
- **Postman environment:** [`docs/postman/GenXSOP.postman_environment.json`](docs/postman/GenXSOP.postman_environment.json)

---

## 🏗️ Architecture Overview

```
GenXSOP/
├── backend/                    # FastAPI Python backend
│   └── app/
│       ├── core/               # Exception hierarchy (SRP)
│       ├── models/             # SQLAlchemy ORM models
│       ├── schemas/            # Pydantic request/response schemas
│       ├── repositories/       # Repository Pattern (GoF) — data access
│       ├── services/           # Service Layer (SRP/DIP) — business logic
│       ├── routers/            # Thin Controllers (SRP) — HTTP only
│       ├── ml/                 # Strategy + Factory Patterns — AI forecasting
│       └── utils/              # Observer Pattern (GoF) — EventBus/audit log
└── frontend/                   # React + TypeScript frontend
```

### Design Patterns Applied

| Pattern | Location | Purpose |
|---------|----------|---------|
| **Repository Pattern** (GoF) | `repositories/` | Abstracts data access; swappable DB backends |
| **Service Layer** (SRP/DIP) | `services/` | Business logic separated from HTTP concerns |
| **Strategy Pattern** (GoF) | `ml/strategies.py` | Interchangeable ML forecasting algorithms |
| **Factory Pattern** (GoF) | `ml/factory.py` | Centralized strategy creation & auto-selection |
| **Observer Pattern** (GoF) | `utils/events.py` | EventBus for decoupled audit logging |
| **Thin Controllers** (SRP) | `routers/` | Routers only handle HTTP routing & auth |

### SOLID Principles

- **S** — Each class has one responsibility (Service, Repository, Router are separate)
- **O** — Add new forecasting models by registering in `ForecastModelFactory`, not modifying existing code
- **L** — All repositories are substitutable for `BaseRepository[T]`
- **I** — Schemas are split by use case (Create, Update, Response, List)
- **D** — Routers depend on Service abstractions; Services depend on Repository abstractions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or SQLite for development)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL and secret key

# Run the server
python run.py

# Optional: enforce migration-only startup behavior
# export AUTO_CREATE_TABLES=false
```

The API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health**: http://localhost:8000/health

### Production DB safety notes

- Set `ENVIRONMENT=production` in production deployments.
- Use PostgreSQL (SQLite is blocked in production mode).
- Set a non-default `SECRET_KEY`.
- Set `AUTO_CREATE_TABLES=false` and apply schema changes via Alembic migrations.

### Database migrations

`alembic upgrade head` builds the full schema from empty and produces a database
identical to `Base.metadata`. Alembic reads its URL from `app.config.settings`,
so it always targets the same database as the API.

```bash
cd backend
python scripts/db_bootstrap.py --check   # report the database's state
alembic upgrade head                     # apply outstanding revisions
alembic revision --autogenerate -m "..." # author a new revision
```

Databases created before the migration chain existed have no `alembic_version`
row. Adopt one with `python scripts/db_bootstrap.py --stamp-legacy`; note that
stamping records the version but does **not** retrofit constraints the database
never received — `--check` lists which tables are affected, and a full rebuild
(`--fresh` into a new file) is the only way to obtain a hardened schema.

Every revision must run under SQLite as well as PostgreSQL, so constraint and
column changes belong inside `op.batch_alter_table(...)`: SQLite cannot `ALTER`
constraints in place.

Run preflight check before deployment:

```bash
cd backend
python scripts/db_preflight.py
```

Run migration governance gate (CI/local):

```bash
cd backend
bash scripts/ci_migration_gate.sh
```

Backup + restore verification helper:

```bash
cd backend
SOURCE_DATABASE_URL='postgresql://user:pass@host:5432/genxsop' \
RESTORE_DATABASE_URL='postgresql://user:pass@host:5432/genxsop_restore_check' \
bash scripts/backup_restore_runbook.sh
```

### Seed Sample Data

```bash
cd backend
python seed_data.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: http://localhost:5173

---

## 📡 API Endpoints

| Module | Prefix | Description |
|--------|--------|-------------|
| Auth | `/api/v1/auth` | Login, register, JWT tokens |
| Dashboard | `/api/v1/dashboard` | Executive summary, alerts, S&OP status |
| Products | `/api/v1/products` | Product & category management |
| Demand | `/api/v1/demand` | Demand plans, adjustments, approvals |
| Supply | `/api/v1/supply` | Supply plans, gap analysis |
| Inventory | `/api/v1/inventory` | Inventory tracking, health, alerts |
| Forecasting | `/api/v1/forecasting` | AI forecast generation, accuracy metrics |
| Scenarios | `/api/v1/scenarios` | What-if scenario planning & comparison |
| S&OP Cycles | `/api/v1/sop-cycles` | 5-step S&OP cycle management |
| KPI | `/api/v1/kpi` | KPI tracking, targets, alerts |

---

## 🤖 AI Forecasting Models

The forecasting engine uses the **Strategy + Factory** pattern:

| Model | ID | Min Data | Best For |
|-------|----|----------|----------|
| Moving Average | `moving_average` | 3 months | Short history, simple trends |
| Exponential Smoothing (Holt-Winters) | `exp_smoothing` | 12 months | Trend + seasonality |
| Prophet (Facebook) | `prophet` | 24 months | Complex seasonality, holidays |

**Auto-selection**: Pass `model_type=null` to `POST /api/v1/forecasting/generate` and the Factory will automatically select the best model based on available data history.

**Add a new model** (OCP):
```python
# 1. Create a new strategy class
class MyCustomStrategy(BaseForecastStrategy):
    @property
    def model_id(self) -> str: return "my_model"
    ...

# 2. Register it — no existing code modified
ForecastModelFactory.register("my_model", MyCustomStrategy)
```

---

## 📊 S&OP 5-Step Process

```
Step 1: Data Gathering    → Collect historical data, market intelligence
Step 2: Demand Review     → Statistical + qualitative demand consensus
Step 3: Supply Review     → Capacity, constraints, gap analysis
Step 4: Pre-S&OP          → Cross-functional reconciliation
Step 5: Executive S&OP    → Leadership decisions, plan approval
```

Use `POST /api/v1/sop-cycles/{id}/advance` to progress through steps.

---

## 🔐 User Roles

| Role | Permissions |
|------|-------------|
| `admin` | Full access |
| `executive` | View all, approve plans & scenarios |
| `sop_coordinator` | Manage S&OP cycles, all plans |
| `demand_planner` | Create/edit demand plans, run forecasts |
| `supply_planner` | Create/edit supply plans, inventory |
| `finance_analyst` | View all, create scenarios |
| `inventory_manager` | Manage inventory |

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## 🐳 Docker

```bash
docker-compose up --build
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/app/core/exceptions.py` | Domain exception hierarchy |
| `backend/app/repositories/base.py` | Generic BaseRepository[T] |
| `backend/app/ml/strategies.py` | Forecasting Strategy Pattern |
| `backend/app/ml/factory.py` | Forecasting Factory Pattern |
| `backend/app/utils/events.py` | Observer Pattern / EventBus |
| `backend/app/services/` | All business logic services |
| `backend/app/main.py` | App entry point, exception handlers, startup |
