from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from event.application.dtos import PaginatedEventsDto
from event.domain.event import Event
from shared.infra.persistence.sqlite import SQLiteDatabase


class SqliteEventRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def list(
        self,
        page: int,
        page_size: int,
        filter_mode: str | None = None,
        user_id: int | None = None,
    ) -> PaginatedEventsDto:
        base_query = "FROM events"
        conditions: list[str] = ["1=1"]
        params: list = []

        if filter_mode == "WITH_TICKETS":
            conditions.append("(max_tickets - tickets_redeemed) > 0")
        elif filter_mode == "SOLD_OUT":
            conditions.append("(max_tickets - tickets_redeemed) = 0")

        where_clause = " WHERE " + " AND ".join(conditions)

        count_query = "SELECT COUNT(*) " + base_query + where_clause
        select_query = (
            "SELECT id, name, location, created_at, start_date, end_date, "
            "max_tickets, initial_max_tickets, organizer_id, staffs_id, tickets_redeemed "
            + base_query
            + where_clause
            + " ORDER BY id ASC LIMIT ? OFFSET ?"
        )

        count_params = list(params)
        params.extend([page_size, (page - 1) * page_size])

        with self._db.connect() as conn:
            rows = conn.execute(select_query, params).fetchall()
            total_event_count = conn.execute(count_query, count_params).fetchone()[0]

        def _to_event(row) -> Event:
            return Event(
                id=row[0],
                name=row[1],
                location=row[2],
                created_at=datetime.fromisoformat(row[3])
                if isinstance(row[3], str)
                else row[3],
                start_date=datetime.fromisoformat(row[4])
                if isinstance(row[4], str)
                else row[4],
                end_date=datetime.fromisoformat(row[5])
                if isinstance(row[5], str)
                else row[5],
                max_tickets=row[6],
                initial_max_tickets=row[7],
                organizer_id=row[8],
                staffs_id=(row[9].split(",") if row[9] else []),
                tickets_redeemed=row[10],
            )

        event_list: list[Event] = [_to_event(r) for r in rows]

        return PaginatedEventsDto(
            event_list=event_list, total_event_count=int(total_event_count)
        )

    def add(self, event: Event) -> Event:
        with self._db.connect() as conn:
            try:
                cursor = conn.execute(
                    """
                    INSERT INTO events (name, created_at, end_date, location, start_date, max_tickets, organizer_id, staffs_id, tickets_redeemed, initial_max_tickets)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        event.name,
                        event.created_at.isoformat(),
                        event.end_date.isoformat(),
                        event.location,
                        event.start_date.isoformat(),
                        event.max_tickets,
                        event.organizer_id,
                        (event.staffs_id and ",".join(event.staffs_id)) or None,
                        event.tickets_redeemed,
                        event.initial_max_tickets,
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
                SELECT id, name, end_date, start_date, location, max_tickets, organizer_id, staffs_id, created_at, initial_max_tickets, tickets_redeemed
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
            max_tickets=row[5],
            organizer_id=row[6],
            staffs_id=row[7].split(",") if row[7] else None,
            created_at=datetime.fromisoformat(row[8]),
            initial_max_tickets=row[9],
            tickets_redeemed=row[10],
        )

    def update(self, event: Event) -> None:
        with self._db.connect() as conn:
            conn.execute(
                """
                UPDATE events
                SET name = ?, end_date = ?, start_date = ?, location = ?, max_tickets = ?, tickets_redeemed = ?, initial_max_tickets = ?
                WHERE id = ?
                """,
                (
                    event.name,
                    event.end_date.isoformat(),
                    event.start_date.isoformat(),
                    event.location,
                    event.max_tickets,
                    event.tickets_redeemed,
                    event.initial_max_tickets,
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
