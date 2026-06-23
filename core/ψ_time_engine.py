# ~/psi_lab/core/ψ_time_engine.py
# ψ-Time Engine v0.1
#
# Amaç:
# - Aktif glifin ASCII bedenini küçük zaman adımlarıyla "akıtmak"
# - Her adımda entropi ve Φ (phi) ölçmek
# - Kısa bir zaman-iz raporu üretmek

import math

from ψ_entropy import entropy_level  # modules klasöründen geliyor


def compute_phi_from_entropy(ent: float) -> float:
    """
    Basit bir Φ modeli:
    - entropi çok düşük → donuk, düşük φ
    - entropi çok yüksek → gürültü, yine düşük φ
    - orta seviyede (merkez ~3) bir tepe var
    """
    center = 3.0
    width = 1.0
    x = (ent - center) / width
    phi = math.exp(-0.5 * x * x)
    return float(phi)


def _time_step(ascii_art: str) -> str:
    """
    Küçük, deterministik bir 'zaman adımı':
    - Her satırı indexine göre sağa kaydırıyoruz.
    - Böylece zaman ilerledikçe desen akıyor ama bozulmuyor.
    """
    lines = ascii_art.splitlines()
    if not lines:
        return ascii_art

    new_lines = []
    for idx, line in enumerate(lines):
        if not line:
            new_lines.append(line)
            continue
        shift = (idx + 1) % len(line)  # satır indexine göre kayma
        new_line = line[shift:] + line[:shift]
        new_lines.append(new_line)

    return "\n".join(new_lines)


def run_time_cycle(glif: dict, steps: int = 5) -> str:
    """
    ψ_game_loop içinden çağrılan ana zaman fonksiyonu.
    Girdi:
        glif: dict (load_all_glifs() çıktısı gibi)
    Çıktı:
        Çok satırlı bir rapor string'i (terminalde okunabilir).
    """
    ascii_art = glif.get("ascii", "")
    if not ascii_art:
        return "[ψ-time] Bu glifin ASCII gövdesi yok, zaman akışı uygulanamadı."

    name = glif.get("seed") or glif.get("name") or "unnamed"
    psi_id = glif.get("id", "∅")

    report_lines = []
    report_lines.append("ψ-Time Cycle Report")
    report_lines.append(f"Glif: {name} | id={psi_id}")
    report_lines.append("-" * 50)

    current_ascii = ascii_art

    for t in range(steps):
        ent = entropy_level(current_ascii)
        phi = compute_phi_from_entropy(ent)

        # Önizleme için bir satır al (t'ye göre)
        lines = current_ascii.splitlines()
        preview = lines[t % len(lines)] if lines else ""

        report_lines.append(
            f"t={t} | Φ={phi:.2f} | Entropi={ent:.2f} | preview: {preview}"
        )

        # Bir sonraki adım için zamanı ilerlet
        current_ascii = _time_step(current_ascii)

    report_lines.append("-" * 50)
    report_lines.append("ψ-time: döngü tamamlandı.")

    return "\n".join(report_lines)
