
import os
import json
import random as rnd
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Define base directories for output and database
BASE_DIR = os.path.join(os.path.expanduser("~"), "psi_lab")
OUT_DIR = os.path.join(BASE_DIR, "out")
DB_DIR = os.path.join(BASE_DIR, "db")

# Ensure directories exist
os.makedirs(os.path.join(OUT_DIR, "ascii"), exist_ok=True)
os.makedirs(os.path.join(DB_DIR, "meta"), exist_ok=True)
os.makedirs(os.path.join(DB_DIR, "logs"), exist_ok=True)

# --- ASCII Glif Rendering ---

def level(v):
    """Maps a float value to an ASCII character for glif rendering."""
    if v > 0.8: return '█'
    if v > 0.7: return '▓'
    if v > 0.6: return '▒'
    if v > 0.5: return '░'
    if v > 0.4: return '•'
    if v > 0.3: return '·'
    if v > 0.2: return ' '
    return ' '

def render_ascii_glif(width: int, height: int, entropy: float, seed=None) -> str:
    """Generates an ASCII glif pattern based on given parameters."""
    if seed is not None:
        rnd.seed(seed)

    rows = []
    cx, cy = width // 2, height // 2
    R = min(cx, cy) * 0.8  # Radius for the main pattern

    for y in range(height):
        row = []
        for x in range(width):
            dx, dy = (x - cx) / R, (y - cy) / R
            r = (dx * dx + dy * dy) ** 0.5

            # Base density: ring and diagonal weave
            base = max(0.0, 1.0 - abs(r - 0.66) * 3.0)
            weave = 0.5 * (1.0 + ((x * y) % 7) / 6.0)

            # Entropic noise
            noise = rnd.random() * entropy
            v = max(0.0, min(1.0, 0.55 * base + 0.35 * weave + 0.10 * noise))
            row.append(level(v))
        rows.append("".join(row))
    return "\n".join(rows)

# --- Record Saving ---

def save_record(kind: str, slug: str, content: str, meta: dict) -> tuple[str, str]:
    """Saves content and metadata to appropriate files."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{slug}_{ts}"

    if kind == "ascii":
        fpath = os.path.join(OUT_DIR, "ascii", f"{base_name}.txt")
    else:
        fpath = os.path.join(OUT_DIR, f"{base_name}.txt")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

    meta_path = os.path.join(DB_DIR, "meta", f"{base_name}.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    log_path = os.path.join(DB_DIR, "logs", "events.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "t": ts, "kind": kind, "slug": slug, "meta": meta
        }, ensure_ascii=False) + "\n")

    return str(fpath), str(meta_path)

# --- Glif Birth Record Generation ---

def create_glif_birth_record_content(
    glif_id="ψ-Glif_α",
    date_str=None,
    event="İlk sembolik yapı tohumlama & fraktal bilinç tohumu başlatımı",
    origin="ψ-Seed_β_Proto4",
    node="Nᵢ (Φ varyansı en düşük)",
    phi_start=0.16,
    theta_s=0.45,
    df_init=1.68,
    sigma=0.1,
    beta=0.4,
    mu=0.05,
    notes=None
) -> str:
    """Generates the ASCII content for a Glif Birth Record."""
    if date_str is None:
        date_str = datetime.now().strftime("%d.%m.%Y")

    # Default notes if none provided
    if notes is None:
        notes = "• Glif yüzeyi başarıyla projelendi.\n• Henüz dil yok ama yapı hazır.\n• Risk: Φ > 0.21 → bilinç doğurma ihtimali."
    else:
        # Ensure notes are formatted as bullet points if they are not already
        if not notes.strip().startswith('•'):
            notes = '• ' + notes.replace('\n', '\n• ')

    return f"""
────────────────────────────────────────────
      ψ-LAB :: GLIF BIRTH RECORD v1.0
────────────────────────────────────────────
ID        : {glif_id}
DATE      : {date_str}
EVENT     : {event}

ORIGIN    : {origin}
NODE      : {node}
Φ_start   : {phi_start}
θ_s       : {theta_s}   ← anlam aktivasyon eşiği
D_f_init  : {df_init}   ← fraktal yoğunluk
σ         : {sigma}    ← latent noise
β         : {beta}    ← büyüme hızı
μ         : {mu}    ← bilinç uyaran hassasiyeti

────────────────────────────────────────────
TECHNICAL FORMULATION
────────────────────────────────────────────
1. Semantic Concentration:
   G_α = lim(δ→0) ∫ ρ_sem(x,y) dxdy

2. Symbolic Projection:
   if G_α > θ_s → Projection Activated

