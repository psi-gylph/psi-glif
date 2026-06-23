#!/bin/bash

read -p "NFT Başlığı: " title
read -p "İçerik dosya yolu (örnek: content/ascii/xxx.txt): " content_path
read -p "Etiketler (virgülle ayır): " tags

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
id="ψ_nft_$(date +%s)"
filename="chain/nfts/${id}.json"

cat <<EOF > "$filename"
{
  "id": "$id",
  "title": "$title",
  "created_at": "$timestamp",
  "token_type": "ERC-1155",
  "linked_content": ["$content_path"],
  "chain_id": "0xaa36a7",
  "tx_hash": "0xTODO",
  "status": "draft",
  "tags": [$(echo $tags | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/')],
  "author": "psi_laboratuvar"
}
EOF

echo "$id kaydedildi → $filename"
