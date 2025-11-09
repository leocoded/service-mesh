const { ethers } = require('ethers');

// Generar wallet aleatoria para pruebas
const wallet = ethers.Wallet.createRandom();

console.log('🔑 WALLET DE PRUEBA GENERADA:');
console.log('Address:', wallet.address);
console.log('Private Key:', wallet.privateKey);
console.log('');
console.log('📋 PASOS SIGUIENTES:');
console.log('1. Copia la Private Key al archivo .env');
console.log('2. Ve a https://faucet.polygon.technology/');
console.log('3. Solicita MATIC para Polygon Amoy testnet');
console.log('4. Usa esta address:', wallet.address);