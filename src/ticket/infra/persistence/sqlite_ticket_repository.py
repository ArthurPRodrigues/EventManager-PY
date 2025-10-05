from __future__ import annotations

from dataclasses import replace

from shared.infra.persistence.sqlite import SQLiteDatabase
from ticket.domain.ticket import Ticket


class SqliteTicketRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def list_by_event_id(self, event_id: int) -> tuple | None:
        query = "SELECT id, code, created_at, status, event_id, client_id FROM tickets WHERE event_id = ?"
        with self._db.connect() as conn:
            return conn.execute(query, (event_id,)).fetchone()

    def add(self, ticket: Ticket) -> Ticket:
        query = "INSERT INTO tickets (code, created_at, status, event_id, client_id) VALUES (?, ?, ?, ?, ?)"
        with self._db.connect() as conn:
            cursor = conn.execute(
                query,
                (
                    ticket.code,
                    ticket.created_at,
                    ticket.status.value,
                    ticket.event_id,
                    ticket.client_id,
                ),
            )
            conn.commit()
            return replace(ticket, id=cursor.lastrowid)

    def list_by_user_id(self, user_id: int) -> list[tuple]:
        query = "SELECT id, code, created_at, status, event_id, client_id FROM tickets WHERE client_id = ?"
        with self._db.connect() as conn:
            rows = conn.execute(query, (user_id,)).fetchall()
            return rows
