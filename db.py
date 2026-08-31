"""SQLite data layer.

Demonstrates the auto-init pattern (tables + seed data created on first run)
and parameterized queries (no string formatting -> no SQL injection).
The database path is read from the DB_PATH environment variable, never
hardcoded, so no secret or environment-specific value lives in the code.
"""

import os
import sqlite3
from datetime import datetime, timezone


# --- Reference data: obesity-related dosing / monitoring alerts ----------
# These are educational prompts, not a formulary. Higher classes inherit
# the alerts of the classes below them.
_CLASS_I_ALERTS = [
    ("Enoxaparin",
     "Dose on total body weight; consider anti-Xa monitoring for prolonged "
     "or therapeutic courses."),
    ("Vancomycin",
     "Dose on total body weight but cap; obesity raises volume of "
     "distribution - monitor trough/AUC levels."),
    ("Gentamicin (aminoglycosides)",
     "Use adjusted body weight to avoid overdosing; monitor levels and renal "
     "function."),
    ("Levothyroxine",
     "Titrate to lean/ideal body weight and TSH - total-body-weight dosing "
     "risks over-replacement."),
]

_CLASS_II_EXTRA = [
    ("Apixaban / Rivaroxaban (DOACs)",
     "Efficacy data limited at high body weight; consider drug-specific level "
     "checks or an alternative anticoagulant."),
    ("Unfractionated heparin",
     "Weight-based bolus/infusion may need dose capping; titrate to "
     "aPTT/anti-Xa."),
]

_CLASS_III_EXTRA = [
    ("Sugammadex",
     "Dose on actual body weight."),
    ("Propofol",
     "Induce on total body weight but maintain on adjusted/lean body weight "
     "to avoid accumulation."),
]


def _seed_rows():
    """Build the full list of (obesity_class, drug, alert) rows to seed."""
    rows = [("Class I", d, a) for d, a in _CLASS_I_ALERTS]
    rows += [("Class II", d, a)
             for d, a in _CLASS_I_ALERTS + _CLASS_II_EXTRA]
    rows += [("Class III", d, a)
             for d, a in _CLASS_I_ALERTS + _CLASS_II_EXTRA + _CLASS_III_EXTRA]
    return rows


def _db_path():
    return os.getenv("DB_PATH", "bmi_app.db")


def get_connection():
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if missing and seed reference data idempotently."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS drug_alerts (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                obesity_class TEXT NOT NULL,
                drug_name     TEXT NOT NULL,
                alert         TEXT NOT NULL,
                UNIQUE (obesity_class, drug_name)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS calculation_log (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                weight_kg  REAL NOT NULL,
                height_cm  REAL NOT NULL,
                bmi        REAL NOT NULL,
                category   TEXT NOT NULL
            )
            """
        )
        # Parameterized insert; INSERT OR IGNORE makes seeding idempotent.
        cur.executemany(
            "INSERT OR IGNORE INTO drug_alerts "
            "(obesity_class, drug_name, alert) VALUES (?, ?, ?)",
            _seed_rows(),
        )
        conn.commit()
    finally:
        conn.close()


def get_alerts(obesity_class):
    """Return list of {drug_name, alert} for an obesity class (parameterized)."""
    if not obesity_class:
        return []
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT drug_name, alert FROM drug_alerts "
            "WHERE obesity_class = ? ORDER BY drug_name",
            (obesity_class,),
        )
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def log_calculation(weight_kg, height_cm, bmi, category):
    """Store a calculation. Stores anthropometrics only - no identifiers."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO calculation_log "
            "(created_at, weight_kg, height_cm, bmi, category) "
            "VALUES (?, ?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(),
             weight_kg, height_cm, bmi, category),
        )
        conn.commit()
    finally:
        conn.close()
