import assert from 'node:assert/strict';
import fs from 'node:fs';
import {calcular} from '../src/modelo_web.mjs';
const root=new URL('../',import.meta.url);
const casos=JSON.parse(fs.readFileSync(new URL('tests/controles_web.json',root),'utf8'));
const datos=JSON.parse(fs.readFileSync(new URL('datos_compatibles/fuentes_sinteticas.json',root),'utf8'));

let n=0;for(const c of casos){const r=calcular(datos,c.caso,c.periodo,c.categoria).k;for(const [k,v] of Object.entries(c.esperado)){if(typeof v==='number')assert.ok(Math.abs(r[k]-v)<1e-9,`${c.caso} ${c.periodo} ${c.categoria} ${k}: ${r[k]} != ${v}`);else assert.deepEqual(r[k],v);n++;}}
console.log(`${casos.length} contextos y ${n} conciliaciones JS/Python correctas; no ejecuta DAX.`);
