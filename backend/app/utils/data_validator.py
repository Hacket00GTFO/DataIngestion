"""Data validation utilities for ensuring data quality."""
from typing import List
import pandas as pd
from app.models.data_models import DataValidationResult

class DataValidator:
    """Clase para validación de datos"""

    def __init__(self):
        self.required_columns = []  # Se definirían según el Excel
        self.data_types = {}  # Se definirían según el Excel

    def validate_dataframe(self, df: pd.DataFrame) -> DataValidationResult:
        """Valida un DataFrame completo."""
        errors = []
        warnings = []

        # Validar columnas requeridas
        missing_columns = self._check_required_columns(df)
        if missing_columns:
            errors.extend([f"Columna faltante: {col}" for col in missing_columns])

        # Validar tipos de datos
        type_errors = self._validate_data_types(df)
        errors.extend(type_errors)

        # Validar valores nulos
        null_warnings = self._check_null_values(df)
        warnings.extend(null_warnings)

        # Validar duplicados
        duplicate_warnings = self._check_duplicates(df)
        warnings.extend(duplicate_warnings)

        is_valid = len(errors) == 0

        return DataValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            validated_data=df.to_dict('records') if is_valid else None # type: ignore
        )

    def _check_required_columns(self, df: pd.DataFrame) -> List[str]:
        """Verifica columnas requeridas."""
        missing = []
        for col in self.required_columns:
            if col not in df.columns:
                missing.append(col)
        return missing

    def _validate_data_types(self, df: pd.DataFrame) -> List[str]:
        """Valida tipos de datos."""
        errors = []
        for col, expected_type in self.data_types.items():
            if col in df.columns:
                actual_type = str(df[col].dtype)
                if actual_type != expected_type:
                    errors.append(
                        f"Columna {col}: tipo esperado {expected_type}, actual {actual_type}"
                    )
        return errors

    def _check_null_values(self, df: pd.DataFrame) -> List[str]:
        """Verifica valores nulos."""
        warnings = []
        for col in df.columns:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                warnings.append(f"Columna {col}: {null_count} valores nulos")
        return warnings

    def _check_duplicates(self, df: pd.DataFrame) -> List[str]:
        """Verifica registros duplicados."""
        warnings = []
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            warnings.append(f"Se encontraron {duplicate_count} registros duplicados")
        return warnings
