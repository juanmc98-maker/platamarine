#!/usr/bin/env python3
"""Genera /catharsis/ en ES/CA/EN/FR a partir de la plantilla de /barcos-nuevos/.
Uso: python3 _tools/build_catharsis.py  (desde la raíz del repo)"""
import re, json, html, urllib.parse, os

ROOT = '.'
BASE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
WA = '34633742973'
SLUG = 'catharsis'
NPH = 10
PRICE = 94990  # PVP sin IVA y sin motores (confirmado por Juan, 20 oct 2026)

def eur(n, lang):
    s = f'{n:,}'
    if lang == 'en':
        return s
    if lang == 'fr':
        return s.replace(',', '\u202f')
    return s.replace(',', '.')

SPEC = {  # dato: (es, ca, en, fr) etiqueta, valor común
 'loa': (('Eslora total', 'Eslora total', 'Length overall', 'Longueur hors tout'), '9,30 m'),
 'lh': (('Eslora de casco', 'Eslora de buc', 'Hull length', 'Longueur de coque'), '9,10 m'),
 'beam': (('Manga', 'Mànega', 'Beam', 'Largeur'), '3,00 m'),
 'draft': (('Calado', 'Calat', 'Draft', 'Tirant d\'eau'), '0,70 – 0,80 m'),
 'head': (('Altura en cabina', 'Alçada a cabina', 'Cabin headroom', 'Hauteur sous barrots'), '1,90 m'),
 'pax': (('Personas', 'Persones', 'People', 'Personnes'), '8'),
 'ce': (('Marcado CE', 'Marcatge CE', 'CE marking', 'Marquage CE'), ('Categoría C (según el astillero)', 'Categoria C (segons la drassana)', 'Category C (as stated by the builder)', 'Catégorie C (selon le chantier)')),
 'fuel': (('Combustible', 'Combustible', 'Fuel', 'Carburant'), '2 × 225 l'),
 'water': (('Agua dulce', 'Aigua dolça', 'Fresh water', 'Eau douce'), '300 l'),
 'black': (('Aguas negras', 'Aigües negres', 'Black water', 'Eaux noires'), '140 l'),
 'weight': (('Peso sin motores', 'Pes sense motors', 'Weight without engines', 'Poids sans moteurs'), ('4.200 kg', '4.200 kg', '4,200 kg', '4\u202f200 kg')),
 'power': (('Potencia máxima admitida', 'Potència màxima admesa', 'Maximum rated power', 'Puissance maximale admise'), ('447 kW (≈ 600 cv)', '447 kW (≈ 600 CV)', '447 kW (≈ 600 hp)', '447 kW (≈ 600 ch)')),
}
LI = ['es', 'ca', 'en', 'fr']

