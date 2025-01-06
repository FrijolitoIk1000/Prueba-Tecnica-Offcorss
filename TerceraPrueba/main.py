import pandas as pd
import os


def anomaly_detection (file_path):
    
    df = pd.read_csv(file_path)
    # Verificar si hay duplicados en la columna 'TransactionID'
    duplicates = df[df.duplicated(subset='TransactionID', keep=False)]

    if not duplicates.empty:
        print('Se han encontrado duplicados en el archivo.')
        print(f"Cantidad de duplicados: {len(duplicates)}")
        # Eliminar duplicados
        df = df.drop_duplicates(subset='TransactionID', keep='first')
        print('Duplicados eliminados.')
    else:
        print('No se han encontrado duplicados en el archivo.')
    
    # Convertir valores negativos en la columna 'PricePerUnit' y 'QuantitySold' a positivos
    df['PricePerUnit'] = df['PricePerUnit'].abs()
    df['QuantitySold'] = df['QuantitySold'].abs()

   # Verificar y corregir la columna 'TotalSales'
    df['CalculatedTotalSales'] = df['QuantitySold'] * df['PricePerUnit']
    incorrect_totals = df[df['CalculatedTotalSales'] != df['TotalSales']]

    if not incorrect_totals.empty:
        print('Se han encontrado discrepancias en la columna TotalSales.')
        print(f"Cantidad de discrepancias: {len(incorrect_totals)}")
        
        # Corregir la columna 'TotalSales'
        df['TotalSales'] = df['CalculatedTotalSales'].round(2)
        print('Discrepancias corregidas.')
    else:
        print('No se han encontrado discrepancias en la columna TotalSales.')

    # Eliminar la columna 'CalculatedTotalSales' 
    df.drop(columns=['CalculatedTotalSales'], inplace=True)

    # Guardar el DataFrame modificado en un nuevo archivo CSV
    output_file_path = os.path.splitext(file_path)[0] + '_cleaned.csv'
    df.to_csv(output_file_path, index=False)
    print(f"Archivo limpio guardado como: {output_file_path}")

def main():

    file_path = 'TerceraPrueba\csv\sales_data.csv'
    
    anomaly_detection(file_path)


if __name__ == "__main__":
    main()