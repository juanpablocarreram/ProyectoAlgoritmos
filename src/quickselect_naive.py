"""
Autor: Juan Pablo Carrera Martinez
Quickselect con pivote ingenuo: siempre se elige el ultimo elemento del
segmento como pivote (via lomuto_partition). Encuentra el k-esimo elemento
mas pequeno (0-indexado) de arr sin ordenar el arreglo completo.

Caso promedio: O(n)
Peor caso: O(n^2)  (por ejemplo, arreglo ya ordenado, pivote = ultimo elemento
    produce siempre la particion mas desbalanceada posible)
"""

from lomuto import lomuto_partition


def quickselect_naive(arr, k, low=None, high=None):
    if low is None:
        low, high = 0, len(arr) - 1

    # Version iterativa: la recursion original es de cola (tail call), asi
    # que se reemplaza por un ciclo para evitar el limite de recursion de
    # Python en el peor caso (arreglo ordenado), donde la profundidad de
    # recursion seria O(n).
    while low < high:
        pivot_index = lomuto_partition(arr, low, high)
        if k == pivot_index:
            return arr[k]
        elif k < pivot_index:
            high = pivot_index - 1
        else:
            low = pivot_index + 1
    return arr[low]
