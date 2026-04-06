"""Feedback endpoint — lightweight SQLite-backed bug/comment capture."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

APP_NAME = "datacenter-optimization-valuation"
DB_PATH = Path(__file__).parent.parent / "feedback.db"

router = APIRouter(prefix="/api", tags=["feedback"])


def _get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        """CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            page TEXT NOT NULL,
            comment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )"""
    )
    conn.row_factory = sqlite3.Row
    return conn


class FeedbackIn(BaseModel):
    page: str
    comment: str


@router.post("/feedback")
def create_feedback(body: FeedbackIn):
    if not body.comment.strip():
        raise HTTPException(status_code=422, detail="Comment cannot be empty")
    db = _get_db()
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO feedback (app_name, page, comment, created_at) VALUES (?, ?, ?, ?)",
        (APP_NAME, body.page, body.comment.strip(), now),
    )
    db.commit()
    db.close()
    return {"status": "saved"}


@router.get("/feedback")
def list_feedback():
    db = _get_db()
    rows = db.execute(
        "SELECT id, app_name, page, comment, created_at FROM feedback WHERE app_name = ? ORDER BY id DESC",
        (APP_NAME,),
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]
