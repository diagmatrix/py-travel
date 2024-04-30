from datetime import datetime

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
    Create a Trip object with one stop and no dates
    """
    return Trip(
        origin="Test Origin",
        destination="Test Destination",
        departure_date=datetime.now(),
        arrival_date=datetime.now(),
        stops=[("Test Stop 1", datetime.now())],
    )
