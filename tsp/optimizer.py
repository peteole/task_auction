from typing import List

from ortools.constraint_solver import pywrapcp, routing_enums_pb2


class Optimizer:
    def __init__(self, costs: List[List[int]],
                 local_search_metaheuristic: routing_enums_pb2.LocalSearchMetaheuristic,
                 first_solution_strategy: routing_enums_pb2.FirstSolutionStrategy,
                 solution_limit: int, log_search: bool, task_values: List[int], bidder):

        self.costs = costs

        # Create routing model
        self.manager = pywrapcp.RoutingIndexManager(
            len(self.costs), 1, [0], [1])
        self.routing = pywrapcp.RoutingModel(self.manager)

        # Create distance callback
        def distance_callback(from_index, to_index):
            from_element_index = self.manager.IndexToNode(from_index)
            to_element_index = self.manager.IndexToNode(to_index)

            return self.costs[from_element_index][to_element_index]

        transit_callback_index = self.routing.RegisterTransitCallback(
            distance_callback)
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Only allow cumulative distance costs of 100% energy
        # self.routing.AddDimension(
        #     transit_callback_index, 0, bidder.max_flight_time, True, 'Distance')

        self.routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            bidder.max_flight_time,  # vehicle maximum travel distance
            True,  # start cumul to zero
            "Capacity")

        # print(self.manager.GetNumberOfNodes())
        # print(self.manager.GetNumberOfIndices())
        # print(self.manager.IndexToNode(self.manager.GetStartIndex(0)))
        # print(self.manager.IndexToNode(self.manager.GetEndIndex(0)))
        # print("****")
        # for i in range(len(costs)):
        #     print(self.manager.NodeToIndex(i))
        # print("****")
        # Allow to drop visits but penalize every dropped point
        for node in range(2, len(costs)):
            # print(round(task_values[node]))
            penalty = round(task_values[node])
            if penalty <= 0:
                penalty = 0
            self.routing.AddDisjunction(
                [self.manager.NodeToIndex(node)], penalty)

        # print("****")

        # Set routing parameters
        self.search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        self.search_parameters.first_solution_strategy = first_solution_strategy.value
        self.search_parameters.local_search_metaheuristic = local_search_metaheuristic.value
        self.search_parameters.solution_limit = solution_limit
        self.search_parameters.time_limit.seconds = 1
        self.search_parameters.log_search = log_search

    def optimize(self) -> List[int]:
        assignment = self.routing.SolveWithParameters(self.search_parameters)
        if self.routing.status() != 1:
            raise Exception(f"Routing failed.")
        optimal_order = self.format_solution(assignment)
        return optimal_order

    def format_solution(self, assignment) -> List[int]:
        index = self.routing.Start(0)
        optimal_order = []
        route_objective = 0
        while not self.routing.IsEnd(index):
            optimal_order.append(self.manager.IndexToNode(index))
            previous_index = index
            index = assignment.Value(self.routing.NextVar(index))
            route_objective += self.routing.GetArcCostForVehicle(
                previous_index, index, 0)
        optimal_order.append(self.manager.IndexToNode(index))

        return optimal_order
