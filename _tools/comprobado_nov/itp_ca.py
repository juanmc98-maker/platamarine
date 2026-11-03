# -*- coding: utf-8 -*-
"""Guia ITP (CA): correccions després de la comprovació del 3 nov 2026 + data i fonts."""
f='ca/guias/itp-comprar-barco-usado-por-comunidad.html'
h=open(f,encoding='utf-8').read()
R=[
 ('i si el vaixell és nou o ve de fora d\'Espanya sense matricular, que és quan entra en joc l\'<a href="/ca/guias/impuesto-matriculacio',
  'i si el vaixell és nou, cas en què la compra porta IVA i, si fa més de 8 m, l\'<a href="/ca/guias/impuesto-matriculacio',1),
 ('<td>Cantàbria</td><td style="white-space:nowrap">4 % / 8 %</td><td>8 % si l&#x27;eslora supera els 8 m</td>',
  '<td>Cantàbria</td><td style="white-space:nowrap">8 %</td><td>Tipus general per a béns mobles, sense distinció per eslora</td>',1),
 ('<td>Castella-la Manxa</td><td>6 %</td><td></td>','<td>Castella-la Manxa</td><td>6 %</td><td>Confirma-ho a la seva agència tributària</td>',1),
 ('<td>Extremadura</td><td>6 %</td><td></td>','<td>Extremadura</td><td>6 %</td><td>Confirma-ho a la seva agència tributària</td>',1),
 ('<td>Navarra</td><td>4 %</td><td>Règim foral</td>','<td>Navarra</td><td>4 %</td><td>Règim foral; confirma-ho a la Hisenda Foral</td>',1),
 ('<td>País Basc</td><td>4 %</td><td>Règim foral (Àlaba, Biscaia, Guipúscoa)</td>','<td>País Basc</td><td>4 %</td><td>Règim foral (Àlaba, Biscaia, Guipúscoa); confirma-ho a la teva diputació</td>',1),
 ('<td>Ceuta i Melilla</td><td>2 %</td><td>Residents</td>','<td>Ceuta i Melilla</td><td>2 %</td><td>Residents; confirma-ho a l&#x27;Agència Tributària</td>',1),
 ('El mateix vaixell amb 7,99 m pagaria el 6 %: 3.600 €.','El mateix vaixell amb 7,99 m també pagaria el 8 %, perquè val més de 20.000 €: n\'hi ha prou que es compleixi una de les dues condicions.',1),
 ('amb caràcter general 30 dies hàbils des de la signatura; a Catalunya és un mes i a Andalusia dos mesos.','amb caràcter general 30 dies hàbils des de la signatura; a Catalunya i a les Illes Balears és un mes i a Andalusia dos mesos.',1),
 ('A Andalusia, Astúries, Cantàbria i la Comunitat Valenciana el tipus puja al 8 % a partir d\'aquesta eslora, i a València també per valor.',
  'A Andalusia, Astúries i la Comunitat Valenciana el tipus puja al 8 % per sobre de 8 m d\'eslora, i a València també si el vaixell val 20.000 € o més.',1),
 ('la venda porta IVA (21 %) i no ITP. Convé demanar factura.','la venda porta IVA i no ITP. Si és una compravenda que aplica el règim de béns usats (REBU), l\'IVA va inclòs en el preu i no apareix desglossat. Convé demanar factura.',2),
 ('(de l\'1 % mensual fins al 15 %, més interessos a partir d\'un any)','(un 1 % més un altre 1 % per cada mes complet de retard durant el primer any; a partir de 12 mesos, un 15 % més interessos de demora)',1),
 ('(de l&#x27;1 % mensual fins al 15 %, més interessos a partir d&#x27;un any)','(un 1 % més un altre 1 % per cada mes complet de retard durant el primer any; a partir de 12 mesos, un 15 % més interessos de demora)',1),
 ('<span>Actualitzat setembre 2026</span>','<span>Comprovat el 3 de novembre de 2026</span>',1),
 ('Informació fiscal orientativa, revisada el setembre de 2026 segons','Informació fiscal orientativa, comprovada el 3 de novembre de 2026 segons',1),
]
import re
for a,b,n in R:
    c=h.count(a)
    assert c>=1 and (n is None or c==n),(a[:50],c)
    h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Fonts oficials</strong> (comprovades el 3 de novembre de 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/no-residentes/impuesto-sobre-transmisiones-patrimoniales-actos-documentados/vehiculos-embarcaciones-recreo-aeronaves-usados620.html" target="_blank" rel="noopener">Agència Tributària: model 620, embarcacions usades</a></li>'
 '<li><a href="https://tramits.gencat.cat/ca/tramits/tramits-temes/ITPAJD-Transmissions-patrimonials-oneroses" target="_blank" rel="noopener">Generalitat de Catalunya: ITP, termini i presentació</a></li>'
 '<li><a href="https://atc.gencat.cat/web/.content/documents/02_doc_tributs/01_itpajd/guia_itp.pdf" target="_blank" rel="noopener">Agència Tributària de Catalunya: guia de l\'ITP</a></li>'
 '<li><a href="https://www.atib.es/ta/contenido.aspx?Id=5347&amp;lang=es" target="_blank" rel="noopener">ATIB (Illes Balears): termini i models</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-1998-8202" target="_blank" rel="noopener">BOE: Llei 13/1997 de la Comunitat Valenciana (tipus del 8 %)</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE: Ordre HAC/1501/2025, preus mitjans d\'embarcacions 2026</a></li>'
 '</ul></div>')
a='Confirma-ho amb la teva gestoria o amb l&#x27;Administració abans de comprar.</p>'
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
