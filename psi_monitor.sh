#!/bin/bash

logfile=~/Desktop/psi_lab/ψ-index.log
echo "ψ-monitor aktif. Yankılar gözlemleniyor..."
tail -f "$logfile" | while read line
do
    if [[ "$line" == *"Glif"* ]]; then
        echo ">> [ψ-ALERT] Glif olay tespit edildi: $line"
        # Buraya sesli uyarı, görsel tetikleyici vs. eklenebilir
    fi
done
