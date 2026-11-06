#!/usr/bin/env python3
"""Añade Sea Water / Kymera a /barcos-nuevos/ (ES/CA/EN/FR): barra de marcas, bloque de marca (tras Mar.Co),
modelos del buscador (PM_HUB, tras Mar.Co) y contador de semirrígidas. Idempotente. Uso: python3 _tools/link_seawater.py"""
import re, json, html, urllib.parse
from collections import Counter
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
TAR = {m['slug']: m for m in json.load(open('_tools/seawater_data/tarifa.json'))}
META = json.load(open('_tools/seawater_data/meta.json'))
ORDER = sorted(TAR, key=lambda s: -TAR[s]['price'])
def eur(n, lg):
    s = f'{n:,}'
    return '€' + s if lg == 'en' else (s.replace(',', '&nbsp;') + '&nbsp;€' if lg == 'fr' else s.replace(',', '.') + '&nbsp;€')
def m2(v, lg): return (f'{v:.2f}'.replace('.', ',') if lg != 'en' else f'{v:.2f}') + ' m'
T = {
 'es': dict(frm='Desde', vat='+ impuestos', noeng='sin motores', kick='De 7,19 a 16,15 m', rng='7,19–16,15 m', go='Ver el barco →', mh='Los modelos',
   d='Semirrígidas Phantom y Ghost y los Kymera 43 y 53: desde una open de 7 m hasta 16 m con camarote. Bajo pedido y configurables. Once modelos.',
   see='Ver Sea Water: fotos y precios', cta='Pedir presupuesto', wa='Hola Juan, me interesa una Sea Water. ¿Me ayudas a elegir modelo?',
   kind={'cab': 'con camarote', 'open': 'open'}),
 'ca': dict(frm='Des de', vat='+ impostos', noeng='sense motors', kick='De 7,19 a 16,15 m', rng='7,19–16,15 m', go='Veure el vaixell →', mh='Els models',
   d='Semirígides Phantom i Ghost i els Kymera 43 i 53: des d’una open de 7 m fins a 16 m amb cabina. Per encàrrec i configurables. Onze models.',
   see='Veure Sea Water: fotos i preus', cta='Demanar pressupost', wa='Hola Juan, m’interessa una Sea Water. M’ajudes a triar model?',
   kind={'cab': 'amb cabina', 'open': 'open'}),
 'en': dict(frm='From', vat='+ taxes', noeng='without engines', kick='From 7.19 to 16.15 m', rng='7.19–16.15 m', go='See the boat →', mh='The models',
   d='Phantom and Ghost RIBs and the Kymera 43 and 53: from a 7 m open boat to 16 m with a cabin. Built to order and configurable. Eleven models.',
   see='See Sea Water: photos and prices', cta='Request a quote', wa='Hi Juan, I am interested in a Sea Water. Can you help me choose a model?',
   kind={'cab': 'with cabin', 'open': 'open'}),
 'fr': dict(frm='À partir de', vat='+ taxes', noeng='sans moteurs', kick='De 7,19 à 16,15 m', rng='7,19–16,15 m', go='Voir le bateau →', mh='Les modèles',
   d='Semi-rigides Phantom et Ghost et les Kymera 43 et 53 : d’un open de 7 m jusqu’à 16 m avec cabine. Sur commande et configurables. Onze modèles.',
   see='Voir Sea Water : photos et prix', cta='Demander un devis', wa='Bonjour Juan, un Sea Water m’intéresse. Pouvez-vous m’aider à choisir ?',
   kind={'cab': 'avec cabine', 'open': 'open'}),
}
CAB = {'kymera-53', 'phantom-500', 'kymera-43', 'phantom-500-yachting'}
def full(n): return n if n.startswith('Kymera') else 'Sea Water ' + n
def run(lg):
    p = LANGS[lg]; t = T[lg]; fn = f'.{p}/barcos-nuevos/index.html'
    s = open(fn, encoding='utf-8').read()
    if '<!-- seawater -->' in s: print('ya está', lg); return
    base = f'{p}/seawater/'; mn = min(m['price'] for m in TAR.values())
    price = f'{t["frm"]} {eur(mn, lg)} <span class="vat">{t["vat"]}</span>'
    nav = f'<!-- seawater --><a href="#marca-seawater"><strong class="nv-lg"><img src="/barcos-nuevos/logos/seawater.png" alt="Sea Water" loading="lazy" decoding="async" data-nolb></strong><span>{t["rng"]}</span><b>{price}</b></a><!-- /seawater -->'
    s, k = re.subn(r'(<!-- /marco -->)(<)', lambda m: m.group(1) + nav + m.group(2), s, count=1); assert k == 1, ('nav', lg)
    cards = ''.join(f'<a class="nv-m" href="{base}{sl}/"><img src="/seawater/fotos/{sl}/01-m.jpg" alt="{html.escape(full(TAR[sl]["name"]))}" width="640" height="427" loading="lazy" decoding="async"><div><h3>{html.escape(full(TAR[sl]["name"]))}</h3><p>{m2(META[sl]["loa"], lg)} · {t["kind"]["cab" if sl in CAB else "open"]}.</p><b>{t["frm"]} {eur(TAR[sl]["price"], lg)} <span class="vat">{t["vat"]}</span></b><span class="go">{t["go"]}</span></div></a>' for sl in ORDER)
    wa = 'https://wa.me/34633742973?text=' + urllib.parse.quote(t['wa'])
    sec = f'''
<!-- seawater -->
    <section class="nv-brand" id="marca-seawater" aria-labelledby="nv-seawater">
      <a class="nv-ph" href="{base}" tabindex="-1" aria-hidden="true"><img class="ph" loading="lazy" src="/seawater/fotos/ghost-420/01-m.jpg" srcset="/seawater/fotos/ghost-420/01-m.jpg 900w, /seawater/fotos/ghost-420/01.jpg 1600w" sizes="(max-width:1120px) 100vw, 1024px" alt="Sea Water Ghost 420" width="640" height="427" decoding="async"><img class="logo" src="/barcos-nuevos/logos/seawater-blanco.png" alt="Sea Water" data-nolb></a>
      <div class="nv-body">
        <p class="nv-kick">{t["kick"]}</p>
        <h2 id="nv-seawater" class="nv-h2lg"><img src="/barcos-nuevos/logos/seawater.png" alt="Sea Water" data-nolb><span class="sr-only">Sea Water</span></h2>
        <p class="d">{html.escape(t["d"])}</p>
        <p class="nv-pr">{price}<small>{t["noeng"]}</small></p>
        <p class="nv-mh">{t["mh"]}</p>
        <div class="nv-models">{cards}</div>
        <div class="nv-cta"><a class="btn btn-pri" href="{base}">{html.escape(t["see"])}</a><a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">{t["cta"]}</a></div>
      </div>
    </section>
<!-- /seawater -->'''
    s, k = re.subn(r'(</section>\n<!-- /marco -->)', lambda m: m.group(1) + sec, s, count=1); assert k == 1, ('sec', lg)
    m = re.search(r'window.PM_HUB=(\{.*?\});</script>', s, re.S); d = json.loads(m.group(1))
    after = max(i for i, x in enumerate(d['m']) if '/marco/' in x['u']) + 1
    d['m'][after:after] = [{"n": full(TAR[sl]['name']), "u": f"{base}{sl}/", "i": f"/seawater/fotos/{sl}/01-m.jpg", "t": "semi", "a": 0, "l": META[sl]['loa'], "p": TAR[sl]['price']} for sl in ORDER]
    s = s[:m.start(1)] + json.dumps(d, ensure_ascii=False) + s[m.end(1):]
    c = Counter(x['t'] for x in d['m'])
    s, k = re.subn(r'(data-t="semi">.*?<i>)(\d+)', lambda mm: mm.group(1) + str(c['semi']), s, count=1, flags=re.S); assert k == 1, ('cnt', lg)
    open(fn, 'w', encoding='utf-8').write(s); print('ok', lg, c['semi'])
for l in LANGS: run(l)
