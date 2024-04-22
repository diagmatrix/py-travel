class ClientNotInitializedError(Exception):
    """Exception raised when the Google Maps API client has not been initialized

    Attributes:
        message: Explanation of the exception (optional)

    """

    def __init__(self, message: str = "Client not initialized") -> None:
        self.message = message
        super().__init__(self.message)
