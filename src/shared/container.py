from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from shared.infra.persistence.sqlite import SQLiteDatabase
from src.friendship.infra.persistence.sqlite_friendship_repository import (
    SqliteFriendshipRepository,
)


@dataclass
class Container:
    db: SQLiteDatabase


def build_container(db_path: Optional[str] = None) -> Container:
    db = SQLiteDatabase(path=db_path)
    db.initialize()

    friendship_repo = SqliteFriendshipRepository(db)

    return Container(db=db, friendship_repo=friendship_repo)
