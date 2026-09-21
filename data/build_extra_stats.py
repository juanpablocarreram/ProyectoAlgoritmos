"""Genera data/atp_extra_stats.csv, el unico dataset de la app, a partir
de los CSV publicos de Jeff Sackmann (tennis_atp, espejo en
Aneeshers/tennis-sackmann-archive, licencia CC BY-NC-SA 4.0).

Toma el top 50 del ranking ATP mas reciente disponible, cruza con
altura/nombre/edad de atp_players.csv, y promedia aces y % de primer
saque adentro de sus partidos de la temporada 2026 (atp_matches_2026.csv).

Uso: python3 data/build_extra_stats.py
Requiere los tres CSV de entrada ya descargados en /tmp (ver README).
"""
import csv
from collections import defaultdict
from pathlib import Path

RANKINGS_PATH = Path("/tmp/rankings_current.csv")
PLAYERS_PATH = Path("/tmp/atp_players.csv")
MATCHES_PATH = Path("/tmp/matches_2026.csv")
SALIDA = Path(__file__).resolve().parent / "atp_extra_stats.csv"

MIN_PARTIDOS = 3
TOP_N_RANKING = 50
ANIO_REFERENCIA = 2026


def cargar_top_ranking():
    filas = list(csv.DictReader(RANKINGS_PATH.open()))
    ultima_fecha = max(f["ranking_date"] for f in filas)
    del filas
    top = []
    with RANKINGS_PATH.open() as archivo:
        for fila in csv.DictReader(archivo):
            if fila["ranking_date"] != ultima_fecha:
                continue
            top.append((int(fila["rank"]), fila["player"], int(fila["points"])))
    top.sort(key=lambda item: item[0])
    return {jugador_id: puntos for _, jugador_id, puntos in top[:TOP_N_RANKING]}


def cargar_jugadores():
    jugadores = {}
    with PLAYERS_PATH.open() as archivo:
        for fila in csv.DictReader(archivo):
            if not fila["height"] or not fila["dob"]:
                continue
            nombre = f"{fila['name_first']} {fila['name_last']}".strip()
            edad = ANIO_REFERENCIA - int(fila["dob"][:4])
            jugadores[fila["player_id"]] = {
                "nombre": nombre,
                "altura": int(fila["height"]),
                "edad": edad,
            }
    return jugadores


def agregar_estadisticas_partidos():
    acumulado = defaultdict(lambda: {"aces": [], "primer_saque_pct": []})
    with MATCHES_PATH.open() as archivo:
        for fila in csv.DictReader(archivo):
            for prefijo in ("winner", "loser"):
                pid = fila[f"{prefijo}_id"]
                columna = "w_" if prefijo == "winner" else "l_"
                try:
                    ace = float(fila[f"{columna}ace"])
                    svpt = float(fila[f"{columna}svpt"])
                    primer_in = float(fila[f"{columna}1stIn"])
                except (ValueError, KeyError):
                    continue
                if svpt <= 0:
                    continue
                acumulado[pid]["aces"].append(ace)
                acumulado[pid]["primer_saque_pct"].append(100 * primer_in / svpt)
    return acumulado


def main():
    ranking = cargar_top_ranking()
    jugadores = cargar_jugadores()
    partidos = agregar_estadisticas_partidos()

    filas_salida = []
    for player_id, puntos in ranking.items():
        info = jugadores.get(player_id)
        stats = partidos.get(player_id)
        if not info or not stats or len(stats["aces"]) < MIN_PARTIDOS:
            continue
        aces_prom = sum(stats["aces"]) / len(stats["aces"])
        saque_prom = sum(stats["primer_saque_pct"]) / len(stats["primer_saque_pct"])
        filas_salida.append({
            "jugador": info["nombre"],
            "ranking_puntos": puntos,
            "altura_cm": info["altura"],
            "edad": info["edad"],
            "aces_promedio": round(aces_prom, 1),
            "primer_saque_pct": round(saque_prom, 1),
        })

    with SALIDA.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=["jugador", "ranking_puntos", "altura_cm", "edad", "aces_promedio", "primer_saque_pct"],
        )
        escritor.writeheader()
        escritor.writerows(filas_salida)

    print(f"{len(filas_salida)} jugadores escritos en {SALIDA}")


if __name__ == "__main__":
    main()
