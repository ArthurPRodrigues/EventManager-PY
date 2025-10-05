from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from friendship.application.dtos import (
    PaginatedFriendshipsDto,
)
from friendship.domain.friendship_status import FriendshipStatus
from friendship.infra.persistence.sqlite_friendship_repository import (
    SqliteFriendshipRepository,
)


@dataclass(frozen=True)
class ListFriendshipsInputDto:
    page: int = 1
    size: int = 10
    requester_client_id: int | None = None
    requested_client_id: int | None = None
    participant_client_id: int | None = (
        None  # participant_client_id can be either requester or requested
    )
    status: FriendshipStatus | None = None
    accepted_at: datetime | None = None


class ListFriendshipsWithUserEmailAndNameUseCase:
    def __init__(self, friendship_repository: SqliteFriendshipRepository) -> None:
        self._friendship_repository = friendship_repository

    def execute(self, input_dto: ListFriendshipsInputDto) -> PaginatedFriendshipsDto:
        paginated_friendships = (
            self._friendship_repository.list_with_user_email_and_name(
                page=input_dto.page,
                size=input_dto.size,
                requester_client_id=input_dto.requester_client_id,
                requested_client_id=input_dto.requested_client_id,
                participant_client_id=input_dto.participant_client_id,
                status=input_dto.status,
                accepted_at=input_dto.accepted_at,
            )
        )

        return paginated_friendships
