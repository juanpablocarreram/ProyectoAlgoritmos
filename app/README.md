# Percentil ATP

Calcula, con quickselect real (no con conteo ni con `sorted()` completo), el
valor de corte de un percentil sobre distintas estadísticas de jugadores ATP
(saque, edad, ranking, altura, aces, % de primer saque).

## Instalación y ejecución

```bash
pip install -r app/requirements.txt
cd app/backend && uvicorn main:app --reload
```

Abrir `http://127.0.0.1:8000` en el navegador.

## Origen de los datos

Prioridad: API pública (si hay `TENNIS_API_KEY` en el entorno) -> CSV local
en `data/atp_serve_speeds.csv`.

Se investigaron Sportradar, api-tennis.com y tennis-api.com (RapidAPI).
Ninguna capa gratuita actual expone la velocidad promedio de saque por
jugador (es un dato de nivel de pago); las capas gratuitas solo cubren
rankings y jugadores en vivo. Por eso, cuando hay `TENNIS_API_KEY`
configurada, la app intenta refrescar contra `api-tennis.com` (variable
`TENNIS_API_URL`, con valor por defecto en `data_sources.py`) y usa esa
respuesta solo para indicar `fuente_datos: "api"`; el valor numérico de cada
estadística siempre proviene del CSV real. Este endpoint no se pudo probar
en vivo (no se dispone de una key), así que su contrato exacto puede
necesitar ajuste si `api-tennis.com` cambia su API — el fallback cubre
justamente ese caso: cualquier fallo de red, autenticación o formato hace
que la app siga funcionando con el CSV, sin ninguna diferencia para quien la
usa.

Para configurar la key (opcional):

```bash
export TENNIS_API_KEY="tu-clave"
```

Sin esa variable, la app funciona igual, siempre desde el CSV local.

### Dataset real (`data/atp_serve_speeds.csv`)

14 jugadores ATP con velocidad promedio de primer saque real:

- 5 de la nota oficial de ATP Tour "It All Adds Up: Mpetshi Perricard's
  serve sizzles above all others in tennis" (temporada 2025).
- 9 de TennisPredict.com ("How Fast Pro Players Serve In Tennis").

La columna `edad_2025` (2025 menos el año de nacimiento) es una segunda
estadística en el mismo archivo.

### Dataset extendido (`data/atp_extra_stats.csv`)

Top 50 del ranking ATP (temporada 2026) con puntos de ranking, altura,
aces promedio por partido y % de primer saque adentro, calculados a partir
de los CSV públicos de **Jeff Sackmann** (`tennis_atp`, licencia
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/);
espejo usado: `github.com/Aneeshers/tennis-sackmann-archive`, ya que el
repositorio original devolvía 404 al momento de generar este dataset).

Se genera con `python3 data/build_extra_stats.py`, que cruza
`atp_rankings_current.csv`, `atp_players.csv` y `atp_matches_2026.csv`
(descargados aparte, ver el script). Solo se incluyen jugadores del top 50
con altura registrada y al menos 3 partidos con estadísticas de saque en la
temporada. Uso no comercial, académico.

## Agregar una estadística nueva

En `app/backend/data_sources.py`, agregar una entrada a `STATS` con
`archivo` (el CSV dentro de `data/`) y `columna`. No hay que tocar
`partition_trace.py` ni el motor de `src/`.

## Pruebas

```bash
python3 -m pytest app/tests -v
```
