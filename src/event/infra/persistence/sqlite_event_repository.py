from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

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
        name: str | None = None,
        location: str | None = None,
        created_at: datetime | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        initial_max_tickets: int | None = None,
        max_tickets: int | None = None,
        tickets_redeemed: int | None = None,
        organizer_id: int | None = None,
        id: int | None = None,
        filter_mode: str | None = None,
        user_id: int | None = None,
    ) -> PaginatedEventsDto | None:
        base_query = "FROM events"
        conditions = ["1=1"]
        params = []

        filters = {
            "name": name,
            "location": location,
            "created_at": created_at,
            "start_date": start_date,
            "end_date": end_date,
            "initial_max_tickets": initial_max_tickets,
            "max_tickets": max_tickets,
            "tickets_redeemed": tickets_redeemed,
            "organizer_id": organizer_id,
        }

        for column, value in filters.items():
            if value is not None:
                conditions.append(f"{column} = ?")
                params.append(value)

        if filter_mode == "WITH_TICKETS":
            conditions.append("(max_tickets - tickets_redeemed) > 0")
        elif filter_mode == "SOLD_OUT":
            conditions.append("(max_tickets - tickets_redeemed) = 0")

        where_clause = " WHERE " + " AND ".join(conditions)

        count_query = "SELECT COUNT(*) " + base_query + where_clause
        select_query = (
            "SELECT id, name, location, created_at, start_date, end_date, "
            "initial_max_tickets, max_tickets, tickets_redeemed, organizer_id "
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
                created_at=datetime.fromisoformat(row[3]).replace(tzinfo=UTC),
                start_date=datetime.fromisoformat(row[4]).replace(tzinfo=UTC),
                end_date=datetime.fromisoformat(row[5]).replace(tzinfo=UTC),
                initial_max_tickets=row[6],
                max_tickets=row[7],
                tickets_redeemed=row[8],
                organizer_id=row[9],
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
                    INSERT INTO events (name, created_at, end_date, location, start_date, max_tickets, organizer_id, tickets_redeemed, initial_max_tickets)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        event.name,
                        event.created_at,
                        event.end_date,
                        event.location,
                        event.start_date,
                        event.max_tickets,
                        event.organizer_id,
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
                SELECT id, name, location, created_at, start_date, end_date, max_tickets, organizer_id, initial_max_tickets, tickets_redeemed
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
            location=row[2],
            created_at=datetime.fromisoformat(row[3]).replace(tzinfo=UTC),
            start_date=datetime.fromisoformat(row[4]).replace(tzinfo=UTC),
            end_date=datetime.fromisoformat(row[5]).replace(tzinfo=UTC),
            max_tickets=row[6],
            organizer_id=row[7],
            initial_max_tickets=row[8],
            tickets_redeemed=row[9],
        )

    def update(self, event: Event) -> None:
        assert event is not None
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
