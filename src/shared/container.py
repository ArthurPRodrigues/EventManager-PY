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


@dataclass
class Container:
    db: SQLiteDatabase
    friendship_repo: SqliteFriendshipRepository
    send_friendship_invite_use_case: SendFriendshipInviteUseCase
    accept_friendship_invite_use_case: AcceptFriendshipInviteUseCase


def build_container(db_path: Optional[str] = None) -> Container:
    db = SQLiteDatabase(path=db_path)
    db.initialize()

    friendship_repo = SqliteFriendshipRepository(db)
    send_friendship_invite_use_case = SendFriendshipInviteUseCase(friendship_repo)
    accept_friendship_invite_use_case = AcceptFriendshipInviteUseCase(friendship_repo)

    return Container(
        db=db,
        friendship_repo=friendship_repo,
        send_friendship_invite_use_case=send_friendship_invite_use_case,
        accept_friendship_invite_use_case=accept_friendship_invite_use_case,
    )
