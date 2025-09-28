from __future__ import annotations

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
from shared.infra.persistence.sqlite import SQLiteDatabase
from ticket.application.validate_ticket_use_case import ValidateTicketUseCase
from ticket.infra.persistence.sqlite_tickets_repository import SqliteTicketsRepository
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
    event_repo: SqliteEventRepository


def build_application(db_path: str | None = None) -> CompositionRoot:
    db = SQLiteDatabase(path=db_path)
    db.initialize()

    # Repositories
    friendship_repo = SqliteFriendshipRepository(db)
    user_repo = SqliteUsersRepository(db)
    tickets_repo = SqliteTicketsRepository(db)
    event_repo = SqliteEventRepository(db)

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
    validate_ticket_use_case = ValidateTicketUseCase(tickets_repo)
    list_event_use_case = ListEventUseCase(event_repo)

    return CompositionRoot(
        db=db,
        send_friendship_invite_use_case=send_friendship_invite_use_case,
        accept_friendship_invite_use_case=accept_friendship_invite_use_case,
        delete_friendship_use_case=delete_friendship_use_case,
        list_friendships_use_case=list_friendships_use_case,
        create_user_use_case=create_user_use_case,
        authenticate_user_use_case=authenticate_user_use_case,
        validate_ticket_use_case=validate_ticket_use_case,
        list_event_use_case=list_event_use_case,
        event_repo=event_repo,
        friendship_repo=friendship_repo,
        user_repo=user_repo,
    )
