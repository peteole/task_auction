from flightcosts.cost_estimator import estimate_costs
from flightcosts.estimation_parameters import EstimationParameters
from flightpath.path_planner import *


class Task:
    def __init__(self, value: float, coordinate: Coordinate) -> None:
        self.value = value
        self.coordinate = coordinate


class Setting:
    def __init__(self, tasks: List[Task]) -> None:
        self.tasks = tasks
        flight_paths = create_flight_paths([t.coordinate for t in self.tasks], [])
        # TODO: fix
        self.costs = estimate_costs(flight_paths, EstimationParameters(2, 5, 0))
        self.max_flight_time = 600
