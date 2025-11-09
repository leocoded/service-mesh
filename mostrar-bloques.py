#!/usr/bin/env python3
from web3 import Web3
import json

def mostrar_estado_blockchain():
    print("🔗 ESTADO ACTUAL DE LA BLOCKCHAIN")
    print("=" * 50)
    
    # Conectar a Ganache
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    
    if not w3.is_connected():
        print("❌ No conectado a Ganache")
        return
    
    print(f"✅ Conectado a Ganache")
    print(f"📊 Número de bloque actual: {w3.eth.block_number}")
    print(f"💰 Cuentas disponibles: {len(w3.eth.accounts)}")
    
    # Mostrar últimos bloques
    print(f"\n🧱 ÚLTIMOS BLOQUES:")
    current_block = w3.eth.block_number
    
    for i in range(max(0, current_block - 2), current_block + 1):
        try:
            block = w3.eth.get_block(i)
            print(f"   Bloque {i}:")
            print(f"   📅 Timestamp: {block.timestamp}")
            print(f"   🔢 Transacciones: {len(block.transactions)}")
            print(f"   🔗 Hash: {block.hash.hex()[:20]}...")
            print()
        except:
            print(f"   Bloque {i}: No disponible")
    
    # Mostrar transacciones recientes
    print(f"📝 TRANSACCIONES RECIENTES:")
    if current_block > 0:
        latest_block = w3.eth.get_block(current_block, full_transactions=True)
        if latest_block.transactions:
            for i, tx in enumerate(latest_block.transactions[-3:]):
                print(f"   TX {i+1}:")
                print(f"   🔗 Hash: {tx.hash.hex()[:20]}...")
                print(f"   👤 From: {tx['from'][:10]}...")
                print(f"   👥 To: {tx.to[:10] if tx.to else 'Contract'}...")
                print(f"   💰 Value: {w3.from_wei(tx.value, 'ether')} ETH")
                print()
        else:
            print("   No hay transacciones en el último bloque")
    
    # Mostrar balances
    print(f"💳 BALANCES DE CUENTAS:")
    for i, account in enumerate(w3.eth.accounts[:3]):
        balance = w3.eth.get_balance(account)
        balance_eth = w3.from_wei(balance, 'ether')
        print(f"   Cuenta {i}: {account[:10]}... = {balance_eth:.2f} ETH")

if __name__ == "__main__":
    mostrar_estado_blockchain()