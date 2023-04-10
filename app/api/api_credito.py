from db.db import get_db
from datetime import date

def new_credito(cliente_cred, items_cred):
    error = None
    con, cur = get_db()
    try:
        total = 0.0
        for item in items_cred:
            total = total + (item.get('cantidad') * item.get('unitario'))
        cur.execute("SELECT GEN_ID(GEN_CREDITOS_ID, 1 ) FROM RDB$DATABASE")
        idcred = cur.to_dict(cur.fetchone()) 
        idcred.get('GEN_ID')
        cur.execute("insert into CREDITOS (ID, IDCLIENTE, FECHA, IDVENDEDOR, IDSUCURSAL, ESTADO, IDAUTORIZO, TOTAL) "
                    "values (?, ?, ?, ?, ?, ?, ?, ?)", (idcred.get('GEN_ID'),
                                                        cliente_cred.get('idcliente'),
                                                        date.today(),
                                                        cliente_cred.get('idvendedor').zfill(4),
                                                        cliente_cred.get('sucursal'),
                                                        0,
                                                        0,
                                                        total))
        for i, item in enumerate(items_cred):
            print(item)
            cur.execute("insert into ITEMS_CREDITOS (ID, IDITEM, IDARTICULO, CANTIDAD, UNITARIO) "
                        "values (?, ?, ?, ?, ?)",
                        (idcred.get('GEN_ID'),
                         i+1,
                         item.get('codigo'),
                         item.get('cantidad'),
                         item.get('unitario')
                        ))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error':'Error grabando credito: ' + str(E)}

    return error