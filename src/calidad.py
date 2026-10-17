"""Contrato y controles bloqueantes de los datos artificiales. Sin datos privados."""
from datetime import date, time
from collections import defaultdict
import re
from generar_esquema import COLUMNAS_A, COLUMNAS_B, CANCHAS, transformar


def minutos(t):
    x=time.fromisoformat(t)
    return x.hour*60+x.minute+x.second/60


def validar(datos):
    errores=[]
    def regla(ok,codigo,caso,fila=None):
        if not ok:errores.append({'regla':codigo,'caso':caso,'fila':fila})
    for caso,p in datos['proyectos'].items():
        columnas=COLUMNAS_A if caso=='A' else COLUMNAS_B
        fecha='Fecha' if caso=='A' else 'FECHA';inicio='Hora inicio' if caso=='A' else 'HORA INICIO';fin='Hora termino' if caso=='A' else 'HORA FIN'
        clave='ID arriendocancha' if caso=='A' else 'ID movimiento (demo)';cliente='Cliente' if caso=='A' else 'CLIENTE';cancha='Cancha' if caso=='A' else 'CANCHA'
        calendario={x['Fecha']:x for x in p['calendario']};ids=set();slots=defaultdict(list)
        regla(len(calendario)==len(p['calendario']),'CALENDARIO_UNICO',caso)
        regla(len(calendario)==(date.fromisoformat(p['fin'])-date.fromisoformat(p['inicio'])).days+1,'CALENDARIO_CONTIGUO',caso)
        for i,r in enumerate(p['registros']):
            regla(list(r)==columnas,'ESQUEMA_ORDENADO',caso,i)
            regla(r[clave] not in ids,'CLAVE_UNICA',caso,i);ids.add(r[clave])
            regla(bool(re.fullmatch(caso+r'_SIM_\d{6}',r[clave])),'ID_ARTIFICIAL',caso,i)
            regla(r[fecha] in calendario,'FK_FECHA',caso,i)
            if r[fecha] not in calendario:continue
            regla(calendario[r[fecha]]['Abierto'],'SIN_MOVIMIENTOS_EN_CIERRE',caso,i)
            regla(r[cliente] is None or bool(re.fullmatch(r'CLIENTE_FICTICIO_\d{4}',r[cliente])),'CLIENTE_ARTIFICIAL',caso,i)
            regla(r[cancha] is None or r[cancha] in {c['Cancha'] for c in CANCHAS},'FK_CANCHA',caso,i)
            if r[inicio] is not None and r[fin] is not None:
                a,b=minutos(r[inicio]),minutos(r[fin]);regla(480<=a<b<=1320,'HORARIO_VALIDO',caso,i)
                slots[(r[fecha],r[cancha])].append((a,b))
                if caso=='A':regla(abs((b-a)/60-r['Uso de cancha'])<1e-9,'DURACION',caso,i)
            else:regla(caso=='B' and r[cancha] is None,'NULOS_HORARIO_JUSTIFICADOS',caso,i)
            if caso=='A':
                bruto=r['Monto a pagar'] if r['¿pagado¡']=='Si' else 0
                regla(r['¿pagado¡'] in ['Si','No','Juego gratis'],'ENUM_PAGO',caso,i)
                regla(r['Monto a pagar']>=0 and (r['¿pagado¡']!='Juego gratis' or r['Monto a pagar']==0),'MONTO_ESTADO',caso,i)
                regla(abs(r['recibido']+r['Comisión mercago pago']-bruto)<0.011,'CONCILIACION_COBRO',caso,i)
                neto,iva=r['Neto Sin IVA'],r['IVA (19%)']
            else:
                bruto=r['MONTO COBRADO'];neto,iva=r['NETO SIN IVA'],r['IVA']
                recibido=r['EFECTIVO RECIBIDO']+r['MONTO RECIBIDO MP']
                regla(abs(recibido-bruto)<0.011 or abs(recibido-round(bruto*.98,2))<0.011,'CONCILIACION_CANAL_DEMO',caso,i)
                regla(r['EMPRESA']=='EMPRESA_FICTICIA','EMPRESA_ARTIFICIAL',caso,i)
            regla(abs(neto+iva-bruto)<0.011,'CONCILIACION_NETO_IVA',caso,i)
            for v in r.values():
                if isinstance(v,str):regla('@' not in v and not re.search(r'https?://|[A-Z]:\\Users\\',v),'SIN_CONTACTOS_RUTAS',caso,i)
        for intervalos in slots.values():
            orden=sorted(intervalos)
            regla(all(a[1]<=b[0] for a,b in zip(orden,orden[1:])),'SIN_SOLAPAMIENTO',caso)
        f=transformar(caso,p['registros'])
        if caso=='B':regla(all(r['LINEA DE NEGOCIO']!='TIENDA' and r['SUBLINEA DE NEGOCIO'] not in ['PAGO G3','COPA LITORAL'] for r in f),'EXCLUSIONES_ETL',caso)
    return errores
