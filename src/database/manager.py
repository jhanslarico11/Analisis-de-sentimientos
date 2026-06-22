"""Capa de base de datos SQLite con CRUD completo."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Any, Generator, Optional

import pandas as pd

import config
from src.utils.helpers import logger, normalize_dates

COMMENTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    source TEXT,
    text TEXT,
    clean_text TEXT,
    author TEXT,
    date TEXT,
    likes INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    video_id TEXT,
    video_title TEXT,
    channel TEXT,
    url TEXT,
    candidate TEXT,
    sentiment TEXT,
    sentiment_score REAL,
    emotion TEXT,
    political_classification TEXT,
    topic TEXT,
    influence_score REAL,
    bot_probability REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_comments_candidate ON comments(candidate);",
    "CREATE INDEX IF NOT EXISTS idx_comments_sentiment ON comments(sentiment);",
    "CREATE INDEX IF NOT EXISTS idx_comments_date ON comments(date);",
    "CREATE INDEX IF NOT EXISTS idx_comments_video ON comments(video_id);",
    "CREATE INDEX IF NOT EXISTS idx_comments_author ON comments(author);",
    "CREATE INDEX IF NOT EXISTS idx_comments_source ON comments(source);",
]


class DatabaseManager:
    """Gestor CRUD para comentarios analizados."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = str(db_path or config.DB_PATH)
        config.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.db_path, timeout=config.SQLITE_TIMEOUT)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize(self) -> None:
        with self.connect() as conn:
            conn.execute(COMMENTS_SCHEMA)
            for idx in INDEXES:
                conn.execute(idx)
        logger.info("Base de datos inicializada: %s", self.db_path)

    def _serialize_value(self, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, pd.Timestamp):
            return value.isoformat()
        if hasattr(value, "item"):
            try:
                return value.item()
            except Exception:
                pass
        if isinstance(value, (bool,)):
            return int(value)
        return value

    def insert_comment(self, record: dict[str, Any]) -> bool:
        columns = [
            "id", "source", "text", "clean_text", "author", "date", "likes", "replies",
            "video_id", "video_title", "channel", "url", "candidate", "sentiment",
            "sentiment_score", "emotion", "political_classification", "topic",
            "influence_score", "bot_probability",
        ]
        values = [self._serialize_value(record.get(c)) for c in columns]
        placeholders = ", ".join(["?"] * len(columns))
        col_names = ", ".join(columns)
        sql = f"""
            INSERT INTO comments ({col_names})
            VALUES ({placeholders})
            ON CONFLICT(id) DO UPDATE SET
                text=excluded.text,
                clean_text=excluded.clean_text,
                likes=excluded.likes,
                replies=excluded.replies,
                candidate=excluded.candidate,
                sentiment=excluded.sentiment,
                sentiment_score=excluded.sentiment_score,
                emotion=excluded.emotion,
                political_classification=excluded.political_classification,
                topic=excluded.topic,
                influence_score=excluded.influence_score,
                bot_probability=excluded.bot_probability
        """
        with self.connect() as conn:
            conn.execute(sql, values)
        return True

    def insert_many(self, records: list[dict[str, Any]]) -> int:
        count = 0
        for record in records:
            try:
                self.insert_comment(record)
                count += 1
            except Exception as exc:
                logger.warning("Error insertando comentario %s: %s", record.get("id"), exc)
        return count

    def get_comment(self, comment_id: str) -> Optional[dict[str, Any]]:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,)).fetchone()
        return dict(row) if row else None

    def update_comment(self, comment_id: str, updates: dict[str, Any]) -> bool:
        if not updates:
            return False
        sets = ", ".join([f"{k} = ?" for k in updates])
        values = list(updates.values()) + [comment_id]
        with self.connect() as conn:
            cur = conn.execute(f"UPDATE comments SET {sets} WHERE id = ?", values)
        return cur.rowcount > 0

    def delete_comment(self, comment_id: str) -> bool:
        with self.connect() as conn:
            cur = conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        return cur.rowcount > 0

    def delete_all(self) -> int:
        with self.connect() as conn:
            cur = conn.execute("DELETE FROM comments")
        return cur.rowcount

    def count(self, where: str = "", params: tuple = ()) -> int:
        sql = "SELECT COUNT(*) FROM comments"
        if where:
            sql += f" WHERE {where}"
        with self.connect() as conn:
            result = conn.execute(sql, params).fetchone()
        return int(result[0]) if result else 0

    def query(
        self,
        where: str = "",
        params: tuple = (),
        order_by: str = "date DESC",
        limit: Optional[int] = None,
    ) -> pd.DataFrame:
        sql = "SELECT * FROM comments"
        if where:
            sql += f" WHERE {where}"
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"
        with self.connect() as conn:
            df = pd.read_sql_query(sql, conn, params=params)
        return normalize_dates(df, "date")

    def get_all_comments(self) -> pd.DataFrame:
        return self.query()

    def get_by_candidate(self, candidate: str) -> pd.DataFrame:
        return self.query("candidate = ?", (candidate,))

    def get_by_sentiment(self, sentiment: str) -> pd.DataFrame:
        return self.query("sentiment = ?", (sentiment,))

    def get_top_influential(self, n: int = 20) -> pd.DataFrame:
        return self.query(order_by="influence_score DESC", limit=n)

    def get_suspicious(self, threshold: float = 0.6) -> pd.DataFrame:
        return self.query("bot_probability >= ?", (threshold,), order_by="bot_probability DESC")

    def aggregate_stats(self) -> dict[str, Any]:
        with self.connect() as conn:
            total = conn.execute("SELECT COUNT(*) FROM comments").fetchone()[0]
            by_candidate = pd.read_sql_query(
                "SELECT candidate, COUNT(*) as count FROM comments GROUP BY candidate", conn
            )
            by_sentiment = pd.read_sql_query(
                "SELECT sentiment, COUNT(*) as count FROM comments GROUP BY sentiment", conn
            )
            by_emotion = pd.read_sql_query(
                "SELECT emotion, COUNT(*) as count FROM comments GROUP BY emotion", conn
            )
            by_topic = pd.read_sql_query(
                "SELECT topic, COUNT(*) as count FROM comments GROUP BY topic", conn
            )
        return {
            "total": total,
            "by_candidate": by_candidate,
            "by_sentiment": by_sentiment,
            "by_emotion": by_emotion,
            "by_topic": by_topic,
        }

    def dataframe_to_db(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0
        records = df.to_dict(orient="records")
        return self.insert_many(records)
