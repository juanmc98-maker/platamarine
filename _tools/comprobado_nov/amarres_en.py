# -*- coding: utf-8 -*-
"""Moorings guide (EN): corrections from the 3 Nov 2026 check (T0, Arenys, Port Olímpic 12 m, Palamós 2027) + date and sources."""
import re
f='en/guias/amarres-cataluna-tipos-precios-alquiler-compra.html'
h=open(f,encoding='utf-8').read()
R=[
 ('For motorboats of 9 metres or more (12 for sailboats), 9.12 euros per square metre a year, and almost every harbour bills it separately.',
  'For motorboats of 9 metres or more (for sailboats, over 12 metres), 9.12 euros per square metre a year. Motorboats under 9 metres pay 22.80 euros per square metre once, valid indefinitely. Almost every harbour bills it separately.'),
 ('<td data-l="Transient per day (8 m / 12 m)">€17 / €33 low season</td><td data-l="What\'s included">VAT included · plus membership entry (€3,000) and fee (€95/month)</td>',
  '<td data-l="Transient per day (8 m / 12 m)">€21 / €33 low season</td><td data-l="What\'s included">VAT included · TA5 and T0 extra · plus membership entry (€3,000) and fee (€95/month)</td>'),
 ('<td data-l="Annual home-based, ~12 m">≈ €7,050</td>','<td data-l="Annual home-based, ~12 m">≈ €7,146</td>'),
 ('VAT not included · calculated per m²: €9.18/m²/month plus €2.50/m²/month community fee and €10/month water and electricity</td>',
  'VAT not included · calculated per m²: up to 10 m, €9.18/m²/month plus €2.50/m²/month community fee and €10/month water and electricity; from 10 to 14 m, €9.49/m²/month and €20/month</td>'),
 ('Marina Palamós<small>2026 rate</small>','Marina Palamós<small>2026 rate · 2027 rates already published (≈ +4.7%)</small>'),
 ('<td data-l="Transient per day (8 m / 12 m)">€27 / €48 low season</td><td data-l="What\'s included">VAT and fee included</td>',
  '<td data-l="Transient per day (8 m / 12 m)">€27 / €48 low season</td><td data-l="What\'s included">VAT and TA5 included · T0 extra</td>'),
 ('<span>September 2026</span>','<span>Checked on 3 November 2026</span>'),
]
for a,b in R:
    c=h.count(a)
    if c==0 and h.count(b)==1: continue  # already applied
    assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Official sources</strong> (rules and rates of Ports de la Generalitat, Arenys, Sant Feliu, Port Olímpic and Marina Palamós checked on 3 November 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2020-443" target="_blank" rel="noopener">BOE: Law 10/2019 on harbours in Catalonia</a></li>'
 '<li><a href="https://ports.gencat.cat/en/taxes/" target="_blank" rel="noopener">Ports de la Generalitat: 2026 fees</a></li>'
 '<li><a href="https://www.boe.es/eli/es/rd/1999/04/16/607/con" target="_blank" rel="noopener">BOE: Royal Decree 607/1999, third-party liability insurance</a></li>'
 '<li><a href="https://portolimpic.barcelona/ca/serveis-portuaris/tarifes" target="_blank" rel="noopener">Port Olímpic: rates</a></li>'
 '</ul></div>')
i=h.find('<p class="aviso">Sources:'); j=h.find('</p>',i)+4
assert i>0
if 'class="fuentes"' not in h: h=h[:j]+'\n        '+FU+h[j:]
open(f,'w',encoding='utf-8').write(h); print('ok',f)
