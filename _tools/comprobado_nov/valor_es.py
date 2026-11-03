# -*- coding: utf-8 -*-
"""Guía valor fiscal (ES): fecha de comprobación, nota de la Orden 2026 y fuentes (3 nov 2026)."""
import re
f='guias/valor-fiscal-barco-tablas-hacienda.html'
h=open(f,encoding='utf-8').read()
R=[('<span>Actualizado octubre 2026</span>','<span>Comprobado el 3 de noviembre de 2026</span>'),
   ('Información orientativa, revisada en octubre de 2026 a partir de','Información orientativa, comprobada el 3 de noviembre de 2026 a partir de'),
   ('en vigor desde el 1 de enero de 2026.','en vigor desde el 1 de enero de 2026. Respecto a la de 2025, cambia los porcentajes por años de uso de cascos y motores e incluye por primera vez los motores eléctricos marinos.')]
for a,b in R:
    c=h.count(a); assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Fuentes oficiales</strong> (comprobadas el 3 de noviembre de 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE: Orden HAC/1501/2025, precios medios 2026</a></li>'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/no-residentes/impuesto-sobre-transmisiones-patrimoniales-actos-documentados/vehiculos-embarcaciones-recreo-aeronaves-usados620.html" target="_blank" rel="noopener">Agencia Tributaria: modelo 620, embarcaciones usadas</a></li>'
 '<li><a href="https://atc.gencat.cat/web/.content/documents/02_doc_tributs/01_itpajd/guia_itp.pdf" target="_blank" rel="noopener">Agència Tributària de Catalunya: guía del ITP</a></li>'
 '</ul></div>')
a='Podemos equivocarnos y nada de esta página es vinculante.</p>'
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
