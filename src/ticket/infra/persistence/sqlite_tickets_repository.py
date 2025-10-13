from datetime import datetime

from shared.infra.persistence.sqlite import SQLiteDatabase
from ticket.domain.ticket import Ticket
from ticket.domain.ticket_status import TicketStatus


class SqliteTicketsRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def get_by_code(self, code: str) -> Ticket | None:
        with self._db.connect() as connection:
            row = connection.execute(
                """
                SELECT id, event_id, client_id, code, status, created_at
                FROM tickets
                WHERE code = ?
                """,
                (code,),
            ).fetchone()

        if not row:
            return None

        id_, event_id, client_id, code, status, created_at = row

        parsed_created_at = datetime.fromisoformat(
            created_at.replace("Z", "+00:00"),
        )

        return Ticket(
            event_id=event_id,
            client_id=client_id,
            code=code,
            status=TicketStatus[status],
            created_at=parsed_created_at,
            id=id_,
        )

    def update(self, ticket: Ticket) -> None:
        created_at_str = ticket.created_at.isoformat()

        with self._db.connect() as conn:
            conn.execute(
                """
                UPDATE tickets
                SET event_id = ?, client_id = ?, code = ?, status = ?, created_at = ?
                WHERE id = ?
                """,
                (
                    ticket.event_id,
                    ticket.client_id,
                    ticket.code,
                    ticket.status.value,
                    created_at_str,
                    ticket.id,
                ),
            )
            conn.commit()

    def create_many(self, tickets: list[Ticket]) -> None:
        rows = [
            (
                ticket.event_id,
                ticket.client_id,
                ticket.code,
                ticket.status.value,
                ticket.created_at.isoformat(),
            )
            for ticket in tickets
        ]
        with self._db.connect() as conn:
            conn.executemany(
                """
                INSERT INTO tickets (event_id, client_id, code, status, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                rows,
            )
            conn.commit()
        return tickets
