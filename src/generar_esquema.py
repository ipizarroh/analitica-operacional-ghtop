"""Reconstrucción 2026: datos artificiales compatibles con los dos esquemas.

No lee ni requiere fuentes privadas. Los importes, frecuencias y cierres se inventan.
"""
from pathlib import Path
from datetime import date, timedelta
from collections import defaultdict
import random, json, csv, argparse, hashlib

RAIZ=Path(__file__).resolve().parents[1]
COLUMNAS_A=["ID arriendocancha","Fecha","Día semana","Hora inicio","Hora termino","Uso de cancha","Cancha","Donde pagó","Cliente","Uso de luz artificial(Si/No)","Monto a pagar","¿pagado¡","Pagado en ","IVA (19%)","Comisión mercago pago","recibido","Neto Sin IVA"]
COLUMNAS_B=["FECHA","MES","DIA","EMPRESA","HORA INICIO","HORA FIN","LINEA DE NEGOCIO","SUBLINEA DE NEGOCIO","DETALLE","CANCHA","CLIENTE","MONTO COBRADO","EFECTIVO RECIBIDO","MONTO RECIBIDO MP","IVA","NETO SIN IVA","Participación administración (demo)","ID movimiento (demo)"]
DIAS=["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
CANCHAS=[{"Cancha":"Cancha T1","Deporte":"Tenis"},{"Cancha":"Cancha T2","Deporte":"Tenis"},{"Cancha":"Cancha P1","Deporte":"Pádel"},{"Cancha":"Cancha P2","Deporte":"Pádel"}]
PERIODOS={"A":("2025-11-03","2026-01-23"),"B":("2026-03-17","2026-06-19")}


def calendario(inicio,fin):
    a,b=date.fromisoformat(inicio),date.fromisoformat(fin);out=[]
    while a<=b:
        # Hipótesis artificial: un cierre cada 23 días de la muestra. No es clima real.
        abierto=len(out)%23!=11
        out.append({"Fecha":a.isoformat(),"Abierto":abierto,"Horas disponibles por cancha":14 if abierto else 0,"Motivo":"Abierto simulado" if abierto else "Cierre simulado", "Cobertura parcial":a.day!=1 if len(out)==0 else False})
        a+=timedelta(days=1)
    return out


def generar(seed=20261016):
    rng=random.Random(seed);result={"naturaleza":"SINTÉTICO DESDE CERO", "seed":seed,"hipotesis":{"horario":"08:00 a 22:00","comision_demo":0.02,"participacion_demo":0.15,"cierres":"artificiales; no corresponden a lluvias ni feriados reales"},"proyectos":{}}
    for caso,(inicio,fin) in PERIODOS.items():
        cal=calendario(inicio,fin);rows=[]
        for day in cal:
            if not day['Abierto']:continue
            fecha=date.fromisoformat(day['Fecha'])
            for cancha in CANCHAS:
                for hora in [8,11,15,19]:
                    if rng.random()>0.35:continue
                    duracion=rng.choice([60,90,120]);finmin=hora*60+duracion
                    iniciohora=f"{hora:02}:00:00";finhora=f"{finmin//60:02}:{finmin%60:02}:00"
                    cliente=f"CLIENTE_FICTICIO_{rng.randrange(1,49):04}"
                    tarifa=8000 if cancha['Deporte']=='Tenis' else 10000
                    precio=tarifa*duracion//60
                    estado=rng.choices(['Si','No','Juego gratis'],weights=[8,1,1])[0]
                    if estado=='Juego gratis':precio=0
                    canal=rng.choice(['EFECTIVO DEMO','MP DEMO']) if estado=='Si' else None
                    bruto=precio if estado=='Si' else 0
                    comision=round(bruto*0.02,2) if canal=='MP DEMO' else 0
                    iva=round(bruto-bruto/1.19,2);neto=round(bruto/1.19,2)
                    if caso=='A':
                        row=dict(zip(COLUMNAS_A,[f'A_SIM_{len(rows)+1:06}',day['Fecha'],DIAS[fecha.weekday()],iniciohora,finhora,duracion/60,cancha['Cancha'],canal,cliente,'Si' if hora>=19 else 'No',precio,estado,canal,iva,comision,round(bruto-comision,2),neto]))
                    else:
                        linea=cancha['Deporte'].upper().replace('Á','A');sub='ARRIENDO'
                        if linea=='TENIS' and rng.random()<0.2:linea='ESCALERILLA';sub='PARTIDO SIMULADO'
                        row=dict(zip(COLUMNAS_B,[day['Fecha'],fecha.strftime('%Y-%m'),DIAS[fecha.weekday()],'EMPRESA_FICTICIA',iniciohora,finhora,linea,sub,'Sesión artificial',cancha['Cancha'],cliente,bruto,bruto if canal=='EFECTIVO DEMO' else 0,round(bruto-comision,2) if canal=='MP DEMO' else 0,iva,neto,round(neto*0.15,2),f'B_SIM_{len(rows)+1:06}']))
                    rows.append(row)
            if caso=='B' and fecha.day%7==0:
                for linea in ['CLASES','ACADEMIA','ESCUELITA','TIENDA','GASTO']:
                    monto=-3500 if linea=='GASTO' else rng.choice([16000,24000,32000]);neto=round(monto/1.19,2);iva=round(monto-neto,2)
                    rows.append(dict(zip(COLUMNAS_B,[day['Fecha'],fecha.strftime('%Y-%m'),DIAS[fecha.weekday()],'EMPRESA_FICTICIA',None,None,linea,'CONCEPTO SIMULADO','Movimiento artificial sin reserva de cancha',None,None,monto,monto,0,iva,neto,round(neto*0.15,2),f'B_SIM_{len(rows)+1:06}'])))
            if caso=='B' and fecha.day==20:
                for sub in ['PAGO G3','COPA LITORAL']:
                    rows.append(dict(zip(COLUMNAS_B,[day['Fecha'],fecha.strftime('%Y-%m'),DIAS[fecha.weekday()],'EMPRESA_FICTICIA',None,None,'TENIS',sub,'Exclusión artificial de prueba',None,None,5000,5000,0,round(5000-5000/1.19,2),round(5000/1.19,2),0,f'B_SIM_{len(rows)+1:06}'])))
        result['proyectos'][caso]={"inicio":inicio,"fin":fin,"hoja":"Arriendos de cancha" if caso=='A' else "REGISTRO","cabeceras":COLUMNAS_A if caso=='A' else COLUMNAS_B,"cancha":CANCHAS,"calendario":cal,"registros":rows}
    return result


def transformar(caso,filas):
    if caso=='A':
        out=[]
        for r in filas:
            if r['Hora inicio'] is None:continue
            n=dict(r);n['Cancha original']=r['Cancha'];n['Cancha']='Pádel' if r['Cancha'].startswith('Cancha P') else 'Tenis';out.append(n)
        return out
    out=[]
    for r in filas:
        if not r['FECHA'] or r['LINEA DE NEGOCIO']=='TIENDA' or r['SUBLINEA DE NEGOCIO'] in ['PAGO G3','COPA LITORAL']:continue
        n=dict(r);n['LINEA DE NEGOCIO']=r['LINEA DE NEGOCIO'].replace('ESCALERILLA','ESCALERILLA TENIS');out.append(n)
    return out


def metricas(caso,datos,mes=None,categoria=None):
    p=datos['proyectos'][caso];r=transformar(caso,p['registros']);fecha='Fecha' if caso=='A' else 'FECHA';cat='Cancha' if caso=='A' else 'LINEA DE NEGOCIO';monto='Monto a pagar' if caso=='A' else 'MONTO COBRADO'
    if mes:r=[x for x in r if x[fecha][:7]==mes]
    if categoria:r=[x for x in r if x[cat]==categoria]
    suma=sum(x[monto] for x in r);positivos=[x for x in r if x[monto]>0]
    out={'filas':len(r),'monto_registrado':suma,'monto_positivo':sum(x[monto] for x in positivos),'registros_positivos':len(positivos),'ticket_positivo':sum(x[monto] for x in positivos)/len(positivos) if positivos else None}
    if caso=='A':
        out['cobro_bruto_confirmado_demo']=sum(x[monto] for x in r if x['¿pagado¡']=='Si')
        out['horas']=sum(x['Uso de cancha'] for x in r)
        c=[d for d in p['calendario'] if not mes or d['Fecha'][:7]==mes];ncancha=2 if categoria else 4
        out['horas_disponibles_sinteticas']=sum(d['Horas disponibles por cancha'] for d in c)*ncancha
        out['utilizacion_sintetica']=out['horas']/out['horas_disponibles_sinteticas'] if out['horas_disponibles_sinteticas'] else None
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seed',type=int,default=20261016);args=parser.parse_args();datos=generar(args.seed)
    out=RAIZ/'datos_compatibles';out.mkdir(exist_ok=True)
    (out/'fuentes_sinteticas.json').write_text(json.dumps(datos,ensure_ascii=False,indent=2)+'\n')
    for c,p in datos['proyectos'].items():
        with (out/f'proyecto_{c}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=p['cabeceras'],lineterminator='\n');w.writeheader();w.writerows(p['registros'])
    controles={c:{'total':metricas(c,datos),'meses':{m:metricas(c,datos,m) for m in sorted({r['Fecha' if c=='A' else 'FECHA'][:7] for r in p['registros']})}} for c,p in datos['proyectos'].items()}
    (out/'controles_esperados.json').write_text(json.dumps(controles,ensure_ascii=False,indent=2)+'\n')
    print('Registros sintéticos:',{c:len(p['registros']) for c,p in datos['proyectos'].items()})

if __name__=='__main__':main()
