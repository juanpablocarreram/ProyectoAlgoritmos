import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

import data_sources


def test_obtener_estadistica_velocidad_saque():
    registros = data_sources.obtener_estadistica("velocidad_saque")
    assert len(registros) == 14
    assert all(isinstance(r["valor"], float) for r in registros)
    assert all(r["jugador"] for r in registros)


def test_obtener_estadistica_edad():
    registros = data_sources.obtener_estadistica("edad")
    assert len(registros) == 14
    assert all(r["valor"] > 0 for r in registros)


def test_listar_estadisticas_sin_api_key(monkeypatch):
    monkeypatch.delenv("TENNIS_API_KEY", raising=False)
    resultado = data_sources.listar_estadisticas()
    assert set(resultado.keys()) == set(data_sources.STATS.keys())
    assert resultado["velocidad_saque"]["fuente_datos"] == "csv_local"
    assert len(resultado["velocidad_saque"]["jugadores"]) == 14


def test_obtener_estadistica_ranking_puntos():
    registros = data_sources.obtener_estadistica("ranking_puntos")
    assert len(registros) > 0
    assert all(r["valor"] > 0 for r in registros)
