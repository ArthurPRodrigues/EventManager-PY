from __future__ import annotations

import secrets
from dataclasses import dataclass, replace
from datetime import UTC, datetime

from event.domain.errors import EventHasNoTicketsAvailableError, EventNotFoundError
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository
from ticket.application.errors import TicketCodeAlreadyExistsError
from ticket.domain.ticket import Ticket
from ticket.domain.ticket_status import TicketStatus
from ticket.infra.persistence.sqlite_tickets_repository import SqliteTicketsRepository


@dataclass
class RedeemTicketInputDto:
    event_id: int
    client_id: int
    redeem_ticket_count: int
    send_email: bool = False


class RedeemTicketUseCase:
    def __init__(
        self,
        tickets_repository: SqliteTicketsRepository,
        events_repository: SqliteEventRepository,
    ) -> None:
        self._tickets_repository = tickets_repository
        self._events_repository = events_repository

    def _generate_code(self, length: int = 8) -> str:
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # excludes O, I, 0, 1
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def _generate_unique_codes(self, count: int) -> list[str]:
        if count <= 0:
            return []
        codes: set[str] = set()
        max_attempts = max(100, count * 20)
        attempts = 0
        while len(codes) < count and attempts < max_attempts:
            attempts += 1
            candidate = self._generate_code()
            if candidate in codes:
                continue
            existing = self._tickets_repository.get_by_code(candidate)
            if existing is None:
                codes.add(candidate)
        if len(codes) < count:
            raise TicketCodeAlreadyExistsError()
        return list(codes)

    def execute(self, input_dto: RedeemTicketInputDto) -> None:
        client_id = input_dto.client_id
        redeem_ticket_count = input_dto.redeem_ticket_count
        event_id = input_dto.event_id
        event = self._events_repository.get_by_id(event_id)
        tickets_available = event.tickets_available
        ticket_list = []

        if redeem_ticket_count <= 0:
            return []

        if event is None:
            raise EventNotFoundError(event_id)

        if tickets_available <= 0:
            raise EventHasNoTicketsAvailableError(event_id)

        if redeem_ticket_count > tickets_available:
            raise EventHasNoTicketsAvailableError(event.id)

        for _ in range(redeem_ticket_count):
            ticket = Ticket(
                event_id=input_dto.event_id,
                client_id=client_id,
                code=self._generate_code(),
                status=TicketStatus.PENDING,
                created_at=datetime.now(UTC),
            )
            ticket_list.append(ticket)

        self._tickets_repository.create_many(ticket_list)
        updated_event = replace(
            event, tickets_available=event.tickets_available - redeem_ticket_count
        )
        self._events_repository.update(updated_event)
