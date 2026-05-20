"""Data models used by the ACO solver."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class City:
    """A point in the Euclidean TSP plane."""

    id: int
    x: float
    y: float
    label: str


@dataclass(frozen=True)
class ACOParameters:
    """Configuration for the Ant Colony Optimization algorithm."""

    num_ants: int
    alpha: float
    beta: float
    rho: float
    q: float
    iterations: int
    initial_pheromone: float = 0.1

    def validate(self, num_cities: int) -> None:
        """Raise ValueError when a parameter cannot produce a valid run."""

        if num_cities < 3:
            raise ValueError("El TSP necesita al menos 3 ciudades.")
        if self.num_ants < 1:
            raise ValueError("El numero de hormigas debe ser mayor o igual a 1.")
        if self.alpha < 0:
            raise ValueError("Alpha no puede ser negativo.")
        if self.beta < 0:
            raise ValueError("Beta no puede ser negativo.")
        if not 0 < self.rho < 1:
            raise ValueError("Rho debe estar entre 0 y 1.")
        if self.q <= 0:
            raise ValueError("Q debe ser mayor que 0.")
        if self.iterations < 1:
            raise ValueError("El numero de iteraciones debe ser mayor o igual a 1.")
        if self.initial_pheromone <= 0:
            raise ValueError("La feromona inicial debe ser mayor que 0.")


@dataclass(frozen=True)
class ACORunResult:
    """Complete output of one ACO execution."""

    cities: list[City]
    distances: np.ndarray
    pheromones: np.ndarray
    best_route: list[int]
    best_length: float
    best_history: list[float]
    iteration_best_lengths: list[float]
    iteration_average_lengths: list[float]
    parameters: ACOParameters

    @property
    def best_route_cycle(self) -> list[int]:
        """Return the best route with the origin repeated at the end."""

        if not self.best_route:
            return []
        return [*self.best_route, self.best_route[0]]
