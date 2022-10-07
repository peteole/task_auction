from typing import List

from shared.geo.coordinate import Coordinate
from shared.io.parsable import Parsable
from shared.io.serializable import Serializable


class Obstacle(Serializable, Parsable):
    """Obstacle is a closed geometric figure that should be flown around."""

    def __init__(self, coordinates: List[Coordinate]):
        self.coordinates = coordinates

    def to_json(self):
        return {
            "coordinates": [coordinate.to_json() for coordinate in self.coordinates]
        }

    @staticmethod
    def from_json(json_message):
        return Obstacle([Coordinate.from_json(coordinate) for coordinate in json_message['coordinates']])
