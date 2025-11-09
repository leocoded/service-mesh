const { Web3 } = require('web3');
require('dotenv').config();

async function testConnection() {
    try {
        const web3 = new Web3(`https://polygon-amoy.infura.io/v3/${process.env.INFURA_PROJECT_ID}`);
        
        console.log('🔗 Probando conexión a Polygon Amoy...');
        
        const blockNumber = await web3.eth.getBlockNumber();
        console.log('✅ Conectado a Polygon Amoy, bloque:', blockNumber);
        
        const account = web3.eth.accounts.privateKeyToAccount(process.env.PRIVATE_KEY);
        console.log('👤 Address:', account.address);
        
        const balance = await web3.eth.getBalance(account.address);
        console.log('💰 Balance:', web3.utils.fromWei(balance, 'ether'), 'POL');
        
        console.log('🎉 Todo configurado correctamente!');
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
}

testConnection();