from shared.io.parsable import Parsable
from shared.io.serializable import Serializable


class EstimationParameters(Serializable, Parsable):
    def __init__(self, energy_per_minute: float, avg_velocity: float, buoy_communication_time: float):
        self.energy_per_minute = energy_per_minute
        self.avg_velocity = avg_velocity
        self.buoy_communication_time = buoy_communication_time

    def to_json(self):
        return {
            "energy_per_minute": self.energy_per_minute,
            "avg_velocity": self.avg_velocity,
            "buoy_communication_time": self.buoy_communication_time
        }

    @staticmethod
    def from_json(json_message):
        return EstimationParameters(json_message["energy_per_minute"],
                                    json_message["avg_velocity"],
                                    json_message["buoy_communication_time"])
