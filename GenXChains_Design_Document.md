# GenXChains — Comprehensive Design Document
## Next-Generation Sales & Operations Planning Platform

**Version:** 1.0  
**Date:** February 25, 2026  
**Author:** GenXChains Team  

---

## Table of Contents

1. [Executive Summary & Vision](#1-executive-summary--vision)
2. [System Architecture & Tech Stack](#2-system-architecture--tech-stack)
3. [Database Schema Design](#3-database-schema-design)
4. [API Design & Endpoints](#4-api-design--endpoints)
5. [Frontend Component Architecture](#5-frontend-component-architecture)
6. [Feature Specifications](#6-feature-specifications)
7. [AI/ML Model Specifications](#7-aiml-model-specifications)
8. [Security & Authentication](#8-security--authentication)
9. [UI/UX Design](#9-uiux-design)
10. [Deployment Strategy](#10-deployment-strategy)
11. [Roadmap & Milestones](#11-roadmap--milestones)

---

## 1. Executive Summary & Vision

### 1.1 Purpose
GenXChains is a **next-generation Sales & Operations Planning (S&OP) platform** designed to transform how organizations align demand, supply, and financial plans. It replaces fragmented spreadsheet-based planning with an integrated, AI-powered, collaborative platform that drives better business decisions.

### 1.2 Vision Statement
*"To empower organizations with intelligent, real-time, and collaborative S&OP capabilities that bridge the gap between strategic intent and operational execution."*

### 1.3 Key Value Propositions
| Value | Description |
|-------|-------------|
| **Unified Planning Hub** | Single platform for demand, supply, inventory, and financial planning |
| **AI-Driven Intelligence** | Machine learning forecasting, anomaly detection, and demand sensing |
| **Scenario Simulation** | What-if analysis with side-by-side scenario comparison |
| **Collaborative Workflows** | Structured 5-step S&OP cycle with role-based collaboration |
| **Real-Time Dashboards** | Executive-level KPI dashboards with drill-down analytics |
| **Decision Acceleration** | Reduce S&OP cycle time from weeks to days |

### 1.4 Target Users
| Role | Responsibilities |
|------|-----------------|
| **Executive / VP** | Review integrated plans, approve scenarios, make strategic decisions |
| **Demand Planner** | Create/adjust demand forecasts, analyze market signals, build consensus |
| **Supply Planner** | Manage capacity, production schedules, supplier constraints |
| **Inventory Manager** | Monitor stock levels, safety stock, reorder points |
| **Finance Analyst** | Validate financial impact of plans, margin analysis |
| **S&OP Coordinator** | Manage the monthly S&OP cycle, facilitate meetings |

### 1.5 Business Outcomes
- **15-30% improvement** in forecast accuracy
- **20-40% reduction** in excess inventory
- **10-25% improvement** in customer service levels (OTIF)
- **50% faster** S&OP cycle completion
- **Single source of truth** across all planning functions

---

## 2. System Architecture & Tech Stack

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              React 18 + TypeScript + Vite                │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │    │
│  │  │Dashboard │ │ Demand   │ │ Supply   │ │ Scenarios │  │    │
│  │  │  Module  │ │ Planning │ │ Planning │ │  Builder  │  │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │    │
│  │  │Inventory │ │Forecasting│ │ S&OP    │ │   KPI     │  │    │
│  │  │ Manager  │ │   AI/ML  │ │ Workflow │ │ Analytics │  │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │ REST API (JSON)                       │
├─────────────────────────────────────────────────────────────────┤
│                        API LAYER                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              FastAPI (Python 3.11+)                       │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │    │
│  │  │  Auth    │ │ Demand   │ │ Supply   │ │ Scenario  │  │    │
│  │  │ Router   │ │ Router   │ │ Router   │ │  Router   │  │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │    │
│  │  │Inventory │ │Forecast  │ │ Workflow │ │   KPI     │  │    │
│  │  │ Router   │ │ Router   │ │ Router   │ │  Router   │  │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
├─────────────────────────────────────────────────────────────────┤
│                     SERVICE LAYER                                │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐    │
│  │Business Logic│ │  ML/AI Engine │ │  Workflow Engine     │    │
│  │  Services    │ │  (Prophet,    │ │  (Cycle Management,  │    │
│  │              │ │   sklearn)    │ │   Approvals)         │    │
│  └──────────────┘ └──────────────┘ └──────────────────────┘    │
│                          │                                       │
├─────────────────────────────────────────────────────────────────┤
│                      DATA LAYER                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │         SQLAlchemy ORM + Alembic Migrations              │    │
│  │  ┌─────────────────┐    ┌─────────────────────────┐     │    │
│  │  │  SQLite (Dev)    │ →  │  PostgreSQL (Production) │     │    │
│  │  └─────────────────┘    └─────────────────────────┘     │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Tech Stack Details

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend Framework** | React 18 + TypeScript | Component-based UI with type safety |
| **Build Tool** | Vite | Fast development server & optimized builds |
| **CSS Framework** | TailwindCSS | Utility-first styling for rapid UI development |
| **Charts** | Recharts + Nivo | Interactive data visualizations |
| **Data Tables** | TanStack Table (React Table v8) | Advanced tables with sorting, filtering, pagination |
| **State Management** | Zustand | Lightweight, scalable state management |
| **HTTP Client** | Axios | API communication with interceptors |
| **Routing** | React Router v6 | Client-side routing with nested layouts |
| **Backend Framework** | FastAPI (Python 3.11+) | High-performance async API framework |
| **ORM** | SQLAlchemy 2.0 | Database abstraction with async support |
| **Migrations** | Alembic | Database schema versioning |
| **Auth** | python-jose + passlib | JWT token generation & password hashing |
| **Validation** | Pydantic v2 | Request/response data validation |
| **ML/Forecasting** | Prophet, scikit-learn, statsmodels | Time series forecasting & ML models |
| **Data Processing** | pandas, numpy | Data manipulation & numerical computing |
| **Database (Dev)** | SQLite | Lightweight development database |
| **Database (Prod)** | PostgreSQL | Production-grade relational database |
| **Testing** | pytest (backend), Vitest (frontend) | Unit & integration testing |

### 2.3 Project Directory Structure

```
GenXChains/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI application entry point
│   │   ├── config.py                    # Configuration & environment variables
│   │   ├── database.py                  # Database connection & session management
│   │   ├── dependencies.py             # Shared dependencies (auth, db session)
│   │   │
│   │   ├── models/                      # SQLAlchemy ORM Models
│   │   │   ├── __init__.py
│   │   │   ├── user.py                  # User & Role models
│   │   │   ├── product.py              # Product, Category, SKU hierarchy
│   │   │   ├── demand_plan.py          # Demand forecasts & actuals
│   │   │   ├── supply_plan.py          # Supply/production plans
│   │   │   ├── inventory.py            # Inventory levels & movements
│   │   │   ├── forecast.py             # ML forecast results
│   │   │   ├── scenario.py             # What-if scenarios
│   │   │   ├── sop_cycle.py            # S&OP cycle & workflow
│   │   │   ├── kpi_metric.py           # KPI definitions & values
│   │   │   └── comment.py              # Collaboration comments
│   │   │
│   │   ├── schemas/                     # Pydantic Request/Response Schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   ├── demand.py
│   │   │   ├── supply.py
│   │   │   ├── inventory.py
│   │   │   ├── forecast.py
│   │   │   ├── scenario.py
│   │   │   ├── sop_cycle.py
│   │   │   └── kpi.py
│   │   │
│   │   ├── routers/                     # API Route Handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                  # Authentication endpoints
│   │   │   ├── users.py                 # User management
│   │   │   ├── dashboard.py            # Dashboard aggregation
│   │   │   ├── products.py             # Product CRUD
│   │   │   ├── demand.py               # Demand planning endpoints
│   │   │   ├── supply.py               # Supply planning endpoints
│   │   │   ├── inventory.py            # Inventory management
│   │   │   ├── forecasting.py          # AI forecasting endpoints
│   │   │   ├── scenarios.py            # Scenario management
│   │   │   ├── sop_cycle.py            # S&OP workflow endpoints
│   │   │   └── kpi.py                  # KPI & analytics endpoints
│   │   │
│   │   ├── services/                    # Business Logic Layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── demand_service.py
│   │   │   ├── supply_service.py
│   │   │   ├── inventory_service.py
│   │   │   ├── forecast_service.py
│   │   │   ├── scenario_service.py
│   │   │   ├── workflow_service.py
│   │   │   └── kpi_service.py
│   │   │
│   │   ├── ml/                          # AI/ML Engine
│   │   │   ├── __init__.py
│   │   │   ├── demand_forecasting.py   # Time series forecasting models
│   │   │   ├── demand_sensing.py       # ML-based demand sensing
│   │   │   ├── anomaly_detection.py    # Anomaly detection algorithms
│   │   │   └── optimization.py         # Supply/inventory optimization
│   │   │
│   │   └── utils/                       # Utility functions
│   │       ├── __init__.py
│   │       ├── helpers.py
│   │       └── constants.py
│   │
│   ├── alembic/                         # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── seed_data.py                     # Sample data seeder
│   └── run.py                           # Server startup script
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── main.tsx                     # React entry point
│   │   ├── App.tsx                      # Root component with routing
│   │   ├── index.css                    # Global styles + Tailwind
│   │   │
│   │   ├── components/                  # Reusable UI Components
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.tsx          # Navigation sidebar
│   │   │   │   ├── Header.tsx           # Top header bar
│   │   │   │   ├── MainLayout.tsx       # Page layout wrapper
│   │   │   │   └── Breadcrumb.tsx
│   │   │   ├── common/
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── DataTable.tsx
│   │   │   │   ├── KPICard.tsx
│   │   │   │   ├── StatusBadge.tsx
│   │   │   │   └── LoadingSpinner.tsx
│   │   │   ├── charts/
│   │   │   │   ├── LineChart.tsx
│   │   │   │   ├── BarChart.tsx
│   │   │   │   ├── WaterfallChart.tsx
│   │   │   │   ├── HeatMap.tsx
│   │   │   │   └── GaugeChart.tsx
│   │   │   ├── dashboard/
│   │   │   ├── demand/
│   │   │   ├── supply/
│   │   │   ├── inventory/
│   │   │   ├── forecasting/
│   │   │   ├── scenarios/
│   │   │   ├── workflow/
│   │   │   └── kpi/
│   │   │
│   │   ├── pages/                       # Page-level Components
│   │   │   ├── LoginPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── DemandPlanningPage.tsx
│   │   │   ├── SupplyPlanningPage.tsx
│   │   │   ├── InventoryPage.tsx
│   │   │   ├── ForecastingPage.tsx
│   │   │   ├── ScenariosPage.tsx
│   │   │   ├── SOPCyclePage.tsx
│   │   │   ├── KPIDashboardPage.tsx
│   │   │   └── SettingsPage.tsx
│   │   │
│   │   ├── hooks/                       # Custom React Hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useDemand.ts
│   │   │   ├── useSupply.ts
│   │   │   ├── useForecast.ts
│   │   │   └── useKPI.ts
│   │   │
│   │   ├── services/                    # API Client Layer
│   │   │   ├── api.ts                   # Axios instance & interceptors
│   │   │   ├── authService.ts
│   │   │   ├── demandService.ts
│   │   │   ├── supplyService.ts
│   │   │   ├── inventoryService.ts
│   │   │   ├── forecastService.ts
│   │   │   ├── scenarioService.ts
│   │   │   └── kpiService.ts
│   │   │
│   │   ├── store/                       # Zustand State Management
│   │   │   ├── authStore.ts
│   │   │   ├── demandStore.ts
│   │   │   ├── supplyStore.ts
│   │   │   └── uiStore.ts
│   │   │
│   │   ├── types/                       # TypeScript Type Definitions
│   │   │   ├── index.ts
│   │   │   ├── demand.ts
│   │   │   ├── supply.ts
│   │   │   ├── inventory.ts
│   │   │   ├── forecast.ts
│   │   │   └── scenario.ts
│   │   │
│   │   └── utils/                       # Utility functions
│   │       ├── formatters.ts
│   │       ├── constants.ts
│   │       └── validators.ts
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── GenXChains_Design_Document.md           # This document
└── README.md
```

### 2.4 Communication Patterns

- **Frontend → Backend:** RESTful API calls via Axios with JWT Bearer tokens
- **Backend → Database:** SQLAlchemy ORM with async session management
- **Backend → ML Engine:** Direct Python function calls (in-process)
- **Error Handling:** Standardized error response format with HTTP status codes
- **Data Format:** JSON for all API communication, ISO 8601 for dates

---

## 3. Database Schema Design

### 3.1 Entity Relationship Overview

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│   User   │────<│  DemandPlan  │>────│   Product    │
│          │     │              │     │              │
│ id       │     │ id           │     │ id           │
│ name     │     │ product_id   │     │ sku          │
│ email    │     │ period       │     │ name         │
│ role     │     │ region       │     │ category_id  │
│ dept     │     │ channel      │     │ family       │
└──────────┘     │ forecast_qty │     │ unit_cost    │
     │           │ actual_qty   │     │ price        │
     │           │ adjusted_qty │     │ lead_time    │
     │           │ confidence   │     └──────┬───────┘
     │           │ status       │            │
     │           └──────────────┘            │
     │                                       │
     │           ┌──────────────┐            │
     │      ────<│  SupplyPlan  │>───────────┘
     │           │              │            │
     │           │ id           │            │
     │           │ product_id   │            │
     │           │ period       │            │
     │           │ location     │     ┌──────┴───────┐
     │           │ prod_qty     │     │  Inventory   │
     │           │ capacity     │     │              │
     │           │ utilization  │     │ id           │
     │           │ lead_time    │     │ product_id   │
     │           │ supplier     │     │ location     │
     │           │ status       │     │ on_hand_qty  │
     │           └──────────────┘     │ safety_stock │
     │                                │ reorder_pt   │
     │           ┌──────────────┐     │ in_transit   │
     │      ────<│   Forecast   │     │ days_supply  │
     │           │              │     └──────────────┘
     │           │ id           │
     │           │ product_id   │     ┌──────────────┐
     │           │ model_type   │     │   Category   │
     │           │ period       │     │              │
     │           │ predicted    │     │ id           │
     │           │ lower_bound  │     │ name         │
     │           │ upper_bound  │     │ parent_id    │
     │           │ confidence   │     └──────────────┘
     │           │ mape         │
     │           └──────────────┘     ┌──────────────┐
     │                                │  KPIMetric   │
     │           ┌──────────────┐     │              │
     └──────────<│   Scenario   │     │ id           │
                 │              │     │ metric_name  │
                 │ id           │     │ period       │
                 │ name         │     │ value        │
                 │ description  │     │ target       │
                 │ base_plan_id │     │ variance     │
                 │ parameters   │     │ trend        │
                 │ status       │     └──────────────┘
                 │ created_by   │
                 └──────────────┘     ┌──────────────┐
                                      │   SOPCycle   │
     ┌──────────────┐                │              │
     │   Comment    │                │ id           │
     │              │                │ period       │
     │ id           │                │ step         │
     │ entity_type  │                │ status       │
     │ entity_id    │                │ owner_id     │
     │ user_id      │                │ due_date     │
     │ content      │                │ decisions    │
     │ created_at   │                │ notes        │
     └──────────────┘                └──────────────┘
```

### 3.2 Detailed Table Definitions

#### 3.2.1 Users Table
```sql
CREATE TABLE users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    email           VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255) NOT NULL,
    role            VARCHAR(50) NOT NULL DEFAULT 'viewer',
                    -- roles: admin, executive, demand_planner, supply_planner,
                    --        inventory_manager, finance_analyst, sop_coordinator, viewer
    department      VARCHAR(100),
    is_active       BOOLEAN DEFAULT TRUE,
    last_login      TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.2.2 Categories Table
```sql
CREATE TABLE categories (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR(255) NOT NULL,
    parent_id       INTEGER REFERENCES categories(id),
    level           INTEGER DEFAULT 0,  -- 0=top, 1=sub, 2=leaf
    description     TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.2.3 Products Table
```sql
CREATE TABLE products (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sku             VARCHAR(50) UNIQUE NOT NULL,
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    category_id     INTEGER REFERENCES categories(id),
    product_family  VARCHAR(100),
    unit_of_measure VARCHAR(20) DEFAULT 'units',
    unit_cost       DECIMAL(12,2),
    selling_price   DECIMAL(12,2),
    lead_time_days  INTEGER DEFAULT 0,
    min_order_qty   INTEGER DEFAULT 1,
    status          VARCHAR(20) DEFAULT 'active',  -- active, discontinued, new
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.2.4 Demand Plans Table
```sql
CREATE TABLE demand_plans (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id      INTEGER NOT NULL REFERENCES products(id),
    period          DATE NOT NULL,           -- Monthly period (first day of month)
    region          VARCHAR(100) DEFAULT 'Global',
    channel         VARCHAR(100) DEFAULT 'All',
    forecast_qty    DECIMAL(12,2) NOT NULL,  -- Statistical forecast
    adjusted_qty    DECIMAL(12,2),           -- Manually adjusted forecast
    actual_qty      DECIMAL(12,2),           -- Actual demand (filled post-period)
    consensus_qty   DECIMAL(12,2),           -- Consensus forecast
    confidence      DECIMAL(5,2),            -- Confidence level (0-100%)
    notes           TEXT,
    status          VARCHAR(20) DEFAULT 'draft',  -- draft, submitted, approved, locked
    created_by      INTEGER REFERENCES users(id),
    approved_by     INTEGER REFERENCES users(id),
    version         INTEGER DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, period, region, channel, version)
);
```

#### 3.2.5 Supply Plans Table
```sql
CREATE TABLE supply_plans (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id      INTEGER NOT NULL REFERENCES products(id),
    period          DATE NOT NULL,
    location        VARCHAR(100) DEFAULT 'Main',
    planned_prod_qty DECIMAL(12,2),          -- Planned production quantity
    actual_prod_qty  DECIMAL(12,2),          -- Actual production
    capacity_max    DECIMAL(12,2),           -- Maximum capacity
    capacity_used   DECIMAL(5,2),            -- Utilization percentage
    supplier_name   VARCHAR(255),
    lead_time_days  INTEGER,
    cost_per_unit   DECIMAL(12,2),
    constraints     TEXT,                     -- JSON: constraint descriptions
    status          VARCHAR(20) DEFAULT 'draft',
    created_by      INTEGER REFERENCES users(id),
    version         INTEGER DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, period, location, version)
);
```

#### 3.2.6 Inventory Table
```sql
CREATE TABLE inventory (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id      INTEGER NOT NULL REFERENCES products(id),
    location        VARCHAR(100) DEFAULT 'Main',
    on_hand_qty     DECIMAL(12,2) DEFAULT 0,
    allocated_qty   DECIMAL(12,2) DEFAULT 0,
    in_transit_qty  DECIMAL(12,2) DEFAULT 0,
    safety_stock    DECIMAL(12,2) DEFAULT 0,
    reorder_point   DECIMAL(12,2) DEFAULT 0,
    max_stock       DECIMAL(12,2),
    days_of_supply  DECIMAL(8,2),
    last_receipt_date DATE,
    last_issue_date   DATE,
    valuation       DECIMAL(14,2),           -- Inventory value
    status          VARCHAR(20) DEFAULT 'normal',  -- normal, low, critical, excess
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, location)
);
```

#### 3.2.7 Forecasts Table (ML Results)
```sql
CREATE TABLE forecasts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id      INTEGER NOT NULL REFERENCES products(id),
    model_type      VARCHAR(50) NOT NULL,    -- prophet, arima, exp_smoothing, ml_ensemble
    period          DATE NOT NULL,
    predicted_qty   DECIMAL(12,2) NOT NULL,
    lower_bound     DECIMAL(12,2),           -- Prediction interval lower
    upper_bound     DECIMAL(12,2),           -- Prediction interval upper
    confidence      DECIMAL(5,2),
    mape            DECIMAL(8,4),            -- Mean Absolute Percentage Error
    rmse            DECIMAL(12,4),           -- Root Mean Square Error
    features_used   TEXT,                     -- JSON: features used in model
    model_version   VARCHAR(50),
    training_date   TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.2.8 Scenarios Table
```sql
CREATE TABLE scenarios (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    scenario_type   VARCHAR(50) DEFAULT 'what_if',  -- what_if, best_case, worst_case, baseline
    parameters      TEXT NOT NULL,            -- JSON: scenario parameter adjustments
    base_demand_version INTEGER,
    base_supply_version INTEGER,
    results         TEXT,                     -- JSON: computed results
    revenue_impact  DECIMAL(14,2),
    margin_impact   DECIMAL(14,2),
    inventory_impact DECIMAL(14,2),
    service_level_impact DECIMAL(5,2),
    status          VARCHAR(20) DEFAULT 'draft',  -- draft, submitted, approved, rejected
    created_by      INTEGER REFERENCES users(id),
    approved_by     INTEGER REFERENCES users(id),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.2.9 S&OP Cycles Table
```sql
CREATE TABLE sop_cycles (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_name      VARCHAR(255) NOT NULL,   -- e.g., "March 2026 S&OP Cycle"
    period          DATE NOT NULL,           -- Planning period
    current_step    INTEGER DEFAULT 1,       -- 1-5 (see step definitions)
    step_1_status   VARCHAR(20) DEFAULT 'pending',  -- Data Gathering
    step_1_due_date DATE,
    step_1_owner_id INTEGER REFERENCES users(id),
    step_2_status   VARCHAR(20) DEFAULT 'pending',  -- Demand Review
    step_2_due_date DATE,
    step_2_owner_id INTEGER REFERENCES users(id),
    step_3_status   VARCHAR(20) DEFAULT 'pending',  -- Supply Review
    step_3_due_date DATE,
    step_3_owner_id INTEGER REFERENCES users(id),
    step_4_status   VARCHAR(20) DEFAULT 'pending',  -- Pre-S&OP
    step_4_due_date DATE,
    step_4_owner_id INTEGER REFERENCES users(id),
    step_5_status   VARCHAR(20) DEFAULT 'pending',  -- Executive S&OP
    step_5_due_date DATE,
    step_5_owner_id INTEGER REFERENCES users(id),
    decisions       TEXT,                     -- JSON: key decisions made
    action_items    TEXT,                     -- JSON: action items
    notes           TEXT,
    overall_status  VARCHAR(20) DEFAULT 'active',  -- active, completed, cancelled
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.2.10 KPI Metrics Table
```sql
CREATE TABLE kpi_metrics (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name     VARCHAR(100) NOT NULL,
    metric_category VARCHAR(50) NOT NULL,    -- demand, supply, inventory, financial, service
    period          DATE NOT NULL,
    value           DECIMAL(12,4) NOT NULL,
    target          DECIMAL(12,4),
    previous_value  DECIMAL(12,4),
    variance        DECIMAL(12,4),           -- value - target
    variance_pct    DECIMAL(8,4),
    trend           VARCHAR(20),             -- improving, declining, stable
    unit            VARCHAR(20),             -- %, units, days, currency
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(metric_name, period)
);
```

#### 3.2.11 Comments Table
```sql
CREATE TABLE comments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type     VARCHAR(50) NOT NULL,    -- demand_plan, supply_plan, scenario, sop_cycle
    entity_id       INTEGER NOT NULL,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    content         TEXT NOT NULL,
    parent_id       INTEGER REFERENCES comments(id),  -- For threaded replies
    mentions        TEXT,                     -- JSON: mentioned user IDs
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.2.12 Audit Log Table
```sql
CREATE TABLE audit_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER REFERENCES users(id),
    action          VARCHAR(50) NOT NULL,    -- create, update, delete, approve, reject
    entity_type     VARCHAR(50) NOT NULL,
    entity_id       INTEGER NOT NULL,
    old_values      TEXT,                     -- JSON: previous values
    new_values      TEXT,                     -- JSON: new values
    ip_address      VARCHAR(45),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.3 Key Indexes
```sql
-- Performance indexes
CREATE INDEX idx_demand_plans_product_period ON demand_plans(product_id, period);
CREATE INDEX idx_supply_plans_product_period ON supply_plans(product_id, period);
CREATE INDEX idx_inventory_product_location ON inventory(product_id, location);
CREATE INDEX idx_forecasts_product_period ON forecasts(product_id, period);
CREATE INDEX idx_kpi_metrics_name_period ON kpi_metrics(metric_name, period);
CREATE INDEX idx_comments_entity ON comments(entity_type, entity_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
```

---

## 4. API Design & Endpoints

### 4.1 API Base URL & Conventions
- **Base URL:** `http://localhost:8000/api/v1`
- **Authentication:** Bearer JWT token in `Authorization` header
- **Content-Type:** `application/json`
- **Pagination:** `?page=1&page_size=20` (default 20, max 100)
- **Filtering:** `?region=North&status=approved`
- **Sorting:** `?sort_by=period&sort_order=desc`
- **Date Format:** ISO 8601 (`YYYY-MM-DD`)

### 4.2 Standard Response Format
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 150,
    "total_pages": 8
  }
}
```

### 4.3 Error Response Format
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      { "field": "forecast_qty", "message": "Must be a positive number" }
    ]
  }
}
```

### 4.4 Authentication Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login & get JWT token | No |
| POST | `/api/v1/auth/refresh` | Refresh access token | Yes |
| GET | `/api/v1/auth/me` | Get current user profile | Yes |
| PUT | `/api/v1/auth/me` | Update current user profile | Yes |
| POST | `/api/v1/auth/change-password` | Change password | Yes |

### 4.5 Dashboard Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/dashboard/summary` | Executive dashboard KPI summary | Yes |
| GET | `/api/v1/dashboard/demand-overview` | Demand plan overview with trends | Yes |
| GET | `/api/v1/dashboard/supply-overview` | Supply plan overview with capacity | Yes |
| GET | `/api/v1/dashboard/inventory-health` | Inventory health summary | Yes |
| GET | `/api/v1/dashboard/alerts` | Active alerts & notifications | Yes |
| GET | `/api/v1/dashboard/sop-status` | Current S&OP cycle status | Yes |

### 4.6 Product Management Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/products` | List all products (paginated, filterable) | Yes |
| POST | `/api/v1/products` | Create new product | Admin |
| GET | `/api/v1/products/{id}` | Get product details | Yes |
| PUT | `/api/v1/products/{id}` | Update product | Admin |
| DELETE | `/api/v1/products/{id}` | Soft-delete product | Admin |
| GET | `/api/v1/categories` | List product categories (tree) | Yes |
| POST | `/api/v1/categories` | Create category | Admin |

### 4.7 Demand Planning Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/demand/plans` | List demand plans (filterable by period, product, region) | Yes |
| POST | `/api/v1/demand/plans` | Create demand plan entry | Planner |
| GET | `/api/v1/demand/plans/{id}` | Get demand plan details | Yes |
| PUT | `/api/v1/demand/plans/{id}` | Update demand plan | Planner |
| DELETE | `/api/v1/demand/plans/{id}` | Delete demand plan | Planner |
| POST | `/api/v1/demand/plans/{id}/adjust` | Apply manual adjustment | Planner |
| POST | `/api/v1/demand/plans/{id}/submit` | Submit for approval | Planner |
| POST | `/api/v1/demand/plans/{id}/approve` | Approve demand plan | Executive |
| POST | `/api/v1/demand/plans/{id}/reject` | Reject demand plan | Executive |
| GET | `/api/v1/demand/plans/{id}/history` | Get plan version history | Yes |
| POST | `/api/v1/demand/consensus` | Build consensus forecast | Planner |
| GET | `/api/v1/demand/actuals` | Get actual demand data | Yes |
| POST | `/api/v1/demand/import` | Bulk import demand data (CSV) | Planner |
| GET | `/api/v1/demand/export` | Export demand plans (CSV/Excel) | Yes |

### 4.8 Supply Planning Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/supply/plans` | List supply plans | Yes |
| POST | `/api/v1/supply/plans` | Create supply plan | Planner |
| GET | `/api/v1/supply/plans/{id}` | Get supply plan details | Yes |
| PUT | `/api/v1/supply/plans/{id}` | Update supply plan | Planner |
| DELETE | `/api/v1/supply/plans/{id}` | Delete supply plan | Planner |
| POST | `/api/v1/supply/plans/{id}/submit` | Submit for approval | Planner |
| POST | `/api/v1/supply/plans/{id}/approve` | Approve supply plan | Executive |
| GET | `/api/v1/supply/capacity` | Get capacity overview | Yes |
| GET | `/api/v1/supply/constraints` | List active constraints | Yes |
| GET | `/api/v1/supply/gap-analysis` | Demand vs supply gap analysis | Yes |

### 4.9 Inventory Management Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/inventory` | List inventory positions | Yes |
| GET | `/api/v1/inventory/{product_id}` | Get inventory for product | Yes |
| PUT | `/api/v1/inventory/{id}` | Update inventory record | Manager |
| GET | `/api/v1/inventory/health` | Inventory health dashboard data | Yes |
| GET | `/api/v1/inventory/alerts` | Low stock / excess alerts | Yes |
| GET | `/api/v1/inventory/aging` | Inventory aging analysis | Yes |
| GET | `/api/v1/inventory/turnover` | Inventory turnover metrics | Yes |

### 4.10 AI Forecasting Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/forecasting/generate` | Generate forecast for product(s) | Planner |
| GET | `/api/v1/forecasting/results` | List forecast results | Yes |
| GET | `/api/v1/forecasting/results/{id}` | Get forecast detail with confidence intervals | Yes |
| GET | `/api/v1/forecasting/models` | List available ML models | Yes |
| POST | `/api/v1/forecasting/compare` | Compare multiple model outputs | Yes |
| GET | `/api/v1/forecasting/accuracy` | Forecast accuracy metrics (MAPE, bias) | Yes |
| GET | `/api/v1/forecasting/accuracy/trend` | Accuracy trend over time | Yes |
| POST | `/api/v1/forecasting/anomalies/detect` | Run anomaly detection | Planner |
| GET | `/api/v1/forecasting/anomalies` | List detected anomalies | Yes |

### 4.11 Scenario Planning Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/scenarios` | List all scenarios | Yes |
| POST | `/api/v1/scenarios` | Create new scenario | Planner |
| GET | `/api/v1/scenarios/{id}` | Get scenario details with results | Yes |
| PUT | `/api/v1/scenarios/{id}` | Update scenario parameters | Planner |
| DELETE | `/api/v1/scenarios/{id}` | Delete scenario | Planner |
| POST | `/api/v1/scenarios/{id}/run` | Execute scenario simulation | Planner |
| POST | `/api/v1/scenarios/{id}/submit` | Submit for approval | Planner |
| POST | `/api/v1/scenarios/{id}/approve` | Approve scenario | Executive |
| POST | `/api/v1/scenarios/{id}/reject` | Reject scenario | Executive |
| POST | `/api/v1/scenarios/compare` | Compare multiple scenarios side-by-side | Yes |

### 4.12 S&OP Cycle Workflow Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/sop-cycles` | List S&OP cycles | Yes |
| POST | `/api/v1/sop-cycles` | Create new S&OP cycle | Coordinator |
| GET | `/api/v1/sop-cycles/{id}` | Get cycle details | Yes |
| PUT | `/api/v1/sop-cycles/{id}` | Update cycle | Coordinator |
| POST | `/api/v1/sop-cycles/{id}/advance` | Advance to next step | Coordinator |
| POST | `/api/v1/sop-cycles/{id}/complete` | Mark cycle as complete | Executive |
| GET | `/api/v1/sop-cycles/{id}/decisions` | Get decisions log | Yes |
| POST | `/api/v1/sop-cycles/{id}/decisions` | Add decision | Executive |
| GET | `/api/v1/sop-cycles/{id}/action-items` | Get action items | Yes |
| POST | `/api/v1/sop-cycles/{id}/action-items` | Add action item | Coordinator |

### 4.13 KPI & Analytics Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/kpi/metrics` | List all KPI metrics | Yes |
| GET | `/api/v1/kpi/metrics/{name}` | Get specific KPI with history | Yes |
| GET | `/api/v1/kpi/dashboard` | KPI dashboard data (all categories) | Yes |
| GET | `/api/v1/kpi/trends` | KPI trend analysis | Yes |
| GET | `/api/v1/kpi/alerts` | KPI threshold breach alerts | Yes |
| POST | `/api/v1/kpi/targets` | Set KPI targets | Admin |
| GET | `/api/v1/kpi/export` | Export KPI report (PDF/Excel) | Yes |

### 4.14 Collaboration Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/comments` | List comments (filterable by entity) | Yes |
| POST | `/api/v1/comments` | Add comment to entity | Yes |
| PUT | `/api/v1/comments/{id}` | Edit comment | Owner |
| DELETE | `/api/v1/comments/{id}` | Delete comment | Owner/Admin |
| GET | `/api/v1/users` | List users (for @mentions) | Yes |

---

## 5. Frontend Component Architecture

### 5.1 Application Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Header Bar                                    [User] [🔔]  │
├────────────┬────────────────────────────────────────────────┤
│            │  Breadcrumb: Dashboard > Demand Planning       │
│  Sidebar   │────────────────────────────────────────────────│
│            │                                                │
│  🏠 Dashboard│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  📊 Demand  │  │ KPI Card│ │ KPI Card│ │ KPI Card│       │
│  🏭 Supply  │  │ Revenue │ │ Forecast│ │  OTIF   │       │
│  📦 Inventory│  │ $12.5M  │ │  87.3%  │ │  94.2%  │       │
│  🤖 Forecast│  └─────────┘ └─────────┘ └─────────┘       │
│  🔄 Scenarios│                                              │
│  📋 S&OP    │  ┌────────────────────────────────────┐      │
│  📈 KPIs    │  │                                    │      │
│  ⚙️ Settings│  │     Main Content Area              │      │
│            │  │     (Charts, Tables, Forms)         │      │
│            │  │                                    │      │
│            │  └────────────────────────────────────┘      │
│            │                                                │
├────────────┴────────────────────────────────────────────────┤
│  Footer: GenXChains v1.0 | © 2026                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Component Hierarchy

```
App.tsx
├── AuthProvider
│   ├── LoginPage
│   └── ProtectedRoute
│       └── MainLayout
│           ├── Sidebar
│           │   ├── Logo
│           │   ├── NavItem (Dashboard)
│           │   ├── NavItem (Demand Planning)
│           │   ├── NavItem (Supply Planning)
│           │   ├── NavItem (Inventory)
│           │   ├── NavItem (Forecasting)
│           │   ├── NavItem (Scenarios)
│           │   ├── NavItem (S&OP Cycle)
│           │   ├── NavItem (KPI Dashboard)
│           │   └── NavItem (Settings)
│           ├── Header
│           │   ├── Breadcrumb
│           │   ├── SearchBar
│           │   ├── NotificationBell
│           │   └── UserMenu
│           └── PageContent (React Router Outlet)
│               ├── DashboardPage
│               │   ├── KPICardRow
│               │   ├── DemandTrendChart
│               │   ├── SupplyCapacityChart
│               │   ├── InventoryHealthWidget
│               │   ├── SOPCycleProgress
│               │   └── AlertsPanel
│               ├── DemandPlanningPage
│               │   ├── FilterBar (period, product, region)
│               │   ├── DemandSummaryCards
│               │   ├── DemandForecastChart
│               │   ├── DemandDataTable
│               │   ├── AdjustmentPanel
│               │   └── ApprovalActions
│               ├── SupplyPlanningPage
│               │   ├── CapacityOverview
│               │   ├── SupplyPlanTable
│               │   ├── GapAnalysisChart
│               │   ├── ConstraintsList
│               │   └── SupplierMatrix
│               ├── InventoryPage
│               │   ├── InventoryHealthCards
│               │   ├── StockLevelChart
│               │   ├── InventoryTable
│               │   ├── AgingAnalysis
│               │   └── AlertsPanel
│               ├── ForecastingPage
│               │   ├── ModelSelector
│               │   ├── ForecastChart (with confidence intervals)
│               │   ├── AccuracyMetrics
│               │   ├── ModelComparisonTable
│               │   └── AnomalyAlerts
│               ├── ScenariosPage
│               │   ├── ScenarioList
│               │   ├── ScenarioBuilder
│               │   │   ├── ParameterSliders
│               │   │   └── ImpactPreview
│               │   ├── ScenarioComparison
│               │   └── ApprovalWorkflow
│               ├── SOPCyclePage
│               │   ├── CycleTimeline (5-step visual)
│               │   ├── StepDetails
│               │   ├── DecisionsLog
│               │   ├── ActionItemsList
│               │   └── MeetingNotes
│               └── KPIDashboardPage
│                   ├── KPICategoryTabs
│                   ├── KPIGaugeCharts
│                   ├── KPITrendCharts
│                   ├── KPITable
│                   └── AlertThresholds
```

### 5.3 Shared/Common Components

| Component | Description | Props |
|-----------|-------------|-------|
| **Card** | Container with shadow, padding, optional header | `title`, `subtitle`, `children`, `actions` |
| **KPICard** | Metric display with value, trend, sparkline | `title`, `value`, `change`, `trend`, `icon`, `color` |
| **DataTable** | Advanced table with sort/filter/paginate | `columns`, `data`, `onSort`, `onFilter`, `pagination` |
| **StatusBadge** | Colored status indicator | `status`, `size` |
| **Modal** | Dialog overlay | `isOpen`, `onClose`, `title`, `children`, `size` |
| **Button** | Styled button with variants | `variant`, `size`, `loading`, `icon`, `onClick` |
| **FilterBar** | Row of filter dropdowns/inputs | `filters`, `onChange`, `onReset` |
| **LoadingSpinner** | Loading state indicator | `size`, `message` |
| **EmptyState** | No data placeholder | `icon`, `title`, `description`, `action` |
| **ConfirmDialog** | Confirmation modal | `message`, `onConfirm`, `onCancel` |

### 5.4 Chart Components

| Component | Library | Use Case |
|-----------|---------|----------|
| **LineChart** | Recharts | Demand trends, forecast vs actual, KPI trends |
| **BarChart** | Recharts | Supply capacity, inventory levels, regional comparison |
| **AreaChart** | Recharts | Forecast with confidence intervals |
| **WaterfallChart** | Nivo | Demand bridge (statistical → adjusted → consensus) |
| **HeatMap** | Nivo | Product-region demand matrix, forecast accuracy grid |
| **GaugeChart** | Custom/Nivo | KPI gauges (OTIF, utilization, accuracy) |
| **PieChart** | Recharts | Inventory distribution, category breakdown |
| **ComboChart** | Recharts | Demand vs supply overlay |

### 5.5 State Management (Zustand Stores)

```typescript
// authStore.ts
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

// demandStore.ts
interface DemandState {
  plans: DemandPlan[];
  selectedPlan: DemandPlan | null;
  filters: DemandFilters;
  loading: boolean;
  fetchPlans: (filters: DemandFilters) => Promise<void>;
  createPlan: (plan: CreateDemandPlan) => Promise<void>;
  updatePlan: (id: number, updates: Partial<DemandPlan>) => Promise<void>;
  adjustForecast: (id: number, adjustment: number) => Promise<void>;
  submitForApproval: (id: number) => Promise<void>;
}

// uiStore.ts
interface UIState {
  sidebarCollapsed: boolean;
  theme: 'light' | 'dark';
  notifications: Notification[];
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  addNotification: (notification: Notification) => void;
}
```

### 5.6 Routing Structure

```typescript
const routes = [
  { path: '/login', element: <LoginPage /> },
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'demand', element: <DemandPlanningPage /> },
      { path: 'demand/:id', element: <DemandPlanDetailPage /> },
      { path: 'supply', element: <SupplyPlanningPage /> },
      { path: 'supply/:id', element: <SupplyPlanDetailPage /> },
      { path: 'inventory', element: <InventoryPage /> },
      { path: 'forecasting', element: <ForecastingPage /> },
      { path: 'scenarios', element: <ScenariosPage /> },
      { path: 'scenarios/:id', element: <ScenarioDetailPage /> },
      { path: 'sop-cycle', element: <SOPCyclePage /> },
      { path: 'sop-cycle/:id', element: <SOPCycleDetailPage /> },
      { path: 'kpi', element: <KPIDashboardPage /> },
      { path: 'settings', element: <SettingsPage /> },
    ]
  }
];
```

---

## 6. Feature Specifications

### 6.1 Phase 1: Foundation & Core Infrastructure

#### 6.1.1 Authentication & User Management
**Description:** Secure JWT-based authentication with role-based access control (RBAC).

**Features:**
- User registration with email verification
- Login with JWT access + refresh token pair
- Role-based permissions (8 roles: admin, executive, demand_planner, supply_planner, inventory_manager, finance_analyst, sop_coordinator, viewer)
- Password hashing with bcrypt (passlib)
- Token refresh mechanism (access: 30min, refresh: 7 days)
- User profile management
- Session management & forced logout

**Permission Matrix:**

| Action | Admin | Executive | Planner | Manager | Analyst | Coordinator | Viewer |
|--------|-------|-----------|---------|---------|---------|-------------|--------|
| View dashboards | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create/edit plans | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Approve/reject plans | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Run forecasts | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Manage scenarios | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Manage S&OP cycle | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Manage users | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Set KPI targets | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

#### 6.1.2 Master Data Management
**Description:** Product catalog, categories, and organizational hierarchy management.

**Features:**
- Product CRUD with SKU, pricing, lead times
- Hierarchical category management (3 levels)
- Product family grouping
- Bulk import/export (CSV)
- Product status lifecycle (new → active → discontinued)
- Search & filter with full-text search

---

### 6.2 Phase 2: S&OP Planning Tool & Dashboard

#### 6.2.1 Executive Dashboard
**Description:** Real-time overview of all S&OP metrics and plan status.

**Dashboard Widgets:**

| Widget | Type | Data |
|--------|------|------|
| Revenue KPI Card | KPICard | Current vs target revenue |
| Forecast Accuracy | KPICard | MAPE % with trend arrow |
| OTIF Score | KPICard | On-Time In-Full % |
| Inventory Value | KPICard | Total inventory valuation |
| Demand Trend | LineChart | 12-month demand forecast vs actual |
| Supply Capacity | BarChart | Capacity utilization by location |
| Inventory Health | PieChart | Normal / Low / Critical / Excess split |
| S&OP Cycle Progress | StepProgress | Current cycle step (1-5) with status |
| Top Alerts | AlertList | Critical alerts requiring attention |
| Plan Status Summary | StatusGrid | Draft / Submitted / Approved counts |

**Interactions:**
- Click any KPI card → drill down to detailed view
- Date range selector (current month, quarter, year)
- Auto-refresh every 5 minutes
- Export dashboard as PDF

#### 6.2.2 Demand Planning Module
**Description:** Create, adjust, and manage demand forecasts by product, region, and channel.

**Features:**
- **Forecast Grid View:** Spreadsheet-like grid showing products × months with forecast quantities
- **Manual Adjustments:** Override statistical forecasts with business intelligence
- **Consensus Building:** Merge inputs from sales, marketing, and statistical models
- **Demand Bridge:** Waterfall chart showing statistical → adjusted → consensus progression
- **Regional Breakdown:** View/edit forecasts by region (North, South, East, West, Global)
- **Channel View:** Split by channel (Retail, Wholesale, Online, Direct)
- **Version Control:** Track all plan versions with diff comparison
- **Approval Workflow:** Submit → Review → Approve/Reject with comments
- **Actual vs Forecast:** Post-period comparison with variance analysis
- **Import/Export:** CSV upload for bulk forecast entry, Excel export

**Demand Planning Workflow:**
```
Statistical Forecast (ML) → Planner Adjustment → Sales Input → 
Marketing Input → Consensus Meeting → Final Consensus → 
Submit for Approval → Executive Approval → Locked Plan
```

#### 6.2.3 Supply Planning Module
**Description:** Manage production plans, capacity, and supplier constraints.

**Features:**
- **Production Planning Grid:** Products × months with planned quantities
- **Capacity Management:** Define max capacity per location, track utilization %
- **Constraint Modeling:** Define and track supply constraints (material, labor, equipment)
- **Supplier Management:** Track suppliers, lead times, reliability scores
- **Gap Analysis:** Visual comparison of demand plan vs supply capability
- **Lead Time Tracking:** Monitor and alert on lead time changes
- **Cost Analysis:** Production cost per unit, total cost projections
- **Approval Workflow:** Same submit/approve flow as demand

**Gap Analysis View:**
```
Product | Demand | Supply | Gap | Gap % | Action Required
--------|--------|--------|-----|-------|----------------
SKU-001 | 10,000 | 8,500  | -1,500 | -15% | ⚠️ Increase capacity
SKU-002 | 5,000  | 5,200  | +200   | +4%  | ✅ Balanced
SKU-003 | 7,500  | 4,000  | -3,500 | -47% | 🔴 Critical shortage
```

#### 6.2.4 Inventory Management Module
**Description:** Monitor and manage inventory positions across locations.

**Features:**
- **Inventory Dashboard:** Health overview with status distribution
- **Stock Level Monitoring:** On-hand, allocated, in-transit, available quantities
- **Safety Stock Management:** Define and track safety stock levels per product
- **Reorder Point Alerts:** Automatic alerts when stock falls below reorder point
- **Days of Supply:** Calculate and display days of supply based on demand forecast
- **Inventory Aging:** Age analysis (0-30, 31-60, 61-90, 90+ days)
- **Turnover Analysis:** Inventory turns calculation with benchmarking
- **Excess Inventory Alerts:** Flag items exceeding max stock levels
- **Valuation:** Real-time inventory valuation (cost × quantity)

**Inventory Status Classification:**
| Status | Condition | Color | Action |
|--------|-----------|-------|--------|
| **Normal** | Safety stock < qty < max stock | 🟢 Green | No action |
| **Low** | Reorder point < qty < safety stock | 🟡 Yellow | Monitor closely |
| **Critical** | qty < reorder point | 🔴 Red | Immediate reorder |
| **Excess** | qty > max stock | 🟠 Orange | Review & reduce |

---

### 6.3 Phase 3: AI-Powered Forecasting

#### 6.3.1 Statistical Forecasting
**Description:** Multiple time series models for demand prediction.

**Models Available:**
1. **Moving Average** — Simple/weighted moving average (3, 6, 12 month windows)
2. **Exponential Smoothing** — Single, double (Holt), triple (Holt-Winters) with trend & seasonality
3. **ARIMA/SARIMA** — Auto-regressive integrated moving average with seasonal components
4. **Prophet** — Facebook's time series model with holidays, changepoints, seasonality
5. **ML Ensemble** — Gradient boosting combining multiple model outputs

**Forecast Output:**
- Point forecast (predicted quantity)
- Confidence intervals (80% and 95%)
- Model accuracy metrics (MAPE, RMSE, MAE, bias)
- Seasonality decomposition
- Trend component visualization

#### 6.3.2 ML-Based Demand Sensing
**Description:** Pattern recognition and short-term demand signal detection.

**Capabilities:**
- Detect demand pattern changes (level shifts, trend changes)
- Seasonality auto-detection and adjustment
- Promotional lift estimation
- New product demand modeling (analogous product matching)
- External signal integration (placeholder for future: weather, economic indicators)

#### 6.3.3 Forecast Accuracy Tracking
**Description:** Comprehensive accuracy measurement and monitoring.

**Metrics Tracked:**
| Metric | Formula | Purpose |
|--------|---------|---------|
| **MAPE** | Mean Absolute Percentage Error | Overall accuracy |
| **Bias** | (Forecast - Actual) / Actual | Over/under forecasting tendency |
| **WMAPE** | Weighted MAPE (volume-weighted) | Accuracy weighted by importance |
| **Tracking Signal** | Cumulative error / MAD | Detect systematic bias |
| **Hit Rate** | % within ±20% of actual | Practical accuracy measure |

**Features:**
- Accuracy by product, category, region, channel
- Accuracy trend over time (improving/declining)
- Model comparison (which model performs best per product)
- Accuracy heatmap (product × period matrix)
- Automatic model selection based on accuracy

#### 6.3.4 Anomaly Detection
**Description:** Automatic identification of unusual demand patterns.

**Detection Methods:**
- Statistical outlier detection (Z-score, IQR method)
- Isolation Forest for multivariate anomalies
- Sudden demand spikes or drops (>2σ from rolling mean)
- Missing data detection and gap filling
- Seasonal pattern breaks

**Alert Output:**
- Anomaly severity (low, medium, high)
- Affected product and period
- Suggested action (investigate, adjust forecast, ignore)
- Historical context (similar past anomalies)

---

### 6.4 Phase 4: Scenario Planning & What-If Analysis

#### 6.4.1 Scenario Builder
**Description:** Interactive tool to create and simulate demand/supply scenarios.

**Adjustable Parameters:**
| Parameter | Type | Range | Example |
|-----------|------|-------|---------|
| Demand change % | Slider | -50% to +100% | +15% demand increase |
| Supply capacity % | Slider | -50% to +50% | -10% capacity reduction |
| Lead time change | Input | -30 to +60 days | +14 days delay |
| Price change % | Slider | -30% to +30% | +5% price increase |
| New product launch | Toggle + Input | On/Off + volume | Launch with 5,000 units/month |
| Supplier disruption | Toggle | On/Off per supplier | Supplier A offline |
| Seasonal adjustment | Slider | 0.5x to 2.0x | 1.3x holiday season |

**Scenario Types:**
- **What-If:** Custom parameter adjustments
- **Best Case:** Optimistic demand + full capacity
- **Worst Case:** Demand drop + supply constraints
- **Baseline:** Current plan without changes

#### 6.4.2 Impact Analysis
**Description:** Calculate financial and operational impact of each scenario.

**Impact Metrics:**
- Revenue impact ($)
- Gross margin impact ($)
- Inventory investment change ($)
- Service level impact (OTIF %)
- Capacity utilization change (%)
- Working capital impact ($)

#### 6.4.3 Scenario Comparison
**Description:** Side-by-side visual comparison of multiple scenarios.

**Comparison View:**
```
Metric          | Baseline | Scenario A | Scenario B | Scenario C
----------------|----------|------------|------------|----------
Revenue         | $12.5M   | $14.2M ↑   | $11.8M ↓   | $13.1M ↑
Margin          | $3.8M    | $4.1M ↑    | $3.2M ↓    | $3.9M ↑
Inventory       | $2.1M    | $2.8M ↑    | $1.6M ↓    | $2.3M ↑
OTIF            | 94.2%    | 91.5% ↓    | 96.8% ↑    | 93.7% ↓
Capacity Util.  | 78%      | 92% ↑      | 65% ↓      | 82% ↑
```

#### 6.4.4 Scenario Approval Workflow
- Create scenario → Run simulation → Review results → Submit for approval
- Executive review with comments
- Approve (becomes the operating plan) or Reject (with feedback)

---

### 6.5 Phase 5: Collaborative S&OP Workflow

#### 6.5.1 S&OP Cycle Management
**Description:** Structured 5-step monthly S&OP cycle with tracking.

**The 5 Steps:**

| Step | Name | Duration | Owner | Key Activities |
|------|------|----------|-------|----------------|
| 1 | **Data Gathering** | Days 1-5 | S&OP Coordinator | Collect actuals, update master data, run statistical forecasts |
| 2 | **Demand Review** | Days 6-12 | Demand Planner | Review forecasts, apply adjustments, build consensus |
| 3 | **Supply Review** | Days 13-18 | Supply Planner | Evaluate capacity, identify constraints, create supply plan |
| 4 | **Pre-S&OP** | Days 19-22 | Cross-functional | Reconcile demand & supply, evaluate scenarios, prepare recommendations |
| 5 | **Executive S&OP** | Days 23-25 | VP/Executive | Review integrated plan, make decisions, approve final plan |

**Cycle Visualization:**
```
Step 1          Step 2          Step 3          Step 4       Step 5
[Data Gather]──>[Demand Rev]──>[Supply Rev]──>[Pre-S&OP]──>[Exec S&OP]
   ✅ Done        🔄 Active      ⏳ Pending     ⏳ Pending    ⏳ Pending
   Jan 1-5        Jan 6-12       Jan 13-18      Jan 19-22    Jan 23-25
```

#### 6.5.2 Meeting Management
**Features:**
- Agenda templates per step
- Action items with assignee, due date, status
- Decisions log with rationale
- Meeting notes with rich text
- Attachments support

#### 6.5.3 Collaboration Features
**Features:**
- **Inline Comments:** Add comments on any plan, scenario, or KPI
- **@Mentions:** Tag team members in comments for attention
- **Threaded Discussions:** Reply chains on comments
- **Activity Feed:** Timeline of all changes and comments
- **Notifications:** In-app alerts for mentions, approvals, deadlines

#### 6.5.4 Plan Versioning
**Features:**
- Automatic version increment on plan changes
- Version comparison (diff view)
- Rollback to previous version
- Audit trail (who changed what, when)
- Lock mechanism for approved plans

---

### 6.6 Phase 6: Advanced Analytics & KPIs

#### 6.6.1 KPI Dashboard
**Description:** Comprehensive KPI monitoring across all S&OP dimensions.

**KPI Categories & Metrics:**

| Category | KPI | Target | Unit |
|----------|-----|--------|------|
| **Demand** | Forecast Accuracy (MAPE) | < 15% | % |
| **Demand** | Forecast Bias | ±5% | % |
| **Demand** | Demand Plan Adherence | > 90% | % |
| **Supply** | Capacity Utilization | 75-85% | % |
| **Supply** | Production Plan Adherence | > 95% | % |
| **Supply** | Supplier On-Time Delivery | > 95% | % |
| **Inventory** | Inventory Turns | > 8x | turns/year |
| **Inventory** | Days of Supply | 15-30 | days |
| **Inventory** | Excess & Obsolete % | < 5% | % |
| **Service** | OTIF (On-Time In-Full) | > 95% | % |
| **Service** | Fill Rate | > 98% | % |
| **Service** | Order Cycle Time | < 3 days | days |
| **Financial** | Revenue vs Plan | ±5% | $ |
| **Financial** | Gross Margin | > 30% | % |
| **Financial** | Working Capital Ratio | < 20% | % |

#### 6.6.2 Trend Analysis
**Features:**
- 12-month rolling trend for each KPI
- Year-over-year comparison
- Drill-down by product, region, channel
- Correlation analysis between KPIs
- Sparkline mini-charts in tables

#### 6.6.3 Alert System
**Features:**
- Threshold-based alerts (KPI breaches target)
- Severity levels: Info, Warning, Critical
- Alert rules configuration (per KPI)
- In-app notification center
- Alert history and resolution tracking

#### 6.6.4 Export & Reporting
**Features:**
- PDF report generation (dashboard snapshots)
- Excel export (data tables with formatting)
- CSV export (raw data)
- Scheduled reports (placeholder for future)
- Custom report builder (select metrics, period, filters)

---

## 7. AI/ML Model Specifications

### 7.1 Forecasting Pipeline Architecture

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐
│  Raw Data   │───>│  Data Prep   │───>│   Model      │───>│  Forecast   │
│  Ingestion  │    │  & Features  │    │  Training    │    │  Output     │
│             │    │              │    │  & Selection │    │             │
│ - Actuals   │    │ - Clean      │    │ - Train/Test │    │ - Point     │
│ - History   │    │ - Impute     │    │ - Cross-val  │    │ - Intervals │
│ - External  │    │ - Features   │    │ - Best model │    │ - Accuracy  │
└─────────────┘    └──────────────┘    └──────────────┘    └─────────────┘
```

### 7.2 Model Specifications

#### 7.2.1 Moving Average
```python
# Configuration
class MovingAverageConfig:
    windows: List[int] = [3, 6, 12]      # Month windows
    weighted: bool = True                  # Use weighted average
    weights: str = "linear"                # linear, exponential
    
# Use Case: Stable products with minimal trend/seasonality
# Pros: Simple, fast, interpretable
# Cons: Lags behind trends, no seasonality handling
# Min Data Required: 12 months
```

#### 7.2.2 Exponential Smoothing (Holt-Winters)
```python
# Configuration
class ExpSmoothingConfig:
    trend: str = "add"                     # add, mul, None
    seasonal: str = "add"                  # add, mul, None
    seasonal_periods: int = 12             # Monthly seasonality
    damped_trend: bool = True
    optimization_method: str = "L-BFGS-B"
    
# Use Case: Products with clear trend and/or seasonality
# Pros: Handles trend + seasonality, well-understood
# Cons: Single seasonality, limited external factors
# Min Data Required: 24 months (2 full seasonal cycles)
```

#### 7.2.3 ARIMA / SARIMA
```python
# Configuration
class ARIMAConfig:
    auto_order: bool = True                # Auto-select (p,d,q)
    max_p: int = 5
    max_d: int = 2
    max_q: int = 5
    seasonal: bool = True
    seasonal_period: int = 12
    information_criterion: str = "aic"     # aic, bic
    stepwise: bool = True
    
# Use Case: Complex time series with autocorrelation
# Pros: Flexible, handles complex patterns
# Cons: Computationally expensive, requires stationarity
# Min Data Required: 36 months
```

#### 7.2.4 Prophet
```python
# Configuration
class ProphetConfig:
    growth: str = "linear"                 # linear, logistic, flat
    seasonality_mode: str = "multiplicative"  # additive, multiplicative
    yearly_seasonality: bool = True
    weekly_seasonality: bool = False
    changepoint_prior_scale: float = 0.05
    seasonality_prior_scale: float = 10.0
    holidays_prior_scale: float = 10.0
    interval_width: float = 0.95           # 95% confidence interval
    mcmc_samples: int = 0                  # 0 for MAP, >0 for full Bayesian
    
# Use Case: Products with holidays, changepoints, strong seasonality
# Pros: Handles holidays, robust to missing data, interpretable
# Cons: May overfit with limited data
# Min Data Required: 24 months
```

#### 7.2.5 ML Ensemble (Gradient Boosting)
```python
# Configuration
class EnsembleConfig:
    base_models: List[str] = ["moving_avg", "exp_smoothing", "prophet"]
    meta_model: str = "gradient_boosting"  # gradient_boosting, random_forest
    features: List[str] = [
        "month", "quarter", "year",
        "lag_1", "lag_3", "lag_6", "lag_12",
        "rolling_mean_3", "rolling_mean_6",
        "rolling_std_3", "rolling_std_6",
        "trend", "seasonality_index",
        "yoy_growth", "mom_growth"
    ]
    n_estimators: int = 100
    max_depth: int = 6
    learning_rate: float = 0.1
    cv_folds: int = 5
    
# Use Case: High-volume products with complex patterns
# Pros: Best accuracy, combines multiple signals
# Cons: Less interpretable, needs more data
# Min Data Required: 36 months
```

### 7.3 Model Selection Strategy

```
For each product:
1. Check data availability (months of history)
2. Run applicable models based on data length
3. Evaluate each model using time-series cross-validation
4. Select best model based on MAPE on holdout set
5. Generate forecast with selected model
6. Store results with accuracy metrics

Auto-Selection Rules:
├── < 12 months history → Moving Average only
├── 12-24 months → Moving Average + Exp Smoothing
├── 24-36 months → + Prophet + ARIMA
└── 36+ months → All models including Ensemble
```

### 7.4 Anomaly Detection Algorithms

#### 7.4.1 Statistical Methods
```python
class StatisticalAnomalyDetector:
    """Z-score and IQR based detection"""
    z_threshold: float = 2.5              # Standard deviations
    iqr_multiplier: float = 1.5           # IQR fence multiplier
    rolling_window: int = 12              # Months for rolling stats
    min_data_points: int = 12
```

#### 7.4.2 Isolation Forest
```python
class IsolationForestDetector:
    """Multivariate anomaly detection"""
    contamination: float = 0.05           # Expected anomaly rate (5%)
    n_estimators: int = 100
    features: List[str] = [
        "demand_qty", "yoy_change", "mom_change",
        "deviation_from_seasonal", "forecast_error"
    ]
```

### 7.5 Accuracy Metrics Calculation

```python
def calculate_metrics(actual: np.array, forecast: np.array) -> dict:
    """Calculate all forecast accuracy metrics"""
    return {
        "mape": np.mean(np.abs((actual - forecast) / actual)) * 100,
        "bias": np.mean((forecast - actual) / actual) * 100,
        "rmse": np.sqrt(np.mean((actual - forecast) ** 2)),
        "mae": np.mean(np.abs(actual - forecast)),
        "wmape": np.sum(np.abs(actual - forecast)) / np.sum(actual) * 100,
        "hit_rate": np.mean(np.abs((actual - forecast) / actual) <= 0.20) * 100,
        "tracking_signal": np.sum(forecast - actual) / np.mean(np.abs(actual - forecast))
    }
```

### 7.6 Data Requirements

| Model | Min History | Recommended | Forecast Horizon |
|-------|------------|-------------|-----------------|
| Moving Average | 12 months | 24 months | 1-3 months |
| Exp Smoothing | 24 months | 36 months | 3-12 months |
| ARIMA/SARIMA | 36 months | 48 months | 3-12 months |
| Prophet | 24 months | 36+ months | 6-18 months |
| ML Ensemble | 36 months | 48+ months | 3-12 months |
| Anomaly Detection | 12 months | 24 months | N/A (detection) |

---

## 8. Security & Authentication

### 8.1 Authentication Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client   │────>│  Login   │────>│ Validate │────>│  Issue   │
│  (React)  │     │ Request  │     │ Password │     │  Tokens  │
│           │<────│          │<────│ (bcrypt) │<────│ (JWT)    │
│           │     └──────────┘     └──────────┘     └──────────┘
│           │                                              │
│           │     ┌──────────┐     ┌──────────┐           │
│           │────>│  API     │────>│ Verify   │           │
│           │     │ Request  │     │  Token   │<──────────┘
│           │<────│ + Bearer │<────│ (jose)   │
│           │     └──────────┘     └──────────┘
└──────────┘
```

### 8.2 JWT Token Strategy

| Token | Lifetime | Storage | Purpose |
|-------|----------|---------|---------|
| **Access Token** | 30 minutes | Memory (Zustand) | API authentication |
| **Refresh Token** | 7 days | HttpOnly cookie | Token renewal |

**Token Payload:**
```json
{
  "sub": "user_id",
  "email": "user@company.com",
  "role": "demand_planner",
  "department": "Planning",
  "exp": 1709000000,
  "iat": 1708998200,
  "type": "access"
}
```

### 8.3 Password Security
- **Hashing:** bcrypt via passlib with 12 rounds
- **Minimum Requirements:** 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character
- **Rate Limiting:** Max 5 failed login attempts per 15 minutes
- **Password History:** Prevent reuse of last 5 passwords (future enhancement)

### 8.4 API Security Measures

| Measure | Implementation |
|---------|---------------|
| **CORS** | Whitelist frontend origin only |
| **Rate Limiting** | 100 requests/minute per user |
| **Input Validation** | Pydantic schemas on all endpoints |
| **SQL Injection** | SQLAlchemy ORM parameterized queries |
| **XSS Prevention** | React auto-escaping + CSP headers |
| **HTTPS** | Enforced in production |
| **Request Size** | Max 10MB payload |
| **Audit Logging** | All write operations logged |

### 8.5 Role-Based Access Control (RBAC)

```python
# FastAPI dependency for role checking
from fastapi import Depends, HTTPException, status

def require_role(allowed_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

# Usage in router
@router.post("/demand/plans/{id}/approve")
async def approve_plan(
    id: int,
    user: User = Depends(require_role(["admin", "executive"]))
):
    ...
```

### 8.6 Data Protection
- **Sensitive Data:** Passwords never stored in plain text, never returned in API responses
- **Audit Trail:** All data modifications logged with user, timestamp, old/new values
- **Data Isolation:** Users can only access data within their organization (multi-tenant ready)
- **Backup Strategy:** SQLite file backup (dev), PostgreSQL pg_dump (production)

---

## 9. UI/UX Design

### 9.1 Design Principles
- **Clean & Professional:** Enterprise-grade look with modern aesthetics
- **Data-Dense but Readable:** Maximize information density without clutter
- **Consistent:** Uniform patterns across all modules
- **Responsive:** Works on desktop (primary), tablet, and large monitors
- **Accessible:** WCAG 2.1 AA compliance, keyboard navigation, screen reader support
- **Dark/Light Mode:** User-selectable theme preference

### 9.2 Color Palette

| Purpose | Light Mode | Dark Mode | Usage |
|---------|-----------|-----------|-------|
| **Primary** | `#3B82F6` (Blue 500) | `#60A5FA` (Blue 400) | Buttons, links, active states |
| **Secondary** | `#6366F1` (Indigo 500) | `#818CF8` (Indigo 400) | Secondary actions, accents |
| **Success** | `#10B981` (Emerald 500) | `#34D399` (Emerald 400) | Positive KPIs, approved status |
| **Warning** | `#F59E0B` (Amber 500) | `#FBBF24` (Amber 400) | Alerts, low stock, caution |
| **Danger** | `#EF4444` (Red 500) | `#F87171` (Red 400) | Critical alerts, negative KPIs |
| **Background** | `#F9FAFB` (Gray 50) | `#111827` (Gray 900) | Page background |
| **Surface** | `#FFFFFF` (White) | `#1F2937` (Gray 800) | Cards, panels |
| **Text Primary** | `#111827` (Gray 900) | `#F9FAFB` (Gray 50) | Headings, body text |
| **Text Secondary** | `#6B7280` (Gray 500) | `#9CA3AF` (Gray 400) | Labels, descriptions |
| **Border** | `#E5E7EB` (Gray 200) | `#374151` (Gray 700) | Dividers, card borders |

### 9.3 Typography
- **Font Family:** Inter (primary), system-ui (fallback)
- **Headings:** Inter Semi-Bold (600)
- **Body:** Inter Regular (400)
- **Data/Numbers:** Inter Medium (500), tabular-nums for alignment
- **Scale:** 12px (xs), 14px (sm/body), 16px (base), 18px (lg), 24px (xl), 30px (2xl)

### 9.4 Page Layout Specifications

#### 9.4.1 Login Page
```
┌─────────────────────────────────────────────┐
│                                             │
│         ┌─────────────────────┐             │
│         │    🏢 GenXChains       │             │
│         │                     │             │
│         │  ┌───────────────┐  │             │
│         │  │ Email         │  │             │
│         │  └───────────────┘  │             │
│         │  ┌───────────────┐  │             │
│         │  │ Password      │  │             │
│         │  └───────────────┘  │             │
│         │                     │             │
│         │  [    Sign In    ]  │             │
│         │                     │             │
│         │  Forgot password?   │             │
│         └─────────────────────┘             │
│                                             │
│  Background: Gradient or subtle pattern     │
└─────────────────────────────────────────────┘
```

#### 9.4.2 Dashboard Page
```
┌──────────────────────────────────────────────────────────┐
│ KPI Row                                                  │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│ │ Revenue  │ │ Forecast │ │   OTIF   │ │Inventory │    │
│ │ $12.5M   │ │  87.3%   │ │  94.2%   │ │  $2.1M   │    │
│ │ ↑ +5.2%  │ │ ↑ +2.1%  │ │ ↓ -0.8%  │ │ ↓ -3.4%  │    │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
│                                                          │
│ ┌──────────────────────────┐ ┌────────────────────────┐  │
│ │ Demand vs Actual (Line)  │ │ Capacity Util. (Bar)   │  │
│ │                          │ │                        │  │
│ │  📈 12-month trend       │ │  📊 By location        │  │
│ │                          │ │                        │  │
│ └──────────────────────────┘ └────────────────────────┘  │
│                                                          │
│ ┌──────────────────────────┐ ┌────────────────────────┐  │
│ │ S&OP Cycle Progress      │ │ Alerts & Notifications │  │
│ │ Step 1 ✅ → Step 2 🔄 → │ │ 🔴 3 Critical          │  │
│ │ Step 3 ⏳ → Step 4 ⏳ → │ │ 🟡 5 Warnings          │  │
│ │ Step 5 ⏳               │ │ 🔵 2 Info              │  │
│ └──────────────────────────┘ └────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

#### 9.4.3 Demand Planning Page
```
┌──────────────────────────────────────────────────────────┐
│ Filter Bar: [Period ▼] [Product ▼] [Region ▼] [Status ▼]│
│                                                          │
│ Summary Cards                                            │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│ │Total Fcst│ │Consensus │ │ Variance │ │ Accuracy │    │
│ │ 125,000  │ │ 118,500  │ │  -5.2%   │ │  87.3%   │    │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
│                                                          │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Forecast vs Actual Chart (Line + Area)               │ │
│ │ — Forecast  — Actual  ░ Confidence Band              │ │
│ └──────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Demand Plan Table                          [Export]  │ │
│ │ Product | Jan | Feb | Mar | Apr | ... | Status | Act │ │
│ │ SKU-001 | 850 | 920 | 880 | 950 | ... | Draft  | ✏️ │ │
│ │ SKU-002 | 450 | 480 | 510 | 490 | ... | Aprvd  | 👁 │ │
│ │ SKU-003 | 720 | 690 | 750 | 780 | ... | Submit | ✏️ │ │
│ └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

### 9.5 Interaction Patterns

| Pattern | Behavior |
|---------|----------|
| **Hover on chart** | Tooltip with exact values |
| **Click KPI card** | Navigate to detailed view |
| **Click table row** | Open detail panel / modal |
| **Double-click cell** | Inline edit (editable tables) |
| **Drag slider** | Real-time scenario parameter adjustment |
| **Right-click** | Context menu (edit, delete, copy) |
| **Keyboard shortcuts** | Ctrl+S (save), Ctrl+E (export), Esc (close modal) |

### 9.6 Loading & Empty States
- **Loading:** Skeleton screens (shimmer effect) matching content layout
- **Empty State:** Illustration + message + CTA button ("No demand plans yet. Create your first plan →")
- **Error State:** Red banner with retry button
- **Success:** Green toast notification (auto-dismiss after 3s)

---

## 10. Deployment Strategy

### 10.1 Development Environment

```bash
# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate          # macOS/Linux
pip install -r requirements.txt
python seed_data.py               # Load sample data
python run.py                     # Start FastAPI on :8000

# Frontend Setup
cd frontend
npm install
npm run dev                       # Start Vite dev server on :5173
```

### 10.2 Environment Configuration

```bash
# backend/.env
DATABASE_URL=sqlite:///./genxchains.db          # Dev: SQLite
# DATABASE_URL=postgresql://user:pass@host/genxchains  # Prod: PostgreSQL
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:5173
DEBUG=true
```

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=GenXChains
VITE_APP_VERSION=1.0.0
```

### 10.3 Development Workflow

```
Feature Branch → Local Dev → Unit Tests → PR Review → 
Merge to main → Integration Tests → Staging Deploy → 
QA Validation → Production Deploy
```

### 10.4 Production Deployment Architecture

```
┌─────────────────────────────────────────────────┐
│                   Cloud / VPS                    │
│                                                  │
│  ┌──────────────┐    ┌──────────────────────┐   │
│  │   Nginx      │    │   Frontend (Static)   │   │
│  │   Reverse    │───>│   React Build Files   │   │
│  │   Proxy      │    │   (dist/)             │   │
│  │   :80/:443   │    └──────────────────────┘   │
│  │              │                                │
│  │              │    ┌──────────────────────┐   │
│  │              │───>│   Backend (API)       │   │
│  │              │    │   Uvicorn + FastAPI   │   │
│  │              │    │   :8000               │   │
│  └──────────────┘    └──────────┬───────────┘   │
│                                  │               │
│                      ┌───────────┴───────────┐   │
│                      │   PostgreSQL           │   │
│                      │   :5432                │   │
│                      └───────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### 10.5 Docker Deployment (Optional)

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://genxchains:password@db:5432/genxchains
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=genxchains
      - POSTGRES_USER=genxchains
      - POSTGRES_PASSWORD=password
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  pgdata:
```

### 10.6 Database Migration Strategy

```bash
# Initialize Alembic (one-time)
cd backend
alembic init alembic

# Create migration after model changes
alembic revision --autogenerate -m "Add demand_plans table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### 10.7 Testing Strategy

| Layer | Tool | Coverage Target | Focus |
|-------|------|----------------|-------|
| **Backend Unit** | pytest | > 80% | Services, models, utils |
| **Backend API** | pytest + httpx | > 70% | Endpoint integration |
| **Frontend Unit** | Vitest | > 70% | Components, hooks, stores |
| **Frontend E2E** | Playwright (future) | Key flows | Login, CRUD, workflows |
| **ML Models** | pytest | > 60% | Forecast accuracy, edge cases |

```bash
# Run backend tests
cd backend && pytest --cov=app tests/

# Run frontend tests
cd frontend && npm run test
```

---

## 11. Roadmap & Milestones

### 11.1 Development Phases

```
Phase 1 ──────> Phase 2 ──────> Phase 3 ──────> Phase 4 ──────> Phase 5 ──────> Phase 6
Foundation      Planning &      AI/ML           Scenario        Collaborative   Advanced
& Core          Dashboard       Forecasting     Planning        S&OP Workflow   Analytics
(4 weeks)       (6 weeks)       (5 weeks)       (4 weeks)       (4 weeks)       (3 weeks)
```

### 11.2 Phase 1: Foundation & Core (Weeks 1-4)

| Week | Deliverables |
|------|-------------|
| **Week 1** | Project setup, backend scaffolding, database models, Alembic migrations |
| **Week 2** | Auth system (register, login, JWT, RBAC), user management API |
| **Week 3** | Frontend setup (Vite, React, Tailwind, routing), login page, layout components |
| **Week 4** | Product/category CRUD (backend + frontend), seed data script, basic navigation |

**Milestone:** ✅ Users can register, login, and manage products

### 11.3 Phase 2: S&OP Planning & Dashboard (Weeks 5-10)

| Week | Deliverables |
|------|-------------|
| **Week 5** | Dashboard API endpoints, KPI card components, executive dashboard layout |
| **Week 6** | Demand planning backend (CRUD, filters, pagination), demand plan schemas |
| **Week 7** | Demand planning frontend (grid view, charts, filter bar, data table) |
| **Week 8** | Supply planning backend + frontend, capacity management |
| **Week 9** | Inventory management module (backend + frontend), stock monitoring |
| **Week 10** | Gap analysis, approval workflow (submit/approve/reject), version control |

**Milestone:** ✅ Full demand/supply/inventory planning with dashboards

### 11.4 Phase 3: AI-Powered Forecasting (Weeks 11-15)

| Week | Deliverables |
|------|-------------|
| **Week 11** | ML pipeline setup, moving average & exponential smoothing models |
| **Week 12** | ARIMA/SARIMA implementation, Prophet integration |
| **Week 13** | ML ensemble model, auto model selection, accuracy metrics |
| **Week 14** | Forecasting frontend (model selector, forecast charts, confidence intervals) |
| **Week 15** | Anomaly detection, accuracy tracking dashboard, model comparison view |

**Milestone:** ✅ AI-generated forecasts with multiple models and accuracy tracking

### 11.5 Phase 4: Scenario Planning (Weeks 16-19)

| Week | Deliverables |
|------|-------------|
| **Week 16** | Scenario backend (CRUD, parameter storage, simulation engine) |
| **Week 17** | Scenario builder frontend (parameter sliders, impact preview) |
| **Week 18** | Impact analysis calculations, scenario comparison view |
| **Week 19** | Scenario approval workflow, integration with demand/supply plans |

**Milestone:** ✅ What-if scenarios with financial impact analysis

### 11.6 Phase 5: Collaborative S&OP Workflow (Weeks 20-23)

| Week | Deliverables |
|------|-------------|
| **Week 20** | S&OP cycle backend (5-step workflow, step management) |
| **Week 21** | S&OP cycle frontend (timeline visualization, step details) |
| **Week 22** | Comments system (inline, @mentions, threads), activity feed |
| **Week 23** | Decisions log, action items, meeting notes, notifications |

**Milestone:** ✅ Complete S&OP cycle management with collaboration

### 11.7 Phase 6: Advanced Analytics & Polish (Weeks 24-26)

| Week | Deliverables |
|------|-------------|
| **Week 24** | KPI dashboard (all categories), trend analysis, gauge charts |
| **Week 25** | Alert system, export/reporting (PDF, Excel, CSV) |
| **Week 26** | Performance optimization, bug fixes, documentation, final testing |

**Milestone:** ✅ Production-ready GenXChains platform

### 11.8 Summary Timeline

```
Month 1        Month 2        Month 3        Month 4        Month 5        Month 6        Month 7
|──Phase 1──|──────Phase 2──────|────Phase 3────|───Phase 4───|───Phase 5───|──Phase 6──|
 Foundation   Planning & Dash    AI Forecasting  Scenarios     Collaboration  Analytics
 Auth, CRUD   Demand/Supply/Inv  ML Models       What-If       S&OP Cycle     KPIs
              Dashboard          Accuracy        Comparison    Comments       Reports
```

### 11.9 Success Criteria

| Criteria | Target |
|----------|--------|
| All 11 database tables created and seeded | ✅ |
| 80+ API endpoints functional | ✅ |
| 10 frontend pages with full CRUD | ✅ |
| 5 ML forecasting models operational | ✅ |
| 5-step S&OP cycle workflow complete | ✅ |
| 15+ KPIs tracked with dashboards | ✅ |
| Role-based access for 8 user roles | ✅ |
| Scenario builder with impact analysis | ✅ |
| Backend test coverage > 80% | ✅ |
| Frontend test coverage > 70% | ✅ |
| Response time < 500ms for all APIs | ✅ |
| Zero critical security vulnerabilities | ✅ |

---

*End of GenXChains Design Document v1.0*
