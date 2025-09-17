from __future__ import annotations
from dataclasses import dataclass

from ..domain.errors import AuthenticationFailedError
from ..infra.persistence.sqlite_users_repository import SqliteUsersRepository

@dataclass(frozen=True)
class AuthenticateUserInputDto:
    email: str
    password: str

class AuthenticateUserUseCase:
    def __init__(self, users_repository: SqliteUsersRepository) -> None:
        self._users_repository = users_repository

    def execute(self, input_dto: AuthenticateUserInputDto):
        email = input_dto.email.strip().lower()
        user = self._users_repository.get_by_email(email)
        if not user or not user.check_password(input_dto.password):
            raise AuthenticationFailedError()
        return user