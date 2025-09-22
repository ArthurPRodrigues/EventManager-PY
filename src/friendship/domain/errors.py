from __future__ import annotations


class DomainError(Exception):
    """Base class for domain errors."""


class InvalidRequesterClientIdError(DomainError):
    def __init__(self, requester_client_id: int) -> None:
        message: str = f"Invalid requester client ID: {requester_client_id}."
        super().__init__(message)


class InvalidRequestedClientIdError(DomainError):
    def __init__(self, requested_client_id: int) -> None:
        message: str = f"Invalid requested client ID: {requested_client_id}."
        super().__init__(message)


class CannotFriendYourselfError(DomainError):
    def __init__(
        self, message: str = "Cannot send a friend request to yourself."
    ) -> None:
        super().__init__(message)


class FriendshipAlreadyAcceptedError(DomainError):
    def __init__(self, friendship_id: int) -> None:
        message: str = f"Friendship with ID {friendship_id} is already accepted."
        super().__init__(message)
