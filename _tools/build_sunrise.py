#!/usr/bin/env python3
"""Genera /sunrise/ en ES/CA/EN/FR a partir de la plantilla de /barcos-nuevos/.
Uso: python3 _tools/build_sunrise.py  (desde la raíz del repo)
Después de generar, relanzar SIEMPRE _tools/sunrise_fotos.py (fotos y portada de oct 2026)."""
import re, json, html, urllib.parse

ROOT = '.'
BASE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
WA = '34633742973'

# slug, nombre, eslora, manga, personas, cv max, precio (+IVA), fotos, titulación (clave), motor incluido
M = [
 ('700-eco-tender', '700 ECO Tender', '7,00', '2,46', 10, None, 52990, 5, 'pnb', True),
 ('680-dc', '680 DC', '6,83', '2,50', 8, 250, 37990, 5, 'pnb', False),
 ('645', '645', '6,05', '2,45', 6, 200, 23990, 5, 'pnb', False),
 ('606-br', '606 BR', '6,07', '2,35', 7, 150, 21990, 5, 'pnb', False),
 ('530-open', '530 Open', '5,30', '2,10', 6, 115, 13990, 5, 'ln', False),
 ('545', '545', '5,40', '2,38', 6, 115, 13990, 5, 'ln', False),
 ('530-tender', '530 Tender', '5,30', '2,10', 8, 90, 12990, 5, 'ln', False),
 ('400-open', '400 Open', '4,00', '1,66', 5, 40, 5990, 5, 'sin', False),
]

def eur(n, lang):
    s = f'{n:,}'
    if lang == 'en':
        return s  # 52,990
    if lang == 'fr':
        return s.replace(',', '\u202f')  # 52 990
    return s.replace(',', '.')

def num(s, lang):
    return s.replace(',', '.') if lang == 'en' else s

