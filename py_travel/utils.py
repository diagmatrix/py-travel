from .vars import METERS_IN_MILE


def meters_to_miles(meters: float) -> float:
    """
    Converts meters to miles
    :param meters: Amount of meters
    :return: Amount of miles
    """
    return meters / METERS_IN_MILE
