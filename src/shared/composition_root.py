from __future__ import annotations

import os
from dataclasses import dataclass

from event.application.list_event_use_case import ListEventUseCase
from event.infra.persistence.sqlite_event_repository import SqliteEventRepository
from friendship.application.accept_friendship_invite_use_case import (
    AcceptFriendshipInviteUseCase,
)
from friendship.application.delete_friendship_use_case import DeleteFriendshipUseCase
from friendship.application.list_friendships_with_user_email_and_name_use_case import (
    ListFriendshipsWithUserEmailAndNameUseCase,
)
from friendship.application.send_friendship_invite_use_case import (
    SendFriendshipInviteUseCase,
)
from friendship.infra.persistence.sqlite_friendship_repository import (
    SqliteFriendshipRepository,
)
from shared.infra.email.smtp_ticket_email_service import SmtpEmailService
from shared.infra.html_template.html_template_engine import HtmlTemplateEngine
from shared.infra.persistence.sqlite import SQLiteDatabase
from ticket.application.redeem_ticket_use_case import RedeemTicketUseCase
from ticket.application.validate_ticket_as_organizer_use_case import (
    ValidateTicketAsOrganizerUseCase,
)
from ticket.application.validate_ticket_as_staff_use_case import (
    ValidateTicketAsStaffUseCase,
)
from ticket.application.redeem_ticket_use_case import RedeemTicketUseCase
from ticket.infra.persistence.sqlite_tickets_repository import SqliteTicketsRepository
from ticket.application.redeem_ticket_use_case import RedeemTicketUseCase
from user.application.authenticate_user_use_case import AuthenticateUserUseCase
from user.application.create_user_use_case import CreateUserUseCase
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


# TODO: Uncomment html template engine and email service lines when ticket redemption is implemented
@dataclass
class CompositionRoot:
    db: SQLiteDatabase
    friendship_repo: SqliteFriendshipRepository
    send_friendship_invite_use_case: SendFriendshipInviteUseCase
    accept_friendship_invite_use_case: AcceptFriendshipInviteUseCase
    delete_friendship_use_case: DeleteFriendshipUseCase
    list_friendships_use_case: ListFriendshipsWithUserEmailAndNameUseCase
    user_repo: SqliteUsersRepository
    create_user_use_case: CreateUserUseCase
    authenticate_user_use_case: AuthenticateUserUseCase
    validate_ticket_as_organizer_use_case: ValidateTicketAsOrganizerUseCase
    validate_ticket_as_staff_use_case: ValidateTicketAsStaffUseCase
    redeem_ticket_use_case: RedeemTicketUseCase
    list_event_use_case: ListEventUseCase
    event_repo: SqliteEventRepository
    ticket_repo: SqliteTicketsRepository
    redeem_ticket_use_case: RedeemTicketUseCase
    html_template_engine: HtmlTemplateEngine | None = None
    smtp_email_service: SmtpEmailService | None = None


def build_application(db_path: str | None = None) -> CompositionRoot:
    db = SQLiteDatabase(path=db_path)
    db.initialize()

    # Services
    templates_dir = os.path.join("assets", "html_templates")
    html_template_engine: HtmlTemplateEngine | None = None
    smtp_email_service: SmtpEmailService | None = None
    try:
        html_template_engine = HtmlTemplateEngine(templates_dir)
    except Exception:
        html_template_engine = None
    try:
        smtp_email_service = SmtpEmailService()
    except Exception:
        smtp_email_service = None

    # Repositories
    friendship_repo = SqliteFriendshipRepository(db)
    user_repo = SqliteUsersRepository(db)
    event_repo = SqliteEventRepository(db)
    tickets_repo = SqliteTicketsRepository(db)
    ticket_repo = SqliteTicketRepository(db)

    # Use Cases
    send_friendship_invite_use_case = SendFriendshipInviteUseCase(
        friendship_repo, user_repo
    )
    accept_friendship_invite_use_case = AcceptFriendshipInviteUseCase(friendship_repo)
    delete_friendship_use_case = DeleteFriendshipUseCase(friendship_repo)
    list_friendships_use_case = ListFriendshipsWithUserEmailAndNameUseCase(
        friendship_repo
    )
    create_user_use_case = CreateUserUseCase(user_repo)
    authenticate_user_use_case = AuthenticateUserUseCase(user_repo)
    list_event_use_case = ListEventUseCase(event_repo)
    validate_ticket_as_organizer_use_case = ValidateTicketAsOrganizerUseCase(
        tickets_repository=tickets_repo,
        events_repository=event_repo,
    )
    validate_ticket_as_staff_use_case = ValidateTicketAsStaffUseCase(
        tickets_repository=tickets_repo,
        events_repository=event_repo,
    )

    redeem_ticket_use_case = RedeemTicketUseCase(
        tickets_repository=tickets_repo,
        events_repository=event_repo,
        users_repository=user_repo,
        email_service=smtp_email_service,
        template_engine=html_template_engine,
    )

    return CompositionRoot(
        db=db,
        friendship_repo=friendship_repo,
        friendship_repo=friendship_repo,
        send_friendship_invite_use_case=send_friendship_invite_use_case,
        accept_friendship_invite_use_case=accept_friendship_invite_use_case,
        delete_friendship_use_case=delete_friendship_use_case,
        list_friendships_use_case=list_friendships_use_case,
        user_repo=user_repo,
        user_repo=user_repo,
        create_user_use_case=create_user_use_case,
        authenticate_user_use_case=authenticate_user_use_case,
        validate_ticket_as_organizer_use_case=validate_ticket_as_organizer_use_case,
        validate_ticket_as_staff_use_case=validate_ticket_as_staff_use_case,
        event_repo=event_repo,
        list_event_use_case=list_event_use_case,
        ticket_repo=tickets_repo,
        redeem_ticket_use_case=redeem_ticket_use_case,
        html_template_engine=html_template_engine,
        smtp_email_service=smtp_email_service,
    )
