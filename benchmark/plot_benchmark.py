import csv
import os
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
CSV_PATH = os.path.join(HERE, "..", "results", "benchmark.csv")
OUT_PATH = os.path.join(HERE, "..", "results", "benchmark.png")

data = {"aleatorio": [], "duplicados": [], "ordenado": []}

with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        data[row["tipo_entrada"]].append(row)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
titles = {
    "aleatorio": "Entrada aleatoria",
    "duplicados": "Muchos valores repetidos",
    "ordenado": "Entrada ya ordenada (peor caso ingenuo)",
}

for ax, kind in zip(axes, ["aleatorio", "duplicados", "ordenado"]):
    rows = data[kind]
    ns = [int(r["n"]) for r in rows]
    naive = [float(r["quickselect_naive_s"]) for r in rows]
    mom = [float(r["quickselect_mom_s"]) for r in rows]
    srt = [float(r["sort_baseline_s"]) for r in rows]

    ax.plot(ns, naive, marker="o", label="quickselect (pivote ingenuo)", color="#D85A30")
    ax.plot(ns, mom, marker="s", label="quickselect (mediana de medianas)", color="#185FA5")
    ax.plot(ns, srt, marker="^", label="sorted() (referencia)", color="#5F5E5A", linestyle="--")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("tamaño del arreglo (n)")
    ax.set_ylabel("tiempo (s)")
    ax.set_title(titles[kind], fontsize=11)
    ax.grid(True, which="both", linewidth=0.3, alpha=0.6)

axes[0].legend(fontsize=8, loc="upper left")
fig.suptitle("Tiempo de ejecución: partición de Lomuto en quickselect, según estrategia de pivote", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(OUT_PATH, dpi=160)
print(f"Gráfica guardada en {OUT_PATH}")
