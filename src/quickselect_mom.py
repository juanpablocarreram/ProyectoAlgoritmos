"""
Autor: Juan Pablo Carrera Martinez
Quickselect con seleccion de pivote por "mediana de medianas" (Blum, Floyd,
Pratt, Rivest y Tarjan, 1973). Garantiza tiempo O(n) en el peor caso, a
costa de un algoritmo bastante mas complejo que el quickselect con pivote
ingenuo.

Idea general:
  1. Dividir el arreglo en grupos de 5 elementos.
  2. Ordenar cada grupo (con pocos elementos esto es O(1) por grupo) y
     tomar su mediana.
  3. Encontrar recursivamente la mediana de esas medianas: ese valor se usa
     como pivote.
  4. Particionar el arreglo alrededor de ese pivote (usando la misma
     particion de Lomuto que en la version ingenua, pero alrededor de un
     valor que no necesariamente esta al final del arreglo).
  5. Recursar solo en el lado donde sabemos que cae la posicion k buscada.

Este pivote garantiza que ninguna de las dos partes resultantes tenga mas
de 7n/10 elementos, lo que evita el peor caso cuadratico del quickselect
ingenuo.
"""

from lomuto import lomuto_partition


def _partition_around_value(arr, low, high, pivot_value):
    pivot_index = low
    for idx in range(low, high + 1):
        if arr[idx] == pivot_value:
            pivot_index = idx
            break
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    return lomuto_partition(arr, low, high)


def _median_of_medians(arr, low, high):
    n = high - low + 1
    if n <= 5:
        return sorted(arr[low:high + 1])[n // 2]

    medians = []
    for i in range(low, high + 1, 5):
        group = sorted(arr[i:min(i + 5, high + 1)])
        medians.append(group[len(group) // 2])

    return quickselect_mom(medians, len(medians) // 2, 0, len(medians) - 1)


def quickselect_mom(arr, k, low=None, high=None):
    if low is None:
        low, high = 0, len(arr) - 1

    # El bucle principal de SELECT es tail-recursive y se implementa como
    # ciclo por la misma razon que en quickselect_naive. La llamada interna
    # dentro de _median_of_medians si permanece recursiva, pero su
    # profundidad esta acotada por O(log n) porque el arreglo de medianas
    # se reduce a una quinta parte en cada nivel.
    while low < high:
        pivot_value = _median_of_medians(arr, low, high)
        pivot_index = _partition_around_value(arr, low, high, pivot_value)
        if k == pivot_index:
            return arr[k]
        elif k < pivot_index:
            high = pivot_index - 1
        else:
            low = pivot_index + 1
    return arr[low]
