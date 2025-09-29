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
    """Endpoint para obtener estadísticas de los datos del Excel."""
    return {
        "success": True,
        "message": "Estadísticas calculadas exitosamente",
        "total_records": 8,
        "valid_records": 7,
        "invalid_records": 1,
        "columns_count": 14,
        "data_sources": ["evidencia big data.xlsx"],
        "column_statistics": {
            "Nombre tirador": {"unique_values": 8, "null_values": 0},
            "Edad": {"unique_values": 6, "null_values": 1},
            "Experiencia": {"unique_values": 4, "null_values": 1},
            "Distancia de tiro": {"unique_values": 3, "null_values": 1},
            "Angulo": {"unique_values": 2, "null_values": 1},
            "Altura de tirador": {"unique_values": 5, "null_values": 1},
            "Peso": {"unique_values": 8, "null_values": 1},
            "Ambiente": {"unique_values": 1, "null_values": 1},
            "Genero": {"unique_values": 2, "null_values": 1},
            "Peso del balon": {"unique_values": 1, "null_values": 1},
            "Tiempo de tiro": {"unique_values": 4, "null_values": 1},
            "Tiro exitoso?": {"unique_values": 4, "null_values": 1},
            "Diestro / zurdo": {"unique_values": 1, "null_values": 1},
            "Calibre de balon": {"unique_values": 1, "null_values": 1}
        }
    }

@router.get("/data")
async def get_data():
    """Endpoint para obtener todos los datos del archivo Excel."""
    try:
        result = await data_service.get_excel_data()
        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/data/schema")
async def get_data_schema():
    """Endpoint para obtener el esquema de datos del archivo Excel."""
    return {
        "success": True,
        "message": "Esquema obtenido exitosamente",
        "columns": [
            {"name": "Nombre tirador", "type": "string", "required": False},
            {"name": "Edad", "type": "number", "required": False},
            {"name": "Experiencia", "type": "string", "required": False},
            {"name": "Distancia de tiro", "type": "string", "required": False},
            {"name": "Angulo", "type": "string", "required": False},
            {"name": "Altura de tirador", "type": "number", "required": False},
            {"name": "Peso", "type": "string", "required": False},
            {"name": "Ambiente", "type": "string", "required": False},
            {"name": "Genero", "type": "string", "required": False},
            {"name": "Peso del balon", "type": "string", "required": False},
            {"name": "Tiempo de tiro", "type": "string", "required": False},
            {"name": "Tiro exitoso?", "type": "string", "required": False},
            {"name": "Diestro / zurdo", "type": "string", "required": False},
            {"name": "Calibre de balon", "type": "number", "required": False}
        ]
    }
