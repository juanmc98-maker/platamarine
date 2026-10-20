#!/usr/bin/env python3
"""Genera /marcas/ (otras marcas de barcos nuevos: Catharsis, Sunrise, SeaStorm) en ES/CA/EN/FR
a partir de la plantilla de /barcos-nuevos/. SKIPPER va aparte: no se mezcla aquí.
Uso: python3 _tools/build_marcas.py  (desde la raíz del repo)"""
import re, json, html, os

ROOT = '.'
BASE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
SLUG = 'marcas'
VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': 'HT'}

# Precios "desde" sacados de cada página de marca (oct 2026), sin IVA.
BRANDS = [
 dict(slug='catharsis', name='Catharsis', price=94990, img='/catharsis/fotos/catharsis-930-1-m.jpg', w=800, h=450, alt='Catharsis 930',
      kick=('Turquía · Avila Marin', 'Turquia · Avila Marin', 'Turkey · Avila Marin', 'Turquie · Avila Marin'),
      d=('Crucero fueraborda de 9,30 m con timonera, dos camarotes y baño, para pasar el día o unos días a bordo.',
         'Creuer fora borda de 9,30 m amb timonera, dos camarots i bany, per passar el dia o uns dies a bord.',
         'A 9.30 m outboard cruiser with a wheelhouse, two cabins and a bathroom, for day trips or a few days on board.',
         'Cruiser hors-bord de 9,30 m avec timonerie, deux cabines et salle d\'eau, pour la journée ou quelques jours à bord.'),
      note=('sin motores', 'sense motors', 'without engines', 'sans moteurs')),
 dict(slug='sunrise', name='Sunrise', price=5990, img='/sunrise/fotos/645-1-m.jpg', w=800, h=480, alt='Sunrise 645',
      kick=('Polonia', 'Polònia', 'Poland', 'Pologne'),
      d=('Barcos pequeños de 4 a 7 m, sencillos y fáciles de mantener: opens, tenders, un bowrider y cabinados.',
         'Vaixells petits de 4 a 7 m, senzills i fàcils de mantenir: opens, tenders, un bowrider i cabinats.',
         'Small boats from 4 to 7 m, simple and easy to look after: opens, tenders, a bowrider and small cabin boats.',
         'Petits bateaux de 4 à 7 m, simples et faciles à entretenir : opens, tenders, un bowrider et des cabines.'),
      note=('sin motor', 'sense motor', 'without engine', 'sans moteur')),
 dict(slug='seastorm', name='SeaStorm', price=4990, img='/seastorm/fotos/portada.jpg', w=1000, h=600, alt='SeaStorm 17',
      kick=('Estonia', 'Estònia', 'Estonia', 'Estonie'),
      d=('Botes de polietileno de una sola pieza, de 3,7 a 5,2 m: ligeros, con muy poco mantenimiento y buenos para acercarse a la playa.',
         'Bots de polietilè d\'una sola peça, de 3,7 a 5,2 m: lleugers, amb molt poc manteniment i bons per acostar-se a la platja.',
         'One-piece polyethylene boats from 3.7 to 5.2 m: light, very low maintenance and easy to bring up to the beach.',
         'Bateaux en polyéthylène d\'une seule pièce, de 3,7 à 5,2 m : légers, très peu d\'entretien et faciles à approcher de la plage.'),
      note=('sin motor', 'sense motor', 'without engine', 'sans moteur')),
]
LI = ['es', 'ca', 'en', 'fr']

