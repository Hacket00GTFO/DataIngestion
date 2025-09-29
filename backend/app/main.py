"""Main FastAPI application module."""
import os
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.api import (
    data_routes, 
    health_routes, 
    database_routes, 
    tiradores_routes
)
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
        # Probar conexión de forma no bloqueante
        logging.info("Aplicación iniciada - Inicializando base de datos en segundo plano")
        # Intentar inicializar pero no bloquear el startup
        import threading  # pylint: disable=import-outside-toplevel
        def init_db_background():
            try:
                if test_connection():
                    init_database()
                    logging.info("Base de datos inicializada correctamente")
                else:
                    logging.warning(
                        "No se pudo conectar a la base de datos - "
                        "La aplicación funcionará sin BD"
                    )
            except Exception as e:  # pylint: disable=broad-exception-caught
                logging.error("Error en inicialización de BD: %s", str(e))

        # Ejecutar inicialización en background
        thread = threading.Thread(target=init_db_background)
        thread.daemon = True
        thread.start()

    except Exception as e:  # pylint: disable=broad-exception-caught
        logging.error("Error en startup: %s", str(e))
# Registro de rutas
app.include_router(health_routes.router, prefix="/api/v1", tags=["health"])
app.include_router(data_routes.router, prefix="/api/v1", tags=["data"])
app.include_router(database_routes.router, prefix="/api/v1", tags=["database"])
# Excel routes eliminadas - solo ingesta manual disponible
app.include_router(tiradores_routes.router, prefix="/api/v1", tags=["tiradores"])

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {"message": "Data Ingestion API - Sistema de procesamiento de datos"}

@app.get("/api/v1/stats/sesiones")
async def get_sesiones_stats():
    """Obtener estadísticas de sesiones de tiro."""
    # pylint: disable=import-outside-toplevel
    from app.services.database_service import DatabaseService
    db_service = DatabaseService()
    return await db_service.get_sesion_statistics()

@app.get("/api/v1/stats/tiradores")
async def get_tiradores_stats():
    """Obtener estadísticas de tiradores."""
    # pylint: disable=import-outside-toplevel
    from app.services.database_service import DatabaseService
    db_service = DatabaseService()
    return await db_service.get_tirador_statistics()

@app.get("/favicon.ico", status_code=204)
async def favicon():
    """Handle favicon requests to prevent 500 errors."""
    # Return a 204 No Content response to indicate successful request with no content
    return
