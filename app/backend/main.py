import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import data_sources
import partition_trace

app = FastAPI(title="Percentil de saque ATP")


class PeticionPercentil(BaseModel):
    stat: str
    percentil: float
    algoritmo: str = "naive"


class PeticionUbicar(BaseModel):
    stat: str
    valor: float


@app.get("/api/stats")
def obtener_stats():
    return data_sources.listar_estadisticas()


@app.post("/api/percentil")
def calcular_percentil(peticion: PeticionPercentil):
    if peticion.stat not in data_sources.STATS:
        raise HTTPException(status_code=404, detail="estadistica desconocida")
    if not 0 <= peticion.percentil <= 100:
        raise HTTPException(status_code=400, detail="percentil fuera de rango")
    if peticion.algoritmo not in ("naive", "mom"):
        raise HTTPException(status_code=400, detail="algoritmo desconocido")

    registros = data_sources.obtener_estadistica(peticion.stat)
    valores = [r["valor"] for r in registros]
    n = len(valores)
    k = max(0, min(n - 1, round((peticion.percentil / 100) * (n - 1))))

    resultado, rondas = partition_trace.ejecutar_percentil_trazado(valores, k, peticion.algoritmo)
    jugador = next((r["jugador"] for r in registros if r["valor"] == resultado), None)

    return {
        "posicion": k,
        "valor_corte": resultado,
        "jugador": jugador,
        "rondas": rondas,
    }


@app.post("/api/ubicar")
def ubicar_valor(peticion: PeticionUbicar):
    if peticion.stat not in data_sources.STATS:
        raise HTTPException(status_code=404, detail="estadistica desconocida")

    registros = data_sources.obtener_estadistica(peticion.stat)
    valores = [r["valor"] for r in registros]
    n = len(valores)

    posicion, rondas = partition_trace.ejecutar_particion_unica(valores, peticion.valor)
    percentil = (posicion / n) * 100

    return {
        "percentil_estimado": round(percentil, 1),
        "posicion": posicion,
        "total_jugadores": n,
        "rondas": rondas,
    }


FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
