# Service Mesh - Sistema de Gestión de Inventario

Este proyecto contiene un sistema de microservicios desarrollado con FastAPI para la gestión integral de inventario, incluyendo bodegas, lotes, productos, proyección de demanda, órdenes de compra y proveedores.

## Arquitectura del Sistema

El sistema está compuesto por 6 microservicios principales:

### 1. MS-Bodega (Puerto 8001)

- **Función**: Gestión de bodegas y ubicaciones geográficas
- **Características principales**:
  - CRUD de bodegas con ubicación geográfica
  - Control de disponibilidad y reservas
  - Operaciones de inventario (reservar, vender)
  - Consultas de disponibilidad

### 2. MS-Lote (Puerto 8002)

- **Función**: Gestión de lotes y control de almacenamiento
- **Características principales**:
  - CRUD de lotes con fechas de vencimiento
  - Tipos de almacenamiento (refrigerado, congelado, ambiente, seco)
  - Alertas de vencimiento
  - Control de temperatura y humedad

### 3. MS-Producto (Puerto 8003)

- **Función**: Catálogo de productos
- **Características principales**:
  - CRUD de productos con categorías
  - Información nutricional y características
  - Búsqueda por código de barras
  - Estadísticas de productos

### 4. MS-ProyeccionDemanda (Puerto 8004)

- **Función**: Proyección y análisis de demanda
- **Características principales**:
  - Proyecciones por diferentes periodos (semanal, mensual, etc.)
  - Alertas de demanda
  - Métricas calculadas automáticamente
  - Estados de proyección (borrador, activa, archivada)

### 5. MS-OrdenCompra (Puerto 8005)

- **Función**: Gestión de órdenes de compra
- **Características principales**:
  - Workflow completo de órdenes (draft → aprobada → enviada → recibida)
  - Gestión de items por orden
  - Cálculo automático de totales
  - Alertas de retrasos y aprobaciones pendientes

### 6. MS-Proveedor (Puerto 8006)

- **Función**: Gestión de proveedores
- **Características principales**:
  - CRUD de proveedores con información completa
  - Sistema de certificaciones sanitarias
  - Evaluaciones y calificaciones
  - Condiciones de entrega personalizadas

## Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- pip

### Instalación

1. Clona el repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Ejecutar un Microservicio

Cada microservicio se puede ejecutar independientemente:

```bash
# MS-Bodega
cd ms-bodega
python main.py

# MS-Lote
cd ms-lote
python main.py

# MS-Producto
cd ms-producto
python main.py

# MS-ProyeccionDemanda
cd ms-proyeccion-demanda
python main.py

# MS-OrdenCompra
cd ms-orden-compra
python main.py

# MS-Proveedor
cd ms-proveedor
python main.py
```

## Endpoints Principales

### MS-Bodega (http://localhost:8001)

- `GET /bodegas` - Listar bodegas con filtros
- `POST /bodegas` - Crear bodega
- `GET /bodegas/{id}/disponibilidad` - Consultar disponibilidad
- `PATCH /bodegas/{id}/reservar/{cantidad}` - Reservar cantidad

### MS-Lote (http://localhost:8002)

- `GET /lotes` - Listar lotes con filtros
- `POST /lotes` - Crear lote
- `GET /alertas/vencimiento` - Alertas de vencimiento
- `GET /lotes/vencidos` - Lotes vencidos

### MS-Producto (http://localhost:8003)

- `GET /productos` - Listar productos con filtros
- `POST /productos` - Crear producto
- `GET /productos/buscar/codigo-barras/{codigo}` - Buscar por código
- `GET /estadisticas/productos` - Estadísticas generales

### MS-ProyeccionDemanda (http://localhost:8004)

- `GET /proyecciones` - Listar proyecciones
- `POST /proyecciones` - Crear proyección
- `GET /proyecciones/vigentes` - Proyecciones activas
- `GET /alertas/demanda` - Alertas de demanda

### MS-OrdenCompra (http://localhost:8005)

- `GET /ordenes` - Listar órdenes con filtros
- `POST /ordenes` - Crear orden
- `PATCH /ordenes/{id}/aprobar` - Aprobar orden
- `GET /alertas/ordenes` - Alertas de órdenes

### MS-Proveedor (http://localhost:8006)

- `GET /proveedores` - Listar proveedores
- `POST /proveedores` - Crear proveedor
- `POST /proveedores/{id}/certificaciones` - Agregar certificación
- `GET /alertas/certificaciones` - Alertas de vencimiento

## Documentación de API

Cada microservicio tiene su documentación interactiva disponible en:

- MS-Bodega: http://localhost:8001/docs
- MS-Lote: http://localhost:8002/docs
- MS-Producto: http://localhost:8003/docs
- MS-ProyeccionDemanda: http://localhost:8004/docs
- MS-OrdenCompra: http://localhost:8005/docs
- MS-Proveedor: http://localhost:8006/docs

## Características Técnicas

### Modelos de Datos

- Uso extensivo de Pydantic para validación de datos
- Enums para valores controlados
- Modelos separados para Create, Update y Response
- Validaciones de negocio incorporadas

### Funcionalidades Avanzadas

- Sistema de filtros avanzados en todas las consultas
- Cálculo automático de métricas derivadas
- Sistema de alertas contextual
- Gestión de estados con workflows definidos
- Simulación de persistencia en memoria

### Integración

- Diseño preparado para integración entre microservicios
- Estructura de respuesta consistente
- Manejo de errores estandarizado
- Logging y monitoreo preparado

## Próximos Pasos

Para un entorno de producción, considerar:

1. Implementar base de datos real (PostgreSQL/MongoDB)
2. Añadir autenticación y autorización
3. Implementar API Gateway
4. Añadir observabilidad (Prometheus, Grafana)
5. Implementar Circuit Breaker y retries
6. Dockerizar los servicios
7. Implementar tests automatizados
