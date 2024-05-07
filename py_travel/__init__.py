"""
Python Travel Library.

This package tries to make it easier to use the Google Maps API for trip planning and a less JSON oriented way of
working with the API.

Modules:
    trip: Provides the tools and classes used to interact with the Google Maps API for trip planning.

Classes:
    Client: Provides a wrapper for the googlemaps client class.

    Location: Represents a location in the globe. Contains the coordinates and the address.

    TravelWarnings: Collection of warnings raised by the trip class.

Functions:
    init_clients: Initializes all the library classes' clients with the ones provided by this library.

Exceptions:
    ClientNotInitializedError: Raised when no client capable of requesting the Google Maps API is found (Trip class).

    InvalidResponseError: Raised when the API response does not contain some expected field or value (Trip class).

    ApiError: Raised when the Google Maps API returns an error (Client subclasses).

    LocationNotFoundError: Raised when the Google Maps API cannot find a location (Client subclasses).

    InvalidRequestError: Raised when an invalid request is sent to the Google Maps API (Client subclasses).

"""

# Export client
from .client import Client

# Export exceptions
from .exceptions import (
    TravelWarnings, ClientNotInitializedError, InvalidResponseError, InvalidRequestError, ApiError,
    LocationNotFoundError
)

# Export location
from .location import Location

# Export init_clients
from .utils import init_clients

__all__ = [
    "TravelWarnings", "ClientNotInitializedError", "InvalidResponseError", "InvalidRequestError", "ApiError",
    "LocationNotFoundError", "Client", "Location", "init_clients"
]
