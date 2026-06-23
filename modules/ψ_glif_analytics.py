def calculate_resonance(glif_a, glif_b, affect_a=None, affect_b=None):
    # eski overlap(score)
    score = ... 

    # affine varyasyon
    if affect_a and affect_b:
        # örneğin resignation farkı rezonans gücünü etkiler
        affect_score = 1 - abs(affect_a.get("resignation",0) - affect_b.get("resignation",0))
        score *= affect_score

    return round(score,2)

