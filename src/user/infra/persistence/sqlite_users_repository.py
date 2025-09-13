from __future__ import annotations

from shared.infra.persistence.sqlite import SQLiteDatabase
from user.domain.user import User


class SqliteUsersRepository:
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

    def get_by_id(self, id: int) -> User | None:
        with self._db.connect() as conn:
            row = conn.execute(
                """
                SELECT id, name, email, hashed_password, role
                FROM users
                WHERE id = ?
                """,
                (id,),
            ).fetchone()

        if not row:
            return None

        user_id, name, email, hashed_password, role = row

        return User(
            id=user_id,
            name=name,
            email=email,
            hashed_password=hashed_password,
            role=role,
        )
