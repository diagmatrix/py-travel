import googlemaps
from datetime import datetime
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Location:
    """
    Represents a location in the globe

    Attributes:
        lat: Latitude of the location (optional)
        lng: Longitude of the location (optional)
        address: Address of the location with that coordinates (optional)
    """

    lat: float | None = None
    lng: float | None = None
    address: str | None = None

    @classmethod
    def from_coords_or_str(cls, arg: Tuple[float, float] | str) -> "Location":
        if isinstance(arg, str):
            return Location(address=arg)
        if isinstance(arg, tuple):
            return Location(lat=arg[0], lng=arg[1])
        else:
            raise TypeError(
                "Argument must be a string or a tuple containing two floats"
            )


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


class Trip(Client):
    """
    Trip class

    Attributes:
        origin: Origin of the trip
        destination: Destination of the trip
        start_date: Start date of the trip
        end_date: End date of the trip
    """

    def __init__(
        self,
        origin: Tuple[float, float] | str | Location,
        destination: Tuple[float, float] | str | Location,
        start_date: datetime,
        end_date: datetime,
    ) -> None:
        """
        Initialize Trip object

        :param origin: Origin of the trip in pair (latitude, longitude) or address or Location object
        :param destination: Destination of the trip in pair (latitude, longitude) or address or Location object
        :param start_date: Start date of the trip
        :param end_date: End date of the trip
        """

        if isinstance(origin, Location):
            self.origin = origin
        else:
            self.origin = Location.from_coords_or_str(origin)

        if isinstance(destination, Location):
            self.destination = destination
        else:
            self.destination = Location.from_coords_or_str(destination)

        self.start_date = start_date
        self.end_date = end_date

    def add_stops(self, stops: List[Tuple[Tuple[float, float] | str | Location, datetime]]) -> None:
        """
        Add stops to the trip

        :param stops: A list of tuples containing the stop location (either a tuple containing the coordinates, the
            address or a Location object) and the departure date from the stop
        """

