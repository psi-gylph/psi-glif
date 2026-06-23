#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ~/psi_lab/game/ψ_game_loop.py

import os
import sys
import math
from datetime import datetime

# ─────────────────────────────────────────
#  MODÜL YOLLARI
# ─────────────────────────────────────────
BASE_DIR = os.path.expanduser("~/psi_lab")
sys.path.append(os.path.join(BASE_DIR, "modules"))
sys.path.append(os.path.join(BASE_DIR, "core"))

# ─────────────────────────────────────────
#  ÇEKİRDEK GLIF MODÜLLERİ
# ─────────────────────────────────────────
from ψ_glif_memory import (
    save_glif,
    load_all_glifs,
    GlifIdentity,
    GlifOperationType,
)
from ascii_glif import generate_ascii_glif           # seed → ASCII
from ψ_glif_mutation import mutate_glif             # küçük mutasyon
from ψ_glif_utils import synthesize_glif            # iki glif → sentez
from ψ_resonance_mapper import calculate_resonance  # rezonans hesabı
from ψ_entropy import entropy_level                 # entropi hesabı

# ─────────────────────────────────────────
#  ÜST KATMAN (PLACEHOLDER) MODÜLLER
# ─────────────────────────────────────────
try:
    from ψ_time_engine import run_time_cycle        # ψ-time döngüsü
except ImportError:
    def run_time_cycle(active_glif):
        print("[ψ-time] Henüz implemente edilmedi (run_time_cycle).")
        return None

try:
    from ψ_value_engine import compute_value_score  # Φ + entropi + rezonans → değer
except ImportError:
    def compute_value_score(glif_meta):
        """
        Basit placeholder:
        value_score ≈ 0.5 * entropi + 2 * phi
        """
        ent = float(glif_meta.get("entropy", 0.0))
        phi = float(glif_meta.get("phi", 0.0))
        return round(0.5 * ent + 2 * phi, 3)

# ─────────────────────────────────────────
#  GLOBAL STATE
# ─────────────────────────────────────────
STATE = {
    "glifs": [],          # load_all_glifs() çıktısı (dict listesi)
    "active_index": None  # aktif glifin index'i
}

# ============================================================
#    YARDIMCI FONKSİYONLAR
# ============================================================

def _refresh_glifs():
    """Diskten glifleri tekrar yükle ve STATE'i güncelle."""
    STATE["glifs"] = load_all_glifs()
    if STATE["glifs"] and STATE["active_index"] is None:
        STATE["active_index"] = len(STATE["glifs"]) - 1


def _get_active_glif():
    """Aktif glifi (dict) döndürür, yoksa None."""
    if STATE["active_index"] is None:
        return None
    if not STATE["glifs"]:
        return None
    if not (0 <= STATE["active_index"] < len(STATE["glifs"])):
        return None
    return STATE["glifs"][STATE["active_index"]]


def compute_phi_from_entropy(ent: float) -> float:
    """
    Basit bir φ modeli:
      - entropi çok düşük → donuk/sıkıcı → φ düşük
      - entropi çok yüksek → gürültü → φ yine düşük
      - orta seviyede bir tepe var (Gaussian gibi)
    """
    center = 3.0   # deneysel merkez (ASCII gürültü seviyene göre ayarlanır)
    width = 1.0    # yayılım
    x = (ent - center) / width
    phi = math.exp(-0.5 * x * x)
    return float(phi)


def status_panel():
    """Her menü öncesi üstte görünen durum barı."""
    ag = _get_active_glif()
    if ag is None:
        print("Aktif Glif: (yok)   |   Φ: 0.00   Entropi: 0.00")
    else:
        name = ag.get("seed") or ag.get("name") or "unknown"
        phi = float(ag.get("phi_score", 0.0))
        ent = float(ag.get("entropy_level", 0.0))
        print(f"Aktif Glif: {name}   |   Φ: {phi:.2f}   Entropi: {ent:.2f}")

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


def _resolve_glif_choice(glifs, user_input: str):
    """
    Kullanıcının girdiği değeri index ya da isim olarak yorumlar:
      1) önce int dene → index
      2) olmazsa isim eşleştirmesi yap
    """
    # 1) Index dene
    try:
        i = int(user_input)
        if 0 <= i < len(glifs):
            return i
    except ValueError:
        pass

    # 2) İsimle bul
    for idx, g in enumerate(glifs):
        name = g.get("seed") or g.get("name")
        if name == user_input:
            return idx

    return None

# ============================================================
#    KOMUTLAR
# ============================================================

