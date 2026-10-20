#!/usr/bin/env python3
"""Genera /barcos-nuevos/ (ES/CA/EN/FR): la página única de barcos nuevos, con todas las marcas al mismo nivel
(SeaStorm, Sunrise, Catharsis y SKIPPER), cada una con su foto, frase, precio "desde" y sus modelos.
Los datos de Sunrise, SeaStorm y Catharsis salen de sus generadores (build_sunrise.py, build_seastorm.py,
build_catharsis.py); los de SKIPPER están aquí abajo. Cabecera y pie salen de la propia página (se regenera sobre sí misma).
OJO: build_sunrise.py, build_catharsis.py y build_seastorm.py usan esta página como plantilla de cabecera y pie:
después de cambiarla, volver a lanzarlos.
Uso (desde la raíz del repo): python3 _tools/build_barcos_nuevos.py"""
import re, json, html, os, sys, glob, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_sunrise as SR      # noqa: E402
import build_seastorm as SS     # noqa: E402
import build_catharsis as CT    # noqa: E402

ROOT = '.'
BASE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
LI = ['es', 'ca', 'en', 'fr']
WA = '34633742973'
VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': 'HT'}


def eur(n, lang):
    s = f'{n:,}'
    if lang == 'en':
        return '€' + s
    if lang == 'fr':
        return s.replace(',', '&nbsp;') + '&nbsp;€'
    return s.replace(',', '.') + '&nbsp;€'


def num(s, lang):
    return s.replace(',', '.') if lang == 'en' else s


def img_size(path):
    try:
        from PIL import Image
        return Image.open(ROOT + path).size
    except Exception:
        return (800, 600)


def first_clause(s):
    s = s.split('. ')[0].split(':')[0].rstrip(' . ')
    return s + '.'


# ---------- SKIPPER (precios del configurador oficial, oct 2026) ----------
SKIPPER_MODELS = [
    ('ace-360', 'SKIPPER ACE 360', '/skipper/fotos/g/ace360-02-t.jpg', 329000,
     ('El más ágil y el más compacto: 10,85 m.', 'El més àgil i el més compacte: 10,85 m.', 'The most agile and the most compact: 10.85 m.', 'Le plus agile et le plus compact : 10,85 m.')),
    ('38-nc', 'SKIPPER 38 NC+', '/skipper/fotos/g/38nc-01-t.jpg', 423000,
     ('El más protegido: hardtop de carbono con parabrisas de cristal.', 'El més protegit: hardtop de carboni amb parabrisa de vidre.', 'The most protected: carbon hardtop with a glass windscreen.', 'Le plus protégé : hardtop en carbone avec pare-brise en verre.')),
    ('42-nc', 'SKIPPER 42 NC', '/skipper/fotos/g/42nc-02-t.jpg', 588000,
     ('El buque insignia: cama doble y baño con ducha en la consola.', 'El vaixell insígnia: llit doble i bany amb dutxa a la consola.', 'The flagship: double bed and bathroom with shower in the console.', 'Le navire amiral : lit double et salle d’eau avec douche dans la console.')),
]

