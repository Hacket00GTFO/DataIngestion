"""Pydantic models for data validation and serialization."""
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text
from sqlalchemy.sql import func

from app.database import Base

# Modelo SQLAlchemy para la base de datos
class DataRecord(Base):
    """Modelo SQLAlchemy para registros de datos en la base de datos"""
    __tablename__ = "data_records"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    data = Column(JSON)  # Almacenar los datos como JSON
    source = Column(String(255))
    is_processed = Column(Boolean, default=False)
    validation_errors = Column(Text, nullable=True)

# Modelo Pydantic para validación y serialización
class DataRecordPydantic(BaseModel):
    """Modelo Pydantic para registros de datos"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    data: Optional[Dict[str, Any]] = None
    source: Optional[str] = None
    is_processed: Optional[bool] = None
    validation_errors: Optional[str] = None

    class Config:
        from_attributes = True

class DataIngestionRequest(BaseModel):
    """Modelo para solicitudes de ingesta de datos."""
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
