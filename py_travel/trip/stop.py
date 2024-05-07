from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from datetime import datetime
    from py_travel.location import Location


class Stop(NamedTuple):
    """
    Tuple representing a stop

    Attributes:
        location: Location of the stop
        departure_date: Departure date from the stop
    """

    location: "Location"
    departure_date: "datetime"