KICK = ('De {} a {} m', 'De {} a {} m', 'From {} to {} m', 'De {} à {} m')  # sin país de fabricación (decisión de Juan, 20 oct 2026)
DESC = {
    'seastorm': ('Botes de polietileno de una sola pieza: ligeros, con muy poco mantenimiento y buenos para acercarse a la playa. Cuatro modelos.',
                 'Bots de polietilè d’una sola peça: lleugers, amb molt poc manteniment i bons per acostar-se a la platja. Quatre models.',
                 'One-piece polyethylene boats: light, very low maintenance and easy to bring up to the beach. Four models.',
                 'Bateaux en polyéthylène d’une seule pièce : légers, très peu d’entretien et faciles à approcher de la plage. Quatre modèles.'),
    'sunrise': ('Barcos pequeños, sencillos y fáciles de mantener: opens, tenders, un bowrider y cabinados. Ocho modelos.',
                'Vaixells petits, senzills i fàcils de mantenir: opens, tenders, un bowrider i cabinats. Vuit models.',
                'Small, simple boats that are easy to look after: opens, tenders, a bowrider and cabin boats. Eight models.',
                'Petits bateaux simples et faciles à entretenir : opens, tenders, un bowrider et des bateaux à cabine. Huit modèles.'),
    'catharsis': ('Crucero fueraborda con timonera, dos camarotes y baño, para pasar el día o unos días a bordo.',
                  'Creuer fora borda amb timonera, dos camarots i bany, per passar el dia o uns dies a bord.',
                  'Outboard cruiser with a wheelhouse, two cabins and a bathroom, for day trips or a few days on board.',
                  'Cruiser hors-bord avec timonerie, deux cabines et salle d’eau, pour la journée ou quelques jours à bord.'),
    'skipper': ('Semirrígidas con casco de 4 escalones. Tres modelos, que se piden a fábrica con la motorización que elijas.',
                'Semirígides amb buc de 4 esglaons. Tres models, que es demanen a fàbrica amb la motorització que triïs.',
                'RIBs with a 4-step hull. Three models, ordered from the factory with the engines you choose.',
                'Semi-rigides avec carène à 4 redans. Trois modèles, commandés à l’usine avec la motorisation de votre choix.'),
}
NOTE = {
    'sunrise': ('sin motor', 'sense motor', 'without engine', 'sans moteur'),
    'catharsis': ('sin motores', 'sense motors', 'without engines', 'sans moteurs'),
    'skipper': ('con motores', 'amb motors', 'with engines', 'avec moteurs'),
}
WA_BRAND = ('Hola Juan, me interesa un barco {}. ¿Me ayudas a elegir modelo?', 'Hola Juan, m’interessa un vaixell {}. M’ajudes a triar model?',
            'Hi Juan, I am interested in a {} boat. Can you help me choose the model?', 'Bonjour Juan, un bateau {} m’intéresse. Pouvez-vous m’aider à choisir le modèle ?')
CATH_TXT = ('9,30 m · timonera, dos camarotes y baño.', '9,30 m · timonera, dos camarots i bany.', '9.30 m · wheelhouse, two cabins and a bathroom.', '9,30 m · timonerie, deux cabines et salle d’eau.')


def brands(lang):
    """Lista de marcas (orden por tamaño, de la más pequeña a la más grande) con sus modelos, para un idioma."""
    li = LI.index(lang)
    p = LANGS[lang]
    out = []
    # SeaStorm
    ms = []
    for m in SS.M:
        slug, name, L, price = m[0], m[1], m[2], m[12]
        ph = f'/seastorm/fotos/{slug}-1-m.jpg'
        ms.append(dict(name=name, href=f'{p}/seastorm/#seastorm-{slug}', img=ph if os.path.exists(ROOT + ph) else None,
                       txt=f'{num(L, lang)} m · {SS.T[lang]["tag"][slug]}.', price=price))
    out.append(dict(key='seastorm', name='SeaStorm', href=f'{p}/seastorm/', quote=f'{p}/seastorm/#presupuesto',
                    img='/seastorm/fotos/portada.jpg', srcset=None, alt='SeaStorm',
                    logo=('/seastorm/fotos/seastorm-logo.png', 840, 60),
                    size=(SS.M[0][2], SS.M[-1][2]), note=SS.T[lang]['hnote'], models=ms))
    # Sunrise (de menor a mayor)
    ms = []
    for slug, name, L, B, pax, hp, price, nph, lic, inc in sorted(SR.M, key=lambda m: (m[6], m[2])):
        ms.append(dict(name=f'Sunrise {name}', href=f'{p}/sunrise/#sunrise-{slug}', img=f'/sunrise/fotos/{slug}-1-m.jpg', contain=True,
                       txt=f'{num(L, lang)} m · {first_clause(SR.T[lang]["d"][slug])}', price=price))
    lens = sorted(m[2] for m in SR.M)
    out.append(dict(key='sunrise', name='Sunrise', href=f'{p}/sunrise/', quote=None, img='/sunrise/fotos/645-1-m.jpg', srcset='/sunrise/fotos/645-1-m.jpg 800w, /sunrise/fotos/645-1.jpg 1000w', alt='Sunrise 645',
                    logo=('/sunrise/fotos/sunrise-logo.png', 400, 136), size=(lens[0], lens[-1]), note=NOTE['sunrise'][li], models=ms))
    # Catharsis
    out.append(dict(key='catharsis', name='Catharsis', href=f'{p}/catharsis/', quote=None,
                    img='/catharsis/fotos/catharsis-930-1-m.jpg', srcset='/catharsis/fotos/catharsis-930-1-m.jpg 800w, /catharsis/fotos/catharsis-930-1.jpg 1400w', alt='Catharsis 930',
                    logo=None, size=('9,30', None), note=NOTE['catharsis'][li],
                    models=[dict(name='Catharsis 930', href=f'{p}/catharsis/', img='/catharsis/fotos/catharsis-930-2-m.jpg', txt=CATH_TXT[li], price=CT.PRICE)]))
    # SKIPPER
    out.append(dict(key='skipper', name='SKIPPER Powerboats', href=f'{p}/skipper/', quote=f'{p}/skipper/#presupuesto',
                    img='/skipper/fotos/42-aerea-m.jpg', srcset='/skipper/fotos/42-aerea-m.jpg 900w, /skipper/fotos/42-aerea.jpg 1920w', alt='SKIPPER 42 NC',
                    logo=('/skipper/fotos/skipper-logo-btp.png', 834, 189), size=('10,85', '12,40'), note=NOTE['skipper'][li],
                    models=[dict(name=n, href=f'{p}/skipper/{s}/', img=im, txt=tx[li], price=pr) for s, n, im, pr, tx in SKIPPER_MODELS]))
    for b in out:
        b['price'] = min(m['price'] for m in b['models'])
        a_, z_ = b['size']
        b['kick'] = KICK[li].format(num(a_, lang), num(z_, lang)) if z_ else f'{num(a_, lang)} m'
        if b['key'] == 'catharsis':
            b['kick'] += ' · Avila Marin'
        b['d'] = DESC[b['key']][li]
        if b['quote'] is None:  # sin formulario propio: presupuesto por WhatsApp
            txt = CT.T[lang]['wa_txt'] if b['key'] == 'catharsis' else WA_BRAND[li].format(b['name'])
            b['quote'] = 'https://wa.me/' + WA + '?text=' + urllib.parse.quote(txt, safe='')
    return out


