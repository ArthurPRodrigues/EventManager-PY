from __future__ import annotations

from dataclasses import replace
from datetime import datetime

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
    # NOTE WHAT A SHAME @fabifabufabo: Repository needs to return domain objects, not raw tuples.
    # Other approach is to create a output DTO (e.g. FriendshipWithUserEmailAndNameDto) in Application layer
    def list_with_user_email_and_name(
        self,
        page: int,
        size: int,
        requester_client_id: int | None = None,
        requested_client_id: int | None = None,
        participant_client_id: int | None = None,
        status: FriendshipStatus | None = None,
        accepted_at: datetime | None = None,
    ) -> tuple[list[tuple], int]:
        query = """
        SELECT
            f.id, f.status, f.accepted_at,
            f.requester_client_id, u1.name as requester_name, u1.email as requester_email,
            f.requested_client_id, u2.name as requested_name, u2.email as requested_email
        FROM friendships f
        JOIN users u1 ON f.requester_client_id = u1.id
        JOIN users u2 ON f.requested_client_id = u2.id
        WHERE 1=1
        """
        count_query = """
        SELECT COUNT(*)
        FROM friendships f
        JOIN users u1 ON f.requester_client_id = u1.id
        JOIN users u2 ON f.requested_client_id = u2.id
        WHERE 1=1
        """
        params: list = []
        count_params: list = []

        if participant_client_id is not None:
            query += " AND (f.requester_client_id = ? OR f.requested_client_id = ?)"
            count_query += (
                " AND (f.requester_client_id = ? OR f.requested_client_id = ?)"
            )
            params.extend([participant_client_id, participant_client_id])
            count_params.extend([participant_client_id, participant_client_id])
        else:
            if requester_client_id is not None:
                query += " AND f.requester_client_id = ?"
                count_query += " AND f.requester_client_id = ?"
                params.append(requester_client_id)
                count_params.append(requester_client_id)

            if requested_client_id is not None:
                query += " AND f.requested_client_id = ?"
                count_query += " AND f.requested_client_id = ?"
                params.append(requested_client_id)
                count_params.append(requested_client_id)

        if status is not None:
            query += " AND f.status = ?"
            count_query += " AND f.status = ?"
            params.append(status.value)
            count_params.append(status.value)

        if accepted_at is not None:
            query += " AND f.accepted_at = ?"
            count_query += " AND f.accepted_at = ?"
            params.append(accepted_at.isoformat())
            count_params.append(accepted_at.isoformat())

        query += " ORDER BY f.id ASC LIMIT ? OFFSET ?"
        params.extend([size, (page - 1) * size])

        with self._db.connect() as conn:
            rows = conn.execute(query, params).fetchall()
            total_count = conn.execute(count_query, count_params).fetchone()[0]

        converted_rows: list[tuple] = []
        for row in rows:
            (
                friendship_id,
                friendship_status,
                accepted_at_raw,
                requester_id,
                requester_name,
                requester_email,
                requested_id,
                requested_name,
                requested_email,
            ) = row

            parsed_accepted_at = None
            if accepted_at_raw:
                parsed_accepted_at = datetime.fromisoformat(
                    str(accepted_at_raw).replace("Z", "+00:00")
                )

            converted_rows.append((
                friendship_id,
                friendship_status,
                parsed_accepted_at,
                requester_id,
                requester_name,
                requester_email,
                requested_id,
                requested_name,
                requested_email,
            ))

        return converted_rows, total_count

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
