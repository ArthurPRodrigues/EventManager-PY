from __future__ import annotations

from dataclasses import dataclass

from event.application.dtos import PaginatedStaffsDto
from user.infra.persistence.sqlite_users_repository import SqliteUsersRepository


@dataclass(frozen=True)
class ListStaffsInputDto:
    page: int = 1
    size: int = 10
    name: str | None = None
    email: str | None = None
    event_id: str | None = None


class ListStaffWithEmailAndNameUseCase:
    def __init__(self, user_repository: SqliteUsersRepository) -> None:
        self._user_repository = user_repository

    def execute(self, input_dto: ListStaffsInputDto) -> PaginatedStaffsDto:
        paginated_staffs = self._user_repository.list_with_email_and_name(
            page=input_dto.page,
            size=input_dto.size,
            name=input_dto.name,
            email=input_dto.email,
            event_id=input_dto.event_id,
        )

        return paginated_staffs
