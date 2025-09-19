from __future__ import annotations

from dataclasses import dataclass

from user.domain.user_role import UserRole


@dataclass(frozen=True)
class AuthContext:
    id: int
    name: str
    email: str
    role: UserRole
