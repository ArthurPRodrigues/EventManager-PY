from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from friendship.application.errors import InvalidPageError, InvalidPageSizeError
from friendship.domain.friendship_status import FriendshipStatus
from friendship.infra.persistence.sqlite_friendship_repository import (
    SqliteFriendshipRepository,
)


@dataclass(frozen=True)
class FriendshipView:
    id: int
    requester_client_id: int
    requester_email: str
    requester_name: str
    requested_client_id: int
    requested_email: str
    requested_name: str
    status: str
    accepted_at: Optional[datetime]


@dataclass(frozen=True)
class ListFriendshipsInputDto:
    page: int = 1
    size: int = 10
    requester_client_id: Optional[int] = None
    requested_client_id: Optional[int] = None
    status: Optional[str] = None
    accepted_at: Optional[datetime] = None


class ListFriendshipsWithUserEmailAndNameUseCase:
    def __init__(self, friendship_repository: SqliteFriendshipRepository) -> None:
        self._friendship_repository = friendship_repository

    def execute(
        self, input_dto: ListFriendshipsInputDto
    ) -> tuple[List[FriendshipView], int]:
        if input_dto.page < 1:
            raise InvalidPageError("Page must be greater than 0")
        if input_dto.size < 1:
            raise InvalidPageSizeError("Size must be greater than 0")

        status_enum: FriendshipStatus | None = None
        if input_dto.status:
            status_enum = FriendshipStatus(input_dto.status)

        rows, total = self._friendship_repository.list_with_user_email_and_name(
            page=input_dto.page,
            size=input_dto.size,
            requester_client_id=input_dto.requester_client_id,
            requested_client_id=input_dto.requested_client_id,
            status=status_enum,
            accepted_at=input_dto.accepted_at,
        )

        views: List[FriendshipView] = []
        for row in rows:
            (
                friendship_id,
                friendship_status,
                accepted_at,
                requester_client_id,
                requester_name,
                requester_email,
                requested_client_id,
                requested_name,
                requested_email,
            ) = row

            views.append(
                FriendshipView(
                    id=friendship_id,
                    requester_client_id=requester_client_id,
                    requester_email=requester_email,
                    requester_name=requester_name,
                    requested_client_id=requested_client_id,
                    requested_email=requested_email,
                    requested_name=requested_name,
                    status=friendship_status,
                    accepted_at=accepted_at,
                )
            )

        return views, total
