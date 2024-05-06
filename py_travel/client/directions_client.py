from typing import Tuple, TYPE_CHECKING, List, Dict
from googlemaps.exceptions import ApiError as GoogleMapsApiError

from py_travel.client import Client
from py_travel.exceptions import LocationNotFoundError, ApiError, InvalidRequestError

if TYPE_CHECKING:  # pragma: no cover
    from datetime import datetime


class DirectionsClient(Client):
    """
    Google Maps Directions API client
    """

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
            response = self.client.directions(
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
