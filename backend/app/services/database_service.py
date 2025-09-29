"""Database service for data operations."""
import logging
from typing import Dict, List

from sqlalchemy import text

from app.database import get_db, init_database, test_connection
from app.models.data_models import DataRecord, DataRecordPydantic

class DatabaseService:
    """Servicio para operaciones de base de datos"""

    def __init__(self):
        pass

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
            import traceback
            logging.error("Traceback: %s", traceback.format_exc())
            return False
        finally:
            db.close()

    async def get_data_records(self, limit: int = 100, offset: int = 0) -> List[DataRecordPydantic]:
        """Obtener registros de datos de la base de datos."""
        db = next(get_db())
        try:
            records = db.query(DataRecord).offset(offset).limit(limit).all()
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
        db = next(get_db())
        try:
            total_records = db.query(DataRecord).count()
            processed_records = db.query(DataRecord).filter(DataRecord.is_processed.is_(True)).count()
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

