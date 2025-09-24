"""Main data service for processing and managing data operations."""
import logging
from typing import Dict, List
import pandas as pd
from app.models.data_models import DataStatistics
from app.utils.data_validator import DataValidator
from app.utils.data_processor import DataProcessor

class DataService:
    """Servicio principal para el procesamiento de datos"""

    def __init__(self):
        self.validator = DataValidator()
        self.processor = DataProcessor()

    async def process_excel_data(self, file_path: str) -> DataStatistics:
        """Procesa datos desde archivo Excel."""
        try:
            # Leer archivo Excel
            df = pd.read_excel(file_path)

            # Validar datos
            validation_result = self.validator.validate_dataframe(df)

            # Procesar datos si son válidos
            if validation_result.is_valid:
                processed_data = self.processor.clean_data(df)
                stats = self._calculate_statistics(processed_data)
            else:
                stats = self._calculate_statistics(df)
                stats.valid_records = 0
                stats.invalid_records = len(df)

            return stats

        except Exception as e:
            raise ValueError(f"Error procesando archivo Excel: {str(e)}") from e

    async def ingest_data(self, data: List[Dict]) -> Dict:
        """Ingesta nuevos registros de datos."""
        try:
            # Convertir a DataFrame
            df = pd.DataFrame(data)

            # Validar datos
            validation_result = self.validator.validate_dataframe(df)

            if not validation_result.is_valid:
                return {
                    "success": False,
                    "message": "Datos inválidos",
                    "errors": validation_result.errors
                }

            # Procesar datos
            processed_data = self.processor.clean_data(df)

            # Aquí se guardaría en base de datos
            # await self._save_to_database(processed_data)

            return {
                "success": True,
                "message": f"Procesados {len(processed_data)} registros exitosamente",
                "processed_records": len(processed_data),
                "data": processed_data.to_dict('records')
            }

        except (ValueError, TypeError, KeyError) as e:
            return {
                "success": False,
                "message": f"Error en ingesta: {str(e)}",
                "errors": [str(e)]
            }
        except Exception as e:
            # Log the full exception for debugging
            logging.error(f"Unexpected error in data ingestion: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": "Error inesperado en ingesta",
                "errors": [f"Error interno: {str(e)}"]
            }

    def _calculate_statistics(self, df: pd.DataFrame) -> DataStatistics:
        """Calcula estadísticas de los datos."""
        return DataStatistics(
            total_records=len(df),
            valid_records=len(df.dropna()),
            invalid_records=len(df) - len(df.dropna()),
            processing_time=0.0,  # Se calcularía el tiempo real
            columns=list(df.columns),
            data_types=df.dtypes.astype(str).to_dict()
        )
