from __future__ import annotations

from dataclasses import dataclass

from friendship.application.errors import (
    FriendshipAlreadyExistsError,
    RequestedNotFoundError,
    RequesterNotFoundError,
)
from friendship.domain.friendship import Friendship
from friendship.infra.persistence.sqlite_friendship_repository import (
    SqliteFriendshipRepository,
)


@dataclass(frozen=True)
class SendFriendshipInviteInputDto:
    requester_client_email: str
    requested_client_email: str


# TODO: Implement user repository and inject it
class SendFriendshipInviteUseCase:
    def __init__(
        self, friendship_repository: SqliteFriendshipRepository, user_repository
    ) -> None:
        self._friendship_repository = friendship_repository
        self._user_repository = user_repository

    def execute(self, input_dto: SendFriendshipInviteInputDto) -> Friendship:
        requester = self._user_repository.get_by_email(input_dto.requester_client_email)
        if not requester:
            raise RequesterNotFoundError(
                f"Requester with client_email {input_dto.requester_client_email} does not exist."
            )

        requested = self._user_repository.get_by_email(input_dto.requested_client_email)
        if not requested:
            raise RequestedNotFoundError(
                f"Requested user with client_email {input_dto.requested_client_email} does not exist."
            )

        if self._friendship_repository.friendship_exists(requester.id, requested.id):
            raise FriendshipAlreadyExistsError(
                f"Friendship between {input_dto.requester_client_email} and {input_dto.requested_client_email} already exists."
            )

        friendship = Friendship.create(requester.id, requested.id)
        self._friendship_repository.add(friendship)
        return friendship
