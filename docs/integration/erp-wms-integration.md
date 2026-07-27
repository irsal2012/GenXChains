# ERP/WMS Integration Scenarios (Vendor-Agnostic)

This document describes how GenXChains typically integrates with an ERP/WMS.

## Key principle

- **ERP/WMS** remains the **system of record** for transactional execution (orders, shipments, receipts, production, inventory movements).
- **GenXChains** becomes the **system of planning + decision governance** (plans, scenarios, approvals, S&OP cycle, KPIs).

## Integration scenarios

### Scenario 1 — Read-only integration (fastest, lowest risk)

**Meaning:** GenXChains reads data from ERP/WMS but does not write back.

**Best when:** you want early value without impacting operational execution.

**Typical inbound data:**

- Item master / SKU master (products)
- Locations
- Actual demand (shipments/sales)
- Inventory snapshots (on-hand, allocated, in-transit)
- Optional: production/procurement actuals

**Outcome:** teams do planning and governance in GenXChains; execution still uses ERP.

### Scenario 2 — Publish-back integration (GenXChains is the planning author)

**Meaning:** GenXChains produces an approved plan and publishes it back into ERP.

**Best when:** you want GenXChains to become the planning front-end feeding ERP.

**Typical publish targets:**

- Approved demand plan → ERP “forecast” object
- Approved supply plan → ERP planned orders / planned production quantities
- Approved inventory policy → ERP safety stock / reorder point parameters (optional)

**Outcome:** one approved plan version drives execution.

### Scenario 3 — Closed-loop (both read + publish)

**Meaning:** GenXChains reads actuals and publishes approved plans back.

This is the most common long-term target:

1. ERP/WMS provides actuals and master data.
2. GenXChains produces plans/scenarios through workflow/approvals.
3. GenXChains publishes the approved plan version back to ERP.
4. ERP execution generates new actuals.
5. GenXChains measures performance (accuracy, adherence, inventory/service outcomes).

## Phased rollout (recommended)

### Phase 1 — Master data alignment

- Products/SKUs + hierarchy
- Locations
- Units of measure
- Lead times, costs/prices (if needed for KPIs)

### Phase 2 — Actuals ingestion

- Demand actuals (shipments/sales)
- Inventory positions (on-hand/allocated/in-transit)
- Optional: production/procurement actuals

### Phase 3 — Publish-back (controlled)

- Start with monthly demand plan publishing.
- Add weekly publishing once governance is stable.
- Expand to supply plans and inventory policy publishing.

### Phase 4 — Advanced signals

- Capacity by location/work center
- Supplier reliability
- Purchase orders and inbound ETAs
- Promotions/events

## Mapping cheat sheet

| Source system object | GenXChains usage |
|---|---|
| Item master / SKU master | Products/categories |
| Sales/shipments history | Demand actuals + forecast accuracy |
| Inventory snapshot | Inventory health, alerts, days of supply |
| Production receipts / PO receipts | Supply/inventory actuals |
| Lead times | Supply feasibility + scenario modeling |

## Operating model decisions (important)

Before publish-back, define:

- **Who is allowed to publish** (often Admin or Coordinator, after Executive approval)
- **Frozen windows** (don’t overwrite near-term execution periods)
- **Versioning** (publish only one approved version)
- **Rollback** procedures
- **Audit logging** of every publish

See also: [`publish-readiness.md`](publish-readiness.md)
