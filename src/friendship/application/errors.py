class AppError(Exception):
    """Base class for application errors."""


class RequesterNotFoundError(AppError):
    pass


class RequestedNotFoundError(AppError):
    pass


class FriendshipAlreadyExistsError(AppError):
    pass


class FriendshipNotFoundError(AppError):
    pass


class InvalidPageError(AppError):
    pass


class InvalidPageSizeError(AppError):
    pass
