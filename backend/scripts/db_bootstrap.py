"""Bring a database under Alembic control.

This project predates its own migration chain: databases were created with
``Base.metadata.create_all()`` and were never stamped, so ``alembic_version``
does not exist and the hardening constraints from revision 20260227_0002 were
never applied. This script resolves either situation.

Usage:
    python scripts/db_bootstrap.py --check         # report state, change nothing
    python scripts/db_bootstrap.py --fresh         # empty DB -> upgrade head
    python scripts/db_bootstrap.py --stamp-legacy  # adopt an unstamped DB as-is

A legacy database cannot be replayed through the chain: create_all built each
table whenever its model first appeared, so different tables sit at different
eras — some already carry indexes revision 20260227_0002 creates while lacking
the constraints from that same revision. Replaying it fails partway and leaves
a half-migrated schema.

--stamp-legacy therefore only records the database at head so that *future*
revisions apply cleanly. It does NOT retrofit the constraints the database
never received; run --check afterwards to see which are missing. The only way
to get a fully hardened schema is to rebuild: --fresh into a new file and
reload data (seed_data.py for development).

Back up before any of this; the runbook is scripts/backup_restore_runbook.sh.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from app.config import settings

# Constraints revision 20260227_0002 is responsible for. A legacy database
# typically has none of them; --check reports which are actually missing so the
# gap is visible rather than assumed.
HARDENED_TABLES = ("demand_plans", "supply_plans", "forecasts", "inventory", "scenarios")


def _config() -> Config:
    cfg = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    cfg.set_main_option("script_location", str(Path(__file__).resolve().parents[1] / "alembic"))
    return cfg


def _state() -> tuple[bool, bool, list[str]]:
    engine = create_engine(settings.DATABASE_URL)
    insp = inspect(engine)
    tables = sorted(insp.get_table_names())
    return ("alembic_version" in tables, bool(set(tables) - {"alembic_version"}), tables)


def _missing_hardening() -> list[str]:
    """Report core tables that never received their CHECK constraints."""
    engine = create_engine(settings.DATABASE_URL)
    missing = []
    with engine.connect() as conn:
        for table in HARDENED_TABLES:
            row = conn.exec_driver_sql(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,)
            ).fetchone()
            if row and row[0] and "CHECK" not in row[0].upper():
                missing.append(table)
    return missing


def check() -> int:
    stamped, has_tables, tables = _state()
    print(f"database : {settings.DATABASE_URL}")
    print(f"tables   : {len(tables)}")
    print(f"stamped  : {stamped}")

    if not has_tables:
        print("\nEmpty database. Run: python scripts/db_bootstrap.py --fresh")
        return 0

    if settings.DATABASE_URL.startswith("sqlite"):
        missing = _missing_hardening()
        if missing:
            print(f"unhardened: {', '.join(missing)} (no CHECK constraints)")
        else:
            print("unhardened: none")

    if not stamped:
        print("\nLegacy database built outside Alembic.")
        print("Run: python scripts/db_bootstrap.py --stamp-legacy")
        print("Note: stamping does not retrofit missing constraints; rebuild with")
        print("      --fresh into a new file for a fully hardened schema.")
    else:
        print("\nUnder Alembic control. Run: alembic upgrade head")
    return 0


def fresh() -> int:
    stamped, has_tables, _ = _state()
    if has_tables:
        print("Refusing --fresh: database is not empty. Use --adopt.")
        return 1
    command.upgrade(_config(), "head")
    print("Database created at head.")
    return 0


def stamp_legacy() -> int:
    stamped, has_tables, _ = _state()
    if stamped:
        print("Refusing: database is already stamped. Use `alembic upgrade head`.")
        return 1
    if not has_tables:
        print("Refusing: database is empty. Use --fresh.")
        return 1

    command.stamp(_config(), "head")
    print("Database stamped at head. Future revisions will apply normally.")

    if settings.DATABASE_URL.startswith("sqlite"):
        missing = _missing_hardening()
        if missing:
            print(
                "\nWARNING: these tables still have no CHECK constraints and "
                f"stamping did not add them: {', '.join(missing)}."
                "\nRebuild with --fresh into a new file for a hardened schema."
            )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="report state only")
    group.add_argument("--fresh", action="store_true", help="empty database -> head")
    group.add_argument(
        "--stamp-legacy", action="store_true",
        help="record an unstamped legacy database at head (adds no constraints)",
    )
    args = parser.parse_args()

    if args.check:
        return check()
    if args.fresh:
        return fresh()
    return stamp_legacy()


if __name__ == "__main__":
    raise SystemExit(main())
