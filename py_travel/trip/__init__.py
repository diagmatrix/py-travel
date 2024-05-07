"""
Trip class to manage and manipulate trips using a Google Maps API client.

Classes:
    Trip: Trip class.

Types:
    TripConfig: Dictionary with the configuration parameters for the Directions API requests.

    Stop: Tuple representing a stop in a trip.
"""

from .trip import Trip
from .trip_config import TripConfig
from .stop import Stop


__all__ = ['Trip', 'TripConfig', 'Stop']
