# Database - SQL Server Simplificado

Base de datos SQL Server en Docker para el sistema de ingesta manual de datos.

## Configuración Rápida

### Iniciar Base de Datos
```bash
# Windows
start.bat

# Manual
docker-compose up -d
```

### Credenciales
- **Host**: localhost:1433
- **Usuario**: sa
- **Password**: YourStrong@Passw0rd
- **BD**: DataIngestionDB

## Estructura de Datos

### Tabla Principal: data_records
```sql
CREATE TABLE data_records (
    id INT IDENTITY(1,1) PRIMARY KEY,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2,
    data NVARCHAR(MAX), -- JSON con los datos
    source NVARCHAR(255) DEFAULT 'manual_input',
    is_processed BIT DEFAULT 1,
    validation_errors NVARCHAR(MAX)
);
```

### Ejemplo de Datos JSON
```json
{
    "nombre": "Juan Perez",
    "edad": 25,
    "genero": "Masculino", 
    "experiencia_anos": 3,
    "distancia_metros": 50.0,
    "ambiente": "Exterior",
    "tiros_exitosos": 8,
    "tiros_totales": 10,
    "tiempo_sesion_minutos": 30.0,
    "precision_porcentaje": 80.0,
    "created_at": "2025-09-29T12:00:00"
}
```

## Scripts de Inicialización

### Crear Base de Datos
```sql
-- database/init/01_create_database.sql
CREATE DATABASE DataIngestionDB;
GO

USE DataIngestionDB;
GO

CREATE TABLE data_records (
    id INT IDENTITY(1,1) PRIMARY KEY,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2,
    data NVARCHAR(MAX),
    source NVARCHAR(255) DEFAULT 'manual_input',
    is_processed BIT DEFAULT 1,
    validation_errors NVARCHAR(MAX)
);
GO
```

## Acceso a la Base de Datos

### Azure Data Studio (Recomendado)
1. Descargar: https://docs.microsoft.com/en-us/sql/azure-data-studio/
2. Conectar: localhost:1433, usuario: sa

### Línea de Comandos
```bash
# Conectar desde Docker
docker exec -it data-ingestion-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P YourStrong@Passw0rd -C

# Ejecutar consulta
1> SELECT TOP 5 * FROM DataIngestionDB.dbo.data_records;
2> GO
```

### Navegador Web (Opcional)
```bash
# Instalar Adminer (interfaz web)
docker run --link data-ingestion-sqlserver:db -p 8080:8080 adminer
# Ir a: http://localhost:8080
# Sistema: MS SQL, Servidor: db:1433
```

## Consultas Útiles

### Ver Todos los Registros
```sql
USE DataIngestionDB;
SELECT 
    id,
    JSON_VALUE(data, '$.nombre') as nombre,
    JSON_VALUE(data, '$.edad') as edad,
    JSON_VALUE(data, '$.genero') as genero,
    JSON_VALUE(data, '$.precision_porcentaje') as precision,
    created_at
FROM data_records
ORDER BY created_at DESC;
```

### Estadísticas por Género
```sql
SELECT 
    JSON_VALUE(data, '$.genero') as genero,
    COUNT(*) as total,
    AVG(CAST(JSON_VALUE(data, '$.edad') AS INT)) as edad_promedio,
    AVG(CAST(JSON_VALUE(data, '$.precision_porcentaje') AS FLOAT)) as precision_promedio
FROM data_records
WHERE JSON_VALUE(data, '$.genero') IS NOT NULL
GROUP BY JSON_VALUE(data, '$.genero');
```

### Registros por Ambiente
```sql
SELECT 
    JSON_VALUE(data, '$.ambiente') as ambiente,
    COUNT(*) as total_registros
FROM data_records
WHERE JSON_VALUE(data, '$.ambiente') IS NOT NULL
GROUP BY JSON_VALUE(data, '$.ambiente');
```

## Docker Configuration

### docker-compose.yml
```yaml
services:
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2022-latest
    container_name: data-ingestion-sqlserver
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=YourStrong@Passw0rd
      - MSSQL_PID=Developer
    ports:
      - "1433:1433"
    volumes:
      - sqlserver_data:/var/opt/mssql
      - ./database/init:/docker-entrypoint-initdb.d
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P YourStrong@Passw0rd -Q 'SELECT 1' -C || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
```

## Comandos Útiles

### Gestión de Contenedor
```bash
# Iniciar
docker-compose up -d

# Ver estado
docker-compose ps

# Ver logs
docker logs data-ingestion-sqlserver

# Detener
docker-compose down

# Limpiar datos (¡cuidado!)
docker-compose down -v
```

### Backup de Datos
```bash
# Exportar datos
docker exec data-ingestion-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P YourStrong@Passw0rd -Q "SELECT * FROM DataIngestionDB.dbo.data_records FOR JSON AUTO" -o backup.json -C

# Backup de BD completa
docker exec data-ingestion-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P YourStrong@Passw0rd -Q "BACKUP DATABASE DataIngestionDB TO DISK = '/var/opt/mssql/backup/DataIngestionDB.bak'" -C
```

## Solución de Problemas

### Container no inicia
```bash
# Ver logs de error
docker logs data-ingestion-sqlserver

# Verificar puerto
netstat -an | findstr 1433

# Limpiar y reiniciar
docker-compose down -v
docker-compose up -d
```

### Error de conexión desde backend
```bash
# Verificar red
docker network ls
docker inspect dataingestion_default

# Probar conexión
docker exec data-ingestion-sqlserver ping localhost
```

### Recuperar contraseña
```bash
# La contraseña está en docker-compose.yml
# SA_PASSWORD=YourStrong@Passw0rd
```

## Opcional: Sin Docker

### SQL Server Local (Windows)
1. Instalar SQL Server Developer Edition
2. Crear base de datos: `DataIngestionDB`
3. Ejecutar script: `database/init/01_create_database.sql`
4. Cambiar connection string en backend

### SQLite (Alternativa ligera)
```python
# En backend/app/database.py cambiar:
DATABASE_URL = "sqlite:///./data_ingestion.db"
```

## Estado del Sistema

### Health Check
```bash
# Verificar que SQL Server responde
curl http://localhost:8000/api/v1/health
```

### Verificar Datos
```bash
# Ver registros desde API
curl http://localhost:8000/api/v1/data
```

Esta configuración está optimizada para desarrollo local y demostraciones.