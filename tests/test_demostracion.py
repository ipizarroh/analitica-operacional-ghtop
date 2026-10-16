import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from demostracion import generar,resumir

class ControlesOperacionales(unittest.TestCase):
    def test_ticket_excluye_cero_y_negativos(self):
        filas=[{'id':str(i),'horas':1,'monto_clp':n} for i,n in enumerate([12000,18000,0,-1000])]
        s=resumir(filas)
        self.assertEqual((s['monto_positivo_clp'],s['filas_positivas'],s['promedio_positivo_clp']),(30000,2,15000))
    def test_ausencia_no_se_convierte_en_ticket_cero(self):
        self.assertIsNone(resumir([])['promedio_positivo_clp'])
        self.assertIsNone(resumir([{'id':'X','horas':1,'monto_clp':0}])['promedio_positivo_clp'])
    def test_clave_duplicada_se_rechaza(self):
        with self.assertRaises(ValueError):resumir([{'id':'X','horas':1,'monto_clp':1}]*2)
    def test_duracion_invalida_se_rechaza(self):
        with self.assertRaises(ValueError):resumir([{'id':'X','horas':-1,'monto_clp':1}])
    def test_cortes_y_reproducibilidad(self):
        f=generar('2031-03-18','2031-06-12','B')
        self.assertEqual(f,generar('2031-03-18','2031-06-12','B'))
        self.assertTrue(all('2031-03-18'<=x['fecha']<='2031-06-12' for x in f))
        self.assertEqual(len(f),len({x['id'] for x in f}))
    def test_conciliacion(self):
        f=generar('2030-11-04','2031-01-20','A');s=resumir(f)
        self.assertEqual(s['filas'],len(f));self.assertEqual(s['horas'],sum(x['horas'] for x in f))

if __name__=='__main__':unittest.main()
