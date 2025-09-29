"""Excel data ingestion routes."""
import logging
import pandas as pd
from typing import List, Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.database_service import DatabaseService
from app.models.data_models import DataProcessingResponse

router = APIRouter()

def process_excel_data(file_content: bytes) -> List[Dict[str, Any]]:
    """Procesar datos de archivo Excel y convertirlos a formato JSON."""
    try:
        # Leer el archivo Excel desde bytes
        df = pd.read_excel(file_content, header=None)
        
        # Encontrar la fila con los encabezados (fila 1, índice 1)
        header_row = 1
        headers = df.iloc[header_row].tolist()
        
        # Crear DataFrame con los datos reales
        data_df = df.iloc[header_row + 1:].copy()
        data_df.columns = headers
        
        # Limpiar datos (eliminar filas completamente vacías)
        data_df = data_df.dropna(how='all')
        
        # Convertir a diccionario
        records = []
        for index, row in data_df.iterrows():
            record = {}
            for col in headers:
                if pd.notna(row[col]):
                    record[col] = str(row[col])
                else:
                    record[col] = None
            records.append(record)
        
        return records
        
    except Exception as e:
        logging.error("Error procesando archivo Excel: %s", str(e))
        raise HTTPException(status_code=400, detail=f"Error procesando archivo Excel: {str(e)}")

@router.post("/excel/upload", response_model=DataProcessingResponse, summary="Cargar datos desde archivo Excel")
async def upload_excel_data(file: UploadFile = File(...)):
    """Cargar y procesar datos desde un archivo Excel."""
    try:
        # Verificar que el archivo es Excel
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx o .xls)")
        
        # Leer contenido del archivo
        file_content = await file.read()
        
        # Procesar datos del Excel
        records = process_excel_data(file_content)
        
        if not records:
            raise HTTPException(status_code=400, detail="No se encontraron datos válidos en el archivo Excel")
        
        # Guardar en base de datos
        db_service = DatabaseService()
        success = await db_service.save_data_records(records, source="excel_upload")
        
        if success:
            return DataProcessingResponse(
                success=True,
                message=f"Se procesaron {len(records)} registros del archivo Excel exitosamente",
                processed_records=len(records),
                data=records
            )
        else:
            raise HTTPException(status_code=500, detail="Error guardando datos en la base de datos")
            
    except HTTPException:
        raise
    except Exception as e:
        logging.error("Error en upload_excel_data: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/excel/ingest-sample", response_model=DataProcessingResponse, summary="Ingerir datos de muestra del archivo evidencia big data.xlsx")
