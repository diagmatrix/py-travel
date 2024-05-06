from datetime import datetime, timedelta

import pytest

from py_travel.trip import Trip
from mock_client import TestClient

# Set the Google Maps API Client to the mock
TC = TestClient("a")
Trip.set_client(TC)


@pytest.fixture
def basic_trip() -> Trip:
    """
    Create a basic Trip object without stops
    """
    return Trip(
        origin="Test Origin",
        destination="Test Destination",
        departure_date=datetime.now(),
        arrival_date=datetime.now(),
    )


@pytest.fixture
def trip_stop() -> Trip:
    """
    Create a Trip object with one stop
    """
    return Trip(
        origin="Test Origin",
        destination="Test Destination",
        departure_date=datetime.now(),
        arrival_date=datetime.now(),
        stops=[("Test Stop 1", datetime.now())],
    )


@pytest.fixture
def trip_stops() -> Trip:
    """
    Create a Trip object with multiple stops
    """
    return Trip(
        origin="Test Origin",
        destination="Test Destination",
        departure_date=datetime(year=1999, month=1, day=1),
        stops=[
            ("Test Stop 1", datetime(year=1999, month=1, day=1) + timedelta(days=1)),
            ("Test Stop 2", datetime(year=1999, month=1, day=1) + timedelta(days=2)),
            ("Test Stop 3", datetime(year=1999, month=1, day=1) + timedelta(days=3))
        ],
    )
