# ~/psi_lab/modules/ψ_glif_memory.py

import os
import json
import uuid
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict

# Gliflerin saklandığı dizin
GLIF_DIR = os.path.expanduser("~/psi_lab/glif_storage")


class GlifOperationType(Enum):
    CREATED = "created"
    SYNTHESIZED = "synthesized"
    RESONANCE = "resonance"
    VISUALIZED = "visualized"


@dataclass
class GlifIdentity:
    """
    Glif'in kimlik ve metrik yapısı.
    """
    id: str
    seed: str
    timestamp: str
    parents: list
    operation: GlifOperationType

    phi_score: float = 0.0
    entropy_level: float = 0.0
    resonance_history: list = None
    masking_barrier: bool = False
    flux_signature: str | None = None
    fractal_depth: int = 0

    def __init__(self, seed: str, operation: GlifOperationType):
        self.id = str(uuid.uuid4())
        self.seed = seed
        self.timestamp = datetime.now().isoformat()
        self.parents = []
        self.operation = operation

        self.phi_score = 0.0
        self.entropy_level = 0.0
        self.resonance_history = []
        self.masking_barrier = False
        self.flux_signature = None
        self.fractal_depth = 0


def save_glif(ascii_form: str, identity: GlifIdentity):
    """
    Oyun içinden çağrılan ana kayıt fonksiyonu.
    ψ_game_loop.py içindeki çağrı ile bire bir uyumlu:
        save_glif(ascii_form, identity)
    """
    os.makedirs(GLIF_DIR, exist_ok=True)
    file_path = os.path.join(GLIF_DIR, f"{identity.id}.json")

    # GlifIdentity → dict
    data = asdict(identity)

    # Enum → string
    data["operation"] = identity.operation.value

    # ASCII içerik + okunabilir isim
    data["ascii"] = ascii_form
    data["name"] = identity.seed  # geriye dönük uyum için

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_all_glifs():
    """
    glif_storage içindeki tüm .json dosyalarını okuyup
    bozuk olanları atlayarak list döndürür.
    """
    glifs = []
    if not os.path.exists(GLIF_DIR):
        return glifs

    for filename in os.listdir(GLIF_DIR):
        if not filename.endswith(".json"):
            continue
        file_path = os.path.join(GLIF_DIR, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                glifs.append(data)
        except Exception as e:
            print(f"[ψ-WARN] Bozuk JSON atlandı: {file_path} → {e}")
            continue

    return glifs
def update_glif(glif_data: dict):
    """
    Var olan glif JSON dosyasını id üzerinden günceller.
    """
    glif_id = glif_data.get("id")
    if not glif_id:
        print("[ψ-WARN] update_glif: id yok, kayıt yapılamadı.")
        return False

    os.makedirs(GLIF_DIR, exist_ok=True)
    file_path = os.path.join(GLIF_DIR, f"{glif_id}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(glif_data, f, ensure_ascii=False, indent=2)

    return True
