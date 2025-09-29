# Backend - Data Ingestion API

API simplificada con FastAPI para ingesta manual de datos de tiro deportivo.

## Características

- **FastAPI**: API moderna con documentación automática
- **Ingesta Manual**: Endpoints para entrada manual de datos
- **Validación**: Modelos Pydantic robustos
- **SQL Server**: Conexión opcional (modo offline disponible)
- **Modo Desarrollo**: Funciona sin BD para pruebas

## Instalación Rápida

### Método 1: Script Automático (Windows)
```bash
# Desde la raíz del proyecto
start-backend.bat
```

### Método 2: Manual
```bash
cd backend

# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python -m uvicorn app.main:app --reload
```

## Acceso

- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## Estructura Simplificada

```
backend/
├── app/
│   ├── main.py                 # App FastAPI principal
│   ├── database.py             # Configuración BD (opcional)
│   ├── api/
│   │   ├── data_routes.py      # Rutas principales
│   │   ├── health_routes.py    # Health checks
│   │   └── tiradores_routes.py # Rutas tiradores
│   ├── models/
│   │   └── data_models.py      # Modelos de datos
│   └── services/
│       └── database_service.py # Servicios BD
└── requirements.txt            # Dependencias
```

## API Endpoints

### Datos Manuales
- `POST /api/v1/data/manual-entry` - Agregar registro manual
- `GET /api/v1/data/schema` - Esquema de campos disponibles
- `GET /api/v1/data` - Obtener datos guardados
- `GET /api/v1/data/statistics` - Estadísticas básicas

### Sistema
- `GET /api/v1/health` - Estado del sistema

### Documentación
- `GET /docs` - Swagger UI interactivo
- `GET /redoc` - Documentación ReDoc

## Modelo de Datos

### Entrada Manual
```python
{
    "nombre": "Juan Perez",           # Requerido
    "edad": 25,                      # Opcional
    "genero": "Masculino",           # Opcional (Masculino/Femenino)
    "experiencia_anos": 3,           # Opcional
    "distancia_metros": 50.0,        # Opcional
    "ambiente": "Exterior",          # Opcional (Interior/Exterior)
    "tiros_exitosos": 8,             # Opcional
    "tiros_totales": 10,             # Opcional  
    "tiempo_sesion_minutos": 30.0    # Opcional
}
```

### Respuesta
```python
{
    "success": true,
    "message": "Registro manual agregado exitosamente (modo offline)",
    "processed_records": 1,
    "data": [{
        "nombre": "Juan Perez",
        "precision_porcentaje": 80.0,  # Calculado automáticamente
        "created_at": "2025-09-29T12:00:00",
        ...
    }]
}
```

## Configuración

### Variables de Entorno (Opcionales)
```env
# Solo si quieres usar BD
DATABASE_URL=mssql+pyodbc://sa:YourStrong@Passw0rd@localhost:1433/DataIngestionDB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
```

### Modo Offline por Defecto
El sistema funciona **sin base de datos** por defecto:
- Acepta y valida datos
- Calcula métricas automáticamente  
- Responde con confirmación
- Perfecto para desarrollo y demos

## Desarrollo

### Comandos Útiles
```bash
# Desarrollo con recarga automática
uvicorn app.main:app --reload --port 8000

# Ver documentación interactiva
# http://localhost:8000/docs

# Probar endpoint manualmente
curl -X POST "http://localhost:8000/api/v1/data/manual-entry" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Test User", "edad": 30}'
```

### Agregar Nuevos Campos
1. Editar `app/models/data_models.py` → `ManualDataEntry`
2. Actualizar `app/api/data_routes.py` → `get_data_schema()`
3. El frontend se actualiza automáticamente

### Habilitar Base de Datos
1. Iniciar SQL Server: `docker-compose up -d`
2. El sistema detecta automáticamente la conexión
3. Los datos se guardan persistentemente

## Dependencias Principales

```txt
fastapi==0.104.1        # Framework web
uvicorn==0.24.0         # Servidor ASGI
pydantic==2.5.0         # Validación de datos
sqlalchemy==2.0.23      # ORM (opcional)
pyodbc==5.0.1          # Driver SQL Server (opcional)
```

## Solución de Problemas

### Error al instalar pyodbc
```bash
# Windows: Instalar Visual C++ Build Tools
# O usar conda:
conda install pyodbc
```

### Puerto ocupado
```bash
# Cambiar puerto
uvicorn app.main:app --reload --port 8001
```

### Error de importación
```bash
# Verificar instalación
pip list
pip install -r requirements.txt --force-reinstall
```

### Modo Debug
```python
# En app/main.py, cambiar:
app = FastAPI(debug=True)
```

## Testing

### Probar Endpoints
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Obtener esquema
curl http://localhost:8000/api/v1/data/schema

# Agregar datos
curl -X POST http://localhost:8000/api/v1/data/manual-entry \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Test", "edad": 25, "tiros_exitosos": 8, "tiros_totales": 10}'
```

Este backend está optimizado para simplicidad y facilidad de uso local.