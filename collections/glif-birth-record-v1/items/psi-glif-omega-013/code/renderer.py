#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ψ-GLIF_Ω_013 renderer
Safe public renderer: no API keys, no network calls.
"""

from pathlib import Path
import shutil
import time
import os
import sys
import json

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GOLD = "\033[38;5;220m"
BLUE = "\033[38;5;39m"
GREEN = "\033[38;5;114m"
PINK = "\033[38;5;205m"
CYAN = "\033[38;5;81m"
GRAY = "\033[38;5;244m"

ROOT = Path(__file__).resolve().parents[1]
GLYPH_TXT = ROOT / "ψ-GLIF_Ω_013.txt"
META_JSON = ROOT / "ψ-GLIF_Ω_013.meta.json"

def center(text: str) -> str:
    width = shutil.get_terminal_size((100, 40)).columns
    return "\n".join(line.center(width) for line in text.splitlines())

def colorize(text: str) -> str:
    lines = []
    palette = [BLUE, CYAN, GREEN, GOLD, PINK, GRAY]
    for idx, line in enumerate(text.splitlines()):
        lines.append(f"{palette[idx % len(palette)]}{line}{RESET}")
    return "\n".join(lines)

def load_meta() -> dict:
    if META_JSON.exists():
        return json.loads(META_JSON.read_text(encoding="utf-8"))
    return {}

def render(delay: float = 0.05) -> None:
    os.system("cls" if os.name == "nt" else "clear")
    meta = load_meta()
    glyph = GLYPH_TXT.read_text(encoding="utf-8") if GLYPH_TXT.exists() else "ψ-GLIF_Ω_013"

    print(center(BOLD + "ψ-GLIF_Ω_013 :: ENTROPIC REFLECTION BLOOM" + RESET))
    print(center(DIM + "Birth of Glif NFT / ψ-LAB / TR-DLP" + RESET))
    print()
    time.sleep(delay)

    print(center(colorize(glyph)))
    print()
    time.sleep(delay)

    params = meta.get("parameters", {})
    print(center(f"{GRAY}Φ={params.get('phi', '?')} | θ={params.get('theta_activation', '?')} | D_f={params.get('fractal_density', '?')} | leakage={params.get('entropic_leakage', '?')}{RESET}"))
    print(center(f"{GRAY}state={params.get('state', 'unknown')} | projection={params.get('symbolic_projection', 'unknown')}{RESET}"))
    print()
    print(center(f"{GOLD}CORE_SEED{RESET} / {BLUE}NESTED_VEIL{RESET} / {CYAN}ENTROPIC_VOID{RESET} / {GREEN}RESONANCE_RIDGE{RESET}"))

if __name__ == "__main__":
    try:
        render()
    except KeyboardInterrupt:
        sys.exit(0)
