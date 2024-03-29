class ServiceError(Exception):
    """Base class for service errors."""

    def __init__(self, message: str | None = None) -> None:
        self._message = message

        args = (message,) if message else ()
        super().__init__(*args)

    @property
    def message(self) -> str | None:
        return self._message


class InstanceNotFoundError(ServiceError):
    """Raised when no near instances of an event are found."""

    pass


class StreamBusyError(ServiceError):
    """Raised when a stream is busy."""

    pass


class RecorderBusyError(ServiceError):
    """Raised when a recorder is busy."""

    pass
