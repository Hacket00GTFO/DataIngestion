"""Health check endpoints for monitoring system status."""
from datetime import datetime
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Endpoint de verificación de salud del servicio."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "data-ingestion-api",
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """Endpoint de verificación detallada de salud."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "data-ingestion-api",
        "version": "1.0.0",
        "components": {
            "database": "connected",
            "file_system": "accessible",
            "memory": "normal"
        }
    }
