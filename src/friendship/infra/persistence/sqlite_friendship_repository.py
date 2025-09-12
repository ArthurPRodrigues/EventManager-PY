from __future__ import annotations

from shared.infra.persistence.sqlite import SQLiteDatabase
from src.friendship.domain.friendship import Friendship


class SqliteFriendshipRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def add(self, friendship: Friendship) -> None:
        with self._db.connect() as conn:
            conn.execute(
                "INSERT INTO friendships (requester_client_id, requested_client_id, status) VALUES (?, ?, ?)",
                (
                    friendship.requester_client_id,
                    friendship.requested_client_id,
                    friendship.status.value,
                    friendship.accepted_at,
                ),
            )
            conn.commit()

    def friendship_exists(
        self, requester_client_id: int, requested_client_id: int
    ) -> bool:
        with self._db.connect() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM friendships WHERE requester_client_id = ? AND requested_client_id = ?",
                (requester_client_id, requested_client_id),
            )
            return cursor.fetchone() is not None

    def delete(self, friendship_id: int) -> None:
        with self._db.connect() as conn:
            conn.execute("DELETE FROM friendships WHERE id = ?", (friendship_id,))
            conn.commit()
