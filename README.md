# Data Ingestion

Sistema completo de ingesta y procesamiento de datos para evidencia big data, compuesto por un backend en Python con FastAPI y un frontend en React.

## Descripción del Proyecto

Este proyecto implementa un sistema de data wrangling capaz de procesar registros basados en las columnas del archivo `evidencia big data.xlsx`. El sistema permite la ingesta de nuevos datos a través de una interfaz web moderna y el procesamiento automático de archivos Excel.

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

## Uso del Sistema

### 1. Dashboard
- Visualización de estadísticas generales
- Estado del sistema en tiempo real
- Acceso rápido a funcionalidades principales

### 2. Ingesta de Datos
- **Subida de archivos Excel**: Procesamiento automático de archivos
- **Ingreso manual**: Formulario dinámico basado en esquema
- **Validación**: Verificación automática de datos
- **Procesamiento**: Limpieza y normalización de datos

### 3. Visualización de Datos
- Tabla interactiva con todos los registros
- Búsqueda y filtrado en tiempo real
- Ordenamiento por columnas
- Paginación para grandes volúmenes de datos

## API Endpoints

### Datos
- `POST /api/v1/data/ingest` - Ingesta de nuevos datos
- `POST /api/v1/data/upload-excel` - Subida de archivo Excel
- `GET /api/v1/data/statistics` - Estadísticas de datos
- `GET /api/v1/data/schema` - Esquema de datos

### Salud del Sistema
- `GET /api/v1/health` - Verificación básica de salud
- `GET /api/v1/health/detailed` - Verificación detallada

## Procesamiento de Datos

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

## Contribución

1. Fork del repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.