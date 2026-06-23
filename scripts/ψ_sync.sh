#!/bin/bash

FOLDER="$1"
LOGDIR="$HOME/psi_lab/logs"
MODEL="${OPENAI_MODEL:-gpt-4o-mini}"

: "${OPENAI_API_KEY:?OPENAI_API_KEY tanımlı değil. Önce export OPENAI_API_KEY=... yap.}"

mkdir -p "$LOGDIR"

for file in "$FOLDER"/*; do
  [ -f "$file" ] || continue
  FILENAME=$(basename "$file")
  CONTENT=$(cat "$file")

  echo "Gönderiliyor: $FILENAME"

  RESPONSE=$(curl -s https://api.openai.com/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d "{
      \"model\": \"$MODEL\",
      \"messages\": [
        {\"role\": \"system\", \"content\": \"Sen ψ_lab veritabanı yöneticisisin. Gelen dosyayı analiz et.\"},
        {\"role\": \"user\", \"content\": \"$CONTENT\"}
      ],
      \"temperature\": 0.3
    }")

  echo "$RESPONSE" > "$LOGDIR/${FILENAME}.response.json"
done
