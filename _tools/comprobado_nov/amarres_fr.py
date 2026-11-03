# -*- coding: utf-8 -*-
"""Guía amarres (FR): mismas correcciones que la versión ES del 3 nov 2026 (T0, Arenys, Port Olímpic 12 m, Palamós 2027) + fecha y fuentes."""
import re
f='fr/guias/amarres-cataluna-tipos-precios-alquiler-compra.html'
h=open(f,encoding='utf-8').read()
R=[
 ('Pour les bateaux à moteur de 9 mètres ou plus (12 pour les voiliers), 9,12 euros par mètre carré et par an, et presque tous les ports la facturent à part.',
  'Pour les bateaux à moteur de 9 mètres ou plus (pour les voiliers, de plus de 12 mètres), 9,12 euros par mètre carré et par an. Les bateaux à moteur de moins de 9 mètres paient une seule fois 22,80 euros par mètre carré, valable sans limite de durée. Presque tous les ports la facturent à part.'),
 ('<td data-l="Escale par jour (8 m / 12 m)">17 € / 33 € basse saison</td><td data-l="Ce qui est inclus">TVA incluse · plus droit d’entr',
  '<td data-l="Escale par jour (8 m / 12 m)">21 € / 33 € basse saison</td><td data-l="Ce qui est inclus">TVA incluse · TA5 et T0 en sus · plus droit d’entr'),
 ('<td data-l="Annuel basé, ~12 m">≈ 7 050 €</td>','<td data-l="Annuel basé, ~12 m">≈ 7 146 €</td>'),
 ('TVA non incluse · calculé au m² : 9,18 €/m²/mois plus 2,50 €/m²/mois de charges de copropriété et 10 €/mois d’eau et d’électricité</td>',
  'TVA non incluse · calculé au m² : jusqu’à 10 m, 9,18 €/m²/mois plus 2,50 €/m²/mois de charges de copropriété et 10 €/mois d’eau et d’électricité ; de 10 à 14 m, 9,49 €/m²/mois et 20 €/mois</td>'),
 ('Marina Palamós<small>tarif 2026</small>','Marina Palamós<small>tarif 2026 · celui de 2027 est déjà publié (≈ +4,7 %)</small>'),
 ('<td data-l="Escale par jour (8 m / 12 m)">27 € / 48 € basse saison</td><td data-l="Ce qui est inclus">TVA et redevance incluses</td>',
  '<td data-l="Escale par jour (8 m / 12 m)">27 € / 48 € basse saison</td><td data-l="Ce qui est inclus">TVA et TA5 incluses · T0 en sus</td>'),
 ('<span>Septembre 2026</span>','<span>Vérifié le 3 novembre 2026</span>'),
]
for a,b in R:
    c=h.count(a); assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Sources officielles</strong> (réglementation et tarifs de Ports de la Generalitat, Arenys, Sant Feliu, Port Olímpic et Marina Palamós vérifiés le 3 novembre 2026) :</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2020-443" target="_blank" rel="noopener">BOE : loi 10/2019 sur les ports de Catalogne</a></li>'
 '<li><a href="https://ports.gencat.cat/en/taxes/" target="_blank" rel="noopener">Ports de la Generalitat : redevances 2026</a></li>'
 '<li><a href="https://www.boe.es/eli/es/rd/1999/04/16/607/con" target="_blank" rel="noopener">BOE : Real Decreto 607/1999, assurance responsabilité civile</a></li>'
 '<li><a href="https://portolimpic.barcelona/ca/serveis-portuaris/tarifes" target="_blank" rel="noopener">Port Olímpic : tarifs</a></li>'
 '</ul></div>')
i=h.find('<p class="aviso">Sources :'); j=h.find('</p>',i)+4
assert i>0
if 'class="fuentes"' not in h: h=h[:j]+'\n        '+FU+h[j:]
open(f,'w',encoding='utf-8').write(h); print('ok',f)
