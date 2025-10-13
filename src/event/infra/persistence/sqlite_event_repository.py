from __future__ import annotations

from datetime import datetime

from event.application.dtos import Event, PaginatedEventsDto
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

    def get_by_id(self, event_id: int) -> Event | None:
        query = (
            "SELECT id, name, location, created_at, start_date, end_date, "
            "tickets_available, organizer_id, staffs_id FROM events WHERE id = ?"
        )
        with self._db.connect() as conn:
            row = conn.execute(query, (event_id,)).fetchone()

        if not row:
            return None

        return Event(
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

    def update(self, event: Event) -> None:
        with self._db.connect() as conn:
            conn.execute(
                """
                UPDATE events
                SET name = ?, location = ?, created_at = ?, start_date = ?, end_date = ?,
                    tickets_available = ?, organizer_id = ?, staffs_id = ?
                WHERE id = ?
                """,
                (
                    event.name,
                    event.location,
                    event.created_at,
                    event.start_date,
                    event.end_date,
                    event.tickets_available,
                    event.organizer_id,
                    ",".join(event.staffs_id) if event.staffs_id else "",
                    event.id,
                ),
            )
            conn.commit()
