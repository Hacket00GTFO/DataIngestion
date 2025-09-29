"""API routes for data ingestion and reporting."""
from __future__ import annotations

import logging
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from app.services.data_service import DataService

LOGGER = logging.getLogger(__name__)

router = APIRouter()
data_service = DataService()


@router.post("/data/upload-excel")
async def upload_excel(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload an Excel or CSV file and push its contents into PostgreSQL."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nombre de archivo inválido")

    try:
        with TemporaryDirectory() as tmpdir:
            temp_input = Path(tmpdir) / file.filename
            temp_input.write_bytes(await file.read())

            csv_path = await _ensure_csv(temp_input)
            rows_loaded = await run_in_threadpool(data_service.load_csv_to_staging, str(csv_path))
            transform_result = await run_in_threadpool(data_service.transform_staging_to_final)
            await run_in_threadpool(data_service.clear_staging)

        metrics = {
            "filas_cargadas": rows_loaded,
            "filas_leidas": transform_result["read"],
            "filas_insertadas": transform_result["inserted"],
            "filas_rechazadas": transform_result["invalid"],
        }

        return {
            "success": True,
            "message": "Archivo procesado exitosamente",
            "metrics": metrics,
            "rechazados": transform_result["invalid_rows"],
        }
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.exception("Error procesando archivo de datos")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/data/statistics")
async def get_statistics() -> Dict[str, Any]:
    """Return aggregated metrics for the tiros dataset."""
    try:
        stats = await run_in_threadpool(data_service.get_statistics)
        return {"success": True, "statistics": stats}
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.exception("Error obteniendo estadisticas")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/data/schema")
async def get_schema() -> Dict[str, Any]:
    """Describe the tiros table schema."""
    try:
        schema = await run_in_threadpool(data_service.get_schema)
        return {"success": True, "columns": schema}
    except Exception as exc:  # pylint: disable=broad-except
        LOGGER.exception("Error obteniendo esquema")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


async def _ensure_csv(path: Path) -> Path:
    """If the provided path points to Excel, convert it to CSV."""
    suffix = path.suffix.lower()
    if suffix in {".csv"}:
        return path

    if suffix in {".xlsx", ".xls"}:
        df = await run_in_threadpool(pd.read_excel, path)
        csv_path = path.with_suffix(".csv")
        await run_in_threadpool(df.to_csv, csv_path, index=False)
        return csv_path

    raise HTTPException(status_code=400, detail="Formato de archivo no soportado - use CSV o Excel")
