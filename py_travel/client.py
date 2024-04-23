import googlemaps


class Client:
    """
    Google Maps Client for interacting with Google Maps API

    Attributes:
        client: Google Maps API client (class attribute)
    """

    client: googlemaps.Client

    @classmethod
    def set_client(cls, api_key: str) -> None:
        """
        Set Google Maps Client

        :param api_key: API key for Google Maps
        """
        cls.client = googlemaps.Client(key=api_key)
