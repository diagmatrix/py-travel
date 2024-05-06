import pytest
from datetime import datetime

from py_travel.location import Location
from py_travel.trip import Trip
from mock_client import TEST_METERS, TEST_SECONDS


TEST_KMS = TEST_METERS / 1000


class TestTrip:
    @pytest.mark.parametrize(
        "test_input",
        [
            # Coordinates
            {"origin": (0.0, 0.0), "destination": (0.0, 0.0)},
            # Address
            {"origin": "Test Origin", "destination": "Test Destination"},
            # Location object
            {
                "origin": Location(0.0, 0.0, "Test Origin"),
                "destination": Location(0.0, 0.0, "Test Destination"),
            },
        ],
    )
    def test_create_trip(self, test_input):
        """
        Test that a Trip object can be instantiated
        """
        try:
            Trip(**test_input)
        except TypeError:
            pytest.fail("Invalid parameter")

    def test_distance(self, basic_trip, trip_stop):
        """
        Test that the distance calculation works
        """
        assert basic_trip.distance == TEST_KMS
        assert trip_stop.distance == TEST_KMS * 2

    def test_distances(self, basic_trip, trip_stop):
        """
        Test that the partial distances calculation works
        """
        assert basic_trip.stages_distances == [TEST_KMS]
        assert trip_stop.stages_distances == [TEST_KMS, TEST_KMS]

    def test_travel_time(self, basic_trip, trip_stop):
        """
        Test that the duration calculation works
        """
        assert basic_trip.seconds == TEST_SECONDS
        assert trip_stop.seconds == TEST_SECONDS * 2

    def test_travel_times(self, basic_trip, trip_stop):
        """
        Test that the partial duration calculation works
        """
        assert basic_trip.stages_seconds == [TEST_SECONDS]
        assert trip_stop.stages_seconds == [TEST_SECONDS, TEST_SECONDS]

    def test_days(self, basic_trip, trip_stop, trip_stops):
        """
        Test that the days calculation works
        """
        assert basic_trip.days == 1
        assert trip_stop.days == 1
        assert trip_stops.days == 4

    @pytest.mark.parametrize(
        ("departure", "arrival"),
        [
            # No dates
            (None, None),
            # Only departure
            (datetime.now(), None),
            # Only arrival
            (None, datetime.now()),
            # Departure & arrival
            (datetime.now(), datetime.now()),
        ],
    )
    def test_updated_dates(self, departure, arrival):
        """
        Test that the dates are updated after trip calculations
        """

        old_departure = departure
        old_arrival = arrival
        trip = Trip("", "", departure_date=departure, arrival_date=arrival)
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

    def test_calendar_no_stops(self, basic_trip):
        """
        Test that the trip calendar works with no stops
        """

        trip_calendar = basic_trip.trip_calendar

        assert len(trip_calendar) == 1
        assert trip_calendar[0][0] == datetime.now().date()

    def test_calendar_stops(self, trip_stops):
        """
        Test that the trip calendar works with no stops
        """

        trip_calendar = trip_stops.trip_calendar

        assert len(trip_calendar) == 4
        assert trip_calendar[0][0] == trip_stops.departure_date.date()
