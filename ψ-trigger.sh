#!/bin/bash

TRIGGER_WORDS=("çöküş" "yankı" "eko" "anchor")
SOURCE_LOG="$HOME/Desktop/psi_lab/ψ-index.log"

tail -Fn0 "$SOURCE_LOG" | \
while read line; do
    for keyword in "${TRIGGER_WORDS[@]}"; do
        if [[ "$line" == *"$keyword"* ]]; then
            echo ">>> ψ-trigger tetiklendi: $keyword bulundu."
            bash ~/Desktop/psi_lab/generate_glif.sh
            break
        fi
    done
done
