from __future__ import annotations

from dataclasses import dataclass

from user.domain.errors import (
    InvalidPasswordError,
    InvalidUserError,
)
from user.domain.user_role import UserRole
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


@dataclass(frozen=True)
class AuthenticateUserInputDto:
    email: str
    password: str
    role: UserRole

class AuthenticateUserUseCase:
    def __init__(self, users_repository: SqliteUsersRepository) -> None:
        self._users_repository = users_repository

    def execute(self, input_dto: AuthenticateUserInputDto):
        email = input_dto.email.strip().lower()
        user = self._users_repository.get_by_email_and_role(email, input_dto.role)
        if not user:
            raise InvalidUserError()
        elif user and not user.check_password(input_dto.password):
            raise InvalidPasswordError()
        return user
