import googlemaps
from datetime import datetime
from dataclasses import dataclass
from typing import Tuple, List, NamedTuple


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


Stop = NamedTuple("Stop", location=Location, departure_date=datetime)  # Represents a stop in the trip


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
        stops: List of stops associated with the trip
    """

    @staticmethod
    def __input_to_location(data: Tuple[float, float] | str | Location) -> Location:
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
            return Location(lat=data[0], lng=data[1])
        else:
            raise TypeError(
                "Argument must be a string or a tuple containing two floats"
            )

    def __init__(
        self,
        origin: Tuple[float, float] | str | Location,
        destination: Tuple[float, float] | str | Location,
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> None:
        """
        Initialize Trip object

        :param origin: Origin of the trip in pair (latitude, longitude) or address or Location object
        :param destination: Destination of the trip in pair (latitude, longitude) or address or Location object
        :param start_date: Start date of the trip (optional)
        :param end_date: End date of the trip (optional)
        """

        self.origin = self.__input_to_location(origin)
        self.destination = self.__input_to_location(destination)

        self.start_date = start_date
        self.end_date = end_date

        self.stops: List[Stop] = []

    def add_stops(self, stops: List[Tuple[Tuple[float, float] | str | Location, datetime]]) -> None:
        """
        Add stops to the trip

        :param stops: A list of tuples containing the stop location (either a tuple containing the coordinates, the
            address or a Location object) and the departure date from the stop
        """

        self.stops.extend([Stop(self.__input_to_location(loc), dep_date) for loc, dep_date in stops])
        self.stops.sort(key=lambda stop: stop.departure_date)
