#!/usr/bin/env python3
"""Añade LAOS / HydroMarin a /barcos-nuevos/ (ES/CA/EN/FR): enlace en la barra de marcas, bloque de marca,
modelos del buscador (PM_HUB) y contadores de tipo. Idempotente.
Uso: python3 _tools/link_laos.py  (desde la raíz del repo)"""
import re, json, html, urllib.parse

LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
WA = '34633742973'
F = '/laos/fotos/laos-'
MODELS = [('LAOS 605', 'laos-605', '605', 'cab', 6.05), ('HydroMarin 5830', 'hydromarin-5830', '5830', 'lancha', 5.6),
          ('HydroMarin 6020', 'hydromarin-6020', '6020', 'lancha', 6.07), ('HydroMarin 6930', 'hydromarin-6930', '6930', 'lancha', 6.83)]
T = {
 'es': dict(rng='5,60–6,83 m', ask='Precio a consultar', ask_s='Te paso el precio por escrito, sin compromiso.', kick='Distribuidor para Cataluña · 5,60–6,83 m',
            d='Lanchas de poliéster con motor Suzuki montado en fábrica: una pilothouse con cabina cerrada y tres HydroMarin para el día. Bajo pedido.',
            mh='Los modelos', go='Ver el barco →', see='Ver LAOS y HydroMarin: fotos y modelos', cta='Pedir presupuesto', wa='Hola Juan, me interesa una lancha LAOS / HydroMarin.',
            m=['6,05 m · pilothouse con cabina cerrada.', '5,60 m · day cruiser con camarote.', '6,07 m · bowrider open para el día.', '6,83 m · day cruiser para 8 personas.'],
            n=('modelos',)),
 'ca': dict(rng='5,60–6,83 m', ask='Preu a consultar', ask_s='Et passo el preu per escrit, sense compromís.', kick='Distribuïdor per a Catalunya · 5,60–6,83 m',
            d='Llanxes de polièster amb motor Suzuki muntat a fàbrica: una pilothouse amb cabina tancada i tres HydroMarin per al dia. Per encàrrec.',
            mh='Els models', go='Veure el vaixell →', see='Veure LAOS i HydroMarin: fotos i models', cta='Demanar pressupost', wa='Hola Juan, m\'interessa una llanxa LAOS / HydroMarin.',
            m=['6,05 m · pilothouse amb cabina tancada.', '5,60 m · day cruiser amb camarot.', '6,07 m · bowrider open per al dia.', '6,83 m · day cruiser per a 8 persones.'],
            n=('models',)),
 'en': dict(rng='5.60–6.83 m', ask='Price on request', ask_s='I will send you the price in writing, with no obligation.', kick='Dealer for Catalonia · 5.60–6.83 m',
            d='GRP boats with a factory-fitted Suzuki outboard: a pilothouse with an enclosed cabin and three HydroMarin day boats. Built to order.',
            mh='The models', go='See the boat →', see='See LAOS and HydroMarin: photos and models', cta='Request a quote', wa='Hi Juan, I am interested in a LAOS / HydroMarin boat.',
            m=['6.05 m · pilothouse with enclosed cabin.', '5.60 m · day cruiser with a cabin.', '6.07 m · open bowrider for the day.', '6.83 m · day cruiser for 8 people.'],
            n=('models',)),
 'fr': dict(rng='5,60–6,83 m', ask='Prix sur demande', ask_s='Je vous envoie le prix par écrit, sans engagement.', kick='Distributeur pour la Catalogne · 5,60–6,83 m',
            d='Bateaux en polyester avec hors-bord Suzuki monté en usine : un pilothouse à cabine fermée et trois HydroMarin pour la journée. Sur commande.',
            mh='Les modèles', go='Voir le bateau →', see='Voir LAOS et HydroMarin : photos et modèles', cta='Demander un devis', wa='Bonjour Juan, un bateau LAOS / HydroMarin m\'intéresse.',
            m=['6,05 m · pilothouse à cabine fermée.', '5,60 m · day cruiser avec cabine.', '6,07 m · bowrider open pour la journée.', '6,83 m · day cruiser pour 8 personnes.'],
            n=('modèles',)),
}


