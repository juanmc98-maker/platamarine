#!/usr/bin/env python3
"""Genera /seastorm/ en ES/CA/EN/FR a partir de la plantilla de /barcos-nuevos/.
Uso (desde la raíz del repo):
  python3 _tools/build_seastorm.py                  -> genera las 4 páginas con las fotos que haya en /seastorm/fotos/
  python3 _tools/build_seastorm.py --fotos CARPETA  -> antes prepara las fotos: CARPETA/<slug>-<n>.(jpg|png|webp)
                                                       (p. ej. 17-1.jpg, 17-2.jpg…) y CARPETA/logo.png (fondo transparente, letras claras)
                                                       y opcional CARPETA/hero.jpg (portada ya encuadrada)
Las fotos se guardan sin EXIF: <slug>-<n>.jpg (1200 px) y <slug>-<n>-m.jpg (800 px); portada 1000x600.
Precios: PVP recomendado (RRP) de la tarifa de distribuidor 2027, sin IVA. None = PENDIENTE."""
import re, json, html, urllib.parse, os, sys, glob

ROOT = '.'
BASE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
WA = '34633742973'
FOTOS = f'{ROOT}/seastorm/fotos'

# slug, nombre, eslora, manga, personas cat. C, personas cat. D, CV máx, kW máx, PVP sin IVA (RRP 2027), titulación
# Datos técnicos: fichas de seastorm-boat.com (octubre 2026).
# PVP: "Dealers Price List 2027" de Ceranos Invest OÜ, columna "RRP w/o VAT", configuración ADVANTAGE (la única de la tarifa),
# redondeado hacia arriba a .990 por decisión de Juan. RRP original: 17 -> 10.928, 14 -> 7.253, 13s -> 6.683, 12 -> 4.454.
M = [
 ('17', 'SeaStorm 17', '5,17', '1,97', 6, 8, 80, 60, 10990, 'ln'),
 ('14', 'SeaStorm 14', '4,28', '1,86', 5, 6, 40, 30, 7990, 'sin'),
 ('13-s', 'SeaStorm 13 S', '4,00', '1,90', 5, 5, 60, 44, 6990, 'sin'),
 ('12', 'SeaStorm 12', '3,66', '1,67', 4, 6, 30, 22, 4990, 'sin'),
]
HERO = '17'  # modelo de la foto de portada

def eur(n, lang):
    s = f'{n:,}'
    if lang == 'en':
        return s
    if lang == 'fr':
        return s.replace(',', ' ')
    return s.replace(',', '.')

def num(s, lang):
    return s.replace(',', '.') if lang == 'en' else s

