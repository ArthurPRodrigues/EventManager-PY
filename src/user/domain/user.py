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
    id: int | None
    name: str
    email: str
    hashed_password: str
    role: UserRole

    @staticmethod
    def register(name: str, email: str, hashed_password: str, role: UserRole) -> "User":
        if not name or not name.strip():
            raise InvalidNameError()
        if not email or not email.strip():
            raise InvalidEmailError()
        if not hashed_password or not hashed_password.strip():
            raise InvalidPasswordError()
        return User(name=name, email=email, hashed_password=hashed_password, role=role)

    def check_password(self, password: str) -> bool:
        if not password:
            return False
        return self.password_hash == _hash_password(password)
