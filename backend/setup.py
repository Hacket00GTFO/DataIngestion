"""Setup script for the Data Ingestion backend."""
from setuptools import setup, find_packages

setup(
    name="data-ingestion-backend",
    version="1.0.0",
    description="Backend API for data ingestion and processing",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "python-multipart>=0.0.6",
        "openpyxl>=3.1.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pylint>=3.0.0",
            "pytest>=7.0.0",
            "black>=23.0.0",
        ]
    }
)
