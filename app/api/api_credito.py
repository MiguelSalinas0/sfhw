from flask import session
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
        error = {'error':'Error grabando credito: ' + str(E)}

    return error

def get_creditos(estado: int = 0):
    error = None
    con, cur = get_db()
    cur.execute("select C.ID, C.IDCLIENTE, (TRIM(CL.NOMBRE) || ', ' || TRIM(CL.APELLIDO)) NOMCLI, C.FECHA, C.IDSUCURSAL, S.NOMBRE as SUCURSAL, C.IDVENDEDOR, C.TOTAL, C.ESTADO, U.NOMBRE as AUTORIZA " +
                "from creditos C " +
                "join clientes CL " +
                "  on CL.CLIEN = C.IDCLIENTE " +
                "left join sucursal S on S.SUCURSAL = C.IDSUCURSAL " +
                "left join usuario U on U.USUARIO = C.IDAUTORIZO " +
                "where ESTADO = ?", (estado,))
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error

def get_credito_pendiente(id: int, estado: int):
    error = None
    con, cur = get_db()
    cur.execute("select CR.IDCLIENTE, TRIM(C.APELLIDO) as APELLIDO , TRIM(C.NOMBRE) as NOMBRE, " +
                "C.SEXO, (TRIM(C.CODAREA) || TRIM(C.TELEFONO)) as TELEFONO, C.DOMICILIO1, C.DNI, " +
                "C.TRABAJO, A.NOMBRE ACTIVIDAD, C.CARGO, C.FNACIM, CR.FECHA, E.NOMBRE as VENDEDOR, " +
                "S.NOMBRE as SUCURSAL, CR.ESTADO, CR.TOTAL, CR.DIA, CR.HORA, CR.TOTAL_AUTORIZADO, " +
                "U.NOMBRE AUTORIZA " +
                "from creditos CR " +
                "left join clientes C on C.CLIEN = CR.IDCLIENTE " +
                "left join sucursal S on S.SUCURSAL = CR.IDSUCURSAL " +
                "left join usuario E on E.USUARIO = CR.IDVENDEDOR " +
                "left join usuario U on U.USUARIO = CR.IDAUTORIZO " +
                "left join tipos A on A.IDTIPO = C.ACTIVIDAD and A.TIPO = '0017' "
                "where CR.ID = ? and ESTADO = ?", (id, estado))
    datos = cur.fetchone()
    if datos == None:
          datos = {}
          error = {'error': f'No hay datos para el crédito solicitado: {id}'}
    else:
      datos = cur.to_dict(datos)
      cur.execute('update creditos set ESTADO = 1, IDAUTORIZO = ? where ID = ?', (session["usuario"], id))
    con.commit()      
    return datos, error

def get_itemscred(id: int):
    error = None
    con, cur = get_db()
    cur.execute("select ICR.IDARTICULO, A.NOMBRE as DETALLE, M.NOMBRE as MARCA, ICR.CANTIDAD, ICR.UNITARIO " +
                "from items_creditos ICR " + 
                "left join articulos A on A.CODIGO = ICR.IDARTICULO " +
                "left join marcas M on M.MARCA = A.MARCA " +
                "where ICR.ID = ?", (id,))
    rows = cur.fetchall()
    if rows == None:
          datos = {}
          error = {'error': f'No hay datos de artículos para el crédito solicitado: {id}'}
    else:
        datos = []
        for row in rows:
            datos.append(cur.to_dict(row))
    con.commit      
    return datos, error

def get_creditos_otorgados(id: int):
    con, cur = get_db()
    cur.execute("select C.CLIEN from creditos CR join clientes C on C.CLIEN = CR.IDCLIENTE where CR.ID = ?", (id,))
    idcliente = cur.fetchone()[0]
    cur.execute("select FECHA, DEBITO, TOTPAGOS, TOTCAPITAL, SALDO_VENCIDO, CTAS_IMPAGAS " +
                "from GET_CTACTE_CLI(?) ", (idcliente,))
    rows = cur.fetchall()
    if rows == None:
          datos = {}
    else:
        datos = []
        for row in rows:
            datos.append(cur.to_dict(row))
    con.commit      
    return datos

def get_historial_creditos(id: int):
    con, cur = get_db()
    cur.execute("select FECHA, DEBITO, TOTPAGOS, TOTCAPITAL, SALDO_VENCIDO, CTAS_IMPAGAS " +
                "from GET_CTACTE_CLI(?) ", (id,))
    rows = cur.fetchall()
    if rows == None:
          datos = {}
    else:
        datos = []
        for row in rows:
            datos.append(cur.to_dict(row))
    con.commit      
    return datos

