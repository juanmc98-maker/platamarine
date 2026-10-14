"""Bloque "Coste al año" en la ficha v2 (ES/CA/EN/FR) y relleno automático de la calculadora
de coste anual desde la URL (?len=&eng=&hp=&val=).
Las cifras salen de la misma fórmula que /herramientas/coste-mantener-barco.html, sin amarre.
Uso: python3 _tools/coste_v2.py   (idempotente)"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent

BOATS = {
    # slug: eslora, motor (fb/ig/id/sv como la calculadora), cv, valor, horas/año, €/l
    # hp = potencia total (2 x 260 cv). engtxt: cómo se describe el motor en la letra pequeña. moor: texto del amarre propio del barco
    'prestige-32': dict(len=10.65, eng='id', hp=520, val=89000, hrs=60, fuel=1.60,
        engtxt={'es': '2 motores diésel de 260 cv', 'ca': '2 motors dièsel de 260 cv', 'en': 'twin 260 hp diesels', 'fr': '2 moteurs diesel de 260 ch'},
        moor={'es': 'El amarre va aparte: el actual es de alquiler y no se transmite con el barco, y el precio depende mucho del puerto.',
              'ca': "L'amarrament va a part: l'actual és de lloguer i no es transmet amb el vaixell, i el preu depèn molt del port.",
              'en': 'The berth is extra: the current one is rented and does not go with the boat, and the price depends a lot on the marina.',
              'fr': "La place de port est en plus : l'actuelle est louée et n'est pas cédée avec le bateau, et le prix dépend beaucoup du port."}),
    'oceanis-50': dict(len=14.75, eng='sv', hp=110, val=155000, hrs=60, fuel=1.60,
        moor={'es': 'El amarre va aparte: el actual es de alquiler, y el precio depende mucho del puerto.',
              'ca': "L'amarrament va a part: l'actual és de lloguer, i el preu depèn molt del port.",
              'en': 'The berth is extra: the current one is rented, and the price depends a lot on the marina.',
              'fr': "La place de port est en plus : l'actuelle est louée, et le prix dépend beaucoup du port."}),
    'sealine-365': dict(len=11.10, eng='id', hp=400, val=75000, hrs=60, fuel=1.60,
        engtxt={'es': '2 motores diésel de 200 cv', 'ca': '2 motors dièsel de 200 cv', 'en': 'twin 200 hp diesels', 'fr': '2 moteurs diesel de 200 ch'},
        moor={'es': 'El amarre va aparte, y el precio depende mucho del puerto.',
              'ca': "L'amarrament va a part, i el preu depèn molt del port.",
              'en': 'The berth is extra, and the price depends a lot on the marina.',
              'fr': 'La place de port est en plus, et le prix dépend beaucoup du port.'}),
    'monte-carlo-27': dict(len=7.98, eng='ig', hp=350, val=64900, hrs=60, fuel=1.80,
        engtxt={'es': 'un motor de gasolina de 350 cv', 'ca': 'un motor de gasolina de 350 cv', 'en': 'a 350 hp petrol engine', 'fr': 'un moteur essence de 350 ch'},
        moor={'es': 'El amarre va aparte: ahora está en seco, y el precio depende mucho del puerto.',
              'ca': "L'amarrament va a part: ara és en sec, i el preu depèn molt del port.",
              'en': 'The berth is extra: it is currently ashore, and the price depends a lot on the marina.',
              'fr': 'La place de port est en plus : il est actuellement à terre, et le prix dépend beaucoup du port.'}),
    'starfisher-840': dict(len=8.40, eng='id', hp=400, val=50900, hrs=60, fuel=1.60,
        engtxt={'es': '2 motores diésel de 200 cv', 'ca': '2 motors dièsel de 200 cv', 'en': 'twin 200 hp diesels', 'fr': '2 moteurs diesel de 200 ch'},
        moor={'es': 'El amarre va aparte: el actual es de alquiler y no entra en la venta, y el precio depende mucho del puerto.',
              'ca': "L'amarrament va a part: l'actual és de lloguer i no entra a la venda, i el preu depèn molt del port.",
              'en': 'The berth is extra: the current one is rented and not included in the sale, and the price depends a lot on the marina.',
              'fr': "La place de port est en plus : l'actuelle est louée et n'est pas comprise dans la vente, et le prix dépend beaucoup du port."}),
    'tiger-marine-650': dict(len=6.50, eng='fb', hp=150, val=33000, hrs=60, fuel=1.80,
        moor={'es': 'El amarre va aparte y no entra en la venta. Al venderse con remolque, también se puede guardar en seco.',
              'ca': "L'amarrament va a part i no entra a la venda. Com que es ven amb remolc, també es pot guardar en sec.",
              'en': 'The berth is extra and not included. As it comes with a trailer, it can also be kept ashore.',
              'fr': "La place de port est en plus et n'est pas comprise. Vendu avec remorque, il peut aussi être gardé à terre."}),
    'cattleya-x6': dict(len=5.98, eng='fb', hp=150, val=55000, hrs=60, fuel=1.80,
        moor={'es': 'El amarre va aparte: el actual es de alquiler en Ibiza y, según el propietario, se podría subrogar; el precio depende mucho del puerto.',
              'ca': "L'amarrament va a part: l'actual és de lloguer a Eivissa i, segons el propietari, es podria subrogar; el preu depèn molt del port.",
              'en': 'The berth is extra: the current one is rented in Ibiza and, according to the owner, could be taken over; the price depends a lot on the marina.',
              'fr': "La place de port est en plus : l'actuelle est louée à Ibiza et, selon le propriétaire, pourrait être reprise ; le prix dépend beaucoup du port."}),
}

def cost(b):
    L, hp, val = b['len'], b['hp'], b['val']
    ins = max(200, val * 0.007)
    eng = {'fb': 250 + 1.0 * hp, 'ig': 350 + 1.2 * hp, 'id': 400 + 1.5 * hp, 'sv': 350 + 2 * hp}[b['eng']]
    hull = L * 70
    itb = 0 if L < 6 else (80 if L <= 12 else 120)
    misc = 150 + 10 * L
    fuel = hp * {'fb': .17, 'ig': .2, 'id': .1, 'sv': .03}[b['eng']] * b['hrs'] * b['fuel']
    return [ins, eng, hull, itb, misc, fuel]

def eur(x, lang):
    n = f'{round(x):,}'
    if lang == 'en': return '€' + n
    return n.replace(',', ' ' if lang == 'fr' else '.') + ' €'

def r500(x): return round(x / 500) * 500

T = {
 'es': dict(nav='Coste al año', k='Coste al año', h='¿Cuánto cuesta mantenerlo?',
  lead='Estimación sin amarre, navegando unas {hrs} horas al año.', y='al año', nf='sin combustible', about='≈',
  rows=['Seguro (todo riesgo)', 'Mantenimiento del motor', 'Varada, limpieza y antifouling', 'ITB (prorrateada)', 'Ánodos, baterías y pequeños extras', 'Combustible ({hrs} h)'], tot='Total sin amarre',
  moor='El amarre va aparte y su precio depende mucho del puerto.',
  btn='Calcularlo con tus datos y tu puerto', path='/herramientas/coste-mantener-barco.html',
  small='Cálculo orientativo con la calculadora de la web (eslora {len}, {eng}, combustible a {fuel} €/l). Cada barco y cada dueño gastan distinto: puede variar mucho y no es vinculante.'),
 'ca': dict(nav='Cost anual', k='Cost anual', h='Quant costa mantenir-lo?',
  lead="Estimació sense amarrament, navegant unes {hrs} hores l'any.", y="l'any", nf='sense combustible', about='≈',
  rows=['Assegurança (tot risc)', 'Manteniment del motor', 'Varada, neteja i antifouling', 'ITB (prorratejada)', 'Ànodes, bateries i petits extres', 'Combustible ({hrs} h)'], tot='Total sense amarrament',
  moor="L'amarrament va a part i el preu depèn molt del port.",
  btn='Calcular-ho amb les teves dades i el teu port', path='/ca/herramientas/coste-mantener-barco.html',
  small="Càlcul orientatiu amb la calculadora del web (eslora {len}, {eng}, combustible a {fuel} €/l). Cada vaixell i cada propietari gasten diferent: pot variar molt i no és vinculant."),
 'en': dict(nav='Running costs', k='Running costs', h='How much does it cost to keep?',
  lead='Estimate without a berth, cruising about {hrs} hours a year.', y='a year', nf='without fuel', about='≈',
  rows=['Insurance (fully comprehensive)', 'Engine servicing', 'Haul-out, cleaning and antifouling', 'ITB inspection (pro rata)', 'Anodes, batteries and small extras', 'Fuel ({hrs} h)'], tot='Total without berth',
  moor="The berth is extra and its price depends a lot on the marina.",
  btn='Work it out with your own figures and marina', path='/en/herramientas/coste-mantener-barco.html',
  small="Rough estimate using the calculator on this website (length {len}, {eng}, fuel at €{fuel}/l). Every boat and owner spends differently: it can vary a lot and is not binding."),
 'fr': dict(nav='Coût annuel', k='Coût annuel', h='Combien coûte son entretien ?',
  lead='Estimation sans place de port, avec environ {hrs} heures de navigation par an.', y='par an', nf='sans carburant', about='≈',
  rows=['Assurance (tous risques)', 'Entretien du moteur', 'Carénage, nettoyage et antifouling', 'ITB (au prorata)', 'Anodes, batteries et petits extras', 'Carburant ({hrs} h)'], tot='Total sans place de port',
  moor="La place de port est en plus et son prix dépend beaucoup du port.",
  btn='Le calculer avec vos données et votre port', path='/fr/herramientas/coste-mantener-barco.html',
  small="Estimation indicative avec le calculateur du site (longueur {len}, {eng}, carburant à {fuel} €/l). Chaque bateau et chaque propriétaire dépensent différemment : cela peut beaucoup varier et n'engage à rien."),
}

ENG = {
 'es': {'fb': 'fueraborda de gasolina de {hp} cv', 'ig': 'motor de gasolina de {hp} cv', 'id': 'diésel de {hp} cv', 'sv': 'velero con diésel de {hp} cv'},
 'ca': {'fb': 'forabord de gasolina de {hp} cv', 'ig': 'motor de gasolina de {hp} cv', 'id': 'dièsel de {hp} cv', 'sv': 'veler amb dièsel de {hp} cv'},
 'en': {'fb': '{hp} hp petrol outboard', 'ig': '{hp} hp petrol engine', 'id': '{hp} hp diesel', 'sv': 'sailing boat with {hp} hp diesel'},
 'fr': {'fb': 'hors-bord essence de {hp} ch', 'ig': 'moteur essence de {hp} ch', 'id': 'diesel de {hp} ch', 'sv': 'voilier avec diesel de {hp} ch'},
}

CSS = """
/* Coste al año */
.v2-cost{display:grid;grid-template-columns:1fr 1.1fr;gap:clamp(24px,4vw,56px);align-items:start}
.v2-cost-big b{display:block;font:700 clamp(2rem,5vw,3rem)/1 "Hanken Grotesk",var(--display);color:var(--ink)}
.v2-cost-big span{display:block;color:var(--muted,#5b6b75);margin:8px 0 18px}
.v2-cost table{width:100%;border-collapse:collapse;font-size:15.5px}
.v2-cost td{padding:10px 0;border-bottom:1px solid rgba(14,48,66,.12)}
.v2-cost td+td{text-align:right;font-weight:700;white-space:nowrap;padding-left:12px}
.v2-cost tr.t td{border-bottom:0;padding-top:14px}
.v2-cost .v2-small{font-size:13px;color:var(--muted,#5b6b75);line-height:1.5;margin-top:14px}
@media (max-width:820px){.v2-cost{grid-template-columns:1fr}}
"""

PREFILL = ("try{var q=new URLSearchParams(location.search);[['len','c_len'],['hp','c_hp'],['val','c_val']].forEach(function(a){var v=q.get(a[0]);"
           "if(v&&/^[0-9.,]{1,9}$/.test(v))document.getElementById(a[1]).value=v;});var e=q.get('eng');"
           "if(e&&/^(fb|ig|id|sv)$/.test(e)){document.getElementById('c_eng').value=e;document.getElementById('c_fuel').value=(e==='fb'||e==='ig')?'1,80':'1,60';}}catch(x){}")

def section(slug, b, lang):
    t = T[lang]; c = cost(b); total = sum(c); dec = '.' if lang == 'en' else ','
    eng = b.get('engtxt', {}).get(lang) or ENG[lang][b['eng']].format(hp=b['hp'])
    f = lambda s: s.format(hrs=b['hrs'], hp=b['hp'], eng=eng, len=f"{b['len']:.2f}".replace('.', dec) + ' m', fuel=f"{b['fuel']:.2f}".replace('.', dec))
    rows = ''.join(f'<tr><td>{f(n)}</td><td>{eur(v, lang)}</td></tr>' for n, v in zip(t['rows'], c))
    q = f"?len={str(b['len']).replace('.', ',')}&amp;eng={b['eng']}&amp;hp={b['hp']}&amp;val={b['val']}"
    return f'''<section class="v2-sec v2-band" id="coste"><div class="wrap">
<p class="v2-k">{t['k']}</p><h2>{t['h']}</h2>
<div class="v2-cost"><div class="v2-cost-big"><p class="v2-lead">{f(t['lead'])}</p><b>{t['about']} {eur(r500(total), lang)} <small>{t['y']}</small></b><span>{t['about']} {eur(r500(total - c[5]), lang)} {t['nf']}</span>
<p>{b.get('moor', {}).get(lang, t['moor'])}</p><a class="btn btn-wa" href="{t['path']}{q}">{t['btn']}</a></div>
<div><table>{rows}<tr class="t"><td><b>{t['tot']}</b></td><td>{eur(total, lang)}</td></tr></table>
<p class="v2-small">{f(t['small'])}</p></div></div>
</div></section>
'''

def run():
    for slug, b in BOATS.items():
        for lang, t in T.items():
            p = ROOT / ('' if lang == 'es' else lang) / 'barcos' / f'{slug}.html'
            s = p.read_text()
            assert 'class="boat v2"' in s
            if 'id="coste"' in s:
                s2 = re.sub(r'<section class="v2-sec v2-band" id="coste">.*?</section>\n', lambda m: section(slug, b, lang), s, count=1, flags=re.S)
                if s2 != s: p.write_text(s2); print(slug, lang, 'coste actualizado')
                continue
            a = '<section class="v2-sec v2-dark" id="ficha">'
            assert s.count(a) == 1
            s = s.replace(a, section(slug, b, lang) + a, 1)
            s, n = re.subn(r'(<a href="#ficha">)', f'<a href="#coste"><span>{t["nav"]}</span><i></i></a>\\1', s, count=1)
            assert n == 1
            s = s.replace('ficha-v2.css?v=20261011"', 'ficha-v2.css?v=20261011b"')
            p.write_text(s); print(slug, lang, 'ok')
    css = ROOT / 'barcos' / 'ficha-v2.css'
    if '.v2-cost' not in css.read_text(): css.write_text(css.read_text().rstrip('\n') + '\n' + CSS)
    for lang in T:
        p = ROOT / ('' if lang == 'es' else lang) / 'herramientas' / 'coste-mantener-barco.html'
        s = p.read_text()
        if 'URLSearchParams' in s: continue
        end = "document.getElementById('calc').addEventListener('change',calc);calc();})();"
        assert s.count(end) == 1, lang
        s = s.replace(end, end.replace('calc();})();', PREFILL + 'calc();})();'))
        p.write_text(s); print('calculadora', lang, 'ok')

if __name__ == '__main__':
    run()
