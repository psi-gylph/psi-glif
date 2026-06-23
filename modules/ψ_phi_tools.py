# 🔹 Save as: ~/psi_lab/modules/ψ_phi_tools.py

def compute_phi(identity):
    if identity.resonance_history:
        avg = sum([r["score"] for r in identity.resonance_history]) / len(identity.resonance_history)
    else:
        avg = 0.0
    identity.phi_score = round(avg / 100, 2)  # 0–1 arası normalize edilmiş Φ
    return identity.phi_score
