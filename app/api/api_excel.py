import openpyxl
import xlrd
from xlutils.copy import copy


def generar_credixsa(datos: list):

    archivo_excel = "AFECTACIONES-CREDIXSA.xlsx"
    workbook = openpyxl.load_workbook(archivo_excel)

    # Seleccionar la hoja en la que se desea trabajar (por defecto, la primera hoja)
    hoja = workbook.active

    claves_a_incluir = ['DNI', 'Apellido', 'Domicilio']

    # Encabezados en la fila 1 (A1, B1, C1, ...)
    # encabezados = claves_a_incluir
    # for columna, encabezado in enumerate(encabezados, start=1):
    #     hoja.cell(row=1, column=columna, value=encabezado)

    # Escribir datos en filas sucesivas (A2, B2, C2, ...)
    fila = 3
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir, start=1):
            valor = dato.get(clave, '')
            hoja.cell(row=fila, column=columna, value=valor)
        fila += 1

    workbook.save(archivo_excel)
    workbook.close()


def generar_veraz(datos: list):

    archivo_excel = "AFECTACIONES_VERAZ_C23057_202307_INI.xls"
    archivo_lectura = xlrd.open_workbook(archivo_excel)

    claves_a_incluir = ['Apellido', 'DNI']

    archivo_escritura = copy(archivo_lectura)

    # Abre la hoja para escritura (asegúrate de que sea la misma hoja que la de lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)

    # Encabezados en la fila 1
    # encabezados = claves_a_incluir
    # for columna, encabezado in enumerate(encabezados):
    #     hoja_escritura.write(ultima_fila, columna, encabezado)

    # Escribir datos en filas sucesivas
    ultima_fila = 2
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            valor = dato.get(clave, '')
            hoja_escritura.write(ultima_fila, columna, valor)
        ultima_fila += 1

    archivo_escritura.save(archivo_excel)


def generar_codesa(datos: list):
    archivo_excel = "AFECTACIONES - CODESA.xls"
    archivo_lectura = xlrd.open_workbook(archivo_excel)
    claves_a_incluir = ['Apellido', 'DNI']
    archivo_escritura = copy(archivo_lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)
    ultima_fila = 4
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            valor = dato.get(clave, '')
            hoja_escritura.write(ultima_fila, columna, valor)
        ultima_fila += 1
    archivo_escritura.save(archivo_excel)