T = {
 'es': dict(
  title='Barcos nuevos: SeaStorm, Sunrise, Catharsis y SKIPPER · Plata Marine',
  desc='Barcos nuevos por encargo de SeaStorm, Sunrise, Catharsis y SKIPPER, de {min_len} a {max_len} m, desde {min_price} +IVA. Te ayudo a elegir modelo y motor, y gestiono la compra.',
  crumbs=('Inicio', 'Barcos en venta', 'Barcos nuevos'), eyebrow='Barcos en venta', h1='Barcos nuevos',
  intro='Barcos nuevos que se piden directamente a fábrica, con el motor y el equipamiento que elijas. Trabajo con cuatro marcas, de {min_len} a {max_len} m: te ayudo a escoger el modelo y me ocupo de gestionar la compra.',
  tabs=('Tipo de barco', 'Barcos nuevos', 'Segunda mano'), jump='Las marcas',
  from_='Desde', models='Los modelos', model_one='El modelo', go='Ver el barco →', see='Ver {}: fotos y precios', quote='Pedir presupuesto', nophoto='Fotos pronto',
  used_h='¿Buscas un barco de ocasión?', used_a='Ver barcos de segunda mano →',
  small='Precios orientativos de octubre de 2026, sin IVA y en fábrica. SKIPPER: según su configurador oficial, con la motorización más económica. SeaStorm, Sunrise y Catharsis: sin motor (salvo el Sunrise 700 ECO Tender, que lo lleva incluido); SeaStorm, en versión Advantage. No incluyen equipamiento opcional, transporte, matriculación ni el IEDMT cuando corresponda. Pueden cambiar y no son vinculantes: el precio final es el del presupuesto por escrito o la oferta oficial del astillero. Podemos equivocarnos; si ves un error, avísanos.'),
 'ca': dict(
  title='Vaixells nous: SeaStorm, Sunrise, Catharsis i SKIPPER · Plata Marine',
  desc='Vaixells nous per encàrrec de SeaStorm, Sunrise, Catharsis i SKIPPER, de {min_len} a {max_len} m, des de {min_price} +IVA. T’ajudo a triar model i motor, i gestiono la compra.',
  crumbs=('Inici', 'Vaixells en venda', 'Vaixells nous'), eyebrow='Vaixells en venda', h1='Vaixells nous',
  intro='Vaixells nous que es demanen directament a fàbrica, amb el motor i l’equipament que triïs. Treballo amb quatre marques, de {min_len} a {max_len} m: t’ajudo a escollir el model i m’ocupo de gestionar la compra.',
  tabs=('Tipus de vaixell', 'Vaixells nous', 'Segona mà'), jump='Les marques',
  from_='Des de', models='Els models', model_one='El model', go='Veure el vaixell →', see='Veure {}: fotos i preus', quote='Demanar pressupost', nophoto='Fotos aviat',
  used_h='Busques un vaixell d’ocasió?', used_a='Veure vaixells de segona mà →',
  small='Preus orientatius d’octubre de 2026, sense IVA i a fàbrica. SKIPPER: segons el seu configurador oficial, amb la motorització més econòmica. SeaStorm, Sunrise i Catharsis: sense motor (excepte el Sunrise 700 ECO Tender, que el porta inclòs); SeaStorm, en versió Advantage. No inclouen equipament opcional, transport, matriculació ni l’IEDMT quan correspongui. Poden canviar i no són vinculants: el preu final és el del pressupost per escrit o l’oferta oficial de la drassana. Ens podem equivocar; si hi veus un error, avisa’ns.'),
 'en': dict(
  title='New boats: SeaStorm, Sunrise, Catharsis and SKIPPER · Plata Marine',
  desc='New boats built to order by SeaStorm, Sunrise, Catharsis and SKIPPER, from {min_len} to {max_len} m, from {min_price} +VAT. I help you choose the model and engine and handle the purchase.',
  crumbs=('Home', 'Boats for sale', 'New boats'), eyebrow='Boats for sale', h1='New boats',
  intro='New boats ordered directly from the factory, with the engine and equipment you choose. I work with four brands, from {min_len} to {max_len} m: I help you pick the model and take care of the purchase.',
  tabs=('Type of boat', 'New boats', 'Pre-owned'), jump='The brands',
  from_='From', models='The models', model_one='The model', go='See the boat →', see='See {}: photos and prices', quote='Request a quote', nophoto='Photos soon',
  used_h='Looking for a used boat?', used_a='See pre-owned boats →',
  small='Indicative prices as of October 2026, ex-works and excluding VAT. SKIPPER: from its official configurator, with the most affordable engine package. SeaStorm, Sunrise and Catharsis: without engine (except the Sunrise 700 ECO Tender, which includes it); SeaStorm, Advantage version. They exclude optional equipment, transport, registration and, where it applies, the Spanish IEDMT tax. They may change and are not binding: the final price is the one in the written quote or the shipyard’s official offer. We can make mistakes; if you spot one, please let us know.'),
 'fr': dict(
  title='Bateaux neufs : SeaStorm, Sunrise, Catharsis et SKIPPER · Plata Marine',
  desc='Bateaux neufs sur commande de SeaStorm, Sunrise, Catharsis et SKIPPER, de {min_len} à {max_len} m, à partir de {min_price} HT. Je vous aide à choisir modèle et moteur, et je gère l’achat.',
  crumbs=('Accueil', 'Bateaux à vendre', 'Bateaux neufs'), eyebrow='Bateaux à vendre', h1='Bateaux neufs',
  intro='Des bateaux neufs commandés directement à l’usine, avec le moteur et l’équipement de votre choix. Je travaille avec quatre marques, de {min_len} à {max_len} m : je vous aide à choisir le modèle et je m’occupe de gérer l’achat.',
  tabs=('Type de bateau', 'Bateaux neufs', 'Occasion'), jump='Les marques',
  from_='À partir de', models='Les modèles', model_one='Le modèle', go='Voir le bateau →', see='Voir {} : photos et prix', quote='Demander un devis', nophoto='Photos bientôt',
  used_h='Vous cherchez un bateau d’occasion ?', used_a='Voir les bateaux d’occasion →',
  small='Prix indicatifs d’octobre 2026, départ usine et hors TVA. SKIPPER : selon son configurateur officiel, avec la motorisation la plus abordable. SeaStorm, Sunrise et Catharsis : sans moteur (sauf le Sunrise 700 ECO Tender, qui l’inclut) ; SeaStorm, en version Advantage. Hors options, transport, immatriculation et, le cas échéant, taxe espagnole IEDMT. Ils peuvent changer et ne sont pas contractuels : le prix final est celui du devis écrit ou de l’offre officielle du chantier. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous.'),
}

