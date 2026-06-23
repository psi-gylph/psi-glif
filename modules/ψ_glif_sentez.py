# 🔹 Save as: ~/psi_lab/modules/ψ_glif_sentez.py

import random

def synthesize_glif(glif1, glif2):
    lines1 = glif1.strip().split('\n')
    lines2 = glif2.strip().split('\n')
    max_len = max(len(lines1), len(lines2))
    new_glif = []

    for i in range(max_len):
        line1 = lines1[i % len(lines1)]
        line2 = lines2[i % len(lines2)]

        # Satır uzunluklarını eşitle
        max_line_len = max(len(line1), len(line2))
        line1 = line1.ljust(max_line_len)
        line2 = line2.ljust(max_line_len)

        mixed_line = ''.join(
            random.choice([char1, char2])
            for char1, char2 in zip(line1, line2)
        )
        new_glif.append(mixed_line)

    return '\n'.join(new_glif)
