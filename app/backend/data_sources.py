import csv
import os
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CSV_PATH = DATA_DIR / "atp_extra_stats.csv"

STATS = {
    "edad": {
        "label": "Edad (2026)",
        "unidad": "años",
        "columna": "edad",
        "etiqueta_bajo": "la edad más baja",
        "etiqueta_alto": "la edad más alta",
    },
    "ranking_puntos": {
        "label": "Puntos de ranking ATP",
        "unidad": "pts",
        "columna": "ranking_puntos",
        "etiqueta_bajo": "menos puntos de ranking",
        "etiqueta_alto": "más puntos de ranking",
    },
    "altura": {
        "label": "Altura",
        "unidad": "cm",
        "columna": "altura_cm",
        "etiqueta_bajo": "la estatura más baja",
        "etiqueta_alto": "la estatura más alta",
    },
    "aces_promedio": {
        "label": "Aces promedio por partido (2026)",
        "unidad": "aces/partido",
        "columna": "aces_promedio",
        "etiqueta_bajo": "menos aces en promedio",
        "etiqueta_alto": "más aces en promedio",
    },
    "primer_saque_pct": {
        "label": "Primer saque adentro (2026)",
        "unidad": "%",
        "columna": "primer_saque_pct",
        "etiqueta_bajo": "el porcentaje de primer saque más bajo",
        "etiqueta_alto": "el porcentaje de primer saque más alto",
    },
}


def _cargar_csv():
    with open(CSV_PATH, newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def _intentar_api():
    api_key = os.environ.get("TENNIS_API_KEY")
    if not api_key or requests is None:
        return None
    url = os.environ.get("TENNIS_API_URL", "https://api.api-tennis.com/tennis/")
    try:
        respuesta = requests.get(
            url,
            params={"method": "get_standings", "event_type": "ATP", "APIkey": api_key},
            timeout=3,
        )
        respuesta.raise_for_status()
        datos = respuesta.json()
        jugadores = [item["player"] for item in datos.get("result", []) if "player" in item]
        return jugadores or None
    except Exception:
        return None


def obtener_estadistica(nombre_stat):
    filas = _cargar_csv()
    columna = STATS[nombre_stat]["columna"]
    return [{"jugador": fila["jugador"], "valor": float(fila[columna])} for fila in filas]


def listar_estadisticas():
    fuente = "api" if _intentar_api() is not None else "csv_local"
    return {
        nombre: {
            "label": meta["label"],
            "unidad": meta["unidad"],
            "etiqueta_bajo": meta["etiqueta_bajo"],
            "etiqueta_alto": meta["etiqueta_alto"],
            "jugadores": obtener_estadistica(nombre),
            "fuente_datos": fuente,
        }
        for nombre, meta in STATS.items()
    }
