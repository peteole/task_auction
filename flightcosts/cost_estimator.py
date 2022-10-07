from math import sqrt
from typing import List

from flightcosts.estimation_parameters import EstimationParameters
from flightpath.flight_path import FlightPath
from shared.geo.converter import latlon_to_utm


def estimate_cost(flight_path: FlightPath, parameters: EstimationParameters) -> int:
    """Estimate cost of a single flight path"""

    flight_distance = 0.0
    utm_coordinates, reference_coordinate = latlon_to_utm(flight_path.coordinates)
    for i in range(len(utm_coordinates) - 1):
        y_diff = utm_coordinates[i].north - utm_coordinates[i + 1].north
        x_diff = utm_coordinates[i].east - utm_coordinates[i + 1].east
        flight_distance += sqrt(y_diff ** 2 + x_diff ** 2)

    flight_time = flight_distance / parameters.avg_velocity + parameters.buoy_communication_time
    return int(flight_time)


def estimate_costs(flight_paths: List[List[FlightPath]], parameters: EstimationParameters) -> List[List[int]]:
    """Estimate costs of a square matrix consisting of flight paths. Return a square matrix of costs"""
    costs = []
    for row in flight_paths:
        costs.append([])
        for path in row:
            costs[-1].append(estimate_cost(path, parameters))

    return costs
