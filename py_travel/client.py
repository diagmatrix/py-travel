import googlemaps

from py_travel.exceptions import ApiError, LocationNotFoundError


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

    @classmethod
    def directions(cls, **kwargs) -> dict:
        """
        Wrapper around Google Maps API to get directions

        :param kwargs: googlemaps.Client directions endpoint arguments
        :return: The response from the Google Maps API
        """

        try:
            response = cls.client.directions(**kwargs)
        except googlemaps.exceptions.ApiError as e:
            if e.status == "NOT_FOUND":
                raise LocationNotFoundError() from None
            else:
                raise ApiError(e.status, e.message) from None

        return response