CSS = """
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.langsw{display:flex;gap:6px;align-items:center;font-size:.78rem;font-weight:600}
.langsw a{padding:3px 7px;border-radius:4px;text-decoration:none;color:inherit;opacity:.65}
.langsw a[aria-current="page"]{opacity:1;text-decoration:underline}
.nv-intro{max-width:64ch;color:var(--ink-2)}
.nv-tabs{display:inline-flex;margin:22px 0 0;border:1px solid rgba(127,146,158,.45);border-radius:999px;overflow:hidden;font-family:var(--display);font-size:.92rem;font-weight:600;max-width:100%}
.nv-tabs a,.nv-tabs span{padding:9px 18px;text-decoration:none;color:var(--ink);white-space:nowrap}
.nv-tabs span{background:var(--ink);color:#fff}
.nv-tabs a:hover{background:var(--paper-2)}
.nv-jump{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:22px}
.nv-jump a{display:flex;flex-direction:column;gap:2px;padding:12px 14px;background:#fff;border:1px solid rgba(127,146,158,.28);border-radius:var(--radius);text-decoration:none;color:inherit;transition:border-color .15s,transform .15s}
.nv-jump a:hover{border-color:rgba(127,146,158,.6);transform:translateY(-1px)}
.nv-jump strong{font-family:var(--display);font-size:1.05rem;font-weight:700;line-height:1.15}
.nv-jump a>span{font-size:.85rem;color:var(--ink-2)}
.nv-jump b{font-family:var(--display);font-size:.9rem;font-weight:700;margin-top:2px}
.nv-brand{margin-top:28px;background:#fff;border:1px solid rgba(127,146,158,.28);border-radius:var(--radius);overflow:hidden;scroll-margin-top:86px}
.nv-ph{position:relative;display:block;background:#0b1620}
.nv-ph img.ph{display:block;width:100%;height:auto;aspect-ratio:16/9;max-height:440px;object-fit:cover}
.nv-ph::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(6,8,11,.62) 0,rgba(6,8,11,0) 55%)}
.nv-ph img.logo{position:absolute;left:clamp(16px,3vw,28px);bottom:clamp(14px,3vw,26px);z-index:1;height:clamp(26px,4vw,42px);width:auto;max-width:62%;object-fit:contain;object-position:left bottom}
.nv-ph img.logo.thin{height:clamp(14px,2.2vw,22px)}
.nv-body{padding:22px clamp(18px,3vw,28px) 26px}
.nv-kick{font-family:var(--display);font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--sea);margin:0 0 6px}
.nv-body h2{font-size:clamp(1.5rem,3vw,2rem);font-weight:700;font-stretch:90%;line-height:1.1}
.nv-body>p.d{color:var(--ink-2);margin-top:10px;max-width:70ch}
.nv-pr{font-family:var(--display);font-weight:700;font-size:1.25rem;margin-top:12px}
.nv-pr small{font-weight:500;font-size:.8rem;color:var(--ink-2);margin-left:6px}
.vat{color:#C62828;font-weight:800;font-size:.8em;margin-left:5px}
.nv-mh{font-family:var(--display);font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-2);margin:24px 0 10px}
.nv-models{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.nv-m{display:flex;flex-direction:column;border:1px solid rgba(127,146,158,.28);border-radius:var(--radius);overflow:hidden;text-decoration:none;color:inherit;background:#fff;transition:transform .15s,box-shadow .15s}
.nv-m:hover{transform:translateY(-2px);box-shadow:0 18px 30px -24px rgba(13,28,39,.5)}
.nv-m img{display:block;width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;background:var(--paper-2)}
.nv-m .nv-noph{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;aspect-ratio:16/10;background:#0E3042;color:rgba(255,255,255,.75);font-size:.78rem;padding:0}
.nv-m .nv-noph img{width:66%;height:auto;aspect-ratio:auto;background:none;min-height:0}
.nv-m>div{padding:12px 14px 14px;display:flex;flex-direction:column;gap:4px;flex:1}
.nv-m h3{font-size:1.15rem;font-weight:700}
.nv-m p{font-size:.92rem;line-height:1.45;color:var(--ink-2);flex:1}
.nv-m b{font-family:var(--display);font-size:.98rem}
.nv-m .go{font-family:var(--display);font-size:.9rem;font-weight:600;color:var(--sea)}
.nv-cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.nv-cta .btn-pri{background:var(--ink);color:#fff}
.nv-cta .btn-pri:hover{background:var(--sea)}
.nv-used{margin-top:36px;padding:22px 24px;border-left:3px solid var(--brass);background:#fff;border-radius:0 var(--radius) var(--radius) 0;max-width:70ch}
.nv-used h2{font-size:1.3rem;font-weight:650}
.nv-used .btn{margin-top:14px}
.nv-small{font-size:.8rem;line-height:1.55;color:var(--ink-2);margin:28px 0 48px;max-width:90ch}
@media (min-width:821px){.nv-m img.ct{object-fit:contain;background:#fff}}
@media (max-width:900px){.nv-jump{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:820px){.nv-models{grid-template-columns:1fr}.nv-m{flex-direction:row}.nv-m>img,.nv-m>.nv-noph{width:38%;aspect-ratio:auto;min-height:100%;flex:none}.nv-m>div{padding:10px 12px}}
@media (max-width:640px){.nv-cta .btn{flex:1 1 100%;text-align:center}.nv-tabs{display:flex}.nv-tabs a,.nv-tabs span{flex:1;text-align:center;padding:9px 10px}.nv-jump{gap:8px}.nv-jump a{padding:10px 12px}}
"""


