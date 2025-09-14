from __future__ import annotations

from dataclasses import dataclass

from user.application.errors import EmailByRoleAlreadyExistsError
from user.domain.user import User
from user.domain.user_role import UserRole
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


@dataclass(frozen=True)
class CreateUserInputDto:
    name: str
    email: str
    password: str
    role: UserRole


# todo: adicionar constraints de registro de usuário
class CreateUserUseCase:
    def __init__(self, users_repository: SqliteUsersRepository) -> None:
        self._users_repository = users_repository

    def execute(self, input_dto: CreateUserInputDto) -> User:
        email_norm = input_dto.email.strip().lower()
        if self._users_repository.get_by_email_and_role(email_norm, input_dto.role):
            raise EmailByRoleAlreadyExistsError()
        user = User.register(
            name=input_dto.name,
            email=input_dto.email,
            password=input_dto.password,
            role=input_dto.role,
        )
        added_user = self._users_repository.add(user)
        return added_user
