"""
Location class.

Classes:
    Location: Represents a location in the globe.

Functions:
    input_to_location: Transforms a coordinates tuple or an address into a Location object.
"""

from typing import Tuple, Any, Dict

from py_travel.exceptions import MissingArgumentError, ClientNotInitializedError


class Location:
    """
    Represents a location in the globe

    Attributes:
        client: Client object for the Google Maps API calls
        coords: Coordinates of the location (optional if address is provided)
        address: Address of the location with that coordinates (optional if lat and lng are provided)
        geocode_api_response: Raw Google Maps Geocode API response
        rev_geocode_api_response: Raw Google Maps Geocode API reverse geocoding response
    """

    client: Any = None

    def __init__(self, coordinates: Tuple[float, float] = None, address: str = None) -> None:
        """
        Initialize Location object.

        Either coordinates or address must be provided.

        :param coordinates: Coordinates of the location
        :param address: Address of the location
        """

        if not coordinates and not address:
            raise MissingArgumentError("coordinates/address","Either coordinates or address is required")

        self.__coords = coordinates if coordinates else None
        self.__address = address

        self.__geocode_api_response = {}
        self.__rev_geocode_api_response = {}

    @property
    def coords(self) -> Tuple[float, float] | None:
        """
        :return: Coordinates of the location
        """
        return self.__coords

    @property
    def address(self) -> str | None:
        """
        :return: Address of the location
        """
        return self.__address

    @classmethod
    def set_client(cls, client: Any) -> None:
        """
        Initializes the client for the geocoding and reverse geocoding requests

        :param client: A client object. Must contain a method called 'geocode' that returns the raw Google Maps
            Geocode API response and takes the following parameters: address and bounds. It must also
            contain a method called 'reverse_geocode' that returns the raw Google Maps Geocode response and takes the
            following parameters: latLng, result_type, location_type and language.
        """

        cls.client = client

    def coords_or_address(self) -> Tuple[float, float] | str:
        """
        Yields the coordinates of the location if they are defined, otherwise returns the address of the Location

        :return: The coordinates if they are present, otherwise the address
        """
        return self.coords if self.coords else self.address

    def geocode(self, bounds: Dict = None, force: bool = False) -> Dict:
        """
        Calls the Google Maps API to geocode the location.

        This method will call the Google Maps API only the first time the method is called in the lifespan of the
        instance or if 'force' is set to 'True' (or if the geocode_api_response is emptied).

        The parameter bounds expects a dictionary like this:
        sydney_bounds = {
            "northeast": {"lat": -33.4245981, "lng": 151.3426361},
            "southwest": {"lat" : -34.1692489, "lng" : 150.502229}
        }

        :param bounds: A dictionary containing the bounds of the location requested.
        :param force: Whether to force a new call to the Google Maps API
        :return: The raw API response
        """

        if not force and self.__geocode_api_response:
            return self.__geocode_api_response

        if not self.client:
            raise ClientNotInitializedError()

        if not self.__address:
            raise AttributeError("Missing address")

        self.__geocode_api_response = self.client.geocode(address=self.__address, bounds=bounds)[0]
        return self.__geocode_api_response


def input_to_location(data: Tuple[float, float] | str | Location) -> Location:
    """
    Converts a given 'Location' into a location object

    :param data: Tuple with (latitude, longitude), string address or Location object
    :return: A Location object from the given data
    """
    if isinstance(data, Location):
        return data
    if isinstance(data, str):
        return Location(address=data)
    if isinstance(data, tuple):
        return Location(coordinates=data)
    else:
        raise TypeError("Argument must be a string or a tuple containing two floats")
