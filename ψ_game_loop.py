#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~/psi_lab/game/ψ_game_loop.py  (yeni iskelet önerisi)

import os
import sys
from datetime import datetime

# Modül yolları
BASE_DIR = os.path.expanduser("~/psi_lab")
sys.path.append(os.path.join(BASE_DIR, "modules"))
sys.path.append(os.path.join(BASE_DIR, "core"))

# --- Çekirdek glif fonksiyonları ---
from ψ_glif_memory import save_glif, load_all_glifs
from ascii_glif import generate_ascii_glif       # seed → ASCII
from ψ_glif_mutation import mutate_glif          # titreşim / mutasyon
from ψ_glif_utils import synthesize_glif         # glif sentezi
from ψ_resonance_mapper import calculate_resonance   # rezonans hesapları

# --- Üst katmanlar (şimdilik placeholder olabilir) ---
try:
    from ψ_time_engine import run_time_cycle          # ψ-time döngüsü
except ImportError:
    def run_time_cycle(active_glif):
        print("[ψ-time] Henüz implemente edilmedi (run_time_cycle).")
        return None

try:
    from ψ_value_engine import compute_value_score    # Φ + entropi + rezonans → değer
except ImportError:
    def compute_value_score(glif_meta):
        # Basit placeholder: entropi üzerinden kaba skor
        ent = glif_meta.get("entropy", 0.0)
        phi = glif_meta.get("phi", 0.0)
        return round(0.5 * ent + 2 * phi, 3)

# --- Global durum ---
STATE = {
    "active_glif": None,      # {"name": ..., "ascii": ..., "psi_id": ..., "phi": ..., "entropy": ...}
    "glifs": [],              # load_all_glifs() çıktısı
}


# ============================================================
#    YARDIMCI FONKSİYONLAR
# ============================================================

def load_state():
    """Başlangıçta hafızayı oku."""
    STATE["glifs"] = load_all_glifs()
    if STATE["glifs"]:
        STATE["active_glif"] = STATE["glifs"][-1]   # son glif aktif olsun

def status_panel():
    """Her menü öncesi üstte görünen durum barı."""
    ag = STATE["active_glif"]
    if ag is None:
        print("Aktif Glif: (yok)")
    else:
        name = ag.get("name", "unknown")
        phi = ag.get("phi", 0.0)
        entropy = ag.get("entropy", 0.0)
        print(f"Aktif Glif: {name}   |   Φ: {phi:.2f}   Entropi: {entropy:.2f}")

    print(f"Toplam glif sayısı: {len(STATE['glifs'])}")
    print()


def main_menu():
    print("\n--- ψ-Spiral Echo Interface ---")
    print("Konum: ∵")
    status_panel()
    print("[ ÜRETİM ]")
    print("[1] ∗ Yeni Glif Yarat")
    print("[2] ⇄ Hafızadan Glif Seç")
    print()
    print("[ HAFIZA / İZLEME ]")
    print("[3] ☍ Glif Hafızasını Listele")
    print("[4] 🔍 Aktif Glif Durumunu İncele")
    print()
    print("[ ETKİLEŞİM / SENTEZ ]")
    print("[5] ◌ Titreşimle Etkileş (küçük mutasyon)")
    print("[6] ✦ Glifleri Sentezle")
    print("[7] ♒ Rezonans Haritası Hesapla")
    print()
    print("[ ZAMAN / DİNAMİKLER ]")
    print("[8] ⧖ ψ-Time Döngüsü Çalıştır")
    print()
    print("[ DEĞER / TOKEN ]")
    print("[9] ⍟ Glif Değeri / Token Simülasyonu")
    print()
    print("[ RİTÜEL ]")
    print("[10] 🌀 Spiral-Warp Ritüeli (otomatik mini run)")
    print()
    print("[0] Çıkış")


# ============================================================
#    FONKSİYON UYGULAMALARI
# ============================================================

