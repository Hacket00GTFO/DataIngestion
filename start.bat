@echo off
echo ====================================
echo   Data Ingestion - Database Only
echo ====================================
echo.

REM Verificar si Docker está ejecutándose
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker no está ejecutándose. Por favor inicia Docker Desktop.
    pause
    exit /b 1
)

echo [1/2] Deteniendo contenedores existentes...
docker-compose down 2>nul

echo [2/2] Iniciando base de datos...
docker-compose up -d

echo.
echo Esperando que SQL Server esté listo...
timeout /t 15 /nobreak >nul

echo.
echo ====================================
echo   Base de datos iniciada
echo ====================================
echo.
echo SQL Server disponible en: localhost:1433
echo Usuario: sa
echo Password: YourStrong@Passw0rd
echo.
echo Para iniciar backend: 
echo   cd backend
echo   pip install -r requirements.txt
echo   python -m uvicorn app.main:app --reload
echo.
echo Para iniciar frontend:
echo   cd frontend  
echo   npm install
echo   npm start
echo.
pause