import googlemaps
from datetime import datetime
from dataclasses import dataclass
from typing import Tuple, List, NamedTuple, Dict, Literal, TypedDict

from .exceptions import ClientNotInitializedError, TripWarning


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

    @property
    def coords(self) -> Tuple[float, float] | None:
        """
        Returns the coordinates of the location if it has them

        :return: The latitude and longitude of the location as a tuple
        """
        if self.lat and self.lng:
            return (self.lat, self.lng)
        else:
            return None


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
        return Location(lat=data[0], lng=data[1])
    else:
        raise TypeError("Argument must be a string or a tuple containing two floats")


Stop = NamedTuple(
    "Stop", location=Location, departure_date=datetime
)  # Represents a stop in the trip


TRIP_MODES = Literal["driving", "walking", "bicycling", "transit"]
AVOID_FEATURES = Literal["tolls", "highways", "ferries", "indoor"]
TRANSIT_MODES = Literal["bus", "subway", "train", "tram", "rail"]
TRANSIT_PREFERENCES = Literal["less_walking", "fewer_transfers"]
TRAFFIC_MODE = Literal["best_guess", "optimistic", "pessimistic"]


class TripConfig(TypedDict, total=False):
    """
    Contains the trip configuration variables

    Attributes:
        mode: Trip mode: driving, walking, bicycling or transit.
        avoid: Features to avoid: tolls, highways, ferries, indoor or a combination of them
        units: Unit system for the calculations: metric or imperial.
        transit_mode: Transit mode if the mode is 'transit': bus, subway, train, tram, rail or a combination of them.
        transit_routing_preference: Preference in calculations for transit: less_walking or fewer_transfer.
        traffic_model: Traffic model to use if mode is 'driving': best_guess, optimistic or pessimistic.
    """

    mode: TRIP_MODES
    avoid: List[AVOID_FEATURES] | AVOID_FEATURES
    units: Literal["metric", "imperial"]
    transit_mode: List[TRANSIT_MODES] | TRANSIT_MODES
    transit_routing_preference: TRANSIT_PREFERENCES
    traffic_model: TRAFFIC_MODE


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
        updated: Boolean indicating if the object needs to call the Google Maps API to get the results
        raw_result: Raw Google Maps API response
    """

    def __init__(
        self,
        origin: Tuple[float, float] | str | Location,
        destination: Tuple[float, float] | str | Location,
        stops: List[Tuple[Tuple[float, float] | str | Location, datetime]] = None,
        start_date: datetime = None,
        end_date: datetime = None,
        config: TripConfig = None,
    ) -> None:
        """
        Initialize Trip object

        :param origin: Origin of the trip in pair (latitude, longitude) or address or Location object
        :param destination: Destination of the trip in pair (latitude, longitude) or address or Location object
        :param stops: A list of tuples containing the stop location (either a tuple containing the coordinates, the
            address or a Location object) and the departure date from the stop
        :param start_date: Start date of the trip (optional)
        :param end_date: End date of the trip (optional)
        :param config: Trip configuration either as a dictionary or as a TripConfig object (optional)
        """

        self.origin = input_to_location(origin)
        self.destination = input_to_location(destination)
        self.stops = (
            [Stop(input_to_location(loc), dep_date) for loc, dep_date in stops]
            if stops
            else []
        )

        self.start_date = start_date
        self.end_date = end_date

        self.config = config

        self.raw_result: Dict = {}
        self.updated = True

    def add_stops(
        self, stops: List[Tuple[Tuple[float, float] | str | Location, datetime]]
    ) -> None:
        """
        Add stops to the trip

        Warning: This method will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param stops: A list of tuples containing the stop location (either a tuple containing the coordinates, the
            address or a Location object) and the departure date from the stop
        """

        self.stops.extend(
            [Stop(input_to_location(loc), dep_date) for loc, dep_date in stops]
        )
        self.stops.sort(key=lambda stop: stop.departure_date)
        self.updated = True

    def set_config(self, config: TripConfig) -> None:
        """
        Set the configuration for the calculations

        Warning: This method will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param config: Trip configuration either as a dictionary or as a TripConfig object
        """

        self.config = config
        self.updated = True

    def calculate_trip(self, config: TripConfig = None) -> Dict:
        """
        Calls the Google Maps API to calculate the trip, only if the trip needs to be updated.

        This method will make at least one call to the Google Maps API and at most 1 + the number of stops.

        If the trip mode is not set to 'transit', 'end_date' is ignored for the request.

        :param config: Trip configuration either as a dictionary or as a TripConfig object
        :return: The raw API response if no stops are provided, otherwise a dictionary with the raw API responses
        """

        if config:
            self.set_config(config)

        if not self.updated:
            return self.raw_result

        if not self.client:
            raise ClientNotInitializedError()

        # Make calls to the API
        if self.stops:
            current_location = self.origin
            current_date = self.start_date if self.start_date else datetime.now()  # HTTP Error 400 otherwise...

            if self.end_date:
                TripWarning.ignore_field('end_date', 'Ignored for trips with stops')

            # Call for each stop
            for index, stop in enumerate(self.stops):
                key = f'stage_{index}' if index > 0 else 'departure'

                self.raw_result[key] = self.client.directions(
                    origin=(
                        current_location.coords
                        if current_location.coords
                        else current_location.address
                    ),
                    destination=(
                        stop.location.coords
                        if stop.location.coords
                        else stop.location.address
                    ),
                    departure_time=current_date,
                    **self.config,
                )[0]

                current_location = stop.location
                current_date = stop.departure_date

            # Call for last stage of the trip
            self.raw_result['arrival'] = self.client.directions(
                origin=(
                    current_location.coords
                    if current_location.coords
                    else current_location.address
                ),
                destination=(
                    self.destination.coords
                    if self.destination.coords
                    else self.destination.address
                ),
                departure_time=current_date,
                **self.config,
            )[0]

        else:
            # Call depending on the given fields and configuration
            if self.start_date:
                self.raw_result = self.client.directions(
                    origin=(
                        self.origin.coords
                        if self.origin.coords
                        else self.origin.address
                    ),
                    destination=(
                        self.destination.coords
                        if self.destination.coords
                        else self.destination.address
                    ),
                    departure_time=self.start_date,
                    **self.config,
                )[0]
            elif self.end_date and self.config.get("mode", "no_mode") == "transit":
                self.raw_result = self.client.directions(
                    origin=(
                        self.origin.coords
                        if self.origin.coords
                        else self.origin.address
                    ),
                    destination=(
                        self.destination.coords
                        if self.destination.coords
                        else self.destination.address
                    ),
                    arrival_time=self.end_date,
                    **self.config,
                )[0]
            elif self.end_date and not self.config.get("mode", "no_mode") == "transit":
                TripWarning.ignore_field("end_date", "Only used for transit mode")
            else:
                self.raw_result = self.client.directions(
                    origin=(
                        self.origin.coords
                        if self.origin.coords
                        else self.origin.address
                    ),
                    destination=(
                        self.destination.coords
                        if self.destination.coords
                        else self.destination.address
                    ),
                    departure_time=datetime.now(),  # HTTP Error 400 otherwise...
                    **self.config,
                )[0]

        self.updated = False
        return self.raw_result
