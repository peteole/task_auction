from flask import Flask, jsonify, request, render_template

from auction.test_auction import run_auction
from flightcosts.cost_estimator import estimate_costs
from flightcosts.estimation_parameters import EstimationParameters
from flightpath.obstacle import Obstacle
from flightpath.path_planner import create_flight_path, create_flight_paths
from shared.geo.coordinate import Coordinate
from tsp.optimizer import Optimizer
from tsp.parameters import LocalSearchMetaheuristic, FirstSolutionStrategy
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)


@app.route("/flight_path", methods=['GET'])
def get_flight_path():
    """
    Input:
    {
        "start": {
            "latitude": 1.23,
            "longitude": 1.23,
        },
        "end": {
            "latitude": 1.23,
            "longitude": 1.23,
        },
        "obstacles": [
            {
                "coordinates": {
                    "latitude": 1.23,
                    "longitude": 1.23,
                }
            },
            {
                "coordinates": {
                    "latitude": 1.23,
                    "longitude": 1.23,
                }
            },
        ]
    }
    """
    # Parse input
    json_data = request.get_json()
    start = Coordinate.from_json(json_data['start'])
    end = Coordinate.from_json(json_data['end'])
    obstacles = [Obstacle.from_json(obstacle) for obstacle in json_data['obstacles']]

    # Create flight path
    flight_path = create_flight_path(start, end, obstacles)

    return jsonify(flight_path.to_json())


@app.route("/flight_costs", methods=['GET'])
def get_flight_costs():
    """
    Input:
    {
        "coordinates": [
            {
                "latitude": 1.23,
                "longitude": 1.23,
            },
            {
                "latitude": 1.23,
                "longitude": 1.23,
            }
        ],
        "obstacles": [
            {
                "coordinates": {
                    "latitude": 1.23,
                    "longitude": 1.23,
                }
            },
            {
                "coordinates": {
                    "latitude": 1.23,
                    "longitude": 1.23,
                }
            },
        ]
    }
    """
    # Parse input
    json_data = request.get_json()
    obstacles = [Obstacle.from_json(obstacle) for obstacle in json_data['obstacles']]
    coordinates = [Coordinate.from_json(coordinate) for coordinate in json_data['coordinates']]
    estimation_parameters = EstimationParameters.from_json(json_data['estimation_parameters'])

    # Create flight paths and estimate their costs
    flight_paths = create_flight_paths(coordinates, obstacles)
    costs = estimate_costs(flight_paths, estimation_parameters)

    return jsonify(costs)


@app.route("/solve_tsp", methods=['GET'])
def solve_tsp():
    # The first point is the depot
    """
    Input:
    {
        "costs": [
            [1, 2],
            [3, 4]
        ],
        "parameters" : {
            "local_search_metaheuristic": "GUIDED_LOCAL_SEARCH",
            "first_solution_strategy": "AUTOMATIC",
            "solution_limit": 100,
        }
    }
    """
    # Parse input
    json_data = request.get_json()
    local_search_metaheuristic = LocalSearchMetaheuristic[json_data['parameters']['local_search_metaheuristic']]
    first_solution_strategy = FirstSolutionStrategy[json_data['parameters']['first_solution_strategy']]

    # Create optimizer
    optimizer = Optimizer(json_data['costs'], local_search_metaheuristic.value, first_solution_strategy.value,
                          json_data['parameters']['solution_limit'], False)

    # Solve TSP
    optimal_order = optimizer.optimize()

    return jsonify(optimal_order)


@app.route("/", methods=['GET'])
def get_index():
    return render_template("index.html")


@app.route("/get_simulation_state", methods=['POST'])
def get_simulation_state():
    data = request.get_json()
    print(data)
    result=run_auction(data)
    print(result)
    return jsonify(result)
