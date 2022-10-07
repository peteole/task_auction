from typing import List, Tuple

from utm import latlon_to_zone_number, from_latlon, to_latlon, latitude_to_zone_letter

from shared.geo.coordinate import Coordinate, UTMCoordinate


def latlon_to_utm(coordinates: List[Coordinate]) -> Tuple[List[UTMCoordinate], Coordinate]:
    # Convert latlon coordinates to UTM coordinates
    utm_zone_number = latlon_to_zone_number(coordinates[0].latitude, coordinates[0].longitude)

    utm_coordinates = []
    for coordinate in coordinates:
        east, north, *_ = from_latlon(coordinate.latitude, coordinate.longitude, force_zone_number=utm_zone_number)
        utm_coordinates.append(UTMCoordinate(north, east))

    return utm_coordinates, coordinates[0]


def utm_to_latlon(coordinates: List[UTMCoordinate], reference_coordinate: Coordinate) -> List[Coordinate]:
    # Convert UTM coordinates to latlon coordinates. A reference latlon coordinate must be supplied.
    # To learn why, read about UTM zones :)
    zone_number = latlon_to_zone_number(reference_coordinate.latitude, reference_coordinate.longitude)
    zone_letter = latitude_to_zone_letter(reference_coordinate.latitude)

    latlon_coordinates = []
    for coordinate in coordinates:
        latitude, longitude = to_latlon(coordinate.east, coordinate.north, zone_number, zone_letter)
        latlon_coordinates.append(Coordinate(latitude, longitude))

    return latlon_coordinates
