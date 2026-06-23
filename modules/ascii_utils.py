import random

def fade_ascii(lines, offset):
    """
    ASCII glifi, verilen offset'e göre kaydırır veya soluklaştırır.
    Pozitif offset → sağa kaydırma
    Negatif offset → karakterleri "." ile soluklaştırma
    """
    result = []
    intensity = abs(offset)
    for line in lines:
        if offset > 0:
            pad = int(intensity * 5)
            result.append(" " * pad + line)
        else:
            fade_pct = min(intensity, 1.0)
            transformed = "".join(c if random.random() > fade_pct else "." for c in line)
            result.append(transformed)
    return "\n".join(result)

