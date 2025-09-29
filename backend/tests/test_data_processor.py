"""Unit tests for data parsing helpers."""
import pytest

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


def test_parse_peso_kg_variants():
    assert parse_peso_kg("50kg") == 50.0
    assert parse_peso_kg("95 kg") == 95.0


def test_parse_anios_allows_zero():
    assert parse_anios("0 años") == 0


def test_parse_exitos_intentos():
    assert parse_exitos_intentos("2 de 6") == (2, 6)


def test_parse_grados_is_case_insensitive():
    assert parse_grados("90 GRADOS") == 90


def test_parse_segundos_single_second():
    assert parse_segundos("1 segundo") == 1.0


def test_parse_metros_returns_float():
    assert parse_metros("5 metros") == 5.0


def test_parse_peso_g_to_int():
    assert parse_peso_g("500 g") == 500


def test_normalize_genero_defaults_to_otro():
    assert normalize_genero("Masculino") == "Masculino"
    assert normalize_genero("desconocido") == "Otro"


def test_normalize_mano_habil_defaults():
    assert normalize_mano_habil("Zurdo") == "Zurdo"
    assert normalize_mano_habil("") == "Ambidiestro"


def test_parse_exitos_intentos_invalid_order():
    with pytest.raises(ValueError):
        parse_exitos_intentos("7 de 6")
