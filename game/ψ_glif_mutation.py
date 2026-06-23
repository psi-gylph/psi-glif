import random

def mutate_glif(glif_ascii):
    charset = ['@', '#', '*', '=', '-', '+', ':', '.', '%', 'ψ']
    lines = glif_ascii.split("\n")
    mutated_lines = []

    for line in lines:
        new_line = ""
        for char in line:
            if char in charset and random.random() < 0.12:
                new_line += random.choice(charset)
            else:
                new_line += char
        mutated_lines.append(new_line)

    return "\n".join(mutated_lines)
