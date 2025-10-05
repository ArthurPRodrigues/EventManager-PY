from datetime import datetime

from ticket.domain.ticket_status import TicketStatus

from ticket.domain.errors import InvalidCodeError


class Ticket:
    def __init__(
        self,
        code: str,
        created_at: datetime,
        status: TicketStatus,
        event_id: int,
        client_id: int,
        id: int,
    ):
        self.code = code
        self.created_at = created_at
        self.status = status
        self.event_id = event_id
        self.client_id = client_id
        self.id = id

    @staticmethod
    def create(
        code: str,
        created_at: datetime,
        status: TicketStatus,
        event_id: int,
        client_id: int | None = None,
    ) -> "Ticket":
        if not code or not code.strip():
            raise InvalidCodeError(code)
        if not created_at or not isinstance(created_at, datetime):
            raise ValueError("created_at must be a valid datetime")
        if not isinstance(status, TicketStatus):
            raise ValueError("status must be a valid TicketStatus")
        if not event_id or not isinstance(event_id, int):
            raise ValueError("event_id must be a valid integer")
        if client_id is not None and not isinstance(client_id, int):
            raise ValueError("client_id must be a valid integer or None")

        return Ticket(
            code=code,
            created_at=created_at,
            status=status,
            event_id=event_id,
            client_id=client_id if client_id is not None else -1,
            id=None,
        )
