# Noviembre de 2025 a enero de 2026

## Problema y preguntas

El registro de uso de canchas permitía analizar tenis y pádel, pero el nombre de un indicador no bastaba para conocer su alcance. Las preguntas de gestión eran cómo variaba la actividad, cuánto tiempo se utilizaban las canchas y qué importes se registraban por deporte.

## Participación y metodología acreditada

Desarrollé un informe Power BI con origen Excel, transformaciones Power Query y medidas DAX. El modelo disponible usa una tabla operacional y un calendario automático. La consulta promueve encabezados, asigna tipos, selecciona filas con hora de inicio y normaliza los códigos de cancha a deporte. La revisión técnica actual recuperó las expresiones y las contrastó con la fuente principal y dos versiones alternativas. Evidencias privadas G01–G08 y G15–G17.

El grano observado es una fila operacional retenida por la consulta. La presencia de identificadores repetidos impide asumir que un recuento distinto representa reservas únicas. Una fila incompleta queda fuera por la regla de hora de inicio; ese tratamiento se documenta y el original se conserva.

## Indicadores y límites

El monto total histórico suma el campo por pagar sin exigir un estado de pago afirmativo. Se denomina públicamente monto registrado. Las horas se obtienen de inicio y término mediante una columna y medidas documentadas. La variación entre noviembre y diciembre utiliza el mes sin fijar año y necesita revisar divisiones por cero antes de extenderse a otros períodos.

Los gráficos que cuentan un estado de pago informado también pueden contar estados negativos o gratuidades. Sirven para describir cobertura del registro, no para certificar cobros. Enero termina antes del fin del mes; no se añadió febrero.

## Resultado demostrado y rediseño posterior

Existe un proyecto auditable con análisis por deporte, mes, día y horario. No se publica su contenido privado. El rediseño posterior organiza resumen y operación en dos páginas, identifica CLP y horas, y sustituye el gráfico de clientes por una lectura agregada de uso. Las fórmulas históricas se preservan en la copia privada para evitar alterar la evidencia.

## Decisión y aprendizaje

El análisis puede orientar la programación de actividades hacia días de baja demanda. La decisión de realizar promociones corresponde al relato del autor; no se atribuye una mejora cuantificada. La lección transferible es definir la unidad de análisis y distinguir importe registrado, cobro y actividad antes de presentar resultados.
