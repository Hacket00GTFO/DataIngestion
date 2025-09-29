"""Main data service for processing and managing data operations."""
import logging
import os
from typing import Dict, List, Optional
import pandas as pd
from app.models.data_models import DataStatistics
from app.utils.data_validator import DataValidator
from app.utils.data_processor import DataProcessor

class DataService:
    """Servicio principal para el procesamiento de datos"""

    def __init__(self):
        self.validator = DataValidator()
        self.processor = DataProcessor()
        self.excel_file_path = "../evidencia big data.xlsx"
        self._cached_data = None

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

    async def load_excel_data(self) -> Optional[pd.DataFrame]:
        """Carga los datos del archivo Excel de evidencia."""
        try:
            if self._cached_data is not None:
                return self._cached_data
                
            if not os.path.exists(self.excel_file_path):
                logging.warning("Archivo Excel no encontrado: %s", self.excel_file_path)
                return None
                
            # Leer el archivo Excel
            df = pd.read_excel(self.excel_file_path, sheet_name='Hoja1', header=0)
            
            # Los nombres de columnas están en la primera fila
            column_names = df.iloc[0].tolist()
            
            # Remover la fila de encabezados y usar los nombres reales
            df_clean = df.iloc[1:].copy()
            df_clean.columns = column_names
            
            # Limpiar datos (remover filas completamente vacías)
            df_clean = df_clean.dropna(how='all')
            
            # Cachear los datos
            self._cached_data = df_clean
            return df_clean
            
        except Exception as e:
            logging.error("Error cargando datos del Excel: %s", str(e))
            return None

    async def get_excel_data(self) -> Dict:
        """Obtiene todos los datos del archivo Excel."""
        try:
            df = await self.load_excel_data()
            if df is None:
                return {
                    "success": False,
                    "message": "No se pudieron cargar los datos del Excel",
                    "data": [],
                    "total": 0
                }
            
            # Convertir a formato JSON
            data_records = []
            for _, row in df.iterrows():
                record = {}
                for col in df.columns:
                    value = row[col]
                    # Convertir NaN a None para JSON
                    if pd.isna(value):
                        value = None
                    record[col] = value
                data_records.append(record)
            
            return {
                "success": True,
                "message": "Datos cargados exitosamente",
                "data": data_records,
                "total": len(data_records),
                "columns": list(df.columns)
            }
            
        except Exception as e:
            logging.error("Error obteniendo datos del Excel: %s", str(e))
            return {
                "success": False,
                "message": f"Error obteniendo datos: {str(e)}",
                "data": [],
                "total": 0
            }

    async def get_excel_schema(self) -> Dict:
        """Obtiene el esquema de datos del archivo Excel."""
        try:
            df = await self.load_excel_data()
            if df is None:
                return {
                    "success": False,
                    "message": "No se pudieron cargar los datos del Excel",
                    "columns": []
                }
            
            # Analizar tipos de datos y valores únicos
            schema = []
            for col in df.columns:
                col_data = df[col].dropna()
                unique_values = col_data.unique()[:10]  # Primeros 10 valores únicos
                
                schema.append({
                    "name": col,
                    "type": str(df[col].dtype),
                    "required": False,  # Por ahora asumimos que no son requeridos
                    "unique_values": [str(val) for val in unique_values],
                    "null_count": df[col].isna().sum(),
                    "total_count": len(df[col])
                })
            
            return {
                "success": True,
                "message": "Esquema obtenido exitosamente",
                "columns": schema
            }
            
        except Exception as e:
            logging.error("Error obteniendo esquema del Excel: %s", str(e))
            return {
                "success": False,
                "message": f"Error obteniendo esquema: {str(e)}",
                "columns": []
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
