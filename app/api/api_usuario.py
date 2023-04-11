from db.db import get_db

def get_usuario(usuario: str, clave: str):
    error = None
    con, cur = get_db()
    cur.execute('select * from usuario where NOMBRE_USR = ? and PASSWORD = ?', (usuario, clave))
    usuario = cur.fetchone()
    if usuario == None:
        error = {'error': 'usuario o contraseña inválida'}
        con.commit()
        return {}, error
    else:
        usuario = cur.to_dict(usuario)
        con.commit()
        return {'USUARIO': usuario.get('USUARIO'), 'NOMBRE': usuario.get('NOMBRE')}, error

