from ψ_glif_mutation import mutate_glif
from ψ_glif_analytics import compute_phi
from ψ_glif_utils import synthesize_variant 

def feedback_loop(psi_id, resonance_logs, current_ascii):
    """
    φ değeri belirli eşik üstündeyse, sistem otomatik yeni glif türetir.
    """
    threshold = 0.65
    phi_val = compute_phi(resonance_logs, psi_id)
    if phi_val > threshold:
        print(f"[Ψ] φ={phi_val} eşik {threshold} üzeri → Yeni varyant sentezleniyor.")
        return synthesize_variant(current_ascii)
    else:
        print(f"[Ψ] φ={phi_val} düşük → Evrimsel geri bildirim yok.")
        return current_ascii
