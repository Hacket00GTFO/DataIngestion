# Data Ingestion

Sistema completo de ingesta y procesamiento de datos para evidencia big data, compuesto por un backend en Python con FastAPI y un frontend en React.

## Descripción del Proyecto

Este proyecto implementa un sistema de data wrangling capaz de procesar registros basados en las columnas del archivo `evidencia big data.xlsx`. El sistema permite la ingesta de nuevos datos a través de una interfaz web moderna y el procesamiento automático de archivos Excel.

**Objetivo Principal:**
- Realizar procesos de data wrangling con los registros de las columnas del archivo `evidencia big data.xlsx`
- Generar reportes del procesamiento de datos desde el frontend
- Proporcionar una interfaz intuitiva para el análisis y visualización de datos procesados

## Arquitectura del Sistema

### Backend (Python + FastAPI)

**Tecnologías principales:**
- FastAPI 0.104.1 - Framework web moderno y rápido
- Pandas 2.1.3 - Manipulación y análisis de datos
- NumPy 1.25.2 - Computación numérica
- SQLAlchemy 2.0.23 - ORM para base de datos
- Pydantic 2.5.0 - Validación de datos
- OpenPyXL 3.1.2 - Procesamiento de archivos Excel

**Estructura del Backend:**
```
backend/
├── app/
│   ├── api/
│   │   ├── data_routes.py      # Endpoints para gestión de datos
│   │   └── health_routes.py    # Endpoints de salud del sistema
│   ├── models/
│   │   └── data_models.py      # Modelos Pydantic para validación
│   ├── services/
│   │   └── data_service.py     # Lógica de negocio principal
│   ├── utils/
│   │   ├── data_validator.py   # Validación de datos
│   │   └── data_processor.py   # Procesamiento y limpieza
│   └── main.py                 # Punto de entrada de la aplicación
├── tests/                      # Pruebas unitarias
└── requirements.txt            # Dependencias de Python
```

**Características del Backend:**
- API RESTful con documentación automática (Swagger/OpenAPI)
- Validación robusta de datos con Pydantic
- Procesamiento de archivos Excel con pandas
- **Capacidad de digerir datos extraños/externos de múltiples fuentes**
- **Procesamiento de formatos de datos no estándar**
- **Adaptación automática a esquemas de datos variables**
- Limpieza automática de datos (duplicados, nulos, normalización)
- Manejo de errores y logging
- CORS configurado para integración con frontend
- Endpoints de salud para monitoreo

### Frontend (React)

**Tecnologías principales:**
- React 18.2.0 - Biblioteca de interfaz de usuario
- React Router DOM 6.8.1 - Enrutamiento
- Axios 1.6.2 - Cliente HTTP
- React Hook Form 7.48.2 - Manejo de formularios
- Styled Components 6.1.1 - Estilos CSS-in-JS

**Estructura del Frontend:**
```
frontend/
├── public/
│   └── index.html              # Plantilla HTML base
├── src/
│   ├── components/
│   │   ├── Header.js           # Componente de navegación
│   │   └── Header.css          # Estilos del header
│   ├── pages/
│   │   ├── Dashboard.js        # Página principal
│   │   ├── Dashboard.css       # Estilos del dashboard
│   │   ├── DataForm.js         # Formulario de ingesta
│   │   ├── DataForm.css        # Estilos del formulario
│   │   ├── DataViewer.js       # Visualizador de datos
│   │   └── DataViewer.css      # Estilos del visualizador
│   ├── services/
│   │   ├── api.js              # Cliente API
│   │   └── DataIngestionContext.js # Context API para estado global
│   ├── App.js                  # Componente principal
│   ├── App.css                 # Estilos globales
│   ├── index.js                # Punto de entrada
│   └── index.css               # Estilos base
└── package.json                # Dependencias y scripts
```

**Características del Frontend:**
- Interfaz responsive y moderna
- Dashboard con estadísticas del sistema
- Formulario dinámico basado en esquema de datos
- Visualizador de datos con paginación y búsqueda
- Subida de archivos Excel
- **Capacidad de procesar y visualizar datos extraños/externos**
- **Interfaz adaptativa para diferentes formatos de datos**
- **Visualización de datos no estructurados**
- **Generación de reportes del procesamiento de datos**
- **Visualización de resultados de data wrangling**
- Manejo de estado con Context API
- Validación de formularios en tiempo real
- Diseño mobile-first

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Node.js 16+
- npm o yarn

