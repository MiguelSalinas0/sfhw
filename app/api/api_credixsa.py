import requests
from db.db import get_db

url = "https://webservice.credixsa.com/ws004.php"

usuario = "1005751018"
clave = "R6cf8DTR872p"


def consultar(nombre: str, dni: str):
    payload = {
        "wscx_id": dni,
        "wscx_usu": usuario,
        "wscx_pas": clave,
        "wscx_nom": nombre
    }
    response = requests.post(url, data=payload)
    resultado = response.text
    fields = resultado.split("|")
    data = {
        "id_cliente": fields[0],
        "nombre": fields[1],
        "id_conyuge/concubino_(dni/cuil)": fields[2],
        "cuit_laboral": fields[3],
        "politica_a_aplicar": fields[4],
        "id_consulta": fields[5],
        "existencia_validada": fields[6],
        "nombre_validado": fields[7],
        "resultado": fields[8],
        "observaciones": fields[9],
        "dni": fields[10],
        "cuil": fields[11],
        "nombre_": fields[12],
        "domicilio_personal": fields[13],
        "cp": fields[14],
        "localidad": fields[15],
        "provincia": fields[16],
        "fecha_nacimiento": fields[17],
        "sexo": fields[18],
        "cuit": fields[19],
        "razon_social": fields[20],
        "domicilio_fiscal": fields[21],
        "cp_fiscal": fields[22],
        "localidad_fiscal": fields[23],
        "provincia_fiscal": fields[24],
        "imp_ganancias": fields[25],
        "imp_iva": fields[26],
        "categoria_monotributo": fields[27],
        "integra_sociedades": fields[28],
        "empleador": fields[29],
        "cantidad_empleados_estimados": fields[30],
        "actividad_principal_afip": fields[31],
        "fecha_inicio_actividades": fields[32],
        "cantidad_atrasos_vigentes_categoria_2": fields[33],
        "cantidad_atrasos_vigentes_categoria_3": fields[34],
        "cantidad_atrasos_vigentes_categoria_4": fields[35],
        "cantidad_atrasos_vigentes_categoria_5": fields[36],
        "cantidad_atrasos_categoria_2_ult_3_meses": fields[37],
        "cantidad_atrasos_categoria_3_ult_3_meses": fields[38],
        "cantidad_atrasos_categoria_4_ult_3_meses": fields[39],
        "cantidad_atrasos_categoria_5_ult_3_meses": fields[40],
        "cantidad_atrasos_categoria_2_ult_6_meses": fields[41],
        "cantidad_atrasos_categoria_3_ult_6_meses": fields[42],
        "cantidad_atrasos_categoria_4_ult_6_meses": fields[43],
        "cantidad_atrasos_categoria_5_ult_6_meses": fields[44],
        "cantidad_atrasos_categoria_2_ult_12_meses": fields[45],
        "cantidad_atrasos_categoria_3_ult_12_meses": fields[46],
        "cantidad_atrasos_categoria_4_ult_12_meses": fields[47],
        "cantidad_atrasos_categoria_5_ult_12_meses": fields[48],
        "cantidad_atrasos_categoria_2_ult_24_meses": fields[49],
        "cantidad_atrasos_categoria_3_ult_24_meses": fields[50],
        "cantidad_atrasos_categoria_4_ult_24_meses": fields[51],
        "cantidad_atrasos_categoria_5_ult_24_meses": fields[52],
        "moroso_en_la_entidad_consultante_vigente": fields[53],
        "moroso_en_la_entidad_consultante_no_vigente": fields[54],
        "cantidad_situaciones_1_vigentes": fields[55],
        "cantidad_situaciones_2_vigentes": fields[56],
        "cantidad_situaciones_3_vigentes": fields[57],
        "cantidad_situaciones_4_vigentes": fields[58],
        "cantidad_situaciones_5_vigentes": fields[59],
        "cantidad_situaciones_6_vigentes": fields[60],
        "cantidad_refinanciaciones_vigentes": fields[61],
        "cantidad_situaciones_juridicas_vigentes": fields[62],
        "monto_adeudado_situaciones_1_vigentes": fields[63],
        "monto_adeudado_situaciones_2_vigentes": fields[64],
        "monto_adeudado_situaciones_3_vigentes": fields[65],
        "monto_adeudado_situaciones_4_vigentes": fields[66],
        "monto_adeudado_situaciones_5_vigentes": fields[67],
        "monto_adeudado_situaciones_6_vigentes": fields[68],
        "monto_adeudado_refinanciaciones_vigentes": fields[69],
        "monto_adeudado_situaciones_juridicas_vigentes": fields[70],
        "cantidad_situaciones_1_ult_6_meses": fields[71],
        "cantidad_situaciones_2_ult_6_meses": fields[72],
        "cantidad_situaciones_3_ult_6_meses": fields[73],
        "cantidad_situaciones_4_ult_6_meses": fields[74],
        "cantidad_situaciones_5_ult_6_meses": fields[75],
        "cantidad_situaciones_6_ult_6_meses": fields[76],
        "cantidad_refinanciaciones_ult_6_meses": fields[77],
        "cantidad_situaciones_juridicas_ult_6_meses": fields[78],
        "monto_adeudado_situaciones_1_ult_6_meses": fields[79],
        "monto_adeudado_situaciones_2_ult_6_meses": fields[80],
        "monto_adeudado_situaciones_3_ult_6_meses": fields[81],
        "monto_adeudado_situaciones_4_ult_6_meses": fields[82],
        "monto_adeudado_situaciones_5_ult_6_meses": fields[83],
        "monto_adeudado_situaciones_6_ult_6_meses": fields[84],
        "monto_adeudado_refinanciaciones_ult_6_meses": fields[85],
        "monto_adeudado_situaciones_juridicas_ult_6_meses": fields[86],
        "cantidad_situaciones_1_ult_12_meses": fields[87],
        "cantidad_situaciones_2_ult_12_meses": fields[88],
        "cantidad_situaciones_3_ult_12_meses": fields[89],
        "cantidad_situaciones_4_ult_12_meses": fields[90],
        "cantidad_situaciones_5_ult_12_meses": fields[91],
        "cantidad_situaciones_6_ult_12_meses": fields[92],
        "cantidad_refinanciaciones_ult_12_meses": fields[93],
        "cantidad_situaciones_juridicas_ult_12_meses": fields[94],
        "monto_adeudado_situaciones_1_ult_12_meses": fields[95],
        "monto_adeudado_situaciones_2_ult_12_meses": fields[96],
        "monto_adeudado_situaciones_3_ult_12_meses": fields[97],
        "monto_adeudado_situaciones_4_ult_12_meses": fields[98],
        "monto_adeudado_situaciones_5_ult_12_meses": fields[99],
        "monto_adeudado_situaciones_6_ult_12_meses": fields[100],
        "monto_adeudado_refinanciaciones_ult_12_meses": fields[101],
        "monto_adeudado_situaciones_juridicas_ult_12_meses": fields[102],
        "cantidad_situaciones_1_ult_24_meses": fields[103],
        "cantidad_situaciones_2_ult_24_meses": fields[104],
        "cantidad_situaciones_3_ult_24_meses": fields[105],
        "cantidad_situaciones_4_ult_24_meses": fields[106],
        "cantidad_situaciones_5_ult_24_meses": fields[107],
        "cantidad_situaciones_6_ult_24_meses": fields[108],
        "cantidad_refinanciaciones_ult_24_meses": fields[109],
        "cantidad_situaciones_juridicas_ult_24_meses": fields[110],
        "monto_adeudado_situaciones_1_ult_24_meses": fields[111],
        "monto_adeudado_situaciones_2_ult_24_meses": fields[112],
        "monto_adeudado_situaciones_3_ult_24_meses": fields[113],
        "monto_adeudado_situaciones_4_ult_24_meses": fields[114],
        "monto_adeudado_situaciones_5_ult_24_meses": fields[115],
        "monto_adeudado_situaciones_6_ult_24_meses": fields[116],
        "monto_adeudado_refinanciaciones_ult_24_meses": fields[117],
        "monto_adeudado_situaciones_juridicas_ult_24_meses": fields[118],
        "cantidad_deudas_en_ex_entidades_financieras": fields[119],
        "cantidad_sin_fondos_impagos_ult_3_meses": fields[120],
        "cantidad_sin_fondos_impagos_ult_6_meses": fields[121],
        "cantidad_sin_fondos_impagos_ult_12_meses": fields[122],
        "cantidad_sin_fondos_impagos_ult_24_meses": fields[123],
        "cantidad_sin_fondos_impagos_ult_60_meses": fields[124],
        "cantidad_sin_fondos_pagados_ult_3_meses": fields[125],
        "cantidad_sin_fondos_pagados_ult_6_meses": fields[126],
        "cantidad_sin_fondos_pagados_ult_12_meses": fields[127],
        "cantidad_sin_fondos_pagados_ult_24_meses": fields[128],
        "cheques_sin_fondos_pagados_dias_atraso_max": fields[129],
        "cantidad_sin_fondos_sin_pago_multa": fields[130],
        "monto_sin_fondos_impagos_ult_3_meses": fields[131],
        "monto_sin_fondos_impagos_ult_6_meses": fields[132],
        "monto_sin_fondos_impagos_ult_12_meses": fields[133],
        "monto_sin_fondos_impagos_ult_24_meses": fields[134],
        "monto_sin_fondos_impagos_ult_60_meses": fields[135],
        "monto_sin_fondos_pagados_ult_3_meses": fields[136],
        "monto_sin_fondos_pagados_ult_6_meses": fields[137],
        "monto_sin_fondos_pagados_ult_12_meses": fields[138],
        "monto_sin_fondos_pagados_ult_24_meses": fields[139],
        "monto_sin_fondos_sin_pago_multa": fields[140],
        "cantidad_defectos_formales_impagos_ult_3_meses": fields[141],
        "cantidad_defectos_formales_impagos_ult_6_meses": fields[142],
        "cantidad_defectos_formales_impagos_ult_12_meses": fields[143],
        "cantidad_defectos_formales_impagos_ult_24_meses": fields[144],
        "cantidad_defectos_formales_impagos_ult_60_meses": fields[145],
        "cantidad_defectos_formales_pagados_ult_3_meses": fields[146],
        "cantidad_defectos_formales_pagados_ult_6_meses": fields[147],
        "cantidad_defectos_formales_pagados_ult_12_meses": fields[148],
        "cantidad_defectos_formales_pagados_ult_24_meses": fields[149],
        "cantidad_defectos_formales_sin_pago_multa": fields[150],
        "monto_defectos_formales_impagos_ult_3_meses": fields[151],
        "monto_defectos_formales_impagos_ult_6_meses": fields[152],
        "monto_defectos_formales_impagos_ult_12_meses": fields[153],
        "monto_defectos_formales_impagos_ult_24_meses": fields[154],
        "monto_defectos_formales_impagos_ult_60_meses": fields[155],
        "monto_defectos_formales_pagados_ult_3_meses": fields[156],
        "monto_defectos_formales_pagados_ult_6_meses": fields[157],
        "monto_defectos_formales_pagados_ult_12_meses": fields[158],
        "monto_defectos_formales_pagados_ult_24_meses": fields[159],
        "cheques_defectos_formales_pagados_dias_atraso_max": fields[160],
        "monto_defectos_formales_sin_pago_multa": fields[161],
        "nombre_segun_id_recibido": fields[162],
        "alerta_morosidad_id_recibido": fields[163],
        "id_credixsa_(dni/cuil)": fields[164],
        "nombre_segun_id_credixsa": fields[165],
        "alerta_morosidad_id_credixsa": fields[166],
        "razon_social_alerta_laboral": fields[167],
        "domicilio_fiscal_alerta_laboral": fields[168],
        "telefono": fields[169],
        "actividad_principal_afip_alerta_laboral": fields[170],
        "cantidad_empleados_estimados_alerta_laboral": fields[171],
        "alerta_morosidad": fields[172],
        "cantidad_ult_5_dias": fields[173],
        "cantidad_ult_30_dias": fields[174],
        "cantidad_ult_5_dias_realizadas_por_otras_entidades": fields[175],
        "cantidad_ult_30_dias_realizadas_por_otras_entidades": fields[176],
        "cantidad_entidades_ult_5_dias": fields[177],
        "cantidad_entidades_ult_30_dias": fields[178],
        "alerta_fallecido": fields[179],
        "telefono_contacto_1": fields[180],
        "telefono_contacto_2": fields[181],
        "telefono_contacto_3": fields[182]
    }
    return data

'''
def reg_consulta(info_consulta: dict):
    error = None
    con, cur = get_db()
    try:
        cur.execute('INSERT INTO nombre_tabla () ' +
                    'VALUES ()', (info_consulta.get('tipo')))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error grabando registro de consulta: ' + str(E)}
    return error
'''