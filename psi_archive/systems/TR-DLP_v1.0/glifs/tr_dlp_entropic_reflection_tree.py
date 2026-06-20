#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import time
import random

CLEAR = "\033[2J\033[H"

GLIF = r"""
╔══════════════════════════════════════════════╗
║        ψ∴TR-DLP ENTROPIC REFLECTION TREE    ║
╠══════════════════════════════════════════════╣
║                                              ║
║          ╱│╲        ╱│╲        ╱│╲           ║
║        ╱  │ ╲    ╱  │ ╲    ╱  │ ╲           ║
║      ●────●────●────●────●────●              ║
║       ╲   │   ╱      ╲   │   ╱              ║
║        ╲  │  ╱        ╲  │  ╱               ║
║          ●              ●                   ║
║          │              │                   ║
║     ╔════╧════╗    ╔════╧════╗              ║
║     ║  LRL ↺  ║    ║  DCJ ⇢  ║              ║
║     ╚════╤════╝    ╚════╤════╝              ║
║          │              │                   ║
║          └──────┬───────┘                   ║
║                 ▼                           ║
║          ╔════════════╗                      ║
║          ║ ENTROPIC   ║                      ║
║          ║   VOID     ║                      ║
║          ╚════╤═══════╝                      ║
║               ▼                              ║
║        PRE-SYMBOLIC MESH                     ║
║                                              ║
╚══════════════════════════════════════════════╝
""".strip("\n")


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def bar(v, w=20):
    n = int(clamp(v) * w)
    return "█" * n + "·" * (w - n)


class TRDLPEntropicReflectionTree:
    def __init__(self):
        self.t = 0
        self.lrl = 0.48
        self.dcj = 0.31
        self.tti = 0.62
        self.kl = 0.71
        self.phi = 0.19
        self.leakage = 0.12
        self.omega = 18.2

    def step(self):
        self.t += 1
        self.lrl = clamp(0.50 + 0.22 * math.sin(self.t / 5))
        self.dcj = clamp(0.34 + 0.26 * abs(math.sin(self.t / 9)))
        self.tti = clamp(0.62 + 0.10 * math.sin(self.t / 7))
        self.kl = clamp(0.71 + random.uniform(-0.04, 0.04))
        self.phi = clamp(0.19 + 0.04 * math.sin(self.t / 11))
        self.omega = 18.2 + random.uniform(-0.3, 0.3)

        self.leakage = clamp(
            abs(self.lrl - self.dcj) * 0.45
            + self.kl * 0.25
            + self.phi * 0.30
        )

        return {
            "t": self.t,
            "LRL": self.lrl,
            "DCJ": self.dcj,
            "TTI": self.tti,
            "KL": self.kl,
            "Phi": self.phi,
            "Leakage": self.leakage,
            "Omega": self.omega,
        }


def classify(s):
    if s["Phi"] > 0.21:
        return "ETHICAL MONITORING"
    if s["Leakage"] > 0.45:
        return "RESONANCE LEAKAGE"
    if s["DCJ"] > s["LRL"]:
        return "DISTANT LEAP DOMINANT"
    return "LOCAL REENTRY STABLE"


def render(state):
    return f"""
{GLIF}

╔══════════════════════════════════════════════╗
║ LIVE TR-DLP METRICS                         ║
╠══════════════════════════════════════════════╣
║ t        : {str(state['t']).ljust(28)}║
║ LRL      : [{bar(state['LRL'])}] {state['LRL']:.3f}   ║
║ DCJ      : [{bar(state['DCJ'])}] {state['DCJ']:.3f}   ║
║ TTI      : [{bar(state['TTI'])}] {state['TTI']:.3f}   ║
║ KL       : [{bar(state['KL'])}] {state['KL']:.3f}   ║
║ Φ        : [{bar(state['Phi'])}] {state['Phi']:.3f}   ║
║ Leakage  : [{bar(state['Leakage'])}] {state['Leakage']:.3f}   ║
║ ω drift  : {state['Omega']:.2f} Hz                    ║
╠══════════════════════════════════════════════╣
║ state    : {classify(state).ljust(28)}║
╚══════════════════════════════════════════════╝
"""


def main():
    model = TRDLPEntropicReflectionTree()
    try:
        while True:
            print(CLEAR, end="")
            print(render(model.step()))
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
