from datetime import datetime
from typing import Tuple, List, Dict, Literal, TypedDict

from .exceptions import ClientNotInitializedError, TripWarning, InvalidResponseError
from .location import Location, input_to_location
from .utils import meters_to_miles
from .vars import (
    Stop,
    TRIP_MODES,
    AVOID_FEATURES,
    TRANSIT_MODES,
    TRANSIT_PREFERENCES,
    TRAFFIC_MODE, METRIC_SYSTEMS,
)
from .client import Client


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
    units: METRIC_SYSTEMS
    transit_mode: List[TRANSIT_MODES] | TRANSIT_MODES
    transit_routing_preference: TRANSIT_PREFERENCES
    traffic_model: TRAFFIC_MODE


class Trip(Client):
    """
    Trip class

    Attributes:
        origin: Origin of the trip
        destination: Destination of the trip
        departure_date: Start date of the trip
        arrival_date: End date of the trip
        stops: List of stops associated with the trip
        updated: Boolean indicating if the object needs to call the Google Maps API to get the results
        api_response: Raw Google Maps API response
    """

    def __init__(
        self,
        origin: Tuple[float, float] | str | Location,
        destination: Tuple[float, float] | str | Location,
        stops: List[Tuple[Tuple[float, float] | str | Location, datetime]] = None,
        departure_date: datetime = None,
        arrival_date: datetime = None,
        config: TripConfig = None,
    ) -> None:
        """
        Initialize Trip object

        :param origin: Origin of the trip in pair (latitude, longitude) or address or Location object
        :param destination: Destination of the trip in pair (latitude, longitude) or address or Location object
        :param stops: A list of tuples containing the stop location (either a tuple containing the coordinates, the
            address or a Location object) and the departure date from the stop
        :param departure_date: Start date of the trip (optional)
        :param arrival_date: End date of the trip (optional)
        :param config: Trip configuration either as a dictionary or as a TripConfig object (optional)
        """

        self.__origin = input_to_location(origin)
        self.__destination = input_to_location(destination)

        self.__stops = (
            [Stop(input_to_location(loc), dep_date) for loc, dep_date in stops]
            if stops
            else []
        )
        self.__stops.sort(key=lambda stop: stop.departure_date)

        self.__departure_date = departure_date
        self.__arrival_date = arrival_date

        self.__config = config

        self.__api_response: Dict = {}
        self.__updated = True

    @property
    def origin(self) -> Location:
        """
        :return: The origin location of the trip
        """
        return self.__origin

    @origin.setter
    def origin(self, new_origin: Tuple[float, float] | str | Location) -> None:
        """
        Sets the origin location of the trip

        Warning: This will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param new_origin: Origin of the trip in pair (latitude, longitude), string with address or Location object
        """
        self.__origin = input_to_location(new_origin)
        self.__updated = True

    @property
    def destination(self) -> Location:
        """
        :return: The destination location of the trip
        """
        return self.__destination

    @destination.setter
    def destination(
        self, new_destination: Tuple[float, float] | str | Location
    ) -> None:
        """
        Sets the destination location of the trip

        Warning: This will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param new_destination: Destination of the trip in pair (latitude, longitude), string with address or Location
            object
        """
        self.__destination = input_to_location(new_destination)
        self.__updated = True

    @property
    def stops(self) -> List[Stop]:
        """
        :return: The list of stops
        """
        return self.__stops

    @stops.setter
    def stops(
        self, stops: List[Tuple[Tuple[float, float] | str | Location, datetime]]
    ) -> None:
        """
        Sets the stops for the trip

        Warning: This will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param stops: A list of tuples containing the stop location (either a tuple containing the coordinates, the
            address or a Location object) and the departure date from the stop
        """

        self.__stops = [
            Stop(input_to_location(loc), dep_date) for loc, dep_date in stops
        ]
        self.__stops.sort(key=lambda stop: stop.departure_date)
        self.__updated = True

    @property
    def departure_date(self) -> datetime:
        """
        :return: The departure date of the trip
        """
        return self.__departure_date

    @departure_date.setter
    def departure_date(self, new_departure_date: datetime) -> None:
        """
        Sets the departure date of the trip

        Warning: This will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param new_departure_date: The departure date of the trip
        """
        self.__departure_date = new_departure_date
        self.__updated = True

    @property
    def arrival_date(self) -> datetime:
        """
        :return: The arrival date of the trip
        """
        return self.__arrival_date

    @arrival_date.setter
    def arrival_date(self, new_arrival_date: datetime) -> None:
        """
        Sets the arrival date of the trip

        Warning: This will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param new_arrival_date: The arrival date of the trip
        """
        self.__arrival_date = new_arrival_date
        self.__updated = True

    @property
    def config(self) -> TripConfig:
        """
        :return: The configuration parameters of the trip
        """
        return self.__config

    @config.setter
    def config(self, new_config: TripConfig) -> None:
        """
        Set the configuration for the calculations

        Warning: This method will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param new_config: Trip configuration
        """

        self.__config = new_config
        self.__updated = True

    @property
    def api_response(self) -> Dict:
        """
        :return: The response from the Google Maps API
        """
        return self.__api_response

    def set_response(self, response: Dict) -> None:
        """
        Set the response from the Google Maps API. USE ONLY FOR TESTS

        TODO: Remove this
        """
        self.__api_response = response
        self.__updated = False

    def calculate_trip(self, trip_config: TripConfig = None) -> Dict:
        """
        Calls the Google Maps API to calculate the trip, only if the trip needs to be updated.

        This method will make at least one call to the Google Maps API and at most 1 + the number of stops.

        :param trip_config: Trip configuration
        :return: The raw API response if no stops are provided, otherwise a dictionary with the raw API responses
        :raises ClientNotInitializedError: If the googlemaps client is not initialized
        :raises TripWarning: If a trip attribute is ignored based on the config given
        """

        if trip_config:
            self.config = trip_config

        if not self.__updated:
            return self.__api_response

        if not self.client:
            raise ClientNotInitializedError()

        if self.__arrival_date and self.__stops:
            TripWarning.ignore_field("arrival_date", "Ignored for trips with stops")
        elif (
            self.__arrival_date
            and not self.__config.get("mode", "not_configured") == "transit"
        ):
            TripWarning.ignore_field("arrival_date", "Only used for transit mode")

        # Make calls to the API
        if self.__stops:
            current_location = self.__origin.get_data()
            current_date = (
                self.__departure_date if self.__departure_date else datetime.now()
            )  # Fixes HTTP 400 error

            # Call for each stop
            for index, stop in enumerate(self.__stops):
                key = f"stage_{index}" if index > 0 else "departure"

                self.__api_response[key] = self.client.directions(
                    origin=current_location,
                    destination=stop.location.get_data(),
                    departure_time=current_date,
                    **self.__config,
                )[0]

                current_location = stop.location.get_data()
                current_date = stop.departure_date

            # Call for last stage of the trip
            self.__api_response["arrival"] = self.client.directions(
                origin=current_location,
                destination=self.__destination.get_data(),
                departure_time=current_date,
                **self.__config,
            )[0]

        else:
            # Date argument depending on the given fields and configuration
            if self.__departure_date:
                date_argument = {"departure_time": self.__departure_date}
            elif (
                self.__arrival_date
                and self.__config.get("mode", "not_configured") == "transit"
            ):
                date_argument = {"arrival_time": self.__arrival_date}
            else:
                date_argument = {"departure_time": datetime.now()}  # Fixes HTTP 400 error

            self.__api_response = self.client.directions(
                origin=self.__origin.get_data(),
                destination=self.__destination.get_data(),
                **date_argument,
                **self.__config,
            )[0]

        self.__updated = False
        return self.__api_response

    @property
    def distance(self) -> float:
        """
        Warning: If the trip is marked as updated, it will first calculate the trip
        :return: The total distance of the trip in the unit given in the config ('metric' if not configured).
        """

        if self.__updated:
            self.calculate_trip()

        if self.__stops:
            meters = 0.0
            for stage in self.__api_response.values():
                stage_meters = stage.get("legs", [{}])[0].get("distance", {}).get("value", None)
                if not stage_meters:
                    raise InvalidResponseError('legs[0].distance.value')
                meters += stage_meters
        else:
            meters: float | None = self.__api_response.get("legs", [{}])[0].get("distance", {}).get("value", None)
            if not meters:
                raise InvalidResponseError('legs[0].distance.value')

        return meters / 1000 if self.__config.get("units", "metric") == "metric" else meters_to_miles(meters)
