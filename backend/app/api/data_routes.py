"""API routes for data management endpoints."""
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
        # Verificar que el archivo es Excel
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx o .xls)")
        
        # Leer contenido del archivo
        file_content = await file.read()
        
        # Procesar datos del Excel usando la función de excel_routes
        from app.api.excel_routes import process_excel_data
        records = process_excel_data(file_content)
        
        if not records:
            raise HTTPException(status_code=400, detail="No se encontraron datos válidos en el archivo Excel")
        
        # Guardar en base de datos
        success = await data_service.db_service.save_data_records(records, source="excel_upload")
        
        if success:
            return {
                "success": True,
                "message": f"Se procesaron {len(records)} registros del archivo Excel exitosamente",
                "processed_records": len(records),
                "data": records
            }
        else:
            raise HTTPException(status_code=500, detail="Error guardando datos en la base de datos")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}") from e

@router.get("/data/statistics")
async def get_data_statistics():
    """Endpoint para obtener estadísticas de los datos."""
    try:
        # Obtener estadísticas de la base de datos
        stats = await data_service.db_service.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

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
    """Endpoint para obtener el esquema de datos."""
    try:
        # Obtener datos de la base de datos para analizar el esquema
        records = await data_service.db_service.get_data_records(limit=1)
        if records and records[0].data:
            # Analizar el primer registro para obtener el esquema
            sample_data = records[0].data
            schema = []
            for key, value in sample_data.items():
                # Inferir tipo de dato
                if isinstance(value, bool):
                    data_type = "boolean"
                elif isinstance(value, (int, float)):
                    data_type = "number"
                else:
                    data_type = "string"
                
                schema.append({
                    "name": key,
                    "type": data_type,
                    "required": True,
                    "description": f"Campo {key} del archivo Excel"
                })
            return {"columns": schema}
        else:
            # Si no hay datos, usar esquema por defecto del archivo Excel
            schema = await data_service.analyze_excel_schema()
            return {"columns": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
