"""Streamlit application for an Ant Colony Optimization TSP project."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.aco import (
    ACOParameters,
    AntColonyOptimizer,
    generate_cities,
    generate_classroom_example_cities,
)
from src.aco.models import ACORunResult
from src.content.educational import (
    ADVANTAGES,
    ALGORITHM_STEPS,
    APPLICATIONS,
    BIOLOGY_CARDS,
    CONCLUSIONS,
    FORMULAS,
    LIMITATIONS,
    PARAMETER_TABLE,
    REFERENCES,
)
from src.visualization import (
    colony_flow_figure,
    convergence_figure,
    pheromone_heatmap_figure,
    pheromone_network_figure,
    route_figure,
)


st.set_page_config(
    page_title="ACO para TSP | Investigacion de Operaciones",
    layout="wide",
    initial_sidebar_state="expanded",
)

PLOTLY_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}


def inject_css() -> None:
    """Apply a polished academic visual style."""

    st.markdown(
        """
        <style>
        :root {
            --navy: #0f172a;
            --blue: #2563eb;
            --amber: #f59e0b;
            --emerald: #10b981;
            --rose: #e11d48;
            --slate: #475569;
            --muted: #64748b;
            --line: #e2e8f0;
            --soft: #f8fafc;
        }

        .stApp {
            background: #f8fafc;
            color: var(--navy);
        }

        [data-testid="stSidebar"] {
            background: #0f172a;
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        [data-testid="stSidebar"] .stSlider div[data-baseweb="slider"] div {
            color: var(--amber);
        }

        .main .block-container {
            padding-top: 1.4rem;
            max-width: 1440px;
        }

        .top-band {
            border: 1px solid var(--line);
            background: white;
            border-radius: 8px;
            padding: 1.25rem 1.35rem;
            margin-bottom: 1rem;
        }

        .eyebrow {
            color: var(--amber);
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }

        .title {
            color: var(--navy);
            font-size: 2.15rem;
            font-weight: 850;
            line-height: 1.08;
            margin: 0;
        }

        .subtitle {
            color: var(--slate);
            max-width: 980px;
            font-size: 1.02rem;
            line-height: 1.55;
            margin-top: 0.55rem;
        }

        .author-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 0.85rem;
        }

        .pill {
            border: 1px solid var(--line);
            color: var(--slate);
            background: var(--soft);
            border-radius: 999px;
            padding: 0.35rem 0.7rem;
            font-weight: 650;
            font-size: 0.84rem;
        }

        .metric-card {
            border: 1px solid var(--line);
            background: white;
            border-radius: 8px;
            padding: 1rem;
            min-height: 104px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 750;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--navy);
            font-size: 1.55rem;
            font-weight: 850;
            margin-top: 0.35rem;
        }

        .metric-help {
            color: var(--muted);
            font-size: 0.82rem;
            margin-top: 0.2rem;
        }

        .info-card {
            border: 1px solid var(--line);
            background: white;
            border-radius: 8px;
            padding: 1rem;
            height: 100%;
        }

        .info-card h3 {
            color: var(--navy);
            font-size: 1rem;
            margin: 0 0 0.35rem 0;
        }

        .info-card p, .info-card li {
            color: var(--slate);
            font-size: 0.94rem;
            line-height: 1.5;
        }

        .accent-line {
            height: 4px;
            width: 54px;
            background: var(--amber);
            border-radius: 999px;
            margin-bottom: 0.65rem;
        }

        .section-note {
            color: var(--slate);
            font-size: 0.96rem;
            line-height: 1.55;
            margin-bottom: 0.85rem;
        }

        .formula-card {
            border: 1px solid var(--line);
            border-left: 4px solid var(--amber);
            background: white;
            border-radius: 8px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.7rem;
        }

        div[data-testid="stMetric"] {
            border: 1px solid var(--line);
            background: white;
            border-radius: 8px;
            padding: 0.85rem 1rem;
        }

        div[data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        div[data-testid="stTabs"] button {
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def run_simulation(
    instance_mode: str,
    num_cities: int,
    num_ants: int,
    alpha: float,
    beta: float,
    rho: float,
    q: float,
    iterations: int,
    seed: int,
    initial_pheromone: float,
) -> ACORunResult:
    """Generate a TSP instance and solve it with ACO."""

    if instance_mode == "classroom":
        cities = generate_classroom_example_cities()
    else:
        cities = generate_cities(num_cities=num_cities, seed=seed)

    parameters = ACOParameters(
        num_ants=num_ants,
        alpha=alpha,
        beta=beta,
        rho=rho,
        q=q,
        iterations=iterations,
        initial_pheromone=initial_pheromone,
    )
    solver = AntColonyOptimizer(cities=cities, parameters=parameters, seed=seed + 10_003)
    return solver.solve()


def main() -> None:
    inject_css()

    controls = render_sidebar()

    with st.spinner("Ejecutando la colonia de hormigas..."):
        result = run_simulation(**controls)

    render_header()
    render_metrics(result)
    render_tabs(result)


def render_sidebar() -> dict[str, int | float | str]:
    st.sidebar.header("Parametros ACO")
    st.sidebar.caption("Ajusta el experimento y observa como cambia la ruta.")

    instance_label = st.sidebar.selectbox(
        "Instancia TSP",
        ["Ejemplo de clase A-E", "Ciudades aleatorias"],
        index=0,
    )
    instance_mode = "classroom" if instance_label.startswith("Ejemplo") else "random"

    if instance_mode == "classroom":
        st.sidebar.info("Caso fijo: A -> B -> C -> D -> E -> A tiene longitud esperada 14.00.")
        num_cities = 5
    else:
        num_cities = st.sidebar.slider("Numero de ciudades", 5, 40, 18, 1)

    seed = st.sidebar.number_input("Semilla aleatoria", min_value=0, max_value=9999, value=425, step=1)
    default_ants = 20 if instance_mode == "classroom" else max(20, num_cities)
    num_ants = st.sidebar.slider("Numero de hormigas", 1, 120, default_ants, 1)

    st.sidebar.divider()
    alpha = st.sidebar.slider("Alpha: influencia de feromonas", 0.0, 4.0, 1.0, 0.1)
    beta = st.sidebar.slider("Beta: influencia de distancia", 0.0, 8.0, 3.0, 0.1)
    rho = st.sidebar.slider("Rho: evaporacion", 0.01, 0.90, 0.25, 0.01)
    q = st.sidebar.slider("Q: refuerzo de feromona", 1.0, 200.0, 80.0, 1.0)
    iterations = st.sidebar.slider("Iteraciones maximas", 20, 500, 150, 10)

    with st.sidebar.expander("Opciones avanzadas"):
        initial_pheromone = st.slider("Feromona inicial", 0.01, 1.00, 0.10, 0.01)
        st.caption("Complejidad aproximada: O(t_max * m * n^2).")

    return {
        "instance_mode": instance_mode,
        "num_cities": int(num_cities),
        "num_ants": int(num_ants),
        "alpha": float(alpha),
        "beta": float(beta),
        "rho": float(rho),
        "q": float(q),
        "iterations": int(iterations),
        "seed": int(seed),
        "initial_pheromone": float(initial_pheromone),
    }


def render_header() -> None:
    st.markdown(
        """
        <div class="top-band">
            <div class="eyebrow">Investigacion de Operaciones | Proyecto final</div>
            <h1 class="title">Algoritmo Colonia de Hormigas aplicado al TSP</h1>
            <div class="subtitle">
                Simulador interactivo de Ant Colony Optimization: las hormigas construyen rutas,
                refuerzan caminos con feromonas y convergen hacia recorridos cada vez mas cortos.
            </div>
            <div class="author-row">
                <span class="pill">Valentina Rosas</span>
                <span class="pill">Cesar Villegas</span>
                <span class="pill">ACO · Ant Colony Optimization</span>
                <span class="pill">Mayo 2025</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics(result: ACORunResult) -> None:
    improvement = (
        result.iteration_average_lengths[0] - result.best_length
        if result.iteration_average_lengths
        else 0.0
    )
    improvement_percent = improvement / result.iteration_average_lengths[0] * 100 if improvement > 0 else 0.0

    columns = st.columns(4)
    columns[0].metric("Mejor distancia", f"{result.best_length:,.2f}")
    columns[1].metric("Ciudades", len(result.cities))
    columns[2].metric("Hormigas", result.parameters.num_ants)
    columns[3].metric("Mejora estimada", f"{improvement_percent:,.1f}%")


def render_tabs(result: ACORunResult) -> None:
    tab_simulator, tab_pheromones, tab_learning, tab_parameters, tab_analysis, tab_refs = st.tabs(
        [
            "Simulador",
            "Feromonas",
            "ACO paso a paso",
            "Parametros",
            "Analisis",
            "Referencias",
        ]
    )

    with tab_simulator:
        render_simulator_tab(result)
    with tab_pheromones:
        render_pheromones_tab(result)
    with tab_learning:
        render_learning_tab()
    with tab_parameters:
        render_parameters_tab()
    with tab_analysis:
        render_analysis_tab()
    with tab_refs:
        render_references_tab()


def render_simulator_tab(result: ACORunResult) -> None:
    left, right = st.columns([1.35, 1.0], gap="large")
    with left:
        st.plotly_chart(route_figure(result), use_container_width=True, config=PLOTLY_CONFIG)
    with right:
        st.plotly_chart(convergence_figure(result), use_container_width=True, config=PLOTLY_CONFIG)
        st.markdown("**Ruta encontrada**")
        route_text = " -> ".join(result.cities[city_id].label for city_id in display_route_cycle(result))
        st.code(route_text, language="text")

        if [city.label for city in result.cities] == ["A", "B", "C", "D", "E"]:
            st.success(
                "Para este ejemplo, una ruta optima esperada es A -> B -> C -> D -> E -> A "
                "con longitud 14.00. Si aparece invertida o rotada, es la misma solucion TSP."
            )

    st.markdown(
        """
        <div class="info-card">
            <div class="accent-line"></div>
            <h3>Lectura de la simulacion</h3>
            <p>
                Cada hormiga crea un recorrido completo. Las rutas mas cortas depositan mas feromona,
                mientras la evaporacion reduce rastros antiguos. La grafica de convergencia muestra
                como la mejor distancia acumulada se estabiliza con las iteraciones.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pheromones_tab(result: ACORunResult) -> None:
    st.markdown(
        """
        <div class="section-note">
            La feromona es la memoria colectiva del algoritmo. Las lineas mas gruesas representan
            aristas que fueron reforzadas con mayor frecuencia por recorridos competitivos.
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.05, 1.0], gap="large")
    with left:
        st.plotly_chart(pheromone_network_figure(result), use_container_width=True, config=PLOTLY_CONFIG)
    with right:
        st.plotly_chart(pheromone_heatmap_figure(result), use_container_width=True, config=PLOTLY_CONFIG)


def render_learning_tab() -> None:
    st.plotly_chart(colony_flow_figure(), use_container_width=True, config=PLOTLY_CONFIG)

    st.subheader("Inspiracion biologica")
    columns = st.columns(4)
    for column, card in zip(columns, BIOLOGY_CARDS):
        column.markdown(
            f"""
            <div class="info-card">
                <div class="accent-line"></div>
                <h3>{card["title"]}</h3>
                <p>{card["body"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Pasos del algoritmo")
    for title, body in ALGORITHM_STEPS:
        st.markdown(
            f"""
            <div class="info-card">
                <h3>{title}</h3>
                <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Formulas clave")
    formula_columns = st.columns(2)
    for index, (title, formula) in enumerate(FORMULAS):
        with formula_columns[index % 2]:
            st.markdown(f'<div class="formula-card"><b>{title}</b></div>', unsafe_allow_html=True)
            st.latex(formula)


def render_parameters_tab() -> None:
    st.markdown(
        """
        <div class="section-note">
            La calidad del ACO depende del balance entre exploracion y explotacion. Un buen ajuste
            permite buscar rutas nuevas sin perder la memoria de las rutas prometedoras.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(pd.DataFrame(PARAMETER_TABLE), use_container_width=True, hide_index=True)

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown(
            """
            <div class="info-card">
                <div class="accent-line"></div>
                <h3>Exploracion</h3>
                <p>
                    Aumenta cuando rho es alto, alpha es bajo o hay mas aleatoriedad en la eleccion.
                    Ayuda a escapar de optimos locales y descubrir rutas diferentes.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
            <div class="info-card">
                <div class="accent-line"></div>
                <h3>Explotacion</h3>
                <p>
                    Aumenta cuando alpha o beta son altos. El algoritmo aprovecha rutas con buena
                    feromona o ciudades cercanas, acelerando la convergencia.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_analysis_tab() -> None:
    left, right = st.columns(2, gap="large")
    with left:
        render_list_card("Ventajas", ADVANTAGES)
    with right:
        render_list_card("Limitaciones", LIMITATIONS)

    st.subheader("Aplicaciones reales")
    columns = st.columns(4)
    for column, item in zip(columns, APPLICATIONS):
        column.markdown(
            f"""
            <div class="info-card">
                <div class="accent-line"></div>
                <h3>{item["title"]}</h3>
                <p>{item["body"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Conclusiones")
    render_list_card("Ideas principales", CONCLUSIONS)


def render_references_tab() -> None:
    st.markdown(
        """
        <div class="info-card">
            <div class="accent-line"></div>
            <h3>Base teorica</h3>
            <p>
                Marco Dorigo formalizo el Ant System en 1992. Desde entonces, ACO se ha consolidado
                como una metaheuristica de Inteligencia de Enjambre para problemas de optimizacion
                combinatoria como TSP, VRP, QAP y scheduling.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    for reference in REFERENCES:
        st.markdown(f"- {reference}")


def render_list_card(title: str, items: list[str]) -> None:
    list_items = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(
        f"""
        <div class="info-card">
            <div class="accent-line"></div>
            <h3>{title}</h3>
            <ul>{list_items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_route_cycle(result: ACORunResult) -> list[int]:
    """Rotate and orient a cycle for readable display without changing the solution."""

    if not result.best_route:
        return []

    route = list(result.best_route)
    origin = 0 if 0 in route else route[0]
    origin_index = route.index(origin)
    rotated = route[origin_index:] + route[:origin_index]
    reversed_rotated = [rotated[0], *reversed(rotated[1:])]
    selected = min(rotated, reversed_rotated)
    return [*selected, selected[0]]


if __name__ == "__main__":
    main()
