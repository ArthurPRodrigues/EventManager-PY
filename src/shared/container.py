from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from shared.infra.persistence.sqlite import SQLiteDatabase


@dataclass
class Container:
    db: SQLiteDatabase


def build_container(db_path: Optional[str] = None) -> Container:
    db = SQLiteDatabase(path=db_path)
    db.initialize()

    return Container(
        db=db,
    )
