import requests
from flask import session


def get_datos(argument: str, idArtCli=0):
    error = None
    switcher = {
        'tipodoc': session['urlWS'] + 'tipodocumento',
        'tipocontribuciones': session['urlWS'] + 'tipocontribuciones',
        'estadocivil': session['urlWS'] + 'estadocivil',
        'localidades': session['urlWS'] + 'localidades',
        'categorias': session['urlWS'] + 'categorias',
        'sucursales': session['urlWS'] + 'sucursales',
        'cliente': session['urlWS'] + 'cliente/' + str(idArtCli),
        'articulo': session['urlWS'] + 'articulo/' + str(idArtCli),
        'creditos': session['urlWS'] + 'solcred/0',
    }
    url = switcher.get(argument)
    if url != None:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            return respuesta.json(), error
        else:
            error = respuesta.status_code
            return {}, error
    else:
        return {}, error
