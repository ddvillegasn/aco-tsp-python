"""Spanish educational content for the ACO presentation app."""

from __future__ import annotations

PARAMETER_TABLE = [
    {
        "Parametro": "alpha",
        "Rango tipico": "0.5 - 2",
        "Efecto": "Mayor alpha aumenta la influencia de las feromonas pasadas.",
    },
    {
        "Parametro": "beta",
        "Rango tipico": "2 - 5",
        "Efecto": "Mayor beta da mas peso a la distancia y a la informacion local.",
    },
    {
        "Parametro": "rho",
        "Rango tipico": "0.1 - 0.5",
        "Efecto": "Controla evaporacion: alto explora mas; bajo conserva memoria.",
    },
    {
        "Parametro": "m",
        "Rango tipico": "n - 3n",
        "Efecto": "Mas hormigas exploran mejor, con mayor costo por iteracion.",
    },
    {
        "Parametro": "Q",
        "Rango tipico": "1 - 100",
        "Efecto": "Define cuanta feromona deposita una ruta segun Q / L.",
    },
    {
        "Parametro": "t_max",
        "Rango tipico": "50 - 1000",
        "Efecto": "Cantidad maxima de ciclos de construccion y actualizacion.",
    },
]

BIOLOGY_CARDS = [
    {
        "title": "Exploracion",
        "body": "Las hormigas salen del nido y prueban rutas sin conocer el mapa completo.",
    },
    {
        "title": "Feromonas",
        "body": "Al regresar con alimento, dejan rastros quimicos sobre el camino recorrido.",
    },
    {
        "title": "Seguimiento",
        "body": "Otras hormigas tienden a elegir caminos con mayor concentracion de feromona.",
    },
    {
        "title": "Convergencia",
        "body": "Los caminos cortos se recorren mas veces y acumulan mas senal colectiva.",
    },
]

ALGORITHM_STEPS = [
    (
        "1. Inicializacion",
        "Se define el grafo de ciudades, el numero de hormigas y los parametros alpha, beta, rho, Q e iteraciones. Todas las aristas empiezan con una feromona inicial.",
    ),
    (
        "2. Construccion de soluciones",
        "Cada hormiga parte de una ciudad y construye un recorrido completo eligiendo probabilisticamente la siguiente ciudad no visitada.",
    ),
    (
        "3. Evaluacion",
        "Se calcula la longitud de cada recorrido, incluyendo el regreso a la ciudad inicial.",
    ),
    (
        "4. Actualizacion de feromonas",
        "Primero se evapora una parte del rastro anterior. Luego las mejores rutas depositan feromona proporcional a Q / L.",
    ),
    (
        "5. Criterio de parada",
        "El ciclo se repite hasta completar las iteraciones. Se conserva la mejor solucion global encontrada.",
    ),
]

FORMULAS = [
    ("Visibilidad", r"\eta_{ij} = \frac{1}{d_{ij}}"),
    (
        "Probabilidad de transicion",
        r"p_{ij} = \frac{\tau_{ij}^{\alpha}\eta_{ij}^{\beta}}{\sum_{l \in N_i}\tau_{il}^{\alpha}\eta_{il}^{\beta}}",
    ),
    (
        "Evaporacion y refuerzo",
        r"\tau_{ij}(t+1) = (1-\rho)\tau_{ij}(t) + \Delta\tau_{ij}",
    ),
    ("Deposito de feromona", r"\Delta\tau_{ij}^{k} = \frac{Q}{L^k}"),
]

ADVANTAGES = [
    "Robusto para problemas de grafos, redes y rutas.",
    "Combina exploracion aleatoria con memoria colectiva.",
    "Encuentra soluciones cercanas al optimo en tiempos razonables.",
    "Se adapta a cambios del problema y puede recalcular rutas.",
    "Las hormigas pueden ejecutarse en paralelo.",
]

LIMITATIONS = [
    "Puede converger prematuramente a optimos locales.",
    "Es sensible a la calibracion de alpha, beta y rho.",
    "Puede ser costoso en instancias muy grandes.",
    "No garantiza encontrar el optimo global.",
    "Su aplicacion a problemas continuos requiere adaptaciones.",
]

APPLICATIONS = [
    {
        "title": "Logistica y rutas",
        "body": "Optimizacion de reparto, TSP, VRP y planeacion de recorridos.",
    },
    {
        "title": "Telecomunicaciones",
        "body": "Enrutamiento dinamico de paquetes y adaptacion a congestion de red.",
    },
    {
        "title": "Diseno de circuitos",
        "body": "Ubicacion de componentes y reduccion de longitud de interconexion.",
    },
    {
        "title": "Scheduling",
        "body": "Programacion de trabajos, turnos, recursos y horarios academicos.",
    },
]

CONCLUSIONS = [
    "ACO transforma un comportamiento biologico simple en una estrategia poderosa para optimizacion combinatoria.",
    "La feromona funciona como memoria distribuida: no hay un controlador central, pero emerge una decision colectiva.",
    "El equilibrio entre exploracion y explotacion depende principalmente de alpha, beta y rho.",
    "El TSP permite ver de forma clara como el algoritmo construye, evalua y mejora soluciones iterativamente.",
]

REFERENCES = [
    "Dorigo, M. & Stutzle, T. (2004). Ant Colony Optimization. MIT Press.",
    "Dorigo, M. (1992). Optimization, Learning and Natural Algorithms. Ph.D. Thesis.",
    "Colorni, A., Dorigo, M. & Maniezzo, V. (1991). Distributed Optimization by Ant Colonies.",
    "Dorigo, M. & Blum, C. (2005). Ant Colony Optimization Theory: A Survey.",
]
