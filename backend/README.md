# Backend API - Data Ingestion

API REST para procesamiento de datos del archivo `evidencia big data.xlsx` con FastAPI y SQL Server.

## Estructura

```
backend/
├── app/
│   ├── main.py                 # Aplicación principal FastAPI
│   ├── database.py             # Configuración de SQL Server
│   ├── api/
│   │   ├── data_routes.py      # Rutas de datos
│   │   ├── excel_routes.py     # Rutas de Excel
│   │   ├── health_routes.py    # Health check
│   │   └── database_routes.py  # Rutas de BD
│   ├── models/
│   │   └── data_models.py      # Modelos SQLAlchemy + Pydantic
│   ├── services/
│   │   ├── data_service.py     # Servicio principal
│   │   └── database_service.py # Servicio de BD
│   └── utils/
│       ├── data_processor.py   # Procesamiento de datos
│       └── data_validator.py   # Validación
├── requirements.txt            # Dependencias
├── Dockerfile                  # Imagen Docker
└── run.py                      # Script de ejecución
```

## Instalación

### Prerrequisitos
- Python 3.8+
- SQL Server (Docker recomendado)

### Instalación Local
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Con Docker
```bash
# Desde la raíz del proyecto
start.bat

# O solo el backend
docker-compose up backend -d
```

## Dependencias Principales
- **FastAPI** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **pyodbc** - Conector para SQL Server
- **Pandas** - Procesamiento de Excel
- **Pydantic** - Validación de datos

## Endpoints Principales

### Datos
- `POST /api/v1/data/ingest` - Ingesta manual de datos
- `POST /api/v1/data/upload-excel` - Carga de archivo Excel
- `GET /api/v1/data` - Obtener todos los datos
- `GET /api/v1/data/schema` - Esquema de columnas
- `GET /api/v1/data/statistics` - Estadísticas

### Base de Datos
- `GET /api/v1/database/records` - Registros de BD
- `GET /api/v1/database/statistics` - Estadísticas de BD
- `POST /api/v1/database/query` - Consultas personalizadas

### Salud
- `GET /api/v1/health` - Health check

## Documentación API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuración

### Variables de Entorno
```bash
DATABASE_URL=mssql+pyodbc://sa:YourStrong@Passw0rd@localhost:1433/DataIngestionDB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
```

### Conexión a Base de Datos
- **Server**: localhost,1433
- **Username**: sa
- **Password**: YourStrong@Passw0rd
- **Database**: DataIngestionDB

## Desarrollo

### Configuración IDE
- Abrir proyecto desde carpeta `backend`
- Configurar intérprete Python en `./venv/Scripts/python.exe`
- Reiniciar servidor de lenguaje Python

### Estructura de Imports
```python
from app.models.data_models import DataStatistics
from app.services.data_service import DataService
```
