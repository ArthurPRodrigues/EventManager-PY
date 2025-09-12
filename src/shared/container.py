from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from shared.infra.persistence.sqlite import SQLiteDatabase
from src.friendship.application.send_friendship_invite_use_case import SendInviteUseCase
from src.friendship.infra.persistence.sqlite_friendship_repository import (
    SqliteFriendshipRepository,
)


@dataclass
class Container:
    db: SQLiteDatabase
    friendship_repo: SqliteFriendshipRepository
    send_invite_use_case: SendInviteUseCase


def build_container(db_path: Optional[str] = None) -> Container:
    db = SQLiteDatabase(path=db_path)
    db.initialize()

    friendship_repo = SqliteFriendshipRepository(db)
    send_invite_use_case = SendInviteUseCase(friendship_repo)

    return Container(
        db=db,
        friendship_repo=friendship_repo,
        send_invite_use_case=send_invite_use_case,
    )
