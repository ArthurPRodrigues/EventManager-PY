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
            code=code,
            created_at=created_at,
            status=status,
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
