from __future__ import annotations

from datetime import datetime

from friendship.domain.friendship import Friendship
from friendship.domain.friendship_status import FriendshipStatus
from shared.infra.persistence.sqlite import SQLiteDatabase


class SqliteFriendshipRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def add(self, friendship: Friendship) -> None:
        with self._db.connect() as conn:
            conn.execute(
                "INSERT INTO friendships (requester_client_id, requested_client_id, status, accepted_at) VALUES (?, ?, ?, ?)",
                (
                    friendship.requester_client_id,
                    friendship.requested_client_id,
                    friendship.status.value,
                    friendship.accepted_at,
                ),
            )
            conn.commit()

    def get_by_id(self, id: int) -> Friendship | None:
        with self._db.connect() as conn:
            row = conn.execute(
                """
                SELECT id, requester_client_id, requested_client_id, status, accepted_at
                FROM friendships
                WHERE id = ?
                """,
                (id,),
            ).fetchone()

        if not row:
            return None

        friendship_id, requester_client_id, requested_client_id, status, accepted_at = (
            row
        )

        parsed_accepted_at = None
        if accepted_at:
            parsed_accepted_at = datetime.fromisoformat(
                accepted_at.replace("Z", "+00:00")
            )

        return Friendship(
            id=friendship_id,
            requester_client_id=requester_client_id,
            requested_client_id=requested_client_id,
            status=FriendshipStatus(status),
            accepted_at=parsed_accepted_at,
        )

    def friendship_exists(
        self, requester_client_id: int, requested_client_id: int
    ) -> bool:
        with self._db.connect() as conn:
            cursor = conn.execute(
                """
                SELECT 1
                FROM friendships
                WHERE requester_client_id = ? AND requested_client_id = ?
                """,
                (requester_client_id, requested_client_id),
            )
            return cursor.fetchone() is not None

    def edit(self, friendship: Friendship) -> None:
        accepted_at_str = None
        if friendship.accepted_at:
            accepted_at_str = friendship.accepted_at.isoformat()

        with self._db.connect() as conn:
            conn.execute(
                """
                UPDATE friendships SET requester_client_id = ?, requested_client_id = ?, status = ?, accepted_at = ?
                WHERE id = ?
                """,
                (
                    friendship.requester_client_id,
                    friendship.requested_client_id,
                    friendship.status.value,
                    accepted_at_str,
                    friendship.id,
                ),
            )
            conn.commit()

    def delete(self, friendship_id: int) -> None:
        with self._db.connect() as conn:
            conn.execute("DELETE FROM friendships WHERE id = ?", (friendship_id,))
            conn.commit()
