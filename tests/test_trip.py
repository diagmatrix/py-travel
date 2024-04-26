from fixtures import *
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

    def test_distance(self, basic_trip, trip_stop):
        """
        Test that the distance calculation works
        """
        assert basic_trip.distance == 1
        assert trip_stop.distance == 2

    def test_distances(self, basic_trip, trip_stop):
        """
        Test that the partial distances calculation works
        """
        assert basic_trip.distances == [1]
        assert trip_stop.distances == [1, 1]

    def test_travel_time(self, basic_trip, trip_stop):
        """
        Test that the duration calculation works
        """
        assert basic_trip.travel_time == 60
        assert trip_stop.travel_time == 120

    def test_travel_times(self, basic_trip, trip_stop):
        """
        Test that the partial duration calculation works
        """
        assert basic_trip.travel_times == [60]
        assert trip_stop.travel_times == [60, 60]

    @pytest.mark.parametrize(
        ('departure', 'arrival'),
        [
            # No dates
            (None, None),
            # Only departure
            (datetime.now(), None),
            # Only arrival
            (None, datetime.now()),
            # Departure & arrival
            (datetime.now(), datetime.now())
        ]
    )
    def test_updated_dates(self, departure, arrival):
        """
        Test that the dates are updated after trip calculations
        """

        old_departure = departure
        old_arrival = arrival
        trip = Trip('', '', departure_date=departure, arrival_date=arrival)
        trip.calculate_trip()

        if not departure:
            assert trip.departure_date != old_departure
        if not arrival or (departure and arrival):
            assert trip.arrival_date != old_arrival

    def test_updated_dates_stops(self, trip_stop):
        """
        Test that the dates are updated after trip calculations for a trip with stops
        """

        stop_date = trip_stop.stops[0].departure_date

        trip_stop.calculate_trip()

        assert trip_stop.stops[0].departure_date != stop_date