def cmd_create_glif():
    seed = input("\n∇ Yeni Glif İsmi / Tetikleyici: ").strip()
    if not seed:
        print("[ψ] Boş seed kullanılamaz.")
        return

    # ASCII üret
    ascii_form = generate_ascii_glif(seed)

    # Kimlik oluştur
    identity = GlifIdentity(seed=seed, operation=GlifOperationType.CREATED)

    # Entropi & φ
    ent = entropy_level(ascii_form)
    phi = compute_phi_from_entropy(ent)
    identity.entropy_level = ent
    identity.phi_score = phi

    # Kaydet
    save_glif(ascii_form, identity)

    # STATE güncelle
    _refresh_glifs()
    # Yeni eklenen genelde listenin sonunda olacak
    # id eşleştirmesi de yapabiliriz:
    for idx, g in enumerate(STATE["glifs"]):
        if g.get("id") == identity.id:
            STATE["active_index"] = idx
            break
    else:
        # bulunamazsa son glifi aktif yap
        STATE["active_index"] = len(STATE["glifs"]) - 1

    print(f"\n[ψ] Yeni glif üretildi ({seed})")
    print("----------------------------------------")
    print(ascii_form)
    print("----------------------------------------")
    print(f"Φ (phi): {phi:.2f} | Entropi: {ent:.2f}")


def cmd_select_from_memory():
    _refresh_glifs()
    if not STATE["glifs"]:
        print("[ψ] Hafızada glif yok.")
        return

    print("\n[ψ] Hafızadaki glifler:")
    for idx, g in enumerate(STATE["glifs"]):
        name = g.get("seed") or g.get("name") or "noname"
        gid = g.get("id", "?")
        phi = float(g.get("phi_score", 0.0))
        ent = float(g.get("entropy_level", 0.0))
        print(f"{idx}: {name} | id={gid} | Φ={phi:.2f} | Entropi={ent:.2f}")

    choice = input("Seç (index ya da isim): ").strip()
    idx = _resolve_glif_choice(STATE["glifs"], choice)
    if idx is None:
        print("[ψ] Geçersiz seçim (ne index ne de isim eşleşmedi).")
        return

    STATE["active_index"] = idx
    ag = _get_active_glif()

    name = ag.get("seed") or ag.get("name") or f"glif_{idx}"
    ascii_form = ag.get("ascii", "")
    phi = float(ag.get("phi_score", 0.0))
    ent = float(ag.get("entropy_level", 0.0))

    print(f"\n[ψ] Aktif glif seçildi → {name}")
    print("----------------------------------------")
    print(ascii_form)
    print("----------------------------------------")
    print(f"Φ (phi): {phi:.2f} | Entropi: {ent:.2f}")


def cmd_list_memory():
    _refresh_glifs()
    if not STATE["glifs"]:
        print("[ψ] Hafızada glif yok.")
        return

    print("\n[ψ] Kaydedilen Glifler:")
    print("----------------------------------------")
    for g in STATE["glifs"]:
        name = g.get("seed") or g.get("name", "noname")
        pid = g.get("id", "?")
        phi = float(g.get("phi_score", 0.0))
        ent = float(g.get("entropy_level", 0.0))
        op = g.get("operation", "unknown")
        print(f"→ {name} | id={pid} | op={op} | Φ={phi:.2f} | Entropi={ent:.2f}")
    print("----------------------------------------")


def cmd_inspect_active():
    ag = _get_active_glif()
    if ag is None:
        print("[ψ] Aktif glif yok.")
        return

    print("\n[ψ] Aktif Glif Durumu")
    print("----------------------------------------")
    for k, v in ag.items():
        print(f"{k}: {v}")
    print("----------------------------------------")
    # İleride: Σ–Ξ–Φ, parents, resonance_history vb. buraya açılabilir.


def cmd_vibrate():
    base = _get_active_glif()
    if base is None:
        print("[ψ] Önce bir glif seç.")
        return

    ascii_form = base.get("ascii", "")
    if not ascii_form:
        print("[ψ] Aktif glifte ASCII içerik yok.")
        return

    print("\n[ψ] Titreşim uygulanıyor (küçük mutasyon)...")
    mutated = mutate_glif(ascii_form)

    base_name = base.get("seed") or base.get("name") or "glif"
    new_name = f"{base_name}_vib"

    identity = GlifIdentity(seed=new_name, operation=GlifOperationType.RESONANCE)

    ent = entropy_level(mutated)
    phi = compute_phi_from_entropy(ent)
    identity.entropy_level = ent
    identity.phi_score = phi

    # soy ağacı için parent ekle
    if "id" in base:
        identity.parents = [base["id"]]

    save_glif(mutated, identity)
    _refresh_glifs()
    # yeni glifi aktif yap
    for idx, g in enumerate(STATE["glifs"]):
        if g.get("id") == identity.id:
            STATE["active_index"] = idx
            break

    print(mutated)
    print(f"\n[ψ] Yeni titreşim glifi → {new_name}")
    print(f"Φ (phi): {phi:.2f} | Entropi: {ent:.2f}")


