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
