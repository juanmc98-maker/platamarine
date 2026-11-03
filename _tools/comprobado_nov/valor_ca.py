# -*- coding: utf-8 -*-
"""Guia valor fiscal (CA): data de comprovació, nota de l'Ordre 2026 i fonts (3 nov 2026)."""
import re
f='ca/guias/valor-fiscal-barco-tablas-hacienda.html'
h=open(f,encoding='utf-8').read()
R=[("<span>Actualitzat l'octubre de 2026</span>",'<span>Comprovat el 3 de novembre de 2026</span>'),
   ("Informació orientativa, revisada l'octubre de 2026 a partir de",'Informació orientativa, comprovada el 3 de novembre de 2026 a partir de'),
   ("vigent des de l'1 de gener de 2026.","vigent des de l'1 de gener de 2026. Respecte a la del 2025, canvia els percentatges per anys d'ús de cascos i motors i inclou per primer cop els motors elèctrics marins.")]
for a,b in R:
    c=h.count(a); assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Fonts oficials</strong> (comprovades el 3 de novembre de 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE: Ordre HAC/1501/2025, preus mitjans 2026</a></li>'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/no-residentes/impuesto-sobre-transmisiones-patrimoniales-actos-documentados/vehiculos-embarcaciones-recreo-aeronaves-usados620.html" target="_blank" rel="noopener">Agència Tributària: model 620, embarcacions usades</a></li>'
 '<li><a href="https://atc.gencat.cat/web/.content/documents/02_doc_tributs/01_itpajd/guia_itp.pdf" target="_blank" rel="noopener">Agència Tributària de Catalunya: guia de l\'ITP</a></li>'
 '</ul></div>')
a="Ens podem equivocar i res d'aquesta pàgina és vinculant.</p>"
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
