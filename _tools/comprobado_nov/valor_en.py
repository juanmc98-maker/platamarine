# -*- coding: utf-8 -*-
"""Tax value guide (EN): check date, note on the 2026 Order and sources (3 Nov 2026)."""
import re
f='en/guias/valor-fiscal-barco-tablas-hacienda.html'
h=open(f,encoding='utf-8').read()
R=[('<span>Updated October 2026</span>','<span>Checked on 3 November 2026</span>'),
   ('For guidance only, reviewed in October 2026 based on','For guidance only, checked on 3 November 2026 based on'),
   ('in force since 1 January 2026.</p>','in force since 1 January 2026. Compared with the 2025 Order, it changes the percentages by years of use for hulls and engines, and for the first time it includes electric marine engines.</p>')]
for a,b in R:
    c=h.count(a)
    if c==0 and h.count(b)==1: continue  # already applied
    assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Official sources</strong> (checked on 3 November 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE: Order HAC/1501/2025, average prices for 2026</a></li>'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/no-residentes/impuesto-sobre-transmisiones-patrimoniales-actos-documentados/vehiculos-embarcaciones-recreo-aeronaves-usados620.html" target="_blank" rel="noopener">Spanish Tax Agency: form 620, used boats</a></li>'
 '<li><a href="https://atc.gencat.cat/web/.content/documents/02_doc_tributs/01_itpajd/guia_itp.pdf" target="_blank" rel="noopener">Catalan Tax Agency: ITP guide</a></li>'
 '</ul></div>')
a='We may be wrong and nothing on this page is binding.</p>'
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
