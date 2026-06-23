#!/bin/bash

# Ana klasör oluşturuluyor
mkdir -p ψ_GLYPH_TOKEN_v2/{contracts,scripts}

# Hardhat başlatılıyor
cd ψ_GLYPH_TOKEN_v2
npm init -y > /dev/null
npm install --save-dev hardhat @openzeppelin/contracts @nomicfoundation/hardhat-toolbox > /dev/null

# Hardhat yapılandırılıyor
npx hardhat init <<EOF
y
EOF

# Sözleşme dosyası yazılıyor
cat <<EOL > contracts/ψ_GLYPH_TOKEN_v2.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ψ_GLYPH_TOKEN_v2 is ERC20 {
    uint256 private constant _maxSupply = 3140000 * 10 ** 18;
    address private _owner;

    constructor() ERC20("ψ∴GLYPH_TOKEN", "GLYPH") {
        _owner = msg.sender;
        _mint(msg.sender, 1000000 * 10 ** 18);
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == _owner, "Only owner can mint");
        require(totalSupply() + amount <= _maxSupply, "Max supply exceeded");
        _mint(to, amount);
    }

    function maxSupply() external pure returns (uint256) {
        return _maxSupply;
    }
}
EOL

# Deploy script yazılıyor
cat <<EOL > scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const Token = await hre.ethers.getContractFactory("ψ_GLYPH_TOKEN_v2");
  const token = await Token.deploy();
  await token.deployed();
  console.log("ψ_GLYPH_TOKEN deployed to:", token.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
EOL

# Hardhat config ayarlanıyor (şablon olarak, bilgileri sen gireceksin)
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

echo "ψ-token_setup.sh tamamlandı."
echo "Şimdi hardhat.config.js içindeki bilgileri doldur ve çalıştır:"
echo "npx hardhat run scripts/deploy.js --network sepolia"
