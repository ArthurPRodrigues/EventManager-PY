class AppError(Exception):
    """Base class for application errors."""


class EmailByRoleAlreadyExistsError(AppError):
    def __init__(self, message: str = "User with this email and role already exists.") -> None:
        super().__init__(message)
