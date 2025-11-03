import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List

class DatabaseService:
    def __init__(self, db_path: str = "blockchain_index.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializar base de datos con tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de índices blockchain
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blockchain_index (
                trace_id TEXT PRIMARY KEY,
                lote_id TEXT,
                producto_id TEXT,
                codigo_barras TEXT,
                blockchain_tx TEXT,
                ipfs_hash TEXT,
                event_type TEXT,
                timestamp TEXT,
                block_number INTEGER,
                status TEXT,
                data_json TEXT
            )
        ''')
        
        # Índices para búsquedas rápidas
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_lote_id ON blockchain_index(lote_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_codigo_barras ON blockchain_index(codigo_barras)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_blockchain_tx ON blockchain_index(blockchain_tx)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ipfs_hash ON blockchain_index(ipfs_hash)')
        
        conn.commit()
        conn.close()
        print("✅ Base de datos inicializada")
    
    def save_blockchain_record(self, record: Dict[str, Any]) -> bool:
        """Guardar registro en base de datos para búsquedas rápidas"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO blockchain_index 
                (trace_id, lote_id, producto_id, codigo_barras, blockchain_tx, 
                 ipfs_hash, event_type, timestamp, block_number, status, data_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record['trace_id'],
                record['lote_id'],
                record['data'].get('producto_id'),
                record['data'].get('codigo_barras'),
                record['blockchain_tx'],
                record['ipfs_hash'],
                record['event_type'],
                record['timestamp'].isoformat() if hasattr(record['timestamp'], 'isoformat') else str(record['timestamp']),
                record.get('block_number', 0),
                record['status'],
                json.dumps(record['data'])
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error guardando en BD: {e}")
            return False
    
    def search_by_lote(self, lote_id: str) -> List[Dict]:
        """Búsqueda rápida por lote ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM blockchain_index 
            WHERE lote_id = ? 
            ORDER BY timestamp
        ''', (lote_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in results]
    
    def search_by_barcode(self, codigo_barras: str) -> List[Dict]:
        """Búsqueda rápida por código de barras"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM blockchain_index 
            WHERE codigo_barras = ? 
            ORDER BY timestamp
        ''', (codigo_barras,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(row) for row in results]
    
    def search_by_tx(self, tx_hash: str) -> Dict:
        """Búsqueda por hash de transacción"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM blockchain_index 
            WHERE blockchain_tx = ?
        ''', (tx_hash,))
        
        result = cursor.fetchone()
        conn.close()
        
        return self._row_to_dict(result) if result else None
    
    def _row_to_dict(self, row) -> Dict:
        """Convertir fila de BD a diccionario"""
        if not row:
            return None
            
        return {
            'trace_id': row[0],
            'lote_id': row[1],
            'producto_id': row[2],
            'codigo_barras': row[3],
            'blockchain_tx': row[4],
            'ipfs_hash': row[5],
            'event_type': row[6],
            'timestamp': row[7],
            'block_number': row[8],
            'status': row[9],
            'data': json.loads(row[10]) if row[10] else {}
        }
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas de la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM blockchain_index')
        total_records = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT lote_id) FROM blockchain_index')
        unique_lotes = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT codigo_barras) FROM blockchain_index WHERE codigo_barras IS NOT NULL')
        unique_products = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_records': total_records,
            'unique_lotes': unique_lotes,
            'unique_products': unique_products
        }