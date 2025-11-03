import json
from datetime import datetime
from confluent_kafka import Producer
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class EventPublisher:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            'client.id': 'service-mesh-publisher'
        })
    
    def publish(self, topic: str, data: Dict[Any, Any], key: str = None):
        """Publicar evento en Kafka"""
        try:
            message = {
                "timestamp": datetime.now().isoformat(),
                "data": data,
                "source": "service-mesh"
            }
            
            self.producer.produce(
                topic=topic,
                key=key,
                value=json.dumps(message)
            )
            self.producer.flush()
            
            logger.info(f"Evento publicado en topic '{topic}': {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error publicando evento: {e}")
            return False
    
    def close(self):
        self.producer.flush()