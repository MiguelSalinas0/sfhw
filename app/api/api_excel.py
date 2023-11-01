import openpyxl
import xlrd
import datetime
import locale
import zipfile

from xlutils.copy import copy



def generar_credixsa(datos: list, ruta_completa):
    workbook = openpyxl.load_workbook(ruta_completa)
    hoja = workbook.active
    claves_a_incluir = ['DNI', 'APENOM', 'Domicilio', 'LOCALIDAD', 'cp', 'prov', 'TELEFONO_CELULAR']
    fila = 3
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir, start=1):
            valor = dato.get(clave, '')
            hoja.cell(row=fila, column=columna, value=valor)
        fila += 1
    workbook.save(ruta_completa)
    workbook.close()


def generar_veraz(datos: list):

    archivo_excel = "AFECTACIONES_VERAZ_C23057_202307_INI.xls"
    archivo_lectura = xlrd.open_workbook(archivo_excel)

    claves_a_incluir = ['Apellido', 'DNI']

    archivo_escritura = copy(archivo_lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)
    ultima_fila = 2
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            valor = dato.get(clave, '')
            hoja_escritura.write(ultima_fila, columna, valor)
        ultima_fila += 1
    archivo_escritura.save(f'{mes}-{anio}-{archivo_excel}')

    # Crear un archivo ZIP y agregar el archivo de Excel
    with zipfile.ZipFile(f'{mes}-{anio}-AFECTACIONES_VERAZ.zip', 'w') as archivo_zip:
        archivo_zip.write(f'{mes}-{anio}-{archivo_excel}')




def generar_codesa(datos: list, ruta_completa):
    archivo_lectura = xlrd.open_workbook(ruta_completa)
    claves_a_incluir = ['APENOM', 'DNI']
    archivo_escritura = copy(archivo_lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)
    ultima_fila = 4
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            valor = dato.get(clave, '')
            hoja_escritura.write(ultima_fila, columna, valor)
        ultima_fila += 1
    archivo_escritura.save(f'{mes}-{anio}-{archivo_excel}')


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
    archivo_escritura.save(f'{mes}-{anio}-{archivo_excel}')
