"""
Python Travel Library.

This package tries to make it easier to use the Google Maps API for trip planning and a less JSON oriented way of
working with the API.

Modules:
    client: Provides some wrappers for the googlemaps python library.

    trip: Provides the tools and classes used to interact with the Google Maps API for trip planning.

Classes:
    Location: Represents a location in the globe. Contains the coordinates and the address.

    TripWarning: Collection of warnings raised by the trip class.

Functions:
    init_clients: Initializes all the library classes' clients with the ones provided by this library.

Exceptions:
    ClientNotInitializedError: Raised when no client capable of requesting the Google Maps API is found (Trip class).

    InvalidResponseError: Raised when the API response does not contain some expected field or value (Trip class).

    ApiError: Raised when the Google Maps API returns an error (Client subclasses).

    LocationNotFoundError: Raised when the Google Maps API cannot find a location (Client subclasses).

    InvalidRequestError: Raised when an invalid request is sent to the Google Maps API (Client subclasses).

"""


def init_clients(api_key: str) -> None:
    """
    Initializes the library provided clients for all classes that use them.

    :param api_key: Google Maps API key
    """
    from py_travel.client import DirectionsClient
    from py_travel.trip import Trip

    # Create clients
    directions_client = DirectionsClient(api_key)

    Trip.set_client(directions_client)