from typing import TypedDict, List

from py_travel.vars import TRIP_MODES, AVOID_FEATURES, METRIC_SYSTEMS, TRANSIT_MODES, TRANSIT_PREFERENCES, TRAFFIC_MODE


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
