import os

def export_glif_as_nft(glif_ascii, glif_name):
    nft_path = os.path.expanduser(f"~/psi_lab/exported_nfts/{glif_name}.glif")
    os.makedirs(os.path.dirname(nft_path), exist_ok=True)

    with open(nft_path, "w") as f:
        f.write(glif_ascii)

    return nft_path
