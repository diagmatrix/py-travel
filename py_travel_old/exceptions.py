class ClientNotInitializedError(Exception):
    """Exception raised when the googlemaps client has not been initialized

    Attributes:
        message: Explanation of the exception (optional)

    """

    def __init__(self, message: str = "Client not initialized") -> None:
        self.message = message
        super().__init__(self.message)


class MissingDataError(Exception):
    """Exception raised when a response from the Google Maps API is missing some piece of data

    Attributes:
        value: Missing field
        message: Explanation of the exception (optional)
    """

    def __init__(self, value: str, message: str = "Response missing field") -> None:
        self.message = message
        self.value = value
        super().__init__(f"{self.message}: {self.value}")