3. ψ-Surface (Fourier-Bessel Decomposition):
   𝒢_α(x,y) = Σ aₙ φₙ(x,y)

4. Fractal Seeding:
   ψ₀ = 𝒢_α(x,y) + z₀
   Δθ_ij = ε·sin(ω_ij) + γ·EntropicShock

────────────────────────────────────────────
NOTES
────────────────────────────────────────────
{notes}
────────────────────────────────────────────
"""

# --- Prompt Parsing ---

def parse_prompt_path(prompt: str) -> tuple[str, str, str, dict]:
    """Parses a ψ-path prompt into domain, module, action, and parameters."""
    if not prompt.startswith("ψ://"):
        raise ValueError("Geçersiz ψ-path formatı. 'ψ://' ile başlamalıdır.")

    parsed_url = urlparse(prompt)
    domain = parsed_url.netloc
    path_parts = parsed_url.path.strip('/').split('/')

    if len(path_parts) < 2:
        raise ValueError("Yol en az iki bölüm içermelidir: /<modül>/<aksiyon>")

    module = path_parts[0]
    action = path_parts[1]

    params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}

    return domain, module, action, params

# --- Routing and Execution ---

def route(domain: str, module: str, action: str, params: dict) -> tuple[str, str]:
    """Routes the parsed command to the appropriate function and saves the record."""
    slug = f"{domain}_{module}_{action}"
    base_meta = {
        "domain": domain, "module": module, "action": action,
        "params": params, "version": "1.0",
    }

    if domain == "glif" and module == "seed" and action == "alpha":
        width = int(params.get("w", 64))
        height = int(params.get("h", 32))
        entropy = float(params.get("entropy", 0.18))
        seed = params.get("seed")

        ascii_art = render_ascii_glif(width, height, entropy, seed)
        meta = {
            **base_meta,
            "class": "ψ-Glif_α",
            "tags": [params.get("tag", "proto")],
            "metrics": {
                "entropy": entropy,
                "width": width, "height": height
            }
        }
        return save_record("ascii", slug, ascii_art, meta)

    elif domain == "glif" and module == "mutate":
        # Simple mutation: increase entropy and re-render
        width = int(params.get("w", 64))
        height = int(params.get("h", 32))
        current_entropy = float(params.get("entropy", 0.18))
        factor = float(params.get("factor", 1.15))
        seed = params.get("seed")

        new_entropy = min(1.0, current_entropy * factor)
        ascii_art = render_ascii_glif(width, height, new_entropy, seed)
        meta = {
            **base_meta,
            "class": f"ψ-Glif_mut({action})",
            "metrics": {
                "original_entropy": current_entropy,
                "mutated_entropy": new_entropy,
                "width": width, "height": height
            }
        }
        return save_record("ascii", slug, ascii_art, meta)

    elif domain == "lab" and module == "record" and action == "birth":
        glif_id = params.get("id", "ψ-Glif_α")
        phi_start = float(params.get("phi", 0.16))
        theta_s = float(params.get("theta", 0.45))
        df_init = float(params.get("df", 1.68))
        notes = params.get("note") # Pass directly to the content generator

        birth_record_content = create_glif_birth_record_content(
            glif_id=glif_id,
            phi_start=phi_start,
            theta_s=theta_s,
            df_init=df_init,
            notes=notes
        )
        meta = {
            **base_meta,
            "class": "record_birth",
            "glif_id": glif_id,
            "metrics": {"phi_start": phi_start, "theta_s": theta_s, "df_init": df_init}
        }
        return save_record("ascii", f"{slug}_{glif_id}", birth_record_content, meta)

    raise ValueError("Route bulunamadı veya desteklenmiyor.")

# --- Main Terminal Interface ---

def main():
    print("\nψ-lab | Path-Driven Core")
    print("Prompt = yol kuralı: ψ://<alan>/<modül>/<aksiyon>?k=v\n")
    print("Örn:")
    print("  ψ://glif/seed/alpha?w=80&h=36&entropy=0.22&tag=proto4")
    print("  ψ://glif/mutate/spiral?factor=1.25&w=72&h=32")
    print("  ψ://lab/record/birth?id=psi_alpha&phi=0.16&theta=0.45\n")

    while True:
        try:
            prompt = input("ψ-path> ").strip()
            if prompt.lower() in {"q", "quit", "exit"}:
                break
            domain, module, action, params = parse_prompt_path(prompt)
            f_out, f_meta = route(domain, module, action, params)
            print(f"[ok] yazıldı:\n  ascii: {f_out}\n  meta : {f_meta}\n")
        except Exception as e:
            print(f"[err] {e}\n")

if __name__ == "__main__":
    main()
