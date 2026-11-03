# -*- coding: utf-8 -*-
"""Guía impuesto de matriculación (FR): mismas correcciones que la versión ES del 3 nov 2026 + fecha y fuentes."""
import re
f='fr/guias/impuesto-matriculacion-barcos.html'
h=open(f,encoding='utf-8').read()
R=[
 ('Ce n’est pas un hasard : à partir de 8 mètres de longueur, la première immatriculation en Espagne entraîne une taxe de 12 %.',
  'Ce n’est pas un hasard : au-delà de 8 mètres de longueur, la première immatriculation en Espagne entraîne une taxe de 12 %.'),
 ('Les véhicules nautiques à moteur (jet-skis) la paient toujours, quelle que soit leur longueur.</p>',
  'Les véhicules nautiques à moteur (jet-skis) la paient toujours, quelle que soit leur longueur, et à un taux différent : 14,75 %.</p>'),
 ('la base est la valeur de marché, que l’administration fiscale calcule à l’aide de ses barèmes officiels de valorisation des bateaux (un arrêté publié chaque année), ou le prix réel s’il est plus élevé.</p>',
  'la base est la valeur de marché ; vous pouvez vous appuyer sur les barèmes officiels de valorisation des bateaux (un arrêté publié chaque année), et l’administration fiscale peut contrôler cette valeur.</p>'),
 ('et si le prix réel est supérieur au barème, c’est le prix réel qui l’emporte.',
  'et l’administration fiscale peut contrôler la valeur que vous déclarez.'),
 ('<td>Bateau de plus de 8 m acheté dans un autre pays de l’UE</td><td>Oui, 12 % sur la valeur du barème</td>',
  '<td>Bateau de plus de 8 m acheté dans un autre pays de l’UE</td><td>Oui, 12 % : s’il est d’occasion, sur sa valeur de marché (barèmes) ; s’il est neuf, sur le prix hors TVA</td>'),
 ('seulement une déclaration d’exonération (formulaire 06).','seulement une déclaration de non-assujettissement (formulaire 06).'),
 ('<p>Ils ne paient pas, mais l’exonération n’est pas automatique : il faut déposer le formulaire 06',
  '<p>Ils ne paient pas, mais ce n’est pas automatique : il faut déposer la déclaration de non-assujettissement (formulaire 06)'),
 ('sur la valeur du bateau à cette date.',
  'sur la valeur du bateau à cette date, avec le formulaire 576 et dans un délai de 15 jours calendaires à compter du changement. L’exonération se perd aussi si le bateau est cédé plus de 3 mois par an à la même personne, ou si le propriétaire ou une personne liée à lui s’en réserve l’usage.'),
 ('<td>Autoliquidation lors du changement d’usage</td>','<td>Formulaire 576 dans les 15 jours suivant le changement d’usage</td>'),
 ('La longueur qui compte est celle qui figure dans les papiers du bateau (la longueur de coque sur la déclaration de conformité CE), et non la longueur hors tout incluant la plateforme de bain ou les balcons.',
  'La longueur qui compte est celle qui figure dans les papiers du bateau, et non la longueur hors tout incluant la plateforme de bain ou les balcons ; en cas de doute, demandez à la gestoría de la confirmer avec le certificat du bateau.'),
 ('<span>Mis à jour en septembre 2026</span>','<span>Vérifié le 3 novembre 2026</span>'),
 ('Information fiscale à titre indicatif, revue en septembre 2026 conformément à','Information fiscale à titre indicatif, vérifiée le 3 novembre 2026 conformément à'),
]
for a,b in R:
    c=h.count(a); assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Sources officielles</strong> (vérifiées le 3 novembre 2026) :</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-1992-28741" target="_blank" rel="noopener">BOE : loi 38/1992 sur les accises (art. 65 à 70)</a></li>'
 '<li><a href="https://www3.agenciatributaria.gob.es/static_files/Sede/Procedimiento_ayuda/G502/instr_mod576.pdf" target="_blank" rel="noopener">Agencia Tributaria : instructions du formulaire 576 (taux et base)</a></li>'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/vehiculos-embarcaciones/primera-matriculacion-medios-transporte/que-supuestos-puedo-estar-exento-transporte.html" target="_blank" rel="noopener">Agencia Tributaria : exonérations (location, formulaire 05)</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE : Orden HAC/1501/2025, prix moyens des bateaux 2026</a></li>'
 '</ul></div>')
a='Veuillez vérifier auprès d’une gestoría ou de l’administration fiscale avant d’acheter.</p>'
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
