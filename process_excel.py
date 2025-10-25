"""
Script para procesar archivos Excel y extraer datos estructurados.
Convierte archivos Excel a formato JSON manteniendo la estructura de datos.
"""

import json
import pandas as pd


def process_excel_file(excel_file_path):
    """Procesar archivo Excel y extraer datos estructurados"""
    try:
        # Leer el archivo Excel
        df = pd.read_excel(excel_file_path, header=None)

        # Encontrar la fila con los encabezados (fila 1, índice 1)
        header_row = 1
        column_headers = df.iloc[header_row].tolist()

        # Crear DataFrame con los datos reales (saltando las filas vacías)
        data_df = df.iloc[header_row + 1:].copy()
        data_df.columns = column_headers

        # Limpiar datos (eliminar filas completamente vacías)
        data_df = data_df.dropna(how='all')

        # Convertir a diccionario
        data_records = []
        for _, row in data_df.iterrows():
            data_record = {}
            for col in column_headers:
                if pd.notna(row[col]):
                    data_record[col] = str(row[col])
                else:
                    data_record[col] = None
            data_records.append(data_record)

        return data_records, column_headers

    except (FileNotFoundError, pd.errors.EmptyDataError, ValueError, OSError) as e:
        print(f"Error procesando archivo: {e}")
        return [], []


if __name__ == "__main__":
    FILE_PATH = "evidencia big data.xlsx"
    records, headers = process_excel_file(FILE_PATH)

    print(f"Encabezados encontrados: {headers}")
    print(f"Número de registros: {len(records)}")
    print("\nPrimeros 3 registros:")
    for i, record in enumerate(records[:3]):
        print(f"Registro {i+1}: {record}")

    # Guardar en JSON para verificar
    with open("excel_data.json", "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print("\nDatos guardados en excel_data.json")
