@echo off
echo Iniciando Data Ingestion con Azure SQL Server...
echo.

REM Verificar si Docker está ejecutándose
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker no está ejecutándose. Por favor, inicia Docker Desktop.
    pause
    exit /b 1
)

echo Construyendo e iniciando contenedores...
docker-compose up --build -d

echo.
echo Esperando a que los servicios estén listos...
timeout /t 30 /nobreak >nul

echo.
echo Verificando estado de los contenedores...
docker-compose ps

echo.
echo ========================================
echo Servicios iniciados:
echo - Azure SQL Server: localhost:1433
echo - Backend API: http://localhost:8000
echo - Frontend: http://localhost:3000
echo - Azure Data Studio: Configurar conexión a localhost:1433
echo ========================================
echo.
echo Para detener los servicios, ejecuta: docker-compose down
echo Para ver logs: docker-compose logs -f
echo.
pause
