from __future__ import annotations

from typing import Optional

from shared.infra.persistence.sqlite import SQLiteDatabase
from user.domain.user import User, UserRole


class SqliteUsersRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    # todo: trocar conn para connection
    def add(self, user: User) -> None:
        with self._db.connect() as conn:
            conn.execute(
                "INSERT INTO users (name, email, hashed_password, role) VALUES (?, ?, ?, ?)",
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

    def get_by_email_and_role(self, email: str, role: UserRole) -> Optional[User]:
        with self._db.connect() as conn:
            cur = conn.execute(
                "SELECT id, name, email, password_hash, role FROM users WHERE email = ? AND role = ?",
                (email.strip().lower(), role.value),
            )
            row = cur.fetchone()
            if not row:
                return None
            user_id, name, email, hashed_password, role = row
            return User(
                name=name,
                email=email,
                hashed_password=hashed_password,
                role=UserRole(role),
                id=user_id,
            )
