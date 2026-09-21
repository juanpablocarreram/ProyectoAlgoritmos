import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from fastapi.testclient import TestClient

import data_sources
from main import app

client = TestClient(app)


def test_stats_endpoint():
    respuesta = client.get("/api/stats")
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert set(cuerpo.keys()) == set(data_sources.STATS.keys())
    assert len(cuerpo["velocidad_saque"]["jugadores"]) == 14


def test_percentil_coincide_con_sorted_para_ambos_algoritmos():
    registros = data_sources.obtener_estadistica("velocidad_saque")
    valores = sorted(r["valor"] for r in registros)
    n = len(valores)
    for percentil in (10, 25, 50, 75, 90):
        k = round((percentil / 100) * (n - 1))
        esperado = valores[k]
        for algoritmo in ("naive", "mom"):
            respuesta = client.post(
                "/api/percentil",
                json={"stat": "velocidad_saque", "percentil": percentil, "algoritmo": algoritmo},
            )
            assert respuesta.status_code == 200
            cuerpo = respuesta.json()
            assert cuerpo["valor_corte"] == esperado
            assert cuerpo["posicion"] == k
            assert len(cuerpo["rondas"]) >= 1


def test_percentil_stat_desconocida():
    respuesta = client.post(
        "/api/percentil",
        json={"stat": "no_existe", "percentil": 50, "algoritmo": "naive"},
    )
    assert respuesta.status_code == 404


def test_ubicar_valor_propio():
    respuesta = client.post("/api/ubicar", json={"stat": "velocidad_saque", "valor": 200.0})
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert 0 <= cuerpo["percentil_estimado"] <= 100
    assert cuerpo["total_jugadores"] == 14
    assert len(cuerpo["rondas"]) == 1
