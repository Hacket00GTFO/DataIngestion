"""SQLAlchemy model for the tiros table."""
from sqlalchemy import BigInteger, Column, Integer, Numeric, SmallInteger, String
from sqlalchemy.dialects.postgresql import ENUM

from app.db import Base

GeneroEnum = ENUM(
    "Masculino",
    "Femenino",
    "Otro",
    name="genero_enum",
    create_type=False,
)

ManoHabilEnum = ENUM(
    "Diestro",
    "Zurdo",
    "Ambidiestro",
    name="mano_habil_enum",
    create_type=False,
)


class Tiro(Base):
    """ORM mapping for tiros table."""

    __tablename__ = "tiros"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, index=False)
    nombre_tirador = Column(String(120), nullable=False)
    edad = Column(SmallInteger, nullable=False)
    experiencia_anios = Column(SmallInteger, nullable=False)
    distancia_m = Column(Numeric(6, 2), nullable=False)
    angulo_grados = Column(SmallInteger, nullable=False)
    altura_tirador_m = Column(Numeric(4, 2), nullable=False)
    peso_tirador_kg = Column(Numeric(6, 2), nullable=False)
    ambiente = Column(String(60), nullable=True)
    genero = Column(GeneroEnum, nullable=True)
    peso_balon_g = Column(Integer, nullable=False)
    tiempo_tiro_s = Column(Numeric(6, 3), nullable=False)
    exitos = Column(Integer, nullable=False)
    intentos = Column(Integer, nullable=False)
    mano_habil = Column(ManoHabilEnum, nullable=True)
    calibre_balon = Column(SmallInteger, nullable=True)
