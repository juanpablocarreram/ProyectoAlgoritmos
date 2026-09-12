import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import partition_trace
from lomuto import lomuto_partition


def test_particion_unica_sin_swaps():
    arr = [5, 3, 8, 4, 2]
    indice_final, rondas = partition_trace.ejecutar_particion_unica(arr[:-1], 2)
    assert len(rondas) == 1
    ronda = rondas[0]
    assert ronda["pivote"] == 2
    esperado = arr[:]
    pivote_index_esperado = lomuto_partition(esperado, 0, len(esperado) - 1)
    assert indice_final == pivote_index_esperado
    assert [p["swap"] for p in ronda["pasos"]] == [False, False, False, False]


def test_particion_unica_con_swaps():
    base = [1, 3, 0, 4]
    indice_final, rondas = partition_trace.ejecutar_particion_unica(base, 2)
    copia = base + [2]
    pivote_index_esperado = lomuto_partition(copia, 0, len(copia) - 1)
    assert indice_final == pivote_index_esperado
    pasos = rondas[0]["pasos"]
    assert [p["j"] for p in pasos] == [0, 1, 2, 3]
    assert pasos[0]["swap"] is True
    assert pasos[0]["i"] == 0
    assert pasos[2]["swap"] is True
    assert pasos[2]["i"] == 1


def test_percentil_trazado_coincide_con_sorted():
    random.seed(11)
    for _ in range(30):
        n = random.randint(2, 60)
        valores = [float(random.randint(-50, 50)) for _ in range(n)]
        k = random.randint(0, n - 1)
        esperado = sorted(valores)[k]
        for algoritmo in ("naive", "mom"):
            resultado, rondas = partition_trace.ejecutar_percentil_trazado(valores, k, algoritmo)
            assert resultado == esperado
            assert len(rondas) >= 1
            for ronda in rondas:
                assert ronda["indice_final"] >= ronda["low"]
                assert ronda["indice_final"] <= ronda["high"]
