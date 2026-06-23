from ψ_entropy_utils import entropy_level
from ψ_glif_mutation import mutate_glif

E_max = 0.85  # entropi eşiği (örnek)

def suppress_mutation(ascii_str):
    """
    Eğer entropi çok yüksekse mutasyonu bastırır.
    """
    ent = entropy_level(ascii_str)
    if ent > E_max:
        print(f"[!] Entropi {ent} > E_max. Mutasyon bastırıldı.")
        return True
    return False

