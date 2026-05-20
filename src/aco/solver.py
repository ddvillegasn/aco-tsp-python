"""Ant Colony Optimization solver for the Travelling Salesman Problem."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .models import ACOParameters, ACORunResult, City
from .utils import build_distance_matrix, build_visibility_matrix, route_length


class AntColonyOptimizer:
    """Solve a Euclidean TSP instance with Ant Colony Optimization."""

    def __init__(
        self,
        cities: Sequence[City],
        parameters: ACOParameters,
        seed: int | None = None,
    ) -> None:
        self.cities = list(cities)
        self.parameters = parameters
        self.parameters.validate(num_cities=len(self.cities))
        self.rng = np.random.default_rng(seed)
        self.distances = build_distance_matrix(self.cities)
        self.visibility = build_visibility_matrix(self.distances)
        self.pheromones = np.full(
            self.distances.shape,
            fill_value=self.parameters.initial_pheromone,
            dtype=float,
        )
        np.fill_diagonal(self.pheromones, 0.0)

    def solve(self) -> ACORunResult:
        """Run the optimizer and return the best tour found."""

        best_route: list[int] = []
        best_length = float("inf")
        best_history: list[float] = []
        iteration_best_lengths: list[float] = []
        iteration_average_lengths: list[float] = []

        for _ in range(self.parameters.iterations):
            routes = [self._construct_route() for _ in range(self.parameters.num_ants)]
            lengths = [route_length(route, self.distances) for route in routes]

            iteration_best_index = int(np.argmin(lengths))
            iteration_best_route = routes[iteration_best_index]
            iteration_best_length = float(lengths[iteration_best_index])

            if iteration_best_length < best_length:
                best_route = list(iteration_best_route)
                best_length = iteration_best_length

            self._update_pheromones(routes, lengths)

            best_history.append(best_length)
            iteration_best_lengths.append(iteration_best_length)
            iteration_average_lengths.append(float(np.mean(lengths)))

        return ACORunResult(
            cities=self.cities,
            distances=self.distances.copy(),
            pheromones=self.pheromones.copy(),
            best_route=best_route,
            best_length=best_length,
            best_history=best_history,
            iteration_best_lengths=iteration_best_lengths,
            iteration_average_lengths=iteration_average_lengths,
            parameters=self.parameters,
        )

    def _construct_route(self) -> list[int]:
        """Build one complete route with the probabilistic transition rule."""

        num_cities = len(self.cities)
        start = int(self.rng.integers(0, num_cities))
        route = [start]
        unvisited = set(range(num_cities))
        unvisited.remove(start)

        while unvisited:
            current = route[-1]
            next_city = self._choose_next_city(current, sorted(unvisited))
            route.append(next_city)
            unvisited.remove(next_city)

        return route

    def _choose_next_city(self, current: int, candidates: list[int]) -> int:
        """Choose the next city using pheromone and visibility weights."""

        pheromone = self.pheromones[current, candidates] ** self.parameters.alpha
        visibility = self.visibility[current, candidates] ** self.parameters.beta
        weights = pheromone * visibility
        total_weight = float(np.sum(weights))

        if total_weight <= 0 or not np.isfinite(total_weight):
            return int(self.rng.choice(candidates))

        probabilities = weights / total_weight
        return int(self.rng.choice(candidates, p=probabilities))

    def _update_pheromones(
        self,
        routes: Sequence[Sequence[int]],
        lengths: Sequence[float],
    ) -> None:
        """Apply evaporation and reinforcement to the pheromone matrix."""

        self.pheromones *= 1.0 - self.parameters.rho

        for route, length in zip(routes, lengths):
            if length <= 0:
                continue
            deposit = self.parameters.q / float(length)
            for current, next_city in zip(route, [*route[1:], route[0]]):
                self.pheromones[current, next_city] += deposit
                self.pheromones[next_city, current] += deposit

        np.fill_diagonal(self.pheromones, 0.0)