T = {
 'es': dict(
  title='Barcos Sunrise nuevos de 4 a 7 m: precios y modelos · Plata Marine',
  desc='Barcos nuevos Sunrise de 4 a 7 m, desde 5.990 € +IVA. Distribuidor en Cataluña: te ayudo a elegir modelo, motor y equipamiento.',
  crumb_last='Sunrise', eyebrow='Barcos nuevos', h1='Sunrise: barcos nuevos de 4 a 7 metros',
  intro='Barcos sencillos y fáciles de mantener, fabricados por Sunrise Yacht. Se piden a fábrica y te ayudo a elegir el modelo, el motor y el equipamiento. Soy su distribuidor en Cataluña.',
  kick='Distribuidor en Cataluña', h2='Los modelos',
  facts=['Categoría de diseño CE: C (certifica PRS)', 'Entrega: de 4 a 12 semanas según modelo', 'Garantía: 3 años desde la entrega', 'Pago: 40 % al hacer el pedido y el resto cuando el barco está listo para el transporte', 'Transporte desde fábrica hasta Barcelona: unos 2.000 € por barco, aparte'],
  len='Eslora', beam='Manga', pax='Personas', hp='Motor', hp_max='hasta {} CV', hp_eco='Eléctrico, incluido',
  lic={'sin': 'Sin titulación con motor de hasta 15 CV (uso privado, de día, a 2 millas como máximo y mayor de 18 años); con más, Licencia de Navegación o superior', 'ln': 'Licencia de Navegación o superior', 'pnb': 'PNB o superior'},
  lic_label='Titulación', price_from='Desde', no_eng='sin motor', with_eng='motor incluido',
  cta='Pedir presupuesto', wa_txt='Hola Juan, me interesa el Sunrise {}.', photos='Fotos del {}',
  d={'700-eco-tender': 'Tender eléctrico con placas solares (1.800 W) y baterías de litio: sin emisiones, sin ruido y sin gasto de combustible. Lleva baño a bordo.',
     '680-dc': 'Day cruiser con depósito de 220 litros, solárium y bañera amplia. El más grande de gasolina.',
     '645': 'Cabinado con timonera cerrada, para salir también fuera de temporada. 6,50 m con plataformas.',
     '606-br': 'Bowrider con asientos a proa, dirección hidráulica y depósito de 100 litros.',
     '530-open': 'Open con consola y asiento de piloto, pensado para pesca y baño.',
     '545': 'Pequeño cabinado con techo y puerta de cabina, con 7 cofres para guardar el equipo.',
     '530-tender': 'Tender con colchonetas a proa y popa y consola central. Cabe una familia entera.',
     '400-open': 'Auxiliar de 4 m para pesca y paseos cerca de la costa. El más económico.'},
  used_h='¿Buscas un barco de ocasión?', used_a='Ver barcos de segunda mano →',
  small='Precios orientativos de octubre de 2026, sin IVA, en fábrica: no incluyen motor (salvo el 700 ECO Tender), equipamiento opcional, transporte ni matriculación. Pueden cambiar y no son vinculantes; el precio final es el del presupuesto por escrito. La titulación es orientativa según la eslora y la potencia: confírmala con tu escuela o con Capitanía. Límite sin titulación desde el 1 de octubre de 2026 (RD 1188/2025): hasta 5 m de eslora y 15 CV; orientativo, confirma con Capitanía. Podemos equivocarnos; si ves un error, avísanos.',
 ),
 'ca': dict(
  title='Vaixells Sunrise nous de 4 a 7 m: preus i models · Plata Marine',
  desc='Vaixells nous Sunrise de 4 a 7 m, des de 5.990 € +IVA. Distribuïdor a Catalunya: t\'ajudo a triar model, motor i equipament.',
  crumb_last='Sunrise', eyebrow='Vaixells nous', h1='Sunrise: vaixells nous de 4 a 7 metres',
  intro='Vaixells senzills i fàcils de mantenir, fabricats per Sunrise Yacht. Es demanen a fàbrica i t\'ajudo a triar el model, el motor i l\'equipament. En sóc el distribuïdor a Catalunya.',
  kick='Distribuïdor a Catalunya', h2='Els models',
  facts=['Categoria de disseny CE: C (certifica PRS)', 'Lliurament: de 4 a 12 setmanes segons el model', 'Garantia: 3 anys des del lliurament', 'Pagament: 40 % en fer la comanda i la resta quan el vaixell és a punt per al transport', 'Transport des de fàbrica fins a Barcelona: uns 2.000 € per vaixell, a part'],
  len='Eslora', beam='Mànega', pax='Persones', hp='Motor', hp_max='fins a {} CV', hp_eco='Elèctric, inclòs',
  lic={'sin': 'Sense titulació amb motor de fins a 15 CV (ús privat, de dia, a 2 milles com a màxim i major de 18 anys); amb més, Llicència de Navegació o superior', 'ln': 'Llicència de Navegació o superior', 'pnb': 'PNB o superior'},
  lic_label='Titulació', price_from='Des de', no_eng='sense motor', with_eng='motor inclòs',
  cta='Demanar pressupost', wa_txt='Hola Juan, m\'interessa el Sunrise {}.', photos='Fotos del {}',
  d={'700-eco-tender': 'Tender elèctric amb plaques solars (1.800 W) i bateries de liti: sense emissions, sense soroll i sense despesa de combustible. Porta bany a bord.',
     '680-dc': 'Day cruiser amb dipòsit de 220 litres, solàrium i banyera àmplia. El més gran de gasolina.',
     '645': 'Cabinat amb timonera tancada, per sortir també fora de temporada. 6,50 m amb plataformes.',
     '606-br': 'Bowrider amb seients a proa, direcció hidràulica i dipòsit de 100 litres.',
     '530-open': 'Open amb consola i seient de pilot, pensat per a pesca i bany.',
     '545': 'Petit cabinat amb sostre i porta de cabina, amb 7 cofres per guardar l\'equip.',
     '530-tender': 'Tender amb matalassos a proa i popa i consola central. Hi cap una família sencera.',
     '400-open': 'Auxiliar de 4 m per a pesca i passejos a prop de la costa. El més econòmic.'},
  used_h='Busques un vaixell d\'ocasió?', used_a='Veure vaixells de segona mà →',
  small='Preus orientatius d\'octubre de 2026, sense IVA, a fàbrica: no inclouen motor (excepte el 700 ECO Tender), equipament opcional, transport ni matriculació. Poden canviar i no són vinculants; el preu final és el del pressupost per escrit. La titulació és orientativa segons l\'eslora i la potència: confirma-la amb la teva escola o amb Capitania. Límit sense titulació des de l\'1 d\'octubre de 2026 (RD 1188/2025): fins a 5 m d\'eslora i 15 CV; orientatiu, confirma-ho amb Capitania. Ens podem equivocar; si hi veus un error, avisa\'ns.',
 ),
 'en': dict(
  title='New Sunrise boats from 4 to 7 m: prices and models · Plata Marine',
  desc='New Sunrise boats from 4 to 7 m, from €5,990 +VAT. Dealer in Catalonia: I help you choose the model, engine and equipment.',
  crumb_last='Sunrise', eyebrow='New boats', h1='Sunrise: new boats from 4 to 7 metres',
  intro='Simple, easy-to-maintain boats built by Sunrise Yacht. They are ordered from the factory and I help you choose the model, engine and equipment. I am their dealer in Catalonia.',
  kick='Dealer in Catalonia', h2='The models',
  facts=['CE design category: C (certified by PRS)', 'Delivery: 4 to 12 weeks depending on the model', 'Warranty: 3 years from delivery', 'Payment: 40% when ordering and the rest when the boat is ready for transport', 'Transport from the factory to Barcelona: about €2,000 per boat, extra'],
  len='Length', beam='Beam', pax='People', hp='Engine', hp_max='up to {} hp', hp_eco='Electric, included',
  lic={'sin': 'No licence needed with an engine up to 15 hp (private use, daytime, within 2 miles, aged 18 or over); above that, Licencia de Navegación or higher', 'ln': 'Spanish Licencia de Navegación or higher', 'pnb': 'Spanish PNB or higher'},
  lic_label='Licence', price_from='From', no_eng='without engine', with_eng='engine included',
  cta='Request a quote', wa_txt='Hi Juan, I am interested in the Sunrise {}.', photos='Photos of the {}',
  d={'700-eco-tender': 'Electric tender with solar panels (1,800 W) and lithium batteries: no emissions, no noise and no fuel costs. Toilet on board.',
     '680-dc': 'Day cruiser with a 220-litre tank, sun deck and a roomy cockpit. The largest petrol model.',
     '645': 'Cabin boat with an enclosed wheelhouse, to keep going out off-season. 6.50 m with platforms.',
     '606-br': 'Bowrider with bow seating, hydraulic steering and a 100-litre tank.',
     '530-open': 'Open boat with console and helm seat, made for fishing and swimming.',
     '545': 'Small cabin boat with a roof and cabin door, with 7 lockers for your gear.',
     '530-tender': 'Tender with bow and stern cushions and a centre console. Fits a whole family.',
     '400-open': '4 m tender for fishing and coastal trips. The most affordable.'},
  used_h='Looking for a used boat?', used_a='See used boats →',
  small='Indicative prices as of October 2026, ex-works, excluding VAT: they do not include the engine (except the 700 ECO Tender), optional equipment, transport or registration. They may change and are not binding; the final price is the one in the written quote. The licence shown is indicative, based on length and power under Spanish rules: please confirm it with your school or the Harbour Master. No-licence limit since 1 October 2026 (Royal Decree 1188/2025): up to 5 m and 15 hp; indicative, please confirm with the Harbour Master. We may be wrong; if you spot an error, let us know.',
 ),
 'fr': dict(
  title='Bateaux neufs Sunrise de 4 à 7 m : prix et modèles · Plata Marine',
  desc='Bateaux neufs Sunrise de 4 à 7 m, à partir de 5 990 € HT. Distributeur en Catalogne : je vous aide à choisir le modèle, le moteur et l\'équipement.',
  crumb_last='Sunrise', eyebrow='Bateaux neufs', h1='Sunrise : bateaux neufs de 4 à 7 mètres',
  intro='Des bateaux simples et faciles à entretenir, fabriqués par Sunrise Yacht. Ils se commandent à l\'usine et je vous aide à choisir le modèle, le moteur et l\'équipement. Je suis leur distributeur en Catalogne.',
  kick='Distributeur en Catalogne', h2='Les modèles',
  facts=['Catégorie de conception CE : C (certifiée par PRS)', 'Livraison : de 4 à 12 semaines selon le modèle', 'Garantie : 3 ans à partir de la livraison', 'Paiement : 40 % à la commande et le reste quand le bateau est prêt pour le transport', 'Transport de l\'usine jusqu\'à Barcelone : environ 2 000 € par bateau, en sus'],
  len='Longueur', beam='Largeur', pax='Personnes', hp='Moteur', hp_max='jusqu\'à {} ch', hp_eco='Électrique, inclus',
  lic={'sin': 'Sans permis avec un moteur jusqu\'à 15 ch (usage privé, de jour, à 2 milles maximum, 18 ans révolus) ; au-delà, Licencia de Navegación ou supérieur (règles espagnoles)', 'ln': 'Licencia de Navegación espagnole ou supérieur', 'pnb': 'PNB espagnol ou supérieur'},
  lic_label='Permis', price_from='À partir de', no_eng='sans moteur', with_eng='moteur inclus',
  cta='Demander un devis', wa_txt='Bonjour Juan, le Sunrise {} m\'intéresse.', photos='Photos du {}',
  d={'700-eco-tender': 'Tender électrique avec panneaux solaires (1 800 W) et batteries lithium : zéro émission, zéro bruit et zéro carburant. Toilettes à bord.',
     '680-dc': 'Day cruiser avec réservoir de 220 litres, bain de soleil et grand cockpit. Le plus grand modèle à essence.',
     '645': 'Bateau à cabine avec timonerie fermée, pour sortir aussi hors saison. 6,50 m avec plateformes.',
     '606-br': 'Bowrider avec assises à l\'avant, direction hydraulique et réservoir de 100 litres.',
     '530-open': 'Open avec console et siège pilote, pensé pour la pêche et la baignade.',
     '545': 'Petit bateau à cabine avec toit et porte de cabine, et 7 coffres de rangement.',
     '530-tender': 'Tender avec matelas à l\'avant et à l\'arrière et console centrale. Toute la famille y tient.',
     '400-open': 'Annexe de 4 m pour la pêche et les sorties côtières. Le plus économique.'},
  used_h='Vous cherchez un bateau d\'occasion ?', used_a='Voir les bateaux d\'occasion →',
  small='Prix indicatifs d\'octobre 2026, départ usine, hors TVA : ils n\'incluent pas le moteur (sauf le 700 ECO Tender), les options, le transport ni l\'immatriculation. Ils peuvent changer et ne sont pas contractuels ; le prix final est celui du devis écrit. Le permis indiqué est indicatif, selon la longueur et la puissance d\'après les règles espagnoles : vérifiez-le auprès de votre école ou de la Capitainerie. Limite sans permis depuis le 1er octobre 2026 (décret royal 1188/2025) : jusqu\'à 5 m et 15 ch ; indicatif, vérifiez auprès de la Capitainerie. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous.',
 ),
}
VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': 'HT'}

