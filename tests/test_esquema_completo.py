import unittest, sys, copy, json, sqlite3
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from generar_esquema import generar, transformar, metricas, COLUMNAS_A, COLUMNAS_B
from calidad import validar


class EsquemaCompleto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=generar()

    def test_contrato_reglas_integridad_economia(self):self.assertEqual(validar(self.d),[])

    def test_reproducibilidad_y_semilla(self):
        self.assertEqual(self.d,generar(20261016));self.assertNotEqual(self.d,generar(20261017))
        for seed in [0,1,731,20261017]:self.assertEqual(validar(generar(seed)),[])

    def test_archivo_publicado_es_generacion_exacta(self):
        p=Path(__file__).resolve().parents[1]/'datos_compatibles/fuentes_sinteticas.json'
        self.assertEqual(json.loads(p.read_text()),self.d)

    def test_totales_independientes_con_sql_y_filtros(self):
        # SQLite recibe RAW y ejecuta por separado las exclusiones; no llama al ETL Python.
        for caso,p in self.d['proyectos'].items():
            db=sqlite3.connect(':memory:')
            db.execute('create table f(fecha text,categoria text,monto real,pago text,linea text,sub text)')
            for r in p['registros']:
                x=(r['Fecha'], 'Pádel' if 'P' in r['Cancha'] else 'Tenis',r['Monto a pagar'],r['¿pagado¡'],'','') if caso=='A' else (r['FECHA'],r['LINEA DE NEGOCIO'].replace('ESCALERILLA','ESCALERILLA TENIS'),r['MONTO COBRADO'],'',r['LINEA DE NEGOCIO'],r['SUBLINEA DE NEGOCIO'])
                db.execute('insert into f values(?,?,?,?,?,?)',x)
            meses=sorted({r['Fecha' if caso=='A' else 'FECHA'][:7] for r in p['registros']})
            for mes in [None,*meses,'2099-01']:
                for cat in [None,'Tenis','Pádel'] if caso=='A' else [None,'TENIS','PADEL','GASTO','SIN FILAS']:
                    where=['1=1'];params=[]
                    if caso=='B':where+=["linea <> 'TIENDA'","sub not in ('PAGO G3','COPA LITORAL')"]
                    if mes:where+=['substr(fecha,1,7)=?'];params.append(mes)
                    if cat:where+=['categoria=?'];params.append(cat)
                    n,total,pos,positivas=db.execute('select count(*),coalesce(sum(monto),0),coalesce(sum(case when monto>0 then monto else 0 end),0),sum(case when monto>0 then 1 else 0 end) from f where '+' and '.join(where),params).fetchone()
                    got=metricas(caso,self.d,mes,cat)
                    self.assertEqual((got['filas'],got['monto_registrado'],got['monto_positivo']),(n,total,pos))
                    if positivas:self.assertAlmostEqual(got['ticket_positivo'],pos/positivas)
                    else:self.assertIsNone(got['ticket_positivo'])
            db.close()

    def test_regresion_conciliacion_raw_modelo(self):
        self.assertEqual(len(self.d['proyectos']['A']['registros']),429)
        self.assertEqual(len(self.d['proyectos']['B']['registros']),539)
        self.assertEqual(len(transformar('B',self.d['proyectos']['B']['registros'])),524)
        self.assertEqual(metricas('A',self.d)['monto_registrado'],5133000)
        self.assertEqual(metricas('A',self.d)['cobro_bruto_confirmado_demo'],4706000)
        self.assertEqual(metricas('A',self.d)['horas'],630.5)
        self.assertEqual(metricas('B',self.d)['monto_positivo'],6235000)
        self.assertEqual(metricas('B',self.d)['monto_registrado'],6196500)

    def test_mutaciones_son_bloqueadas(self):
        for campo,valor,codigo in [('Cliente','persona@ejemplo.test','CLIENTE_ARTIFICIAL'),('Uso de cancha',99,'DURACION'),('recibido',-100,'CONCILIACION_COBRO'),('Cancha','Cancha privada','FK_CANCHA')]:
            d=copy.deepcopy(self.d);d['proyectos']['A']['registros'][0][campo]=valor
            self.assertIn(codigo,{x['regla'] for x in validar(d)})
        d=copy.deepcopy(self.d);d['proyectos']['A']['registros'].append(d['proyectos']['A']['registros'][0]);self.assertIn('CLAVE_UNICA',{x['regla'] for x in validar(d)})

    def test_capacidad_depende_de_filtro_no_de_existencia_de_reserva(self):
        total=metricas('A',self.d,'2025-11');tenis=metricas('A',self.d,'2025-11','Tenis');padel=metricas('A',self.d,'2025-11','Pádel')
        self.assertEqual(total['horas_disponibles_sinteticas'],1512)
        self.assertEqual(tenis['horas_disponibles_sinteticas']+padel['horas_disponibles_sinteticas'],1512)
        self.assertAlmostEqual(total['horas'],tenis['horas']+padel['horas'])

if __name__=='__main__':unittest.main()
