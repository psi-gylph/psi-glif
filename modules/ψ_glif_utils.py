# ~/psi_lab/modules/ψ_glif_utils.py

import numpy as np
import random

from PIL import Image, ImageDraw, ImageFont
from global_events import ψ_trace

class GlifFeedbackEngine:
    THRESH = {"LOW":0.3, "MEDIUM":0.6, "HIGH":0.8}
   
    def evaluate(self, identity):
        phi = identity.phi_score
        ent = identity.entropy_level
       
        if phi < self.THRESH["LOW"]:
            identity.masking_barrier = True
            ψ_trace.record("FEEDBACK", identity.id, {"action": "barrier"})
            return "BARRIER"
       
        if phi > self.THRESH["HIGH"] and ent < 1.5:
            ψ_trace.record("FEEDBACK", identity.id, {"action": "self_mutation"})
            return "MUTATE"
       
        if phi > self.THRESH["MEDIUM"]:
            ψ_trace.record("FEEDBACK", identity.id, {"action": "resonance_boost"})
            return "BOOST"
       
        return "NONE"

def ascii_to_image(ascii_str, output_path="glif.png"):
    lines = ascii_str.strip().split('\n')
    font = ImageFont.load_default()
    width = max([font.getsize(line)[0] for line in lines])
    height = font.getsize(lines[0])[1] * len(lines)

    img = Image.new("RGB", (width + 20, height + 20), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    y = 10
    for line in lines:
        draw.text((10, y), line, font=font, fill=(0, 0, 0))
        y += font.getsize(line)[1]

    img.save(output_path)
    return output_path

def synthesize_glif(glif1, glif2):
    lines1 = glif1.strip().splitlines()
    lines2 = glif2.strip().splitlines()
    max_len = max(len(lines1), len(lines2))
    synthesized = ""

    for i in range(max_len):
        line1 = lines1[i % len(lines1)]
        line2 = lines2[i % len(lines2)]
        mixed_line = ""

        for a, b in zip(line1, line2):
            mixed_line += a if random.random() < 0.5 else b

        synthesized += mixed_line + "\n"

    return synthesized

def synthesize_variant(ascii_str):
    """
    Belirli bir ascii glifin varyasyonel sentezini üretir.
    Burada rastlantısal sapmalar yerine örüntüsel yeniden yapılandırmalar yapılabilir.
    """
    lines = ascii_str.splitlines()
    # Basit örnek: her satırı ters çevir
    new_lines = [line[::-1] for line in lines]
    return "\n".join(new_lines)

# Görsel filtreleme/bariyer
def validate_external(image_path):
    img = Image.open(image_path)
    if img.size[0] > 512 or img.size[1] > 512:
        return False
    if img.mode not in ["RGB", "L"]:
        return False
    return True

# Görseli ASCII'ye dönüştür
def convert_to_ascii(image_path, width=80):
    img = Image.open(image_path).convert("L")
    w, h = img.size
    ratio = h / w
    new_h = int(width * ratio * 0.5)
    img = img.resize((width, new_h))
    chars = "@%#*+=-:. "
    pixels = img.getdata()
    ascii_str = "".join(chars[p//25] for p in pixels)
    return "\n".join(ascii_str[i:i+width] for i in range(0, len(ascii_str), width))

# İki ASCII bloğunu satır satır birleşik hale getir
def merge_ascii(a1, a2):
    lines1 = a1.splitlines()
    lines2 = a2.splitlines()
    maxlen1 = max(len(line) for line in lines1)
    merged = []
    for i in range(max(len(lines1), len(lines2))):
        l1 = lines1[i] if i < len(lines1) else ""
        l2 = lines2[i] if i < len(lines2) else ""
        merged.append(l1.ljust(maxlen1) + "  " + l2)
    return "\n".join(merged)

# Glif sentez fonksiyonu
def external_synthesis(glif_ascii, image_path=None):
    base = glif_ascii
    if image_path:
        if not validate_external(image_path):
            raise ValueError("Dış görsel uygun değil — boyut/mode")
        img_ascii = convert_to_ascii(image_path, width=60)
        base = merge_ascii(glif_ascii, img_ascii)
    # Sonra mevcut sentez fonksiyonuna yönlendirebilirsin:
    return base

def external_synthesis(image_path, current_glif_ascii):
    """
    Dışarıdan alınan görseli, mevcut glif ASCII'siyle sentezler.
    Örneğin: görseli ASCII'ye dönüştürüp birleştirebilir.
    """
    img = Image.open(image_path).convert('L').resize((80, 80))
    arr = np.array(img)
    # Basit ASCII çeviri: parlaklık eşiklerine göre karakterler
    chars = "@%#*+=-:. "
    ascii_img = "\n".join(
        "".join(chars[pixel//25] for pixel in row)
        for row in arr
    )
    # Sadece mevcut glifle alt alta birleştirip geri döner
    return f"{current_glif_ascii}\n\n---\n{ascii_img}"

def external_synthesis(image_path, current_glif_ascii):
    chars = "@%#*+=-:. "
    img = Image.open(image_path).convert('L').resize((80, 40))
    arr = np.array(img)
    ascii_img = "\n".join(
        "".join(chars[pixel // 25] for pixel in row)
        for row in arr
    )
    return f"{current_glif_ascii}\n\n---\n{ascii_img}"

import time

def vibrate_interaction(current_glif):
    if not current_glif:
        print("[!] Henüz bir glif seçilmedi.")
        return

    freq_map = {
        'ψ': 5, '@': 4, '#': 3, '%': 2, '*': 1, '=': 1, '+': 1, '-': 1, '.': 0.5
    }

    score = sum(freq_map.get(char, 0) for char in current_glif)
    duration = min(max(score / 100, 1), 5)  # 1–5 saniye arası

    print(f"\n[ψ] Titreşim başlatılıyor… Rezonans Skoru: {score:.2f}")
    print(">>", end="", flush=True)

    for _ in range(int(duration * 10)):
        print("~", end="", flush=True)
        time.sleep(0.1)

    print("\n[ψ] Titreşim tamamlandı.")

def fade_ascii(lines, offset):
    """Offset [-1,1]: pozitifse parlaklaştır, negatifse soluklaştır."""
    result = []
    intensity = abs(offset)
    for line in lines:
        if offset > 0:
            # Shift glifi sağa
            pad = int(intensity * 5)
            result.append(" " * pad + line)
        else:
            # Soluklaştır: karakterleri . ile değiştir
            fade_pct = min(intensity, 1.0)
            transformed = "".join(c if random.random() > fade_pct else "." for c in line)
            result.append(transformed)
    return "\n".join(result)
