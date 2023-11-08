from emistream.models.data import Event


class StreamError(Exception):
    """Base class for all exceptions related to stream management."""

    pass


class RecorderError(StreamError):
    """Raised when a recorder service error occurs."""

    def __init__(self) -> None:
        super().__init__("Recorder service error.")


class StreamBusyError(StreamError):
    """Raised when a stream is busy."""

    def __init__(self, event: Event) -> None:
        self._event = event
        super().__init__("Stream is busy.")

    @property
    def event(self) -> Event:
        return self._event