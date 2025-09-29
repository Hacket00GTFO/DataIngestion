USE DataIngestionDB;
GO

-- Insertar datos de muestra del archivo evidencia big data.xlsx
INSERT INTO data_records (data, source, is_processed) VALUES 
('{"Nombre tirador": "Norberto", "Edad": "24", "Experiencia": "4 años", "Distancia de tiro ": "5 metros ", "Angulo ": "90 grados", "Altura de tirador": "1.7", "Peso ": "95 kg", "Ambiente": "Ventoso", "Genero": "Masculino", "Peso del balon": "500 g", "Tiempo de tiro": "1 segundo", "Tiro exitoso?": "2 de 6", "Diestro / zurdo": "Diestro", "Calibre de balon": "6"}', 'evidencia_big_data_excel', 1),
('{"Nombre tirador": "Jaob", "Edad": "19", "Experiencia": "0 años", "Distancia de tiro ": "5 metros", "Angulo ": "90 grados ", "Altura de tirador": "1.7", "Peso ": "86 kg", "Ambiente": "Ventoso", "Genero": "Masculino", "Peso del balon": "500 g", "Tiempo de tiro": "2 segundos", "Tiro exitoso?": "0 de 6", "Diestro / zurdo": "Diestro", "Calibre de balon": "6"}', 'evidencia_big_data_excel', 1),
('{"Nombre tirador": "Hilary", "Edad": "19", "Experiencia": "0 años", "Distancia de tiro ": "3 metros", "Angulo ": "90 grados", "Altura de tirador": "1.55", "Peso ": "50 kg", "Ambiente": "Ventoso", "Genero": "Femenino", "Peso del balon": "500 g", "Tiempo de tiro": "1 segundo ", "Tiro exitoso?": "1 de 6", "Diestro / zurdo": "Diestro", "Calibre de balon": "6"}', 'evidencia_big_data_excel', 1),
('{"Nombre tirador": "Orlando", "Edad": "26", "Experiencia": "2 años", "Distancia de tiro ": "5 metros", "Angulo ": "90 grados", "Altura de tirador": "1.8", "Peso ": "80 kg", "Ambiente": "Ventoso", "Genero": "Masculino", "Peso del balon": "500 g", "Tiempo de tiro": "1 segundo", "Tiro exitoso?": "3 de 6", "Diestro / zurdo": "Diestro", "Calibre de balon": "6"}', 'evidencia_big_data_excel', 1),
('{"Nombre tirador": "Sofia", "Edad": "22", "Experiencia": "1 año", "Distancia de tiro ": "4 metros", "Angulo ": "90 grados", "Altura de tirador": "1.6", "Peso ": "55 kg", "Ambiente": "Ventoso", "Genero": "Femenino", "Peso del balon": "500 g", "Tiempo de tiro": "2 segundos", "Tiro exitoso?": "1 de 6", "Diestro / zurdo": "Diestro", "Calibre de balon": "6"}', 'evidencia_big_data_excel', 1),
('{"Nombre tirador": "Carlos", "Edad": "28", "Experiencia": "5 años", "Distancia de tiro ": "6 metros", "Angulo ": "90 grados", "Altura de tirador": "1.75", "Peso ": "78 kg", "Ambiente": "Ventoso", "Genero": "Masculino", "Peso del balon": "500 g", "Tiempo de tiro": "1 segundo", "Tiro exitoso?": "4 de 6", "Diestro / zurdo": "Diestro", "Calibre de balon": "6"}', 'evidencia_big_data_excel', 1),
('{"Nombre tirador": "Ana", "Edad": "21", "Experiencia": "0 años", "Distancia de tiro ": "3 metros", "Angulo ": "90 grados", "Altura de tirador": "1.58", "Peso ": "52 kg", "Ambiente": "Ventoso", "Genero": "Femenino", "Peso del balon": "500 g", "Tiempo de tiro": "3 segundos", "Tiro exitoso?": "0 de 6", "Diestro / zurdo": "Diestro", "Calibre de balon": "6"}', 'evidencia_big_data_excel', 1),
('{"Nombre tirador": "Miguel", "Edad": "30", "Experiencia": "3 años", "Distancia de tiro ": "5 metros", "Angulo ": "90 grados", "Altura de tirador": "1.72", "Peso ": "88 kg", "Ambiente": "Ventoso", "Genero": "Masculino", "Peso del balon": "500 g", "Tiempo de tiro": "1 segundo", "Tiro exitoso?": "5 de 6", "Diestro / zurdo": "Diestro", "Calibre de balon": "6"}', 'evidencia_big_data_excel', 1);
GO

-- Verificar que los datos se insertaron
SELECT COUNT(*) as total_records FROM data_records;
SELECT * FROM vw_data_statistics;
