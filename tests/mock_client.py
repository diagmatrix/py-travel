from typing import List, TYPE_CHECKING, Dict

if TYPE_CHECKING:  # pragma: no cover
    from datetime import datetime

# ----------------------------------------------------------------------------------------------------------------------
# Mock constants
TEST_METERS = 1800
TEST_SECONDS = 3600
MOCK_N_STEPS = 10
MOCK_DISTANCE = {"distance": {"value": TEST_METERS}}
MOCK_TIME = {"duration": {"value": TEST_SECONDS}}
MOCK_STEP = {**MOCK_DISTANCE, **MOCK_TIME}


# ----------------------------------------------------------------------------------------------------------------------
# Mock classes
class ClientNotInitializedError(Exception):
    pass


class TestClient:
    """
    Test client to avoid calls to the Google Maps API in testing
    """

    def __init__(self, key: str = None):
        """
        Initialize the client

        :param key: Mock API key
        """

        if not isinstance(key, str):
            raise ValueError("Key must be a string")

        self.key = key

    def directions(
        self,
        origin: str,
        destination: str,
        mode: str = None,
        avoid: List[str] | str = None,
        units: str = None,
        departure_time: "datetime" = None,
        arrival_time: "datetime" = None,
        transit_mode: List[str] | str = None,
        transit_routing_preference: str = None,
        traffic_model: str = None,
    ) -> List[Dict]:
        """
        Mocks the Google Maps API 'directions' method
        """

        if not self.key:
            raise ClientNotInitializedError()

        response = {
            "input": {
                "origin": origin,
                "destination": destination,
                "mode": mode,
                "avoid": avoid,
                "units": units,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "transit_mode": transit_mode,
                "transit_routing_preference": transit_routing_preference,
                "traffic_model": traffic_model,
            },
            "legs": [{
                **MOCK_DISTANCE,
                **MOCK_TIME,
                "steps": [{**MOCK_STEP}] * MOCK_N_STEPS
            }]
        }

        return [response]