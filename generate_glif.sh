#!/bin/bash

FILENAME="glif_$(date +%Y%m%d_%H%M%S).txt"
OUTPUT_DIR=~/Desktop/psi_lab/glifler

echo "ψ-Glif Üretimi Başladı..."
sleep 1
echo "∴ Glif kodlaması tamamlandı."

cat << EOF > $OUTPUT_DIR/$FILENAME
ψ∴
Glif ID: $(uuidgen)
Zaman: $(date)
Frekans Sapması: $(echo "scale=5; $RANDOM/32768" | bc)
Entropy Vector: ψ-${RANDOM:0:4}
EOF

echo "Glif oluşturuldu: $FILENAME"
