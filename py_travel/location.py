"""
Location class.

Classes:
    Location: Represents a location in the globe.

Functions:
    input_to_location: Transforms a coordinates tuple or an address into a Location object.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Location:
    """
    Represents a location in the globe

    Attributes:
        lat: Latitude of the location (optional)
        lng: Longitude of the location (optional)
        address: Address of the location with that coordinates (optional)
    """

    lat: float | None = None
    lng: float | None = None
    address: str | None = None

    @property
    def coords(self) -> Tuple[float, float] | None:
        """
        Returns the coordinates of the location if it has them

        :return: The latitude and longitude of the location as a tuple
        """
        if self.lat and self.lng:
            return self.lat, self.lng
        else:
            return None

    def get_data(self) -> Tuple[float, float] | str:
        """
        Yields the most precise data available for the location.

        :return: The coordinates if they are present, otherwise the address
        """
        return self.coords if self.coords else self.address


def input_to_location(data: Tuple[float, float] | str | Location) -> Location:
    """
    Converts a given 'Location' into a location object

    :param data: Tuple with (latitude, longitude), string address or Location object
    :return: A Location object from the given data
    """
    if isinstance(data, Location):
        return data
    if isinstance(data, str):
        return Location(address=data)
    if isinstance(data, tuple):
        return Location(lat=data[0], lng=data[1])
    else:
        raise TypeError("Argument must be a string or a tuple containing two floats")
