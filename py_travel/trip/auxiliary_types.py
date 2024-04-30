from typing import TypedDict, Literal, List, NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from datetime import datetime
    from py_travel.location import Location


TRIP_MODES = Literal["driving", "walking", "bicycling", "transit"]  # Trip modes
AVOID_FEATURES = Literal["tolls", "highways", "ferries", "indoor"]  # Road features to avoid
TRANSIT_MODES = Literal["bus", "subway", "train", "tram", "rail"]  # Transit modes
TRANSIT_PREFERENCES = Literal["less_walking", "fewer_transfers"]  # Transit preferences
TRAFFIC_MODE = Literal["best_guess", "optimistic", "pessimistic"]  # Traffic model
METRIC_SYSTEMS = Literal["metric", "imperial"]  # Metric system


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


class Stop(NamedTuple):
    """
    Tuple representing a stop

    Attributes:
        location: Location of the stop
        departure_date: Departure date from the stop
    """

    location: "Location"
    departure_date: "datetime"
