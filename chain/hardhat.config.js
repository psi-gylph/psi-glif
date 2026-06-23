require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.28",
  networks: {
    sepolia: {
      url: "https://sepolia.infura.io/v3/",
      accounts: ["30477e1c00af48053c9a02f79ee94523beccfcf9e1c48fa7b78c804ddcac8ba5"]
    }
  }
};
