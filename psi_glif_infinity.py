# -*- coding: utf-8 -*-
# psi_glif_infinity.py
# Terminalde animasyonlu "∞" (lemniskat) ASCII glifi üretir.
# İlk kareyi arşive kaydeder: ~/psi_lab/out/ascii/...
# Bağımlılık: Sadece Python stdlib

import os, sys, time, math, json
from pathlib import Path
from datetime import datetime

# ——— Klasör yapısı ———
ROOT = Path.home() / "psi_lab"
OUT_ASCII = ROOT / "out" / "ascii"
OUT_META  = ROOT / "db"  / "meta"
for p in (OUT_ASCII, OUT_META):
    p.mkdir(parents=True, exist_ok=True)

# ——— Yardımcılar ———
def nowstamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def save_snapshot(text, params):
    ts = nowstamp()
    f_txt = OUT_ASCII / f"psi_glif_infinity_{ts}.txt"
    f_meta = OUT_META / f"psi_glif_infinity_{ts}.json"
    f_txt.write_text(text, encoding="utf-8")
    f_meta.write_text(json.dumps({
        "title": "ψ-Glif_∞",
        "desc": "Lemniskat tabanlı nefes animasyonu (sonsuzluk glifi)",
        "timestamp": ts,
        "params": params
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(f_txt), str(f_meta)

def clear():
    # ANSI clear
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()

def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

# ——— Görselleştirme ———
# Palet: ikili (glif hissi) veya çok tonlu
PALETTE_BINARY = "░█"
PALETTE_TONAL  = " .:-=+*#%@"

def pick_char(v, palette=PALETTE_BINARY):
    i = int(clamp(v, 0.0, 1.0) * (len(palette)-1))
    return palette[i]

def render_infinity(width=92, height=36, phase=0.0, palette=PALETTE_BINARY):
    """
    Lemniskat (Bernoulli) için seviye-seti benzeri yoğunluk alanı:
    f(x,y) = (x^2 + y^2)^2 - a^2*(x^2 - y^2)  ~  0
    'a' parametresi fazla (sinüs) bağlı değişir → “nefes” efekti.
    """
    # Ekran → sürekli uzay eşlemesi (en-boy dengesi için x aralığı geniş)
    x_min, x_max = -2.1, 2.1
    y_min, y_max = -1.2, 1.2

    # Nefes: a(t)  ~  1.25 + 0.35*sin(phase)
    a = 1.25 + 0.35 * math.sin(phase)
    k = 0.35  # keskinlik
    rows = []

    for j in range(height):
        y = y_min + (y_max - y_min) * (j / (height - 1))
        row = []
        for i in range(width):
            x = x_min + (x_max - x_min) * (i / (width - 1))

            # Lemniskat seviye fonksiyonu (0'a yakınsa eğri üzeri)
            f = (x*x + y*y)**2 - (a*a)*(x*x - y*y)

            # Yoğunluk: 0'a yakın bölgeleri parlat, uzaklaştıkça sönümle
            intensity = math.exp(-abs(f)/k)

            # Merkez bağlantısını güçlendirmek için hafif “köprü” ekleyelim
            bridge = math.exp(-(x*x + (y*0.5)**2)/0.8) * 0.10

            v = clamp(intensity + bridge, 0.0, 1.0)
            row.append(pick_char(v, palette))
        rows.append("".join(row))
    return "\n".join(rows)

def animate(width=92, height=36, fps=16, palette=PALETTE_BINARY, duration=None, save_first=True):
    """
    duration=None → Ctrl+C ile durdur (sürekli)
    duration=10.0 → saniye bazlı
    """
    t0 = time.time()
    first_frame_saved = False
    params = {"width": width, "height": height, "fps": fps, "palette": "binary" if palette==PALETTE_BINARY else "tonal"}

    try:
        while True:
            t = time.time() - t0
            if duration is not None and t >= duration:
                break
            phase = t * 2.2  # nefes hızı
            art = render_infinity(width, height, phase, palette)
            clear()
            sys.stdout.write("ψ-Glif_∞  (q ile çık)\n")
            sys.stdout.write(art + "\n")
            sys.stdout.flush()

            if save_first and not first_frame_saved:
                f_txt, f_meta = save_snapshot(art, params)
                sys.stdout.write(f"\n[ok] İlk kare kaydedildi:\n  ascii: {f_txt}\n  meta : {f_meta}\n")
                first_frame_saved = True

            time.sleep(1.0 / fps)

    except KeyboardInterrupt:
        pass

# ——— CLI ———
if __name__ == "__main__":
    # Basit argüman okuyucu
    import argparse
    ap = argparse.ArgumentParser(description="ψ-Glif_∞ | animasyonlu lemniskat ASCII")
    ap.add_argument("--w", type=int, default=92, help="genişlik (kolon)")
    ap.add_argument("--h", type=int, default=36, help="yükseklik (satır)")
    ap.add_argument("--fps", type=int, default=16, help="fps")
    ap.add_argument("--seconds", type=float, default=None, help="süre (sn), boşsa sınırsız")
    ap.add_argument("--palette", type=str, default="binary", choices=["binary","tonal"], help="palet")
    args = ap.parse_args()

    pal = PALETTE_BINARY if args.palette == "binary" else PALETTE_TONAL
    animate(width=args.w, height=args.h, fps=args.fps, palette=pal, duration=args.seconds, save_first=True)
