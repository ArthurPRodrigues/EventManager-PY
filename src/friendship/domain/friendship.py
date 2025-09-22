from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime

from .errors import (
    CannotFriendYourselfError,
    FriendshipAlreadyAcceptedError,
    InvalidRequestedClientIdError,
    InvalidRequesterClientIdError,
)
from .friendship_status import FriendshipStatus


@dataclass(frozen=True)
class Friendship:
    requester_client_id: int
    requested_client_id: int
    status: FriendshipStatus = FriendshipStatus.PENDING
    accepted_at: datetime | None = None
    id: int | None = None

    @staticmethod
    def create(requester_client_id: int, requested_client_id: int) -> Friendship:
        if not isinstance(requester_client_id, int) or requester_client_id <= 0:
            raise InvalidRequesterClientIdError(requester_client_id)
        if not isinstance(requested_client_id, int) or requested_client_id <= 0:
            raise InvalidRequestedClientIdError(requested_client_id)
        if requester_client_id == requested_client_id:
            raise CannotFriendYourselfError()
        return Friendship(
            requester_client_id=requester_client_id,
            requested_client_id=requested_client_id,
        )

    def accept(self) -> Friendship:
        if self.status == FriendshipStatus.ACCEPTED:
            raise FriendshipAlreadyAcceptedError()
        return replace(
            self,
            status=FriendshipStatus.ACCEPTED,
            accepted_at=datetime.now(UTC),
        )
