from typing import List

from flightpath.flight_path import FlightPath
from flightpath.obstacle import Obstacle
from shared.geo.coordinate import Coordinate, UTMCoordinate
from shared.id_creator import create_id
from pyvisgraph import VisGraph, Point
from shared.geo.converter import latlon_to_utm, utm_to_latlon


def create_flight_path(start: Coordinate, end: Coordinate, obstacles: List[Obstacle],
                       visgraph: VisGraph = None, reference_coordinate: Coordinate = None) -> FlightPath:
    """Create flight path from start to end which avoids obstacles"""

    flight_path_id = create_id()

    # if visgraph is None:
    #     # build pyvisgraph
    #     vg = VisGraph()
    #     if len(obstacles) > 0:
    #         polys, reference_coordinate = obstacle_list_to_pyvisgraph_polys(obstacles)
    #         vg.build(polys)

    # # get List[pyvisgraph.Point] which is shortest path
    # shortest_pyvisgraph_path = visgraph.shortest_path(coordinate_to_pyvisgraph_point(start),
    #                                                   coordinate_to_pyvisgraph_point(end))
    # shortest = pyvisgraph_path_to_coordinate_list(
    #     shortest_pyvisgraph_path, reference_coordinate)

    return FlightPath(flight_path_id, start, end, [start, end])


def coordinate_to_pyvisgraph_point(crd: Coordinate) -> Point:
    utm_coordinate = latlon_to_utm([crd])[0][0]
    return Point(utm_coordinate.east, utm_coordinate.north)


def obstacle_list_to_pyvisgraph_polys(obstacles: List[Obstacle]) -> (List[List[Point]], UTMCoordinate):
    # Convert List[Obstacle] to List[List[pyvisgraph.Point]]
    assert len(obstacles) > 0, "obstacle_list_to_pyvisgraph_polys: do not call this method with empty list"

    reference = latlon_to_utm(obstacles[0].coordinates)[1]

    polys = []
    for obs in obstacles:
        utm_coordinates = latlon_to_utm(obs.coordinates)
        obs_poly = [Point(crd.east, crd.north) for crd in utm_coordinates[0]]
        polys.append(obs_poly)

    return polys, reference


def pyvisgraph_path_to_coordinate_list(path: List[Point], ref: Coordinate) -> List[Coordinate]:
    # Convert List[pyvisgraph.Point] to List[Coordinate]
    utm_coordinates = [UTMCoordinate(point.y, point.x) for point in path]
    return utm_to_latlon(utm_coordinates, ref)


def create_flight_paths(coordinates: List[Coordinate], obstacles: List[Obstacle]) -> List[List[FlightPath]]:
    # Create a square matrix of flight paths between all pairs of coordinates. Flight paths avoid obstacles
    paths = []

    # build pyvisgraph
    #vg = VisGraph()
    # polys, reference_coordinate = obstacle_list_to_pyvisgraph_polys(obstacles)
    # vg.build(polys)

    for coordinate_from in coordinates:
        paths.append([])
        for coordinate_to in coordinates:
            if len(obstacles) == 0:
                flight_path_id = create_id()
                paths[-1].append(
                    FlightPath(flight_path_id, coordinate_from, coordinate_to, [coordinate_from, coordinate_to]))

            paths[-1].append(create_flight_path(coordinate_from, coordinate_to, obstacles, None, coordinates[0]))

    return paths
