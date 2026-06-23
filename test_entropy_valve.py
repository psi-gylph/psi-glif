# -*- coding: utf-8 -*-
# ~/psi_lab/test_entropy_valve.py

from pathlib import Path
import sys

# Proje path'lerini sys.path'e ekleyelim
ROOT = Path.home() / "psi_lab"
sys.path.append(str(ROOT / "glifs"))
sys.path.append(str(ROOT / "core"))

from psi_toroidal_glif_v2 import radial_profile, symmetry_lr, symmetry_tb
from ψ_entropy_valve import EntropyValve

# Torus metriklerini oku
profile = radial_profile(16)
sym_lr = symmetry_lr()
sym_tb = symmetry_tb()

valve = EntropyValve(profile, sym_lr, sym_tb)

print("Valve Stability:", valve.stability_index())
Phi, H = valve.regulate(Phi=0.94, entropy=2.64)
print("Regulated Phi / Entropy:", Phi, H)
