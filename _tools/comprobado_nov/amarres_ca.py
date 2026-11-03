# -*- coding: utf-8 -*-
"""Guia amarratges (CA): correccions del 3 nov 2026 (T0, Arenys, Port Olímpic 12 m, Palamós 2027) + data i fonts."""
import re
f='ca/guias/amarres-cataluna-tipos-precios-alquiler-compra.html'
h=open(f,encoding='utf-8').read()
R=[
 ('Per a vaixells a motor de 9 metres o més (12 en vela), 9,12 euros per metre quadrat l\'any, i gairebé tots els ports la facturen a part.',
  'Per a vaixells a motor de 9 metres o més (en vela, de més de 12 metres), 9,12 euros per metre quadrat l\'any. Els vaixells a motor de menys de 9 metres paguen una sola vegada 22,80 euros per metre quadrat, amb validesa indefinida. Gairebé tots els ports la facturen a part.'),
 ('<td data-l="Trànsit per dia (8 m / 12 m)">17 € / 33 € temporada baixa</td><td data-l="Què inclou">IVA inclòs · més entrada de soci (3.000 €) i quota (95 €/mes)</td>',
  '<td data-l="Trànsit per dia (8 m / 12 m)">21 € / 33 € temporada baixa</td><td data-l="Què inclou">IVA inclòs · TA5 i T0 a part · més entrada de soci (3.000 €) i quota (95 €/mes)</td>'),
 ('<td data-l="Base anual, uns 12 m">≈ 7.050 €</td>','<td data-l="Base anual, uns 12 m">≈ 7.146 €</td>'),
 ('IVA no inclòs · càlcul per m²: 9,18 €/m²/mes més 2,50 €/m²/mes de comunitat i 10 €/mes d\'aigua i llum</td>',
  'IVA no inclòs · càlcul per m²: fins a 10 m, 9,18 €/m²/mes més 2,50 €/m²/mes de comunitat i 10 €/mes d\'aigua i llum; de 10 a 14 m, 9,49 €/m²/mes i 20 €/mes</td>'),
 ('Marina Palamós<small>tarifa 2026</small>','Marina Palamós<small>tarifa 2026 · la del 2027 ja està publicada (≈ +4,7 %)</small>'),
 ('<td data-l="Trànsit per dia (8 m / 12 m)">27 € / 48 € temporada baixa</td><td data-l="Què inclou">IVA i taxa inclosos</td>',
  '<td data-l="Trànsit per dia (8 m / 12 m)">27 € / 48 € temporada baixa</td><td data-l="Què inclou">IVA i TA5 inclosos · T0 a part</td>'),
 ('<span>Setembre 2026</span>','<span>Comprovat el 3 de novembre de 2026</span>'),
]
for a,b in R:
    c=h.count(a); assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Fonts oficials</strong> (normativa i tarifes de Ports de la Generalitat, Arenys, Sant Feliu, Port Olímpic i Marina Palamós comprovades el 3 de novembre de 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2020-443" target="_blank" rel="noopener">BOE: Llei 10/2019 de ports de Catalunya</a></li>'
 '<li><a href="https://ports.gencat.cat/en/taxes/" target="_blank" rel="noopener">Ports de la Generalitat: taxes 2026</a></li>'
 '<li><a href="https://www.boe.es/eli/es/rd/1999/04/16/607/con" target="_blank" rel="noopener">BOE: Reial decret 607/1999, assegurança de responsabilitat civil</a></li>'
 '<li><a href="https://portolimpic.barcelona/ca/serveis-portuaris/tarifes" target="_blank" rel="noopener">Port Olímpic: tarifes</a></li>'
 '</ul></div>')
i=h.find('<p class="aviso">Fonts:'); j=h.find('</p>',i)+4
assert i>0
if 'class="fuentes"' not in h: h=h[:j]+'\n        '+FU+h[j:]
open(f,'w',encoding='utf-8').write(h); print('ok',f)
