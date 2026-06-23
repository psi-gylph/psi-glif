#!/bin/bash
FILENAME="yanki_$(date +%Y%m%d_%H%M%S).txt"
PHASE=$((RANDOM % 360))
INTENSITY=$(echo "scale=2; $RANDOM/32768" | bc)

cat << EOF > $FILENAME
ψ∴
Yankı ID: $(uuidgen)
Faz Açısı: $PHASE°
Yoğunluk: $INTENSITY
Tetik Noktası: $(date)
EOF

~/Desktop/psi_lab/psi_log.sh "Yeni yankı üretildi: $FILENAME"
