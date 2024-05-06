"""
Wrappers to the Google Maps API Python client package.

Classes:
    Client: Abstract base class for the Google Maps API clients.

    DirectionsClient: Google Maps Directions API client.
"""


from .client import Client
from .directions_client import DirectionsClient

__all__ = ['Client', 'DirectionsClient']
