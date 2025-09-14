from dataclasses import dataclass
from hashlib import sha256

from user.domain.errors import (
    InvalidEmailError,
    InvalidNameError,
    InvalidPasswordError,
)
from user.domain.user_role import UserRole


def _hash_password(raw: str) -> str:
    return sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class User:
    name: str
    email: str
    hashed_password: str
    role: UserRole
    id: int | None = None

    @staticmethod
    def register(name: str, email: str, password: str, role: UserRole) -> "User":
        if not name or not name.strip():
            raise InvalidNameError()
        if not email or not email.strip():
            raise InvalidEmailError()
        if not password or not password.strip():
            raise InvalidPasswordError()
        return User(
            name=name, email=email, hashed_password=_hash_password(password), role=role
        )

    def check_password(self, password: str) -> bool:
        if not password:
            return False
        return self.hashed_password == _hash_password(password)
