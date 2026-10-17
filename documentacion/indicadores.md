# Contrato de indicadores · versión 2026

Todos los ejemplos numéricos siguientes pertenecen exclusivamente al generador artificial de semilla 20261016. No describen resultados de GHTOP. Los cálculos Python/SQL/JavaScript están probados; su equivalente DAX está preparado, con ejecución nativa pendiente.

| KPI | Numerador / cálculo | Base y filtros | Validación / límite |
|---|---|---|---|
| A Monto registrado | SUM(Monto a pagar) | Filas con hora de inicio | 5.133.000 CLP demo; no es cobro |
| A Cobro bruto confirmado demo | Suma del monto con estado Si | KEEPFILTERS estado; antes de comisión | 4.706.000 demo; sin conciliación bancaria |
| A Recibido neto canal | SUM(recibido) | Después de comisión artificial MP | No es neto sin IVA |
| A Horas | Suma duración por fila en horas | Hora término menos inicio | 630,5 h demo; no DATEDIFF entre mínimos del agregado |
| A Registros | COUNTROWS | Filas de uso | 429 demo; no COUNT de un campo de pago |
| A Reservas únicas demo | DISTINCTCOUNT ID | Solo ID sintético garantizado | No asumir clave histórica única |
| A Capacidad demo | SUM horas por cancha en calendario × COUNTROWS DimCancha | Filtro fecha y dimensión cancha/deporte | 4.368 h artificiales; no calendario real |
| A Utilización demo | Horas / capacidad demo | DIVIDE; ausencia si base 0 | 14,43% demo; exige filtro de dimensión |
| A Horas/día abierto | Horas / días abiertos de calendario | Incluye días abiertos sin reservas | No corrige causalidad ni meses completos |
| A Variación nov-dic | (229,5 – 215,5) / 215,5 | Ventanas fijas 2025; ignora filtro fecha, conserva cancha | 6,50% demo; totales de coberturas desiguales |
| B Monto positivo | SUM MONTO COBRADO > 0 | Universo tras exclusiones M; KEEPFILTERS | 6.235.000 demo; no flujo bancario auditado |
| B Monto con signo | SUM MONTO COBRADO | Incluye negativos del universo | 6.196.500 demo; diferencia 38.500 por negativos |
| B Movimientos | COUNTROWS | Después de excluir 15 filas RAW demo | 524 demo; no arriendos únicos |
| B Promedio positivo | Monto positivo / filas positivas | 432 filas positivas; cero/negativo fuera | 14.432,87 demo; no ticket transaccional |

Los conteos y sumas aditivas usan `COALESCE(..., 0)` para un contexto vacío, en coherencia con Python/SQL/JavaScript. Los cocientes conservan ausencia de base.

`DIVIDE` sin resultado alternativo retorna BLANK sin denominador; no convierte falta de base en desempeño cero. `KEEPFILTERS` preserva la intersección con filtros existentes. Las medidas de noviembre/diciembre eliminan solo Calendario y fijan año y mes: se titulan «ventana fija» para que no parezcan responder al segmentador temporal.

La comparación por total mensual no equivale a comparación de productividad: noviembre y enero A, marzo y junio B son parciales. Incluso normalizar por días abiertos de una demo no acredita días abiertos históricos. Los cierres inventados no se etiquetan como lluvia o feriados. No se atribuyen aumentos a promociones ni se presenta una mejora de rendimiento porcentual.

Prueba nativa futura: repetir controles totales, por mes, por deporte/línea y sin base contra `datos_compatibles/controles_esperados.json` y `tests/controles_web.json`, sin sumar promedios ni porcentajes de filas. Los totales deben recalcular sus numeradores y denominadores.

Referencias de lenguaje: [DIVIDE](https://learn.microsoft.com/en-us/dax/divide-function-dax), [KEEPFILTERS](https://learn.microsoft.com/en-us/dax/keepfilters-function-dax), [TMDL](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview).
