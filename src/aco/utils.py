"""Utility functions for generating and evaluating TSP instances."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .models import City


def generate_cities(
    num_cities: int,
    seed: int,
    width: float = 100.0,
    height: float = 100.0,
) -> list[City]:
    """Generate reproducible Euclidean cities in a 2D plane."""

    if num_cities < 3:
        raise ValueError("Se requieren al menos 3 ciudades.")

    rng = np.random.default_rng(seed)
    points = rng.uniform([0.0, 0.0], [width, height], size=(num_cities, 2))

    return [
        City(id=index, x=float(x), y=float(y), label=f"C{index + 1}")
        for index, (x, y) in enumerate(points)
    ]


def generate_classroom_example_cities() -> list[City]:
    """Return the 5-city classroom TSP example with optimal tour length 14."""

    base_points = np.array(
        [
            [0.0, 2.0],
            [3.0, 4.0],
            [6.0, 2.0],
            [4.0, 0.0],
            [1.0, 0.0],
        ],
        dtype=float,
    )
    perimeter = float(
        sum(
            np.linalg.norm(current - next_point)
            for current, next_point in zip(base_points, [*base_points[1:], base_points[0]])
        )
    )
    scaled_points = base_points * (14.0 / perimeter) + np.array([2.0, 2.0])

    return [
        City(id=index, x=float(x), y=float(y), label=label)
        for index, (label, (x, y)) in enumerate(
            zip(["A", "B", "C", "D", "E"], scaled_points)
        )
    ]


def build_distance_matrix(cities: Sequence[City]) -> np.ndarray:
    """Build a symmetric Euclidean distance matrix."""

    coordinates = np.array([(city.x, city.y) for city in cities], dtype=float)
    deltas = coordinates[:, None, :] - coordinates[None, :, :]
    distances = np.linalg.norm(deltas, axis=2)
    np.fill_diagonal(distances, 0.0)
    return distances


def build_visibility_matrix(distances: np.ndarray) -> np.ndarray:
    """Return eta(i,j) = 1 / d(i,j), with zeros on the diagonal."""

    visibility = np.zeros_like(distances, dtype=float)
    np.divide(1.0, distances, out=visibility, where=distances > 0)
    np.fill_diagonal(visibility, 0.0)
    return visibility


def route_length(route: Sequence[int], distances: np.ndarray) -> float:
    """Compute the closed TSP tour length for a route permutation."""

    if len(route) == 0:
        return 0.0

    total = 0.0
    for current, next_city in zip(route, [*route[1:], route[0]]):
        total += float(distances[current, next_city])
    return total


def route_edges(route: Sequence[int]) -> list[tuple[int, int]]:
    """Return the undirected cycle edges used by a route."""

    if len(route) == 0:
        return []
    return [
        (int(current), int(next_city))
        for current, next_city in zip(route, [*route[1:], route[0]])
    ]
