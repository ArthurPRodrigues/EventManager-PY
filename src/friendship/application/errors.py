class AppError(Exception):
    """Base class for application errors."""


class RequesterNotFoundError(AppError):
    pass


class RequestedNotFoundError(AppError):
    pass


class FriendshipAlreadyExistsError(AppError):
    pass
