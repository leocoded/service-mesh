const { ethers } = require("hardhat");

async function main() {
  console.log("🚀 Deploying MedicineTraceability contract...");

  const MedicineTraceability = await ethers.getContractFactory("MedicineTraceability");
  const contract = await MedicineTraceability.deploy();

  await contract.waitForDeployment();

  const contractAddress = await contract.getAddress();
  
  console.log("✅ Contract deployed to:", contractAddress);
  console.log("🔗 Verify on PolygonScan:", `https://amoy.polygonscan.com/address/${contractAddress}`);
  
  // Guardar dirección del contrato
  const fs = require('fs');
  const contractInfo = {
    address: contractAddress,
    network: "polygon-amoy",
    deployedAt: new Date().toISOString()
  };
  
  fs.writeFileSync('contract-address.json', JSON.stringify(contractInfo, null, 2));
  console.log("📄 Contract address saved to contract-address.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });