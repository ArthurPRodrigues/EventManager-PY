from __future__ import annotations

from dataclasses import dataclass

from user.application.errors import UserNotFoundError, WrongPasswordError
from user.domain.user import User
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

    def execute(self, input_dto: AuthenticateUserInputDto) -> User:
        email, role, password = input_dto.email, input_dto.role, input_dto.password
        user = self._users_repository.get_by_email_and_role(email, role)
        if not user:
            raise UserNotFoundError()
        elif user and not user.check_password(password):
            raise WrongPasswordError()
        return user