T = {
 'es': dict(
  title='Barcos SeaStorm nuevos de 3,7 a 5,2 m: modelos y precios · Plata Marine',
  desc='Barcos nuevos SeaStorm de polietileno, fabricados en Estonia, de 3,7 a 5,2 m. Dealer en Cataluña: se piden a fábrica y te ayudo a elegir modelo y motor.',
  eyebrow='Barcos nuevos', h1='SeaStorm: barcos de polietileno de 3,7 a 5,2 metros',
  intro='Barcos pequeños de polietileno (HDPE), de una sola pieza, fabricados en Estonia por SeaStorm. Pesan poco, no necesitan apenas mantenimiento y se acercan bien a la playa. Se piden a fábrica y te ayudo a elegir el modelo y el motor. Soy su dealer en Cataluña.',
  kick='Dealer en Cataluña', h2='Los modelos',
  facts=['Fabricados en Estonia, en polietileno (HDPE) de una sola pieza. Marca presente en 75 países', 'Categoría de diseño CE: C (y D con más personas a bordo)', 'Se fabrican bajo pedido: plazo orientativo, lo confirmamos en el presupuesto', 'Portes desde Estonia no incluidos en el precio: orientativo, unos 2.090 € un envío compartido (p. ej. un 17 y un 13) y unos 4.390 € un camión completo', 'Precios en configuración Advantage: consola con volante, parabrisas, cojines con respaldo, barandillas laterales y placa de motor', 'Casco doble, autovaciante y de poco calado (de 18 a 22 cm)'],
  len='Eslora', beam='Manga', pax='Personas', pax_v='{c} (cat. C) · {d} (cat. D)', hp='Motor', hp_max='hasta {} CV ({} kW)',
  lic={'sin': 'Sin titulación con motor de hasta 15 kW; con más, Licencia de Navegación o superior', 'ln': 'Licencia de Navegación o superior', 'pnb': 'PNB o superior'},
  lic_label='Titulación', price_from='Desde', no_eng='Advantage, sin motor', pend='Precio pendiente',
  cta='Pedir presupuesto', wa_txt='Hola Juan, me interesa el {}.', photos='Fotos del {}',
  d={'17': 'El más grande de la gama: hasta 8 personas en categoría D y motor de hasta 80 CV. Para salir en familia, pescar o bucear.',
     '14': 'Líneas clásicas, consola con volante y cofres a proa y popa. Con 18 cm de calado se acerca bien a la playa.',
     '13-s': 'Casco con dos redanes diseñado por Mannerfeldt Design: planea con motores pequeños y admite hasta 60 CV.',
     '12': 'El más pequeño: un primer barco o una auxiliar para salir cerca de la costa. Pesa unos 200 kg.'},
  used_h='¿Buscas un barco de ocasión?', used_a='Ver barcos de segunda mano →',
  small='Precios orientativos, sin IVA, según el PVP recomendado de la tarifa 2027 de SeaStorm, en fábrica (Estonia): no incluyen motor, equipamiento opcional, transporte ni matriculación. El transporte y los plazos son orientativos y dependen de la carga y de la fábrica. Datos técnicos según la web del fabricante. Pueden cambiar y no son vinculantes; el precio final es el del presupuesto por escrito. La titulación es orientativa según la eslora y la potencia: confírmala con tu escuela o con Capitanía. Podemos equivocarnos; si ves un error, avísanos.',
 ),
 'ca': dict(
  title='Vaixells SeaStorm nous de 3,7 a 5,2 m: models i preus · Plata Marine',
  desc='Vaixells nous SeaStorm de polietilè, fabricats a Estònia, de 3,7 a 5,2 m. Dealer a Catalunya: es demanen a fàbrica i t\'ajudo a triar model i motor.',
  eyebrow='Vaixells nous', h1='SeaStorm: vaixells de polietilè de 3,7 a 5,2 metres',
  intro='Vaixells petits de polietilè (HDPE), d\'una sola peça, fabricats a Estònia per SeaStorm. Pesen poc, gairebé no necessiten manteniment i s\'acosten bé a la platja. Es demanen a fàbrica i t\'ajudo a triar el model i el motor. En sóc el dealer a Catalunya.',
  kick='Dealer a Catalunya', h2='Els models',
  facts=['Fabricats a Estònia, en polietilè (HDPE) d\'una sola peça. Marca present a 75 països', 'Categoria de disseny CE: C (i D amb més persones a bord)', 'Es fabriquen per encàrrec: termini orientatiu, el confirmem al pressupost', 'Ports des d\'Estònia no inclosos en el preu: orientatiu, uns 2.090 € un enviament compartit (p. ex. un 17 i un 13) i uns 4.390 € un camió complet', 'Preus en configuració Advantage: consola amb volant, parabrisa, coixins amb respatller, baranes laterals i placa de motor', 'Buc doble, autobuidant i de poc calat (de 18 a 22 cm)'],
  len='Eslora', beam='Mànega', pax='Persones', pax_v='{c} (cat. C) · {d} (cat. D)', hp='Motor', hp_max='fins a {} CV ({} kW)',
  lic={'sin': 'Sense titulació amb motor de fins a 15 kW; amb més, Llicència de Navegació o superior', 'ln': 'Llicència de Navegació o superior', 'pnb': 'PNB o superior'},
  lic_label='Titulació', price_from='Des de', no_eng='Advantage, sense motor', pend='Preu pendent',
  cta='Demanar pressupost', wa_txt='Hola Juan, m\'interessa el {}.', photos='Fotos del {}',
  d={'17': 'El més gran de la gamma: fins a 8 persones en categoria D i motor de fins a 80 CV. Per sortir en família, pescar o bussejar.',
     '14': 'Línies clàssiques, consola amb volant i cofres a proa i popa. Amb 18 cm de calat s\'acosta bé a la platja.',
     '13-s': 'Buc amb dos redans dissenyat per Mannerfeldt Design: planeja amb motors petits i admet fins a 60 CV.',
     '12': 'El més petit: un primer vaixell o un auxiliar per sortir a prop de la costa. Pesa uns 200 kg.'},
  used_h='Busques un vaixell d\'ocasió?', used_a='Veure vaixells de segona mà →',
  small='Preus orientatius, sense IVA, segons el PVP recomanat de la tarifa 2027 de SeaStorm, a fàbrica (Estònia): no inclouen motor, equipament opcional, transport ni matriculació. El transport i els terminis són orientatius i depenen de la càrrega i de la fàbrica. Dades tècniques segons la web del fabricant. Poden canviar i no són vinculants; el preu final és el del pressupost per escrit. La titulació és orientativa segons l\'eslora i la potència: confirma-la amb la teva escola o amb Capitania. Ens podem equivocar; si hi veus un error, avisa\'ns.',
 ),
 'en': dict(
  title='New SeaStorm boats from 3.7 to 5.2 m: models and prices · Plata Marine',
  desc='New SeaStorm polyethylene boats built in Estonia, from 3.7 to 5.2 m. Dealer in Catalonia: ordered from the factory, I help you choose the model and engine.',
  eyebrow='New boats', h1='SeaStorm: polyethylene boats from 3.7 to 5.2 metres',
  intro='Small one-piece polyethylene (HDPE) boats built in Estonia by SeaStorm. They are light, need very little maintenance and are easy to take close to the beach. They are ordered from the factory and I help you choose the model and engine. I am their dealer in Catalonia.',
  kick='Dealer in Catalonia', h2='The models',
  facts=['Built in Estonia from one-piece polyethylene (HDPE). Brand present in 75 countries', 'CE design category: C (and D with more people on board)', 'Built to order: indicative lead time, confirmed in the quote', 'Shipping from Estonia not included in the price: indicative, about €2,090 for a shared load (e.g. a 17 and a 13) and about €4,390 for a full truck', 'Prices for the Advantage configuration: console with steering wheel, windscreen, cushions with backrests, side rails and motor plate', 'Double hull, self-draining, shallow draught (18 to 22 cm)'],
  len='Length', beam='Beam', pax='People', pax_v='{c} (cat. C) · {d} (cat. D)', hp='Engine', hp_max='up to {} hp ({} kW)',
  lic={'sin': 'No licence needed with an engine up to 15 kW; above that, Licencia de Navegación or higher', 'ln': 'Spanish Licencia de Navegación or higher', 'pnb': 'Spanish PNB or higher'},
  lic_label='Licence', price_from='From', no_eng='Advantage, without engine', pend='Price to be confirmed',
  cta='Request a quote', wa_txt='Hi Juan, I am interested in the {}.', photos='Photos of the {}',
  d={'17': 'The largest in the range: up to 8 people in category D and engines up to 80 hp. For family days, fishing or diving.',
     '14': 'Classic lines, console with steering wheel and lockers fore and aft. With an 18 cm draught it gets close to the beach.',
     '13-s': 'Twin-step hull designed by Mannerfeldt Design: planes with small engines and takes up to 60 hp.',
     '12': 'The smallest: a first boat or a tender for coastal trips. It weighs about 200 kg.'},
  used_h='Looking for a used boat?', used_a='See used boats →',
  small='Indicative prices, excluding VAT, based on the recommended retail price in SeaStorm\'s 2027 price list, ex-works (Estonia): they do not include the engine, optional equipment, transport or registration. Transport and lead times are indicative and depend on the load and the factory. Technical data from the manufacturer\'s website. They may change and are not binding; the final price is the one in the written quote. The licence shown is indicative, based on length and power under Spanish rules: please confirm it with your school or the Harbour Master. We may be wrong; if you spot an error, let us know.',
 ),
 'fr': dict(
  title='Bateaux neufs SeaStorm de 3,7 à 5,2 m : modèles et prix · Plata Marine',
  desc='Bateaux neufs SeaStorm en polyéthylène, fabriqués en Estonie, de 3,7 à 5,2 m. Concessionnaire en Catalogne : commande à l\'usine, je vous aide à choisir le modèle et le moteur.',
  eyebrow='Bateaux neufs', h1='SeaStorm : bateaux en polyéthylène de 3,7 à 5,2 mètres',
  intro='De petits bateaux en polyéthylène (HDPE) d\'une seule pièce, fabriqués en Estonie par SeaStorm. Ils sont légers, demandent très peu d\'entretien et s\'approchent facilement de la plage. Ils se commandent à l\'usine et je vous aide à choisir le modèle et le moteur. Je suis leur concessionnaire en Catalogne.',
  kick='Concessionnaire en Catalogne', h2='Les modèles',
  facts=['Fabriqués en Estonie, en polyéthylène (HDPE) d\'une seule pièce. Marque présente dans 75 pays', 'Catégorie de conception CE : C (et D avec plus de personnes à bord)', 'Fabriqués sur commande : délai indicatif, confirmé dans le devis', 'Transport depuis l\'Estonie non inclus dans le prix : indicatif, environ 2 090 € pour un envoi partagé (p. ex. un 17 et un 13) et environ 4 390 € pour un camion complet', 'Prix en configuration Advantage : console avec volant, pare-brise, coussins avec dossiers, mains courantes latérales et plaque moteur', 'Double coque, autovideuse, faible tirant d\'eau (de 18 à 22 cm)'],
  len='Longueur', beam='Largeur', pax='Personnes', pax_v='{c} (cat. C) · {d} (cat. D)', hp='Moteur', hp_max='jusqu\'à {} ch ({} kW)',
  lic={'sin': 'Sans permis avec un moteur jusqu\'à 15 kW ; au-delà, Licencia de Navegación ou supérieur (règles espagnoles)', 'ln': 'Licencia de Navegación espagnole ou supérieur', 'pnb': 'PNB espagnol ou supérieur'},
  lic_label='Permis', price_from='À partir de', no_eng='Advantage, sans moteur', pend='Prix à confirmer',
  cta='Demander un devis', wa_txt='Bonjour Juan, le {} m\'intéresse.', photos='Photos du {}',
  d={'17': 'Le plus grand de la gamme : jusqu\'à 8 personnes en catégorie D et moteur jusqu\'à 80 ch. Pour les sorties en famille, la pêche ou la plongée.',
     '14': 'Lignes classiques, console avec volant et coffres à l\'avant et à l\'arrière. Avec 18 cm de tirant d\'eau, il s\'approche bien de la plage.',
     '13-s': 'Coque à deux redans dessinée par Mannerfeldt Design : elle déjauge avec de petits moteurs et accepte jusqu\'à 60 ch.',
     '12': 'Le plus petit : un premier bateau ou une annexe pour les sorties côtières. Il pèse environ 200 kg.'},
  used_h='Vous cherchez un bateau d\'occasion ?', used_a='Voir les bateaux d\'occasion →',
  small='Prix indicatifs, hors TVA, selon le prix de vente conseillé du tarif 2027 de SeaStorm, départ usine (Estonie) : ils n\'incluent pas le moteur, les options, le transport ni l\'immatriculation. Le transport et les délais sont indicatifs et dépendent du chargement et de l\'usine. Caractéristiques selon le site du fabricant. Ils peuvent changer et ne sont pas contractuels ; le prix final est celui du devis écrit. Le permis indiqué est indicatif, selon la longueur et la puissance d\'après les règles espagnoles : vérifiez-le auprès de votre école ou de la Capitainerie. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous. Nous ne parlons pas français : nous utilisons un traducteur, merci de votre indulgence.',
 ),
}
VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': 'HT'}

