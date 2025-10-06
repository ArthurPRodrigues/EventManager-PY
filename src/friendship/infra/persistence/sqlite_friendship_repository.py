from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from friendship.application.dtos import (
    FriendshipSummary,
    PaginatedFriendshipsDto,
)
from friendship.domain.friendship import Friendship
from friendship.domain.friendship_status import FriendshipStatus
from shared.infra.persistence.sqlite import SQLiteDatabase


class SqliteFriendshipRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self._db = db

    def add(self, friendship: Friendship) -> Friendship:
        with self._db.connect() as conn:
            cursor = conn.execute(
                "INSERT INTO friendships (requester_client_id, requested_client_id, status, accepted_at) VALUES (?, ?, ?, ?)",
                (
                    friendship.requester_client_id,
                    friendship.requested_client_id,
                    friendship.status.value,
                    friendship.accepted_at,
                ),
            )
            conn.commit()
            return replace(friendship, id=cursor.lastrowid)

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

    # NOTE (Clean Architecture VIOLATION): JOIN com users para evitar N+1
    def list_with_user_email_and_name(
        self,
        page: int,
        size: int,
        requester_client_id: int | None = None,
        requested_client_id: int | None = None,
        participant_client_id: int | None = None,
        status: FriendshipStatus | None = None,
        accepted_at: datetime | None = None,
    ) -> PaginatedFriendshipsDto:
        select_columns = """
        SELECT
            f.id, f.status, f.accepted_at,
            f.requester_client_id, u1.name as requester_name, u1.email as requester_email,
            f.requested_client_id, u2.name as requested_name, u2.email as requested_email
        """
        base_query = """
        FROM friendships f
        JOIN users u1 ON f.requester_client_id = u1.id
        JOIN users u2 ON f.requested_client_id = u2.id
        """
        conditions = ["1=1"]
        params = []

        if participant_client_id is not None:
            conditions.append(
                "(f.requester_client_id = ? OR f.requested_client_id = ?)"
            )
            params.extend([participant_client_id, participant_client_id])
        else:
            filters = {
                "f.requester_client_id": requester_client_id,
                "f.requested_client_id": requested_client_id,
            }

            for column, value in filters.items():
                if value is not None:
                    conditions.append(f"{column} = ?")
                    params.append(value)

        if status is not None:
            conditions.append("f.status = ?")
            params.append(status.value)

        if accepted_at is not None:
            conditions.append("f.accepted_at = ?")
            params.append(accepted_at)

        where_clause = " WHERE " + " AND ".join(conditions)

        count_query = "SELECT COUNT(*) " + base_query + where_clause
        select_query = (
            select_columns
            + base_query
            + where_clause
            + " ORDER BY f.id ASC LIMIT ? OFFSET ?"
        )

        count_params = params.copy()
        params.extend([size, (page - 1) * size])

        with self._db.connect() as conn:
            rows = conn.execute(select_query, params).fetchall()
            total_count = conn.execute(count_query, count_params).fetchone()[0]

        converted_rows: list[FriendshipSummary] = []
        for row in rows:
            friendship_id, friendship_status, accepted_at_raw, *user_data = row

            (
                requester_id,
                requester_name,
                requester_email,
                requested_id,
                requested_name,
                requested_email,
            ) = user_data

            parsed_accepted_at = None
            if accepted_at_raw:
                parsed_accepted_at = datetime.fromisoformat(
                    str(accepted_at_raw).replace("Z", "+00:00")
                )

            parsed_status = FriendshipStatus(friendship_status)

            converted_rows.append(
                FriendshipSummary(
                    id=friendship_id,
                    requester_client_id=requester_id,
                    requester_name=requester_name,
                    requester_email=requester_email,
                    requested_client_id=requested_id,
                    requested_name=requested_name,
                    requested_email=requested_email,
                    status=parsed_status,
                    accepted_at=parsed_accepted_at,
                )
            )

        return PaginatedFriendshipsDto(
            friendship_summaries=converted_rows,
            total_friendships_count=total_count,
        )

    def friendship_exists(
        self, requester_client_id: int, requested_client_id: int
    ) -> bool:
        with self._db.connect() as conn:
            cursor = conn.execute(
                """
                SELECT 1
                FROM friendships
                WHERE (requester_client_id = ? AND requested_client_id = ?)
                   OR (requester_client_id = ? AND requested_client_id = ?)
                """,
                (
                    requester_client_id,
                    requested_client_id,
                    requested_client_id,
                    requester_client_id,
                ),
            )
            return cursor.fetchone() is not None

    def is_friendship_pending(
        self, requester_client_id: int, requested_client_id: int
    ) -> bool:
        with self._db.connect() as conn:
            cursor = conn.execute(
                """
                SELECT 1
                FROM friendships
                WHERE ((requester_client_id = ? AND requested_client_id = ?)
                   OR (requester_client_id = ? AND requested_client_id = ?))
                  AND status = ?
                """,
                (
                    requester_client_id,
                    requested_client_id,
                    requested_client_id,
                    requester_client_id,
                    FriendshipStatus.PENDING.value,
                ),
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
