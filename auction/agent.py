import copy
from pprint import pprint
from random import random

from auction.auction import *
from auction.setting import *
from tsp.optimizer import *
from tsp.parameters import *




class Bidder:
    def __init__(self, coordinate: Coordinate, max_flight_time: int, tasks, home_coordinate: Coordinate):
        self.id = create_id()
        self.max_flight_time = max_flight_time
        self.coordinate = coordinate
        self.tasks = tasks
        self.home_coordinate = home_coordinate
        self.current_path:List[int] = None

        self.costs = self.create_costs()

    def create_costs(self):
        points = [self.coordinate, self.home_coordinate] + [task.coordinate for task in self.tasks]
        paths = [[FlightPath(create_id(), start=from_coordinate, end=to_coordinate,
                             coordinates=[from_coordinate, to_coordinate]) for to_coordinate in points] for
                 from_coordinate in points]

        return estimate_costs(paths, EstimationParameters(0, 5, 0))

    def place_bids(self, auction: Auction, solution_limit: int):
        last_round = auction.rounds[-2]
        # benefits after costs for bidding for them
        net_benefits = [self.tasks[i].value for i in range(
            last_round.item_count)]
        for i in range(last_round.item_count):
            last_highest_bid=last_round.get_highest_bid(i)
            if last_highest_bid.bidder_id is self.id:
                net_benefits[i] += auction.take_back_bid_cost(i)
            else:
                net_benefits[i] -= last_highest_bid.price
        net_benefits = [0, 0] + net_benefits
        # pprint(self.costs)
        # print(net_benefits)
        adoptedCosts=copy.deepcopy(self.costs)
        for i in range(last_round.item_count):
            if net_benefits[i] < 0:
                adoptedCosts[i]=[1000000000 for _ in range(last_round.item_count+2)]
        opt = Optimizer(adoptedCosts, LocalSearchMetaheuristic.SIMULATED_ANNEALING,
                        FirstSolutionStrategy.AUTOMATIC, solution_limit, False, net_benefits, self)
        # this still has start and end
        optimal_order = opt.optimize()

        # print(optimal_order)
        # for i in range(len(optimal_order) - 1):
        #     print(f"{optimal_order[i]} -> {optimal_order[i+1]} = {self.costs[optimal_order[i]][optimal_order[i+1]]}")
        
        # remove start and end from tasks
        task_order = [i-2 for i in optimal_order[1:-1]]
        # now claim tasks in route
        for task_index in task_order:
            last_highest_bid=last_round.get_highest_bid(task_index)
            if last_highest_bid.bidder_id is not self.id:
                auction.place_bid(task_index, Bid(self.id, last_highest_bid.price + 20*random()))
        for i in range(auction.item_count):
            bid_to_check = last_round.get_highest_bid(i)
            if bid_to_check.bidder_id is self.id and i not in task_order:
                auction.takeback_bid(i, bid_to_check)
        self.current_path = task_order
        print("Agent " + self.id + " chooses the path start ->", *[str(t)+" ->" for t in task_order],"end")
