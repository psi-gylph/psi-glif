# 🔹 Save as: ~/psi_lab/modules/ψ_spiral_warp.py

import random
import os

def spiral_warp(glif_content, glif_name):
    mutated = "".join(random.choice(["@", "#", "ψ", "-", ":", "*", "+", "%", "=", ".", "~"]) for _ in range(64))
    resonance = round(random.uniform(0.7, 0.99), 3)

    export_dir = os.path.expanduser("~/psi_lab/exported_nfts")
    os.makedirs(export_dir, exist_ok=True)
    export_path = os.path.join(export_dir, f"{glif_name}_mutated.glif")

    with open(export_path, "w") as f:
        f.write(mutated)

    return {
        "resonance": resonance,
        "export_path": export_path,
        "mutated": mutated
    }
