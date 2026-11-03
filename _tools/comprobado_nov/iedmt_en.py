# -*- coding: utf-8 -*-
"""Registration tax guide (EN): corrections from the 3 Nov 2026 check + date and sources."""
import re
f='en/guias/impuesto-matriculacion-barcos.html'
h=open(f,encoding='utf-8').read()
R=[
 ("That's no coincidence: from 8 metres of length upward, first registration in Spain carries a 12% tax.",
  "That's no coincidence: above 8 metres of length, first registration in Spain carries a 12% tax."),
 ('Personal watercraft always pay it, whatever their length.</p>',
  'Personal watercraft always pay it, whatever their length, and at a different rate: 14.75%.</p>'),
 ("the base is market value, which the tax authority calculates using its official boat valuation tables (an order published every year), or the real price if it's higher.</p>",
  "the base is market value; you can use the official boat valuation tables (an order published every year), and the tax authority can check that value.</p>"),
 ('and if the real price is higher than the table, the real price wins.',
  'and the tax authority can check the value you declare.'),
 ('<td>Boat over 8 m bought in another EU country</td><td>Yes, 12% on table value</td>',
  '<td>Boat over 8 m bought in another EU country</td><td>Yes, 12%: if used, on its market value (tables); if new, on the price excluding VAT</td>'),
 ('just an exemption declaration (form 06).','just a declaration of non-liability (form 06).'),
 ("<p>They don't pay, but the exemption isn't automatic: form 06 has to be filed",
  "<p>They don't pay, but it isn't automatic: the declaration of non-liability (form 06) has to be filed"),
 ("on the boat's value at that time.",
  "on the boat's value at that time, using form 576 and within 15 calendar days of the change. The exemption is also lost if the boat is let to the same person for more than 3 months in a year, or if the owner or someone linked to them keeps its use for themselves."),
 ("The length that counts is the one shown in the boat's paperwork (the hull length on the CE declaration of conformity), not the overall length including the bathing platform or pulpits.",
  "The length that counts is the one shown in the boat's paperwork, not the overall length including the bathing platform or pulpits; if in doubt, have your gestoría confirm it with the boat's certificate."),
 ('<td>Yes, on current value</td><td>Self-assessment when use changes</td>',
  '<td>Yes, on current value</td><td>Form 576 within 15 days of the change of use</td>'),
 ('<span>Updated September 2026</span>','<span>Checked on 3 November 2026</span>'),
 ('Tax information for guidance only, reviewed in September 2026 under','Tax information for guidance only, checked on 3 November 2026 under'),
]
for a,b in R:
    c=h.count(a)
    if c==0 and h.count(b)==1: continue  # already applied
    assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Official sources</strong> (checked on 3 November 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-1992-28741" target="_blank" rel="noopener">BOE: Law 38/1992 on Excise Duties (articles 65 to 70)</a></li>'
 '<li><a href="https://www3.agenciatributaria.gob.es/static_files/Sede/Procedimiento_ayuda/G502/instr_mod576.pdf" target="_blank" rel="noopener">Spanish Tax Agency: form 576 instructions (rates and base)</a></li>'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/vehiculos-embarcaciones/primera-matriculacion-medios-transporte/que-supuestos-puedo-estar-exento-transporte.html" target="_blank" rel="noopener">Spanish Tax Agency: exemptions (charter, form 05)</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE: Order HAC/1501/2025, average boat prices for 2026</a></li>'
 '</ul></div>')
a='Please confirm with a gestoría or the tax authorities before buying.</p>'
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
