import warnings


class TripWarning:
    """
    Class wrapping all warnings raised by the Trip class
    """

    @staticmethod
    def ignore_field(field: str, message: str) -> None:
        """
        Warning raised when a field is ignored by a method

        :param field: Ignored field name
        :param message: Message to display
        """
        warn_message = f"IGNORED FIELD '{field}': {message}"
        warnings.warn(warn_message, UserWarning, stacklevel=3)


class ClientNotInitializedError(Exception):
    """Exception raised when the Google Maps API client has not been initialized

    Attributes:
        message: Explanation of the exception (optional)

    """

    def __init__(self, message: str = "Client not initialized") -> None:
        self.message = message
        super().__init__(self.message)
