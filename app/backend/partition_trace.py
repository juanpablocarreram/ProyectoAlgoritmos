import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import lomuto
import quickselect_naive
import quickselect_mom


class _ArregloEspia:
    def __init__(self, datos, eventos):
        self._datos = datos
        self._eventos = eventos

    def __getitem__(self, indice):
        valor = self._datos[indice]
        self._eventos.append(("lectura", indice, valor))
        return valor

    def __setitem__(self, indice, valor):
        self._eventos.append(("escritura", indice, valor))
        self._datos[indice] = valor

    def __len__(self):
        return len(self._datos)


def _reconstruir_pasos(eventos, low, high):
    pasos = []
    i_actual = low - 1
    pos = 1  # eventos[0] es la lectura inicial del pivote (arr[high])
    for j in range(low, high):
        _, _, valor_j = eventos[pos]
        pos += 1
        hubo_swap = pos < len(eventos) and eventos[pos][1] == j
        if hubo_swap:
            pos += 1  # segunda lectura de j (lado derecho del swap)
            _, indice_i, _ = eventos[pos]
            pos += 1  # lectura de i
            pos += 2  # las dos escrituras del swap
            i_actual = indice_i
        pasos.append({"j": j, "valor_j": valor_j, "i": i_actual, "swap": hubo_swap})
    return pasos


def _particionar_y_registrar(arr, low, high, rondas):
    eventos = []
    espia = _ArregloEspia(arr, eventos)
    pivote = arr[high]
    indice_final = lomuto.lomuto_partition(espia, low, high)
    pasos = _reconstruir_pasos(eventos, low, high)
    rondas.append({
        "low": low,
        "high": high,
        "pivote": pivote,
        "indice_final": indice_final,
        "pasos": pasos,
    })
    return indice_final


def ejecutar_percentil_trazado(valores, k, algoritmo):
    rondas = []
    original = lomuto.lomuto_partition

    def particion_trazada(arr, low, high):
        return _particionar_y_registrar(arr, low, high, rondas)

    quickselect_naive.lomuto_partition = particion_trazada
    quickselect_mom.lomuto_partition = particion_trazada
    try:
        copia = valores[:]
        funcion = quickselect_mom.quickselect_mom if algoritmo == "mom" else quickselect_naive.quickselect_naive
        resultado = funcion(copia, k)
    finally:
        quickselect_naive.lomuto_partition = original
        quickselect_mom.lomuto_partition = original
    return resultado, rondas


def ejecutar_particion_unica(valores, valor_pivote):
    rondas = []
    copia = valores + [valor_pivote]
    indice_final = _particionar_y_registrar(copia, 0, len(copia) - 1, rondas)
    return indice_final, rondas
