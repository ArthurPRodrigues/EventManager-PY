from dataclasses import dataclass
from datetime import datetime

from friendship.domain.friendship_status import FriendshipStatus


@dataclass(frozen=True)
class FriendshipSummary:
    id: int
    requester_client_id: int
    requester_name: str
    requester_email: str
    requested_client_id: int
    requested_name: str
    requested_email: str
    status: FriendshipStatus
    accepted_at: datetime | None


@dataclass(frozen=True)
class PaginatedFriendshipsDto:
    friendship_summaries: list[FriendshipSummary]
    total_friendships_count: int
