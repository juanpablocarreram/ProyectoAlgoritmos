import csv
import os
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

STATS = {
    "velocidad_saque": {
        "label": "Velocidad de primer saque",
        "unidad": "km/h",
        "archivo": "atp_serve_speeds.csv",
        "columna": "velocidad_kmh",
        "etiqueta_bajo": "el saque más lento",
        "etiqueta_alto": "el saque más rápido",
    },
    "edad": {
        "label": "Edad (cumplida en 2025)",
        "unidad": "años",
        "archivo": "atp_serve_speeds.csv",
        "columna": "edad_2025",
        "etiqueta_bajo": "la edad más baja",
        "etiqueta_alto": "la edad más alta",
    },
    "ranking_puntos": {
        "label": "Puntos de ranking ATP",
        "unidad": "pts",
        "archivo": "atp_extra_stats.csv",
        "columna": "ranking_puntos",
        "etiqueta_bajo": "menos puntos de ranking",
        "etiqueta_alto": "más puntos de ranking",
    },
    "altura": {
        "label": "Altura",
        "unidad": "cm",
        "archivo": "atp_extra_stats.csv",
        "columna": "altura_cm",
        "etiqueta_bajo": "la estatura más baja",
        "etiqueta_alto": "la estatura más alta",
    },
    "aces_promedio": {
        "label": "Aces promedio por partido (2026)",
        "unidad": "aces/partido",
        "archivo": "atp_extra_stats.csv",
        "columna": "aces_promedio",
        "etiqueta_bajo": "menos aces en promedio",
        "etiqueta_alto": "más aces en promedio",
    },
    "primer_saque_pct": {
        "label": "Primer saque adentro (2026)",
        "unidad": "%",
        "archivo": "atp_extra_stats.csv",
        "columna": "primer_saque_pct",
        "etiqueta_bajo": "el porcentaje de primer saque más bajo",
        "etiqueta_alto": "el porcentaje de primer saque más alto",
    },
}


def _cargar_csv(nombre_archivo):
    with open(DATA_DIR / nombre_archivo, newline="", encoding="utf-8") as archivo:
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
    meta = STATS[nombre_stat]
    filas = _cargar_csv(meta["archivo"])
    columna = meta["columna"]
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
