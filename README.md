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

## Base de Datos (PostgreSQL en Azure)

1. Crea un **Azure Database for PostgreSQL - Flexible Server** desde el portal de Azure. Selecciona autenticación por contraseña y toma nota de `usuario`, `password`, región y nombre del servidor.
2. En la sección *Networking* habilita el acceso público e incluye tu dirección IP en la lista de firewall. Azure exige conexiones TLS, por lo que se debe usar `sslmode=require` en la cadena de conexión.
3. En el proyecto copia el archivo de ejemplo y actualiza las credenciales reales:
   ```bash
   cd backend
   cp .env.example .env
   # Edita .env y reemplaza usuario, password y host
   ```
4. Aplica la migración inicial para crear tipos ENUM, tablas e índices:
   ```bash
   make migrate
   ```

### Carga manual al staging desde psql

1. Conéctate a la base de datos usando `psql` (ajusta host, usuario y base de datos):
   ```bash
   psql "host=tu-servidor.postgres.database.azure.com port=5432 dbname=appdb user=usuario password=******** sslmode=require"
   ```
2. Importa un archivo CSV directamente a la tabla `public.tiros_staging`:
   ```sql
   \copy public.tiros_staging(nombre_tirador,edad,experiencia,distancia_de_tiro,angulo,altura_de_tirador,peso,ambiente,genero,peso_del_balon,tiempo_de_tiro,tiro_exitoso,diestro_zurdo,calibre_de_balon)
   FROM 'data/tiros.csv' WITH (FORMAT csv, HEADER true);
   ```
3. Ejecuta la transformación desde el script o el endpoint para poblar `public.tiros`:
   ```bash
   make transform
   # o invoca POST /api/v1/data/upload-excel desde el backend
   ```

## Ejecución Local (PostgreSQL + FastAPI)

### 1) Prerrequisitos
- Docker Desktop (para levantar PostgreSQL local).
- Python 3.10+ (recomendado).
- (Opcional) Cliente `psql` para revisar datos:
  ```bash
  # macOS (Homebrew)
  brew install libpq
  echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
  psql --version
  ```

### 2) Levantar PostgreSQL en Docker
Desde `backend/`:
```bash
docker run --name db-evidencia \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=appdb \
  -p 5432:5432 -d postgres:16
```

Verifica:
```bash
docker ps  # debe aparecer el contenedor postgres:16 escuchando en 5432
```

### 3) Configurar variables de entorno
Crear `.env` a partir del ejemplo:
```bash
cd backend
cp .env.example .env
```

Editar `backend/.env`:
```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/appdb
CORS_ORIGINS=*
```

### 4) Preparar entorno Python
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Opcional (pruebas de parsers):
```bash
python -m pytest tests/test_data_processor.py
```

### 5) Migraciones (crear tablas y enums)
Si Alembic no encuentra el paquete `app`, agrega `export PYTHONPATH=$(pwd)` antes del comando.
```bash
export PYTHONPATH=$(pwd)
alembic upgrade head
```
Salida esperada: `Running upgrade -> 202403120001, create tiros tables and enums.`

### 6) Ejecutar el backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
API Docs: `http://localhost:8000/docs`

### 7) Cargar datos (Excel o CSV)
**A) Subir desde Swagger UI**
- `POST /api/v1/data/upload-excel` → `Try it out` → seleccionar archivo → `Execute`.
- Acepta `.xlsx` o `.csv`. Si es Excel, el backend lo convierte a CSV automáticamente.

**B) Subir con curl (opcional)**
```bash
# Excel
curl -X POST "http://localhost:8000/api/v1/data/upload-excel" \
  -H "accept: application/json" -H "Content-Type: multipart/form-data" \
  -F "file=@data/tu_archivo.xlsx"

# CSV
curl -X POST "http://localhost:8000/api/v1/data/upload-excel" \
  -H "accept: application/json" -H "Content-Type: multipart/form-data" \
  -F "file=@data/tiros.csv"
```

**Formato de columnas (CSV con encabezados exactos)**
- Encabezados en `snake_case`, sin tildes ni signos, y en UTF-8:
  ```text
  nombre_tirador,edad,experiencia,distancia_de_tiro,angulo,altura_de_tirador,peso,ambiente,genero,peso_del_balon,tiempo_de_tiro,tiro_exitoso,diestro_zurdo,calibre_de_balon
  ```
- Ejemplo de fila:
  ```text
  Norberto,24,"4 años","5 metros","90 grados",1.7,"95 kg",Ventoso,Masculino,"500 g","1 segundo","2 de 6",Diestro,6
  ```

### 8) Verificar resultados
```bash
# Estadísticas
curl "http://localhost:8000/api/v1/data/statistics"

# Esquema
curl "http://localhost:8000/api/v1/data/schema"

# Con SQL (opcional)
psql "postgresql://postgres:postgres@localhost:5432/appdb" -c "SELECT COUNT(*) FROM public.tiros;"
```

### 9) Limpiar datos (reiniciar tablas)
Si hiciste varias cargas y quieres empezar en limpio:
```bash
psql "postgresql://postgres:postgres@localhost:5432/appdb" -c "TRUNCATE TABLE public.tiros RESTART IDENTITY CASCADE;"
psql "postgresql://postgres:postgres@localhost:5432/appdb" -c "TRUNCATE TABLE public.tiros_staging RESTART IDENTITY CASCADE;"
```

### 10) Notas y solución de problemas
- **Encabezados inválidos** → el log dirá: `CSV missing expected columns ...`. Revisa nombres exactos.
- **Codificación** → exporta CSV como `CSV UTF-8 (delimitado por comas)`.
- **Alembic no ve app** → `export PYTHONPATH=$(pwd)` o agrega en `alembic/env.py`:
  ```python
  import os, sys
  sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
  from dotenv import load_dotenv
  load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
  ```
- **Enums existentes** (al reintentar migraciones) → limpia la BD (ver sección 9) o borra tipos `genero_enum`, `mano_habil_enum` desde `psql` y vuelve a migrar.
- **PostgreSQL no arranca** → asegúrate de que el puerto 5432 esté libre o cambia el mapeo `-p 5432:5432`.


## Uso del Sistema

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
- `POST /api/v1/data/upload-excel` - Carga un archivo Excel/CSV, ingesta al staging y transforma hacia la tabla final en PostgreSQL
- `GET /api/v1/data` - Obtener todos los datos
- `GET /api/v1/data/schema` - Expone las columnas y tipos de la tabla `tiros`
- `GET /api/v1/data/statistics` - Devuelve totales, promedios y distribuciones agregadas desde la tabla `tiros`

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
