from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
import json
from datetime import datetime
from typing import Dict, List
import threading
import time

app = FastAPI(
    title="MS-Analytics API",
    description="Microservicio de Analytics para Event-Mesh",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Almacén de métricas
metrics = {
    "total_events": 0,
    "events_by_type": {},
    "events_by_hour": {},
    "recent_events": []
}

def process_analytics_events():
    """Procesar eventos de analytics desde Redis"""
    print("📊 MS-Analytics iniciado - Procesando eventos...")
    
    while True:
        try:
            # Procesar eventos de diferentes tipos
            for event_type in ["medicine.lote.created", "medicine.producto.created", "medicine.lote.reserved"]:
                queue_key = f"analytics:{event_type}"
                
                # Obtener evento de Redis
                event_data = redis_client.rpop(queue_key)
                
                if event_data:
                    event = json.loads(event_data)
                    process_event(event)
            
            time.sleep(1)  # Polling cada segundo
            
        except Exception as e:
            print(f"❌ Error procesando analytics: {e}")
            time.sleep(5)

def process_event(event: Dict):
    """Procesar evento individual"""
    global metrics
    
    event_type = event.get("event_type", "unknown")
    timestamp = event.get("timestamp", datetime.now().isoformat())
    
    print(f"📈 Procesando evento analytics: {event_type}")
    
    # Actualizar métricas
    metrics["total_events"] += 1
    
    # Contar por tipo
    if event_type not in metrics["events_by_type"]:
        metrics["events_by_type"][event_type] = 0
    metrics["events_by_type"][event_type] += 1
    
    # Contar por hora
    hour = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:00')
    if hour not in metrics["events_by_hour"]:
        metrics["events_by_hour"][hour] = 0
    metrics["events_by_hour"][hour] += 1
    
    # Mantener eventos recientes (últimos 10)
    metrics["recent_events"].insert(0, {
        "event_type": event_type,
        "timestamp": timestamp,
        "source": event.get("source", "unknown")
    })
    
    if len(metrics["recent_events"]) > 10:
        metrics["recent_events"] = metrics["recent_events"][:10]

# Iniciar procesamiento en hilo separado
analytics_thread = threading.Thread(target=process_analytics_events, daemon=True)
analytics_thread.start()

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud del servicio"""
    return {"message": "MS-Analytics API activa", "timestamp": datetime.now()}

@app.get("/metrics", tags=["Analytics"])
async def get_metrics():
    """Obtener métricas de eventos"""
    return {
        "metrics": metrics,
        "timestamp": datetime.now()
    }

@app.get("/metrics/events-by-type", tags=["Analytics"])
async def get_events_by_type():
    """Métricas por tipo de evento"""
    return {
        "events_by_type": metrics["events_by_type"],
        "total_events": metrics["total_events"]
    }

@app.get("/metrics/timeline", tags=["Analytics"])
async def get_timeline():
    """Timeline de eventos por hora"""
    return {
        "timeline": metrics["events_by_hour"],
        "recent_events": metrics["recent_events"]
    }

@app.get("/health/redis", tags=["Health"])
async def redis_health():
    """Verificar conexión a Redis"""
    try:
        redis_client.ping()
        return {"status": "connected", "broker": "redis"}
    except Exception as e:
        return {"status": "disconnected", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)