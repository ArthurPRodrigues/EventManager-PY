class AppError(Exception):
    """Base class for application errors."""


class EmailByRoleAlreadyExistsError(AppError):
    def __init__(self, message: str = "User with this email and role already exists.") -> None:
        super().__init__(message)

class UserNotFoundError(AppError):
    def __init__(self, message: str = "Authentication failed, user was not found.") -> None:
        super().__init__(message)

class WrongPasswordError(AppError):
    def __init__(self, message: str = "Wrong password, try again.") -> None:
        super().__init__(message)