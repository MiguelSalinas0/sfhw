from flask import Blueprint

bp = Blueprint('bp', __name__, template_folder='templates', static_folder='static')

from .routers import login, cliente, credito, estadocuenta, usuario, mensajes, perfil_menu, excel