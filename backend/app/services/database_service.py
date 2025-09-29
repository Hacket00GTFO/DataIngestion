"""Database service for data operations."""
# pylint: disable=broad-exception-caught,line-too-long,trailing-whitespace,import-outside-toplevel,not-callable
import logging
import traceback
from typing import Any, Dict, List, Optional

import sqlalchemy as sa
from sqlalchemy import text, cast, Float
sqlfunc: Any = sa.func
from sqlalchemy.orm import Session

from app.database import get_db, init_database, test_connection
from app.models.data_models import (
    DataRecord, DataRecordPydantic, 
    Tirador, TiradorPydantic, TiradorConSesiones,
    SesionTiro, SesionTiroPydantic,
    TiradorStatistics, SesionStatistics, AnalisisCompleto
)

class DatabaseService:
    """Servicio para operaciones de base de datos"""

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    async def initialize_database(self):
        """Inicializar la base de datos y crear tablas."""
        try:
            # Probar conexión
            if not test_connection():
                raise ConnectionError("No se pudo conectar a la base de datos")

            # Inicializar tablas
            init_database()
            logging.info("Base de datos inicializada correctamente")
            return True
        except Exception as e:
            logging.error("Error inicializando base de datos: %s", str(e))
            return False

    async def save_data_records(self, data: List[Dict], source: str) -> bool:
        """Guardar registros de datos en la base de datos."""
        db = next(get_db())
        try:
            logging.info("Starting to save %d records to database", len(data))
            for i, record_data in enumerate(data):
                logging.info("Processing record %d: %s", i, record_data)
                db_record = DataRecord(
                    data=record_data,
                    source=source,
                    is_processed=False
                )
                db.add(db_record)

            logging.info("Committing transaction...")
            db.commit()
            logging.info("Guardados %d registros en la base de datos", len(data))
            return True
        except Exception as e:
            db.rollback()
            logging.error("Error guardando registros: %s", str(e))
            logging.error("Exception type: %s", type(e).__name__)
            logging.error("Traceback: %s", traceback.format_exc())
            return False
        finally:
            db.close()

    async def get_data_records(self, limit: int = 100, offset: int = 0) -> List[DataRecordPydantic]:
        """Obtener registros de datos de la base de datos."""
        # Verificar conexión antes de intentar operaciones
        if not test_connection():
            logging.warning("Base de datos no disponible - retornando lista vacía")
            return []
            
        db = next(get_db())
        try:
            records = db.query(DataRecord).order_by(DataRecord.created_at.desc()).offset(offset).limit(limit).all()
            return [DataRecordPydantic.model_validate(record) for record in records]
        except Exception as e:
            logging.error("Error obteniendo registros: %s", str(e))
            return []
        finally:
            db.close()

    async def get_data_by_source(self, source: str) -> List[DataRecordPydantic]:
        """Obtener registros por fuente."""
        db = next(get_db())
        try:
            records = db.query(DataRecord).filter(DataRecord.source == source).all()
            return [DataRecordPydantic.model_validate(record) for record in records]
        except Exception as e:
            logging.error("Error obteniendo registros por fuente: %s", str(e))
            return []
        finally:
            db.close()

    async def update_record_status(self, record_id: int, is_processed: bool, validation_errors: str = None):
        """Actualizar el estado de procesamiento de un registro."""
        db = next(get_db())
        try:
            record = db.query(DataRecord).filter(DataRecord.id == record_id).first()
            if record:
                record.is_processed = is_processed
                if validation_errors:
                    record.validation_errors = validation_errors
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            logging.error("Error actualizando estado del registro: %s", str(e))
            return False
        finally:
            db.close()

    async def get_statistics(self) -> Dict:
        """Obtener estadísticas de los datos."""
        # Verificar conexión antes de intentar operaciones
        if not test_connection():
            logging.warning("Base de datos no disponible - retornando estadísticas vacías")
            return {
                "total_records": 0,
                "processed_records": 0,
                "unprocessed_records": 0,
                "sources": [],
                "processing_rate": 0
            }
            
        db = next(get_db())
        try:
            total_records = db.query(DataRecord).count()
            processed_records = db.query(DataRecord).filter(DataRecord.is_processed).count()
            sources = db.query(DataRecord.source).distinct().all()

            return {
                "total_records": total_records,
                "processed_records": processed_records,
                "unprocessed_records": total_records - processed_records,
                "sources": [source[0] for source in sources],
                "processing_rate": (
                    processed_records / total_records * 100
                    if total_records > 0 else 0
                )
            }
        except Exception as e:
            logging.error("Error obteniendo estadísticas: %s", str(e))
            return {}
        finally:
            db.close()

    async def execute_custom_query(self, query: str) -> List[Dict]:
        """Ejecutar consulta personalizada."""
        db = next(get_db())
        try:
            result = db.execute(text(query))
            columns = result.keys()
            rows = result.fetchall()

            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logging.error("Error ejecutando consulta personalizada: %s", str(e))
            return []
        finally:
            db.close()

    # Métodos para tiradores
    async def get_tiradores(self, skip: int = 0, limit: int = 100, genero: Optional[str] = None) -> List[TiradorPydantic]:
        """Obtener lista de tiradores."""
        # Verificar conexión antes de intentar operaciones
        if not test_connection():
            logging.warning("Base de datos no disponible - retornando lista vacía de tiradores")
            return []
            
        db = self.db or next(get_db())
        try:
            query = db.query(Tirador)
            if genero:
                query = query.filter(Tirador.genero == genero)
            
            tiradores = query.order_by(Tirador.nombre.asc()).offset(skip).limit(limit).all()
            return [TiradorPydantic.model_validate(tirador) for tirador in tiradores]
        except Exception as e:
            logging.error("Error obteniendo tiradores: %s", str(e))
            return []
        finally:
            if not self.db:
                db.close()

    async def get_tirador_by_id(self, tirador_id: int) -> Optional[TiradorConSesiones]:
        """Obtener un tirador por ID con sus sesiones."""
        db = self.db or next(get_db())
        try:
            tirador = db.query(Tirador).filter(Tirador.id == tirador_id).first()
            if not tirador:
                return None
            
            # Obtener sesiones del tirador
            sesiones = db.query(SesionTiro).filter(SesionTiro.tirador_id == tirador_id).all()
            
            tirador_data = TiradorConSesiones.model_validate(tirador)
            tirador_data.sesiones_tiro = [SesionTiroPydantic.model_validate(sesion) for sesion in sesiones]
            
            return tirador_data
        except Exception as e:
            logging.error("Error obteniendo tirador por ID: %s", str(e))
            return None
        finally:
            if not self.db:
                db.close()

    async def create_tirador(self, tirador: TiradorPydantic) -> TiradorPydantic:
        """Crear un nuevo tirador."""
        db = self.db or next(get_db())
        try:
            db_tirador = Tirador(**tirador.model_dump(exclude={'id', 'created_at', 'updated_at'}))
            db.add(db_tirador)
            db.commit()
            db.refresh(db_tirador)
            return TiradorPydantic.model_validate(db_tirador)
        except Exception as e:
            db.rollback()
            logging.error("Error creando tirador: %s", str(e))
            raise
        finally:
            if not self.db:
                db.close()

    async def update_tirador(self, tirador_id: int, tirador: TiradorPydantic) -> Optional[TiradorPydantic]:
        """Actualizar un tirador existente."""
        db = self.db or next(get_db())
        try:
            db_tirador = db.query(Tirador).filter(Tirador.id == tirador_id).first()
            if not db_tirador:
                return None
            
            for key, value in tirador.model_dump(exclude_unset=True).items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(db_tirador, key, value)
            
            db.commit()
            db.refresh(db_tirador)
            return TiradorPydantic.model_validate(db_tirador)
        except Exception as e:
            db.rollback()
            logging.error("Error actualizando tirador: %s", str(e))
            raise
        finally:
            if not self.db:
                db.close()

    async def delete_tirador(self, tirador_id: int) -> bool:
        """Eliminar un tirador."""
        db = self.db or next(get_db())
        try:
            db_tirador = db.query(Tirador).filter(Tirador.id == tirador_id).first()
            if not db_tirador:
                return False
            
            db.delete(db_tirador)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logging.error("Error eliminando tirador: %s", str(e))
            return False
        finally:
            if not self.db:
                db.close()

    # Métodos para sesiones de tiro
    async def get_sesiones_by_tirador(self, tirador_id: int, skip: int = 0, limit: int = 100) -> List[SesionTiroPydantic]:
        """Obtener sesiones de tiro de un tirador."""
        db = self.db or next(get_db())
        try:
            sesiones = db.query(SesionTiro).filter(
                SesionTiro.tirador_id == tirador_id
            ).order_by(SesionTiro.fecha_sesion.desc()).offset(skip).limit(limit).all()         
            return [SesionTiroPydantic.model_validate(sesion) for sesion in sesiones]
        except Exception as e:
            logging.error("Error obteniendo sesiones del tirador: %s", str(e))
            return []
        finally:
            if not self.db:
                db.close()

    async def create_sesion_tiro(self, sesion: SesionTiroPydantic) -> SesionTiroPydantic:
        """Crear una nueva sesión de tiro."""
        db = self.db or next(get_db())
        try:
            db_sesion = SesionTiro(**sesion.model_dump(exclude={'id', 'created_at', 'updated_at'}))
            db.add(db_sesion)
            db.commit()
            db.refresh(db_sesion)
            return SesionTiroPydantic.model_validate(db_sesion)
        except Exception as e:
            db.rollback()
            logging.error("Error creando sesión de tiro: %s", str(e))
            raise
        finally:
            if not self.db:
                db.close()

    # Métodos para estadísticas
    async def get_tirador_statistics(self) -> TiradorStatistics:
        """Obtener estadísticas de tiradores."""
        db = self.db or next(get_db())
        try:
            stats = db.query(
                sqlfunc.count(Tirador.id).label('total_tiradores'),  # pylint: disable=not-callable
                sqlfunc.count(sqlfunc.distinct(Tirador.genero)).label('generos_unicos'),  # pylint: disable=not-callable
                sqlfunc.avg(Tirador.edad).label('edad_promedio'),
                sqlfunc.avg(Tirador.experiencia_anos).label('experiencia_promedio'),
                sqlfunc.avg(Tirador.altura).label('altura_promedio'),
                sqlfunc.avg(Tirador.peso).label('peso_promedio'),
                sqlfunc.min(Tirador.created_at).label('primer_registro'),
                sqlfunc.max(Tirador.created_at).label('ultimo_registro')
            ).first()
            
            return TiradorStatistics(
                total_tiradores=stats.total_tiradores or 0,
                generos_unicos=stats.generos_unicos or 0,
                edad_promedio=float(stats.edad_promedio) if stats.edad_promedio else None,
                experiencia_promedio=float(stats.experiencia_promedio) if stats.experiencia_promedio else None,
                altura_promedio=float(stats.altura_promedio) if stats.altura_promedio else None,
                peso_promedio=float(stats.peso_promedio) if stats.peso_promedio else None,
                primer_registro=stats.primer_registro,
                ultimo_registro=stats.ultimo_registro
            )
        except Exception as e:
            logging.error("Error obteniendo estadísticas de tiradores: %s", str(e))
            return TiradorStatistics(total_tiradores=0, generos_unicos=0)
        finally:
            if not self.db:
                db.close()

    async def get_sesion_statistics(self) -> SesionStatistics:
        """Obtener estadísticas de sesiones de tiro."""
        db = self.db or next(get_db())
        try:
            stats = db.query(
                sqlfunc.count(SesionTiro.id).label('total_sesiones'),  # pylint: disable=not-callable
                sqlfunc.avg(
                    cast(SesionTiro.tiros_exitosos, Float) / cast(SesionTiro.tiros_totales, Float) * 100
                ).label('precision_promedio'),
                sqlfunc.avg(SesionTiro.distancia_metros).label('distancia_promedio'),
                sqlfunc.avg(SesionTiro.tiempo_tiro_segundos).label('tiempo_promedio'),
                sqlfunc.count(sqlfunc.distinct(SesionTiro.ambiente)).label('ambientes_unicos'),  # pylint: disable=not-callable
                sqlfunc.min(SesionTiro.fecha_sesion).label('primera_sesion'),
                sqlfunc.max(SesionTiro.fecha_sesion).label('ultima_sesion')
            ).first()
            
            return SesionStatistics(
                total_sesiones=stats.total_sesiones or 0,
                precision_promedio=float(stats.precision_promedio) if stats.precision_promedio else None,
                distancia_promedio=float(stats.distancia_promedio) if stats.distancia_promedio else None,
                tiempo_promedio=float(stats.tiempo_promedio) if stats.tiempo_promedio else None,
                ambientes_unicos=stats.ambientes_unicos or 0,
                primera_sesion=stats.primera_sesion,
                ultima_sesion=stats.ultima_sesion
            )
        except Exception as e:
            logging.error("Error obteniendo estadísticas de sesiones: %s", str(e))
            return SesionStatistics(total_sesiones=0, ambientes_unicos=0)
        finally:
            if not self.db:
                db.close()

    async def get_analisis_completo(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        genero: Optional[str] = None,
        ambiente: Optional[str] = None
    ) -> List[AnalisisCompleto]:
        """Obtener análisis completo de tiradores y sesiones."""
        db = self.db or next(get_db())
        try:
            query = db.query(
                Tirador.nombre,
                Tirador.edad,
                Tirador.experiencia_anos,
                Tirador.genero,
                Tirador.altura,
                Tirador.peso,
                Tirador.mano_dominante,
                SesionTiro.distancia_metros,
                SesionTiro.angulo_grados,
                SesionTiro.ambiente,
                SesionTiro.peso_balon,
                SesionTiro.calibre_balon,
                SesionTiro.tiempo_tiro_segundos,
                SesionTiro.tiros_exitosos,
                SesionTiro.tiros_totales,
                sa.case(
                    (SesionTiro.tiros_totales > 0,
                     cast(SesionTiro.tiros_exitosos, Float) / cast(SesionTiro.tiros_totales, Float) * 100),
                    else_=0,
                ).label('precision_porcentaje'),
                SesionTiro.fecha_sesion
            ).join(SesionTiro, Tirador.id == SesionTiro.tirador_id)
            
            if genero:
                query = query.filter(Tirador.genero == genero)
            if ambiente:
                query = query.filter(SesionTiro.ambiente == ambiente)
            
            results = query.order_by(Tirador.nombre.asc()).offset(skip).limit(limit).all()
            
            return [
                AnalisisCompleto(
                    nombre=row.nombre,
                    edad=row.edad,
                    experiencia_anos=row.experiencia_anos,
                    genero=row.genero,
                    altura=float(row.altura) if row.altura else None,
                    peso=float(row.peso) if row.peso else None,
                    mano_dominante=row.mano_dominante,
                    distancia_metros=float(row.distancia_metros) if row.distancia_metros else None,
                    angulo_grados=row.angulo_grados,
                    ambiente=row.ambiente,
                    peso_balon=float(row.peso_balon) if row.peso_balon else None,
                    calibre_balon=row.calibre_balon,
                    tiempo_tiro_segundos=float(row.tiempo_tiro_segundos) if row.tiempo_tiro_segundos else None,
                    tiros_exitosos=row.tiros_exitosos,
                    tiros_totales=row.tiros_totales,
                    precision_porcentaje=float(row.precision_porcentaje) if row.precision_porcentaje else None,
                    fecha_sesion=row.fecha_sesion
                )
                for row in results
            ]
        except Exception as e:
            logging.error("Error obteniendo análisis completo: %s", str(e))
            return []
        finally:
            if not self.db:
                db.close()

    async def delete_all_data(self) -> bool:
        """Eliminar todos los datos de tiradores y sesiones de tiro."""
        db = self.db or next(get_db())
        try:
            # Eliminar primero las sesiones de tiro (por la relación de foreign key)
            sesiones_deleted = db.query(SesionTiro).count()
            db.query(SesionTiro).delete()
            
            # Luego eliminar los tiradores
            tiradores_deleted = db.query(Tirador).count()
            db.query(Tirador).delete()
            
            # También eliminar los registros de datos generales si existen
            data_records_deleted = db.query(DataRecord).count()
            db.query(DataRecord).delete()
            
            db.commit()
            logging.info(f"Eliminados {sesiones_deleted} sesiones de tiro, {tiradores_deleted} tiradores y {data_records_deleted} registros de datos")
            return True
        except Exception as e:
            db.rollback()
            logging.error("Error eliminando todos los datos: %s", str(e))
            return False
        finally:
            if not self.db:
                db.close()

    # Funcionalidad de Excel eliminada - solo ingesta manual disponible
