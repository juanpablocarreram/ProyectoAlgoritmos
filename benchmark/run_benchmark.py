import sys
import os
import csv
import random
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from quickselect_naive import quickselect_naive
from quickselect_mom import quickselect_mom


def make_input(kind, n):
    if kind == "aleatorio":
        return [random.randint(0, 10 * n) for _ in range(n)]
    if kind == "ordenado":
        return list(range(n))
    if kind == "duplicados":
        return [random.randint(0, 9) for _ in range(n)]
    raise ValueError(kind)


def time_call(func, arr, k, repeats):
    best = float("inf")
    for _ in range(repeats):
        a = arr[:]
        start = time.perf_counter()
        func(a, k)
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)
    return best


def main():
    random.seed(42)

    sizes_normal = [500, 1000, 2000, 5000, 10000, 20000, 40000, 80000]
    sizes_ordenado = [500, 1000, 2000, 4000, 8000, 16000]
    # 'duplicados' se limita a un rango mas chico: la variante mediana-de-
    # medianas se degrada fuertemente aqui (ver discusion en el reporte),
    # y con sizes_normal completo el benchmark tardaria demasiado.
    sizes_duplicados = [500, 1000, 2000, 4000, 8000]

    configs = [
        ("aleatorio", sizes_normal),
        ("duplicados", sizes_duplicados),
        ("ordenado", sizes_ordenado),
    ]

    out_path = os.path.join(os.path.dirname(__file__), "..", "results", "benchmark.csv")
    fieldnames = ["tipo_entrada", "n", "quickselect_naive_s", "quickselect_mom_s", "sort_baseline_s"]

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for kind, sizes in configs:
            for n in sizes:
                arr = make_input(kind, n)
                k = n // 2  # mediana

                repeats = 3 if n <= 20000 else 1

                t_naive = time_call(quickselect_naive, arr, k, repeats)
                t_mom = time_call(quickselect_mom, arr, k, repeats)
                t_sort = time_call(lambda a, kk: sorted(a)[kk], arr, k, repeats)

                row = {
                    "tipo_entrada": kind,
                    "n": n,
                    "quickselect_naive_s": t_naive,
                    "quickselect_mom_s": t_mom,
                    "sort_baseline_s": t_sort,
                }
                writer.writerow(row)
                f.flush()
                print(f"{kind:12s} n={n:7d}  naive={t_naive:.5f}s  "
                      f"mom={t_mom:.5f}s  sort={t_sort:.5f}s", flush=True)

    print(f"\nResultados guardados en {out_path}")


if __name__ == "__main__":
    main()
