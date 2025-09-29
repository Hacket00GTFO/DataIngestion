-- Crear base de datos si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'DataIngestionDB')
BEGIN
    CREATE DATABASE DataIngestionDB;
END
GO

-- Usar la base de datos
USE DataIngestionDB;
GO

-- Crear tabla de registros de datos
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='data_records' AND xtype='U')
BEGIN
    CREATE TABLE data_records (
        id INT IDENTITY(1,1) PRIMARY KEY,
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2,
        data NVARCHAR(MAX), -- JSON data
        source NVARCHAR(255),
        is_processed BIT DEFAULT 0,
        validation_errors NVARCHAR(MAX)
    );
END
GO

-- Crear índices para mejorar el rendimiento
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_data_records_source')
BEGIN
    CREATE INDEX IX_data_records_source ON data_records(source);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_data_records_created_at')
BEGIN
    CREATE INDEX IX_data_records_created_at ON data_records(created_at);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_data_records_is_processed')
BEGIN
    CREATE INDEX IX_data_records_is_processed ON data_records(is_processed);
END
GO

-- Crear vista para estadísticas
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_data_statistics')
BEGIN
    EXEC('CREATE VIEW vw_data_statistics AS
    SELECT 
        COUNT(*) as total_records,
        SUM(CASE WHEN is_processed = 1 THEN 1 ELSE 0 END) as processed_records,
        SUM(CASE WHEN is_processed = 0 THEN 1 ELSE 0 END) as unprocessed_records,
        COUNT(DISTINCT source) as unique_sources,
        MIN(created_at) as first_record_date,
        MAX(created_at) as last_record_date
    FROM data_records');
END
GO

PRINT 'Base de datos DataIngestionDB inicializada correctamente';
