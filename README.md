## README: Prueba Técnica OFFCORSS

### Descripción General

Este repositorio contiene los archivos de la prueba técnica realizada para OFFCORSS, enfocada en el procesamiento de datos de facturas y ventas utilizando Python.

### Estructura del Proyecto

* **SegundaPrueba:**
  * **main.py:** Script principal encargado de: Extraer informacion de las Facturas y generar un csv
    * Cargar archivos de facturas en formato [JPG] desde la carpeta `InvoicesExamples`.
  * **InvoicesExamples:** Contiene ejemplos de facturas en el formato especificado.

* **TerceraPrueba:**
  * **main.py:** Script principal que: Verifica anomalias y genera un nuevo csv depurado
    * Carga el archivo `sales_data.csv` desde la carpeta `csv`.
  * **csv:** Contiene el archivo `sales_data.csv` con datos de ventas en formato CSV.

### Requisitos Previos

* **Python:** Versión [versión de Python].
* **Librerías:**
  * [pandas,easyocr]
  * Instalar con `pip install -r requirements.txt`.


