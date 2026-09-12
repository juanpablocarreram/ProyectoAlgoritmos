"""
Particion de Lomuto.
Autor: Juan Pablo Carrera Martinez
Reordena, en una sola pasada, el segmento arr[low..high] de manera que
todos los elementos menores o iguales al pivote (el ultimo elemento del
segmento) queden a su izquierda, y todos los mayores queden a su derecha.
Devuelve el indice final del pivote.

Complejidad: O(n) en el numero de comparaciones, donde n = high - low + 1.
"""


def lomuto_partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
