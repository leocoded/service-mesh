import json
import hashlib
from typing import Dict, Any

class IPFSService:
    def __init__(self):
        # Por ahora simulamos IPFS
        # En producción usarías un nodo IPFS real
        self.storage = {}
        print("📁 IPFS Service iniciado (simulado)")
    
    def store_data(self, data: Dict[Any, Any]) -> str:
        """Almacenar datos en IPFS y retornar hash"""
        try:
            # Convertir datos a JSON
            json_data = json.dumps(data, sort_keys=True, default=str)
            
            # Generar hash simulado estilo IPFS
            hash_obj = hashlib.sha256(json_data.encode())
            ipfs_hash = f"Qm{hash_obj.hexdigest()[:44]}"
            
            # Almacenar localmente (simulación)
            self.storage[ipfs_hash] = {
                "data": data,
                "timestamp": data.get("timestamp"),
                "size": len(json_data)
            }
            
            print(f"📁 Datos almacenados en IPFS: {ipfs_hash}")
            return ipfs_hash
            
        except Exception as e:
            print(f"Error almacenando en IPFS: {e}")
            return f"Qm{hashlib.md5(str(data).encode()).hexdigest()[:44]}"
    
    def retrieve_data(self, ipfs_hash: str) -> Dict[Any, Any]:
        """Recuperar datos desde IPFS"""
        if ipfs_hash in self.storage:
            return self.storage[ipfs_hash]["data"]
        else:
            return {"error": "Datos no encontrados en IPFS"}
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Obtener información del almacenamiento"""
        total_files = len(self.storage)
        total_size = sum(item["size"] for item in self.storage.values())
        
        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "files": list(self.storage.keys())
        }