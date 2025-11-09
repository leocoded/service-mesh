from web3 import Web3
import json
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class BlockchainService:
    def __init__(self):
        # Conectar a Polygon Amoy via Infura
        infura_project_id = os.getenv('INFURA_PROJECT_ID')
        self.infura_url = f"https://polygon-amoy.infura.io/v3/{infura_project_id}"
        self.w3 = Web3(Web3.HTTPProvider(self.infura_url))
        
        # Verificar conexión
        if self.w3.is_connected():
            print("✅ Conectado a Polygon Amoy blockchain")
            print(f"📊 Último bloque: {self.w3.eth.block_number}")
        else:
            print("❌ Error conectando a Polygon Amoy")
    
    def create_trace_record(self, lote_id: str, event_type: str, ipfs_hash: str) -> Dict[str, Any]:
        """Crear registro en blockchain (simulado por ahora)"""
        try:
            # Por ahora simulamos la transacción
            # En producción aquí iría el smart contract
            
            block_number = self.w3.eth.block_number
            
            # Simular hash de transacción
            tx_hash = f"0x{hash(f'{lote_id}{event_type}{ipfs_hash}'):x}"[-40:]
            
            return {
                "tx_hash": f"0x{tx_hash}",
                "block_number": block_number,
                "network": "polygon-amoy",
                "status": "confirmed",
                "gas_used": 21000  # Simulado
            }
            
        except Exception as e:
            print(f"Error en blockchain: {e}")
            return {
                "tx_hash": f"0x{hash(lote_id):x}"[-40:],
                "block_number": 0,
                "network": "polygon-amoy",
                "status": "failed",
                "error": str(e)
            }
    
    def verify_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Verificar transacción en blockchain"""
        try:
            # En producción verificaría la transacción real
            return {
                "verified": True,
                "confirmations": 12,
                "network": "polygon-amoy"
            }
        except Exception as e:
            return {
                "verified": False,
                "error": str(e)
            }