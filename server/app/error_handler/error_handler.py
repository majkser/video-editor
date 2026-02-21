class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    """Raised when a requested resource is not found."""

    pass


class ValidationError(AppError):
    """Raised when input validation fails."""

    pass


class FfmpegError(AppError):
    """Raised when an error occurs during ffmpeg processing."""

    pass


class UnauthorizedError(AppError):
    """Raised when authentication fails."""

    pass


class AlreadyExistsError(AppError):
    """Raised when trying to create a resource that already exists."""

    pass