CSS = """
.sr-hero{position:relative;margin-top:24px;border-radius:var(--radius);overflow:hidden;background:#0b1620}
.sr-hero img.ph{display:block;width:100%;height:auto;aspect-ratio:16/8;max-height:420px;object-fit:cover}
.sr-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(6,8,11,.65) 0,rgba(6,8,11,0) 60%)}
.sr-hero img.logo{position:absolute;left:clamp(16px,3vw,28px);bottom:clamp(14px,3vw,26px);z-index:1;width:min(58%,420px);height:auto}
.sr-hero.nophoto img.logo{position:static;display:block}
.sr-hero.nophoto{padding:clamp(28px,6vw,56px) clamp(16px,3vw,28px);color:#fff;font-family:var(--display);font-weight:700;font-size:clamp(1.8rem,5vw,3rem);letter-spacing:.02em}
.sr-hero.nophoto::after{display:none}
.sr-facts{list-style:none;padding:0;margin:22px 0 0;display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.sr-facts li{background:#fff;border:1px solid rgba(127,146,158,.28);border-radius:var(--radius);padding:12px 14px;font-size:.93rem;line-height:1.4;color:var(--ink-2)}
.sr-list{display:grid;gap:18px;margin-top:8px}
.sr-m{background:#fff;border:1px solid rgba(127,146,158,.28);border-radius:var(--radius);overflow:hidden;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr)}
.sr-m.nogal{grid-template-columns:1fr}
.sr-gal{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;background:#fff;-webkit-overflow-scrolling:touch}
.sr-gal img{flex:0 0 100%;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;scroll-snap-align:start;background:#fff}
.sr-b{padding:18px clamp(16px,2.5vw,24px) 20px;display:flex;flex-direction:column;gap:8px}
.sr-b h3{font-size:1.35rem;font-weight:700}
.sr-b p.d{color:var(--ink-2);font-size:.95rem;line-height:1.5}
.sr-b dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:.92rem;margin:4px 0 0}
.sr-b dt{color:var(--ink-2)}
.sr-b dd{margin:0;font-weight:600}
.sr-b .pr{font-family:var(--display);font-weight:700;font-size:1.2rem;margin-top:6px}
.sr-b .pr small{font-weight:500;font-size:.8rem;color:var(--ink-2);margin-left:6px;white-space:nowrap;display:inline-block}
.sr-b .pr.pend{color:#C62828}
.sr-b .btn{align-self:flex-start;margin-top:6px}
.sr-hint{font-size:.78rem;color:var(--ink-2)}
@media (max-width:820px){.sr-facts{grid-template-columns:1fr 1fr}.sr-m{grid-template-columns:1fr}}
@media (max-width:520px){.sr-facts{grid-template-columns:1fr}.sr-b .btn{align-self:stretch;text-align:center}}
"""

