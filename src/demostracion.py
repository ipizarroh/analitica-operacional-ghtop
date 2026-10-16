"""Demostración posterior con datos inventados. Solo biblioteca estándar."""
import csv
import json
from collections import defaultdict
from datetime import date, timedelta
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def generar(inicio, fin, prefijo):
    inicio, fin = date.fromisoformat(inicio), date.fromisoformat(fin)
    filas = []
    dia = inicio
    while dia <= fin:
        for j in range(1 + (dia.day % 3)):
            n = len(filas) + 1
            filas.append({"id": f"{prefijo}-{n:04}", "fecha": dia.isoformat(),
                          "deporte": "Tenis" if n % 3 == 0 else "Pádel",
                          "horas": 1.0 if n % 2 else 1.5,
                          "monto_clp": 0 if n % 11 == 0 else 9000 + (n % 5) * 2000})
        dia += timedelta(days=2)
    return filas


def resumir(filas):
    ids = [f["id"] for f in filas]
    if len(ids) != len(set(ids)):
        raise ValueError("ID duplicado: no se puede asumir una fila por sesión")
    if any(float(f["horas"]) <= 0 for f in filas):
        raise ValueError("Duración no positiva")
    positivos = [f for f in filas if int(f["monto_clp"]) > 0]
    monto = sum(int(f["monto_clp"]) for f in positivos)
    return {"naturaleza": "SINTÉTICO POSTERIOR", "filas": len(filas),
            "filas_positivas": len(positivos), "monto_positivo_clp": monto,
            "promedio_positivo_clp": monto / len(positivos) if positivos else None,
            "horas": sum(float(f["horas"]) for f in filas)}


def dibujar(nombre, filas, titulo):
    s = resumir(filas)
    meses = defaultdict(float)
    for f in filas:
        meses[f["fecha"][:7]] += max(0,int(f["monto_clp"])) if nombre == "marzo_junio" else float(f["horas"])
    partes = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="660" viewBox="0 0 1200 660" role="img" aria-labelledby="titulo desc">',
              '<title id="titulo">Demostración sintética de uso de canchas</title>',
              '<desc id="desc">Datos enteramente inventados; horas por mes, registros e importes positivos.</desc>',
              '<rect width="1200" height="660" fill="#F3F6FA"/>']
    def texto(x,y,t,size=18,color="#16324F",bold=False):
        partes.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{size}" fill="{color}" font-weight="{"bold" if bold else "normal"}">{escape(str(t))}</text>')
    texto(40,46,'ANALÍTICA OPERACIONAL',16,'#146D78',True)
    texto(40,88,titulo,29,bold=True)
    texto(40,119,'DEMOSTRACIÓN SINTÉTICA POSTERIOR · fechas y magnitudes inventadas',16)
    tarjetas=[('Sesiones inventadas',str(s['filas'])),('Horas registradas',f"{s['horas']:.1f}"),('Monto positivo (CLP)',f"${s['monto_positivo_clp']:,}".replace(',','.'))]
    if nombre == 'marzo_junio':
        tarjetas=[('Registros positivos',s['filas_positivas']),('Promedio positivo (CLP)',f"${s['promedio_positivo_clp']:,.0f}".replace(',','.')),('Monto positivo (CLP)',f"${s['monto_positivo_clp']:,}".replace(',','.'))]
    for i,(et,val) in enumerate(tarjetas):
        x=40+i*378
        partes.append(f'<rect x="{x}" y="151" width="362" height="110" rx="12" fill="white"/>')
        texto(x+20,184,et,16);texto(x+20,230,val,30,bold=True)
    texto(40,310,'Monto positivo por mes de demostración' if nombre == 'marzo_junio' else 'Horas de uso por mes de demostración',21,bold=True)
    maximo=max(meses.values(),default=1)
    for i,(mes,horas) in enumerate(sorted(meses.items())):
        y=350+i*60;w=790*horas/maximo
        texto(40,y+23,mes,18)
        partes.append(f'<rect x="170" y="{y}" width="{w:.1f}" height="32" rx="4" fill="#146D78"/>')
        texto(185+w,y+23,f'${horas:,.0f}'.replace(',','.') if nombre == 'marzo_junio' else f'{horas:.1f} h',17)
    texto(40,612,'Fuente: generador incluido. No representa cifras ni resultados reales de GHTOP.',16)
    partes.append('</svg>')
    p=RAIZ/'imagenes'/f'{nombre}.svg';p.parent.mkdir(exist_ok=True);p.write_text('\n'.join(partes)+'\n')


def main():
    out=RAIZ/'datos_sinteticos';out.mkdir(exist_ok=True)
    casos=[('noviembre_enero','2030-11-04','2031-01-20','A','Uso de canchas · ejemplo noviembre a enero'),
           ('marzo_junio','2031-03-18','2031-06-12','B','Gestión comercial · ejemplo marzo a junio')]
    resultados={}
    for nombre,inicio,fin,prefijo,titulo in casos:
        filas=generar(inicio,fin,prefijo)
        with (out/f'{nombre}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['id','fecha','deporte','horas','monto_clp']);w.writeheader();w.writerows(filas)
        resultados[nombre]=resumir(filas);dibujar(nombre,filas,titulo)
    (out/'resumen.json').write_text(json.dumps(resultados,ensure_ascii=False,indent=2)+'\n')
    print('Dos muestras sintéticas y sus visualizaciones regeneradas.')

if __name__ == '__main__':
    main()
