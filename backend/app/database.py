"""Database configuration and connection management."""
import logging
import os
import time

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configuración de la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pyodbc://sa:YourStrong%40Passw0rd@localhost:1433/DataIngestionDB?"
    "driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no"
)

# Crear engine de SQLAlchemy con configuración optimizada
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    connect_args={
        "timeout": 60,  # Aumentar timeout de conexión
        "login_timeout": 60,  # Timeout específico para login
    },
    echo=False,  # Cambiar a True para ver las consultas SQL
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=300,  # Reciclar conexiones cada 5 minutos
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Metadata para crear tablas
metadata = MetaData()

def get_db():
    """Dependency para obtener sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Inicializar la base de datos creando las tablas."""
    try:
        # Importar todos los modelos aquí para que se registren
        from app.models.data_models import DataRecord  # noqa: F401

        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        logging.info("Base de datos inicializada correctamente")
    except Exception as e:
        logging.error("Error inicializando base de datos: %s", str(e))
        raise

# Variable global para caché de estado de conexión
_connection_status = {"available": None, "last_check": 0}

def test_connection(force_check: bool = False):
    """Probar la conexión a la base de datos con caché para evitar reintentos innecesarios."""
    current_time = time.time()
    # Caché de estado de conexión por 30 segundos para evitar checks repetitivos
    if not force_check and _connection_status["available"] is not None:
        if current_time - _connection_status["last_check"] < 30:
            return _connection_status["available"]

    max_retries = 3  # Reducir reintentos para operaciones frecuentes
    retry_delay = 2  # Reducir delay entre reintentos

    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                logging.info("Conexión a base de datos exitosa")
                _connection_status["available"] = True
                _connection_status["last_check"] = current_time
                return True
        except Exception as e:
            logging.warning("Intento %d/%d falló: %s", attempt + 1, max_retries, str(e))
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                error_msg = (f"Error conectando a base de datos después de "
                           f"{max_retries} intentos: {str(e)}")
                logging.error(error_msg)
                _connection_status["available"] = False
                _connection_status["last_check"] = current_time
                return False
