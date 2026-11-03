# -*- coding: utf-8 -*-
"""Guía ITP (ES): correcciones tras la comprobación del 3 nov 2026 + fecha y fuentes."""
f='guias/itp-comprar-barco-usado-por-comunidad.html'
h=open(f,encoding='utf-8').read()
R=[
 ('y si el barco es nuevo o viene de fuera de España sin matricular, que es cuando entra en juego el <a href="/guias/impuesto-matriculacio',
  'y si el barco es nuevo, en cuyo caso la compra lleva IVA y, si mide más de 8 m, el <a href="/guias/impuesto-matriculacio',1),
 ('<td>Cantabria</td><td style="white-space:nowrap">4 % / 8 %</td><td>8 % si la eslora supera los 8 m</td>','<td>Cantabria</td><td style="white-space:nowrap">8 %</td><td>Tipo general para bienes muebles, sin distinción por eslora</td>',1),
 ('<td>Castilla-La Mancha</td><td>6 %</td><td></td>','<td>Castilla-La Mancha</td><td>6 %</td><td>Confírmalo en su agencia tributaria</td>',1),
 ('<td>Extremadura</td><td>6 %</td><td></td>','<td>Extremadura</td><td>6 %</td><td>Confírmalo en su agencia tributaria</td>',1),
 ('<td>Navarra</td><td>4 %</td><td>Régimen foral</td>','<td>Navarra</td><td>4 %</td><td>Régimen foral; confírmalo en Hacienda Foral</td>',1),
 ('<td>País Vasco</td><td>4 %</td><td>Régimen foral (Álava, Bizkaia, Gipuzkoa)</td>','<td>País Vasco</td><td>4 %</td><td>Régimen foral (Álava, Bizkaia, Gipuzkoa); confírmalo en tu diputación</td>',1),
 ('<td>Ceuta y Melilla</td><td>2 %</td><td>Residentes</td>','<td>Ceuta y Melilla</td><td>2 %</td><td>Residentes; confírmalo en la Agencia Tributaria</td>',1),
 ('El mismo barco con 7,99 m pagaría el 6 %: 3.600 €.','El mismo barco con 7,99 m también pagaría el 8 %, porque vale más de 20.000 €: basta con cumplir una de las dos condiciones.',1),
 ('con carácter general 30 días hábiles desde la firma; en Cataluña es un mes y en Andalucía dos meses.','con carácter general 30 días hábiles desde la firma; en Cataluña y en Baleares es un mes y en Andalucía dos meses.',1),
 ('En Andalucía, Asturias, Cantabria y la Comunidad Valenciana el tipo sube al 8 % a partir de esa eslora, y en Valencia también por valor.','En Andalucía, Asturias y la Comunidad Valenciana el tipo sube al 8 % por encima de 8 m de eslora, y en Valencia también si el barco vale 20.000 € o más.',1),
 ('la venta lleva IVA (21 %) y no ITP. Conviene pedir factura.','la venta lleva IVA y no ITP. Si es una compraventa que aplica el régimen de bienes usados (REBU), el IVA va incluido en el precio y no aparece desglosado. Conviene pedir factura.',None),
 ('(del 1 % mensual hasta el 15 %, más intereses a partir de un año)','(un 1 % más otro 1 % por cada mes completo de retraso durante el primer año; a partir de 12 meses, un 15 % más intereses de demora)',None),
 ('<span>Actualizado septiembre 2026</span>','<span>Comprobado el 3 de noviembre de 2026</span>',1),
 ('Información fiscal orientativa, revisada en septiembre de 2026 según','Información fiscal orientativa, comprobada el 3 de noviembre de 2026 según',1),
]
import re
for a,b,n in R:
    c=h.count(a)
    assert c>=1 and (n is None or c==n),(a[:50],c)
    h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Fuentes oficiales</strong> (comprobadas el 3 de noviembre de 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/no-residentes/impuesto-sobre-transmisiones-patrimoniales-actos-documentados/vehiculos-embarcaciones-recreo-aeronaves-usados620.html" target="_blank" rel="noopener">Agencia Tributaria: modelo 620, embarcaciones usadas</a></li>'
 '<li><a href="https://tramits.gencat.cat/ca/tramits/tramits-temes/ITPAJD-Transmissions-patrimonials-oneroses" target="_blank" rel="noopener">Generalitat de Catalunya: ITP, plazo y presentación</a></li>'
 '<li><a href="https://atc.gencat.cat/web/.content/documents/02_doc_tributs/01_itpajd/guia_itp.pdf" target="_blank" rel="noopener">Agència Tributària de Catalunya: guía del ITP</a></li>'
 '<li><a href="https://www.atib.es/ta/contenido.aspx?Id=5347&amp;lang=es" target="_blank" rel="noopener">ATIB (Baleares): plazo y modelos</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-1998-8202" target="_blank" rel="noopener">BOE: Ley 13/1997 de la Comunitat Valenciana (tipo del 8 %)</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE: Orden HAC/1501/2025, precios medios de embarcaciones 2026</a></li>'
 '</ul></div>')
a='Confírmalo con tu gestoría o con la Administración antes de comprar.</p>'
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
