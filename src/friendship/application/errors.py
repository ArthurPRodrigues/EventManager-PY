class AppError(Exception):
    """Base class for application errors."""


class RequesterNotFoundError(AppError):
    def __init__(self, requester_email: str) -> None:
        message = f'Requester with client email "{requester_email}" does not exist.'
        super().__init__(message)


class RequestedNotFoundError(AppError):
    def __init__(self, requested_email: str) -> None:
        message = (
            f'Requested user with client email "{requested_email}" does not exist.'
        )
        super().__init__(message)


class FriendshipPendingError(AppError):
    def __init__(self, requester_email: str, requested_email: str) -> None:
        message = f'Friendship invitation between "{requested_email}" and "{requester_email}" is already pending.'
        super().__init__(message)


class FriendshipAlreadyExistsError(AppError):
    def __init__(self, requester_email: str, requested_email: str) -> None:
        message = f'Friendship between "{requester_email}" and "{requested_email}" already exists.'
        super().__init__(message)


class FriendshipNotFoundError(AppError):
    def __init__(self, friendship_id: int) -> None:
        message = f'Friendship with ID "{friendship_id}" does not exist.'
        super().__init__(message)
