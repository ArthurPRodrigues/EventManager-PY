from __future__ import annotations

import os
import sqlite3


class SQLiteDatabase:
    def __init__(self, path: str | None = None) -> None:
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
                    hashed_password TEXT NOT NULL,
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
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at datetime NOT NULL,
                    end_date datetime NOT NULL,
                    location TEXT NOT NULL,
                    name TEXT NOT NULL,
                    start_date datetime NOT NULL,
                    tickets_available datetime NOT NULL,
                    organizer_id INTEGER NOT NULL,
                    FOREIGN KEY(organizer_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """
            )
            conn.commit()