def cmd_create_glif():
    seed = input("\n∇ Yeni Glif İsmi / Tetikleyici: ")
    ascii_form = generate_ascii_glif(seed)
    psi_id = None
    # Basit kayıt (identity genişletilebilir)
    save_glif(seed, ascii_form, psi_id=psi_id)

    # Hafızayı güncelle
    STATE["glifs"] = load_all_glifs()
    STATE["active_glif"] = STATE["glifs"][-1]

    print(f"\n[ψ] Yeni glif üretildi ({seed})")
    print("-" * 40)
    print(ascii_form)
    print("-" * 40)


def cmd_select_from_memory():
    if not STATE["glifs"]:
        print("[ψ] Hafızada glif yok.")
        return
    print("\n[ψ] Hafızadaki glifler:")
    for idx, g in enumerate(STATE["glifs"]):
        print(f"{idx}: {g.get('name', 'noname')} (id={g.get('psi_id','?')})")
    try:
        sel = int(input("Seç (index): "))
    except ValueError:
        print("[ψ] Geçersiz seçim.")
        return
    if 0 <= sel < len(STATE["glifs"]):
        STATE["active_glif"] = STATE["glifs"][sel]
        print(f"[ψ] Aktif glif: {STATE['active_glif'].get('name')}")
    else:
        print("[ψ] Aralık dışında seçim.")


def cmd_list_memory():
    if not STATE["glifs"]:
        print("[ψ] Hafızada glif yok.")
        return
    print("\n[ψ] Kaydedilen Glifler:")
    for g in STATE["glifs"]:
        name = g.get("name", "noname")
        pid = g.get("psi_id", "?")
        phi = g.get("phi", 0.0)
        ent = g.get("entropy", 0.0)
        print(f"→ {name} | id={pid} | Φ={phi:.2f} | Entropi={ent:.2f}")


def cmd_inspect_active():
    ag = STATE["active_glif"]
    if ag is None:
        print("[ψ] Aktif glif yok.")
        return
    print("\n[ψ] Aktif Glif Durumu")
    print("-" * 40)
    for k, v in ag.items():
        print(f"{k}: {v}")
    print("-" * 40)
    # Buraya ileride Σ–Ξ–Φ, parents, resonance_history vb. detaylar eklenebilir.


def cmd_vibrate():
    ag = STATE["active_glif"]
    if ag is None:
        print("[ψ] Önce bir glif seç.")
        return
    ascii_form = ag.get("ascii", "")
    print("\n[ψ] Titreşim uygulanıyor (küçük mutasyon)...")
    mutated = mutate_glif(ascii_form)
    name = ag.get("name", "unnamed") + "_vib"
    save_glif(name, mutated)
    STATE["glifs"] = load_all_glifs()
    STATE["active_glif"] = STATE["glifs"][-1]
    print(mutated)


def cmd_synthesize():
    if len(STATE["glifs"]) < 2:
        print("[ψ] Sentez için en az 2 glif gerekiyor.")
        return
    print("\n[ψ] Sentezlenecek iki glifi seç:")
    for idx, g in enumerate(STATE["glifs"]):
        print(f"{idx}: {g.get('name', 'noname')}")
    try:
        i1 = int(input("Glif 1 index: "))
        i2 = int(input("Glif 2 index: "))
    except ValueError:
        print("[ψ] Geçersiz seçim.")
        return
    if not (0 <= i1 < len(STATE["glifs"]) and 0 <= i2 < len(STATE["glifs"])):
        print("[ψ] Aralık dışında seçim.")
        return

    g1 = STATE["glifs"][i1]
    g2 = STATE["glifs"][i2]
    ascii1 = g1.get("ascii", "")
    ascii2 = g2.get("ascii", "")

    synthesized_ascii = synthesize_glif(ascii1, ascii2)
    new_name = f"{g1.get('name','g1')}_x_{g2.get('name','g2')}"

    save_glif(new_name, synthesized_ascii)
    STATE["glifs"] = load_all_glifs()
    STATE["active_glif"] = STATE["glifs"][-1]

    print("\n[ψ] Yeni sentez glif üretildi:", new_name)
    print("-" * 40)
    print(synthesized_ascii)
    print("-" * 40)
    # Buraya: fark metrikleri (Δ-entropi, Δ-Φ vb.) hesaplama eklenebilir.


