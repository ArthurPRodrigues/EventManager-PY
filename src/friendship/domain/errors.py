from __future__ import annotations


class DomainError(Exception):
    """Base class for domain errors."""


class InvalidRequesterClientIdError(DomainError):
    def __init__(self, message: str = "Invalid requester client ID.") -> None:
        super().__init__(message)


class InvalidRequestedClientIdError(DomainError):
    def __init__(self, message: str = "Invalid requested client ID.") -> None:
        super().__init__(message)


class CannotFriendYourselfError(DomainError):
    def __init__(
        self, message: str = "Cannot send a friend request to yourself."
    ) -> None:
        super().__init__(message)


class FriendshipAlreadyAcceptedError(DomainError):
    def __init__(self, message: str = "Friendship request already accepted.") -> None:
        super().__init__(message)
