import os
import re
import glob
import pandas as pd
import matplotlib.pyplot as plt

# Étape 1 : Récupérer tous les fichiers NMI
files = sorted(glob.glob("NMI_results_HR_rate_*.txt"))

# Étape 2 : Liste pour stocker les résultats
records = []

# Étape 3 : Extraire core_mu et les valeurs de NMI
for filepath in files:
    match = re.search(r"HR_rate_([\d.]+)", filepath)
    if match:
        HR_rate = float(match.group(1).rstrip('.'))
    else:
        continue

    with open(filepath) as f:
        for line in f:
            if "KMeans vs FastBAPS" in line:
                nmi_kf = float(line.strip().split(":")[-1])
            elif "KMeans vs PopPUNK" in line:
                nmi_kp = float(line.strip().split(":")[-1])
            elif "FastBAPS vs PopPUNK" in line:
                nmi_fp = float(line.strip().split(":")[-1])
    
    records.append({
        "HR_rate": HR_rate,
        "KMeans vs FastBAPS": nmi_kf,
        "KMeans vs PopPUNK": nmi_kp,
        "FastBAPS vs PopPUNK": nmi_fp
    })

# Étape 4 : Convertir en DataFrame
df = pd.DataFrame(records)
df = df.sort_values("HR_rate")

# Étape 5 : Tracer
plt.figure(figsize=(8, 5))
plt.plot(df["HR_rate"], df["KMeans vs FastBAPS"], label="KMeans vs FastBAPS", marker="o")
plt.plot(df["HR_rate"], df["KMeans vs PopPUNK"], label="KMeans vs PopPUNK", marker="o")
plt.plot(df["HR_rate"], df["FastBAPS vs PopPUNK"], label="FastBAPS vs PopPUNK", marker="o")

plt.xlabel("Homologous recombination rate(HR_rate)")
plt.ylabel("Normalized Mutual Information (NMI)")
plt.title("NMI vs HR_rate for different clustering comparisons")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("NMI_vs_HR_rate_plot.png")
plt.show()

