from firebird.driver import connect, driver_config, DESCRIPTION_NAME, DESCRIPTION_DISPLAY_SIZE
from flask import current_app, g

def get_db():
  if 'db' not in g:
    g.db = connect('sfh')
    g.cur = g.db.cursor()
  return g.db, g.cur

def close_db(e=None):
  db = g.pop('db', None)
  if db is not None:
    db.close()

def init_app(app):
  app.teardown_appcontext(close_db)    



# Register Firebird server

#driver_config.fb_client_library.set_value("C:/Progr~2/Firebird/Firebi~2/fbclient.dll")
#driver_config.fb_client_library.set_value("C:\Program Files (x86)\Firebird\Firebird_3_0\Fbclient.dll")
srv_cfg = """[local]
host = localhost
user = SYSDBA
password = masterkey
"""
driver_config.register_server('local', srv_cfg)

# Register database
db_cfg = """[sfh]
server = local
database = C:/Adrian/bd/NV30_000024.fdb
protocol = inet
charset = utf8
"""
driver_config.register_database('sfh', db_cfg)
#driver_config.fb_client_library('C:/Progra_1/Firebird/Firebird_3_0/fbclient.dll')


