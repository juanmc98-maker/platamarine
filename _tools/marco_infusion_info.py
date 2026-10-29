# -*- coding: utf-8 -*-
"""Páginas de modelo Mar.Co con versión por infusión (ES/CA/EN/FR): añade bajo «1. Versión» del configurador
un desplegable que explica qué cambia con el laminado por infusión, con la diferencia de precio y el peso de
la tarifa oficial. Idempotente (marca mm-infx). Uso: python3 _tools/marco_infusion_info.py (raíz del repo)."""
import re, json
T = json.load(open('_tools/marco_data/tarifa.json', encoding='utf-8'))
SLUG = {'R-EVOLUTION X36': 'r-evolution-x36', 'R-EVOLUTION 35': 'r-evolution-35', 'E-MOTION 32': 'e-motion-32',
        'E-MOTION 29': 'e-motion-29', 'TWENTYSIX': 'twentysix'}
def eur(n, lg):
    s = f'{n:,.0f}'
    if lg == 'en': return '€' + s
    return s.replace(',', '.' if lg != 'fr' else ' ') + ' €'
TX = {
 'es': ('¿Qué cambia con el laminado por infusión?',
        'Los dos cascos son de fibra de vidrio; cambia cómo se aplica la resina. En la versión estándar se lamina a mano, capa a capa. En la de infusión, la fibra se coloca en seco en el molde y la resina entra con vacío: el casco lleva solo la resina necesaria, sin bolsas de aire, y sale más ligero y más uniforme.',
        'En la práctica, un barco más ligero necesita menos potencia para la misma velocidad y suele gastar menos combustible.',
        'En la {m}, la versión por infusión cuesta {d} más (+ impuestos). Según la tarifa del astillero pesa {w}.',
        'Datos orientativos de la tarifa oficial de Mar.Co; te confirmo las diferencias exactas por escrito en el presupuesto.', '+ impuestos'),
 'ca': ('Què canvia amb el laminat per infusió?',
        'Els dos cascos són de fibra de vidre; canvia com s’aplica la resina. A la versió estàndard es lamina a mà, capa a capa. A la d’infusió, la fibra es col·loca en sec al motlle i la resina entra amb buit: el casc porta només la resina necessària, sense bosses d’aire, i surt més lleuger i més uniforme.',
        'A la pràctica, un vaixell més lleuger necessita menys potència per a la mateixa velocitat i sol gastar menys combustible.',
        'A la {m}, la versió per infusió costa {d} més (+ impostos). Segons la tarifa de la drassana pesa {w}.',
        'Dades orientatives de la tarifa oficial de Mar.Co; et confirmo les diferències exactes per escrit al pressupost.', ''),
 'en': ('What changes with infusion lamination?',
        'Both hulls are fibreglass; what changes is how the resin goes in. The standard version is laminated by hand, layer by layer. In the infusion version the fibre is laid dry in the mould and the resin is drawn in under vacuum: the hull carries only the resin it needs, with no air pockets, and comes out lighter and more consistent.',
        'In practice, a lighter boat needs less power for the same speed and usually burns less fuel.',
        'On the {m}, the infusion version costs {d} more (+ taxes). According to the shipyard’s price list it weighs {w}.',
        'Indicative data from Mar.Co’s official price list; I’ll confirm the exact differences in writing in your quote.', ''),
 'fr': ('Qu’est-ce qui change avec la stratification par infusion ?',
        'Les deux coques sont en fibre de verre ; c’est la façon d’appliquer la résine qui change. La version standard est stratifiée à la main, couche par couche. Pour la version infusion, la fibre est posée à sec dans le moule et la résine est aspirée sous vide : la coque ne contient que la résine nécessaire, sans bulles d’air, et elle est plus légère et plus homogène.',
        'En pratique, un bateau plus léger demande moins de puissance pour la même vitesse et consomme généralement moins.',
        'Sur le {m}, la version infusion coûte {d} de plus (+ taxes). D’après le tarif du chantier, elle pèse {w}.',
        'Données indicatives issues du tarif officiel de Mar.Co ; je vous confirme les différences exactes par écrit dans le devis.', ''),
}
CSS = '<style>.mm-infx{margin:10px 0 0;border:1px solid var(--line,#dfe5e8);border-radius:10px;background:#fff;padding:0 14px}.mm-infx summary{cursor:pointer;padding:11px 0;font-weight:600;font-size:14px}.mm-infx p{margin:0 0 10px;font-size:14px;line-height:1.5}.mm-infx p.n{font-size:12px;opacity:.75}</style>'
NAME = {'R-EVOLUTION X36': 'R-Evolution X36', 'R-EVOLUTION 35': 'R-Evolution 35', 'E-MOTION 32': 'E-Motion 32', 'E-MOTION 29': 'E-Motion 29', 'TWENTYSIX': 'TwentySix'}
n = 0
for m in T:
    if m['name'] not in SLUG: continue
    w = [v for k, v in m['specs'].items() if 'Infusion' in k][0].replace('kg', '').strip()
    for lg in ('es', 'ca', 'en', 'fr'):
        f = ('' if lg == 'es' else lg + '/') + f"marco/{SLUG[m['name']]}/index.html"
        s = open(f, encoding='utf-8').read()
        if 'mm-infx' in s: continue
        h, a, b, c, note, _ = TX[lg]
        wn = int(w.replace('.', ''))
        ww = (f'{wn:,}'.replace(',', {'en': ',', 'fr': '\u202f'}.get(lg, '.'))) + ' kg'
        c = c.format(m=NAME[m['name']], d=eur(m['infusion'] - m['price'], lg), w=ww)
        blk = f'<details class="mm-infx"><summary>{h}</summary><p>{a}</p><p>{b}</p><p>{c}</p><p class="n">{note}</p></details>'
        s, k = re.subn(r'(<input type="radio" name="mmv" value="1">.*?</label></div>)', lambda x: x.group(1) + blk, s, count=1, flags=re.S)
        assert k == 1, f
        s = s.replace('</head>', CSS + '\n</head>', 1)
        open(f, 'w', encoding='utf-8').write(s); n += 1
print(n, 'páginas')
