# ~/psi_lab/game/ψ_resonance_mapper.py

def calculate_resonance(glifA, glifB):
    """
    İki glif arasındaki benzerliği ASCII üzerinden hesaplar.
    Basit ama çalışır bir rezonans prototipi:
    - aynı pozisyondaki eşleşme sayısı / uzunluk
    """

    asciiA = glifA.get("ascii", "")
    asciiB = glifB.get("ascii", "")

    if not asciiA or not asciiB:
        return 0.0

    min_len = min(len(asciiA), len(asciiB))
    matches = 0

    for i in range(min_len):
        if asciiA[i] == asciiB[i]:
            matches += 1

    raw_score = matches / min_len

    # normalize: 0 → düşük rezonans / 1 → yüksek
    return float(round(raw_score, 3))
