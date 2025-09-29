"""Database management routes."""
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.data_models import DataRecordPydantic
from app.services.database_service import DatabaseService

router = APIRouter()

@router.get("/database/records", response_model=List[DataRecordPydantic])
async def get_records(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    source: Optional[str] = None,
    _db: Session = Depends(get_db)
):
    """Obtener registros de la base de datos."""
    try:
        db_service = DatabaseService()

        if source:
            records = await db_service.get_data_by_source(source)
        else:
            records = await db_service.get_data_records(limit, offset)

        return records
    except Exception as e:
        logging.error("Error obteniendo registros: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/database/statistics")
async def get_database_statistics(_db: Session = Depends(get_db)):
    """Obtener estadísticas de la base de datos."""
    try:
        db_service = DatabaseService()
        stats = await db_service.get_statistics()
        return stats
    except Exception as e:
        logging.error("Error obteniendo estadísticas: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/database/query")
async def execute_custom_query(
    query: str,
    _db: Session = Depends(get_db)
):
    """Ejecutar consulta personalizada en la base de datos."""
    try:
        # Validar que la consulta no sea peligrosa
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE']
        if any(keyword in query.upper() for keyword in dangerous_keywords):
            raise HTTPException(status_code=400, detail="Consulta no permitida")

        db_service = DatabaseService()
        results = await db_service.execute_custom_query(query)
        return {"results": results, "count": len(results)}
    except HTTPException:
        raise
    except Exception as e:
        logging.error("Error ejecutando consulta: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.put("/database/records/{record_id}/status")
async def update_record_status(
    record_id: int,
    is_processed: bool,
    validation_errors: Optional[str] = None,
    _db: Session = Depends(get_db)
):
    """Actualizar el estado de procesamiento de un registro."""
    try:
        db_service = DatabaseService()
        success = await db_service.update_record_status(record_id, is_processed, validation_errors)

        if success:
            return {"message": "Estado actualizado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        logging.error("Error actualizando estado: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e)) from e
