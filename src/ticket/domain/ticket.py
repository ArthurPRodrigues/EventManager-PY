from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime

from .errors import (
    InvalidClientIdError,
    InvalidEventIdError,
    InvalidTicketCodeError,
    TicketAlreadyValidatedError,
)
from .ticket_status import TicketStatus


@dataclass(frozen=True)
class Ticket:
    event_id: int
    client_id: int
    code: str
    status: TicketStatus = TicketStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: int | None = None

    @staticmethod
    def create(event_id: int, client_id: int, code: str) -> Ticket:
        if not isinstance(event_id, int) or event_id <= 0:
            raise InvalidEventIdError(event_id)
        if not isinstance(client_id, int) or client_id <= 0:
            raise InvalidClientIdError(client_id)
        if not isinstance(code, str) or not code.strip():
            raise InvalidTicketCodeError(code)
        return Ticket(
            event_id=event_id,
            client_id=client_id,
            code=code,
        )

    def validate(self) -> Ticket:
        if self.status is not TicketStatus.PENDING:
            raise TicketAlreadyValidatedError()
        return replace(self, status=TicketStatus.VALIDATED)
