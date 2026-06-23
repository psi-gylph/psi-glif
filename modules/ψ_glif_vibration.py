import math
import time
from ascii_utils import fade_ascii  # fade işlemleri için gerekli

class GlifTitreşim:
    def __init__(self, frequency=0.8, decay=0.95):
        self.amplitude = 1.0
        self.frequency = frequency
        self.decay = decay

    def vibrate(self, ascii_glif):
        lines = ascii_glif.split("\n")
        print("ψ∴SIMETRI_BREAK titreşimi başlatıldı...")
        step = 0
        while self.amplitude > 0.01:
            offset = self.amplitude * math.sin(self.frequency * step)
            faded = fade_ascii(lines, -offset) if offset < 0 else fade_ascii(lines, offset)
            print(faded)
            self.amplitude *= self.decay
            step += 1
            time.sleep(0.2)
        print("ψ∴ Glif titreşimi sona erdi. Sessizlik başlıyor...")