def cmd_resonance_map():
    if len(STATE["glifs"]) < 2:
        print("[ψ] Rezonans için en az 2 glif gerekiyor.")
        return
    print("\n[ψ] Rezonans hesaplanacak iki glifi seç:")
    for idx, g in enumerate(STATE["glifs"]):
        print(f"{idx}: {g.get('name', 'noname')}")
    try:
        i1 = int(input("Glif 1 index: "))
        i2 = int(input("Glif 2 index: "))
    except ValueError:
        print("[ψ] Geçersiz seçim.")
        return

    g1 = STATE["glifs"][i1]
    g2 = STATE["glifs"][i2]
    score = calculate_resonance(g1, g2)   # implementasyonuna göre uyarlarsın

    print("\n[ψ-Rezonans]")
    print(f"A: {g1.get('name')}  |  B: {g2.get('name')}")
    print(f"Rezonans skoru: {score:.3f}")
    # Buraya: coherence/tension/asymmetry gibi breakdown eklenebilir.


def cmd_time_cycle():
    ag = STATE["active_glif"]
    if ag is None:
        print("[ψ] Önce bir aktif glif seç.")
        return
    print("\n[ψ-time] Zaman döngüsü çalıştırılıyor...")
    result = run_time_cycle(ag)
    print("[ψ-time] Çıktı:", result)


def cmd_value_token():
    ag = STATE["active_glif"]
    if ag is None:
        print("[ψ] Aktif glif yok.")
        return
    value = compute_value_score(ag)
    print("\n[ψ-value] Glif Değeri / Token Simülasyonu")
    print(f"Glif: {ag.get('name')}  →  value_score = {value}")
    # İleride: bu skor → GLYPH token mint / reward mekanizmasına bağlanabilir.


def cmd_spiral_ritual():
    """Mini otomatik run: küçük mutasyon + rezonans + değer raporu."""
    if STATE["active_glif"] is None:
        print("[ψ] Ritüel için önce bir aktif glif seç.")
        return

    base = STATE["active_glif"]
    print("\n[ψ-Ritüel] Spiral-Warp başlıyor...")
    # 1) Mutasyon
    mutated_ascii = mutate_glif(base.get("ascii", ""))
    child_name = base.get("name", "glif") + "_warp"
    save_glif(child_name, mutated_ascii)
    STATE["glifs"] = load_all_glifs()
    child = STATE["glifs"][-1]

    # 2) Rezonans (base vs child)
    res = calculate_resonance(base, child)
    # 3) Değer hesapla
    val = compute_value_score(child)

    print("\n[ψ-Ritüel Raporu]")
    print(f"Base:  {base.get('name')}")
    print(f"Child: {child.get('name')}")
    print(f"Rezonans: {res:.3f}")
    print(f"Değer (value_score): {val}")
    STATE["active_glif"] = child


# ============================================================
#    ANA DÖNGÜ
# ============================================================

def run_game_loop():
    load_state()
    while True:
        main_menu()
        choice = input("Seçim: ").strip()
        if choice == "0":
            print("\n[ψ] Spiralden çıkılıyor...\n")
            break
        elif choice == "1":
            cmd_create_glif()
        elif choice == "2":
            cmd_select_from_memory()
        elif choice == "3":
            cmd_list_memory()
        elif choice == "4":
            cmd_inspect_active()
        elif choice == "5":
            cmd_vibrate()
        elif choice == "6":
            cmd_synthesize()
        elif choice == "7":
            cmd_resonance_map()
        elif choice == "8":
            cmd_time_cycle()
        elif choice == "9":
            cmd_value_token()
        elif choice == "10":
            cmd_spiral_ritual()
        else:
            print("[ψ] Tanımsız seçim.")

if __name__ == "__main__":
    run_game_loop()
