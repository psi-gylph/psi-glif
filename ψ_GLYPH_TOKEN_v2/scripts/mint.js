import hre from "hardhat";

async function main() {
  const contractAddress = process.env.GLYPH_CONTRACT_ADDRESS || "YOUR_CONTRACT_ADDRESS";
  const recipient = process.env.GLYPH_RECIPIENT_ADDRESS || "YOUR_RECIPIENT_ADDRESS";

  const amount = hre.ethers.parseUnits("100", 18);

  const GLYPH = await hre.ethers.getContractAt("GLYPH_TOKEN_v2", contractAddress);

  const tx = await GLYPH.mint(recipient, amount);
  console.log("GLYPH mint işlemi gönderildi:", tx.hash);

  await tx.wait();
  console.log("✅ 100 GLYPH gönderildi!");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

