"""Data processing utilities for cleaning and transforming data."""
from typing import Dict, Any
import pandas as pd
import numpy as np

class DataProcessor:
    """Clase para procesamiento y limpieza de datos"""

    def __init__(self):
        self.cleaning_rules = {
            'remove_duplicates': True,
            'handle_nulls': True,
            'normalize_text': True,
            'validate_ranges': True
        }

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpia y procesa los datos."""
        cleaned_df = df.copy()

        # Eliminar duplicados
        if self.cleaning_rules['remove_duplicates']:
            cleaned_df = self._remove_duplicates(cleaned_df)

        # Manejar valores nulos
        if self.cleaning_rules['handle_nulls']:
            cleaned_df = self._handle_nulls(cleaned_df)

        # Normalizar texto
        if self.cleaning_rules['normalize_text']:
            cleaned_df = self._normalize_text(cleaned_df)

        # Validar rangos
        if self.cleaning_rules['validate_ranges']:
            cleaned_df = self._validate_ranges(cleaned_df)

        return cleaned_df

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Elimina registros duplicados."""
        return df.drop_duplicates()

    def _handle_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Maneja valores nulos."""
        # Para columnas numéricas, reemplazar con la mediana
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col] = df[col].fillna(df[col].median())

        # Para columnas de texto, reemplazar con 'N/A'
        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            df[col] = df[col].fillna('N/A')

        return df

    def _normalize_text(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza texto en las columnas."""
        text_columns = df.select_dtypes(include=['object']).columns
        for col in text_columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
        return df

    def _validate_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """Valida rangos de valores numéricos."""
        # Aquí se implementarían reglas específicas según el dominio
        # Por ejemplo, validar que las edades estén entre 0 y 120
        return df

    def transform_data(self, df: pd.DataFrame, transformations: Dict[str, Any]) -> pd.DataFrame:
        """Aplica transformaciones específicas a los datos."""
        transformed_df = df.copy()

        for transformation, params in transformations.items():
            if transformation == 'group_by':
                transformed_df = self._group_by(transformed_df, params)
            elif transformation == 'aggregate':
                transformed_df = self._aggregate(transformed_df, params)
            elif transformation == 'filter':
                transformed_df = self._filter_data(transformed_df, params)

        return transformed_df

    def _group_by(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Agrupa datos por columnas específicas."""
        group_columns = params.get('columns', [])
        agg_functions = params.get('aggregations', {})

        if group_columns and agg_functions:
            return df.groupby(group_columns).agg(agg_functions).reset_index()
        return df

    def _aggregate(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Aplica agregaciones a los datos."""
        # Implementar agregaciones específicas
        # params se usará en futuras implementaciones
        _ = params  # Evitar warning de parámetro no usado
        return df

    def _filter_data(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Filtra datos según criterios específicos."""
        conditions = params.get('conditions', {})

        for column, condition in conditions.items():
            if column in df.columns:
                if condition['operator'] == 'equals':
                    df = df[df[column] == condition['value']]
                elif condition['operator'] == 'greater_than':
                    df = df[df[column] > condition['value']]
                elif condition['operator'] == 'less_than':
                    df = df[df[column] < condition['value']]

        return df
