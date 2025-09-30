from __future__ import annotations

from datetime import datetime

from events.domain.events import Events
from shared.infra.persistence.sqlite import SQLiteDatabase


class SqliteEventsRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def list(
        self,
        page: int,
        page_size: int,
        created_at: str | None = None,
        end_date: str | None = None,
        location: str | None = None,
        name: str | None = None,
        start_date: str | None = None,
        tickets_available: int | None = None,
    ) -> tuple[list[Events], int]:
        offset = (page - 1) * page_size
        where: list[str] = []
        params: list[object] = []
        where_clause = f"WHERE {' AND '.join(where)}" if where else ""

        with self._db.connect() as conn:
            total = conn.execute(
                f"SELECT COUNT(*) FROM events {where_clause}",
                tuple(params),
            ).fetchone()[0]

            rows = conn.execute(
                f"""
                SELECT id, name, created_at, end_date, location, start_date, tickets_available, organizer_id
                FROM events
                {where_clause}
                ORDER BY created_at ASC, name ASC
                LIMIT ? OFFSET ?
                """,
                (*params, page_size, offset),
            ).fetchall()

        items: list[Events] = []
        for row in rows:
            (
                id_,
                name,
                created_at,
                end_date,
                location,
                start_date,
                tickets_available,
                organizer_id,
            ) = row
            event = Events(
                id=id_,
                name=name,
                created_at=datetime.fromisoformat(created_at),
                end_date=datetime.fromisoformat(end_date),
                location=location,
                start_date=datetime.fromisoformat(start_date),
                tickets_available=tickets_available,
                organizer_id=organizer_id,
            )
            items.append(event)

        return items, int(total)
