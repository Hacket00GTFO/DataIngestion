@echo off
echo ====================================
echo   Iniciando Frontend - Data Ingestion
echo ====================================
echo.

cd frontend

echo Verificando dependencias...
if not exist node_modules (
    echo Instalando dependencias de Node.js...
    npm install
)

echo.
echo Iniciando servidor frontend en http://localhost:3000
echo.

npm start
