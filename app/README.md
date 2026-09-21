# Percentil ATP

Calcula, con quickselect real (no con conteo ni con `sorted()` completo), el
valor de corte de un percentil sobre distintas estadísticas de jugadores ATP
(edad, ranking, altura, aces, % de primer saque).

## Instalación y ejecución

```bash
pip install -r app/requirements.txt
cd app/backend && uvicorn main:app --reload
```

Abrir `http://127.0.0.1:8000` en el navegador.

## Origen de los datos

Prioridad: API pública (si hay `TENNIS_API_KEY` en el entorno) -> CSV local
en `data/atp_extra_stats.csv`. Si no hay key, o si `api-tennis.com` falla
por red/autenticación/formato, la app sigue funcionando igual con el CSV —
el valor numérico de cada estadística siempre proviene del CSV, la API solo
afecta el campo informativo `fuente_datos`.

Para configurar la key (opcional):

```bash
export TENNIS_API_KEY="tu-clave"
```

### Dataset (`data/atp_extra_stats.csv`)

Único dataset de la app: top 50 del ranking ATP (temporada 2026) con
puntos de ranking, altura, edad, aces promedio por partido y % de primer
saque adentro, calculados a partir de los CSV públicos de **Jeff Sackmann**
(`tennis_atp`, licencia
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/);
espejo usado: `github.com/Aneeshers/tennis-sackmann-archive`, ya que el
repositorio original devolvía 404 al momento de generar este dataset).

Se genera con `python3 data/build_extra_stats.py`, que cruza
`atp_rankings_current.csv`, `atp_players.csv` y `atp_matches_2026.csv`
(descargados aparte, ver el script). Solo se incluyen jugadores del top 50
con altura y fecha de nacimiento registradas, y al menos 3 partidos con
estadísticas de saque en la temporada. Uso no comercial, académico.

## Agregar una estadística nueva

Si el dato ya está en `atp_extra_stats.csv` (o se puede agregar en
`data/build_extra_stats.py`), basta con sumar una entrada a `STATS` en
`app/backend/data_sources.py` apuntando a esa columna. No hay que tocar
`partition_trace.py` ni el motor de `src/`.

## Pruebas

```bash
python3 -m pytest app/tests -v
```
