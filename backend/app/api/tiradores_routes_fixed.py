"""Rutas de API para gestión de tiradores y sesiones de tiro."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.data_models import (
    TiradorPydantic, 
    TiradorConSesiones, 
    SesionTiroPydantic, 
    TiradorStatistics,
    SesionStatistics,
    AnalisisCompleto
)
from app.services.database_service import DatabaseService

router = APIRouter(prefix="/tiradores", tags=["tiradores"])

# RUTAS ESPECÍFICAS PRIMERO (más específicas)
@router.get("/estadisticas/tiradores", response_model=TiradorStatistics)
async def get_estadisticas_tiradores(db: Session = Depends(get_db)):
    """Obtener estadísticas de tiradores."""
    db_service = DatabaseService(db)
    return await db_service.get_tirador_statistics()

@router.get("/estadisticas/sesiones", response_model=SesionStatistics)
async def get_estadisticas_sesiones(db: Session = Depends(get_db)):
    """Obtener estadísticas de sesiones de tiro."""
    db_service = DatabaseService(db)
    return await db_service.get_sesion_statistics()

@router.get("/analisis/completo", response_model=List[AnalisisCompleto])
async def get_analisis_completo(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    genero: Optional[str] = None,
    ambiente: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener análisis completo de tiradores y sesiones con filtros."""
    db_service = DatabaseService(db)
    return await db_service.get_analisis_completo(
        skip=skip, 
        limit=limit, 
        genero=genero, 
        ambiente=ambiente
    )

# RUTAS GENÉRICAS DESPUÉS (menos específicas)
@router.get("/", response_model=List[TiradorPydantic])
async def get_tiradores(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    genero: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de tiradores con filtros opcionales."""
    db_service = DatabaseService(db)
    return await db_service.get_tiradores(skip=skip, limit=limit, genero=genero)

@router.post("/", response_model=TiradorPydantic)
async def create_tirador(
    tirador: TiradorPydantic,
    db: Session = Depends(get_db)
):
    """Crear un nuevo tirador."""
    db_service = DatabaseService(db)
    return await db_service.create_tirador(tirador)

# RUTAS CON PARÁMETROS AL FINAL (menos específicas)
@router.get("/{tirador_id}", response_model=TiradorConSesiones)
async def get_tirador(
    tirador_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un tirador específico con sus sesiones de tiro."""
    db_service = DatabaseService(db)
    tirador = await db_service.get_tirador_by_id(tirador_id)
    if not tirador:
        raise HTTPException(status_code=404, detail="Tirador no encontrado")
    return tirador

@router.put("/{tirador_id}", response_model=TiradorPydantic)
async def update_tirador(
    tirador_id: int,
    tirador: TiradorPydantic,
    db: Session = Depends(get_db)
):
    """Actualizar un tirador existente."""
    db_service = DatabaseService(db)
    updated_tirador = await db_service.update_tirador(tirador_id, tirador)
    if not updated_tirador:
        raise HTTPException(status_code=404, detail="Tirador no encontrado")
    return updated_tirador

@router.delete("/{tirador_id}")
async def delete_tirador(
    tirador_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un tirador."""
    db_service = DatabaseService(db)
    success = await db_service.delete_tirador(tirador_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tirador no encontrado")
    return {"message": "Tirador eliminado exitosamente"}

@router.get("/{tirador_id}/sesiones", response_model=List[SesionTiroPydantic])
async def get_sesiones_tirador(
    tirador_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener sesiones de tiro de un tirador específico."""
    db_service = DatabaseService(db)
    return await db_service.get_sesiones_by_tirador(tirador_id, skip=skip, limit=limit)

@router.post("/{tirador_id}/sesiones", response_model=SesionTiroPydantic)
async def create_sesion_tiro(
    tirador_id: int,
    sesion: SesionTiroPydantic,
    db: Session = Depends(get_db)
):
    """Crear una nueva sesión de tiro para un tirador."""
    db_service = DatabaseService(db)
    sesion.tirador_id = tirador_id
    return await db_service.create_sesion_tiro(sesion)
