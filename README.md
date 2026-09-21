# Particionamiento de datasets: Lomuto, Quickselect y Percentil ATP

Proyecto sobre el algoritmo de partición de Lomuto y su uso en quickselect
para encontrar percentiles sin ordenar un arreglo completo. Incluye el
motor del algoritmo, benchmarks de rendimiento entre dos estrategias de
pivote, y una aplicación web que aplica todo esto a estadísticas reales del
top 50 ATP (ranking, altura, aces, % de primer saque).

## Estructura del repositorio

```
src/         Motor: partición de Lomuto y las dos variantes de quickselect
benchmark/   Scripts que miden y grafican el rendimiento de cada variante
results/     Salida de los benchmarks (benchmark.csv, benchmark.png)
data/        Dataset de jugadores ATP y script que lo genera
app/         Aplicación web (FastAPI + frontend) de percentil de saque ATP
Reporte_Percentil_ATP_Lomuto.pdf   Reporte con el análisis completo
```

## Requisitos

- Python 3.12+
- Dependencias de la app web: `pip install -r app/requirements.txt`
- Para graficar los benchmarks: `matplotlib` (`pip install matplotlib`)

## 1. Motor de partición y quickselect (`src/`)

- `lomuto.py`: partición de Lomuto, O(n) por pasada, pivote = último elemento.
- `quickselect_naive.py`: quickselect con pivote ingenuo (caso promedio O(n),
  peor caso O(n²) con entradas ya ordenadas).
- `quickselect_mom.py`: quickselect con pivote por mediana de medianas
  (Blum-Floyd-Pratt-Rivest-Tarjan), garantiza O(n) en el peor caso a costa de
  mayor complejidad y overhead constante.

Correr las pruebas de corrección (compara contra `sorted()` en 300 casos
aleatorios):

```bash
python3 src/test_correctness.py
```

## 2. Benchmarks (`benchmark/`, `results/`)

Comparan tiempos de `quickselect_naive`, `quickselect_mom` y `sorted()` como
referencia, sobre entradas aleatorias, con muchos duplicados y ya ordenadas.

```bash
python3 benchmark/run_benchmark.py    # genera results/benchmark.csv
python3 benchmark/plot_benchmark.py   # genera results/benchmark.png
```

## 3. Aplicación web (`app/`)

Calcula el valor de corte de un percentil sobre estadísticas reales del top
50 ATP (temporada 2026), usando quickselect real —no `sorted()` ni
conteo— y visualiza paso a paso cómo se va particionando el arreglo.

```bash
pip install -r app/requirements.txt
cd app/backend && uvicorn main:app --reload
```

Abrir `http://127.0.0.1:8000` en el navegador. Detalle de endpoints, origen
de los datos y cómo agregar una estadística nueva en [`app/README.md`](app/README.md).

Pruebas de la app:

```bash
python3 -m pytest app/tests -v
```

## 4. Reporte

[`Reporte_Percentil_ATP_Lomuto.pdf`](Reporte_Percentil_ATP_Lomuto.pdf)
documenta el análisis de la partición de Lomuto, la comparación entre
pivote ingenuo y mediana de medianas, y la aplicación de percentil ATP
construida sobre ese motor.
