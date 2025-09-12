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


# TODO: Implement user repository
def mock_user_repository():
    class MockUserRepository:
        def __init__(self):
            self._users = {
                "1": {"id": 1, "name": "Alice"},
                "2": {"id": 2, "name": "Bob"},
            }

        def get_user(self, user_id: str):
            return self._users.get(user_id)

    return MockUserRepository()


def build_container(db_path: Optional[str] = None) -> Container:
    db = SQLiteDatabase(path=db_path)
    db.initialize()

    friendship_repo = SqliteFriendshipRepository(db)
    user_repo = mock_user_repository()
    send_friendship_invite_use_case = SendFriendshipInviteUseCase(
        friendship_repo, user_repo
    )
    accept_friendship_invite_use_case = AcceptFriendshipInviteUseCase(friendship_repo)

    return Container(
        db=db,
        friendship_repo=friendship_repo,
        send_friendship_invite_use_case=send_friendship_invite_use_case,
        accept_friendship_invite_use_case=accept_friendship_invite_use_case,
    )
