from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from friendship.application.accept_friendship_invite_use_case import (
    AcceptFriendshipInviteUseCase,
)
from friendship.application.send_friendship_invite_use_case import (
    SendFriendshipInviteUseCase,
)
from friendship.infra.persistence.sqlite_friendship_repository import (
    SqliteFriendshipRepository,
)
from shared.infra.persistence.sqlite import SQLiteDatabase
from user.application.create_user_use_case import CreateUserUseCase
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


@dataclass
# todo: mudar nome da classe container para algo decente
class Container:
    db: SQLiteDatabase
    friendship_repo: SqliteFriendshipRepository
    send_friendship_invite_use_case: SendFriendshipInviteUseCase
    accept_friendship_invite_use_case: AcceptFriendshipInviteUseCase
    user_repo: SqliteUsersRepository
    create_user_use_case: CreateUserUseCase


def build_container(db_path: Optional[str] = None) -> Container:
    db = SQLiteDatabase(path=db_path)
    db.initialize()

    # Repositories
    friendship_repo = SqliteFriendshipRepository(db)
    user_repo = SqliteUsersRepository(db)

    # Use Cases
    send_friendship_invite_use_case = SendFriendshipInviteUseCase(
        friendship_repo, user_repo
    )
    accept_friendship_invite_use_case = AcceptFriendshipInviteUseCase(friendship_repo)
    create_user_use_case = CreateUserUseCase(user_repo)

    return Container(
        db=db,
        friendship_repo=friendship_repo,
        send_friendship_invite_use_case=send_friendship_invite_use_case,
        accept_friendship_invite_use_case=accept_friendship_invite_use_case,
        user_repo=user_repo,
        create_user_use_case=create_user_use_case,
    )
