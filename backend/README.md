# Data Ingestion Backend

Backend API para el sistema de procesamiento y gestión de datos de evidencia big data.

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación principal FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   ├── data_routes.py      # Rutas para gestión de datos
│   │   └── health_routes.py    # Rutas de health check
│   ├── models/
│   │   ├── __init__.py
│   │   └── data_models.py      # Modelos de datos Pydantic
│   ├── services/
│   │   ├── __init__.py
│   │   └── data_service.py     # Servicio principal de datos
│   └── utils/
│       ├── __init__.py
│       ├── data_processor.py   # Utilidades de procesamiento
│       └── data_validator.py   # Utilidades de validación
├── requirements.txt
├── run.py                      # Script para ejecutar la aplicación
├── .pylintrc                   # Configuración de Pylint
└── pyproject.toml              # Configuración del proyecto
```

## Instalación

1. Asegúrate de tener Python 3.12+ instalado
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

### Opción 1: Usando el script run.py
```bash
python run.py
```

### Opción 2: Usando uvicorn directamente
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Opción 3: Usando el módulo Python
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints Disponibles

- `GET /` - Información general de la API
- `GET /api/v1/health` - Health check básico
- `GET /api/v1/health/detailed` - Health check detallado
- `POST /api/v1/data/ingest` - Ingesta de nuevos datos
- `POST /api/v1/data/upload-excel` - Subida y procesamiento de archivos Excel
- `GET /api/v1/data/statistics` - Estadísticas de los datos
- `GET /api/v1/data/schema` - Esquema de datos

## Documentación de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a:
- Documentación interactiva: http://localhost:8000/docs
- Documentación alternativa: http://localhost:8000/redoc

## Desarrollo

### Configuración del IDE

El proyecto incluye configuración para varios linters y IDEs:

- `.pylintrc` - Configuración de Pylint
- `pyproject.toml` - Configuración moderna del proyecto
- `pyrightconfig.json` - Configuración para Pyright (VS Code)
- `.vscode/settings.json` - Configuración específica de VS Code

### Configuración del Linter

Si estás viendo errores de importación en tu IDE, asegúrate de:

1. **Abrir el proyecto desde la carpeta `backend`** (no desde la raíz del repositorio)
2. **Configurar el intérprete de Python** para usar el entorno virtual en `./venv/Scripts/python.exe`
3. **Reiniciar el servidor de lenguaje** de Python en tu IDE

### Estructura de Imports

Todos los imports usan rutas absolutas desde el paquete `app`. Por ejemplo:
```python
from app.models.data_models import DataStatistics
from app.services.data_service import DataService
```

Esto asegura que los imports funcionen correctamente independientemente del directorio desde donde se ejecute el código.
