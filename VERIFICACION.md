# Qué se ha verificado

- Generadores Python ejecutados localmente con biblioteca estándar.
- Pruebas de denominadores, claves, filtros y reproducibilidad mediante `unittest`.
- CSV y resultados regenerables sin ninguna fuente privada.
- Visualizaciones SVG nuevas, con rótulo sintético y revisión visual.
- Revisión de archivos candidatos y de todos los objetos del historial Git antes de publicación.

No se ejecutaron DAX ni Power Query en Power BI Desktop. Los ejemplos de `powerbi/` son código posterior para importar manualmente y validar. Las imágenes SVG son salidas de Python, no capturas de un informe Power BI abierto. Este repositorio no contiene PBIX ni PBIP históricos.

Ejecutar desde la raíz:

```bash
python src/demostracion.py
python -m unittest discover -s tests -v
```

No se necesitan paquetes externos. Los archivos generados permanecen separados de la evidencia histórica. Para revisar una propuesta DAX/M se deben verificar tipos, contexto de filtro y totales en Desktop antes de utilizarla.
