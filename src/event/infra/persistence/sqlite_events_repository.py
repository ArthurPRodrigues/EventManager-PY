from __future__ import annotations

from datetime import datetime

from shared.infra.persistence.sqlite import SQLiteDatabase
from event.domain.event import Event

class SqliteEventsRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def add(self, event: Event) -> Event:
        with self._db.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO events (name, start_date, end_date, location, tickets_available, created_at, id, organizer_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.name,
                    event.start_date.isoformat(),
                    event.end_date.isoformat(),
                    event.location,
                    event.tickets_available,
                    event.created_at.isoformat(),
                    event.organizer_id,
                ),
            )
            event.id = cursor.lastrowid
            conn.commit()
            return self.get_by_id(event.id)