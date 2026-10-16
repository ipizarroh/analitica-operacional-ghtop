# Marzo a junio de 2026

## Problema y necesidad

La fuente reúne distintas líneas de negocio. Para comparar actividad y montos es necesario distinguir qué operaciones entran en cada visual y cómo se calcula el ticket. Marzo y junio tienen cobertura parcial: sus totales no representan meses completos.

## Participación y método

Desarrollé reportería comercial en Power BI sobre un registro Excel distinto del período anterior. La consulta disponible promueve dos filas de encabezados, tipa columnas, selecciona fechas informadas y excluye la tienda y dos conceptos de eventos. También normaliza una línea de actividad. La revisión actual contrastó los filtros M, las medidas y los recuentos con la hoja seleccionada. Evidencias privadas G09–G14 y G17.

El grano es un movimiento del registro, no una transacción bancaria conciliada ni una reserva única. Hay clases y actividades además de arriendos. Las visuales cambian de universo cuando se seleccionan líneas y sublíneas.

## Definiciones que cambian la lectura

La medida histórica de ingresos cobrados suma solamente importes positivos. El ticket general divide esa suma por el número de filas positivas, con resultado alternativo cero. Por tanto, se interpreta como promedio por registro positivo, no gasto por cliente ni ticket de una reserva única.

Algunas tablas suman importes con signo, mientras la tarjeta excluye los no positivos. La diferencia entre ambas puede estar justificada por la definición y debe explicarse. Los gráficos que cuentan un texto de empresa se presentan como registros con empresa informada. Esa cuenta no acredita número de arriendos cuando el universo incluye otras actividades.

## Entregable y resultado demostrado

El proyecto disponible contiene segmentadores, análisis temporal, comparación entre líneas y ticket. El rediseño posterior añade jerarquía visual, formato CLP y dos páginas con filtros independientes. Se mantienen las reglas históricas y se registran sus límites; no se fusiona con el primer modelo.

## Uso para gestión y mejoras pendientes

Una lectura útil combina montos positivos, cantidad de registros y cobertura de fechas. Antes de comparar desempeño por día debe definirse si se mide monto, movimientos o duración, y si existe un denominador de días abiertos. No se estimó ocupación sobre capacidad disponible, porque esa disponibilidad no está acreditada.

Falta comprobar la copia rediseñada en Desktop: actualización, gráficos, contexto de segmentadores y totales. La demostración pública inventada ilustra controles actuales y no completa esos vacíos históricos.
