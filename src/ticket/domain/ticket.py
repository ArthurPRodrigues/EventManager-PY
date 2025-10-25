from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from .errors import (
    InvalidClientIdError,
    InvalidCodeError,
    InvalidEventIdError,
    InvalidStatusError,
    TicketAlreadyValidatedError,
    TicketNotActiveError,
)
from .ticket_status import TicketStatus


@dataclass(frozen=True)
class Ticket:
    event_id: int
    client_id: int
    code: str
    status: TicketStatus
    created_at: datetime
    id: int | None = None

    @staticmethod
    def create(
        event_id: int,
        client_id: int,
        code: str,
        status: TicketStatus,
        created_at: datetime,
        id: int | None = None,
    ) -> Ticket:
        if not isinstance(event_id, int) or event_id <= 0:
            raise InvalidEventIdError(event_id)
        if not isinstance(client_id, int) or client_id <= 0:
            raise InvalidClientIdError(client_id)
        if not isinstance(code, str) or not code.strip():
            raise InvalidCodeError(code)
        if not isinstance(status, TicketStatus):
            raise InvalidStatusError(status)
        if not isinstance(created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        return Ticket(
            event_id=event_id,
            client_id=client_id,
            code=code,
            status=status,
            created_at=created_at,
            id=id,
        )

    def validate(self) -> Ticket:
        if self.status == TicketStatus.VALIDATED:
            raise TicketAlreadyValidatedError()
        if self.status != TicketStatus.PENDING:
            raise TicketNotActiveError(self.id or self.code)
        return replace(self, status=TicketStatus.VALIDATED)
