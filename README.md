# Data Ingestion System

Sistema simplificado de ingesta manual de datos para análisis usando FastAPI, React y SQL Server.

## Características

- **Ingesta Manual**: Formulario web para entrada de datos
- **Backend API**: FastAPI con validación automática
- **Frontend**: React con interfaz intuitiva
- **Base de Datos**: SQL Server en Docker
- **Análisis**: Estadísticas y métricas básicas
- **Modo Offline**: Funciona sin BD para demostración

## Requisitos Previos

- **Docker Desktop** (solo para base de datos)
- **Python 3.8+** 
- **Node.js 16+**
- **SQL Server ODBC Driver 17** (para Windows, se instala automáticamente)

## Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd DataIngestion
```

### 2. Iniciar Base de Datos
```bash
# Windows
start.bat

# Manual
docker-compose up -d
```

### 3. Configurar Backend
```bash
# Windows
start-backend.bat

# Manual
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 4. Configurar Frontend
```bash
# Windows  
start-frontend.bat

# Manual
cd frontend
npm install
npm start
```

### 5. Acceder al Sistema
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Scripts Disponibles

- `start.bat` - Inicia solo la base de datos
- `start-backend.bat` - Inicia el servidor backend
- `start-frontend.bat` - Inicia el servidor frontend
- `stop.bat` - Detiene la base de datos

## Estructura Simplificada

```
DataIngestion/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Rutas API
│   │   ├── models/         # Modelos de datos
│   │   └── services/       # Servicios
│   └── requirements.txt    # Dependencias
├── frontend/               # App React
│   ├── src/
│   │   ├── pages/         # Páginas
│   │   └── services/      # API calls
│   └── package.json       # Dependencias
├── database/              # SQL Scripts
├── docker-compose.yml     # Solo BD
└── *.bat                 # Scripts Windows
```

## API Endpoints Principales

### Datos Manuales
- `POST /api/v1/data/manual-entry` - Agregar registro manual
- `GET /api/v1/data/schema` - Esquema de campos
- `GET /api/v1/data` - Obtener datos guardados
- `GET /api/v1/data/statistics` - Estadísticas

### Utilidades
- `GET /api/v1/health` - Estado del sistema

## Campos de Datos

El sistema maneja estos campos para cada registro:

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| nombre | string | ✅ | Nombre del tirador |
| edad | number | ❌ | Edad del tirador |
| genero | string | ❌ | Masculino/Femenino |
| experiencia_anos | number | ❌ | Años de experiencia |
| distancia_metros | number | ❌ | Distancia de tiro |
| ambiente | string | ❌ | Interior/Exterior |
| tiros_exitosos | number | ❌ | Tiros acertados |
| tiros_totales | number | ❌ | Total de tiros |
| tiempo_sesion_minutos | number | ❌ | Duración sesión |
| precision_porcentaje | number | ❌ | Calculado automáticamente |

## Configuración Base de Datos

**SQL Server** (solo con Docker):
- **Host**: localhost:1433
- **Usuario**: sa  
- **Password**: YourStrong@Passw0rd
- **BD**: DataIngestionDB

## Modo Offline

Si la base de datos no está disponible, el sistema funciona en **modo offline**:
- Acepta y procesa datos normalmente
- Muestra mensaje indicando el modo
- Permite demostrar funcionalidad sin BD

## Solución de Problemas

### Backend no inicia
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend no inicia  
```bash
cd frontend
npm install --force
npm start
```

### Error de Base de Datos
```bash
docker-compose down
docker-compose up -d
# Esperar 30 segundos
```

### Puerto ocupado
- Backend (8000): Cambiar en `uvicorn --port 8001`
- Frontend (3000): Se detecta automáticamente
- BD (1433): Cambiar en `docker-compose.yml`

## Desarrollo

### Solo Frontend (modo demo)
```bash
cd frontend && npm start
# Funciona en modo offline
```

### Solo Backend (API testing)
```bash
cd backend && python -m uvicorn app.main:app --reload
# Ir a http://localhost:8000/docs
```

## Comandos Útiles

```bash
# Ver logs de BD
docker logs data-ingestion-sqlserver

# Conectar a BD
docker exec -it data-ingestion-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P YourStrong@Passw0rd -C

# Limpiar todo
docker-compose down -v
```

Este sistema está optimizado para desarrollo local y demostraciones rápidas.