# 🔹 Save as: ~/psi_lab/modules/global_events.py

from ψ_trace import ψ_trace

def log_create(glif_id, metadata):
    ψ_trace.record("CREATE", glif_id, metadata)

def log_synthesize(glif_id, parent_ids, score):
    ψ_trace.record("SYNTH", glif_id, {
        "parents": parent_ids,
        "resonance_score": score
    })

def log_resonance(glif_a, glif_b, score):
    ψ_trace.record("RESONANCE", glif_a, {
        "partner": glif_b,
        "score": score
    })

def log_visualization(glif_id, format_used):
    ψ_trace.record("VISUAL", glif_id, {
        "output_format": format_used
    })

def log_feedback(glif_id, phi, entropy, action):
    ψ_trace.record("FEEDBACK", glif_id, {
        "phi": phi,
        "entropy": entropy,
        "action": action
    })
