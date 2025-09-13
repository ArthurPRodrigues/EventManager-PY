from __future__ import annotations

from shared.infra.persistence.sqlite import SQLiteDatabase
from user.domain.user import User


class SqliteUserRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    # todo: trocar conn para connection
    def add(self, user: User) -> None:
        with self._db.connect() as conn:
            conn.execute(
                "INSERT INTO friendships (name, email, hashed_password, role) VALUES (?, ?, ?, ?)",
                (
                    user.name,
                    user.email,
                    user.hashed_password,
                    user.role,
                ),
            )
            conn.commit()