### Backend

1. Navegar al directorio backend:
```bash
cd backend
```

2. Crear entorno virtual:
```bash
python -m venv venv
```

3. Activar entorno virtual:
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Ejecutar servidor:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. Navegar al directorio frontend:
```bash
cd frontend
```

2. Instalar dependencias:
```bash
npm install
```

3. Ejecutar aplicación:
```bash
npm start
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

### 1. Dashboard
- Visualización de estadísticas generales
- Estado del sistema en tiempo real
- Acceso rápido a funcionalidades principales

### 2. Ingesta de Datos
- **Subida de archivos Excel**: Procesamiento automático de archivos
- **Ingreso manual**: Formulario dinámico basado en esquema
- **Ingesta de datos extraños/externos**: Procesamiento de fuentes de datos no estándar
- **Adaptación automática**: Detección y mapeo de esquemas de datos variables
- **Validación**: Verificación automática de datos
- **Procesamiento**: Limpieza y normalización de datos

### 3. Visualización de Datos
- Tabla interactiva con todos los registros
- Búsqueda y filtrado en tiempo real
- Ordenamiento por columnas
- Paginación para grandes volúmenes de datos

### 4. Data Wrangling y Reportes
- **Procesamiento de columnas del archivo `evidencia big data.xlsx`**
- **Generación automática de reportes de procesamiento**
- **Visualización de estadísticas de limpieza de datos**
- **Exportación de reportes en diferentes formatos**
- **Seguimiento del estado de procesamiento en tiempo real**

## API Endpoints

### Datos
- `POST /api/v1/data/upload-excel` - Carga un archivo Excel/CSV, ingesta al staging y transforma hacia la tabla final en PostgreSQL
- `GET /api/v1/data/statistics` - Devuelve totales, promedios y distribuciones agregadas desde la tabla `tiros`
- `GET /api/v1/data/schema` - Expone las columnas y tipos de la tabla `tiros`

### Salud del Sistema
- `GET /api/v1/health` - Verificación básica de salud
- `GET /api/v1/health/detailed` - Verificación detallada

## Procesamiento de Datos

### Data Wrangling con `evidencia big data.xlsx`
- **Procesamiento específico de columnas del archivo Excel**
- **Mapeo automático de campos según el esquema definido**
- **Validación de estructura de datos contra el archivo de referencia**
- **Procesamiento batch de registros masivos**

### Procesamiento de Datos Extraños/Externos
- **Detección automática de formatos de datos no estándar**
- **Adaptación dinámica a esquemas de datos variables**
- **Procesamiento de fuentes de datos heterogéneas**
- **Normalización de datos de diferentes orígenes**
- **Manejo de datos malformados o incompletos**

### Validación
- Verificación de columnas requeridas
- Validación de tipos de datos
- Detección de valores nulos
- Identificación de duplicados

### Limpieza
- Eliminación de registros duplicados
- Manejo de valores nulos
- Normalización de texto
- Validación de rangos numéricos

### Transformación
- Agrupación de datos
- Agregaciones estadísticas
- Filtrado por criterios específicos
- Exportación a diferentes formatos

### Generación de Reportes
- **Reportes automáticos del procesamiento de datos**
- **Métricas de calidad de datos procesados**
- **Estadísticas de limpieza y transformación**
- **Visualización de resultados en el frontend**
- **Exportación de reportes en PDF, Excel y CSV**

## Configuración de Desarrollo

### Variables de Entorno

**Backend (.env):**
```
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
DEBUG=True
```

**Frontend (.env):**
```
REACT_APP_API_URL=http://localhost:8000/api/v1
```

### Base de Datos
El sistema está preparado para integrarse con PostgreSQL, pero puede adaptarse a otros motores de base de datos modificando la configuración en `requirements.txt` y los modelos de SQLAlchemy.

## Testing

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm test
```

## Despliegue

### Backend
- Configurar variables de entorno de producción
- Usar Gunicorn o similar para producción
- Configurar proxy reverso (Nginx)
- Implementar SSL/TLS

### Frontend
```bash
cd frontend
npm run build
```
Los archivos generados en `build/` pueden servirse con cualquier servidor web estático.
