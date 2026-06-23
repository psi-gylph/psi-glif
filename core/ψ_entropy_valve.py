# -*- coding: utf-8 -*-
"""
ψ-EntropyValve
Path: ~/psi_lab/core/ψ_entropy_valve.py

Torus tabanlı entropi regülatörü.
Glif çıktılarının stabilitesini değerlendirir, kaos → düzen dönüşümü sağlar.
"""

import math

class EntropyValve:
    def __init__(self, radial_profile, symmetry_lr, symmetry_tb):
        self.profile = radial_profile
        self.sym_lr  = symmetry_lr
        self.sym_tb  = symmetry_tb

        # Temel eşikler (deneysel)
        self.min_sym = 0.25      # altı kaotik
        self.mid_sym = 0.40      # ideal aralık
        self.high_sym = 0.70     # aşırı simetri → ölü alan

    def stability_index(self):
        """
        Torusun dalga biçimine göre genel stabilite ölçümü.
        0..1 arasında normalize skor.
        """
        radial_peak = max(self.profile)
        radial_var = sum(abs(self.profile[i] - self.profile[i-1])
                         for i in range(1, len(self.profile)))

        # Normalize
        peak_norm = radial_peak / 1.0
        var_norm  = math.exp(-radial_var)  # varyans arttıkça düşer
        sym_avg   = (self.sym_lr + self.sym_tb) / 2.0

        score = (0.50 * var_norm) + (0.30 * peak_norm) + (0.20 * sym_avg)
        return min(1.0, max(0.0, score))

    def regulate(self, Phi, entropy):
        """
        Bir glifin Φ (hayat değeri) ve entropisini torus alanında düzenler.
        Geri: yeni (Phi, entropy)
        """

        S = self.stability_index()

        # Faz dönüşümü
        if S < 0.30:
            # Kaotik bölge → container devreye girer
            Phi  *= 1.05          # güçlendirme
            entropy *= 0.85       # entropi azaltma

        elif S < 0.60:
            # İdeal bölge → yumuşak regülasyon
            Phi  *= 1.01
            entropy *= 0.95

        else:
            # Aşırı stabil → nefes ver
            Phi  *= 0.97
            entropy *= 1.05

        return round(Phi, 4), round(entropy, 4)
