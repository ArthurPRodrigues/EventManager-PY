from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from event.application.dtos import Event, PaginatedEventsDto
from event.application.errors import EventNotFoundError
from shared.infra.persistence.sqlite import SQLiteDatabase


class SqliteEventRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def list(
        self,
        page: int,
        page_size: int,
        name: str | None = None,
        location: str | None = None,
        created_at: datetime | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        tickets_available: int | None = None,
        organizer_id: int | None = None,
        staffs_id: list[str] | None = None,
        id: int | None = None,
        filter_mode: str | None = None,
    ) -> PaginatedEventsDto | None:
        base_query = "FROM events"
        conditions = ["1=1"]
        params = []

        filters = {
            "id": id,
            "name": name,
            "location": location,
            "created_at": created_at,
            "start_date": start_date,
            "end_date": end_date,
            "tickets_available": tickets_available,
            "organizer_id": organizer_id,
        }

        for column, value in filters.items():
            if value is not None:
                conditions.append(f"{column} = ?")
                params.append(value)

        if filter_mode == "WITH_TICKETS":
            conditions.append("tickets_available > 0")
        elif filter_mode == "SOLD_OUT":
            conditions.append("tickets_available = 0")

        if staffs_id:
            for staff_id in staffs_id:
                conditions.append("',' || staffs_id || ',' LIKE ?")
                params.append(f"%,{staff_id},%")

        where_clause = " WHERE " + " AND ".join(conditions)

        count_query = "SELECT COUNT(*) " + base_query + where_clause
        select_query = (
            "SELECT id, name, location, created_at, start_date, end_date, "
            "tickets_available, organizer_id, staffs_id "
            + base_query
            + where_clause
            + " ORDER BY id ASC LIMIT ? OFFSET ?"
        )

        count_params = params.copy()

        params.extend([page_size, (page - 1) * page_size])

        with self._db.connect() as conn:
            rows = conn.execute(select_query, params).fetchall()
            total_event_count = conn.execute(count_query, count_params).fetchone()[0]

        event_list: list[Event] = [
            Event(
                id=row[0],
                name=row[1],
                location=row[2],
                created_at=row[3],
                start_date=row[4],
                end_date=row[5],
                tickets_available=row[6],
                organizer_id=row[7],
                staffs_id=row[8].split(",") if row[8] else [],
            )
            for row in rows
        ]

        return PaginatedEventsDto(
            event_list=event_list, total_event_count=int(total_event_count)
        )

    def add(self, event: Event) -> Event:
        with self._db.connect() as conn:
            try:
                cursor = conn.execute(
                    """
                    INSERT INTO events (name, created_at, end_date, location, start_date, tickets_available, organizer_id, staffs_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        event.name,
                        event.created_at.isoformat(),
                        event.end_date.isoformat(),
                        event.location,
                        event.start_date.isoformat(),
                        event.tickets_available,
                        event.organizer_id,
                        (event.staffs_id and ",".join(event.staffs_id)) or None,
                    ),
                )
                conn.commit()
                return replace(event, id=cursor.lastrowid)

            except Exception as e:
                conn.rollback()
                raise e

    def get_by_id(self, id: int) -> Event | None:
        with self._db.connect() as conn:
            row = conn.execute(
                """
                SELECT id, name, end_date, start_date, location, tickets_available, organizer_id, staffs_id, created_at
                FROM events
                WHERE id = ?
                """,
                (id,),
            ).fetchone()

        if not row:
            return None

        return Event(
            id=row[0],
            name=row[1],
            end_date=datetime.fromisoformat(row[2]),
            start_date=datetime.fromisoformat(row[3]),
            location=row[4],
            tickets_available=row[5],
            organizer_id=row[6],
            staffs_id=row[7].split(",") if row[7] else None,
            created_at=datetime.fromisoformat(row[8]),
        )

    def update(self, event: Event) -> None:
        assert event is not None
        existing_event = self.get_by_id(event.id)
        if not existing_event:
            raise EventNotFoundError(existing_event.id)
        with self._db.connect() as conn:
            conn.execute(
                """
                UPDATE events
                SET name = ?, end_date = ?, start_date = ?, location = ?, tickets_available = ?
                WHERE id = ?
                """,
                (
                    event.name,
                    event.end_date,
                    event.start_date,
                    event.location,
                    event.tickets_available,
                    event.id,
                ),
            )
            conn.commit()

    def delete(self, id: int) -> None:
        with self._db.connect() as conn:
            conn.execute(
                """
                DELETE FROM events
                WHERE id = ?
                """,
                (id,),
            )
            conn.commit()
