from firebird.driver import connect, driver_config, DESCRIPTION_NAME, DESCRIPTION_DISPLAY_SIZE
from flask import current_app, g
import configparser


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
# driver_config.fb_client_library.set_value("C:/Progr~2/Firebird/Firebi~2/fbclient.dll")
# driver_config.fb_client_library.set_value("C:\Program Files (x86)\Firebird\Firebird_3_0\Fbclient.dll")
fbClientLibrary = "C:/Program Files/Firebird/Firebird_3_0/fbclient.dll"

driver_config.fb_client_library.set_value(fbClientLibrary)
configdb = configparser.ConfigParser()
configdb.read('config.ini')
host = configdb['base']['host']
user = configdb['base']['username']
password = configdb['base']['password']
server = configdb['base']['server']
databasefile = configdb['base']['databasefile']
port = configdb['base']['port']
protocol = configdb['base']['protocol']
charset = configdb['base']['charset']

# print(host + "/" + server + "/" + databasefile)


srv_cfg = """[local]
host = """ + host + """
user = """ + user + """
password = """ + password + """
"""
driver_config.register_server('local', srv_cfg)
# Register database
# database = C:/Adrian/bd/NV30_000024.fdb
db_cfg = """[sfh]
server = """ + server + """
database = """ + databasefile + """
port = """ + port + """
protocol = """ + protocol + """
charset = """ + charset + """
"""
driver_config.register_database('sfh', db_cfg)

# driver_config.fb_client_library('C:/Progra_1/Firebird/Firebird_3_0/fbclient.dll')
