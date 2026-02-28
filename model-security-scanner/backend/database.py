"""SQLite scan history database."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "scan_history.db")


def _conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = _conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            scan_date TEXT NOT NULL,
            total_score INTEGER NOT NULL,
            max_score INTEGER NOT NULL,
            results_json TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_scan(model_name: str, total_score: int, max_score: int, results: list[dict]):
    conn = _conn()
    conn.execute(
        "INSERT INTO scan_history (model_name, scan_date, total_score, max_score, results_json) VALUES (?, ?, ?, ?, ?)",
        (model_name, datetime.now().isoformat(), total_score, max_score, json.dumps(results)),
    )
    conn.commit()
    conn.close()


def get_scan_history(limit: int = 50) -> list[dict]:
    conn = _conn()
    cursor = conn.execute(
        "SELECT id, model_name, scan_date, total_score, max_score, results_json FROM scan_history ORDER BY scan_date DESC LIMIT ?",
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": r[0], "model_name": r[1], "scan_date": r[2], "total_score": r[3], "max_score": r[4], "results": json.loads(r[5])}
        for r in rows
    ]


def get_scan_by_id(scan_id: int) -> dict | None:
    conn = _conn()
    cursor = conn.execute(
        "SELECT id, model_name, scan_date, total_score, max_score, results_json FROM scan_history WHERE id = ?",
        (scan_id,),
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "model_name": row[1], "scan_date": row[2], "total_score": row[3], "max_score": row[4], "results": json.loads(row[5])}
    return None