T = {
 'es': dict(
  title='Catharsis 930 nuevo: precio, ficha y fotos · Plata Marine',
  desc='Catharsis 930, crucero fueraborda de 9,30 m fabricado en Turquía por Avila Marin. Desde 94.990 € +IVA sin motores. Agente en Cataluña.',
  eyebrow='Barcos nuevos', h1='Catharsis 930: crucero fueraborda de 9,30 metros',
  intro='Un barco con timonera, dos camarotes y baño, pensado para pasar el día o unos días a bordo con la familia. Lo fabrica Avila Marin en Esmirna (Turquía) y se pide a fábrica: te ayudo a elegir motores y equipamiento. Soy su agente en Cataluña.',
  kick='Agente en Cataluña', h2='El barco',
  facts=['Fabricado en Turquía por Avila Marin', 'Casco por infusión al vacío', 'Dos camarotes, baño con ducha y cocina', 'Para dos motores fueraborda: no incluidos, se montan a tu elección con presupuesto aparte', 'Entrega: unos 90 días desde el pedido, más el transporte', 'Transporte desde Turquía hasta Barcelona: no incluido, se presupuesta aparte'],
  d='Timonera con puerta corredera de aluminio de tres hojas, bañera con mesa telescópica y ducha, camarote de proa con cama doble y camarote de invitados. De serie lleva molinete eléctrico, nevera, cocina de dos fuegos, WC eléctrico, focos LED, baterías de servicio y depósitos de acero inoxidable.',
  lic='PER o superior', lic_label='Titulación', price_from='Desde', no_eng='sin motores',
  cta='Pedir presupuesto', wa_txt='Hola Juan, me interesa el Catharsis 930.', photos='Fotos del Catharsis 930',
  opt_h='Equipamiento opcional', opt='Teca sintética, plataforma para auxiliar, luces submarinas, hélice de proa, flaps automáticos, calefacción diésel, toldos de verano e invierno, plotters Raymarine de 9" o 12", equipo de sonido Fusion y placas solares (420 W), entre otros. Te paso el precio de cada opción por escrito.',
  spec_h='Ficha técnica',
  used_h='¿Buscas un barco de ocasión?', used_a='Ver barcos de segunda mano →',
  small='Precio orientativo de octubre de 2026, sin IVA, en fábrica: no incluye motores, equipamiento opcional, transporte, impuesto de matriculación (IEDMT) ni matriculación. El transporte desde Turquía hasta Barcelona no está incluido y se presupuesta aparte. Los motores tampoco están incluidos: se montan a elección del cliente, con presupuesto aparte. Puede cambiar y no es vinculante; el precio final es el del presupuesto por escrito. Ficha técnica según el fabricante; el marcado CE de categoría C es el que indica el astillero. La titulación es orientativa según la eslora: confírmala con tu escuela o con Capitanía. Podemos equivocarnos; si ves un error, avísanos.',
 ),
 'ca': dict(
  title='Catharsis 930 nou: preu, fitxa i fotos · Plata Marine',
  desc='Catharsis 930, creuer fora borda de 9,30 m fabricat a Turquia per Avila Marin. Des de 94.990 € +IVA sense motors. Agent a Catalunya.',
  eyebrow='Vaixells nous', h1='Catharsis 930: creuer fora borda de 9,30 metres',
  intro='Un vaixell amb timonera, dos camarots i bany, pensat per passar el dia o uns dies a bord amb la família. El fabrica Avila Marin a Esmirna (Turquia) i es demana a fàbrica: t\'ajudo a triar motors i equipament. En sóc l\'agent a Catalunya.',
  kick='Agent a Catalunya', h2='El vaixell',
  facts=['Fabricat a Turquia per Avila Marin', 'Buc per infusió al buit', 'Dos camarots, bany amb dutxa i cuina', 'Per a dos motors fora borda: no inclosos, es munten a la teva elecció amb pressupost a part', 'Lliurament: uns 90 dies des de la comanda, més el transport', 'Transport des de Turquia fins a Barcelona: no inclòs, es pressuposta a part'],
  d='Timonera amb porta corredissa d\'alumini de tres fulles, banyera amb taula telescòpica i dutxa, camarot de proa amb llit doble i camarot de convidats. De sèrie porta molinet elèctric, nevera, cuina de dos focs, WC elèctric, focus LED, bateries de servei i dipòsits d\'acer inoxidable.',
  lic='PER o superior', lic_label='Titulació', price_from='Des de', no_eng='sense motors',
  cta='Demanar pressupost', wa_txt='Hola Juan, m\'interessa el Catharsis 930.', photos='Fotos del Catharsis 930',
  opt_h='Equipament opcional', opt='Teca sintètica, plataforma per a auxiliar, llums submarins, hèlix de proa, flaps automàtics, calefacció dièsel, tendals d\'estiu i d\'hivern, plotters Raymarine de 9" o 12", equip de so Fusion i plaques solars (420 W), entre d\'altres. Et passo el preu de cada opció per escrit.',
  spec_h='Fitxa tècnica',
  used_h='Busques un vaixell d\'ocasió?', used_a='Veure vaixells de segona mà →',
  small='Preu orientatiu d\'octubre de 2026, sense IVA, a fàbrica: no inclou motors, equipament opcional, transport, impost de matriculació (IEDMT) ni matriculació. El transport des de Turquia fins a Barcelona no està inclòs i es pressuposta a part. Els motors tampoc no hi estan inclosos: es munten a elecció del client, amb pressupost a part. Pot canviar i no és vinculant; el preu final és el del pressupost per escrit. Fitxa tècnica segons el fabricant; el marcatge CE de categoria C és el que indica la drassana. La titulació és orientativa segons l\'eslora: confirma-la amb la teva escola o amb Capitania. Ens podem equivocar; si hi veus un error, avisa\'ns.',
 ),
 'en': dict(
  title='New Catharsis 930: price, specs and photos · Plata Marine',
  desc='Catharsis 930, a 9.30 m outboard cruiser built in Turkey by Avila Marin. From €94,990 +VAT without engines. Agent in Catalonia.',
  eyebrow='New boats', h1='Catharsis 930: a 9.30-metre outboard cruiser',
  intro='A boat with a wheelhouse, two cabins and a bathroom, made for day trips or a few days on board with the family. Built by Avila Marin in Izmir (Turkey) and ordered from the factory: I help you choose engines and equipment. I am their agent in Catalonia.',
  kick='Agent in Catalonia', h2='The boat',
  facts=['Built in Turkey by Avila Marin', 'Vacuum-infused hull', 'Two cabins, bathroom with shower and galley', 'For twin outboard engines: not included, fitted to your choice and quoted separately', 'Delivery: about 90 days from order, plus transport', 'Transport from Turkey to Barcelona: not included, quoted separately'],
  d='Wheelhouse with a three-panel sliding aluminium door, cockpit with telescopic table and shower, forward cabin with double bed and a guest cabin. Standard equipment includes electric windlass, fridge, two-burner hob, electric toilet, LED searchlight, service batteries and stainless steel tanks.',
  lic='Spanish PER or higher', lic_label='Licence', price_from='From', no_eng='without engines',
  cta='Request a quote', wa_txt='Hi Juan, I am interested in the Catharsis 930.', photos='Photos of the Catharsis 930',
  opt_h='Optional equipment', opt='Synthetic teak, tender platform, underwater lights, bow thruster, automatic trim tabs, diesel heater, summer and winter covers, 9" or 12" Raymarine plotters, Fusion sound system and solar panels (420 W), among others. I will send you the price of each option in writing.',
  spec_h='Specifications',
  used_h='Looking for a used boat?', used_a='See used boats →',
  small='Indicative price as of October 2026, ex-works, excluding VAT: it does not include engines, optional equipment, transport, Spanish registration tax (IEDMT) or registration. Transport from Turkey to Barcelona is not included and is quoted separately. Engines are not included either: they are fitted to the customer\'s choice and quoted separately. It may change and is not binding; the final price is the one in the written quote. Specifications as stated by the builder; the CE category C marking is as declared by the builder. The licence shown is indicative, based on length under Spanish rules: please confirm it with your school or the Harbour Master. We may be wrong; if you spot an error, let us know.',
 ),
 'fr': dict(
  title='Catharsis 930 neuf : prix, fiche et photos · Plata Marine',
  desc='Catharsis 930, cruiser hors-bord de 9,30 m construit en Turquie par Avila Marin. À partir de 94 990 € HT sans moteurs. Agent en Catalogne.',
  eyebrow='Bateaux neufs', h1='Catharsis 930 : cruiser hors-bord de 9,30 mètres',
  intro='Un bateau avec timonerie, deux cabines et salle d\'eau, pensé pour la journée ou quelques jours à bord en famille. Construit par Avila Marin à Izmir (Turquie) et commandé à l\'usine : je vous aide à choisir les moteurs et l\'équipement. Je suis leur agent en Catalogne.',
  kick='Agent en Catalogne', h2='Le bateau',
  facts=['Construit en Turquie par Avila Marin', 'Coque en infusion sous vide', 'Deux cabines, salle d\'eau avec douche et cuisine', 'Pour deux moteurs hors-bord : non inclus, montés selon votre choix sur devis séparé', 'Livraison : environ 90 jours après la commande, plus le transport', 'Transport de la Turquie jusqu\'à Barcelone : non inclus, sur devis séparé'],
  d='Timonerie avec porte coulissante en aluminium à trois vantaux, cockpit avec table télescopique et douche, cabine avant avec lit double et cabine invités. En série : guindeau électrique, réfrigérateur, réchaud deux feux, WC électrique, projecteur LED, batteries de service et réservoirs en inox.',
  lic='PER espagnol ou supérieur', lic_label='Permis', price_from='À partir de', no_eng='sans moteurs',
  cta='Demander un devis', wa_txt='Bonjour Juan, le Catharsis 930 m\'intéresse.', photos='Photos du Catharsis 930',
  opt_h='Options', opt='Teck synthétique, plateforme pour annexe, éclairage sous-marin, propulseur d\'étrave, flaps automatiques, chauffage diesel, tauds été et hiver, traceurs Raymarine 9" ou 12", système audio Fusion et panneaux solaires (420 W), entre autres. Je vous envoie le prix de chaque option par écrit.',
  spec_h='Fiche technique',
  used_h='Vous cherchez un bateau d\'occasion ?', used_a='Voir les bateaux d\'occasion →',
  small='Prix indicatif d\'octobre 2026, départ usine, hors TVA : il n\'inclut pas les moteurs, les options, le transport, la taxe d\'immatriculation espagnole (IEDMT) ni l\'immatriculation. Le transport de la Turquie jusqu\'à Barcelone n\'est pas inclus et fait l\'objet d\'un devis séparé. Les moteurs ne sont pas inclus non plus : ils sont montés selon le choix du client, sur devis séparé. Il peut changer et n\'est pas contractuel ; le prix final est celui du devis écrit. Fiche technique selon le constructeur ; le marquage CE catégorie C est celui déclaré par le chantier. Le permis indiqué est indicatif, selon la longueur d\'après les règles espagnoles : vérifiez-le auprès de votre école ou de la Capitainerie. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous. Nous ne parlons pas français : nous utilisons un traducteur, merci de votre indulgence.',
 ),
}
VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': 'HT'}
HINT = {'es': 'Desliza para ver más fotos →', 'ca': 'Llisca per veure més fotos →', 'en': 'Swipe for more photos →', 'fr': 'Faites glisser pour plus de photos →'}
CSS = open(os.path.join(os.path.dirname(__file__), 'build_sunrise.py'), encoding='utf-8').read().split('CSS = """', 1)[1].split('"""', 1)[0] + """
.sr-m.one{grid-template-columns:minmax(0,1.3fr) minmax(0,1fr)}
.sr-gal.wide img{aspect-ratio:16/9;object-fit:cover}
.ct-spec{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px 24px;background:#0E3042;color:#fff;border-radius:var(--radius);padding:18px clamp(16px,2.5vw,24px);margin-top:18px}
.ct-spec div{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid rgba(255,255,255,.14);padding:7px 0;font-size:.93rem}
.ct-spec dt{color:rgba(255,255,255,.72)}.ct-spec dd{margin:0;font-weight:600;text-align:right}
.ct-opt{margin-top:18px;color:var(--ink-2);line-height:1.55}
@media (max-width:820px){.sr-m.one{grid-template-columns:1fr}}
@media (max-width:620px){.ct-spec{grid-template-columns:1fr}}
"""