T = {
 'es': dict(
  title='Otras marcas de barcos nuevos: Catharsis, Sunrise y SeaStorm · Plata Marine',
  desc='Barcos nuevos por encargo de Catharsis (Turquía), Sunrise (Polonia) y SeaStorm (Estonia), desde 4.990 € +IVA. Te ayudo a elegir modelo y motor en Cataluña.',
  crumbs=('Inicio', 'Barcos en venta'), eyebrow='Barcos nuevos', h1='Otras marcas de barcos nuevos',
  intro='Barcos nuevos que se piden a fábrica, de astilleros con los que trabajo en Cataluña. Te ayudo a elegir el modelo, el motor y el equipamiento, y te paso el presupuesto por escrito.',
  from_='Desde', see='Ver la marca',
  used_h='¿Buscas un barco de ocasión?', used_a='Ver barcos de segunda mano →',
  small='Precios orientativos de octubre de 2026, sin IVA y en fábrica, del modelo más económico de cada marca: no incluyen motor, equipamiento opcional, transporte ni matriculación. Pueden cambiar y no son vinculantes; el precio final es el del presupuesto por escrito. Podemos equivocarnos; si ves un error, avísanos.'),
 'ca': dict(
  title='Altres marques de vaixells nous: Catharsis, Sunrise i SeaStorm · Plata Marine',
  desc='Vaixells nous per encàrrec de Catharsis (Turquia), Sunrise (Polònia) i SeaStorm (Estònia), des de 4.990 € +IVA. T\'ajudo a triar model i motor a Catalunya.',
  crumbs=('Inici', 'Vaixells en venda'), eyebrow='Vaixells nous', h1='Altres marques de vaixells nous',
  intro='Vaixells nous que es demanen a fàbrica, de drassanes amb què treballo a Catalunya. T\'ajudo a triar el model, el motor i l\'equipament, i et passo el pressupost per escrit.',
  from_='Des de', see='Veure la marca',
  used_h='Busques un vaixell d\'ocasió?', used_a='Veure vaixells de segona mà →',
  small='Preus orientatius d\'octubre de 2026, sense IVA i a fàbrica, del model més econòmic de cada marca: no inclouen motor, equipament opcional, transport ni matriculació. Poden canviar i no són vinculants; el preu final és el del pressupost per escrit. Ens podem equivocar; si hi veus un error, avisa\'ns.'),
 'en': dict(
  title='Other new boat brands: Catharsis, Sunrise and SeaStorm · Plata Marine',
  desc='New boats built to order by Catharsis (Turkey), Sunrise (Poland) and SeaStorm (Estonia), from €4,990 +VAT. I help you choose the model and engine in Catalonia.',
  crumbs=('Home', 'Boats for sale'), eyebrow='New boats', h1='Other new boat brands',
  intro='New boats ordered from the factory, from boatbuilders I work with in Catalonia. I help you choose the model, engine and equipment, and send you the quote in writing.',
  from_='From', see='See the brand',
  used_h='Looking for a used boat?', used_a='See used boats →',
  small='Indicative prices as of October 2026, ex-works and excluding VAT, for the most affordable model of each brand: they do not include engine, optional equipment, transport or registration. They may change and are not binding; the final price is the one in the written quote. We may be wrong; if you spot an error, let us know.'),
 'fr': dict(
  title='Autres marques de bateaux neufs : Catharsis, Sunrise et SeaStorm · Plata Marine',
  desc='Bateaux neufs sur commande de Catharsis (Turquie), Sunrise (Pologne) et SeaStorm (Estonie), à partir de 4 990 € HT. Je vous aide à choisir modèle et moteur en Catalogne.',
  crumbs=('Accueil', 'Bateaux à vendre'), eyebrow='Bateaux neufs', h1='Autres marques de bateaux neufs',
  intro='Des bateaux neufs commandés à l\'usine, auprès de chantiers avec lesquels je travaille en Catalogne. Je vous aide à choisir le modèle, le moteur et l\'équipement, et je vous envoie le devis par écrit.',
  from_='À partir de', see='Voir la marque',
  used_h='Vous cherchez un bateau d\'occasion ?', used_a='Voir les bateaux d\'occasion →',
  small='Prix indicatifs d\'octobre 2026, départ usine et hors TVA, pour le modèle le plus abordable de chaque marque : ils n\'incluent pas le moteur, les options, le transport ni l\'immatriculation. Ils peuvent changer et ne sont pas contractuels ; le prix final est celui du devis écrit. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous. Nous ne parlons pas français : nous utilisons un traducteur, merci de votre indulgence.'),
}

CSS = """
.mk-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:26px}
.mk-c{display:flex;flex-direction:column;background:#fff;border:1px solid rgba(127,146,158,.28);border-radius:var(--radius);overflow:hidden}
.mk-c>a.mk-ph{display:block;background:var(--paper-2)}
.mk-c img{display:block;width:100%;height:auto;aspect-ratio:16/10;object-fit:cover}
.mk-b{padding:16px 18px 18px;display:flex;flex-direction:column;gap:6px;flex:1}
.mk-b h2{font-size:1.4rem;font-weight:700;line-height:1.1}
.mk-b h2 a{color:inherit;text-decoration:none}
.mk-b p.d{color:var(--ink-2);font-size:.95rem;line-height:1.5;flex:1}
.mk-b .pr{font-family:var(--display);font-weight:700;font-size:1.15rem;margin-top:4px}
.mk-b .pr small{font-weight:500;font-size:.8rem;color:var(--ink-2);margin-left:6px}
.mk-b .btn{align-self:flex-start;margin-top:8px;background:var(--ink);color:#fff}
.mk-b .btn:hover{background:var(--sea)}
@media (max-width:900px){.mk-grid{grid-template-columns:1fr}.mk-c img{aspect-ratio:16/9}}
@media (max-width:520px){.mk-b .btn{align-self:stretch;text-align:center}}
"""


