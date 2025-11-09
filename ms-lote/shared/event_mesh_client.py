import httpx
import json
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class EventMeshClient:
    def __init__(self, event_mesh_url: str = "http://localhost:8009"):
        self.event_mesh_url = event_mesh_url
        self.service_name = "unknown"
    
    def set_service_name(self, service_name: str):
        """Configurar nombre del servicio"""
        self.service_name = service_name
    
    async def publish_event(self, event_type: str, data: Dict[Any, Any], key: str = None):
        """Publicar evento a través del Event-Mesh"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.event_mesh_url}/events/publish",
                    params={
                        "event_type": event_type,
                        "source": self.service_name
                    },
                    json=data,
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ Evento publicado: {event_type} → {result['destinations']}")
                    return True
                else:
                    logger.error(f"❌ Error publicando evento: {response.status_code}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error conectando a Event-Mesh: {e}")
            return False
    
    def publish_event_sync(self, event_type: str, data: Dict[Any, Any], key: str = None):
        """Versión síncrona para compatibilidad"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.publish_event(event_type, data, key))
        except RuntimeError:
            # Si no hay loop, crear uno nuevo
            return asyncio.run(self.publish_event(event_type, data, key))
    
    async def register_service(self, event_patterns: list):
        """Registrar servicio en Event-Mesh"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.event_mesh_url}/services/subscribe",
                    params={
                        "service_name": self.service_name,
                    },
                    json=event_patterns
                )
                
                if response.status_code == 200:
                    logger.info(f"📡 Servicio registrado: {self.service_name}")
                    return True
                    
        except Exception as e:
            logger.error(f"❌ Error registrando servicio: {e}")
            return False