def run(lang):
    p = LANGS[lang]
    t = T[lang]
    fn = f'.{p}/barcos-nuevos/index.html'
    s = open(fn, encoding='utf-8').read()
    if '<!-- laos -->' in s:
        print('ya está', lang)
        return
    base = f'{p}/laos/'
    # 1. barra de marcas
    nav = (f'<!-- laos --><a href="#marca-laos"><strong class="nv-lg"><img src="/barcos-nuevos/logos/laos-hydromarin.png" alt="LAOS Boats · HydroMarin" loading="lazy" decoding="async" data-nolb></strong>'
           f'<span>{t["rng"]}</span><b>{t["ask"]}</b></a><!-- /laos -->')
    s, k = re.subn(r'(<!-- /squama -->)(<a href="#marca-seastorm")', lambda m: m.group(1) + nav + m.group(2), s, count=1)
    assert k == 1, ('nav', lang)
    # 2. bloque de marca
    cards = ''.join(f'<a class="nv-m" href="{base}#{mid}"><img src="{F}{key}-1-m.jpg" alt="{html.escape(name)}" width="900" height="675" loading="lazy" decoding="async"><div><h3>{html.escape(name)}</h3><p>{html.escape(t["m"][i])}</p><b>{t["ask"]}</b><span class="go">{t["go"]}</span></div></a>'
                    for i, (name, mid, key, _, _) in enumerate(MODELS))
    wa = f'https://wa.me/{WA}?text=' + urllib.parse.quote(t['wa'])
    sec = f'''
<!-- laos -->
    <section class="nv-brand" id="marca-laos" aria-labelledby="nv-laos">
      <a class="nv-ph" href="{base}" tabindex="-1" aria-hidden="true"><img class="ph" loading="lazy" src="{F}605-1-m.jpg" srcset="{F}605-1-m.jpg 900w, {F}605-1.jpg 1600w" sizes="(max-width:1120px) 100vw, 1024px" alt="LAOS 605" width="900" height="675" decoding="async"><img class="logo" src="/barcos-nuevos/logos/laos-hydromarin-blanco.png" alt="LAOS Boats · HydroMarin" data-nolb></a>
      <div class="nv-body">
        <p class="nv-kick">{html.escape(t["kick"])}</p>
        <h2 id="nv-laos" class="nv-h2lg"><img src="/barcos-nuevos/logos/laos-hydromarin.png" alt="LAOS Boats · HydroMarin" data-nolb><span class="sr-only">LAOS / HydroMarin</span></h2>
        <p class="d">{html.escape(t["d"])}</p>
        <p class="nv-pr">{t["ask"]}<small>{html.escape(t["ask_s"])}</small></p>
        <p class="nv-mh">{t["mh"]}</p>
        <div class="nv-models">{cards}</div>
        <div class="nv-cta"><a class="btn btn-pri" href="{base}">{html.escape(t["see"])}</a><a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">{t["cta"]}</a></div>
      </div>
    </section>
<!-- /laos -->'''
    s, k = re.subn(r'(</section>\n<!-- /squama -->)', lambda m: m.group(1) + sec, s, count=1)
    assert k == 1, ('sec', lang)
    # 3. buscador
    m = re.search(r'window.PM_HUB=(\{.*?\});</script>', s, re.S)
    d = json.loads(m.group(1))
    after = max(i for i, x in enumerate(d['m']) if '/squama/' in x['u']) + 1
    new = [{"n": name, "u": f"{base}#{mid}", "i": f"{F}{key}-1-m.jpg", "t": tt, "a": 0, "l": ln, "p": None} for name, mid, key, tt, ln in MODELS]
    d['m'][after:after] = new
    s = s[:m.start(1)] + json.dumps(d, ensure_ascii=False) + s[m.end(1):]
    # 4. contadores de tipo
    from collections import Counter
    c = Counter(x['t'] for x in d['m'])
    for tt in ('lancha', 'cab'):
        s, k = re.subn(r'(data-t="' + tt + r'">.*?<i>)(\d+)', lambda mm: mm.group(1) + str(c[tt]), s, count=1, flags=re.S)
        assert k == 1, ('cnt', tt, lang)
    open(fn, 'w', encoding='utf-8').write(s)
    print('ok', lang, dict(c))


if __name__ == '__main__':
    for l in LANGS:
        run(l)
