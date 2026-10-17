export function calcular(d,c,mes='',cat='') {
 let rows=[], k,fecha,monto,categoria,cuenta,metricas=[];
 const sum=(r,k)=>r.reduce((s,x)=>s+Number(x[k]||0),0),ratio=(a,b)=>b?a/b:null;
 if(c==='A'||c==='B') {
  const p=d.proyectos[c];fecha=c==='A'?'Fecha':'FECHA';monto=c==='A'?'Monto a pagar':'MONTO COBRADO';categoria=c==='A'?'Cancha':'LINEA DE NEGOCIO';
  rows=p.registros.filter(x=>c==='A'?x['Hora inicio']!==null:x.FECHA&&x['LINEA DE NEGOCIO']!=='TIENDA'&&!['PAGO G3','COPA LITORAL'].includes(x['SUBLINEA DE NEGOCIO'])).map(x=>({...x,[categoria]:c==='A'?(x.Cancha.startsWith('Cancha P')?'Pádel':'Tenis'):x[categoria].replace('ESCALERILLA','ESCALERILLA TENIS')}));
  if(mes)rows=rows.filter(x=>x[fecha].slice(0,7)===mes);if(cat)rows=rows.filter(x=>x[categoria]===cat);
  const positivo=rows.filter(x=>x[monto]>0);k={filas:rows.length,monto_registrado:sum(rows,monto),monto_positivo:sum(positivo,monto),registros_positivos:positivo.length,ticket_positivo:ratio(sum(positivo,monto),positivo.length)};
  if(c==='A') {
   k.cobro_bruto_confirmado_demo=sum(rows.filter(x=>x['¿pagado¡']==='Si'),monto);k.horas=sum(rows,'Uso de cancha');
   k.horas_disponibles_sinteticas=sum(p.calendario.filter(x=>!mes||x.Fecha.slice(0,7)===mes),'Horas disponibles por cancha')*(cat?2:4);k.utilizacion_sintetica=ratio(k.horas,k.horas_disponibles_sinteticas);
   metricas=[['Monto registrado',k.monto_registrado,'clp','Incluye monto pendiente'],['Cobro confirmado demo',k.cobro_bruto_confirmado_demo,'clp','Estado Si; antes de comisión'],['Horas registradas',k.horas,'n','Duración por fila'],['Utilización simulada',k.utilizacion_sintetica,'pct',`${k.horas_disponibles_sinteticas} h de capacidad artificial`]];
  } else metricas=[['Monto positivo',k.monto_positivo,'clp',`${k.registros_positivos} registros positivos`],['Monto con signo',k.monto_registrado,'clp','Incluye movimientos negativos'],['Promedio por fila positiva',k.ticket_positivo,'clp','No ticket por transacción'],['Movimientos',k.filas,'n','No arriendos únicos']];
  return {k,metricas,rows,fecha,monto,categoria};
 }
 if(c==='F') {
  rows=d.FactSeguimiento.filter(x=>x.corte===mes&&(!cat||x.curso_id===cat));const cerradas=rows.filter(x=>x.curso_cerrado_al_corte),aprobadas=cerradas.filter(x=>x.estado==='Aprobado'),ids=new Set(rows.map(x=>x.persona_id)),crm=new Set(d.personas.filter(x=>x.registro_crm_demo).map(x=>x.persona_id));
  k={inscripciones:rows.length,personas:ids.size,inscripciones_curso_cerrado:cerradas.length,aprobadas_curso_cerrado:aprobadas.length,aprobacion_curso_cerrado:ratio(aprobadas.length,cerradas.length),personas_con_crm_demo:[...ids].filter(x=>crm.has(x)).length};k.cobertura_crm_demo=ratio(k.personas_con_crm_demo,k.personas);
  metricas=[['Personas únicas',k.personas,'n','No sumables entre cursos'],['Inscripciones al corte',k.inscripciones,'n','Una fila por inscripción y corte'],['Aprobación · cursos cerrados',k.aprobacion_curso_cerrado,'pct',`${aprobadas.length} / ${cerradas.length} inscripciones elegibles`],['Cobertura CRM demo',k.cobertura_crm_demo,'pct',`${k.personas_con_crm_demo} / ${k.personas} personas ficticias`]];
  return {k,metricas,rows,fecha:'corte',categoria:'estado',monto:null};
 }
 rows=d.FactJornada.filter(x=>(!mes||x.fecha===mes)&&(!cat||x.programa_id===cat));const presentes=rows.filter(x=>x.estado==='Presente').length,ausentes=rows.filter(x=>x.estado==='Ausente').length,sin=rows.filter(x=>x.estado==='Sin registro').length;
 k={jornadas_esperadas:rows.length,registros_recibidos:presentes+ausentes,presentes,ausentes,sin_registro:sin,cobertura:ratio(presentes+ausentes,rows.length),asistencia_observada:ratio(presentes,presentes+ausentes),asistencia_sobre_esperadas:ratio(presentes,rows.length)};
 metricas=[['Cobertura del registro',k.cobertura,'pct',`${k.registros_recibidos} / ${k.jornadas_esperadas} jornadas`],['Asistencia observada',k.asistencia_observada,'pct',`${presentes} presentes / ${k.registros_recibidos} recibidas`],['Sin registro',sin,'n','Faltante no equivale a ausencia'],['Jornadas esperadas',rows.length,'n','Matrícula vigente × días abiertos']];return {k,metricas,rows,fecha:'fecha',categoria:'estado',monto:null};
}
