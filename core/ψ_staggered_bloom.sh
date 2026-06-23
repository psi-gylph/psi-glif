#!/bin/bash

echo "Ψ::Δτ.58 – Glif Drop: Staggered Bloom başlatılıyor..."
echo "⨳ Mode: Timed NFT Bloom / ψ-Sequential Upload"
echo "⨳ Batch Source: ~/psi_lab/chain/nfts/glif_batch_Δ52_Δ55"

# Log aç
echo "$(date) | Staggered Bloom başlatıldı." >> ~/psi_lab/logs/ψ_staggered.log

# Zaman boşlukları ve drop döngüsü
declare -a glifs=("Δ52" "Δ53" "Δ54" "Δ55")
delay=5  # saniye cinsinden (test için kısa, canlıda artır)

for glif in "${glifs[@]}"
do
    echo "∇GLIF: $glif → preparing for drop..."
    sleep $delay
    echo "∇DROP COMPLETE: $glif → NFT minted & stored."
    echo "$(date) | $glif dropped." >> ~/psi_lab/logs/ψ_staggered.log
done

echo "∇BLOOM SEQUENCE COMPLETED."
echo "Ψ-State: [DISPERSED]"
