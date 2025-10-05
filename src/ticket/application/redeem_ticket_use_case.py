from dataclasses import dataclass
from datetime import datetime

from events.infra.persistence.sqlite_event_repository import SqliteEventRepository
from ticket.domain.ticket import Ticket
from ticket.domain.ticket_status import TicketStatus
from ticket.infra.persistence.sqlite_ticket_repository import SqliteTicketRepository
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


@dataclass(frozen=True)
class TicketInputDto:
    code: str
    user_id: int
    event_id: int


@dataclass(frozen=True)
class TicketView:
    id: int
    code: str
    created_at: str
    status: str
    event_id: int
    client_id: int


@dataclass(frozen=True)
class RedeemTicketResult:
    items: list[TicketView]
    total: int


class RedeemTicketUseCase:
    def __init__(
        self,
        ticket_repository: SqliteTicketRepository,
        event_repository: SqliteEventRepository,
        user_repository: SqliteUsersRepository,
    ) -> None:
        self._ticket_repository = ticket_repository
        self._event_repository = event_repository
        self._user_repository = user_repository

    def redeem(self, input_dto: TicketInputDto) -> RedeemTicketResult:
        user = self._user_repository.get_by_id(input_dto.user_id)
        if user is None:
            raise ValueError("User not found")

        event_row = self._event_repository.list_by_id(input_dto.event_id)
        if event_row is None:
            raise ValueError("Event not found")
        (
            event_id,
            _name,
            _location,
            _event_start_date,
            event_end_date,
            tickets_available,
            _organizer_id,
            _created_at,
        ) = event_row

        if tickets_available <= 0:
            raise ValueError("No tickets available for this event")

        now = datetime.now()
        if isinstance(event_end_date, str):
            try:
                parsed_end = datetime.fromisoformat(event_end_date.replace(" ", "T"))
            except Exception:
                parsed_end = now
        else:
            parsed_end = event_end_date

        if parsed_end < now:
            raise ValueError("Event already finished")

        redeemed_ticket = Ticket.create(
            code=input_dto.code,
            created_at=now,
            status=TicketStatus.PENDING,
            event_id=event_id,
            client_id=input_dto.user_id,
        )
        saved_ticket = self._ticket_repository.add(redeemed_ticket)

        self._event_repository.decrement_tickets_available(event_id)

        view = TicketView(
            id=saved_ticket.id or -1,
            code=saved_ticket.code,
            created_at=saved_ticket.created_at.isoformat(sep=" "),
            status=saved_ticket.status.value,
            event_id=saved_ticket.event_id,
            client_id=saved_ticket.client_id,
        )
        return RedeemTicketResult(items=[view], total=1)
