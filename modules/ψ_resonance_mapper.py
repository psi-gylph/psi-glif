# ~/psi_lab/modules/ψ_resonance_mapper.py
import math
import numpy as np
from collections import Counter
from collections import Counter

def compute_phi(identity):
    avg_res = np.mean([r[2] for r in identity.resonance_history]) if identity.resonance_history else 0
    flux_vals = [v for v in identity.resonance_history[-10:]]  # placeholder
    flux_stab = 1 / (np.std(flux_vals)+0.01) if flux_vals else 0.5
    phi = 0.6*(1 - math.exp(-0.3*avg_res)) + 0.4*math.tanh(0.5*flux_stab)
    return round(phi, 2)

def compute_entropy(glif_ascii):
    counts = Counter(glif_ascii)
    total = len(glif_ascii)
    entropy = -sum((c/total)*math.log2(c/total) for c in counts.values())
    return min(entropy, 3.0)

def calculate_resonance(glif_a, glif_b):
    glif_a = glif_a.replace('\n', '').strip()
    glif_b = glif_b.replace('\n', '').strip()

    if not glif_a or not glif_b:
        return 0.0

    counter_a = Counter(glif_a)
    counter_b = Counter(glif_b)

    shared = sum(min(counter_a[c], counter_b[c]) for c in counter_a if c in counter_b)
    total = max(len(glif_a), len(glif_b))

    return round((shared / total) * 100, 2)

def calculate_resonance(glif_a, glif_b, affect_a=None, affect_b=None):
    # eski overlap(score)
    score = ... 

    # affine varyasyon
    if affect_a and affect_b:
        # örneğin resignation farkı rezonans gücünü etkiler
        affect_score = 1 - abs(affect_a.get("resignation",0) - affect_b.get("resignation",0))
        score *= affect_score

    return round(score,2)
