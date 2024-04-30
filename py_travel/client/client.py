import googlemaps
from typing import Dict
from abc import abstractmethod


class Client:
    """
    Base Client Class for all Google Maps API clients

    Attributes:
        client: Google Maps API client (class attribute)
    """

    __abstract__ = True

    def __init__(self, api_key: str) -> None:
        self.__client = googlemaps.Client(key=api_key)

    @property
    def client(self) -> googlemaps.Client:
        return self.__client

    @client.setter
    def client(self, api_key: str) -> None:
        """
        Set Google Maps Client

        :param api_key: API key for Google Maps
        """
        self.client = googlemaps.Client(key=api_key)

    @abstractmethod
    def directions(self, **kwargs) -> Dict:
        raise NotImplementedError
