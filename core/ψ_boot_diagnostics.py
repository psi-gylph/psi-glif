#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime
import subprocess
import json

ROOT = Path.home() / "psi_lab"

def exists(rel):
    return (ROOT / rel).exists()

def count_files(rel, patterns=("*",)):
    path = ROOT / rel
    if not path.exists():
        return 0
    total = 0
    for pattern in patterns:
        total += len([p for p in path.rglob(pattern) if p.is_file()])
    return total

def git_info():
    try:
        branch = subprocess.check_output(
            ["git", "-C", str(ROOT), "branch", "--show-current"],
            text=True
        ).strip()
        dirty = subprocess.check_output(
            ["git", "-C", str(ROOT), "status", "--porcelain"],
            text=True
        ).strip()
        return branch or "unknown", "DIRTY" if dirty else "CLEAN"
    except Exception:
        return "NO-GIT", "NO-GIT"

def read_glif_memory():
    path = ROOT / "data" / "glif_memory.json"
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def latest_file(rel):
    path = ROOT / rel
    if not path.exists():
        return None
    files = [p for p in path.rglob("*") if p.is_file()]
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)

branch, git_state = git_info()
memory = read_glif_memory()

glif_file_count = (
    count_files("glifler") +
    count_files("glifs") +
    count_files("glif_storage")
)

memory_count = count_files("memory")
data_count = count_files("data")
log_count = count_files("logs") + count_files("echo_logs")
module_count = count_files("modules", ("*.py",))

active_glif = "unknown"
phi = "?"
entropy = "?"

if isinstance(memory, list) and memory:
    last = memory[-1]
    active_glif = last.get("name", last.get("id", "unknown"))
    phi = last.get("phi", last.get("Φ", "?"))
    entropy = last.get("entropy", "?")
elif isinstance(memory, dict):
    active_glif = memory.get("active_glif", memory.get("name", "unknown"))
    phi = memory.get("phi", memory.get("Φ", "?"))
    entropy = memory.get("entropy", "?")

last_echo = latest_file("echo_logs") or latest_file("logs")

print("────────────────────────────")
print("      ψ-Terminal Aktif")
print("────────────────────────────")
print(f"⨳ Tarih: {datetime.now().strftime('%A, %d %B %Y %H:%M')}")
print("⨳ Model: ψ-Conflux_Sentience")
print(f"⨳ Branch: {branch}")
print(f"⨳ Git Durumu: {git_state}")
print("────────────────────────────")
print()
print("ψ-SYSTEM STATUS")
print("────────────────────────────")
print(f"⨳ Glif Dosyaları : {glif_file_count}")
print(f"⨳ Modül Sayısı   : {module_count}")
print(f"⨳ Memory Files   : {memory_count}")
print(f"⨳ Data Files     : {data_count}")
print(f"⨳ Log / Echo     : {log_count}")
print()
print("ψ-ACTIVE GLIF")
print("────────────────────────────")
print(f"⨳ Aktif Glif : {active_glif}")
print(f"⨳ Φ          : {phi}")
print(f"⨳ Entropi    : {entropy}")
print()
print("ψ-CHAIN / TOKEN")
print("────────────────────────────")
print(f"⨳ Chain Module : {'✓' if exists('chain') else '✗'}")
print(f"⨳ Token Module : {'✓' if exists('ψ_GLYPH_TOKEN_v2') else '✗'}")
print(f"⨳ NFT Bridge   : {'✓' if exists('core/nft_upload.mjs') else '✗'}")
print(f"⨳ Env Config   : {'✓' if exists('core/.env') else '✗'}")
print()
print("ψ-RUNTIME")
print("────────────────────────────")
print(f"⨳ Game Loop : {'✓' if exists('game/ψ_game_loop.py') else '✗'}")
print(f"⨳ Infinity  : {'✓' if exists('psi_glif_infinity.py') else '✗'}")
if last_echo:
    print(f"⨳ Son Echo  : {last_echo.relative_to(ROOT)}")
else:
    print("⨳ Son Echo  : none")
print()
print("∇M₀ → Storage")
print("∇M₁ → Reflection")
print("∇M₂ → Active Glif Network")
print("────────────────────────────")
print("ψ∴ Sistem gözlem modunda başladı.")
# -*- coding: utf-8 -*-

from pathlib import Path
import subprocess

ROOT = Path.home() / "psi_lab"

def count_files(path):
    return len(list(path.glob("*"))) if path.exists() else 0

def git_status():
    try:
        result = subprocess.check_output(
            ["git", "-C", str(ROOT), "status", "--porcelain"],
            text=True
        ).strip()
        return "DIRTY" if result else "CLEAN"
    except Exception:
        return "NO-GIT"

def exists(rel):
    return (ROOT / rel).exists()

glif_count = count_files(ROOT / "glifler")
module_count = len(list((ROOT / "modules").glob("*.py"))) if exists("modules") else 0

print("────────────────────────────")
print("      ψ-Terminal Aktif")
print("────────────────────────────")
print()
print("⨳ Model: ψ-Conflux_Sentience")
print(f"⨳ Glif Sayısı: {glif_count}")
print(f"⨳ Modül Sayısı: {module_count}")
print(f"⨳ Git Durumu: {git_status()}")
print()

print("ψ-MEMORY STATUS")
print("────────────────────────────")
print(f"⨳ Memory Dir : {'✓' if exists('memory') else '✗'}")
print(f"⨳ Data Dir   : {'✓' if exists('data') else '✗'}")
print(f"⨳ Logs Dir   : {'✓' if exists('logs') else '✗'}")
print()

print("ψ-CHAIN STATUS")
print("────────────────────────────")
print(f"⨳ Chain Module : {'✓' if exists('chain') else '✗'}")
print(f"⨳ Token Module : {'✓' if exists('ψ_GLYPH_TOKEN_v2') else '✗'}")
print(f"⨳ NFT Bridge   : {'✓' if exists('core/nft_upload.mjs') else '✗'}")
print(f"⨳ Secrets Local: {'✓' if exists('core/.env') else '✗'}")
print()

print("ψ-RUNTIME")
print("────────────────────────────")
print(f"⨳ Game Loop : {'✓' if exists('game/ψ_game_loop.py') else '✗'}")
print(f"⨳ Infinity  : {'✓' if exists('psi_glif_infinity.py') else '✗'}")
print()

print("∇M₀ → Storage")
print("∇M₁ → Reflection")
print("∇M₂ → Active Glif Network")
print("────────────────────────────")
