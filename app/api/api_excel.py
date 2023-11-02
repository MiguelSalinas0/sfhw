import os
import openpyxl
import xlrd
import datetime
import locale
import zipfile

from xlutils.copy import copy


locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

fecha_actual = datetime.datetime.now()
mes = fecha_actual.strftime("%B")
anio = fecha_actual.year


def generar_credixsa(datos: list):
    archivo_excel = "AFECTACIONES-CREDIXSA.xlsx"
    workbook = openpyxl.load_workbook(archivo_excel)
    hoja = workbook.active
    claves_a_incluir = ['','DNI', 'APENOM', 'DOMICILIO1', 'LOCALIDAD', 'cp', 'PROVINCIA', 'CODAREA']
    fila = 3
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir, start=1):
            valor = dato.get(clave, '')
            hoja.cell(row=fila, column=columna, value=valor)
        fila += 1
    nuevo_nombre = f'{mes}-{anio}-{archivo_excel}'
    workbook.save(os.path.join('excel', nuevo_nombre))
    workbook.close()


def generar_veraz(datos: list):

    archivo_excel = "AFECTACIONES_VERAZ_C23057_202307_INI.xls"
    archivo_lectura = xlrd.open_workbook(archivo_excel)

    claves_a_incluir = ['APENOM', 'DNI']

    archivo_escritura = copy(archivo_lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)
    ultima_fila = 2
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            valor = dato.get(clave, '')
            hoja_escritura.write(ultima_fila, columna, valor)
        ultima_fila += 1
    nuevo_nombre = f'{mes}-{anio}-{archivo_excel}'
    archivo_escritura.save(os.path.join('excel', nuevo_nombre))

    # Crear un archivo ZIP y agregar el archivo de Excel
    archivo_excel_ruta = os.path.join('excel', nuevo_nombre)
    with zipfile.ZipFile(f'{mes}-{anio}-AFECTACIONES_VERAZ.zip', 'w') as archivo_zip:
        archivo_zip.write(archivo_excel_ruta, os.path.basename(nuevo_nombre))


def generar_codesa(datos: list):
    archivo_excel = "AFECTACIONES - CODESA.xls"
    archivo_lectura = xlrd.open_workbook(archivo_excel)
    claves_a_incluir = ['APENOM', 'DNI']
    archivo_escritura = copy(archivo_lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)
    ultima_fila = 4
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            valor = dato.get(clave, '')
            hoja_escritura.write(ultima_fila, columna, valor)
        ultima_fila += 1
    nuevo_nombre = f'{mes}-{anio}-{archivo_excel}'
    archivo_escritura.save(os.path.join('excel', nuevo_nombre))


def generar_catamarca(datos: list):
    archivo_excel = "AFECTACIONES - CATAMARCA.xls"
    archivo_lectura = xlrd.open_workbook(archivo_excel)
    claves_a_incluir = ['Documento', 'Apellido_y_Nombre', 'Fecha_Acuerdo', 'Codigo', 'Monto', 'Cuotas', 'Importe_Cuotas', '1_Vencimiento']
    archivo_escritura = copy(archivo_lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)
    ultima_fila = 4
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            valor = dato.get(clave, '')
            hoja_escritura.write(ultima_fila, columna, valor)
        ultima_fila += 1
    nuevo_nombre = f'{mes}-{anio}-{archivo_excel}'
    archivo_escritura.save(os.path.join('excel', nuevo_nombre))
