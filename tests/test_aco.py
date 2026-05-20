from __future__ import annotations

import numpy as np

from src.aco import ACOParameters, AntColonyOptimizer
from src.aco.models import City
from src.aco.utils import (
    build_distance_matrix,
    generate_cities,
    generate_classroom_example_cities,
    route_length,
)


def test_distance_matrix_is_symmetric_and_euclidean() -> None:
    cities = [
        City(id=0, x=0.0, y=0.0, label="C1"),
        City(id=1, x=3.0, y=4.0, label="C2"),
        City(id=2, x=6.0, y=8.0, label="C3"),
    ]

    distances = build_distance_matrix(cities)

    assert distances.shape == (3, 3)
    assert np.allclose(distances, distances.T)
    assert np.allclose(np.diag(distances), 0.0)
    assert distances[0, 1] == 5.0
    assert distances[1, 2] == 5.0


def test_route_length_closes_the_cycle() -> None:
    cities = [
        City(id=0, x=0.0, y=0.0, label="C1"),
        City(id=1, x=1.0, y=0.0, label="C2"),
        City(id=2, x=0.0, y=1.0, label="C3"),
    ]
    distances = build_distance_matrix(cities)

    length = route_length([0, 1, 2], distances)

    assert np.isclose(length, 1.0 + np.sqrt(2.0) + 1.0)


def test_solver_returns_valid_tsp_cycle() -> None:
    cities = generate_cities(num_cities=10, seed=7)
    parameters = ACOParameters(
        num_ants=12,
        alpha=1.0,
        beta=3.0,
        rho=0.25,
        q=80.0,
        iterations=25,
    )

    result = AntColonyOptimizer(cities, parameters, seed=99).solve()

    assert len(result.best_route) == len(cities)
    assert sorted(result.best_route) == list(range(len(cities)))
    assert result.best_route_cycle[0] == result.best_route_cycle[-1]
    assert len(result.best_route_cycle) == len(cities) + 1
    assert result.best_length > 0


def test_pheromone_matrix_is_updated_and_symmetric() -> None:
    cities = generate_cities(num_cities=8, seed=15)
    parameters = ACOParameters(
        num_ants=8,
        alpha=1.0,
        beta=2.5,
        rho=0.2,
        q=60.0,
        iterations=5,
    )
    solver = AntColonyOptimizer(cities, parameters, seed=21)
    initial_pheromones = solver.pheromones.copy()

    result = solver.solve()

    assert not np.allclose(result.pheromones, initial_pheromones)
    assert np.allclose(result.pheromones, result.pheromones.T)
    assert np.allclose(np.diag(result.pheromones), 0.0)


def test_best_history_is_monotonic_non_increasing() -> None:
    cities = generate_cities(num_cities=9, seed=23)
    parameters = ACOParameters(
        num_ants=10,
        alpha=1.0,
        beta=3.0,
        rho=0.3,
        q=90.0,
        iterations=30,
    )

    result = AntColonyOptimizer(cities, parameters, seed=24).solve()

    assert len(result.best_history) == parameters.iterations
    assert all(
        later <= earlier
        for earlier, later in zip(result.best_history, result.best_history[1:])
    )


def test_classroom_example_has_expected_route_length() -> None:
    cities = generate_classroom_example_cities()
    distances = build_distance_matrix(cities)

    assert [city.label for city in cities] == ["A", "B", "C", "D", "E"]
    assert np.isclose(route_length([0, 1, 2, 3, 4], distances), 14.0)
