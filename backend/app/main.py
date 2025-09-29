"""Main FastAPI application module."""
import os
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.api import data_routes, health_routes, database_routes, excel_routes
from app.database import init_database, test_connection
from app.services.data_service import DataService

app = FastAPI(
    title="Data Ingestion API",
    description="API para procesamiento y gestión de datos de evidencia big data",
    version="1.0.0"
)

# Configuración CORS
allowed_origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización de servicios
data_service = DataService()

# Evento de inicio para inicializar la base de datos
@app.on_event("startup")
async def startup_event():
    """Inicializar la base de datos al arrancar la aplicación."""
    try:
        # Probar conexión
        if test_connection():
            # Inicializar tablas
            init_database()
            logging.info("Aplicación iniciada correctamente con base de datos")
        else:
            logging.warning("No se pudo conectar a la base de datos")
    except Exception as e:
        logging.error("Error en inicialización: %s", str(e))
# Registro de rutas
app.include_router(health_routes.router, prefix="/api/v1", tags=["health"])
app.include_router(data_routes.router, prefix="/api/v1", tags=["data"])
app.include_router(database_routes.router, prefix="/api/v1", tags=["database"])
app.include_router(excel_routes.router, prefix="/api/v1", tags=["excel"])

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {"message": "Data Ingestion API - Sistema de procesamiento de datos"}

@app.get("/favicon.ico")
async def favicon():
    """Favicon endpoint to prevent 404 errors from frontend proxy."""
    return Response(status_code=204)
