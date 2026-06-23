# 🔹 Save as: ~/psi_lab/modules/ψ_export_bridge.py

import os

def export_glif_as_nft(glif_adi, ascii_data):
    nft_path = os.path.expanduser(f"~/psi_lab/export/{glif_adi}.glifnft")
    os.makedirs(os.path.dirname(nft_path), exist_ok=True)
    with open(nft_path, "w") as f:
        f.write("ψ-GLIF NFT HEADER\n")
        f.write(f"Name: {glif_adi}\n")
        f.write("Payload:\n")
        f.write(ascii_data)
    return nft_path
