from typing import List

from shared.geo.coordinate import Coordinate
from shared.io.parsable import Parsable
from shared.io.serializable import Serializable


class FlightPath(Serializable, Parsable):
    """FlightPath is a path in 2D space that a drone will follow."""

    def __init__(self, id_: str, start: Coordinate, end: Coordinate, coordinates: List[Coordinate]):
        self.id = id_
        self.start = start
        self.end = end
        self.coordinates = coordinates

    def to_json(self):
        return {
            "id": self.id,
            "start": self.start.to_json(),
            "end": self.end.to_json(),
            "coordinates": [coordinate.to_json() for coordinate in self.coordinates]
        }

    @staticmethod
    def from_json(json_message):
        return FlightPath(json_message['id'],
                          Coordinate.from_json(json_message['start']), Coordinate.from_json(json_message['end']),
                          [Coordinate.from_json(coordinate) for coordinate in json_message['coordinates']])
