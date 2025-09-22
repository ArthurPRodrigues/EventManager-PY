from __future__ import annotations


class DomainError(Exception):
    """Base class for domain errors."""


class InvalidNameError(DomainError):
    def __init__(self, message: str = "Invalid name.") -> None:
        super().__init__(message)

class InvalidEmailError(DomainError):
    def __init__(self, message: str = "Invalid email.") -> None:
        super().__init__(message)

class InvalidPasswordError(DomainError):
    def __init__(self, message: str = "Invalid password.") -> None:
        super().__init__(message)

class AuthenticationFailedError(DomainError):
    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(message)
