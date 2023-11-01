import openpyxl
import xlrd
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


def generar_veraz(datos: list, ruta_completa):
    archivo_lectura = xlrd.open_workbook(ruta_completa)
    claves_a_incluir = ['APENOM', 'DNI']
    archivo_escritura = copy(archivo_lectura)
    hoja_escritura = archivo_escritura.get_sheet(0)
    ultima_fila = 2
    for dato in datos:
        for columna, clave in enumerate(claves_a_incluir):
            valor = dato.get(clave, '')
            hoja_escritura.write(ultima_fila, columna, valor)
        ultima_fila += 1
    archivo_escritura.save(ruta_completa)


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
    archivo_escritura.save(ruta_completa)
