from typing import Dict, List, Tuple

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


def estimate_distance(m_second: float, travel_seconds: int) -> float:
    """
    Estimates the distance travelled in a given time

    :param m_second: Amount of meters travelled per second
    :param travel_seconds: Travel time in seconds
    :return: An estimated distance travelled in 'travel_seconds'
    """

    return m_second * travel_seconds


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
