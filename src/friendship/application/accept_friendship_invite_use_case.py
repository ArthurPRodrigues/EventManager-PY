from __future__ import annotations

from dataclasses import dataclass

from friendship.application.errors import FriendshipNotFoundError
from friendship.domain.friendship import Friendship
from friendship.infra.persistence.sqlite_friendship_repository import (
    SqliteFriendshipRepository,
)


@dataclass(frozen=True)
class AcceptFriendshipInviteInputDto:
    friendship_id: int


class AcceptFriendshipInviteUseCase:
    def __init__(self, friendship_repository: SqliteFriendshipRepository) -> None:
        self._friendship_repository = friendship_repository

    def execute(self, input_dto: AcceptFriendshipInviteInputDto) -> Friendship:
        friendship = self._friendship_repository.get_by_id(input_dto.friendship_id)
        if not friendship:
            raise FriendshipNotFoundError(input_dto.friendship_id)

        accepted_friendship = friendship.accept()
        self._friendship_repository.edit(accepted_friendship)
        return accepted_friendship
