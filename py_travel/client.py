from typing import Tuple, TYPE_CHECKING, List, Dict
from googlemaps.exceptions import ApiError as GoogleMapsApiError
from googlemaps.client import Client as GoogleMapsClient
from py_travel.exceptions import LocationNotFoundError, ApiError, InvalidRequestError

if TYPE_CHECKING:  # pragma: no cover
    from datetime import datetime


class Client:
    """
    Base Client Class for all Google Maps API clients

    Attributes:
        client: Google Maps API client (class attribute)
    """
    def __init__(self, api_key: str) -> None:
        self.__client = GoogleMapsClient(key=api_key)

    @property
    def client(self) -> GoogleMapsClient:
        return self.__client

    @client.setter
    def client(self, api_key: str) -> None:
        """
        Set Google Maps Client

        :param api_key: API key for Google Maps
        """
        self.client = GoogleMapsClient(key=api_key)

    def directions(
            self,
            origin: Tuple[float, float] | str,
            destination: Tuple[float, float] | str,
            departure_time: 'datetime' = None,
            arrival_time: 'datetime' = None,
            mode: str = None,
            avoid: str = None,
            units: str = None,
            transit_mode: List[str] | str = None,
            transit_routing_preference: str = None,
            traffic_model: str = None
    ) -> Dict:
        """
        Directions API method

        Information about the parameters can be found here:
        https://googlemaps.github.io/google-maps-services-python/docs/index.html#googlemaps.Client.directions

        :return: The Google Maps Directions API response
        """

        try:
            response = self.__client.directions(
                origin=origin,
                destination=destination,
                departure_time=departure_time,
                arrival_time=arrival_time,
                mode=mode,
                avoid=avoid,
                units=units,
                transit_mode=transit_mode,
                transit_routing_preference=transit_routing_preference,
                traffic_model=traffic_model
            )
        except GoogleMapsApiError as e:
            if e.status == "NOT_FOUND":
                raise LocationNotFoundError() from None
            elif e.status == "INVALID_REQUEST":
                raise InvalidRequestError(e.message) from None
            else:
                raise ApiError(e.status, e.message) from None

        return response

