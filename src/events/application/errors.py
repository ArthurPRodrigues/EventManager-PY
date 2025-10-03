class AppError(Exception):
    """Base class for application errors."""

class PastDateError(AppError):
    def __init__(
        self,
        date,
    ) -> None:
        message = (
            f"The date '{date}' is incorrect, it cannot be in the past."
        )
        super().__init__(message)
    
