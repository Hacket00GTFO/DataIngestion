"""Main FastAPI application module."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import data_routes, health_routes
from app.services.data_service import DataService

app = FastAPI(
    title="Data Ingestion API",
    description="API para procesamiento y gestión de datos de evidencia big data",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización de servicios
data_service = DataService()

# Registro de rutas
app.include_router(health_routes.router, prefix="/api/v1", tags=["health"])
app.include_router(data_routes.router, prefix="/api/v1", tags=["data"])

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {"message": "Data Ingestion API - Sistema de procesamiento de datos"}
