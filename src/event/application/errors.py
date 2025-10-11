from __future__ import annotations


# TODO: Chante to AppError like event/application/errors.py and friendship/application/errors.py
# @ArthurPRodrigues
class DomainError(Exception):
    """Base class for domain errors."""


# TODO: Remove unused errors
# @ArthurPRodrigues
class InvalidPageSizeError(DomainError):
    def __init__(self, size: int) -> None:
        message = f"Invalid page size: {size}."
        super().__init__(message)


class InvalidPageError(DomainError):
    def __init__(self, page: int) -> None:
        message = f"Invalid page number: {page}."
        super().__init__(message)
