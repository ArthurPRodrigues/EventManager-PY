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
