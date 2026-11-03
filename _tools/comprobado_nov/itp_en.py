# -*- coding: utf-8 -*-
"""ITP guide (EN): corrections from the 3 Nov 2026 check + date and sources."""
import re
f='en/guias/itp-comprar-barco-usado-por-comunidad.html'
h=open(f,encoding='utf-8').read()
R=[
 ('and when the boat is new or comes from outside Spain unregistered, which is when the <a href="/en/guias/impuesto-matriculacion-barcos">registration tax</a> comes into play.',
  'and when the boat is new, in which case the purchase carries VAT and, if it is over 8 m long, the <a href="/en/guias/impuesto-matriculacion-barcos">registration tax</a>.',1),
 ('<td>Cantabria</td><td style="white-space:nowrap">4 % / 8 %</td><td>8 % if the boat is over 8 m long</td>',
  '<td>Cantabria</td><td style="white-space:nowrap">8 %</td><td>General rate for movable goods, no distinction by length</td>',1),
 ('<td>Castilla-La Mancha</td><td>6 %</td><td></td>','<td>Castilla-La Mancha</td><td>6 %</td><td>Check with its tax agency</td>',1),
 ('<td>Extremadura</td><td>6 %</td><td></td>','<td>Extremadura</td><td>6 %</td><td>Check with its tax agency</td>',1),
 ('<td>Navarre</td><td>4 %</td><td>Regional (foral) tax regime</td>','<td>Navarre</td><td>4 %</td><td>Regional (foral) tax regime; check with the Navarre tax office</td>',1),
 ('<td>Basque Country</td><td>4 %</td><td>Regional (foral) regime (Álava, Bizkaia, Gipuzkoa)</td>','<td>Basque Country</td><td>4 %</td><td>Regional (foral) regime (Álava, Bizkaia, Gipuzkoa); check with your provincial tax office</td>',1),
 ('<td>Ceuta and Melilla</td><td>2 %</td><td>Residents</td>','<td>Ceuta and Melilla</td><td>2 %</td><td>Residents; check with the national tax agency</td>',1),
 ('The same boat at 7.99 m would pay 6 %: €3,600.','The same boat at 7.99 m would also pay 8 %, because it is worth more than €20,000: meeting either of the two conditions is enough.',1),
 ('generally 30 working days from signing; in Catalonia it is one month and in Andalusia two months.','generally 30 working days from signing; in Catalonia and the Balearic Islands it is one month and in Andalusia two months.',1),
 ('In Andalusia, Asturias, Cantabria and the Valencia region the rate rises to 8 % above that length, and in Valencia also by value.','In Andalusia, Asturias and the Valencia region the rate rises to 8 % above 8 m in length, and in Valencia also if the boat is worth €20,000 or more.',1),
 ('the sale carries 21 % VAT and no ITP. Ask for an invoice.','the sale carries VAT and no ITP. If it is a dealer using the margin scheme for second-hand goods (REBU), the VAT is included in the price and not shown separately. Ask for an invoice.',None),
 ('(from 1 % per month up to 15 %, plus interest after a year)','(1 % plus another 1 % for each full month of delay during the first year; after 12 months, 15 % plus late-payment interest)',None),
 ('<span>Updated September 2026</span>','<span>Checked on 3 November 2026</span>',1),
 ('Indicative tax information, reviewed in September 2026 under','Indicative tax information, checked on 3 November 2026 under',1),
]
for a,b,n in R:
    c=h.count(a)
    if c==0 and h.count(b)>=1: continue  # already applied
    assert c>=1 and (n is None or c==n),(a[:50],c)
    h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Official sources</strong> (checked on 3 November 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/no-residentes/impuesto-sobre-transmisiones-patrimoniales-actos-documentados/vehiculos-embarcaciones-recreo-aeronaves-usados620.html" target="_blank" rel="noopener">Spanish Tax Agency: form 620, used boats</a></li>'
 '<li><a href="https://tramits.gencat.cat/ca/tramits/tramits-temes/ITPAJD-Transmissions-patrimonials-oneroses" target="_blank" rel="noopener">Generalitat de Catalunya: ITP, deadline and filing</a></li>'
 '<li><a href="https://atc.gencat.cat/web/.content/documents/02_doc_tributs/01_itpajd/guia_itp.pdf" target="_blank" rel="noopener">Catalan Tax Agency: ITP guide</a></li>'
 '<li><a href="https://www.atib.es/ta/contenido.aspx?Id=5347&amp;lang=es" target="_blank" rel="noopener">ATIB (Balearic Islands): deadline and forms</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-1998-8202" target="_blank" rel="noopener">BOE: Valencian Law 13/1997 (8 % rate)</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE: Order HAC/1501/2025, average boat prices for 2026</a></li>'
 '</ul></div>')
a='Confirm with your tax adviser or the tax office before buying.</p>'
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
