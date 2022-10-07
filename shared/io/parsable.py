from abc import ABC, abstractmethod


class Parsable(ABC):
    @staticmethod
    @abstractmethod
    def from_json(json_message):
        pass
