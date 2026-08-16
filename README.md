# ACO TSP Python

[![tests](https://github.com/ddvillegasn/aco-tsp-python/actions/workflows/tests.yml/badge.svg)](https://github.com/ddvillegasn/aco-tsp-python/actions/workflows/tests.yml)

Proyecto final de Investigacion de Operaciones sobre el algoritmo Colonia de Hormigas, ACO
(*Ant Colony Optimization*), aplicado al Problema del Viajero de Comercio, TSP.

La aplicacion permite generar ciudades aleatorias, modificar parametros del algoritmo y observar
como una colonia artificial construye rutas, actualiza feromonas y converge hacia una solucion de
baja distancia.

## Autores

- Valentina Rosas
- Cesar Villegas

## Tema

**Investigacion de Operaciones**  
Algoritmo Colonia de Hormigas, ACO, aplicado al TSP.

## Caracteristicas

- Implementacion propia del algoritmo ACO en Python.
- Interfaz interactiva con Streamlit.
- Control de numero de ciudades, hormigas, alpha, beta, rho, Q, iteraciones y semilla.
- Preset del ejemplo de clase con ciudades A-E y recorrido esperado de longitud 14.00.
- Visualizacion de la mejor ruta encontrada.
- Grafica de convergencia por iteracion.
- Red de feromonas y matriz de calor.
- Secciones educativas con formulas, pasos, parametros, ventajas, limitaciones y aplicaciones.
- Codigo modular con `dataclasses`, type hints y pruebas basicas.

## Instalacion

```bash
pip install -r requirements.txt
```

## Ejecucion

```bash
streamlit run app.py
```

La aplicacion se abrira en el navegador. Desde la barra lateral se pueden ajustar los parametros
del experimento y la simulacion se actualiza automaticamente.

Para replicar el ejemplo visto en clase, selecciona **Ejemplo de clase A-E** en la barra lateral.
La ruta esperada es:

```text
A -> B -> C -> D -> E -> A
Longitud: 14.00
```

Como el TSP es un ciclo, la misma solucion tambien puede aparecer rotada o invertida.

## Como funciona el algoritmo

ACO imita el comportamiento colectivo de las hormigas:

1. Las hormigas exploran rutas posibles.
2. Cada ruta deja una cantidad de feromona.
3. Las rutas mas cortas depositan mas feromona.
4. La evaporacion reduce rastros antiguos y evita depender demasiado de caminos malos.
5. Con el tiempo, la colonia tiende a reforzar recorridos de menor distancia.

Formulas principales:

```text
eta(i,j) = 1 / d(i,j)

p(i,j) = tau(i,j)^alpha * eta(i,j)^beta
         / sum(tau(i,l)^alpha * eta(i,l)^beta)

tau(i,j)(t+1) = (1-rho) * tau(i,j)(t) + delta_tau(i,j)

delta_tau = Q / L
```

## Estructura del proyecto

```text
aco-tsp-python/
├── app.py
├── src/
│   ├── aco/
│   │   ├── models.py
│   │   ├── solver.py
│   │   └── utils.py
│   ├── content/
│   │   └── educational.py
│   └── visualization/
│       └── plots.py
├── tests/
│   └── test_aco.py
├── requirements.txt
└── README.md
```

## Archivos principales

- `app.py`: interfaz visual interactiva en Streamlit.
- `src/aco/solver.py`: implementacion del algoritmo ACO.
- `src/aco/models.py`: modelos de datos para ciudades, parametros y resultados.
- `src/aco/utils.py`: generacion de ciudades, matriz de distancias y calculo de rutas.
- `src/visualization/plots.py`: graficas interactivas con Plotly.
- `src/content/educational.py`: contenido academico de la exposicion.
- `tests/test_aco.py`: pruebas unitarias basicas.

## Pruebas

```bash
pytest
```

Las pruebas verifican la matriz de distancias, el calculo de rutas cerradas, la validez del ciclo
TSP, la actualizacion de feromonas y la convergencia de la mejor solucion acumulada.

## Referencias

- Dorigo, M. & Stutzle, T. (2004). *Ant Colony Optimization*. MIT Press.
- Dorigo, M. (1992). *Optimization, Learning and Natural Algorithms*. Ph.D. Thesis.
- Colorni, A., Dorigo, M. & Maniezzo, V. (1991). *Distributed Optimization by Ant Colonies*.
- Dorigo, M. & Blum, C. (2005). *Ant Colony Optimization Theory: A Survey*.
