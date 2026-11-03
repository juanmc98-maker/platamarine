# -*- coding: utf-8 -*-
"""Guía amarres (ES): correcciones del 3 nov 2026 (T0, Arenys, Port Olímpic 12 m, Palamós 2027) + fecha y fuentes."""
import re
f='guias/amarres-cataluna-tipos-precios-alquiler-compra.html'
h=open(f,encoding='utf-8').read()
R=[
 ('Para barcos a motor de 9 metros o más (12 en vela), 9,12 euros por metro cuadrado al año, y casi todos los puertos la facturan aparte.',
  'Para barcos a motor de 9 metros o más (en vela, de más de 12 metros), 9,12 euros por metro cuadrado al año. Los barcos a motor de menos de 9 metros pagan una sola vez 22,80 euros por metro cuadrado, con validez indefinida. Casi todos los puertos la facturan aparte.'),
 ('<td data-l="Tránsito por día (8 m / 12 m)">17 € / 33 € temporada baja</td><td data-l="Qué incluye">IVA incluido · más entrada de socio (3.000 €) y cuota (95 €/mes)</td>',
  '<td data-l="Tránsito por día (8 m / 12 m)">21 € / 33 € temporada baja</td><td data-l="Qué incluye">IVA incluido · TA5 y T0 aparte · más entrada de socio (3.000 €) y cuota (95 €/mes)</td>'),
 ('<td data-l="Base anual, unos 12 m">≈ 7.050 €</td>','<td data-l="Base anual, unos 12 m">≈ 7.146 €</td>'),
 ('IVA no incluido · cálculo por m²: 9,18 €/m²/mes más 2,50 €/m²/mes de comunidad y 10 €/mes de agua y luz</td>',
  'IVA no incluido · cálculo por m²: hasta 10 m, 9,18 €/m²/mes más 2,50 €/m²/mes de comunidad y 10 €/mes de agua y luz; de 10 a 14 m, 9,49 €/m²/mes y 20 €/mes</td>'),
 ('Marina Palamós<small>tarifa 2026</small>','Marina Palamós<small>tarifa 2026 · la de 2027 ya está publicada (≈ +4,7 %)</small>'),
 ('<td data-l="Tránsito por día (8 m / 12 m)">27 € / 48 € temporada baja</td><td data-l="Qué incluye">IVA y tasa incluidos</td>',
  '<td data-l="Tránsito por día (8 m / 12 m)">27 € / 48 € temporada baja</td><td data-l="Qué incluye">IVA y TA5 incluidos · T0 aparte</td>'),
 ('<span>Septiembre 2026</span>','<span>Comprobado el 3 de noviembre de 2026</span>'),
]
for a,b in R:
    c=h.count(a); assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Fuentes oficiales</strong> (normativa y tarifas de Ports de la Generalitat, Arenys, Sant Feliu, Port Olímpic y Marina Palamós comprobadas el 3 de noviembre de 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2020-443" target="_blank" rel="noopener">BOE: Ley 10/2019 de puertos de Cataluña</a></li>'
 '<li><a href="https://ports.gencat.cat/en/taxes/" target="_blank" rel="noopener">Ports de la Generalitat: tasas 2026</a></li>'
 '<li><a href="https://www.boe.es/eli/es/rd/1999/04/16/607/con" target="_blank" rel="noopener">BOE: Real Decreto 607/1999, seguro de responsabilidad civil</a></li>'
 '<li><a href="https://portolimpic.barcelona/ca/serveis-portuaris/tarifes" target="_blank" rel="noopener">Port Olímpic: tarifas</a></li>'
 '</ul></div>')
i=h.find('<p class="aviso">Fuentes:'); j=h.find('</p>',i)+4
assert i>0
if 'class="fuentes"' not in h: h=h[:j]+'\n        '+FU+h[j:]
open(f,'w',encoding='utf-8').write(h); print('ok',f)