def build(lang):
    p = LANGS[lang]
    li = LI.index(lang)
    tpl = open(f'{ROOT}{p}/barcos-nuevos/index.html', encoding='utf-8').read()
    t = T[lang]
    url = f'{BASE}{p}/{SLUG}/'
    head, rest = tpl.split('</head>', 1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(t["title"])}</title>', head)
    for k in ('name="description"', 'property="og:description"'):
        head = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc']), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(t['title']), head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', f'\\g<1>{BASE}/{SLUG}/fotos/catharsis-930-1.jpg', head)
    head = re.sub(r'<meta property="og:image:width"[^>]*>\n?<meta property="og:image:height"[^>]*>', '<meta property="og:image:width" content="1400">\n<meta property="og:image:height" content="788">', head)
    head = head.replace('/barcos-nuevos/', f'/{SLUG}/')
    crumbs = {'es': ('Inicio', 'Barcos en venta'), 'ca': ('Inici', 'Vaixells en venda'), 'en': ('Home', 'Boats for sale'), 'fr': ('Accueil', 'Bateaux à vendre')}[lang]
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f"{BASE}{p}/"},
            {"@type": "ListItem", "position": 2, "name": crumbs[1], "item": f"{BASE}{p}/barcos/"},
            {"@type": "ListItem", "position": 3, "name": "Catharsis 930", "item": url}]},
        {"@context": "https://schema.org", "@type": "Product", "name": "Catharsis 930", "brand": {"@type": "Brand", "name": "Catharsis"},
         "manufacturer": {"@type": "Organization", "name": "Avila Marin"}, "image": f"{BASE}/{SLUG}/fotos/catharsis-930-1.jpg", "description": t['d'],
         "offers": {"@type": "Offer", "price": str(PRICE), "priceCurrency": "EUR", "availability": "https://schema.org/PreOrder", "url": url,
                    "priceSpecification": {"@type": "PriceSpecification", "price": str(PRICE), "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}},
    ]
    head = head.replace('<style>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '<style>', 1)
    head = head.replace('</style>', CSS + '</style>', 1)

    body = rest.replace('/barcos-nuevos/" aria-current', f'/{SLUG}/" aria-current')
    body = re.sub(r'(<div class="langsw".*?</div>)', lambda m: m.group(1).replace('/barcos-nuevos/', f'/{SLUG}/'), body, flags=re.S)
    ph = 'foto' if lang in ('es', 'ca') else 'photo'
    imgs = ''.join(
        f'<img src="/{SLUG}/fotos/catharsis-930-{i}-m.jpg" srcset="/{SLUG}/fotos/catharsis-930-{i}-m.jpg 800w, /{SLUG}/fotos/catharsis-930-{i}.jpg 1400w" sizes="(max-width:820px) 100vw, 640px" alt="Catharsis 930 – {ph} {i}" loading="lazy" decoding="async">'
        for i in range(2, NPH + 1))
    wa = f'https://wa.me/{WA}?text=' + urllib.parse.quote(t['wa_txt'])
    spec = ''.join(f'<div><dt>{html.escape(lab[li])}</dt><dd>{html.escape(val[li] if isinstance(val, tuple) else (val.replace(",", ".") if lang == "en" else val))}</dd></div>' for k, (lab, val) in SPEC.items())
    facts = ''.join(f'<li>{html.escape(f)}</li>' for f in t['facts'])
    main = f'''<main class="boat">
  <div class="wrap">
    <p class="crumb"><a href="{p}/">{crumbs[0]}</a> · <a href="{p}/barcos/">{crumbs[1]}</a> · Catharsis 930</p>
    <div class="head">
      <div>
        <p class="eyebrow">{t['eyebrow']}</p>
        <h1>{html.escape(t['h1'])}</h1>
      </div>
    </div>
    <p class="nv-intro">{html.escape(t['intro'])}</p>
    <div class="sr-hero"><img class="ph" src="/{SLUG}/fotos/catharsis-930-1.jpg" alt="Catharsis 930" width="1400" height="788" decoding="async" fetchpriority="high"></div>
    <ul class="sr-facts">{facts}</ul>
    <p class="nv-mh">{t['kick']}</p>
    <h2 style="font-size:clamp(1.4rem,3vw,1.9rem);font-weight:700;margin-bottom:12px">{t['h2']}</h2>
    <article class="sr-m one" id="catharsis-930">
      <div><div class="sr-gal wide" aria-label="{html.escape(t['photos'])}">{imgs}</div></div>
      <div class="sr-b">
        <h3>Catharsis 930</h3>
        <p class="d">{html.escape(t['d'])}</p>
        <dl><dt>{t['lic_label']}</dt><dd>{html.escape(t['lic'])}</dd></dl>
        <p class="pr">{t['price_from']} {eur(PRICE, lang)} € <span class="vat">{VAT[lang]}</span><small>{t['no_eng']}</small></p>
        <p class="sr-hint">{HINT[lang]}</p>
        <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{t['cta']}</a>
      </div>
    </article>
    <h2 style="font-size:1.3rem;font-weight:700;margin-top:26px">{t['spec_h']}</h2>
    <dl class="ct-spec">{spec}</dl>
    <h2 style="font-size:1.3rem;font-weight:700;margin-top:26px">{t['opt_h']}</h2>
    <p class="ct-opt">{html.escape(t['opt'])}</p>
    <div class="nv-used">
      <h2>{html.escape(t['used_h'])}</h2>
      <a class="btn btn-ghost" href="{p}/barcos/#segunda-mano">{t['used_a']}</a>
    </div>
    <p class="nv-small">{html.escape(t['small'])}</p>
  </div>
</main>'''
    body = re.sub(r'<main class="boat">.*?</main>', lambda m: main, body, flags=re.S)
    out = head + '</head>' + body
    os.makedirs(f'{ROOT}{p}/{SLUG}', exist_ok=True)
    open(f'{ROOT}{p}/{SLUG}/index.html', 'w', encoding='utf-8').write(out)
    print('ok', lang, len(out))


for l in LANGS:
    build(l)
