from fixtures import basic_trip, trip_one_stop
import pytest

from py_travel import Location, Trip


class TestTrip:
    @pytest.mark.parametrize(
        'test_input',
        [
            # Coordinates
            {'origin': (0.0, 0.0), 'destination': (0.0, 0.0)},
            # Address
            {'origin': 'Test Origin', 'destination': 'Test Destination'},
            # Location object
            {'origin': Location(0.0, 0.0, 'Test Origin'), 'destination': Location(0.0, 0.0, 'Test Destination')}
        ])
    def test_create_trip(self, test_input):
        """
        Test that a Trip object can be instantiated
        """
        try:
            Trip(**test_input)
        except TypeError:
            pytest.fail('Invalid parameter')

    def test_distance(self, basic_trip, trip_one_stop):
        """
        Test that the distance calculation works
        """
        assert basic_trip.distance == 1
        assert trip_one_stop.distance == 2

    def test_distances(self, basic_trip, trip_one_stop):
        """
        Test that the partial distances calculation works
        """
        assert basic_trip.get_distances() == [1]
        assert trip_one_stop.get_distances() == [1, 1]
