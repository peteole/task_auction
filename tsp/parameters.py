from enum import Enum

from ortools.constraint_solver import routing_enums_pb2


class LocalSearchMetaheuristic(Enum):
    GUIDED_LOCAL_SEARCH = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    GREEDY_DESCENT = routing_enums_pb2.LocalSearchMetaheuristic.GREEDY_DESCENT
    SIMULATED_ANNEALING = routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING
    TABU_SEARCH = routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH


class FirstSolutionStrategy(Enum):
    AUTOMATIC = routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
    PATH_CHEAPEST_ARC = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    SAVINGS = routing_enums_pb2.FirstSolutionStrategy.SAVINGS
    SWEEP = routing_enums_pb2.FirstSolutionStrategy.SWEEP
    CHRISTOFIDES = routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES
    PARALLEL_CHEAPEST_INSERTION = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    LOCAL_CHEAPEST_INSERTION = routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_INSERTION
    GLOBAL_CHEAPEST_ARC = routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC
    LOCAL_CHEAPEST_ARC = routing_enums_pb2.FirstSolutionStrategy.LOCAL_CHEAPEST_ARC
    FIRST_UNBOUND_MIN_VALUE = routing_enums_pb2.FirstSolutionStrategy.FIRST_UNBOUND_MIN_VALUE
