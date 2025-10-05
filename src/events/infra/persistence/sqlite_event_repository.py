from __future__ import annotations

from shared.infra.persistence.sqlite import SQLiteDatabase


class SqliteEventRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def list(
        self,
        page: int,
        page_size: int,
        organizer_id: int | None = None,
    ) -> tuple[list[tuple], int]:
        page = max(1, page)
        page_size = max(1, page_size)
        offset = (page - 1) * page_size

        params: list[object] = []
        where_sql = ""
        if organizer_id is not None:
            where_sql = " WHERE organizer_id = ?"
            params.append(organizer_id)

        count_sql = "SELECT COUNT(*) FROM events" + where_sql
        data_sql = (
            "SELECT id, name, location, start_date, end_date, tickets_available, organizer_id, created_at "
            "FROM events"
            + where_sql
            + " ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?"
        )

        with self._db.connect() as conn:
            total = conn.execute(count_sql, tuple(params)).fetchone()[0]
            if total == 0:
                return [], 0
            rows = conn.execute(data_sql, (*params, page_size, offset)).fetchall()

        return rows, int(total)

    def list_by_id(self, event_id: int) -> tuple | None:
        query = "SELECT id, name, location, start_date, end_date, tickets_available, organizer_id, created_at FROM events WHERE id = ?"
        with self._db.connect() as conn:
            return conn.execute(query, (event_id,)).fetchone()

    def decrement_tickets_available(self, event_id: int) -> None:
        query = "UPDATE events SET tickets_available = tickets_available - 1 WHERE id = ? AND tickets_available > 0"
        with self._db.connect() as conn:
            conn.execute(query, (event_id,))
            conn.commit()
