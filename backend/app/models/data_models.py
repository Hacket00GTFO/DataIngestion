"""Pydantic models for data validation and serialization."""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class DataRecord(BaseModel):
    """Modelo base para registros de datos"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DataIngestionRequest(BaseModel):
    """Modelo para solicitudes de ingesta de datos"""
    data: List[Dict[str, Any]] = Field(..., description="Lista de registros a procesar")
    source: str = Field(..., description="Fuente de los datos")
    validation_rules: Optional[Dict[str, Any]] = None

class DataProcessingResponse(BaseModel):
    """Modelo para respuestas de procesamiento"""
    success: bool
    message: str
    processed_records: int
    errors: Optional[List[str]] = None
    data: Optional[List[Dict[str, Any]]] = None

class DataValidationResult(BaseModel):
    """Modelo para resultados de validación"""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    validated_data: Optional[List[Dict[str, Any]]] = None

class DataStatistics(BaseModel):
    """Modelo para estadísticas de datos"""
    total_records: int
    valid_records: int
    invalid_records: int
    processing_time: float
    columns: List[str]
    data_types: Dict[str, str]
