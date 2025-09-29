"""Data service providing ETL helpers for tiros records."""
from __future__ import annotations

import logging
import unicodedata
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.exc import SQLAlchemyError

from app.db import engine, session_scope
from app.models.tiro import Tiro
from app.utils.data_processor import (
    normalize_genero,
    normalize_mano_habil,
    parse_anios,
    parse_exitos_intentos,
    parse_grados,
    parse_metros,
    parse_peso_g,
    parse_peso_kg,
    parse_segundos,
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

STAGING_COLUMNS = [
    "nombre_tirador",
    "edad",
    "experiencia",
    "distancia_de_tiro",
    "angulo",
    "altura_de_tirador",
    "peso",
    "ambiente",
    "genero",
    "peso_del_balon",
    "tiempo_de_tiro",
    "tiro_exitoso",
    "diestro_zurdo",
    "calibre_de_balon",
]


metadata = sa.MetaData(schema="public")
TIROS_STAGING = sa.Table(
    "tiros_staging",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True),
    *(sa.Column(column, TEXT) for column in STAGING_COLUMNS),
)

COLUMN_ALIASES = {
    "nombre tirador": "nombre_tirador",
    "nombre_tirador": "nombre_tirador",
    "edad": "edad",
    "experiencia": "experiencia",
    "experiencia laboral": "experiencia",
    "distancia de tiro": "distancia_de_tiro",
    "distancia_de_tiro": "distancia_de_tiro",
    "angulo": "angulo",
    "ángulo": "angulo",
    "altura de tirador": "altura_de_tirador",
    "altura_de_tirador": "altura_de_tirador",
    "peso": "peso",
    "ambiente": "ambiente",
    "genero": "genero",
    "género": "genero",
    "peso del balon": "peso_del_balon",
    "peso_del_balon": "peso_del_balon",
    "tiempo de tiro": "tiempo_de_tiro",
    "tiempo_de_tiro": "tiempo_de_tiro",
    "tiro exitoso?": "tiro_exitoso",
    "tiro exitoso": "tiro_exitoso",
    "diestro / zurdo": "diestro_zurdo",
    "diestro/zurdo": "diestro_zurdo",
    "diestro_zurdo": "diestro_zurdo",
    "calibre de balon": "calibre_de_balon",
    "calibre_de_balon": "calibre_de_balon",
}


