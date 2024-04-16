from datetime import datetime, timedelta
from typing import Any, Tuple, Dict

from py_travel_old.models import Client, Location, Trip
from py_travel_old.exceptions import ClientNotInitializedError, MissingDataError


def get_step_data(trip_data: Dict[str, Any]) -> Tuple[float, timedelta, Location, Dict]:
    """
    Parses a piece of data from the Google Maps API response and returns relevant data

    :param trip_data: Piece of data from the Google Maps API ('legs' value or one 'legs.steps' item)
    :return: A tuple containing the amount of kms travelled, the amount of time travelled, the ending location and ...
    :raises MissingDataError: If some of the required fields are missing from the response
    """

    # Get distance travelled
    if (distance := trip_data.get("distance", {}).get("value", None)) is None:
        raise MissingDataError("distance")
    distance: float = float(distance) / 1000

    # Get travel duration
    if (duration_seconds := trip_data.get("duration", {}).get("value", None)) is None:
        raise MissingDataError("duration")
    duration: timedelta = timedelta(seconds=duration_seconds)

    # Get end location
    if (coords := trip_data.get("end_location", None)) is None:
        raise MissingDataError("end_location")
    end_address = trip_data.get("end_address", "")
    end_location = Location(address=end_address, **coords)

    return distance, duration, end_location, {}


class TripManager(Client):
    @classmethod
    def calculate_trip(
        cls,
        origin: str,
        destination: str,
        departure_date: datetime = datetime.now(),
        arrival_date: datetime = None,
    ) -> Trip:
        if not cls.client:
            raise ClientNotInitializedError()
        else:
            gmaps_response: Dict = cls.client.directions(
                origin=origin, destination=destination
            )[0]
            trip_data: Dict = gmaps_response.get("legs", [{}])[0]

            trip_kms, trip_duration, trip_end_location, trip = get_step_data(trip_data)

            return Trip(trip_kms, trip_duration, end_location=trip_end_location)
