# -*- coding: utf-8 -*-
"""Guia impost de matriculació (CA): correccions del 3 nov 2026 + data i fonts."""
import re
f='ca/guias/impuesto-matriculacion-barcos.html'
h=open(f,encoding='utf-8').read()
R=[
 ("No és casualitat: a partir de 8 metres d'eslora, la primera matriculació a Espanya paga un 12 % d'impost.",
  "No és casualitat: per sobre de 8 metres d'eslora, la primera matriculació a Espanya paga un 12 % d'impost."),
 ("Les motos d'aigua el paguen sempre, sigui quina sigui l'eslora.</p>",
  "Les motos d'aigua el paguen sempre, sigui quina sigui l'eslora, i a un tipus diferent: el 14,75 %.</p>"),
 ("la base és el valor de mercat, i Hisenda el calcula amb les seves taules oficials de valoració d'embarcacions (una ordre que es publica cada any) o amb el preu real si és superior.</p>",
  "la base és el valor de mercat; pots fer servir les taules oficials de valoració d'embarcacions (una ordre que es publica cada any) i Hisenda pot comprovar aquest valor.</p>"),
 ("i si el preu real és més gran que la taula, mana el preu real.",
  "i Hisenda pot comprovar el valor que declaris."),
 ('<td>Vaixell de més de 8 m comprat en un altre país de la UE</td><td>Sí, 12 % sobre valor de taules</td>',
  '<td>Vaixell de més de 8 m comprat en un altre país de la UE</td><td>Sí, 12 %: si és usat, sobre el seu valor de mercat (taules); si és nou, sobre el preu sense IVA</td>'),
 ('<td>Ex-xàrter que passa a ús privat abans de 4 anys</td><td>Sí, sobre el valor actual</td><td>Autoliquidació en canviar d\'ús</td>',
  '<td>Ex-xàrter que passa a ús privat abans de 4 anys</td><td>Sí, sobre el valor actual</td><td>Model 576 en 15 dies des del canvi d\'ús</td>'),
 ("només es presenta una declaració d'exempció (model 06).","només es presenta una declaració de no subjecció (model 06)."),
 ("<p>No paguen, però l'exempció no és automàtica: cal presentar el model 06","<p>No paguen, però no és automàtic: cal presentar la declaració de no subjecció (model 06)"),
 ("sobre el valor que tingui el vaixell aleshores.","sobre el valor que tingui el vaixell aleshores, amb el model 576 i en un termini de 15 dies naturals des del canvi. L'exempció també es perd si el vaixell es cedeix més de 3 mesos en un any a la mateixa persona, o si el titular o algú vinculat a ell se'n reserva l'ús."),
 ("L'eslora que compta és la que figura a la documentació del vaixell (l'eslora de casc de la declaració de conformitat CE), no l'eslora total amb plataforma de bany o púlpits.",
  "L'eslora que compta és la que figura a la documentació del vaixell, no l'eslora total amb plataforma de bany o púlpits; si tens dubtes, que la gestoria la confirmi amb el certificat del vaixell."),
 ('<span>Actualitzat setembre 2026</span>','<span>Comprovat el 3 de novembre de 2026</span>'),
 ('Informació fiscal orientativa, revisada el setembre de 2026 segons','Informació fiscal orientativa, comprovada el 3 de novembre de 2026 segons'),
]
for a,b in R:
    c=h.count(a); assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Fonts oficials</strong> (comprovades el 3 de novembre de 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-1992-28741" target="_blank" rel="noopener">BOE: Llei 38/1992 d\'Impostos Especials (arts. 65 a 70)</a></li>'
 '<li><a href="https://www3.agenciatributaria.gob.es/static_files/Sede/Procedimiento_ayuda/G502/instr_mod576.pdf" target="_blank" rel="noopener">Agència Tributària: instruccions del model 576 (tipus i base)</a></li>'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/vehiculos-embarcaciones/primera-matriculacion-medios-transporte/que-supuestos-puedo-estar-exento-transporte.html" target="_blank" rel="noopener">Agència Tributària: exempcions (lloguer, model 05)</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE: Ordre HAC/1501/2025, preus mitjans d\'embarcacions 2026</a></li>'
 '</ul></div>')
a="Confirma-ho amb la teva gestoria o amb l'Administració abans de comprar.</p>"
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
