-- Crear base de datos si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'DataIngestionDB')
BEGIN
    CREATE DATABASE DataIngestionDB;
END
GO

-- Usar la base de datos
USE DataIngestionDB;
GO

-- Crear tabla de tiradores
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tiradores' AND xtype='U')
BEGIN
    CREATE TABLE tiradores (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nombre NVARCHAR(100) NOT NULL,
        edad INT,
        experiencia_anos INT,
        altura DECIMAL(4,2), -- en metros
        peso DECIMAL(5,2), -- en kg
        genero NVARCHAR(20),
        mano_dominante NVARCHAR(20), -- Diestro/Zurdo
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2
    );
END
GO

-- Crear tabla de sesiones de tiro
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='sesiones_tiro' AND xtype='U')
BEGIN
    CREATE TABLE sesiones_tiro (
        id INT IDENTITY(1,1) PRIMARY KEY,
        tirador_id INT NOT NULL,
        distancia_metros DECIMAL(4,2),
        angulo_grados INT,
        ambiente NVARCHAR(50),
        peso_balon DECIMAL(6,2), -- en gramos
        calibre_balon INT,
        tiempo_tiro_segundos DECIMAL(4,2),
        tiros_exitosos INT,
        tiros_totales INT,
        fecha_sesion DATETIME2 DEFAULT GETDATE(),
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2,
        FOREIGN KEY (tirador_id) REFERENCES tiradores(id)
    );
END
GO

-- Crear tabla de registros de datos (mantener para compatibilidad)
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

-- Crear tabla específica para datos del Excel de tiro (todas las 14 columnas)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tiro_excel' AND xtype='U')
BEGIN
    CREATE TABLE tiro_excel (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nombre_tirador NVARCHAR(100),
        edad INT,
        experiencia INT, -- años de experiencia
        distancia_de_tiro DECIMAL(6,2), -- metros
        angulo INT, -- grados
        altura_de_tirador DECIMAL(4,2), -- metros
        peso DECIMAL(5,2), -- kg
        ambiente NVARCHAR(50),
        genero NVARCHAR(20),
        peso_del_balon DECIMAL(6,2), -- gramos
        tiempo_de_tiro DECIMAL(4,2), -- segundos
        tiro_exitoso BIT,
        diestro_zurdo NVARCHAR(20), -- Diestro/Zurdo
        calibre_de_balon INT,
        created_at DATETIME2 DEFAULT GETDATE(),
        updated_at DATETIME2
    );
END
GO

-- Crear índices para mejorar el rendimiento
-- Índices para tabla tiradores
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_tiradores_nombre')
BEGIN
    CREATE INDEX IX_tiradores_nombre ON tiradores(nombre);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_tiradores_genero')
BEGIN
    CREATE INDEX IX_tiradores_genero ON tiradores(genero);
END
GO

-- Índices para tabla sesiones_tiro
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_sesiones_tiro_tirador_id')
BEGIN
    CREATE INDEX IX_sesiones_tiro_tirador_id ON sesiones_tiro(tirador_id);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_sesiones_tiro_fecha')
BEGIN
    CREATE INDEX IX_sesiones_tiro_fecha ON sesiones_tiro(fecha_sesion);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_sesiones_tiro_ambiente')
BEGIN
    CREATE INDEX IX_sesiones_tiro_ambiente ON sesiones_tiro(ambiente);
END
GO

-- Índices para tabla data_records (mantener compatibilidad)
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

-- Índices para tabla tiro_excel
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_tiro_excel_nombre_tirador')
BEGIN
    CREATE INDEX IX_tiro_excel_nombre_tirador ON tiro_excel(nombre_tirador);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_tiro_excel_genero')
BEGIN
    CREATE INDEX IX_tiro_excel_genero ON tiro_excel(genero);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_tiro_excel_ambiente')
BEGIN
    CREATE INDEX IX_tiro_excel_ambiente ON tiro_excel(ambiente);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_tiro_excel_created_at')
BEGIN
    CREATE INDEX IX_tiro_excel_created_at ON tiro_excel(created_at);
