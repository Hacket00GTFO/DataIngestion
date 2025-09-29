# Sistema de Data Ingestion

Sistema completo para procesar y gestionar datos del archivo `evidencia big data.xlsx` con interfaz web moderna y base de datos SQL Server.

## Descripción

Sistema de data wrangling que procesa registros de tiradores basados en el archivo Excel de evidencia. Permite ingesta manual y automática de datos, procesamiento de archivos Excel, y visualización de resultados.

**Características principales:**
- Procesamiento de archivos Excel (.xlsx)
- Ingesta manual de datos con formulario dinámico
- Almacenamiento en base de datos SQL Server
- Interfaz web moderna con React
- API REST con FastAPI

## Arquitectura

### Backend (FastAPI + Python)
- **FastAPI**: API REST moderna y rápida
- **Pandas**: Procesamiento de archivos Excel
- **SQLAlchemy**: ORM para base de datos
- **SQL Server**: Base de datos principal

### Frontend (React)
- **React**: Interfaz de usuario moderna
- **Formularios dinámicos**: Basados en esquema de datos
- **Carga de archivos**: Procesamiento de Excel
- **Visualización**: Tablas interactivas de datos

### Base de Datos (SQL Server)
- **Tabla principal**: `data_records` (almacena datos JSON)
- **Vista de estadísticas**: `vw_data_statistics`
- **Índices optimizados**: Para consultas rápidas

## Instalación y Uso

### Prerrequisitos
- Python 3.8+
- Node.js 16+
- SQL Server (Docker recomendado)

### Instalación Rápida

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd DataIngestion
```

2. **Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

3. **Frontend:**
```bash
cd frontend
npm install
npm start
```

4. **Base de datos (Docker):**
```bash
docker-compose up sqlserver -d
```

## Funcionalidades

### 1. Procesamiento de Excel
- Carga de archivo `evidencia big data.xlsx`
- Extracción automática de 8 registros con 14 columnas
- Validación y limpieza de datos

### 2. Ingesta Manual
- Formulario dinámico basado en esquema de datos
- Validación en tiempo real
- Múltiples registros simultáneos

### 3. Visualización
- Tabla interactiva con todos los datos
- Búsqueda y filtrado
- Estadísticas en tiempo real

### 4. Base de Datos
- Almacenamiento en SQL Server
- Consultas optimizadas
- Backup automático

## API Endpoints

### Principales
- `POST /api/v1/data/ingest` - Ingesta manual de datos
- `POST /api/v1/data/upload-excel` - Carga de archivo Excel
- `GET /api/v1/data` - Obtener todos los datos
- `GET /api/v1/data/schema` - Esquema de columnas
- `GET /api/v1/data/statistics` - Estadísticas

### Documentación
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Estructura de Datos

### Archivo Excel (`evidencia big data.xlsx`)
- **8 registros** de tiradores
- **14 columnas**: Nombre, Edad, Experiencia, Distancia, Ángulo, etc.
- **Formato**: Primera fila = encabezados, datos desde fila 2

### Base de Datos
- **Tabla**: `data_records`
- **Campos**: `id`, `created_at`, `data` (JSON), `source`, `is_processed`
- **Vista**: `vw_data_statistics` para consultas rápidas

## Configuración

### Variables de Entorno
```bash
# Backend
DATABASE_URL=mssql+pyodbc://sa:YourStrong@Passw0rd@localhost:1433/DataIngestionDB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes

# Frontend
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### Conexión a Base de Datos
- **Server**: localhost,1433
- **Database**: DataIngestionDB
- **Username**: sa
- **Password**: YourStrong@Passw0rd
