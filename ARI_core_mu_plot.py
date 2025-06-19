import os
import re
import glob
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Collect all ARI result files
files = sorted(glob.glob("ARI_results_coremu_*.txt"))

# Step 2: Prepare a list to store parsed results
records = []

# Step 3: Extract core_mu and ARI values from each file
for filepath in files:
    match = re.search(r"coremu_([\d.]+)", filepath)
    if match:
        core_mu = float(match.group(1).rstrip('.'))
    else:
        continue

    with open(filepath) as f:
        for line in f:
            if "KMeans vs FastBAPS" in line:
                ari_kf = float(line.strip().split(":")[-1])
            elif "KMeans vs PopPUNK" in line:
                ari_kp = float(line.strip().split(":")[-1])
            elif "FastBAPS vs PopPUNK" in line:
                ari_fp = float(line.strip().split(":")[-1])
    
    records.append({
        "core_mu": core_mu,
        "KMeans vs FastBAPS": ari_kf,
        "KMeans vs PopPUNK": ari_kp,
        "FastBAPS vs PopPUNK": ari_fp
    })

# Step 4: Convert to DataFrame
df = pd.DataFrame(records)
df = df.sort_values("core_mu")

# Step 5: Plot
plt.figure(figsize=(8, 5))
plt.plot(df["core_mu"], df["KMeans vs FastBAPS"], label="KMeans vs FastBAPS", marker="o")
plt.plot(df["core_mu"], df["KMeans vs PopPUNK"], label="KMeans vs PopPUNK", marker="o")
plt.plot(df["core_mu"], df["FastBAPS vs PopPUNK"], label="FastBAPS vs PopPUNK", marker="o")

plt.xlabel("Core mutation rate (core_mu)")
plt.ylabel("Adjusted Rand Index (ARI)")
plt.title("ARI vs core_mu for different clustering comparisons")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("ARI_vs_coremu_plot.png")
plt.show()
