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

    @staticmethod
    def update_date(date_name: str, message: str) -> None:
        """
        Warning raised when a date is automatically updated by a method
        :param date_name: Field date name
        :param message: Message to display
        """

        warn_message = f"UPDATED {date_name.upper()} DATE: {message}"
        warnings.warn(warn_message, UserWarning, stacklevel=3)


class ClientNotInitializedError(Exception):
    """Exception raised when the Google Maps API client has not been initialized

    Attributes:
        message: Explanation of the exception (optional)

    """

    def __init__(self, message: str = "Client not initialized") -> None:
        self.message = message
        super().__init__(self.message)


class InvalidResponseError(Exception):
    """Exception raised when the Google Maps API response does not contain the expected fields

    Attributes:
        field: Missing field
        message: Explanation of the exception (optional)
    """

    def __init__(self, field: str, message: str = "Invalid API response") -> None:
        self.field = field
        self.message = message
        super().__init__(self.message)
