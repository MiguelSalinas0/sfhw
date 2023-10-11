from functools import wraps
from flask import flash, redirect, session, url_for

from app.api.api_usuario import eval_menu


def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            flash('No está iniciada la sesión', category='error')
            return redirect(url_for("bp.login"))
        return view_func(*args, **kwargs)
    return wrapper


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not eval_menu(session.get('menu'), permission):
                flash('No tiene autorización', category='error')
                return redirect(url_for('bp.usuario'))
            return func(*args, **kwargs)
        return decorated_view
    return decorator