END
GO

-- Crear vista para estadísticas de tiradores
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_tiradores_statistics')
BEGIN
    EXEC('CREATE VIEW vw_tiradores_statistics AS
    SELECT 
        COUNT(*) as total_tiradores,
        COUNT(DISTINCT genero) as generos_unicos,
        AVG(CAST(edad AS FLOAT)) as edad_promedio,
        AVG(CAST(experiencia_anos AS FLOAT)) as experiencia_promedio,
        AVG(CAST(altura AS FLOAT)) as altura_promedio,
        AVG(CAST(peso AS FLOAT)) as peso_promedio,
        MIN(created_at) as primer_registro,
        MAX(created_at) as ultimo_registro
    FROM tiradores');
END
GO

-- Crear vista para estadísticas de sesiones de tiro
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_sesiones_statistics')
BEGIN
    EXEC('CREATE VIEW vw_sesiones_statistics AS
    SELECT 
        COUNT(*) as total_sesiones,
        AVG(CAST(tiros_exitosos AS FLOAT) / CAST(tiros_totales AS FLOAT)) * 100 as precision_promedio,
        AVG(CAST(distancia_metros AS FLOAT)) as distancia_promedio,
        AVG(CAST(tiempo_tiro_segundos AS FLOAT)) as tiempo_promedio,
        COUNT(DISTINCT ambiente) as ambientes_unicos,
        MIN(fecha_sesion) as primera_sesion,
        MAX(fecha_sesion) as ultima_sesion
    FROM sesiones_tiro');
END
GO

-- Crear vista para estadísticas generales (mantener compatibilidad)
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

-- Crear vista combinada para análisis completo
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_analisis_completo')
BEGIN
    EXEC('CREATE VIEW vw_analisis_completo AS
    SELECT 
        t.nombre,
        t.edad,
        t.experiencia_anos,
        t.genero,
        t.altura,
        t.peso,
        t.mano_dominante,
        st.distancia_metros,
        st.angulo_grados,
        st.ambiente,
        st.peso_balon,
        st.calibre_balon,
        st.tiempo_tiro_segundos,
        st.tiros_exitosos,
        st.tiros_totales,
        CASE 
            WHEN st.tiros_totales > 0 
            THEN CAST(st.tiros_exitosos AS FLOAT) / CAST(st.tiros_totales AS FLOAT) * 100 
            ELSE 0 
        END as precision_porcentaje,
        st.fecha_sesion
    FROM tiradores t
    INNER JOIN sesiones_tiro st ON t.id = st.tirador_id');
END
GO

-- Crear vista para estadísticas de la tabla tiro_excel
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_tiro_excel_statistics')
BEGIN
    EXEC('CREATE VIEW vw_tiro_excel_statistics AS
    SELECT 
        COUNT(*) as total_records,
        SUM(CASE WHEN tiro_exitoso = 1 THEN 1 ELSE 0 END) as tiros_exitosos,
        CASE 
            WHEN COUNT(*) > 0 
            THEN CAST(SUM(CASE WHEN tiro_exitoso = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 
            ELSE 0 
        END as precision_general,
        COUNT(DISTINCT genero) as generos_unicos,
        COUNT(DISTINCT ambiente) as ambientes_unicos,
        AVG(CAST(edad AS FLOAT)) as edad_promedio,
        AVG(CAST(experiencia AS FLOAT)) as experiencia_promedio,
        AVG(CAST(distancia_de_tiro AS FLOAT)) as distancia_promedio,
        AVG(CAST(tiempo_de_tiro AS FLOAT)) as tiempo_promedio,
        MIN(created_at) as primer_registro,
        MAX(created_at) as ultimo_registro
    FROM tiro_excel');
END
GO

-- Crear vista para distribución por género
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_tiro_excel_genero_distribution')
BEGIN
    EXEC('CREATE VIEW vw_tiro_excel_genero_distribution AS
    SELECT 
        genero,
        COUNT(*) as count,
        AVG(CAST(edad AS FLOAT)) as edad_promedio,
        SUM(CASE WHEN tiro_exitoso = 1 THEN 1 ELSE 0 END) as tiros_exitosos,
        CASE 
            WHEN COUNT(*) > 0 
            THEN CAST(SUM(CASE WHEN tiro_exitoso = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 
            ELSE 0 
        END as precision_porcentaje
    FROM tiro_excel
    WHERE genero IS NOT NULL
    GROUP BY genero');
END
GO

-- Crear vista para distribución por ambiente
IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'vw_tiro_excel_ambiente_distribution')
BEGIN
    EXEC('CREATE VIEW vw_tiro_excel_ambiente_distribution AS
    SELECT 
        ambiente,
        COUNT(*) as count,
        AVG(CAST(distancia_de_tiro AS FLOAT)) as distancia_promedio,
        AVG(CAST(tiempo_de_tiro AS FLOAT)) as tiempo_promedio,
        SUM(CASE WHEN tiro_exitoso = 1 THEN 1 ELSE 0 END) as tiros_exitosos,
        CASE 
            WHEN COUNT(*) > 0 
            THEN CAST(SUM(CASE WHEN tiro_exitoso = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 
            ELSE 0 
        END as precision_porcentaje
    FROM tiro_excel
    WHERE ambiente IS NOT NULL
    GROUP BY ambiente');
END
GO

PRINT 'Base de datos DataIngestionDB inicializada correctamente';

-- Migrar datos del Excel automáticamente
PRINT 'Iniciando migración de datos del Excel...';

-- Insertar datos de tiradores únicos (valores numéricos limpios)
INSERT INTO tiradores (nombre, edad, experiencia_anos, altura, peso, genero, mano_dominante)
SELECT DISTINCT
    TRIM(nombre_tirador) as nombre,
    CAST(edad AS INT) as edad,
    CAST(experiencia AS INT) as experiencia_anos,
    CAST(altura_tirador AS DECIMAL(4,2)) as altura,
    CAST(peso AS DECIMAL(5,2)) as peso,
    genero,
    CASE 
        WHEN LOWER(TRIM(diestro_zurdo)) LIKE '%diestro%' THEN 'Diestro'
        WHEN LOWER(TRIM(diestro_zurdo)) LIKE '%zurdo%' THEN 'Zurdo'
        ELSE TRIM(diestro_zurdo)
    END as mano_dominante
FROM (
    VALUES 
    ('Norberto', 24, 4, 1.70, 95.0, 'Masculino', 'Diestro'),
    ('Jaob', 19, 0, 1.70, 86.0, 'Masculino', 'Diestro'),
    ('Hilary', 19, 0, 1.55, 50.0, 'Femenino', 'Diestro'),
    ('Orlando', 26, 0, 1.67, 69.0, 'Masculino', 'Diestro'),
    ('Josué', 24, 0, 1.70, 50.0, 'Masculino', 'Diestro'),
    ('Valentino', 24, 10, 1.85, 88.0, 'Masculino', 'Diestro'),
    ('Diego', 22, 4, 1.68, 58.0, 'Masculino', 'Diestro'),
    ('David', 20, 0, 1.70, 71.0, 'Masculino', 'Diestro')
) AS datos_excel(nombre_tirador, edad, experiencia, altura_tirador, peso, genero, diestro_zurdo)
WHERE NOT EXISTS (
    SELECT 1 FROM tiradores t 
    WHERE t.nombre = TRIM(datos_excel.nombre_tirador)
);

-- Insertar sesiones de tiro (valores numéricos limpios)
INSERT INTO sesiones_tiro (
    tirador_id, 
    distancia_metros, 
    angulo_grados, 
    ambiente, 
    peso_balon, 
    calibre_balon, 
    tiempo_tiro_segundos, 
    tiros_exitosos, 
    tiros_totales
)
SELECT 
    t.id as tirador_id,
    distancia_metros,
    angulo_grados,
    ambiente,
    peso_balon,
    calibre_balon,
    tiempo_tiro_segundos,
    tiros_exitosos,
    tiros_totales
FROM (
    VALUES 
    ('Norberto', 5.0, 90, 'Ventoso', 500.0, 6, 1.0, 2, 6),
    ('Jaob', 5.0, 90, 'Ventoso', 500.0, 6, 2.0, 0, 6),
    ('Hilary', 3.0, 90, 'Ventoso', 500.0, 6, 1.0, 1, 6),
    ('Orlando', 5.0, 90, 'Ventoso', 500.0, 6, 2.0, 1, 6),
    ('Josué', 5.0, 90, 'Ventoso', 500.0, 6, 1.0, 1, 6),
    ('Valentino', 5.0, 90, 'Ventoso', 500.0, 6, 2.0, 0, 6),
    ('Diego', 5.0, 90, 'Ventoso', 500.0, 6, 1.0, 0, 6),
    ('David', 5.0, 90, 'Ventoso', 500.0, 6, 2.0, 1, 6)
) AS sesiones_excel(nombre_tirador, distancia_metros, angulo_grados, ambiente, peso_balon, calibre_balon, tiempo_tiro_segundos, tiros_exitosos, tiros_totales)
INNER JOIN tiradores t ON t.nombre = sesiones_excel.nombre_tirador;

PRINT 'Migración de datos del Excel completada exitosamente';

-- Insertar datos de ejemplo en la tabla tiro_excel (valores numéricos limpios)
INSERT INTO tiro_excel (
    nombre_tirador, edad, experiencia, distancia_de_tiro, angulo, 
    altura_de_tirador, peso, ambiente, genero, peso_del_balon, 
    tiempo_de_tiro, tiro_exitoso, diestro_zurdo, calibre_de_balon
)
SELECT 
    nombre_tirador,
    edad,
    experiencia,
    distancia_de_tiro,
    angulo,
    altura_de_tirador,
    peso,
    ambiente,
    genero,
    peso_del_balon,
    tiempo_de_tiro,
    tiro_exitoso,
    diestro_zurdo,
    calibre_de_balon
FROM (
    VALUES 
    ('Norberto', 24, 4, 5.0, 90, 1.70, 95.0, 'Ventoso', 'Masculino', 500.0, 1.0, 1, 'Diestro', 6),
    ('Jaob', 19, 0, 5.0, 90, 1.70, 86.0, 'Ventoso', 'Masculino', 500.0, 2.0, 0, 'Diestro', 6),
    ('Hilary', 19, 0, 3.0, 90, 1.55, 50.0, 'Ventoso', 'Femenino', 500.0, 1.0, 1, 'Diestro', 6),
    ('Orlando', 26, 0, 5.0, 90, 1.67, 69.0, 'Ventoso', 'Masculino', 500.0, 2.0, 1, 'Diestro', 6),
    ('Josué', 24, 0, 5.0, 90, 1.70, 50.0, 'Ventoso', 'Masculino', 500.0, 1.0, 1, 'Diestro', 6),
    ('Valentino', 24, 10, 5.0, 90, 1.85, 88.0, 'Ventoso', 'Masculino', 500.0, 2.0, 0, 'Diestro', 6),
    ('Diego', 22, 4, 5.0, 90, 1.68, 58.0, 'Ventoso', 'Masculino', 500.0, 1.0, 0, 'Diestro', 6),
    ('David', 20, 0, 5.0, 90, 1.70, 71.0, 'Ventoso', 'Masculino', 500.0, 2.0, 1, 'Diestro', 6)
) AS excel_data(
    nombre_tirador, edad, experiencia, distancia_de_tiro, angulo, altura_de_tirador, 
    peso, ambiente, genero, peso_del_balon, tiempo_de_tiro, tiro_exitoso, diestro_zurdo, calibre_de_balon
)
WHERE NOT EXISTS (
    SELECT 1 FROM tiro_excel te 
    WHERE te.nombre_tirador = excel_data.nombre_tirador
);

PRINT 'Datos de ejemplo insertados en tabla tiro_excel';