class DataService:
    """Service encapsulating persistence and transformation logic."""

    def __init__(self) -> None:
        self.engine = engine

    # -----------------------------
    # Staging loading
    # -----------------------------
    def load_csv_to_staging(self, file_path: str) -> int:
        """Load a CSV file into the staging table.

        Returns the number of rows ingested.
        """
        csv_path = Path(file_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")

        read_kwargs = {"dtype": str, "keep_default_na": False, "engine": "python", "sep": None}
        encodings = ["utf-8", "latin-1", "cp1252"]
        df = None
        last_error: Exception | None = None
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_path, encoding=encoding, **read_kwargs)
                if encoding != "utf-8":
                    LOGGER.info("Loaded CSV %s using fallback encoding %s", csv_path, encoding)
                break
            except UnicodeDecodeError as exc:
                last_error = exc
                continue

        if df is None:
            raise UnicodeDecodeError(
                "csv", b"", 0, 0, f"No se pudo decodificar el archivo {csv_path}: {last_error}"
            )
        if df.empty:
            LOGGER.info("No rows found in %s", csv_path)
            return 0

        LOGGER.info("Column headers before cleaning: %s", df.columns.tolist())
        df.rename(columns=self._clean_column_header, inplace=True)
        LOGGER.info("Column headers after cleaning: %s", df.columns.tolist())
        df = self._rename_columns(df)
        LOGGER.info("Column headers after alias mapping: %s", df.columns.tolist())
        strip_cell = lambda value: value.strip() if isinstance(value, str) else value
        if hasattr(df, "map"):
            df = df.map(strip_cell)
        else:
            df = df.applymap(strip_cell)
        df = df.replace({"": None})

        missing = [col for col in STAGING_COLUMNS if col not in df.columns]
        if missing:
            for column in missing:
                df[column] = None
            LOGGER.warning("CSV missing expected columns: %s", ", ".join(missing))

        df = df[STAGING_COLUMNS]

        try:
            df.to_sql(
                "tiros_staging",
                con=self.engine,
                schema="public",
                if_exists="append",
                index=False,
                method="multi",
            )
        except SQLAlchemyError as exc:
            LOGGER.error("Error loading CSV into staging: %s", exc)
            raise

        return len(df)

    # -----------------------------
    # Transformation
    # -----------------------------
    def transform_staging_to_final(self) -> Dict[str, Any]:
        """Transform staging rows into the final table.

        Returns a dictionary with counts and details about invalid rows.
        """
        with session_scope() as session:
            rows = session.execute(sa.select(TIROS_STAGING)).mappings().all()

        total_rows = len(rows)
        valid_payload: List[Dict[str, Any]] = []
        invalid_rows: List[Dict[str, Any]] = []

        for raw in rows:
            try:
                valid_payload.append(self._transform_row(raw))
            except Exception as exc:  # pylint: disable=broad-except
                invalid_info = {
                    "staging_id": raw.get("id"),
                    "error": str(exc),
                    "row": {key: raw.get(key) for key in STAGING_COLUMNS},
                }
                invalid_rows.append(invalid_info)
                LOGGER.warning("Skipping staging row %s due to error: %s", raw.get("id"), exc)

        inserted = 0
        if valid_payload:
            with session_scope() as session:
                session.execute(sa.insert(Tiro.__table__), valid_payload)
                inserted = len(valid_payload)

        return {
            "read": total_rows,
            "inserted": inserted,
            "invalid": len(invalid_rows),
            "invalid_rows": invalid_rows,
        }

    def clear_staging(self) -> None:
        """Remove all rows from staging."""
        with session_scope() as session:
            session.execute(sa.text("TRUNCATE TABLE public.tiros_staging RESTART IDENTITY"))

    def get_statistics(self) -> Dict[str, Any]:
        """Aggregate metrics from the tiros table."""
        with session_scope() as session:
            total = session.execute(sa.select(sa.func.count(Tiro.id))).scalar_one()
            avg_distance = session.execute(sa.select(sa.func.avg(Tiro.__table__.c.distancia_m))).scalar()
            avg_angle = session.execute(sa.select(sa.func.avg(Tiro.__table__.c.angulo_grados))).scalar()
            sum_exitos, sum_intentos = session.execute(
                sa.select(
                    sa.func.coalesce(sa.func.sum(Tiro.__table__.c.exitos), 0),
                    sa.func.coalesce(sa.func.sum(Tiro.__table__.c.intentos), 0),
                )
            ).one()

            genero_distribution = self._group_count(session, Tiro.__table__.c.genero, default_label="Desconocido")
            mano_distribution = self._group_count(session, Tiro.__table__.c.mano_habil, default_label="Ambidiestro")
            calibre_distribution = self._group_count(session, Tiro.__table__.c.calibre_balon, default_label="Sin dato")

        success_rate = float(sum_exitos) / float(sum_intentos) if sum_intentos else 0.0

        return {
            "total_rows": total,
            "avg_distancia_m": float(avg_distance) if avg_distance is not None else None,
            "avg_angulo_grados": float(avg_angle) if avg_angle is not None else None,
            "success_rate": success_rate,
            "distribution": {
                "genero": genero_distribution,
                "mano_habil": mano_distribution,
                "calibre_balon": calibre_distribution,
            },
        }

    def get_schema(self) -> List[Dict[str, Any]]:
        """Describe the tiros table columns."""
        columns = []
        for column in Tiro.__table__.columns:
            columns.append(
                {
                    "name": column.name,
                    "type": str(column.type),
                    "nullable": column.nullable,
                }
            )
        return columns

    # -----------------------------
    # Helpers
    # -----------------------------
    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        renamed = {}
        for column in df.columns:
            normalized = self._normalize_column_name(column)
            target = COLUMN_ALIASES.get(normalized)
            if target:
                renamed[column] = target
        return df.rename(columns=renamed)

    @staticmethod
    def _normalize_column_name(column: str) -> str:
        column = column.replace("\ufeff", "").strip()
        decomposed = unicodedata.normalize("NFKD", column)
        ascii_only = "".join(char for char in decomposed if not unicodedata.combining(char))
        return ascii_only.lower().strip()

    @staticmethod
    def _clean_column_header(column: str) -> str:
        if not isinstance(column, str):
            return column
        return column.replace("\ufeff", "").strip()

    def _transform_row(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        nombre = (raw.get("nombre_tirador") or "").strip()
        if not nombre:
            raise ValueError("nombre_tirador requerido")

        edad = self._parse_int(raw.get("edad"), "edad")
        experiencia = parse_anios(raw.get("experiencia", "0"))
        distancia = Decimal(str(parse_metros(raw.get("distancia_de_tiro")))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        angulo = parse_grados(raw.get("angulo"))
        altura = self._parse_decimal(raw.get("altura_de_tirador"), "altura_tirador_m", "0.01")
        peso_tirador = Decimal(str(parse_peso_kg(raw.get("peso")))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        ambiente = self._safe_strip(raw.get("ambiente"))
        genero = normalize_genero(raw.get("genero"))
        peso_balon = parse_peso_g(raw.get("peso_del_balon"))
        tiempo_tiro = Decimal(str(parse_segundos(raw.get("tiempo_de_tiro")))).quantize(
            Decimal("0.001"), rounding=ROUND_HALF_UP
        )
        exitos, intentos = parse_exitos_intentos(raw.get("tiro_exitoso"))
        mano_habil = normalize_mano_habil(raw.get("diestro_zurdo"))
        calibre = self._parse_optional_int(raw.get("calibre_de_balon"))

        return {
            "nombre_tirador": nombre,
            "edad": edad,
            "experiencia_anios": experiencia,
            "distancia_m": distancia,
            "angulo_grados": angulo,
            "altura_tirador_m": altura,
            "peso_tirador_kg": peso_tirador,
            "ambiente": ambiente or None,
            "genero": genero,
            "peso_balon_g": peso_balon,
            "tiempo_tiro_s": tiempo_tiro,
            "exitos": exitos,
            "intentos": intentos,
            "mano_habil": mano_habil,
            "calibre_balon": calibre,
        }

    @staticmethod
    def _safe_strip(value: Any) -> str:
        return value.strip() if isinstance(value, str) and value.strip() else None

    @staticmethod
    def _parse_int(value: Any, field: str) -> int:
        if value is None or str(value).strip() == "":
            raise ValueError(f"{field} requerido")
        try:
            return int(float(str(value).strip()))
        except ValueError as exc:
            raise ValueError(f"{field} invalido: {value}") from exc

    @staticmethod
    def _parse_optional_int(value: Any) -> Any:
        if value is None or str(value).strip() == "":
            return None
        try:
            return int(float(str(value).strip()))
        except ValueError as exc:
            raise ValueError(f"calibre_balon invalido: {value}") from exc

    @staticmethod
    def _parse_decimal(value: Any, field: str, quantize: str) -> Decimal:
        if value is None or str(value).strip() == "":
            raise ValueError(f"{field} requerido")
        try:
            decimal_value = Decimal(str(value).replace(",", "."))
        except Exception as exc:  # pylint: disable=broad-except
            raise ValueError(f"{field} invalido: {value}") from exc
        return decimal_value.quantize(Decimal(quantize), rounding=ROUND_HALF_UP)

    def _group_count(self, session, column: Any, default_label: str) -> Dict[str, int]:
        rows = session.execute(
            sa.select(column, sa.func.count()).group_by(column).order_by(column)
        ).all()
        distribution: Dict[str, int] = {}
        for value, count in rows:
            key = str(value) if value is not None else default_label
            distribution[key] = count
        return distribution
