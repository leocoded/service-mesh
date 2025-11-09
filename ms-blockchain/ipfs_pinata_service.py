import requests
import json
import os
from typing import Dict, Any

class IPFSPinataService:
    def __init__(self):
        self.api_key = os.getenv('PINATA_API_KEY')
        self.secret_key = os.getenv('PINATA_SECRET_API_KEY')
        self.base_url = "https://api.pinata.cloud"
        
    def store_data(self, data: Dict[Any, Any]) -> str:
        """Almacenar datos en IPFS usando Pinata"""
        try:
            url = f"{self.base_url}/pinning/pinJSONToIPFS"
            
            headers = {
                'pinata_api_key': self.api_key,
                'pinata_secret_api_key': self.secret_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                "pinataContent": data,
                "pinataMetadata": {
                    "name": f"medicine_trace_{data.get('lote_id', 'unknown')}"
                }
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                return result['IpfsHash']
            else:
                print(f"Error storing to Pinata: {response.text}")
                return f"ERROR_{response.status_code}"
                
        except Exception as e:
            print(f"Exception storing to Pinata: {e}")
            return f"ERROR_EXCEPTION"
    
    def retrieve_data(self, ipfs_hash: str) -> Dict[Any, Any]:
        """Recuperar datos desde IPFS usando Pinata Gateway"""
        try:
            url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
            response = requests.get(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to retrieve data: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Exception retrieving data: {e}"}
    
    def get_storage_info(self) -> Dict[str, Any]:
        """Obtener información del almacenamiento Pinata"""
        try:
            url = f"{self.base_url}/data/userPinnedDataTotal"
            
            headers = {
                'pinata_api_key': self.api_key,
                'pinata_secret_api_key': self.secret_key
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get storage info: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Exception getting storage info: {e}"}