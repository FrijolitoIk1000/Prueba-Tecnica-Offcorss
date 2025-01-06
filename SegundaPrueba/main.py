import easyocr
import re
import pandas as pd
import os
import glob

def extract_text_from_image(image_path, reader):
    result = reader.readtext(image_path, paragraph=True, x_ths=0.2)
    df = pd.DataFrame(result, columns=['bbox', 'text'])
    df.drop(columns=['bbox'], inplace=True)
    return '\n\n'.join(df['text'].tolist())

def extract_data_from_text(text):
    patterns = {
        'provider_name': re.compile(r"((?:(?![A-Z]{2,})[A-Za-z\s])+?Inc)"),
        'items': re.compile(r"(?s)(?<=IMPORTE)(.*?)(?=Sub)"),
        'date': re.compile(r"(\d{2}/\d{2}/\d{4})"),
        'provider_id': re.compile(r"ES-\d*"),
        'iva': re.compile(r"IVA\s+(\d+[.,]?\d*)")
    }

    data = {}
    try:
        data['provider_name'] = patterns['provider_name'].search(text).group(1).strip()
    except AttributeError:
        data['provider_name'] = "No encontrado"

    try:
        data['provider_id'] = patterns['provider_id'].search(text).group(0).strip()
    except AttributeError:
        data['provider_id'] = "No encontrado"

    try:
        data['items_match'] = patterns['items'].search(text)
    except AttributeError:
        data['items_match'] = None

    try:
        data['date'] = patterns['date'].search(text).group(1).strip()
    except AttributeError:
        data['date'] = "No encontrado"

    try:
        data['iva'] = patterns['iva'].search(text).group(1).strip()
    except AttributeError:
        data['iva'] = "No encontrado"

    return data

def process_items(items_match):
    items_list = []
    total_sum = 0
    if items_match:
        items_text = items_match.group(1).strip()
        item_pattern = re.compile(r"([^\d\n]+)\s+(\d+[.,]?\d*)\s+(\d+[.,]?\d*)")
        items = item_pattern.findall(items_text)
        
        for item in items:
            item_name = item[0].strip()
            price = float(item[1].replace(',', '.').strip())
            total = float(item[2].replace(',', '.').strip())
            items_list.append(f"{item_name} (Precio: {price}, Total: {total}, Cantidad: {total/price})")
            total_sum += total
    else:
        items_list.append("No se encontraron items")
    
    return items_list, total_sum

def main():
    # Crear un lector de EasyOCR
    reader = easyocr.Reader(["es"], gpu=False)

    # Directorio de las imágenes
    image_dir = "SegundaPrueba/InvoicesExamples/"

    # Crear un diccionario vacío para los datos
    data_output = {
        'Numero de factura': [],
        'Fecha': [],
        'Nombre del proveedor': [],
        'IVA': [],
        'Items': [],
        'Total': []
    }

    # Obtener la lista de archivos de imagen en el directorio
    image_files = glob.glob(os.path.join(image_dir, "*.jpg"))

    for image_file in image_files:
        text = extract_text_from_image(image_file, reader)
        data = extract_data_from_text(text)
        items_list, total_sum = process_items(data['items_match'])

        # Añadir los datos al diccionario
        data_output['Numero de factura'].append(data['provider_id'])
        data_output['Fecha'].append(data['date'])
        data_output['Nombre del proveedor'].append(data['provider_name'])
        data_output['IVA'].append(data['iva'])
        data_output['Items'].append("; ".join(items_list))
        data_output['Total'].append(total_sum)

    # Convertir el diccionario en un DataFrame
    df_output = pd.DataFrame(data_output)

    # Guardar el DataFrame en un archivo CSV
    df_output.to_csv('data_output.csv', index=False)

    print(df_output)

if __name__ == "__main__":
    main()
