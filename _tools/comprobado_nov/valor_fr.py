# -*- coding: utf-8 -*-
"""Guía valor fiscal (FR): fecha de comprobación, nota sobre el arrêté 2026 y fuentes (3 nov 2026)."""
import re
f='fr/guias/valor-fiscal-barco-tablas-hacienda.html'
h=open(f,encoding='utf-8').read()
R=[('<span>Mis à jour en octobre 2026</span>','<span>Vérifié le 3 novembre 2026</span>'),
   ("Information indicative, revue en octobre 2026 sur la base de","Information indicative, vérifiée le 3 novembre 2026 sur la base de"),
   ('en vigueur depuis le 1er janvier 2026.</p>','en vigueur depuis le 1er janvier 2026. Par rapport à celui de 2025, il modifie les pourcentages par années d’utilisation des coques et des moteurs et inclut pour la première fois les moteurs électriques marins.</p>')]
for a,b in R:
    c=h.count(a); assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Sources officielles</strong> (vérifiées le 3 novembre 2026) :</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE : Orden HAC/1501/2025, prix moyens 2026</a></li>'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/no-residentes/impuesto-sobre-transmisiones-patrimoniales-actos-documentados/vehiculos-embarcaciones-recreo-aeronaves-usados620.html" target="_blank" rel="noopener">Agencia Tributaria : formulaire 620, bateaux d’occasion</a></li>'
 '<li><a href="https://atc.gencat.cat/web/.content/documents/02_doc_tributs/01_itpajd/guia_itp.pdf" target="_blank" rel="noopener">Agència Tributària de Catalunya : guide de l’ITP</a></li>'
 '</ul></div>')
a="Nous pouvons nous tromper et rien sur cette page n'est contractuel.</p>"
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