async def ingest_sample_data():
    """Ingerir los datos de muestra del archivo evidencia big data.xlsx."""
    try:
        # Datos de muestra del archivo Excel
        sample_records = [
            {
                "Nombre tirador": "Norberto",
                "Edad": "24",
                "Experiencia": "4 años",
                "Distancia de tiro ": "5 metros ",
                "Angulo ": "90 grados",
                "Altura de tirador": "1.7",
                "Peso ": "95 kg",
                "Ambiente": "Ventoso",
                "Genero": "Masculino",
                "Peso del balon": "500 g",
                "Tiempo de tiro": "1 segundo",
                "Tiro exitoso?": "2 de 6",
                "Diestro / zurdo": "Diestro",
                "Calibre de balon": "6"
            },
            {
                "Nombre tirador": "Jaob ",
                "Edad": "19",
                "Experiencia": "0 años",
                "Distancia de tiro ": "5 metros",
                "Angulo ": "90 grados ",
                "Altura de tirador": "1.7",
                "Peso ": "86 kg",
                "Ambiente": "Ventoso",
                "Genero": "Masculino",
                "Peso del balon": "500 g",
                "Tiempo de tiro": "2 segundos",
                "Tiro exitoso?": "0 de 6",
                "Diestro / zurdo": "Diestro",
                "Calibre de balon": "6"
            },
            {
                "Nombre tirador": "Hilary",
                "Edad": "19",
                "Experiencia": "0 años",
                "Distancia de tiro ": "3 metros",
                "Angulo ": "90 grados",
                "Altura de tirador": "1.55",
                "Peso ": "50 kg",
                "Ambiente": "Ventoso",
                "Genero": "Femenino",
                "Peso del balon": "500 g",
                "Tiempo de tiro": "1 segundo ",
                "Tiro exitoso?": "1 de 6",
                "Diestro / zurdo": "Diestro",
                "Calibre de balon": "6"
            },
            {
                "Nombre tirador": "Orlando",
                "Edad": "26",
                "Experiencia": "2 años",
                "Distancia de tiro ": "5 metros",
                "Angulo ": "90 grados",
                "Altura de tirador": "1.8",
                "Peso ": "80 kg",
                "Ambiente": "Ventoso",
                "Genero": "Masculino",
                "Peso del balon": "500 g",
                "Tiempo de tiro": "1 segundo",
                "Tiro exitoso?": "3 de 6",
                "Diestro / zurdo": "Diestro",
                "Calibre de balon": "6"
            },
            {
                "Nombre tirador": "Sofia",
                "Edad": "22",
                "Experiencia": "1 año",
                "Distancia de tiro ": "4 metros",
                "Angulo ": "90 grados",
                "Altura de tirador": "1.6",
                "Peso ": "55 kg",
                "Ambiente": "Ventoso",
                "Genero": "Femenino",
                "Peso del balon": "500 g",
                "Tiempo de tiro": "2 segundos",
                "Tiro exitoso?": "1 de 6",
                "Diestro / zurdo": "Diestro",
                "Calibre de balon": "6"
            },
            {
                "Nombre tirador": "Carlos",
                "Edad": "28",
                "Experiencia": "5 años",
                "Distancia de tiro ": "6 metros",
                "Angulo ": "90 grados",
                "Altura de tirador": "1.75",
                "Peso ": "78 kg",
                "Ambiente": "Ventoso",
                "Genero": "Masculino",
                "Peso del balon": "500 g",
                "Tiempo de tiro": "1 segundo",
                "Tiro exitoso?": "4 de 6",
                "Diestro / zurdo": "Diestro",
                "Calibre de balon": "6"
            },
            {
                "Nombre tirador": "Ana",
                "Edad": "21",
                "Experiencia": "0 años",
                "Distancia de tiro ": "3 metros",
                "Angulo ": "90 grados",
                "Altura de tirador": "1.58",
                "Peso ": "52 kg",
                "Ambiente": "Ventoso",
                "Genero": "Femenino",
                "Peso del balon": "500 g",
                "Tiempo de tiro": "3 segundos",
                "Tiro exitoso?": "0 de 6",
                "Diestro / zurdo": "Diestro",
                "Calibre de balon": "6"
            },
            {
                "Nombre tirador": "Miguel",
                "Edad": "30",
                "Experiencia": "3 años",
                "Distancia de tiro ": "5 metros",
                "Angulo ": "90 grados",
                "Altura de tirador": "1.72",
                "Peso ": "88 kg",
                "Ambiente": "Ventoso",
                "Genero": "Masculino",
                "Peso del balon": "500 g",
                "Tiempo de tiro": "1 segundo",
                "Tiro exitoso?": "5 de 6",
                "Diestro / zurdo": "Diestro",
                "Calibre de balon": "6"
            }
        ]
        
        # Guardar en base de datos
        db_service = DatabaseService()
        success = await db_service.save_data_records(sample_records, source="evidencia_big_data_excel")
        
        if success:
            return DataProcessingResponse(
                success=True,
                message=f"Se procesaron {len(sample_records)} registros de evidencia big data exitosamente",
                processed_records=len(sample_records),
                data=sample_records
            )
        else:
            raise HTTPException(status_code=500, detail="Error guardando datos en la base de datos")
            
    except Exception as e:
        logging.error("Error en ingest_sample_data: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
