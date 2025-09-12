from __future__ import annotations

import os
import sqlite3
from typing import Optional


class SQLiteDatabase:
    def __init__(self, path: Optional[str] = None) -> None:
        self._path = path or os.path.join("data", "app.db")
        os.makedirs(os.path.dirname(self._path), exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS friendships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requester_client_id INTEGER NOT NULL,
                    requested_client_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    accepted_at TIMESTAMP NULL,
                    UNIQUE(requester_client_id, requested_client_id),
                    FOREIGN KEY(requested_client_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY(requester_client_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """
            )
            conn.commit()
