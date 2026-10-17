# Verificación de la fase 2

Las pruebas son reproducibles desde un clon limpio. Consulte los comandos del README. Python/SQL validan reglas y agregados de los datos artificiales; JavaScript contrasta los cálculos del visor con expectativas Python. El workflow de GitHub ejecuta esas mismas pruebas en cada cambio. Los resultados remotos y capturas se documentan tras la publicación.

Power Query, DAX y los candidatos PBIP requieren validación en Power BI Desktop. No se ejecutaron Desktop, Performance Analyzer ni DAX Studio en Linux. Ningún test JSON/PBIR ni la vista web sustituye apertura, refresh, filtros, guardado y reapertura nativos. No se presenta mejora de rendimiento medida.

La auditoría privada compara términos e identificadores de fuentes, revisa archivos y contenido XLSX, bloquea rutas personales, secretos y originales y revisa los blobs del historial Git. Es un control técnico y revisión de contenido, no una certificación legal. La fuente histórica privada no se publica.

## Evidencia ejecutada

- 14 tests Python aprobados; Excel completo incluido en GHTOP y SQL independiente en ambos.
- Paridad web: 32 contextos / 208 valores.
- [GitHub Actions](https://github.com/ipizarroh/analitica-operacional-ghtop/actions/runs/38985000723): ejecución remota de contratos, calidad, paridad y regeneración HTML.
- Visor HTTPS revisado en navegador: total A, mes/deporte, detalle, total B y GASTO sin base positiva. Capturas en `imagenes/` y expectativas en `tests/controles_web.json`.

Los archivos DAX/M se revisan como fuentes preparados. La ausencia de ejecución nativa sigue siendo una limitación material: no afirmar que estos tests los compilan o validan sus contextos en el motor Power BI.
