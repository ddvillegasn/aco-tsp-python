"""Interactive Plotly figures used by the Streamlit interface."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import plotly.graph_objects as go

from src.aco.models import ACORunResult, City

NAVY = "#0f172a"
BLUE = "#2563eb"
AMBER = "#f59e0b"
EMERALD = "#10b981"
ROSE = "#e11d48"
SLATE = "#475569"
GRID = "#e2e8f0"


def _base_layout(fig: go.Figure, title: str, height: int = 520) -> go.Figure:
    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left"},
        height=height,
        margin={"l": 32, "r": 24, "t": 68, "b": 36},
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"family": "Inter, Segoe UI, Arial", "color": NAVY},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "x": 0.02},
    )
    return fig


def route_figure(result: ACORunResult) -> go.Figure:
    """Plot cities and the best TSP cycle found by ACO."""

    route = result.best_route_cycle
    city_map = {city.id: city for city in result.cities}
    route_x = [city_map[city_id].x for city_id in route]
    route_y = [city_map[city_id].y for city_id in route]
    labels = [city.label for city in result.cities]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=route_x,
            y=route_y,
            mode="lines",
            name="Mejor ruta",
            line={"color": AMBER, "width": 4},
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[city.x for city in result.cities],
            y=[city.y for city in result.cities],
            mode="markers+text",
            text=labels,
            textposition="top center",
            name="Ciudades",
            marker={
                "size": 13,
                "color": BLUE,
                "line": {"color": "white", "width": 2},
            },
            hovertemplate="<b>%{text}</b><br>x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>",
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False, title="Coordenada X")
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        title="Coordenada Y",
        scaleanchor="x",
        scaleratio=1,
    )
    return _base_layout(fig, "Mejor recorrido encontrado", height=560)


def convergence_figure(result: ACORunResult) -> go.Figure:
    """Show convergence of best, iteration-best and average tour lengths."""

    x_values = list(range(1, len(result.best_history) + 1))
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=result.best_history,
            mode="lines",
            name="Mejor acumulada",
            line={"color": EMERALD, "width": 4},
            hovertemplate="Iteracion %{x}<br>Mejor=%{y:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=result.iteration_best_lengths,
            mode="lines",
            name="Mejor de la iteracion",
            line={"color": AMBER, "width": 2},
            opacity=0.75,
            hovertemplate="Iteracion %{x}<br>Mejor local=%{y:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=result.iteration_average_lengths,
            mode="lines",
            name="Promedio",
            line={"color": SLATE, "width": 2, "dash": "dot"},
            opacity=0.7,
            hovertemplate="Iteracion %{x}<br>Promedio=%{y:.2f}<extra></extra>",
        )
    )
    fig.update_xaxes(title="Iteracion", showgrid=True, gridcolor=GRID)
    fig.update_yaxes(title="Longitud del recorrido", showgrid=True, gridcolor=GRID)
    return _base_layout(fig, "Convergencia del algoritmo", height=420)


def pheromone_network_figure(result: ACORunResult, max_edges: int = 35) -> go.Figure:
    """Visualize the strongest pheromone trails as a weighted network."""

    strongest_edges = _top_pheromone_edges(result.pheromones, max_edges=max_edges)
    city_map = {city.id: city for city in result.cities}
    pheromone_values = [value for _, _, value in strongest_edges]
    max_pheromone = max(pheromone_values, default=1.0)

    fig = go.Figure()
    for start, end, value in strongest_edges:
        start_city = city_map[start]
        end_city = city_map[end]
        width = 1.0 + 6.0 * (value / max_pheromone)
        fig.add_trace(
            go.Scatter(
                x=[start_city.x, end_city.x],
                y=[start_city.y, end_city.y],
                mode="lines",
                showlegend=False,
                line={"color": f"rgba(245, 158, 11, {0.18 + 0.58 * value / max_pheromone})", "width": width},
                hovertemplate=(
                    f"{start_city.label} - {end_city.label}<br>"
                    f"Feromona={value:.4f}<extra></extra>"
                ),
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[city.x for city in result.cities],
            y=[city.y for city in result.cities],
            mode="markers+text",
            text=[city.label for city in result.cities],
            textposition="top center",
            name="Ciudades",
            marker={
                "size": 12,
                "color": NAVY,
                "line": {"color": "white", "width": 2},
            },
            hovertemplate="<b>%{text}</b><br>x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>",
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False, title="Coordenada X")
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        title="Coordenada Y",
        scaleanchor="x",
        scaleratio=1,
    )
    return _base_layout(fig, "Rastros de feromona mas fuertes", height=500)


def pheromone_heatmap_figure(result: ACORunResult) -> go.Figure:
    """Display the pheromone matrix as a heatmap."""

    labels = [city.label for city in result.cities]
    fig = go.Figure(
        data=go.Heatmap(
            z=result.pheromones,
            x=labels,
            y=labels,
            colorscale=[
                [0.0, "#f8fafc"],
                [0.35, "#fde68a"],
                [0.75, "#f59e0b"],
                [1.0, "#92400e"],
            ],
            colorbar={"title": "Tau"},
            hovertemplate="%{y} -> %{x}<br>Feromona=%{z:.4f}<extra></extra>",
        )
    )
    fig.update_xaxes(title="Ciudad destino")
    fig.update_yaxes(title="Ciudad origen", autorange="reversed")
    return _base_layout(fig, "Matriz de feromonas", height=500)


def colony_flow_figure() -> go.Figure:
    """Create a visual summary of the biological inspiration."""

    stages = [
        ("Exploracion", "Las hormigas prueban caminos"),
        ("Feromonas", "Cada ruta deja una senal"),
        ("Seguimiento", "La colonia prefiere rastros fuertes"),
        ("Convergencia", "Las rutas cortas se refuerzan"),
    ]
    x_values = [0.08, 0.36, 0.64, 0.92]
    y_values = [0.5] * len(stages)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            line={"color": GRID, "width": 10},
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="markers+text",
            text=[title for title, _ in stages],
            textposition="top center",
            marker={
                "size": [38, 42, 42, 46],
                "color": [SLATE, AMBER, BLUE, EMERALD],
                "line": {"color": "white", "width": 3},
            },
            hovertemplate="<b>%{text}</b><extra></extra>",
            showlegend=False,
        )
    )

    for x_value, (title, subtitle) in zip(x_values, stages):
        fig.add_annotation(
            x=x_value,
            y=0.28,
            text=f"<b>{title}</b><br>{subtitle}",
            showarrow=False,
            align="center",
            font={"size": 13, "color": NAVY},
        )

    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False, range=[0, 1])
    return _base_layout(fig, "Inspiracion biologica convertida en algoritmo", height=280)


def _top_pheromone_edges(
    pheromones: np.ndarray,
    max_edges: int,
) -> list[tuple[int, int, float]]:
    edges: list[tuple[int, int, float]] = []
    size = pheromones.shape[0]
    for i in range(size):
        for j in range(i + 1, size):
            edges.append((i, j, float(pheromones[i, j])))
    edges.sort(key=lambda item: item[2], reverse=True)
    return edges[:max_edges]
