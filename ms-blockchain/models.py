from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class EventType(str, Enum):
    LOTE_CREATED = "LOTE_CREATED"
    LOTE_UPDATED = "LOTE_UPDATED"
    LOTE_RESERVED = "LOTE_RESERVED"
    PRODUCTO_CREATED = "PRODUCTO_CREATED"
    BODEGA_MOVEMENT = "BODEGA_MOVEMENT"

class TraceRecord(BaseModel):
    trace_id: str
    lote_id: str
    event_type: EventType
    data: Dict[Any, Any]
    timestamp: datetime
    blockchain_tx: str
    ipfs_hash: str
    status: str

class TraceResponse(BaseModel):
    lote_id: str
    total_records: int
    records: list[TraceRecord]