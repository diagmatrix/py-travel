import googlemaps
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from datetime import timedelta


class Client:
    """
    Google Maps Client for interacting with Google Maps API
    """

    client: googlemaps.Client

    @classmethod
    def set_client(cls, api_key: str) -> None:
        """
        Set Google Maps Client

        :param api_key: API key for Google Maps
        """
        cls.client = googlemaps.Client(key=api_key)


@dataclass
class Location:
    """
    Represents a location in the globe

    Attributes:
        lat: Latitude of the location
        lng: Longitude of the location
        address: Address of the location with that coordinates (optional)
    """

    lat: float
    lng: float
    address: str = ""


@dataclass
class Trip:
    """
    Represents a trip

    Attributes:
        kms: Amount of kilometers travelled on the trip
        duration: Duration of the trip
        start_location: Starting location of the trip (optional)
        end_location: Ending location of the trip (optional)
    """

    kms: float
    duration: "timedelta"

    start_location: Location = None
    end_location: Location = None
