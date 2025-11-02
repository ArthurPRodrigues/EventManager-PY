from __future__ import annotations

from dataclasses import replace

from event.application.dtos import PaginatedStaffsDto, StaffDto
from shared.infra.persistence.sqlite import SQLiteDatabase
from user.domain.user import User, UserRole


class SqliteUsersRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def add(self, user: User) -> User:
        with self._db.connect() as conn:
            cursor = conn.execute(
                "INSERT INTO users (name, email, hashed_password, role) VALUES (?, ?, ?, ?)",
                (
                    user.name,
                    user.email,
                    user.hashed_password,
                    user.role,
                ),
            )
            conn.commit()
            return replace(user, id=cursor.lastrowid)

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

    def get_by_email_and_role(self, email: str, role: UserRole) -> User | None:
        with self._db.connect() as conn:
            cur = conn.execute(
                "SELECT id, name, email, hashed_password, role FROM users WHERE email = ? AND role = ?",
                (email, role.value),
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

    def list_with_email_and_name(
        self,
        page: int,
        size: int,
        name: str | None = None,
        email: str | None = None,
        event_id: int | None = None,
    ) -> PaginatedStaffsDto:
        select_columns = """
        SELECT DISTINCT
            u.id, u.name, u.email
        """
        base_query = """
        FROM users u
        INNER JOIN events e ON (',' || e.staffs_id || ',') LIKE ('%,' || CAST(u.id AS TEXT) || ',%')
        """
        conditions = ["1=1"]
        params = []

        filters = {"u.name": name, "u.email": email}

        if role := UserRole.STAFF:
            conditions.append("u.role = ?")
            params.append(role.value)

        if event_id is not None:
            conditions.append("e.id = ?")
            params.append(event_id)

        for column, value in filters.items():
            if value is not None:
                conditions.append(f"{column} = ?")
                params.append(value)

        where_clause = " WHERE " + " AND ".join(conditions)

        count_query = "SELECT COUNT(*) " + base_query + where_clause
        select_query = (
            select_columns
            + base_query
            + where_clause
            + " ORDER BY u.id ASC LIMIT ? OFFSET ?"
        )

        count_params = params.copy()

        params.extend([size, (page - 1) * size])

        with self._db.connect() as conn:
            rows = conn.execute(select_query, params).fetchall()
            total_count = conn.execute(count_query, count_params).fetchone()[0]

        staffs_list: list[StaffDto] = [
            StaffDto(
                id=row[0],
                name=row[1],
                email=row[2],
            )
            for row in rows
        ]

        return PaginatedStaffsDto(
            staff_list=staffs_list, total_staffs_count=int(total_count)
        )
