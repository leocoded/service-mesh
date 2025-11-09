import json
from confluent_kafka import Consumer
from typing import Callable, Dict, Any
import logging

logger = logging.getLogger(__name__)

class EventConsumer:
    def __init__(self, topics: list, group_id: str, bootstrap_servers=None):
        if bootstrap_servers is None:
            import os
            bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'latest'
        })
        self.consumer.subscribe(topics)
        self.handlers = {}
    
    def register_handler(self, topic: str, handler: Callable):
        """Registrar handler para un topic específico"""
        self.handlers[topic] = handler
    
    def start_consuming(self):
        """Iniciar consumo de eventos"""
        logger.info("Iniciando consumo de eventos...")
        
        try:
            while True:
                msg = self.consumer.poll(1.0)
                
                if msg is None:
                    continue
                if msg.error():
                    logger.error(f"Error en mensaje: {msg.error()}")
                    continue
                
                topic = msg.topic()
                key = msg.key().decode('utf-8') if msg.key() else None
                data = json.loads(msg.value().decode('utf-8'))
                
                logger.info(f"Evento recibido de topic '{topic}': {key}")
                
                if topic in self.handlers:
                    self.handlers[topic](data, key)
                else:
                    logger.warning(f"No hay handler para topic: {topic}")
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()
    
    def close(self):
        self.consumer.close()