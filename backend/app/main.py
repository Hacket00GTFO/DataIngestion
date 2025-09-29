"""Main FastAPI application module."""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.api import data_routes, health_routes

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

# Registro de rutas
app.include_router(health_routes.router, prefix="/api/v1", tags=["health"])
app.include_router(data_routes.router, prefix="/api/v1", tags=["data"])

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {"message": "Data Ingestion API - Sistema de procesamiento de datos"}

@app.get("/favicon.ico")
async def favicon():
    """Favicon endpoint to prevent 404 errors from frontend proxy."""
    return Response(status_code=204)
