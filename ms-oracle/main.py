from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from datetime import datetime, date
import random
import threading
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from shared.kafka_client import KafkaEventClient

app = FastAPI(
    title="MS-Oracle API",
    description="Microservicio Oracle para validaciones externas",
    version="1.0.0"
)

# Kafka client para eventos
kafka_client = KafkaEventClient()
kafka_client.set_service_name("ms-oracle")

def validate_temperature_conditions(data: Dict[Any, Any]) -> Dict[str, Any]:
    """Validar condiciones de temperatura para el lote"""
    temp_optima = data.get("temperatura_optima", 5.0)
    tipo_almacenamiento = data.get("tipo_almacenamiento", "refrigerado")
    
    # Simular lectura de sensores externos
    temp_actual = random.uniform(temp_optima - 2, temp_optima + 3)
    
    # Validaciones según tipo de almacenamiento
    validations = {
        "refrigerado": {"min": 2, "max": 8},
        "congelado": {"min": -20, "max": -15},
        "ambiente": {"min": 15, "max": 25},
        "seco": {"min": 10, "max": 30}
    }
    
    limits = validations.get(tipo_almacenamiento, {"min": 0, "max": 50})
    is_valid = limits["min"] <= temp_actual <= limits["max"]
    
    return {
        "temperatura_actual": round(temp_actual, 2),
        "temperatura_optima": temp_optima,
        "rango_valido": limits,
        "cumple_condiciones": is_valid,
        "alerta": not is_valid,
        "timestamp": datetime.now().isoformat()
    }

def validate_expiration_date(data: Dict[Any, Any]) -> Dict[str, Any]:
    """Validar fecha de vencimiento contra estándares farmacéuticos"""
    fecha_vencimiento = data.get("fecha_vencimiento")
    
    if isinstance(fecha_vencimiento, str):
        fecha_venc = datetime.fromisoformat(fecha_vencimiento).date()
    else:
        fecha_venc = fecha_vencimiento
    
    dias_restantes = (fecha_venc - date.today()).days
    
    # Clasificación según días restantes
    if dias_restantes < 0:
        status = "VENCIDO"
        risk_level = "CRITICO"
    elif dias_restantes <= 30:
        status = "PROXIMO_VENCIMIENTO"
        risk_level = "ALTO"
    elif dias_restantes <= 90:
        status = "MONITOREO"
        risk_level = "MEDIO"
    else:
        status = "VIGENTE"
        risk_level = "BAJO"
    
    return {
        "fecha_vencimiento": fecha_venc.isoformat(),
        "dias_restantes": dias_restantes,
        "status": status,
        "nivel_riesgo": risk_level,
        "requiere_accion": dias_restantes <= 30,
        "timestamp": datetime.now().isoformat()
    }

def validate_market_price(data: Dict[Any, Any]) -> Dict[str, Any]:
    """Validar precios contra mercado farmacéutico"""
    producto_id = data.get("producto_id", "UNKNOWN")
    
    # Simular consulta a API de precios farmacéuticos
    precio_mercado = random.uniform(50, 500)
    precio_referencia = precio_mercado * random.uniform(0.8, 1.2)
    
    variacion = ((precio_mercado - precio_referencia) / precio_referencia) * 100
    
    return {
        "producto_id": producto_id,
        "precio_mercado": round(precio_mercado, 2),
        "precio_referencia": round(precio_referencia, 2),
        "variacion_porcentual": round(variacion, 2),
        "precio_competitivo": abs(variacion) <= 15,
        "timestamp": datetime.now().isoformat()
    }

def handle_lote_created(data: Dict[Any, Any], key: str):
    """Handler para validar lotes recién creados"""
    print(f"🔍 Oracle validando lote: {key}")
    
    lote_data = data["data"]
    
    # Ejecutar validaciones
    temp_validation = validate_temperature_conditions(lote_data)
    expiry_validation = validate_expiration_date(lote_data)
    price_validation = validate_market_price(lote_data)
    
    # Consolidar resultados
    oracle_result = {
        "lote_id": key,
        "validaciones": {
            "temperatura": temp_validation,
            "vencimiento": expiry_validation,
            "precio": price_validation
        },
        "score_general": calculate_quality_score(temp_validation, expiry_validation, price_validation),
        "timestamp": datetime.now().isoformat()
    }
    
    # Publicar resultado de validación
    kafka_client.publish_event(
        event_type="oracle.validation.completed",
        data=oracle_result,
        key=key
    )
    
    print(f"✅ Validación Oracle completada: Score {oracle_result['score_general']}/100")

def calculate_quality_score(temp_val: dict, exp_val: dict, price_val: dict) -> int:
    """Calcular score de calidad basado en validaciones"""
    score = 0
    
    # Temperatura (40 puntos)
    if temp_val["cumple_condiciones"]:
        score += 40
    
    # Vencimiento (40 puntos)
    risk_scores = {"BAJO": 40, "MEDIO": 30, "ALTO": 15, "CRITICO": 0}
    score += risk_scores.get(exp_val["nivel_riesgo"], 0)
    
    # Precio (20 puntos)
    if price_val["precio_competitivo"]:
        score += 20
    
    return min(score, 100)

def start_event_consumer():
    """Iniciar consumer de eventos Oracle"""
    handlers = {
        "medicine.lote.created": handle_lote_created
    }
    
    kafka_client.consume_events(
        topics=["medicine.lote.created"],
        group_id="oracle-service",
        handlers=handlers
    )

@app.on_event("startup")
async def startup_event():
    """Iniciar consumer al arrancar la aplicación"""
    consumer_thread = threading.Thread(target=start_event_consumer, daemon=True)
    consumer_thread.start()
    print("🔮 MS-Oracle iniciado - Validando eventos...")

@app.get("/", tags=["Health"])
async def root():
    """Endpoint de salud del servicio"""
    return {"message": "MS-Oracle API activa", "timestamp": datetime.now()}

@app.post("/validate/temperature", tags=["Validaciones"])
async def validate_temperature(data: dict):
    """Validar condiciones de temperatura"""
    return validate_temperature_conditions(data)

@app.post("/validate/expiration", tags=["Validaciones"])
async def validate_expiration(data: dict):
    """Validar fecha de vencimiento"""
    return validate_expiration_date(data)

@app.post("/validate/price", tags=["Validaciones"])
async def validate_price(data: dict):
    """Validar precios de mercado"""
    return validate_market_price(data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)