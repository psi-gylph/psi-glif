#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~/psi_lab/modules/ψ_import_glif.py

import os
import sys
import math

BASE_DIR = os.path.expanduser("~/psi_lab")
sys.path.append(os.path.join(BASE_DIR, "modules"))

from ψ_glif_memory import GlifIdentity, GlifOperationType, save_glif
from ψ_entropy import entropy_level


def compute_phi_from_entropy(ent: float) -> float:
    """
    ψ-game içindeki φ modeliyle aynı mantık:
    - Çok düşük entropi → donuk → φ düşük
    - Çok yüksek entropi → gürültü → φ düşük
    - Orta band (≈3) → φ yüksek
    """
    center = 3.0
    width = 1.0
    x = (ent - center) / width
    phi = math.exp(-0.5 * x * x)
    return float(phi)


def import_ascii_glif(file_path: str, seed: str | None = None):
    """
    Dışarıda üretilmiş bir ASCII glif dosyasını alır,
    GlifIdentity ile sarar ve ψ_lab/glif_storage içine kaydeder.
    """
    file_path = os.path.expanduser(file_path)

    if not os.path.exists(file_path):
        print(f"[ψ-import] Dosya bulunamadı: {file_path}")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        ascii_str = f.read().rstrip("\n")

    if not seed or not seed.strip():
        seed = os.path.splitext(os.path.basename(file_path))[0]

    # Kimlik yarat
    identity = GlifIdentity(seed=seed, operation=GlifOperationType.CREATED)

    # Entropi + φ hesapla
    ent = entropy_level(ascii_str)
    phi = compute_phi_from_entropy(ent)
    identity.entropy_level = ent
    identity.phi_score = phi

    # ψ_glif_memory.save_glif ile sistem formatında kaydet
    save_glif(ascii_str, identity)

    print("[ψ-import] Glif içe aktarıldı.")
    print(f"  seed : {identity.seed}")
    print(f"  id   : {identity.id}")
    print(f"  Φ    : {identity.phi_score:.2f}")
    print(f"  H    : {identity.entropy_level:.2f}")
    print(f"  path : ~/psi_lab/glif_storage/{identity.id}.json")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  python3 modules/ψ_import_glif.py import/ψ_external_test.ascii [seed_ismi]")
        sys.exit(1)

    path = sys.argv[1]
    seed_arg = sys.argv[2] if len(sys.argv) >= 3 else None
    import_ascii_glif(path, seed_arg)
