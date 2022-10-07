from shared.io.parsable import Parsable
from shared.io.serializable import Serializable


class Coordinate(Serializable, Parsable):
    """Coordinate is a point with latitude and longitude."""

    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def to_json(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    @staticmethod
    def from_json(json_message):
        return Coordinate(json_message['latitude'], json_message['longitude'])

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"

    def __repr__(self):
        return self.__str__()


class UTMCoordinate:
    """
    UTM coordinates are X,Y-coordinates that can be used for normal geometric operations.
    See this article:
    https://gisgeography.com/utm-universal-transverse-mercator-projection/
    """

    def __init__(self, north: float, east: float):
        self.north = north
        self.east = east

    def __str__(self):
        return f"({self.north}, {self.east})"

    def __repr__(self):
        return self.__str__()
