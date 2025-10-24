from __future__ import annotations

import secrets
from dataclasses import dataclass, replace
from datetime import UTC, datetime

from event.domain.errors import EventHasNoTicketsAvailableError, EventNotFoundError
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository
from shared.infra.email.smtp_ticket_email_service import SmtpEmailService
from shared.infra.html_template.html_template_engine import HtmlTemplateEngine
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

    def _send_email_to_client(self, client_id: int, ticket_list) -> None:
        user = self._users_repository.get_by_id(client_id)
        if user is not None:
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

    def _get_event_or_raise(self, event_id: int):
        event = self._events_repository.get_by_id(event_id)
        if event is None:
            raise EventNotFoundError(event_id)
        return event

    def _get_ticket_available_or_raise(self, event, redeem_ticket_count):
        if redeem_ticket_count > max(0, event.max_tickets - event.tickets_redeemed):
            raise EventHasNoTicketsAvailableError(event.name)

    def list_event(self, input_dto: RedeemTicketInputDto) -> None:
        client_id = input_dto.client_id
        redeem_ticket_count = input_dto.redeem_ticket_count
        event_id = input_dto.event_id
        event = self._events_repository.get_by_id(event_id)
        send_email = input_dto.send_email
        ticket_list = []

        event = self._get_event_or_raise(event_id)
        self._get_ticket_available_or_raise(event, redeem_ticket_count)

        for _ in range(redeem_ticket_count):
            generated_code = self._generate_code()
            ticket = Ticket(
                event_id=input_dto.event_id,
                client_id=client_id,
                code=generated_code,
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
            self._send_email_to_client(client_id, ticket_list)
