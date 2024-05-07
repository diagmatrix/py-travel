"""
Global constants used throughout the package
"""
from typing import Literal

METERS_IN_MILE = 1609.344  # Meters in a mile

TRIP_MODES = Literal["driving", "walking", "bicycling", "transit"]  # Trip modes
AVOID_FEATURES = Literal["tolls", "highways", "ferries", "indoor"]  # Road features to avoid
TRANSIT_MODES = Literal["bus", "subway", "train", "tram", "rail"]  # Transit modes
TRANSIT_PREFERENCES = Literal["less_walking", "fewer_transfers"]  # Transit preferences
TRAFFIC_MODE = Literal["best_guess", "optimistic", "pessimistic"]  # Traffic model
METRIC_SYSTEMS = Literal["metric", "imperial"]  # Metric system
