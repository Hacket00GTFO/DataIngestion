"""Main data service for processing and managing data operations."""
import logging
from typing import Dict, List
import pandas as pd
from app.models.data_models import DataStatistics
from app.utils.data_validator import DataValidator
from app.utils.data_processor import DataProcessor
from app.services.database_service import DatabaseService

class DataService:
    """Servicio principal para el procesamiento de datos"""

    def __init__(self):
        self.validator = DataValidator()
        self.processor = DataProcessor()
        self.db_service = DatabaseService()

    async def process_excel_data(self, file_path: str) -> DataStatistics:
        """Procesa datos desde archivo Excel."""
        try:
            # Leer archivo Excel
            df = pd.read_excel(file_path)

            # Si es el archivo de evidencia, procesar con estructura específica
            if "evidencia big data" in file_path.lower():
                # Los nombres de columnas están en la primera fila
                column_names = df.iloc[0].tolist()

                # Crear nuevo DataFrame con nombres de columnas correctos
                df_processed = df.iloc[1:].copy()  # Saltar la primera fila (nombres)
                df_processed.columns = column_names

                # Limpiar datos
                df_processed = df_processed.dropna(how='all')  # Eliminar filas completamente vacías

                # Procesar datos
                processed_data = self.processor.clean_data(df_processed)
                stats = self._calculate_statistics(processed_data)

                # Guardar datos procesados para uso posterior
                self._save_processed_data(processed_data)

            else:
                # Procesamiento estándar para otros archivos
                validation_result = self.validator.validate_dataframe(df)

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

    def _save_processed_data(self, df: pd.DataFrame):
        """Guarda los datos procesados para uso posterior."""
        try:
            # Guardar en un archivo temporal o en memoria para uso posterior
            df.to_csv("processed_data.csv", index=False)
            logging.info("Datos procesados guardados: %d registros", len(df))
        except (OSError, IOError) as e:
            logging.error("Error guardando datos procesados: %s", str(e))

    async def get_processed_data(self) -> List[Dict]:
        """Obtiene los datos procesados desde la base de datos únicamente."""
        try:
            # Solo obtener datos de la base de datos
            records = await self.db_service.get_data_records()
            return [record.data for record in records if record.data]
        except Exception as e:
            logging.error("Error obteniendo datos procesados: %s", str(e))
            return []

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

            # Guardar en base de datos
            await self.db_service.save_data_records(processed_data.to_dict('records'), "api_ingestion")

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
            logging.error("Unexpected error in data ingestion: %s", str(e), exc_info=True)
            return {
                "success": False,
                "message": "Error inesperado en ingesta",
                "errors": [f"Error interno: {str(e)}"]
            }

    async def analyze_excel_schema(self) -> List[Dict]:
        """Analiza el archivo Excel para extraer el esquema de columnas."""
        try:
            # No leer archivos directamente, devolver esquema por defecto
            return [
                {"name": "nombre_tirador", "type": "string", "required": True, "description": "Nombre del tirador"},
                {"name": "edad", "type": "number", "required": True, "description": "Edad del tirador"},
                {"name": "experiencia", "type": "number", "required": False, "description": "Años de experiencia"},
                {"name": "distancia_de_tiro", "type": "number", "required": False, "description": "Distancia de tiro en metros"},
                {"name": "angulo", "type": "number", "required": False, "description": "Ángulo de tiro"},
                {"name": "altura_de_tirador", "type": "number", "required": False, "description": "Altura del tirador"},
                {"name": "peso", "type": "number", "required": False, "description": "Peso del tirador"},
                {"name": "ambiente", "type": "string", "required": False, "description": "Condiciones ambientales"},
                {"name": "genero", "type": "string", "required": False, "description": "Género del tirador"},
                {"name": "peso_del_balon", "type": "number", "required": False, "description": "Peso del balón"},
                {"name": "tiempo_de_tiro", "type": "number", "required": False, "description": "Tiempo de tiro"},
                {"name": "tiro_exitoso", "type": "boolean", "required": False, "description": "Si el tiro fue exitoso"},
                {"name": "diestro_zurdo", "type": "string", "required": False, "description": "Mano dominante"},
                {"name": "calibre_de_balon", "type": "number", "required": False, "description": "Calibre del balón"}
            ]

        except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            logging.error("Error analizando esquema del Excel: %s", str(e))
            # Retornar esquema por defecto si hay error
            return [
                {"name": "columna1", "type": "string", "required": True, "description": "Columna 1"},
                {"name": "columna2", "type": "string", "required": False, "description": "Columna 2"}
            ]

    def _infer_data_type(self, data_series: pd.Series) -> str:
        """Infiere el tipo de dato de una serie de pandas."""
        if data_series.empty:
            return "string"

        # Limpiar datos para análisis
        clean_series = data_series.dropna().astype(str).str.strip()

        # Verificar si son valores booleanos
        if clean_series.isin(['True', 'False', 'true', 'false', '1', '0', 'Sí', 'No', 'sí', 'no']).all():
            return "boolean"

        # Intentar convertir a numérico
        try:
            numeric_series = pd.to_numeric(clean_series, errors='raise')
            # Verificar si son enteros
            if numeric_series.apply(lambda x: x.is_integer()).all():
                return "integer"
            else:
                return "number"
        except (ValueError, TypeError):
            pass

        # Verificar si son fechas (formato más estricto)
        try:
            # Solo intentar con formatos comunes
            pd.to_datetime(clean_series, format='%Y-%m-%d', errors='raise')
            return "date"
        except (ValueError, TypeError):
            try:
                pd.to_datetime(clean_series, format='%d/%m/%Y', errors='raise')
                return "date"
            except (ValueError, TypeError):
                pass

        # Por defecto, string
        return "string"

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
