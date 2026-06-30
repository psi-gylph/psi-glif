#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import uuid
import shutil
import hashlib
import math
from collections import Counter
from datetime import datetime

BASE_DIR = os.path.expanduser("~/psi_lab")
IMPORT_DIR = os.path.join(BASE_DIR, "imports")
ASSET_DIR = os.path.join(BASE_DIR, "imported_assets")
GLIF_DIR = os.path.join(BASE_DIR, "glif_storage")

SUPPORTED_EXT = {".png", ".mp4", ".ascii", ".txt", ".py", ".json"}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def estimate_entropy(text: str) -> float:
    if not text:
        return 0.0

    counts = Counter(text)
    total = len(text)
    entropy = 0.0

    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return round(entropy, 2)


def estimate_phi(text: str) -> float:
    if not text:
        return 0.0

    unique_ratio = len(set(text)) / max(len(text), 1)
    line_count = max(len(text.splitlines()), 1)
    density = min(len(text) / 1000, 1.0)
    structure = min(line_count / 20, 1.0)

    phi = 0.35 + density * 0.30 + structure * 0.20 + unique_ratio * 0.15
    return round(min(phi, 0.99), 2)


def import_external_glif(source_path: str, creator: str = "external_user"):
    source_path = os.path.expanduser(source_path)

    if not os.path.exists(source_path):
        raise FileNotFoundError(source_path)

    ext = os.path.splitext(source_path)[1].lower()
    if ext not in SUPPORTED_EXT:
        raise ValueError(f"Desteklenmeyen dosya tipi: {ext}")

    os.makedirs(IMPORT_DIR, exist_ok=True)
    os.makedirs(ASSET_DIR, exist_ok=True)
    os.makedirs(GLIF_DIR, exist_ok=True)

    file_hash = sha256_file(source_path)
    glif_id = str(uuid.uuid4())

    original_name = os.path.basename(source_path)
    safe_name = original_name.replace(" ", "_")
    asset_name = f"{glif_id}_{safe_name}"
    asset_path = os.path.join(ASSET_DIR, asset_name)

    shutil.copy2(source_path, asset_path)

    seed = os.path.splitext(safe_name)[0]

    ascii_content = ""
    if ext in {".ascii", ".txt", ".py", ".json"}:
        try:
            with open(source_path, "r", encoding="utf-8") as f:
                ascii_content = f.read()
        except Exception:
            ascii_content = ""

    entropy = estimate_entropy(ascii_content)
    phi = estimate_phi(ascii_content)

    data = {
        "id": glif_id,
        "seed": seed,
        "name": seed,
        "creator": creator,
        "timestamp": datetime.now().isoformat(),
        "operation": "external_import",
        "source_type": ext.replace(".", ""),
        "source_path": asset_path,
        "ascii": ascii_content,
        "sha256": file_hash,
        "parents": [],
        "phi_score": phi,
        "entropy_level": entropy,
        "resonance_history": [],
        "masking_barrier": False,
        "flux_signature": None,
        "fractal_depth": 0,
        "token_value": 0.0,
        "nft_status": "not_minted",
        "license": "creator_attested"
    }

    json_path = os.path.join(GLIF_DIR, f"{glif_id}.json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data
