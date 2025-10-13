from dataclasses import dataclass

from user.domain.user_role import UserRole


@dataclass(frozen=True)
class ValidateTicketInputDto:
    user_id: int
    user_role: UserRole
    code: str