def rng(a, b, lang, t):
    if not b:
        return f'{num(a, lang)} m'
    return f'{num(a, lang)}–{num(b, lang)} m'


def build(lang):
    p = LANGS[lang]
    t = T[lang]
    vat = VAT[lang]
    B = brands(lang)
    allm = [m for b in B for m in b['models']]
    lens = [b['size'][0] for b in B] + [b['size'][1] for b in B if b['size'][1]]
    lens = sorted(lens, key=lambda s: float(s.replace(',', '.')))
    fill = dict(min_len=num(lens[0], lang), max_len=num(lens[-1], lang), min_price=eur(min(m['price'] for m in allm), lang).replace('&nbsp;', ' '))
    title, desc, intro = t['title'], t['desc'].format(**fill), t['intro'].format(**fill)
    url = f'{BASE}{p}/barcos-nuevos/'
    path = f'{ROOT}{p}/barcos-nuevos/index.html'
    tpl = open(path, encoding='utf-8').read()
    head, rest = tpl.split('</head>', 1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title, quote=False)}</title>', head)
    for k in ('name="description"', 'property="og:description"'):
        head = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + html.escape(desc), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(title), head)
    head = re.sub(r'<style>.*?</style>', lambda m: '<style>' + CSS + '</style>', head, count=1, flags=re.S)
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f"{BASE}{p}/"},
            {"@type": "ListItem", "position": 2, "name": t['crumbs'][1], "item": f"{BASE}{p}/barcos/"},
            {"@type": "ListItem", "position": 3, "name": t['crumbs'][2], "item": url}]},
        {"@context": "https://schema.org", "@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": title,
         "description": desc, "inLanguage": lang, "isPartOf": {"@id": f"{BASE}/#website"},
         "hasPart": [{"@type": "WebPage", "name": b['name'], "url": BASE + b['href']} for b in B],
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": m['name'], "url": BASE + m['href']} for i, m in enumerate(allm)]}},
    ]
    head = head.replace('<style>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '<style>', 1)

    jump = ''.join(f'<a href="#marca-{b["key"]}"><strong>{html.escape(b["name"].replace(" Powerboats", ""))}</strong><span>{rng(*b["size"], lang, t)}</span>'
                   f'<b>{t["from_"]} {eur(b["price"], lang)} <span class="vat">{vat}</span></b></a>' for b in B)
    secs = ''
    for n, b in enumerate(B):
        first = n == 0
        w, h = img_size(b['img'])
        ss = f' srcset="{b["srcset"]}" sizes="(max-width:1120px) 100vw, 1024px"' if b['srcset'] else ''
        load = ' decoding="async" fetchpriority="high"' if first else ' loading="lazy" decoding="async"'
        logo = ''
        if b['logo']:
            lsrc, lw, lh = b['logo']
            logo = f'<img class="logo{" thin" if lw / lh > 8 else ""}" src="{lsrc}" alt="{html.escape(b["name"])}" width="{lw}" height="{lh}">'
        cards = ''
        for m in b['models']:
            if m['img']:
                mw, mh = img_size(m['img'])
                pic = f'<img{" class=" + chr(34) + "ct" + chr(34) if m.get("contain") else ""} src="{m["img"]}" alt="{html.escape(m["name"])}" width="{mw}" height="{mh}" loading="lazy" decoding="async">'
            else:
                lsrc, lw, lh = b['logo']
                pic = f'<span class="nv-noph"><img src="{lsrc}" alt="" width="{lw}" height="{lh}" loading="lazy" decoding="async">{t["nophoto"]}</span>'
            cards += (f'<a class="nv-m" href="{m["href"]}">{pic}<div><h3>{html.escape(m["name"])}</h3><p>{html.escape(m["txt"], quote=False)}</p>'
                      f'<b>{t["from_"]} {eur(m["price"], lang)} <span class="vat">{vat}</span></b><span class="go">{t["go"]}</span></div></a>')
        ext = ' target="_blank" rel="noopener"' if b['quote'].startswith('https://wa.me/') else ''
        short = b['name'].replace(' Powerboats', '')
        secs += f'''
    <section class="nv-brand" id="marca-{b['key']}" aria-labelledby="nv-{b['key']}">
      <a class="nv-ph" href="{b['href']}" tabindex="-1" aria-hidden="true"><img class="ph" src="{b['img']}"{ss} alt="{html.escape(b['alt'])}" width="{w}" height="{h}"{load}>{logo}</a>
      <div class="nv-body">
        <p class="nv-kick">{html.escape(b['kick'])}</p>
        <h2 id="nv-{b['key']}">{html.escape(b['name'])}</h2>
        <p class="d">{html.escape(b['d'], quote=False)}</p>
        <p class="nv-pr">{t['from_']} {eur(b['price'], lang)} <span class="vat">{vat}</span><small>{html.escape(b['note'])}</small></p>
        <p class="nv-mh">{t['models'] if len(b['models']) > 1 else t['model_one']}</p>
        <div class="nv-models">{cards}</div>
        <div class="nv-cta"><a class="btn btn-pri" href="{b['href']}">{html.escape(t['see'].format(short))}</a><a class="btn btn-ghost" href="{html.escape(b['quote'])}"{ext}>{t['quote']}</a></div>
      </div>
    </section>
'''
    main = f'''<main class="boat">
  <div class="wrap">
    <p class="crumb"><a href="{p}/">{t['crumbs'][0]}</a> · <a href="{p}/barcos/">{t['crumbs'][1]}</a> · {t['crumbs'][2]}</p>
    <div class="head">
      <div>
        <p class="eyebrow">{t['eyebrow']}</p>
        <h1>{t['h1']}</h1>
      </div>
    </div>
    <p class="nv-intro">{html.escape(intro, quote=False)}</p>
    <nav class="nv-tabs" aria-label="{t['tabs'][0]}"><span aria-current="page">{t['tabs'][1]}</span><a href="{p}/barcos/#segunda-mano">{t['tabs'][2]}</a></nav>
    <nav class="nv-jump" aria-label="{t['jump']}">{jump}</nav>
{secs}
    <div class="nv-used">
      <h2>{html.escape(t['used_h'], quote=False)}</h2>
      <a class="btn btn-ghost" href="{p}/barcos/#segunda-mano">{t['used_a']}</a>
    </div>

    <p class="nv-small">{html.escape(t['small'], quote=False)}</p>
  </div>
</main>'''
    body = re.sub(r'<main class="boat">.*?</main>', lambda m: main, rest, count=1, flags=re.S)
    out = head + '</head>' + body
    open(path, 'w', encoding='utf-8').write(out)
    print('ok', lang, len(out))


if __name__ == '__main__':
    for l in LANGS:
        build(l)
