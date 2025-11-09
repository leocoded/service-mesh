from confluent_kafka import Producer, Consumer
import json
import logging
from typing import Dict, Any, Callable

logger = logging.getLogger(__name__)

class KafkaEventClient:
    def __init__(self, bootstrap_servers: str = None):
        # Auto-detectar si estamos en Docker o local
        if bootstrap_servers is None:
            import os
            # Priorizar variable de entorno
            bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
            if not bootstrap_servers:
                # Si estamos en Docker, usar nombre del servicio
                if os.getenv('DOCKER_ENV') or os.path.exists('/.dockerenv'):
                    bootstrap_servers = "kafka:9092"
                else:
                    bootstrap_servers = "localhost:9092"
        self.bootstrap_servers = bootstrap_servers
        # Configuración con timeout corto para fallar rápido
        config = {
            'bootstrap.servers': bootstrap_servers,
            'socket.timeout.ms': 3000,
            'api.version.request.timeout.ms': 3000,
            'request.timeout.ms': 5000
        }
        try:
            self.producer = Producer(config)
            self.service_name = "unknown"
        except Exception as e:
            logger.error(f"❌ No se pudo conectar a Kafka: {e}")
            self.producer = None
            self.service_name = "unknown"
    
    def set_service_name(self, service_name: str):
        self.service_name = service_name
    
    def publish_event(self, event_type: str, data: Dict[Any, Any], key: str = None):
        """Publicar evento directo a Kafka"""
        if self.producer is None:
            logger.warning(f"⚠️ Kafka no disponible, evento {event_type} no enviado")
            return False
            
        try:
            event_data = {
                "event_type": event_type,
                "source": self.service_name,
                "timestamp": "2025-11-02T19:30:00",
                "data": data
            }
            
            self.producer.produce(
                topic=event_type,
                value=json.dumps(event_data),
                key=key or str(data.get("lote_id", ""))
            )
            self.producer.flush(timeout=3)
            
            logger.info(f"✅ Evento publicado: {event_type}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error publicando evento: {e}")
            return False
    
    def create_consumer(self, topics: list, group_id: str):
        """Crear consumer para topics específicos"""
        consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'latest'
        })
        consumer.subscribe(topics)
        return consumer
    
    def consume_events(self, topics: list, group_id: str, handlers: Dict[str, Callable]):
        """Consumir eventos con handlers específicos"""
        consumer = self.create_consumer(topics, group_id)
        
        try:
            while True:
                msg = consumer.poll(1.0)
                
                if msg is None:
                    continue
                    
                if msg.error():
                    logger.error(f"❌ Error consumer: {msg.error()}")
                    continue
                
                try:
                    event_data = json.loads(msg.value().decode('utf-8'))
                    event_type = msg.topic()
                    
                    if event_type in handlers:
                        handlers[event_type](event_data, msg.key().decode('utf-8') if msg.key() else None)
                    
                except Exception as e:
                    logger.error(f"❌ Error procesando evento: {e}")
                    
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()