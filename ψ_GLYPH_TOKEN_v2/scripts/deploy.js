async function main() {
  const Token = await ethers.getContractFactory("GLYPH_TOKEN_v2");
  const token = await Token.deploy();
  
  await token.waitForDeployment(); //
  
  console.log("GLYPH_TOKEN deployed to:", await token.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
