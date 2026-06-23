# ~/psi_lab/modules/ψ_local_agent.py

import uuid
from datetime import datetime
from ψ_glif_memory import GlifIdentity, GlifOperationType
from ψ_entropy import entropy_level
from ψ_resonance_mapper import calculate_resonance
from global_events import log_create, log_resonance

def register_glif_identity(ascii_glif: str, seed: str, flux_signature: str) -> GlifIdentity:
    """
    Yeni glif için kimlik oluştur, entropi ve flux_signature ekle,
    create-log kaydı oluşturur.
    """
    identity = GlifIdentity(seed=seed, operation=GlifOperationType.CREATED)
    identity.flux_signature = flux_signature
    identity.entropy_level = entropy_level(ascii_glif)
    log_create(identity.id, {"seed": seed, "flux": flux_signature, "entropy": identity.entropy_level})
    return identity

def update_resonance(identity: GlifIdentity, other: GlifIdentity, ascii_a: str, ascii_b: str):
    """
    İki glif arasında rezonans hesapla, identity.resonance_history'e ekle
    ve global-event loglarına kaydet.
    """
    score = calculate_resonance(ascii_a, ascii_b)
    timestamp = datetime.now().isoformat()
    identity.resonance_history.append((timestamp, other.id, score))
    # aynı şekilde karşılıklı da ekleyebiliriz
    log_resonance(identity.id, other.id, score)
    return score
