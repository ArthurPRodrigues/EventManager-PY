from __future__ import annotations

import secrets
from dataclasses import dataclass, replace
from datetime import UTC, datetime

from event.domain.errors import EventHasNoTicketsAvailableError, EventNotFoundError
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository
from shared.infra.email.smtp_ticket_email_service import SmtpEmailService
from shared.infra.html_template.html_template_engine import HtmlTemplateEngine
from ticket.application.errors import TicketCodeAlreadyExistsError
from ticket.domain.ticket import Ticket
from ticket.domain.ticket_status import TicketStatus
from ticket.infra.persistence.sqlite_ticket_repository import SqliteTicketRepository
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


@dataclass
class RedeemTicketInputDto:
    event_id: int
    client_id: int
    redeem_ticket_count: int
    send_email: bool = False


class RedeemTicketUseCase:
    def __init__(
        self,
        tickets_repository: SqliteTicketRepository,
        events_repository: SqliteEventRepository,
        users_repository: SqliteUsersRepository | None = None,
        email_service: SmtpEmailService | None = None,
        template_engine: HtmlTemplateEngine | None = None,
    ) -> None:
        self._tickets_repository = tickets_repository
        self._events_repository = events_repository
        self._users_repository = users_repository
        self._email_service = email_service
        self._template_engine = template_engine

    def _generate_code(self, length: int = 6) -> str:
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
        event_name = event.name
        send_email = input_dto.send_email
        ticket_list = []

        if event is None:
            raise EventNotFoundError(event_id)

        if redeem_ticket_count > max(0, event.max_tickets - event.tickets_redeemed):
            raise EventHasNoTicketsAvailableError(event_name)

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
            event,
            tickets_redeemed=event.tickets_redeemed + redeem_ticket_count,
        )
        self._events_repository.update(updated_event)

        if send_email:
            if not (
                self._users_repository and self._template_engine and self._email_service
            ):
                return
            try:
                user = self._users_repository.get_by_id(client_id)
                if user is not None and getattr(user, "email", None):
                    codes_html = "<br>".join(t.code for t in ticket_list)
                    body = self._template_engine.render(
                        "redeem_ticket.html",
                        {
                            "user_name": getattr(user, "name", ""),
                            "ticket_code": codes_html,
                        },
                    )
                    subject = "Your ticket(s) were redeemed"
                    self._email_service.send_email(user.email, subject, body)
            except Exception:
                pass