HINT = {'es': 'Desliza para ver más fotos →', 'ca': 'Llisca per veure més fotos →', 'en': 'Swipe for more photos →', 'fr': 'Faites glisser pour plus de photos →'}


def prep_fotos(src):
    """Copia las fotos de fábrica a /seastorm/fotos/ redimensionadas y sin metadatos."""
    from PIL import Image, ImageOps
    os.makedirs(FOTOS, exist_ok=True)
    def save(im, path, w, h=None):
        im = im.convert('RGB')
        if h:
            im = ImageOps.fit(im, (w, h), Image.LANCZOS)
        else:
            im = ImageOps.fit(im, (w, w * 3 // 4), Image.LANCZOS)
        im.save(path, 'JPEG', quality=82, optimize=True, progressive=True)  # sin exif
    for slug, *_ in M:
        files = sorted(f for f in glob.glob(f'{src}/{slug}-*') if re.search(rf'/{re.escape(slug)}-\d+\.(jpe?g|png|webp)$', f, re.I))
        files.sort(key=lambda f: int(re.search(r'-(\d+)\.\w+$', f).group(1)))
        for i, f in enumerate(files, 1):
            im = ImageOps.exif_transpose(Image.open(f))
            save(im, f'{FOTOS}/{slug}-{i}.jpg', 1200)
            save(im, f'{FOTOS}/{slug}-{i}-m.jpg', 800)
            if slug == HERO and i == 1 and not os.path.exists(f'{src}/hero.jpg'):
                save(im, f'{FOTOS}/portada.jpg', 1000, 600)
    if os.path.exists(f'{src}/hero.jpg'):
        save(Image.open(f'{src}/hero.jpg'), f'{FOTOS}/portada.jpg', 1000, 600)
    logo = f'{src}/logo.png'
    if os.path.exists(logo):
        im = Image.open(logo).convert('RGBA')
        im = im.crop(im.getbbox())
        w = 840
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(f'{FOTOS}/seastorm-logo.png', optimize=True)


def nfotos(slug):
    return len(glob.glob(f'{FOTOS}/{slug}-[0-9]*.jpg')) // 2


def build(lang):
    p = LANGS[lang]
    tpl = open(f'{ROOT}{p}/barcos-nuevos/index.html', encoding='utf-8').read()
    t = T[lang]
    url = f'{BASE}{p}/seastorm/'
    has_hero = os.path.exists(f'{FOTOS}/portada.jpg')
    has_logo = os.path.exists(f'{FOTOS}/seastorm-logo.png')
    head, rest = tpl.split('</head>', 1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(t["title"])}</title>', head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc']), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(t['title']), head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc']), head)
    og = (f'{BASE}/seastorm/fotos/portada.jpg', 1000, 600) if has_hero else (f'{BASE}/og-image.jpg', 1200, 630)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', f'\\g<1>{og[0]}', head)
    head = re.sub(r'<meta property="og:image:width"[^>]*>\n?<meta property="og:image:height"[^>]*>', f'<meta property="og:image:width" content="{og[1]}">\n<meta property="og:image:height" content="{og[2]}">', head)
    head = head.replace('/barcos-nuevos/', '/seastorm/')
    crumbs = {'es': ('Inicio', 'Barcos en venta'), 'ca': ('Inici', 'Vaixells en venda'), 'en': ('Home', 'Boats for sale'), 'fr': ('Accueil', 'Bateaux à vendre')}[lang]
    items = []
    for i, m in enumerate(M):
        it = {"@type": "Product", "name": m[1], "brand": {"@type": "Brand", "name": "SeaStorm"}, "description": t['d'][m[0]]}
        if nfotos(m[0]):
            it["image"] = f"{BASE}/seastorm/fotos/{m[0]}-1.jpg"
        if m[8] is not None:
            it["offers"] = {"@type": "Offer", "price": str(m[8]), "priceCurrency": "EUR", "availability": "https://schema.org/PreOrder", "url": f"{url}#seastorm-{m[0]}",
                            "priceSpecification": {"@type": "PriceSpecification", "price": str(m[8]), "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}
        items.append({"@type": "ListItem", "position": i + 1, "item": it})
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f"{BASE}{p}/"},
            {"@type": "ListItem", "position": 2, "name": crumbs[1], "item": f"{BASE}{p}/barcos/"},
            {"@type": "ListItem", "position": 3, "name": "SeaStorm", "item": url}]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": t['h1'], "url": url, "itemListElement": items},
    ]
    head = head.replace('<style>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '<style>', 1)
    head = head.replace('</style>', CSS + '</style>', 1)

    body = rest
    body = body.replace('/barcos-nuevos/" aria-current', '/seastorm/" aria-current')
    body = re.sub(r'(<div class="langsw".*?</div>)', lambda m: m.group(1).replace('/barcos-nuevos/', '/seastorm/'), body, flags=re.S)
    vat = VAT[lang]
    cards = []
    for slug, name, L, B, pc, pd, hp, kw, price, lic in M:
        n = nfotos(slug)
        imgs = ''.join(
            f'<img src="/seastorm/fotos/{slug}-{i}-m.jpg" srcset="/seastorm/fotos/{slug}-{i}-m.jpg 800w, /seastorm/fotos/{slug}-{i}.jpg 1200w" sizes="(max-width:820px) 100vw, 560px" alt="{name} – {"foto" if lang in ("es","ca") else "photo"} {i}" width="800" height="600" loading="lazy" decoding="async">'
            for i in range(1, n + 1))
        gal = f'<div><div class="sr-gal" aria-label="{html.escape(t["photos"].format(name))}">{imgs}</div></div>\n  ' if n else ''
        hint = f'\n    <p class="sr-hint">{HINT[lang]}</p>' if n > 1 else ''
        wa = f'https://wa.me/{WA}?text=' + urllib.parse.quote(t['wa_txt'].format(name))
        if price is None:
            pr = f'<p class="pr pend">{t["pend"]}</p>'
        else:
            pr = f'<p class="pr">{t["price_from"]} {eur(price, lang)} € <span class="vat">{vat}</span><small>{t["no_eng"]}</small></p>'
        cards.append(f'''<article class="sr-m{'' if n else ' nogal'}" id="seastorm-{slug}">
  {gal}<div class="sr-b">
    <h3>{name}</h3>
    <p class="d">{html.escape(t['d'][slug])}</p>
    <dl><dt>{t['len']}</dt><dd>{num(L, lang)} m</dd><dt>{t['beam']}</dt><dd>{num(B, lang)} m</dd><dt>{t['pax']}</dt><dd>{t['pax_v'].format(c=pc, d=pd)}</dd><dt>{t['hp']}</dt><dd>{t['hp_max'].format(hp, kw)}</dd><dt>{t['lic_label']}</dt><dd>{html.escape(t['lic'][lic])}</dd></dl>
    {pr}{hint}
    <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{t['cta']}</a>
  </div>
</article>''')
    facts = ''.join(f'<li>{html.escape(f)}</li>' for f in t['facts'])
    logo = '<img class="logo" src="/seastorm/fotos/seastorm-logo.png" alt="SeaStorm" decoding="async">' if has_logo else ''
    if has_hero:
        hero = f'<div class="sr-hero"><img class="ph" src="/seastorm/fotos/portada.jpg" alt="SeaStorm 17" width="1000" height="600" decoding="async" fetchpriority="high">{logo}</div>'
    else:
        hero = f'<div class="sr-hero nophoto">{logo or "SeaStorm"}</div>'
    main = f'''<main class="boat">
  <div class="wrap">
    <p class="crumb"><a href="{p}/">{crumbs[0]}</a> · <a href="{p}/barcos/">{crumbs[1]}</a> · SeaStorm</p>
    <div class="head">
      <div>
        <p class="eyebrow">{t['eyebrow']}</p>
        <h1>{html.escape(t['h1'])}</h1>
      </div>
    </div>
    <p class="nv-intro">{html.escape(t['intro'])}</p>
    {hero}
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
    os.makedirs(f'{ROOT}{p}/seastorm', exist_ok=True)
    open(f'{ROOT}{p}/seastorm/index.html', 'w', encoding='utf-8').write(out)
    print('ok', lang, len(out))


if __name__ == '__main__':
    if '--fotos' in sys.argv:
        prep_fotos(sys.argv[sys.argv.index('--fotos') + 1])
    pend = [m[1] for m in M if m[8] is None]
    if pend:
        print('AVISO: PVP PENDIENTE en', ', '.join(pend))
    sin = [m[1] for m in M if not nfotos(m[0])]
    if sin:
        print('AVISO: sin fotos en', ', '.join(sin))
    for l in LANGS:
        build(l)