CSS = """
.sr-hero{position:relative;margin-top:24px;border-radius:var(--radius);overflow:hidden;background:#0b1620}
.sr-hero img.ph{display:block;width:100%;height:auto;aspect-ratio:16/8;max-height:420px;object-fit:cover}
.sr-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(6,8,11,.65) 0,rgba(6,8,11,0) 60%)}
.sr-hero img.logo{position:absolute;left:clamp(16px,3vw,28px);bottom:clamp(14px,3vw,26px);z-index:1;height:clamp(44px,7vw,72px);width:auto}
.sr-facts{list-style:none;padding:0;margin:22px 0 0;display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.sr-facts li{background:#fff;border:1px solid rgba(127,146,158,.28);border-radius:var(--radius);padding:12px 14px;font-size:.93rem;line-height:1.4;color:var(--ink-2)}
.sr-list{display:grid;gap:18px;margin-top:8px}
.sr-m{background:#fff;border:1px solid rgba(127,146,158,.28);border-radius:var(--radius);overflow:hidden;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr)}
.sr-gal{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;background:#fff;-webkit-overflow-scrolling:touch}
.sr-gal img{flex:0 0 100%;width:100%;height:auto;aspect-ratio:4/3;object-fit:contain;scroll-snap-align:start;background:#fff}
.sr-b{padding:18px clamp(16px,2.5vw,24px) 20px;display:flex;flex-direction:column;gap:8px}
.sr-b h3{font-size:1.35rem;font-weight:700}
.sr-b p.d{color:var(--ink-2);font-size:.95rem;line-height:1.5}
.sr-b dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:.92rem;margin:4px 0 0}
.sr-b dt{color:var(--ink-2)}
.sr-b dd{margin:0;font-weight:600}
.sr-b .pr{font-family:var(--display);font-weight:700;font-size:1.2rem;margin-top:6px}
.sr-b .pr small{font-weight:500;font-size:.8rem;color:var(--ink-2);margin-left:6px}
.sr-b .btn{align-self:flex-start;margin-top:6px}
.sr-hint{font-size:.78rem;color:var(--ink-2)}
.sr-m{scroll-margin-top:86px}
@media (max-width:820px){.sr-facts{grid-template-columns:1fr 1fr}.sr-m{grid-template-columns:1fr}}
@media (max-width:520px){.sr-facts{grid-template-columns:1fr}.sr-b .btn{align-self:stretch;text-align:center}}
"""

