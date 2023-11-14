import os
import openpyxl
import xlrd
import datetime
import locale
import zipfile

from xlutils.copy import copy

def get_mes_anio():
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    fecha_actual = datetime.datetime.now()
    mes = fecha_actual.strftime("%B")
    anio = fecha_actual.year
    return mes, anio


def generar_credixsa(datos: list):
    mes, anio = get_mes_anio()
    archivo_excel = "AFECTACIONES-CREDIXSA.xlsx"
    workbook = openpyxl.load_workbook(archivo_excel)
    hoja = workbook.active
    claves_a_incluir = ['DNI', '', 'DOMICILIO1', 'LOCALIDAD', 'cp', 'PROVINCIA', '', 'n_op', 'tipo_c', 'estado', 'fecha', 'TOTAL_DEUDA']
    fila = 3
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir, start=1):
            if columna == 2:
                valor = str(dato.get('APELLIDO')).strip() + ', ' + str(dato.get('NOMBRE')).strip()
            elif columna == 7:
                valor = str(dato.get('CODAREA')).strip() + str(dato.get('TELEFONO')).strip()
            else:
                valor = dato.get(clave, '')
            hoja.cell(row=fila, column=columna, value=valor)
        fila += 1
    nuevo_nombre = f'{mes}-{anio}-{archivo_excel}'
    workbook.save(os.path.join('excel', nuevo_nombre))
    workbook.close()


def generar_veraz(datos: list):
    mes, anio = get_mes_anio()
    archivo_excel = "AFECTACIONES_VERAZ_C23057_202307_INI.xls"
    archivo_lectura = xlrd.open_workbook(archivo_excel)
    claves_a_incluir = ['', 'DNI', '', '', '', '', '', 'TOTAL_DEUDA', '', '', 'SEXO', '', '', '', 'LOCALIDAD', 'PROVINCIA', 'cp', '', '', '', '', 'FNACIM', '', '', '']
    archivo_escritura = copy(archivo_lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)
    ultima_fila = 3
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            if columna == 0:
                valor = str(dato.get('APELLIDO')).strip() + ', ' + str(dato.get('NOMBRE')).strip()
            elif columna == 20:
                valor = str(dato.get('CODAREA')).strip() + str(dato.get('TELEFONO')).strip()
            else:
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
    mes, anio = get_mes_anio()
    archivo_excel = "AFECTACIONES - CODESA.xls"
    archivo_lectura = xlrd.open_workbook(archivo_excel)
    claves_a_incluir = ['n_cr', 'DNI', '', 'APELLIDO', 'NOMBRE', 'f_otorg', 'TOTAL_DEUDA', 'DOMICILIO1', 'LOCALIDAD', 'PROVINCIA', 'cp', '', 'TRABAJO', 'dom_tr', 'LOCALIDAD_TRABAJO', 'CODPOS_TRABAJO', 'tel_em', 'tipo']
    archivo_escritura = copy(archivo_lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)
    ultima_fila = 4
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            if columna == 2:
                sexo = str(dato.get('SEXO')).strip()
                valor = 'F' if sexo == 'Femenino' else 'M'
            elif columna == 11:
                valor = str(dato.get('CODAREA')).strip() + str(dato.get('TELEFONO')).strip()
            else: 
                valor = dato.get(clave, '')
            hoja_escritura.write(ultima_fila, columna, valor)
        ultima_fila += 1
    nuevo_nombre = f'{mes}-{anio}-{archivo_excel}'
    archivo_escritura.save(os.path.join('excel', nuevo_nombre))


def generar_catamarca(datos: list):
    mes, anio = get_mes_anio()
    archivo_excel = "AFECTACIONES - CATAMARCA.xls"
    archivo_lectura = xlrd.open_workbook(archivo_excel)
    claves_a_incluir = ['DNI', '', 'fecha_pedido', 'Fecha_Acuerdo', 'Codigo', 'nro_cred', 'Monto', 'Cuotas', 'Importe_Cuotas', '1_Vencimiento']
    archivo_escritura = copy(archivo_lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)
    ultima_fila = 4
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            if columna == 1:
                valor = str(dato.get('APELLIDO')).strip() + ', ' + str(dato.get('NOMBRE')).strip()
            else:
                valor = dato.get(clave, '')
            hoja_escritura.write(ultima_fila, columna, valor)
        ultima_fila += 1
    nuevo_nombre = f'{mes}-{anio}-{archivo_excel}'
    archivo_escritura.save(os.path.join('excel', nuevo_nombre))
