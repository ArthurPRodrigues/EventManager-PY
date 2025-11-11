from __future__ import annotations

import os
from dataclasses import dataclass

from event.application.create_event_use_case import CreateEventUseCase
from event.application.delete_event_use_case import DeleteEventUseCase
from event.application.list_event_use_case import ListEventUseCase
from event.application.update_event_use_case import UpdateEventUseCase
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
from ticket.application.validate_ticket_use_case import ValidateTicketUseCase
from ticket.infra.persistence.sqlite_ticket_repository import (
    SqliteTicketsRepository,
)
from user.application.authenticate_user_use_case import AuthenticateUserUseCase
from user.application.create_user_use_case import CreateUserUseCase
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


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
    validate_ticket_use_case: ValidateTicketUseCase
    list_event_use_case: ListEventUseCase
    create_event_use_case: CreateEventUseCase
    delete_event_use_case: DeleteEventUseCase
    update_event_use_case: UpdateEventUseCase
    event_repo: SqliteEventRepository
    ticket_repo: SqliteTicketsRepository
    redeem_ticket_use_case: RedeemTicketUseCase
    html_template_engine: HtmlTemplateEngine
    smtp_email_service: SmtpEmailService


def build_application(db_path: str | None = None) -> CompositionRoot:
    db = SQLiteDatabase(path=db_path)
    db.initialize()

    # Services
    templates_dir = os.path.join("assets", "html_templates")
    html_template_engine = HtmlTemplateEngine(templates_dir)
    smtp_email_service = SmtpEmailService()

    # Repositories
    friendship_repo = SqliteFriendshipRepository(db)
    user_repo = SqliteUsersRepository(db)
    event_repo = SqliteEventRepository(db)
    ticket_repo = SqliteTicketsRepository(db)

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
    validate_ticket_use_case = ValidateTicketUseCase(ticket_repo, event_repo)
    create_event_use_case = CreateEventUseCase(event_repo, user_repo)
    delete_event_use_case = DeleteEventUseCase(event_repo, user_repo)
    update_event_use_case = UpdateEventUseCase(event_repo, user_repo)
    list_event_use_case = ListEventUseCase(event_repo)

    redeem_ticket_use_case = RedeemTicketUseCase(
        tickets_repository=ticket_repo,
        events_repository=event_repo,
        users_repository=user_repo,
        email_service=smtp_email_service,
        template_engine=html_template_engine,
    )

    return CompositionRoot(
        db=db,
        friendship_repo=friendship_repo,
        send_friendship_invite_use_case=send_friendship_invite_use_case,
        accept_friendship_invite_use_case=accept_friendship_invite_use_case,
        delete_friendship_use_case=delete_friendship_use_case,
        list_friendships_use_case=list_friendships_use_case,
        user_repo=user_repo,
        create_user_use_case=create_user_use_case,
        authenticate_user_use_case=authenticate_user_use_case,
        create_event_use_case=create_event_use_case,
        delete_event_use_case=delete_event_use_case,
        update_event_use_case=update_event_use_case,
        validate_ticket_use_case=validate_ticket_use_case,
        list_event_use_case=list_event_use_case,
        event_repo=event_repo,
        ticket_repo=ticket_repo,
        redeem_ticket_use_case=redeem_ticket_use_case,
        html_template_engine=html_template_engine,
        smtp_email_service=smtp_email_service,
    )
