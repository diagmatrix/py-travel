from typing import NamedTuple, Literal, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .location import Location
    from datetime import datetime


# ----------------------------------------------------------------------------------------------------------------------
# NEW TYPES

class Stop(NamedTuple):
    """
    Tuple representing a stop

    Attributes:
        location: Location of the stop
        departure_date: Departure date from the stop
    """

    location: "Location"
    departure_date: "datetime"


TRIP_MODES = Literal["driving", "walking", "bicycling", "transit"]  # Trip modes
AVOID_FEATURES = Literal["tolls", "highways", "ferries", "indoor"]  # Road features to avoid
TRANSIT_MODES = Literal["bus", "subway", "train", "tram", "rail"]  # Transit modes
TRANSIT_PREFERENCES = Literal["less_walking", "fewer_transfers"]  # Transit preferences
TRAFFIC_MODE = Literal["best_guess", "optimistic", "pessimistic"]  # Traffic model
METRIC_SYSTEMS = Literal["metric", "imperial"]  # Metric system

# ----------------------------------------------------------------------------------------------------------------------
# CONSTANTS

METERS_IN_MILE = 1609.344  # Meters in a mile
