"""API routes for manual data management endpoints."""
import logging
from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from app.models.data_models import DataIngestionRequest, DataProcessingResponse, ManualDataEntry
from app.services.data_service import DataService

LOGGER = logging.getLogger(__name__)

router = APIRouter()
data_service = DataService()

@router.post("/data/ingest", response_model=DataProcessingResponse)
async def ingest_data(request: DataIngestionRequest):
    """Endpoint para ingesta de nuevos datos."""
    try:
        result = await data_service.ingest_data(request.data)
        return DataProcessingResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/data/manual-entry", response_model=DataProcessingResponse)
async def add_manual_entry(entry: ManualDataEntry):
    """Endpoint para agregar datos manualmente."""
    try:
        # Convertir ManualDataEntry a diccionario
        data_dict = entry.model_dump(exclude_unset=True)
        
        # Calcular precisión si se proporcionan ambos valores
        if entry.tiros_exitosos is not None and entry.tiros_totales is not None and entry.tiros_totales > 0:
            data_dict["precision_porcentaje"] = (entry.tiros_exitosos / entry.tiros_totales) * 100
        
        # Agregar timestamp
        from datetime import datetime
        data_dict["created_at"] = datetime.now().isoformat()
        
        # Intentar guardar en base de datos, pero continuar si falla
        db_success = False
        try:
            db_success = await data_service.db_service.save_data_records([data_dict], source="manual_input")
        except Exception as db_error:
            # Si falla la BD, continuar en modo offline para demostración
            logging.warning(f"Base de datos no disponible, funcionando en modo offline: {str(db_error)}")
            db_success = False
        
        # Siempre retornar éxito para demostración, indicando el modo
        return DataProcessingResponse(
            success=True,
            message="Registro manual agregado exitosamente" + (" (modo offline - BD no disponible)" if not db_success else " (guardado en BD)"),
            processed_records=1,
            data=[data_dict]
        )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}") from e

@router.get("/data/statistics")
async def get_statistics() -> Dict[str, Any]:
    """Return aggregated metrics for the dataset."""
    try:
        # Obtener estadísticas básicas de la base de datos
        records = await data_service.db_service.get_data_records()
        data = [record.data for record in records if record.data]
        
        if not data:
            return {"success": True, "statistics": {"total_records": 0, "message": "No hay datos disponibles"}}
        
        # Calcular estadísticas básicas
        total_records = len(data)
        stats = {
            "total_records": total_records,
            "message": f"Estadísticas basadas en {total_records} registros"
        }
        
        return {"success": True, "statistics": stats}
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.exception("Error obteniendo estadisticas")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.get("/data")
async def get_data():
    """Endpoint para obtener los datos almacenados."""
    try:
        # Obtener datos de la base de datos
        records = await data_service.db_service.get_data_records()
        data = [record.data for record in records if record.data]
        return {
            "data": data,
            "total_records": len(data),
            "message": f"Se encontraron {len(data)} registros en la base de datos"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/data/schema")
async def get_data_schema():
    """Endpoint para obtener el esquema de datos para entrada manual."""
    try:
        # Esquema fijo para entrada manual de datos
        schema = [
            {"name": "nombre", "type": "string", "required": True, "description": "Nombre del tirador"},
            {"name": "edad", "type": "number", "required": False, "description": "Edad del tirador"},
            {"name": "genero", "type": "string", "required": False, "description": "Género (Masculino/Femenino)"},
            {"name": "experiencia_anos", "type": "number", "required": False, "description": "Años de experiencia"},
            {"name": "distancia_metros", "type": "number", "required": False, "description": "Distancia de tiro en metros"},
            {"name": "ambiente", "type": "string", "required": False, "description": "Ambiente (Interior/Exterior)"},
            {"name": "tiros_exitosos", "type": "number", "required": False, "description": "Número de tiros exitosos"},
            {"name": "tiros_totales", "type": "number", "required": False, "description": "Número total de tiros"},
            {"name": "tiempo_sesion_minutos", "type": "number", "required": False, "description": "Duración de la sesión en minutos"},
            {"name": "precision_porcentaje", "type": "number", "required": False, "description": "Precisión calculada automáticamente"}
        ]
        return {"columns": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