def cmd_synthesize():
    _refresh_glifs()
    if len(STATE["glifs"]) < 2:
        print("[ψ] Sentez için en az 2 glif gerekiyor.")
        return

    print("\n[ψ] Sentezlenecek iki glifi seç:")
    for idx, g in enumerate(STATE["glifs"]):
        name = g.get("seed") or g.get("name", "noname")
        print(f"{idx}: {name}")

    try:
        i1 = int(input("Glif 1 index: ").strip())
        i2 = int(input("Glif 2 index: ").strip())
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
    new_name = f"{g1.get('seed') or g1.get('name','g1')}_x_{g2.get('seed') or g2.get('name','g2')}"

    identity = GlifIdentity(seed=new_name, operation=GlifOperationType.SYNTHESIZED)
    # parents
    parents = []
    if "id" in g1:
        parents.append(g1["id"])
    if "id" in g2:
        parents.append(g2["id"])
    identity.parents = parents

    ent = entropy_level(synthesized_ascii)
    phi = compute_phi_from_entropy(ent)
    identity.entropy_level = ent
    identity.phi_score = phi

    save_glif(synthesized_ascii, identity)
    _refresh_glifs()
    for idx, g in enumerate(STATE["glifs"]):
        if g.get("id") == identity.id:
            STATE["active_index"] = idx
            break

    print("\n[ψ] Yeni sentez glif üretildi:", new_name)
    print("----------------------------------------")
    print(synthesized_ascii)
    print("----------------------------------------")
    print(f"Φ (phi): {phi:.2f} | Entropi: {ent:.2f}")


def cmd_resonance_map():
    _refresh_glifs()
    if len(STATE["glifs"]) < 2:
        print("[ψ] Rezonans için en az 2 glif gerekiyor.")
        return

    print("\n[ψ] Rezonans hesaplanacak iki glifi seç:")
    for idx, g in enumerate(STATE["glifs"]):
        name = g.get("seed") or g.get("name", "noname")
        print(f"{idx}: {name}")

    try:
        i1 = int(input("Glif 1 index: ").strip())
        i2 = int(input("Glif 2 index: ").strip())
    except ValueError:
        print("[ψ] Geçersiz seçim.")
        return

    if not (0 <= i1 < len(STATE["glifs"]) and 0 <= i2 < len(STATE["glifs"])):
        print("[ψ] Aralık dışında seçim.")
        return

    g1 = STATE["glifs"][i1]
    g2 = STATE["glifs"][i2]

    # ψ_resonance_mapper implementasyonuna göre:
    score = calculate_resonance(g1, g2)

    print("\n[ψ-Rezonans]")
    print(f"A: {g1.get('seed') or g1.get('name')}  |  B: {g2.get('seed') or g2.get('name')}")
    print(f"Rezonans skoru: {score:.3f}")


def cmd_time_cycle():
    ag = _get_active_glif()
    if ag is None:
        print("[ψ] Önce bir aktif glif seç.")
        return
    print("\n[ψ-time] Zaman döngüsü çalıştırılıyor...")
    result = run_time_cycle(ag)
    print("[ψ-time] Çıktı:", result)


def cmd_value_token():
    ag = _get_active_glif()
    if ag is None:
        print("[ψ] Aktif glif yok.")
        return

    ent = float(ag.get("entropy_level", 0.0))
    phi = float(ag.get("phi_score", 0.0))
    meta = {"entropy": ent, "phi": phi}

    value = compute_value_score(meta)

    print("\n[ψ-value] Glif Değeri / Token Simülasyonu")
    name = ag.get("seed") or ag.get("name", "noname")
    print(f"Glif: {name}  →  value_score = {value}")
    print(f"(entropy={ent:.2f}, phi={phi:.2f})")


def cmd_spiral_ritual():
    """Mini otomatik run: küçük mutasyon + rezonans + değer raporu."""
    base = _get_active_glif()
    if base is None:
        print("[ψ] Ritüel için önce bir aktif glif seç.")
        return

    print("\n[ψ-Ritüel] Spiral-Warp başlıyor...")

    # 1) Mutasyon
    ascii_base = base.get("ascii", "")
    mutated_ascii = mutate_glif(ascii_base)
    child_name = (base.get("seed") or base.get("name") or "glif") + "_warp"

    identity = GlifIdentity(seed=child_name, operation=GlifOperationType.RESONANCE)
    ent = entropy_level(mutated_ascii)
    phi = compute_phi_from_entropy(ent)
    identity.entropy_level = ent
    identity.phi_score = phi
    if "id" in base:
        identity.parents = [base["id"]]

    save_glif(mutated_ascii, identity)
    _refresh_glifs()
    child = None
    for g in STATE["glifs"]:
        if g.get("id") == identity.id:
            child = g
            break

    # 2) Rezonans (base vs child)
    res = calculate_resonance(base, child) if child is not None else 0.0

    # 3) Değer hesapla
    meta = {"entropy": ent, "phi": phi, "resonance": res}
    val = compute_value_score(meta)

    print("\n[ψ-Ritüel] Sonuç")
    print("----------------------------------------")
    print(mutated_ascii)
    print("----------------------------------------")
    print(f"Φ (phi): {phi:.2f} | Entropi: {ent:.2f} | Rezonans: {res:.3f}")
    print(f"Value score: {val}")
    print("[ψ-Ritüel] Spiral-Warp tamamlandı.")

# ============================================================
#    ANA DÖNGÜ
# ============================================================

def run_game_loop():
    _refresh_glifs()
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
