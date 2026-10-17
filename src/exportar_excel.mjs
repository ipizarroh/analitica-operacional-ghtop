import fs from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const datos=JSON.parse(await fs.readFile(`${repo}/datos_compatibles/fuentes_sinteticas.json`,'utf8'));
const evidencia=path.resolve(process.argv[2]??'evidencias/excel');
await fs.mkdir(evidencia,{recursive:true});
const serialFecha = s => (Date.parse(s+'T00:00:00Z')-Date.UTC(1899,11,30))/86400000;
const serialHora = s => s==null ? null : s.split(':').reduce((a,v,i)=>a+Number(v)/(24*60**i),0);

for(const caso of ['A','B']){
  const p=datos.proyectos[caso], wb=Workbook.create();
  const sheet=wb.worksheets.add(p.hoja);
  const ncols=caso==='A'?39:21;
  const headers=[...p.cabeceras];
  while(headers.length<ncols)headers.push(`Column${headers.length+1}`);
  const rows=p.registros.map(r=>headers.map(k=>{
    const v=r[k]??null;
    if(k==='Fecha'||k==='FECHA')return serialFecha(v);
    if(['Hora inicio','Hora termino','HORA INICIO','HORA FIN'].includes(k))return serialHora(v);
    return v;
  }));
  let offset=0;
  if(caso==='B'){
    sheet.getRange('A1').values=[['REGISTRO OPERACIONAL SINTÉTICO - DEMOSTRACIÓN 2026']];
    offset=1;
  }
  sheet.getRangeByIndexes(offset,0,rows.length+1,ncols).values=[headers,...rows];
  sheet.getRangeByIndexes(0,0,rows.length+offset+1,p.cabeceras.length).format.font={name:'Arial',size:10,color:'#18354B'};
  sheet.getRangeByIndexes(offset,0,1,p.cabeceras.length).format={fill:'#18354B',font:{name:'Arial',bold:true,color:'#FFFFFF'},rowHeight:44,wrapText:true};
  sheet.getRangeByIndexes(offset+1,0,rows.length,p.cabeceras.length).format.rowHeight=21;
  sheet.getRangeByIndexes(0,0,rows.length+offset+1,p.cabeceras.length).format.columnWidth=19;
  for(let i=0;i<p.cabeceras.length;i++){
    const h=p.cabeceras[i],r=sheet.getRangeByIndexes(offset+1,i,rows.length,1);
    if(h==='Fecha'||h==='FECHA')r.setNumberFormat('yyyy-mm-dd');
    if(['Hora inicio','Hora termino','HORA INICIO','HORA FIN'].includes(h))r.setNumberFormat('hh:mm');
    if(caso==='A'&&[10,13,14,15,16].includes(i)||caso==='B'&&[11,12,13,14,15,16].includes(i))r.setNumberFormat('"$"#,##0.00');
  }
  sheet.getRangeByIndexes(0,caso==='A'?8:10,rows.length+offset+1,1).format.columnWidth=30;
  sheet.showGridLines=false;sheet.freezePanes.freezeRows(offset+1);
  const cal=wb.worksheets.add('CalendarioOperacion');
  const ch=['Fecha','Abierto','Horas disponibles por cancha','Motivo'];
  const cr=p.calendario.map(r=>[serialFecha(r.Fecha),r.Abierto,r['Horas disponibles por cancha'],r.Motivo]);
  cal.getRangeByIndexes(0,0,cr.length+1,4).values=[ch,...cr];
  cal.getRange(`A2:A${cr.length+1}`).setNumberFormat('yyyy-mm-dd');
  const courts=wb.worksheets.add('Canchas');
  courts.getRange('A1:B5').values=[['Cancha','Deporte'],...p.cancha.map(r=>[r.Cancha,r.Deporte])];
  const readme=wb.worksheets.add('LEEME');
  readme.getRange('A1:B8').values=[['Contrato','Fuente sintética compatible'],['Proyecto',caso],['Período',`${p.inicio} a ${p.fin}`],['Semilla',datos.seed],['Origen','Generador incluido; ningún registro real'],['Cierres','Hipótesis simuladas; no son lluvia ni feriados reales'],['Uso','Entrada de demostración; no evidencia de resultados comerciales'],['Importación','Power Query: hoja principal, calendario y canchas']];
  for(const s of [cal,courts,readme]){
    s.showGridLines=false;s.getUsedRange().format.font={name:'Arial',size:10,color:'#18354B'};
    s.getUsedRange().format.columnWidth=25;s.getUsedRange().format.rowHeight=24;
    s.getRangeByIndexes(0,0,1,s===cal?4:2).format={fill:'#18354B',font:{name:'Arial',bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true};
  }
  cal.getRange('C1:C1').format.columnWidth=29;cal.getRange(`D1:D${cr.length+1}`).format.columnWidth=26;
  readme.getRange('B1:B8').format.columnWidth=82;
  wb.recalculate();
  const scan=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#N/A',options:{useRegex:true,maxResults:30},maxChars:1000});
  await fs.writeFile(`${evidencia}/inspeccion_${caso}.txt`,scan.ndjson);
  for(const [name,range,label] of [[p.hoja,caso==='A'?'A1:I8':'A1:K9','fuente_1'],[p.hoja,caso==='A'?'J1:Q8':'L2:R9','fuente_2'],['CalendarioOperacion','A1:D9','calendario'],['Canchas','A1:B5','canchas'],['LEEME','A1:B8','leeme']]){
    const img=await wb.render({sheetName:name,range,scale:1.3,format:'png'});
    await fs.writeFile(`${evidencia}/${caso}_${label}.png`,new Uint8Array(await img.arrayBuffer()));
  }
  const output=await SpreadsheetFile.exportXlsx(wb);
  await output.save(`${repo}/datos_compatibles/GHTOP_${caso}_sintetico.xlsx`);
  console.log(caso,rows.length,'filas,',ncols,'columnas; exportado');
}