HINT = {'es': 'Desliza para ver más fotos →', 'ca': 'Llisca per veure més fotos →', 'en': 'Swipe for more photos →', 'fr': 'Faites glisser pour plus de photos →'}

def build(lang):
    p = LANGS[lang]
    tpl = open(f'{ROOT}{p}/barcos-nuevos/index.html', encoding='utf-8').read()
    t = T[lang]
    url = f'{BASE}{p}/sunrise/'
    head, rest = tpl.split('</head>', 1)
    # quitar JSON-LD y metas que cambian
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(t["title"].replace(" · Plata Marine", ""))}</title>', head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc']), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(t['title']), head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc']), head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', f'\\g<1>{BASE}/sunrise/fotos/645-1.jpg', head)
    head = re.sub(r'<meta property="og:image:width"[^>]*>\n?<meta property="og:image:height"[^>]*>', '<meta property="og:image:width" content="1000">\n<meta property="og:image:height" content="600">', head)
    head = head.replace('/barcos-nuevos/', '/sunrise/')
    crumbs = {'es': ('Inicio', 'Barcos en venta', 'Barcos nuevos'), 'ca': ('Inici', 'Vaixells en venda', 'Vaixells nous'), 'en': ('Home', 'Boats for sale', 'New boats'), 'fr': ('Accueil', 'Bateaux à vendre', 'Bateaux neufs')}[lang]
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f"{BASE}{p}/"},
            {"@type": "ListItem", "position": 2, "name": crumbs[1], "item": f"{BASE}{p}/barcos/"},
            {"@type": "ListItem", "position": 3, "name": crumbs[2], "item": f"{BASE}{p}/barcos-nuevos/"},
            {"@type": "ListItem", "position": 4, "name": "Sunrise", "item": url}]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": t['h1'], "url": url, "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "item": {"@type": "Product", "name": f"Sunrise {m[1]}", "brand": {"@type": "Brand", "name": "Sunrise"},
              "image": f"{BASE}/sunrise/fotos/{m[0]}-1.jpg", "description": t['d'][m[0]],
              "offers": {"@type": "Offer", "price": str(m[6]), "priceCurrency": "EUR", "availability": "https://schema.org/PreOrder", "url": f"{url}#sunrise-{m[0]}",
                         "priceSpecification": {"@type": "PriceSpecification", "price": str(m[6]), "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}}}
            for i, m in enumerate(M)]},
    ]
    head = head.replace('<style>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '<style>', 1)
    head = head.replace('</style>', CSS + '</style>', 1)

    body = rest
    body = body.replace('/barcos-nuevos/" aria-current', '/sunrise/" aria-current')
    body = re.sub(r'(<div class="langsw".*?</div>)', lambda m: m.group(1).replace('/barcos-nuevos/', '/sunrise/'), body, flags=re.S)
    vat = VAT[lang]
    cards = []
    for slug, name, L, B, pax, hp, price, nph, lic, inc in M:
        imgs = ''.join(
            f'<img src="/sunrise/fotos/{slug}-{i}-m.jpg" srcset="/sunrise/fotos/{slug}-{i}-m.jpg 800w, /sunrise/fotos/{slug}-{i}.jpg 1400w" sizes="(max-width:820px) 100vw, 560px" alt="Sunrise {name} – {"foto" if lang in ("es","ca") else "photo"} {i}" loading="lazy" decoding="async">'
            for i in range(1, nph + 1))
        motor = t['hp_eco'] if hp is None else t['hp_max'].format(hp)
        wa = f'https://wa.me/{WA}?text=' + urllib.parse.quote(t['wa_txt'].format(name))
        cards.append(f'''<article class="sr-m" id="sunrise-{slug}">
  <div><div class="sr-gal" aria-label="{html.escape(t['photos'].format('Sunrise ' + name))}">{imgs}</div></div>
  <div class="sr-b">
    <h3>Sunrise {name}</h3>
    <p class="d">{html.escape(t['d'][slug])}</p>
    <dl><dt>{t['len']}</dt><dd>{num(L, lang)} m</dd><dt>{t['beam']}</dt><dd>{num(B, lang)} m</dd><dt>{t['pax']}</dt><dd>{pax}</dd><dt>{t['hp']}</dt><dd>{motor}</dd><dt>{t['lic_label']}</dt><dd>{html.escape(t['lic'][lic])}</dd></dl>
    <p class="pr">{t['price_from']} {eur(price, lang)} € <span class="vat">{vat}</span><small>{t['with_eng'] if inc else t['no_eng']}</small></p>
    <p class="sr-hint">{HINT[lang]}</p>
    <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{t['cta']}</a>
  </div>
</article>''')
    facts = ''.join(f'<li>{html.escape(f)}</li>' for f in t['facts'])
    main = f'''<main class="boat">
  <div class="wrap">
    <p class="crumb"><a href="{p}/">{crumbs[0]}</a> · <a href="{p}/barcos/">{crumbs[1]}</a> · <a href="{p}/barcos-nuevos/">{crumbs[2]}</a> · Sunrise</p>
    <div class="head">
      <div>
        <p class="eyebrow">{t['eyebrow']}</p>
        <h1>{html.escape(t['h1'])}</h1>
      </div>
    </div>
    <p class="nv-intro">{html.escape(t['intro'])}</p>
    <div class="sr-hero"><img class="ph" src="/sunrise/fotos/645-1.jpg" alt="Sunrise 645" width="1000" height="600" decoding="async" fetchpriority="high"><img class="logo" src="/sunrise/fotos/sunrise-logo.png" alt="Sunrise" width="400" height="136"></div>
    <ul class="sr-facts">{facts}</ul>
    <p class="nv-mh">{t['kick']}</p>
    <h2 style="font-size:clamp(1.4rem,3vw,1.9rem);font-weight:700;margin-bottom:12px">{t['h2']}</h2>
    <div class="sr-list">
{chr(10).join(cards)}
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
    import os
    os.makedirs(f'{ROOT}{p}/sunrise', exist_ok=True)
    open(f'{ROOT}{p}/sunrise/index.html', 'w', encoding='utf-8').write(out)
    print('ok', lang, len(out))

if __name__ == '__main__':
    for l in LANGS:
        build(l)
