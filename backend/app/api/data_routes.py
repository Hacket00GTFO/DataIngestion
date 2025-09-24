"""API routes for data management endpoints."""
import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.data_models import DataIngestionRequest, DataProcessingResponse
from app.services.data_service import DataService

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

@router.post("/data/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    """Endpoint para subir y procesar archivo Excel."""
    try:
        # Guardar archivo temporalmente
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Procesar archivo
        stats = await data_service.process_excel_data(file_path)

        # Limpiar archivo temporal
        os.remove(file_path)

        return {
            "success": True,
            "message": "Archivo procesado exitosamente",
            "statistics": stats.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/data/statistics")
async def get_data_statistics():
    """Endpoint para obtener estadísticas de los datos."""
    try:
        # Aquí se obtendrían estadísticas de la base de datos
        return {
            "total_records": 0,
            "last_updated": None,
            "data_sources": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/data/schema")
async def get_data_schema():
    """Endpoint para obtener el esquema de datos."""
    try:
        # Aquí se retornaría el esquema basado en el Excel
        return {
            "columns": [
                {"name": "columna1", "type": "string", "required": True},
                {"name": "columna2", "type": "number", "required": False},
                # Se definirían según el Excel real
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
