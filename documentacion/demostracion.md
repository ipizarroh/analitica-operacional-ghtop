# Reproducción de datos, pruebas y visor

## Datos compatibles

`python src/generar_esquema.py --seed 20261016` genera JSON, CSV y controles. No lee fuentes privadas ni ajusta frecuencias a registros reales. Slots, probabilidades, tarifas, estados, identidades y cierres fueron elegidos para probar reglas. A contiene 429 filas; B 539 RAW y 524 tras filtros. Semilla distinta cambia datos, no el contrato; los controles y el HTML deben regenerarse juntos.

Los Excel tienen las hojas operativas y la posición de cabecera esperada, más CalendarioOperacion, Canchas y LEEME. Las fechas/horas son celdas numéricas con formato de fecha/hora; no cadenas que solo parecen fechas. Importes numéricos, clientes CLIENTE_FICTICIO, sin fórmulas privadas o vínculos externos. [Contratos A/B](../powerbi/modelos/) y `datos_compatibles/diccionario.csv` documentan campos y nulos.

## Exportar Excel

Los binarios entregados fueron creados con `@oai/artifact-tool`, recálculo e inspección, y leídos de forma independiente con openpyxl. `src/exportar_excel.mjs` reproduce la autoría cuando ese runtime está disponible:

```bash
node src/exportar_excel.mjs /ruta/a/evidencias_excel
```

Requiere que Node resuelva `@oai/artifact-tool` (runtime de autoría de Work); no se afirma que esté disponible mediante npm público. Esa dependencia limita la regeneración del formato XLSX fuera de ese entorno. Python/CSV/JSON y el visor sí son reproducibles con herramientas estándar. Para cambiar semilla y refrescar Power BI desde Excel, regenere también ambos XLSX en el runtime indicado. No renombre un CSV a XLSX.

## Pruebas

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
node tests/test_web.mjs
python src/construir_web.py
```

`test_esquema_completo.py`: integridad, economía, temporalidad, reproducibilidad con varios seeds, rechazo de defectos y SQL independiente para filtros/totales. `test_excel.py`: compara todas las filas XLSX con RAW JSON, tipos, cabeceras, dimensiones y ausencia de enlaces externos. `test_web.mjs`: 32 contextos y 208 valores contrastados con Python; no ejecuta M/DAX. La demo pequeña de la edición anterior queda en `src/demostracion.py` y `datos_sinteticos/`, separada del nuevo contrato completo.

Abra `demo/index.html` o el sitio público para usar filtros y detalle. La captura identifica su origen web. La publicación pública usa GitHub Pages con los mismos datos artificiales del repositorio; no contiene cargas o consultas externas.
