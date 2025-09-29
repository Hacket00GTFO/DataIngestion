# Base de Datos SQL Server

Configuración y scripts para la base de datos del sistema de Data Ingestion.

## Estructura

```
database/
├── init/
│   └── 01_create_database.sql    # Scripts de inicialización
├── records/                      # Archivos de datos persistentes
└── README.md                     # Este archivo
```

## Configuración

### Parámetros de Conexión
- **Server**: `localhost,1433`
- **Username**: `sa`
- **Password**: `YourStrong@Passw0rd`
- **Database**: `DataIngestionDB`
- **Trust Server Certificate**: ✅ Marcado

### Iniciar Base de Datos
```bash
# Con Docker
docker-compose up sqlserver -d

# O todos los servicios
start.bat
```

## Estructura de la Base de Datos

### Tabla Principal: `data_records`
```sql
CREATE TABLE data_records (
    id INT IDENTITY(1,1) PRIMARY KEY,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2,
    data NVARCHAR(MAX),           -- Datos JSON
    source NVARCHAR(255),         -- Fuente de datos
    is_processed BIT DEFAULT 0,   -- Estado de procesamiento
    validation_errors NVARCHAR(MAX) -- Errores de validación
);
```

### Vista de Estadísticas: `vw_data_statistics`
```sql
CREATE VIEW vw_data_statistics AS
SELECT 
    COUNT(*) as total_records,
    SUM(CASE WHEN is_processed = 1 THEN 1 ELSE 0 END) as processed_records,
    SUM(CASE WHEN is_processed = 0 THEN 1 ELSE 0 END) as unprocessed_records,
    COUNT(DISTINCT source) as unique_sources,
    MIN(created_at) as first_record_date,
    MAX(created_at) as last_record_date
FROM data_records;
```

## Consultas Útiles

### Ver Estadísticas
```sql
SELECT * FROM vw_data_statistics;
```

### Ver Registros Recientes
```sql
SELECT TOP 10 
    id, created_at, source, is_processed
FROM data_records 
ORDER BY created_at DESC;
```

### Consultar Datos JSON
```sql
SELECT 
    id, created_at, source,
    JSON_VALUE(data, '$') as json_data
FROM data_records 
WHERE data IS NOT NULL;
```

## Comandos Docker

```bash
# Ver estado
docker-compose ps

# Ver logs
docker-compose logs sqlserver

# Detener servicios
docker-compose down

# Reiniciar SQL Server
docker-compose restart sqlserver
```

## Solución de Problemas

### Error de Conexión
1. Verificar que Docker esté ejecutándose
2. Verificar contenedor: `docker-compose ps`
3. Revisar logs: `docker-compose logs sqlserver`

### Error de Autenticación
1. Verificar contraseña: `YourStrong@Passw0rd`
2. Marcar "Trust Server Certificate" en Azure Data Studio
