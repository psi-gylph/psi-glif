#!/bin/bash

# Gerekli araçların yüklü olduğundan emin olun
if ! command -v npx &> /dev/null
then
    echo "npx bulunamadi. Lütfen Node.js ve npm kurulumunu kontrol edin."
    exit
fi

# Hardhat projesi oluştur
npx hardhat init ψ_GLYPH_TOKEN_v2_project

cd ψ_GLYPH_TOKEN_v2_project

# Gerekli bağımlılıkları yükle
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox @openzeppelin/contracts

# contracts klasörüne geç ve sözleşmeyi kopyala
mkdir contracts
cp ../contracts/ψ_GLYPH_TOKEN_v2.sol contracts/

# hardhat.config.js dosyasını düzenle
cat <<EOL > hardhat.config.js
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.20",
  networks: {
    sepolia: {
      url: "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID",
      accounts: ["YOUR_PRIVATE_KEY"]
    }
  }
};
EOL

# Deploy scripti oluştur
mkdir scripts
cat <<EOL > scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const Token = await hre.ethers.getContractFactory("ψ_GLYPH_TOKEN_v2");
  const token = await Token.deploy();

  await token.deployed();

  console.log("ψ_GLYPH_TOKEN_v2 deployed to:", token.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
EOL

echo "Kurulum tamamlandi. Deploy etmek için aşağıdaki komutu kullanın:"
echo "npx hardhat run scripts/deploy.js --network sepolia"
