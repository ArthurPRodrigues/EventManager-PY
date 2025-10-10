from __future__ import annotations


class DomainError(Exception):
    """Base class for domain errors."""


class InvalidPageSizeError(DomainError):
    def __init__(self, size: int) -> None:
        message = f"Invalid page size: {size}."
        super().__init__(message)


class InvalidPageError(DomainError):
    def __init__(self, page: int) -> None:
        message = f"Invalid page number: {page}."
        super().__init__(message)
