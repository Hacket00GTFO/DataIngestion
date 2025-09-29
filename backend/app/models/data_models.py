"""Pydantic models for data validation and serialization."""
# pylint: disable=not-callable,line-too-long
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text, DECIMAL, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

# Modelos SQLAlchemy para la base de datos

class Tirador(Base):
    """Modelo SQLAlchemy para tiradores"""
    __tablename__ = "tiradores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer)
    experiencia_anos = Column(Integer)
    altura = Column(DECIMAL(4, 2))  # en metros
    peso = Column(DECIMAL(5, 2))    # en kg
    genero = Column(String(20))
    mano_dominante = Column(String(20))  # Diestro/Zurdo
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con sesiones de tiro
    sesiones_tiro = relationship("SesionTiro", back_populates="tirador")

class SesionTiro(Base):
    """Modelo SQLAlchemy para sesiones de tiro"""
    __tablename__ = "sesiones_tiro"

    id = Column(Integer, primary_key=True, index=True)
    tirador_id = Column(Integer, ForeignKey("tiradores.id"), nullable=False)
    distancia_metros = Column(DECIMAL(4, 2))
    angulo_grados = Column(Integer)
    ambiente = Column(String(50))
    peso_balon = Column(DECIMAL(6, 2))  # en gramos
    calibre_balon = Column(Integer)
    tiempo_tiro_segundos = Column(DECIMAL(4, 2))
    tiros_exitosos = Column(Integer)
    tiros_totales = Column(Integer)
    fecha_sesion = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con tirador
    tirador = relationship("Tirador", back_populates="sesiones_tiro")

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

# Modelo TiroExcel eliminado - se usa solo ingesta manual

# Modelos Pydantic para validación y serialización

class TiradorPydantic(BaseModel):
    """Modelo Pydantic para tiradores"""
    id: Optional[int] = None
    nombre: str
    edad: Optional[int] = None
    experiencia_anos: Optional[int] = None
    altura: Optional[float] = None
    peso: Optional[float] = None
    genero: Optional[str] = None
    mano_dominante: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SesionTiroPydantic(BaseModel):
    """Modelo Pydantic para sesiones de tiro"""
    id: Optional[int] = None
    tirador_id: int
    distancia_metros: Optional[float] = None
    angulo_grados: Optional[int] = None
    ambiente: Optional[str] = None
    peso_balon: Optional[float] = None
    calibre_balon: Optional[int] = None
    tiempo_tiro_segundos: Optional[float] = None
    tiros_exitosos: Optional[int] = None
    tiros_totales: Optional[int] = None
    fecha_sesion: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TiradorConSesiones(TiradorPydantic):
    """Modelo Pydantic para tirador con sus sesiones de tiro"""
    sesiones_tiro: Optional[List[SesionTiroPydantic]] = []

class SesionTiroConTirador(SesionTiroPydantic):
    """Modelo Pydantic para sesión de tiro con información del tirador"""
    tirador: Optional[TiradorPydantic] = None

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
    """Modelo para solicitudes de ingesta de datos manual."""
    data: List[Dict[str, Any]] = Field(..., description="Lista de registros a procesar manualmente")
    source: str = Field(default="manual_input", description="Fuente de los datos (siempre manual)")
    validation_rules: Optional[Dict[str, Any]] = None

class ManualDataEntry(BaseModel):
    """Modelo para entrada manual de datos básicos de análisis."""
    # Datos básicos del tirador
    nombre: str = Field(..., description="Nombre del tirador")
    edad: Optional[int] = Field(None, description="Edad del tirador")
    genero: Optional[str] = Field(None, description="Género (Masculino/Femenino)")
    experiencia_anos: Optional[int] = Field(None, description="Años de experiencia")
    
    # Datos de la sesión de tiro
    distancia_metros: Optional[float] = Field(None, description="Distancia de tiro en metros")
    ambiente: Optional[str] = Field(None, description="Ambiente (Interior/Exterior)")
    tiros_exitosos: Optional[int] = Field(None, description="Número de tiros exitosos")
    tiros_totales: Optional[int] = Field(None, description="Número total de tiros")
    tiempo_sesion_minutos: Optional[float] = Field(None, description="Duración de la sesión en minutos")

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

class TiradorStatistics(BaseModel):
    """Modelo para estadísticas de tiradores"""
    total_tiradores: int
    generos_unicos: int
    edad_promedio: Optional[float] = None
    experiencia_promedio: Optional[float] = None
    altura_promedio: Optional[float] = None
    peso_promedio: Optional[float] = None
    primer_registro: Optional[datetime] = None
    ultimo_registro: Optional[datetime] = None

class SesionStatistics(BaseModel):
    """Modelo para estadísticas de sesiones de tiro"""
    total_sesiones: int
    precision_promedio: Optional[float] = None
    distancia_promedio: Optional[float] = None
    tiempo_promedio: Optional[float] = None
    ambientes_unicos: int
    primera_sesion: Optional[datetime] = None
    ultima_sesion: Optional[datetime] = None

# Modelo TiroExcelPydantic eliminado - se usa solo ingesta manual

class AnalisisCompleto(BaseModel):
    """Modelo para análisis completo de tiradores y sesiones"""
    nombre: str
    edad: Optional[int] = None
    experiencia_anos: Optional[int] = None
    genero: Optional[str] = None
    altura: Optional[float] = None
    peso: Optional[float] = None
    mano_dominante: Optional[str] = None
    distancia_metros: Optional[float] = None
    angulo_grados: Optional[int] = None
    ambiente: Optional[str] = None
    peso_balon: Optional[float] = None
    calibre_balon: Optional[int] = None
    tiempo_tiro_segundos: Optional[float] = None
    tiros_exitosos: Optional[int] = None
    tiros_totales: Optional[int] = None
    precision_porcentaje: Optional[float] = None
    fecha_sesion: Optional[datetime] = None
