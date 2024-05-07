"""
Utils functions used throughout the package. Divided by auxiliary functions and JSON parsing functions.

Auxiliary functions:
    meters_to_miles: Converts meters to miles.
    calculate_stage_steps: Calculates a portion of a trip calendar (used by Trip class).

Parser functions:
    get_distance: Parses a Google Maps Directions API response to retrieve the distance value.
    get_duration: Parses a Google Maps Directions API response to retrieve the duration value.
    get_steps: Parses a Google Maps Directions API response to retrieve the trip steps list.
"""

from typing import Dict, List, Tuple
from datetime import datetime, date, timedelta

from .exceptions import InvalidResponseError
from .vars import METERS_IN_MILE


# ----------------------------------------------------------------------------------------------------------------------
# AUXILIARY FUNCTIONS


def meters_to_miles(meters: float) -> float:
    """
    Converts meters to miles

    :param meters: Amount of meters
    :return: Amount of miles
    """
    return meters / METERS_IN_MILE


def calculate_stage_steps(steps: List[Tuple[int, int]], departure_date: datetime, calendar: Dict[date, float]) ->  Dict[date, float]:
    """
    Calculates the distance travelled each day

    :param steps: The stage steps as a list of pairs (meters, seconds)
    :param departure_date: The departure date of the stage
    :param calendar: The calendar dictionary.
    :return: The calendar with updated distances
    """
    current_date = departure_date
    max_day = datetime.combine(current_date, datetime.max.time())

    for step in steps:
        meters_second = step[0] / step[1]
        # Calculate the time after the step
        new_date = current_date + timedelta(seconds=step[1])

        # Add the distance travelled to the calendar
        while current_date < new_date:
            if new_date <= max_day:
                calendar.setdefault(current_date.date(), 0)  # If the key doesn't exist, create it and initialize to 0
                calendar[current_date.date()] += (new_date - current_date).total_seconds() * meters_second
                current_date = new_date
            # Estimate the distance travelled if the step spans more than one day
            else:
                calendar[current_date.date()] += (max_day - current_date).total_seconds() * meters_second
                current_date = datetime.combine(current_date + timedelta(days=1), datetime.min.time())
                max_day = datetime.combine(current_date, datetime.max.time())

    return calendar


def init_clients(api_key: str) -> None:
    """
    Initializes the library provided clients for all classes that use them.

    :param api_key: Google Maps API key
    """
    from py_travel import Client, Location
    from py_travel.trip import Trip

    client = Client(api_key)

    # Set clients
    Trip.set_client(client)
    Location.set_client(client)

# ----------------------------------------------------------------------------------------------------------------------
# PARSER FUNCTIONS


def get_distance(json: Dict, step: bool = False) -> int:
    """
    Retrieves distance in meters from API response

    :param json: The API response
    :param step: Whether the json is a step or not (default: False)
    :return: The distance in meters
    """

    json_subdict = json if step else json.get("legs", [{}])[0]
    error_msg = "distance.value" if step else "legs[0].distance.value"

    meters = json_subdict.get("distance", {}).get("value", -1)
    if meters < 0:
        raise InvalidResponseError(error_msg)

    return meters


def get_duration(json: Dict, step: bool = False) -> int:
    """
    Retrieves duration in seconds from API response

    :param json: The API response
    :param step: Whether the json is a step or not (default: False)
    :return: The duration in seconds
    """

    json_subdict = json if step else json.get("legs", [{}])[0]
    error_msg = "duration.value" if step else "legs[0].duration.value"

    seconds = json_subdict.get("duration", {}).get("value", -1)
    if seconds < 0:
        raise InvalidResponseError(error_msg)

    return seconds


def get_steps(json: Dict) -> List[Tuple[int, int]]:
    """
    Takes the API response and retrieves the steps

    :param json: The API response
    :return: A list containing tuples with the amount of meters and the amount of seconds
    """

    raw_steps = json.get("legs", [{}])[0].get("steps", [])
    if not raw_steps:
        raise InvalidResponseError("legs[0].steps")

    return [(get_distance(step, True), get_duration(step, True)) for step in raw_steps]