def eur(n, lang):
    s = f'{n:,}'
    if lang == 'en':
        return s
    if lang == 'fr':
        return s.replace(',', '\u202f')
    return s.replace(',', '.')


def price(n, lang, t):
    return f'{eur(n, lang)} €'


def build(lang):
    p = LANGS[lang]
    li = LI.index(lang)
    t = T[lang]
    tpl = open(f'{ROOT}{p}/barcos-nuevos/index.html', encoding='utf-8').read()
    url = f'{BASE}{p}/{SLUG}/'
    head, rest = tpl.split('</head>', 1)
    head = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(t["title"])}</title>', head)
    for k in ('name="description"', 'property="og:description"'):
        head = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc']), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(t['title']), head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', f'\\g<1>{BASE}/catharsis/fotos/catharsis-930-1.jpg', head)
    head = re.sub(r'<meta property="og:image:width"[^>]*>\n?<meta property="og:image:height"[^>]*>', '<meta property="og:image:width" content="1400">\n<meta property="og:image:height" content="788">', head)
    head = head.replace('/barcos-nuevos/', f'/{SLUG}/')
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f"{BASE}{p}/"},
            {"@type": "ListItem", "position": 2, "name": t['crumbs'][1], "item": f"{BASE}{p}/barcos/"},
            {"@type": "ListItem", "position": 3, "name": t['h1'], "item": url}]},
        {"@context": "https://schema.org", "@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": t['title'],
         "description": t['desc'], "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"},
         "hasPart": [{"@type": "WebPage", "name": b['name'], "url": f"{BASE}{p}/{b['slug']}/"} for b in BRANDS]},
    ]
    head = head.replace('<style>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '<style>', 1)
    head = head.replace('</style>', CSS + '</style>', 1)

    body = re.sub(r'(<div class="langsw".*?</div>)', lambda m: m.group(1).replace('/barcos-nuevos/', f'/{SLUG}/'), rest, count=1, flags=re.S)
    cards = ''
    for b in BRANDS:
        h = f'{p}/{b["slug"]}/'
        cards += f'''
      <article class="mk-c">
        <a class="mk-ph" href="{h}" tabindex="-1" aria-hidden="true"><img src="{b['img']}" alt="{html.escape(b['alt'])}" width="{b['w']}" height="{b['h']}" loading="lazy" decoding="async"></a>
        <div class="mk-b">
          <p class="nv-kick">{html.escape(b['kick'][li])}</p>
          <h2><a href="{h}">{b['name']}</a></h2>
          <p class="d">{html.escape(b['d'][li])}</p>
          <p class="pr">{t['from_']} {price(b['price'], lang, t)} <span class="vat">{VAT[lang]}</span><small>{b['note'][li]}</small></p>
          <a class="btn" href="{h}">{t['see']}</a>
        </div>
      </article>'''
    main = f'''<main class="boat">
  <div class="wrap">
    <p class="crumb"><a href="{p}/">{t['crumbs'][0]}</a> · <a href="{p}/barcos/">{t['crumbs'][1]}</a> · {html.escape(t['h1'])}</p>
    <div class="head">
      <div>
        <p class="eyebrow">{t['eyebrow']}</p>
        <h1>{html.escape(t['h1'])}</h1>
      </div>
    </div>
    <p class="nv-intro">{html.escape(t['intro'])}</p>
    <div class="mk-grid">{cards}
    </div>
    <div class="nv-used">
      <h2>{html.escape(t['used_h'])}</h2>
      <a class="btn btn-ghost" href="{p}/barcos/#segunda-mano">{t['used_a']}</a>
    </div>
    <p class="nv-small">{html.escape(t['small'])}</p>
  </div>
</main>'''
    body = re.sub(r'<main class="boat">.*?</main>', lambda m: main, body, flags=re.S)
    out = head + '</head>' + body
    assert 'skipper' not in re.sub(r'<header class="top">.*?</header>', '', out, flags=re.S).lower(), lang
    os.makedirs(f'{ROOT}{p}/{SLUG}', exist_ok=True)
    open(f'{ROOT}{p}/{SLUG}/index.html', 'w', encoding='utf-8').write(out)
    print('ok', lang, len(out))


for l in LANGS:
    build(l)
