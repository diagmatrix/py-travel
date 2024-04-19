from .models import Client, Trip


def init_client(api_key: str) -> None:
    """
    Initializes the Google Maps API client

    :param api_key: The Google Maps API key
    :raises ValueError: If the API key is invalid
    """

    Client.set_client(api_key=api_key)


__all__ = ["init_client", "Trip"]
