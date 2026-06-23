# 🔹 Save as: ~/psi_lab/modules/ψ_glif_mutation.py

import random

def mutate_glif(ascii_glif, mutation_level=0.3):
    mutated = ""
    for char in ascii_glif:
        if char.strip() and random.random() < mutation_level:
            mutated += random.choice(['*', '+', ':', '%', '@', '-', '=', '~', 'ψ'])
        else:
            mutated += char
    return mutated
