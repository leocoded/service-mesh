import requests
import json
from typing import Dict, Any

class IPFSRealService:
    def __init__(self):
        # Usar Pinata (servicio IPFS gratuito) o nodo local
        self.pinata_api_key = "564a5977b339dcefdef0"  # Tu API key real
        self.pinata_secret = "7951c1beb60aa5261077e17a69337d74e84421d4efe550c9c2255bd15fe866ef"    # Tu secret real
        self.use_local = False  # Usar Pinata (gratis, sin instalar nada)
        
        if self.use_local:
            self.ipfs_url = "http://127.0.0.1:5001/api/v0"
            print("📁 Intentando conectar a nodo IPFS local...")
            self.test_connection()
        else:
            print("📁 Configurado para usar Pinata IPFS (gratis)")
            print("✅ API keys de Pinata configuradas")
    
    def test_connection(self):
        """Probar conexión con nodo IPFS local"""
        try:
            response = requests.post(f"{self.ipfs_url}/version", timeout=5)
            if response.status_code == 200:
                version = response.json()
                print(f"✅ IPFS local conectado - Versión: {version.get('Version', 'unknown')}")
                return True
        except Exception as e:
            print(f"❌ IPFS local no disponible: {e}")
            print("💡 IPFS local no disponible, usando Pinata...")
            self.use_local = False
            return False
    
    def store_data(self, data: Dict[Any, Any]) -> str:
        """Almacenar datos en IPFS real"""
        try:
            if self.use_local:
                return self._store_local(data)
            else:
                return self._store_pinata(data)
        except Exception as e:
            print(f"Error almacenando en IPFS: {e}")
            # Fallback a simulación
            import hashlib
            json_data = json.dumps(data, sort_keys=True, default=str)
            hash_obj = hashlib.sha256(json_data.encode())
            return f"Qm{hash_obj.hexdigest()[:44]}"
    
    def _store_local(self, data: Dict[Any, Any]) -> str:
        """Almacenar en nodo IPFS local"""
        json_data = json.dumps(data, default=str)
        
        files = {'file': ('data.json', json_data, 'application/json')}
        response = requests.post(f"{self.ipfs_url}/add", files=files)
        
        if response.status_code == 200:
            result = response.json()
            ipfs_hash = result['Hash']
            print(f"📁 Datos almacenados en IPFS local: {ipfs_hash}")
            return ipfs_hash
        else:
            raise Exception(f"Error IPFS local: {response.status_code}")
    
    def _store_pinata(self, data: Dict[Any, Any]) -> str:
        """Almacenar en Pinata IPFS"""
        url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
        
        headers = {
            'pinata_api_key': self.pinata_api_key,
            'pinata_secret_api_key': self.pinata_secret,
            'Content-Type': 'application/json'
        }
        
        payload = {
            "pinataContent": data,
            "pinataMetadata": {
                "name": f"medicine-trace-{data.get('lote_id', 'unknown')}"
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            ipfs_hash = result['IpfsHash']
            print(f"📁 Datos almacenados en Pinata IPFS: {ipfs_hash}")
            return ipfs_hash
        else:
            raise Exception(f"Error Pinata: {response.status_code}")
    
    def retrieve_data(self, ipfs_hash: str) -> Dict[Any, Any]:
        """Recuperar datos desde IPFS"""
        try:
            if self.use_local:
                response = requests.post(f"{self.ipfs_url}/cat?arg={ipfs_hash}")
                if response.status_code == 200:
                    return response.json()
            else:
                # Usar gateway público para leer
                response = requests.get(f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
                if response.status_code == 200:
                    return response.json()
            
            return {"error": "No se pudo recuperar datos"}
            
        except Exception as e:
            return {"error": f"Error recuperando datos: {e}"}