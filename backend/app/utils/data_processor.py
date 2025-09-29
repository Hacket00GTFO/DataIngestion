"""Utilities to parse and normalize shooter metrics coming from CSV uploads."""
from __future__ import annotations

import re
from typing import Tuple

_NUMERIC_PATTERN = re.compile(r"-?\d+(?:[\.,]\d+)?")

_GENERO_MAP = {
    "masculino": "Masculino",
    "femenino": "Femenino",
    "otro": "Otro",
}

_MANO_MAP = {
    "diestro": "Diestro",
    "zurdo": "Zurdo",
    "ambidiestro": "Ambidiestro",
}


def _extract_numeric(value: str) -> str:
    """Return the first numeric fragment found in the input string."""
    if value is None:
        raise ValueError("valor vacio")

    match = _NUMERIC_PATTERN.search(str(value))
    if not match:
        raise ValueError(f"no se encontro numero en '{value}'")
    return match.group(0).replace(",", ".")


def parse_anios(value: str) -> int:
    """Parse strings like '4 años' into an integer."""
    number = int(float(_extract_numeric(value)))
    if number < 0:
        raise ValueError("experiencia negativa")
    return number


def parse_metros(value: str) -> float:
    """Parse strings like '5 metros' into meters as float."""
    number = float(_extract_numeric(value))
    if number <= 0:
        raise ValueError("distancia invalida")
    return round(number, 2)


def parse_grados(value: str) -> int:
    """Parse strings like '90 grados' into degrees as integer."""
    number = int(float(_extract_numeric(value)))
    if not 0 <= number <= 360:
        raise ValueError("angulo fuera de rango")
    return number


def parse_peso_kg(value: str) -> float:
    """Parse strings like '95 kg' or '50kg' into kilograms as float."""
    number = float(_extract_numeric(value))
    if number <= 0:
        raise ValueError("peso tirador invalido")
    return round(number, 2)


def parse_peso_g(value: str) -> int:
    """Parse strings like '500 g' into grams as integer."""
    number = int(float(_extract_numeric(value)))
    if number <= 0:
        raise ValueError("peso balon invalido")
    return number


def parse_segundos(value: str) -> float:
    """Parse strings like '1 segundo' or '2 segundos' into seconds as float."""
    number = float(_extract_numeric(value))
    if number <= 0:
        raise ValueError("tiempo de tiro invalido")
    return round(number, 3)


def parse_exitos_intentos(value: str) -> Tuple[int, int]:
    """Parse expressions like '2 de 6' into (exitos, intentos)."""
    if value is None:
        raise ValueError("valor vacio")

    parts = re.split(r"\s*de\s*", str(value), flags=re.IGNORECASE)
    if len(parts) != 2:
        raise ValueError(f"formato invalido para exitos/intentos: '{value}'")

    exitos = int(parts[0].strip())
    intentos = int(_extract_numeric(parts[1]))

    if exitos < 0:
        raise ValueError("exitos negativos")
    if intentos <= 0 or intentos > 100:
        raise ValueError("intentos fuera de rango")
    if exitos > intentos:
        raise ValueError("exitos no pueden superar intentos")
    return exitos, intentos


def normalize_genero(value: str) -> str:
    """Normalize gender values to the genero_enum choices."""
    if not value:
        return "Otro"
    key = str(value).strip().lower()
    return _GENERO_MAP.get(key, "Otro")


def normalize_mano_habil(value: str) -> str:
    """Normalize handedness to mano_habil_enum choices."""
    if not value:
        return "Ambidiestro"
    key = str(value).strip().lower()
    return _MANO_MAP.get(key, "Ambidiestro")
