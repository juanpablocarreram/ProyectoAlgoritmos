import csv
import os
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
CSV_PATH = DATA_DIR / "atp_serve_speeds.csv"

STATS = {
    "velocidad_saque": {
        "label": "Velocidad de primer saque",
        "unidad": "km/h",
        "columna": "velocidad_kmh",
    },
    "edad": {
        "label": "Edad (cumplida en 2025)",
        "unidad": "años",
        "columna": "edad_2025",
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
            "jugadores": obtener_estadistica(nombre),
            "fuente_datos": fuente,
        }
        for nombre, meta in STATS.items()
    }
