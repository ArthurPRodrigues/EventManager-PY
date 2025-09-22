from __future__ import annotations

from dataclasses import dataclass

from friendship.application.errors import (
    FriendshipAlreadyExistsError,
    FriendshipPendingError,
    RequestedNotFoundError,
    RequesterNotFoundError,
)
from friendship.domain.friendship import Friendship
from friendship.infra.persistence.sqlite_friendship_repository import (
    SqliteFriendshipRepository,
)
from user.domain.user_role import UserRole
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


@dataclass(frozen=True)
class SendFriendshipInviteInputDto:
    requester_client_email: str
    requested_client_email: str


class SendFriendshipInviteUseCase:
    def __init__(
        self,
        friendship_repository: SqliteFriendshipRepository,
        user_repository: SqliteUsersRepository,
    ) -> None:
        self._friendship_repository = friendship_repository
        self._user_repository = user_repository

    def execute(self, input_dto: SendFriendshipInviteInputDto) -> Friendship:
        requester_email, requested_email = (
            input_dto.requester_client_email,
            input_dto.requested_client_email,
        )

        requester = self._user_repository.get_by_email_and_role(
            requester_email, UserRole.CLIENT
        )
        if not requester:
            raise RequesterNotFoundError(requester_email)

        requested = self._user_repository.get_by_email_and_role(
            requested_email, UserRole.CLIENT
        )
        if not requested:
            raise RequestedNotFoundError(requested_email)

        if self._friendship_repository.friendship_exists(requester.id, requested.id):
            if self._friendship_repository.friendship_is_pending(
                requested.id, requester.id
            ):
                raise FriendshipPendingError(requester_email, requested_email)

            raise FriendshipAlreadyExistsError(requester_email, requested_email)

        friendship = Friendship.create(requester.id, requested.id)
        added_friendship = self._friendship_repository.add(friendship)
        return added_friendship
