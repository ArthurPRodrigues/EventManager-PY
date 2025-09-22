from __future__ import annotations


class DomainError(Exception):
    """Base class for domain errors."""


class InvalidNameError(DomainError):
    def __init__(self, user_name) -> None:
        message = f'Invalid name: "{user_name}".'
        super().__init__(message)


class InvalidEmailError(DomainError):
    def __init__(self, user_email) -> None:
        message = f'Invalid email: "{user_email}".'
        super().__init__(message)


class InvalidPasswordError(DomainError):
    def __init__(self, user_password) -> None:
        message = f'Invalid password: "{user_password}".'
        super().__init__(message)
