from datetime import datetime, timedelta

import pytest

from py_travel import Client, Trip

from test_client import TestClient

# Set the Google Maps API Client to the mock
Client.client = TestClient('a')


@pytest.fixture
def basic_trip() -> Trip:
    """
    Create a basic Trip object without stops and dates
    """
    return Trip(origin='Test Origin', destination='Test Destination')

@pytest.fixture
def trip_one_stop() -> Trip:
    """
    Create a Trip object with one stop and no dates
    """
    return Trip(origin='Test Origin', destination='Test Destination', stops=[('Test Stop 1', datetime.now() + timedelta(days=1))])
