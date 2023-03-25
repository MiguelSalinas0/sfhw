import requests
from flask import session


def get_cliente(idcliente):
    error = None
    url = session['urlWS'] + 'cliente/' + idcliente
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json(), error
    else:
        error = respuesta.status_code
        return {}, error


def get_tipodoc():
    error = None
    url = session['urlWS'] + 'tipodocumento'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json(), error
    else:
        error = respuesta.status_code
        return {}, error


def get_tipocontribuciones():
    error = None
    url = session['urlWS'] + 'tipocontribuciones'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json(), error
    else:
        error = respuesta.status_code
        return {}, error


def get_estadocivil():
    error = None
    url = session['urlWS'] + 'estadocivil'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json(), error
    else:
        error = respuesta.status_code
        return {}, error


def get_localidades():
    error = None
    url = session['urlWS'] + 'localidades'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json(), error
    else:
        error = respuesta.status_code
        return {}, error


def get_categorias():
    error = None
    url = session['urlWS'] + 'categorias'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json(), error
    else:
        error = respuesta.status_code
        return {}, error


def get_sucursales():
    error = None
    url = session['urlWS'] + 'sucursales'
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json(), error
    else:
        error = respuesta.status_code
        return {}, error


def get_articulo(idArticulo):
    error = None
    url = session['urlWS'] + 'articulo/' + idArticulo
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json(), error
    else:
        error = respuesta.status_code
        return {}, error
