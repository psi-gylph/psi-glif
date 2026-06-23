import hre from "hardhat";

async function main() {
  const contractAddress = process.env.GLYPH_CONTRACT_ADDRESS || "YOUR_CONTRACT_ADDRESS";
  const wallet = process.env.GLYPH_WALLET_ADDRESS || "YOUR_WALLET_ADDRESS";

  const GLYPH = await hre.ethers.getContractAt("GLYPH_TOKEN_v2", contractAddress);

  const name = await GLYPH.name();
  const symbol = await GLYPH.symbol();
  const totalSupply = await GLYPH.totalSupply();
  const balance = await GLYPH.balanceOf(wallet);
  const maxSupply = await GLYPH.maxSupply();

  console.log("Name:", name);
  console.log("Symbol:", symbol);
  console.log("Total Supply:", hre.ethers.formatUnits(totalSupply, 18));
  console.log("Wallet Balance:", hre.ethers.formatUnits(balance, 18));
  console.log("Max Supply:", hre.ethers.formatUnits(maxSupply, 18));
}

main().catch(console.error);
