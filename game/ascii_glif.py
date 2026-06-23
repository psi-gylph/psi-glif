# 🔹 Save as: ~/psi_lab/game/ascii_glif.py

import random

def generate_ascii_glif(seed=None, width=40, height=20):
    chars = ['.', ':', '-', '=', '+', '*', '#', '%', '@', 'ψ']
    random.seed(seed)
    return '\n'.join(
        ''.join(random.choice(chars) for _ in range(width))
        for _ in range(height)
    )

if __name__ == "__main__":
    print(generate_ascii_glif(seed="glif_seed_001"))
