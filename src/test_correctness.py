#Autor: Juan Pablo Carrera Martinez
import random
from lomuto import lomuto_partition
from quickselect_naive import quickselect_naive
from quickselect_mom import quickselect_mom


def check_partition(arr):
    a = arr[:]
    pivot_index = lomuto_partition(a, 0, len(a) - 1)
    pivot = a[pivot_index]
    assert all(x <= pivot for x in a[:pivot_index]), a
    assert all(x >= pivot for x in a[pivot_index + 1:]), a


def run():
    random.seed(7)
    for trial in range(300):
        n = random.randint(1, 200)
        arr = [random.randint(-50, 50) for _ in range(n)]

        check_partition(arr)

        k = random.randint(0, n - 1)
        expected = sorted(arr)[k]

        got_naive = quickselect_naive(arr[:], k)
        got_mom = quickselect_mom(arr[:], k)

        assert got_naive == expected, (trial, n, k, got_naive, expected)
        assert got_mom == expected, (trial, n, k, got_mom, expected)

    print("Todas las pruebas de corrección pasaron.")


if __name__ == "__main__":
    run()
