"""Database configuration and connection management."""
import logging
import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configuración de la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pyodbc://@localhost/DataIngestionDB?"
    "driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes"
)

# Crear engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    connect_args={
        "timeout": 30,
    },
    echo=False,  # Cambiar a True para ver las consultas SQL
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=300  # Reciclar conexiones cada 5 minutos
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

def test_connection():
    """Probar la conexión a la base de datos."""
    import time
    from sqlalchemy import text
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                logging.info("Conexión a base de datos exitosa")
                return True
        except Exception as e:
            logging.warning("Intento %d/%d falló: %s", attempt + 1, max_retries, str(e))
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logging.error("Error conectando a base de datos después de %d intentos: %s", max_retries, str(e))
                return False
