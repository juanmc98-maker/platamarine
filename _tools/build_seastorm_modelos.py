#!/usr/bin/env python3
"""Páginas por modelo de SeaStorm (/seastorm/<slug>/ en ES/CA/EN/FR), generadas a partir de /seastorm/index.html de cada idioma.
Cada página: portada del modelo, su ficha y fotos, configurador con el modelo marcado, llave en mano, colores, cómo se compra,
preguntas del modelo (FAQPage), los otros tres modelos y el formulario de presupuesto.
En /seastorm/ las tarjetas de elección pasan a enlazar a estas páginas.
Relanzar después de _tools/build_seastorm.py.  Uso: python3 _tools/build_seastorm_modelos.py"""
import re, json, html, os

BASE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
F = '/seastorm/fotos/'
# slug, nombre, eslora, manga, peso casco, calado, carga, pers C, pers D, CV máx, kW máx, CV recomendados, PVP, eslora > 5 m
M = [
 ('12',   'SeaStorm 12',   '3,66', '1,67', 200, 18, 380, 4, 6, 30, 22, '25–30', 4454, False),
 ('13-s', 'SeaStorm 13 S', '4,00', '1,90', 250, 20, 475, 5, 5, 60, 44, '40', 6683, False),
 ('14',   'SeaStorm 14',   '4,28', '1,86', 260, 18, 475, 5, 6, 40, 30, '30–40', 7253, False),
 ('17',   'SeaStorm 17',   '5,17', '1,97', 380, 22, 610, 6, 8, 80, 60, '60', 10928, True),
]

def eur(n, l):
    s = f'{n:,}'
    return '€' + s if l == 'en' else (s.replace(',', ' ') + ' €' if l == 'fr' else s.replace(',', '.') + ' €')

def num(s, l):
    return s.replace(',', '.') if l == 'en' else s

T = {
 'es': dict(title='{n}: precio y ficha del barco de polietileno', desc='{n}, barco de polietileno de {loa} m con 20 años de garantía de casco. Ficha, fotos, configurador y precio desde {p} + impuestos sin motor.',
            crumb='Barcos nuevos', faq_h='Preguntas sobre el {n}', others='Los otros SeaStorm', tax='+ impuestos', see='Ver modelo', from_='Desde',
            kick='El {n}', h2m='Ficha, fotos y precio'),
 'ca': dict(title='{n}: preu i fitxa del vaixell de polietilè', desc='{n}, vaixell de polietilè de {loa} m amb 20 anys de garantia de buc. Fitxa, fotos, configurador i preu des de {p} + impostos sense motor.',
            crumb='Vaixells nous', faq_h='Preguntes sobre el {n}', others='Els altres SeaStorm', tax='+ impostos', see='Veure model', from_='Des de',
            kick='El {n}', h2m='Fitxa, fotos i preu'),
 'en': dict(title='{n}: price and specs of the polyethylene boat', desc='{n}, a {loa} m polyethylene boat with a 20-year hull warranty. Specs, photos, configurator and price from {p} + taxes without engine.',
            crumb='New boats', faq_h='Questions about the {n}', others='The other SeaStorm models', tax='+ taxes', see='See model', from_='From',
            kick='The {n}', h2m='Specs, photos and price'),
 'fr': dict(title='{n} : prix et fiche du bateau en polyéthylène', desc='{n}, bateau en polyéthylène de {loa} m avec coque garantie 20 ans. Fiche, photos, configurateur et prix dès {p} + taxes sans moteur.',
            crumb='Bateaux neufs', faq_h='Questions sur le {n}', others='Les autres SeaStorm', tax='+ taxes', see='Voir le modèle', from_='Dès',
            kick='Le {n}', h2m='Fiche, photos et prix'),
}

def faq(m, l):
    slug, n, loa, beam, w, dr, cap, pc, pd, hp, kw, rec, price, over5 = m
    p = LANGS[l]; tg = f'{p}/titulaciones/'; t = T[l]['tax']; L = num(loa, l)
    if l == 'es':
        lic = (f'Sí. Mide {L} m, así que siempre necesita la Licencia de Navegación o superior, sea cual sea el motor.' if over5 else
               f'Depende del motor. Mide {L} m: sin título solo puedes llevarlo con un motor de hasta 15 CV, para uso privado, de día, a no más de 2 millas náuticas del puerto, playa o lugar de salida y siendo mayor de 18 años. Con el motor que recomienda la marca ({rec} CV) necesitas la Licencia de Navegación o superior.')
        return [(f'¿Cuánto cuesta el {n}?', f'Desde {eur(price,l)} {t}, en versión Advantage y sin motor. En el configurador le puedes añadir un motor Mercury instalado en fábrica y ver el total al momento. El remolque, el transporte y la matriculación se presupuestan aparte.'),
                (f'¿Necesito titulación para el {n}?', lic + f' <a href="{tg}">Ver titulaciones</a>.'),
                ('¿Qué motor le pongo?', f'La marca recomienda {rec} CV con eje largo. Nunca por encima de la potencia máxima de su placa CE: {hp} CV ({kw} kW).'),
                ('¿Cuántas personas lleva?', f'{pc} personas en categoría de diseño C y {pd} en categoría D. La carga máxima es de {cap} kg, contando personas, motor, combustible y equipaje.'),
                ('¿Me vale el carnet B para el remolque?', f'El casco pesa {w} kg sin motor. Con el carnet B puedes llevar un remolque de hasta 750 kg de masa máxima autorizada, o uno más pesado si el coche y el remolque juntos no pasan de 3.500 kg. Te digo qué remolque encaja con tu barco y con tu coche.'),
                ('¿Qué garantía tiene?', 'SeaStorm da una garantía comercial de 20 años en el casco frente a defectos de materiales y fabricación, al primer comprador, con un uso normal y con las condiciones y exclusiones de la marca. El motor, el remolque y los accesorios tienen la garantía de su propio fabricante.'),
                ('¿Cuánto tarda la entrega?', 'Se fabrica bajo pedido. El plazo se confirma por escrito en el presupuesto, antes de pedir nada. El transporte va aparte.')]
    if l == 'ca':
        lic = (f'Sí. Fa {L} m, així que sempre necessita la Llicència de Navegació o superior, sigui quin sigui el motor.' if over5 else
               f'Depèn del motor. Fa {L} m: sense títol només el pots portar amb un motor de fins a 15 CV, per a ús privat, de dia, a no més de 2 milles nàutiques del port, platja o lloc de sortida i sent major de 18 anys. Amb el motor que recomana la marca ({rec} CV) necessites la Llicència de Navegació o superior.')
        return [(f'Quant costa el {n}?', f'Des de {eur(price,l)} {t}, en versió Advantage i sense motor. Al configurador hi pots afegir un motor Mercury instal·lat a fàbrica i veure el total al moment. El remolc, el transport i la matriculació es pressuposten a part.'),
                (f'Necessito titulació per al {n}?', lic + f' <a href="{tg}">Veure titulacions</a>.'),
                ('Quin motor li poso?', f'La marca recomana {rec} CV amb eix llarg. Mai per sobre de la potència màxima de la placa CE: {hp} CV ({kw} kW).'),
                ('Quantes persones porta?', f'{pc} persones en categoria de disseny C i {pd} en categoria D. La càrrega màxima és de {cap} kg, comptant persones, motor, combustible i equipatge.'),
                ('Em serveix el carnet B per al remolc?', f'El buc pesa {w} kg sense motor. Amb el carnet B pots portar un remolc de fins a 750 kg de massa màxima autoritzada, o un de més pesat si el cotxe i el remolc junts no passen de 3.500 kg. Et dic quin remolc encaixa amb el teu vaixell i el teu cotxe.'),
                ('Quina garantia té?', 'SeaStorm dona una garantia comercial de 20 anys al buc davant de defectes de materials i fabricació, al primer comprador, amb un ús normal i amb les condicions i exclusions de la marca. El motor, el remolc i els accessoris tenen la garantia del seu fabricant.'),
                ('Quant triga l’entrega?', 'Es fabrica sota comanda. El termini es confirma per escrit al pressupost, abans de demanar res. El transport va a part.')]
    if l == 'en':
        lic = (f'Yes. It is {L} m long, so in Spain it always needs the Licencia de Navegación or higher, whatever the engine.' if over5 else
               f'It depends on the engine. It is {L} m long: in Spain you can only use it without a licence with an engine of up to 15 hp, for private use, by day, no more than 2 nautical miles from the port, beach or place of departure and if you are over 18. With the engine the brand recommends ({rec} hp) you need the Licencia de Navegación or higher.')
        return [(f'How much does the {n} cost?', f'From {eur(price,l)} {t}, Advantage version without engine. In the configurator you can add a factory-fitted Mercury engine and see the total instantly. Trailer, transport and registration are quoted separately.'),
                (f'Do I need a licence for the {n}?', lic + f' <a href="{tg}">Licences explained</a>.'),
                ('Which engine should I fit?', f'The brand recommends {rec} hp, long shaft. Never above the maximum power on its CE plate: {hp} hp ({kw} kW).'),
                ('How many people does it carry?', f'{pc} people in design category C and {pd} in category D. Maximum load is {cap} kg, including people, engine, fuel and gear.'),
                ('Can I tow it with a standard car licence?', f'The hull weighs {w} kg without engine. In Spain a B licence lets you tow a trailer of up to 750 kg gross weight, or a heavier one if car and trailer together are no more than 3,500 kg. I tell you which trailer suits your boat and your car.'),
                ('What warranty does it have?', 'SeaStorm gives a 20-year commercial hull warranty against material and manufacturing defects, to the first buyer, with normal use and subject to the brand’s terms and exclusions. Engine, trailer and accessories carry their own manufacturer’s warranty.'),
                ('How long is delivery?', 'It is built to order. Lead time is confirmed in writing in the quote, before you order anything. Transport is extra.')]
    lic = (f'Oui. Il mesure {L} m : en Espagne il faut toujours la Licencia de Navegación ou supérieur, quel que soit le moteur.' if over5 else
           f'Cela dépend du moteur. Il mesure {L} m : en Espagne, sans permis, seulement avec un moteur jusqu’à 15 ch, pour un usage privé, de jour, à 2 milles nautiques maximum du port, de la plage ou du lieu de départ et à partir de 18 ans. Avec le moteur recommandé par la marque ({rec} ch), il faut la Licencia de Navegación ou supérieur.')
    return [(f'Combien coûte le {n} ?', f'À partir de {eur(price,l)} {t}, version Advantage sans moteur. Dans le configurateur, vous pouvez ajouter un moteur Mercury monté en usine et voir le total immédiatement. La remorque, le transport et l’immatriculation sont chiffrés à part.'),
            (f'Faut-il un permis pour le {n} ?', lic + f' <a href="{tg}">Voir les permis</a>.'),
            ('Quel moteur choisir ?', f'La marque recommande {rec} ch, arbre long. Jamais au-dessus de la puissance maximale de sa plaque CE : {hp} ch ({kw} kW).'),
            ('Combien de personnes ?', f'{pc} personnes en catégorie de conception C et {pd} en catégorie D. La charge maximale est de {cap} kg, personnes, moteur, carburant et bagages compris.'),
            ('Le permis B suffit-il pour la remorque ?', f'La coque pèse {w} kg sans moteur. En Espagne, le permis B permet de tracter une remorque jusqu’à 750 kg de PTAC, ou plus lourde si voiture et remorque ensemble ne dépassent pas 3 500 kg. Je vous dis quelle remorque convient à votre bateau et à votre voiture.'),
            ('Quelle garantie ?', 'SeaStorm offre une garantie commerciale de 20 ans sur la coque contre les défauts de matériaux et de fabrication, au premier acheteur, pour un usage normal et selon les conditions et exclusions de la marque. Le moteur, la remorque et les accessoires ont la garantie de leur fabricant.'),
            ('Quel est le délai de livraison ?', 'Il est construit sur commande. Le délai est confirmé par écrit dans le devis, avant toute commande. Le transport est en sus.')]

def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))

def cut(h, sid, tag='section'):
    return re.sub(r'<%s class="[^"]*" id="%s".*?</%s>\n?' % (tag, sid, tag), '', h, count=1, flags=re.S)

FAQ_CSS = '<style>.ss-oth .ss-choose{margin-top:18px}</style>'

for l, p in LANGS.items():
    src = f'.{p}/seastorm/index.html'
    hub = open(src, encoding='utf-8').read()
    t = T[l]
    cards = {mm.group(2): mm.group(1) for mm in re.finditer(r'(<a class="ss-card" href="(?:#seastorm-|' + re.escape(p) + r'/seastorm/)([\w-]+)/?">.*?</a>)', hub, flags=re.S)}
    for m in M:
        slug, n, loa = m[0], m[1], m[2]
        url = f'{BASE}{p}/seastorm/{slug}/'
        h = hub
        head, body = h.split('</head>', 1)
        title = t['title'].format(n=n)
        desc = t['desc'].format(n=n, loa=num(loa, l), p=eur(m[12], l))
        head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', head, flags=re.S)
        for k, v in (('name="description"', desc), ('property="og:description"', desc), ('name="twitter:description"', desc),
                     ('property="og:title"', title), ('name="twitter:title"', title)):
            head = re.sub(r'(<meta ' + re.escape(k) + r' content=")[^"]*', lambda mm, v=v: mm.group(1) + html.escape(v, quote=True), head, count=1)
        head = re.sub(r'(href|content)="(https://www\.platamarine\.com(?:/ca|/en|/fr)?/seastorm/)"', lambda mm: f'{mm.group(1)}="{mm.group(2)}{slug}/"', head)
        head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
        fq = faq(m, l)
        art = re.search(r'<article class="ss-model" id="seastorm-%s">.*?</article>' % re.escape(slug), body, re.S).group(0)
        imgs = re.findall(r'data-src="(/seastorm/fotos/[^"]+\.jpg)"', art) or re.findall(r'src="(/seastorm/fotos/%s-\d+\.jpg)"' % re.escape(slug), art)
        dtext = strip(re.search(r'<p class="d">(.*?)</p>', art, re.S).group(1))
        prod = {"@type": "Product", "name": n, "url": url, "brand": {"@type": "Brand", "name": "SeaStorm"}, "description": dtext, "category": "Boat",
                "offers": {"@type": "Offer", "price": m[12], "priceCurrency": "EUR", "availability": "https://schema.org/PreOrder", "url": url,
                           "itemCondition": "https://schema.org/NewCondition", "seller": {"@type": "Organization", "name": "Plata Marine"},
                           "priceSpecification": {"@type": "UnitPriceSpecification", "price": m[12], "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}}
        if imgs:
            prod["image"] = [BASE + i for i in imgs]
        ld = [{"@context": "https://schema.org", **prod},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f"{BASE}{p}/"},
                  {"@type": "ListItem", "position": 2, "name": t['crumb'], "item": f"{BASE}{p}/barcos-nuevos/"},
                  {"@type": "ListItem", "position": 3, "name": "SeaStorm", "item": f"{BASE}{p}/seastorm/"},
                  {"@type": "ListItem", "position": 4, "name": n, "item": url}]},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                  {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in fq]}]
        head = head.replace('<style>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '<style>', 1)
        if imgs:
            head = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda mm: mm.group(1) + BASE + imgs[0], head, count=1)
            head = re.sub(r'<link rel="preload" as="image"[^>]*>', f'<link rel="preload" as="image" href="{imgs[0]}" imagesrcset="{imgs[0][:-4]}-m.jpg 800w, {imgs[0]} 1200w" imagesizes="100vw">', head, count=1)
        # idioma: el selector apunta a la página del modelo en cada idioma
        body = re.sub(r'(<div class="langsw".*?</div>)', lambda mm: re.sub(r'href="((?:/ca|/en|/fr)?/seastorm/)"', lambda x: f'href="{x.group(1)}{slug}/"', mm.group(1)), body, count=1, flags=re.S)
        # portada
        hero = re.search(r'<section class="ss-hero">.*?</section>', body, re.S).group(0)
        nh = hero
        if imgs:
            nh = re.sub(r'<img src="[^"]*" srcset="[^"]*" sizes="100vw" alt="[^"]*"', f'<img src="{imgs[0]}" srcset="{imgs[0][:-4]}-m.jpg 800w, {imgs[0]} 1200w" sizes="100vw" alt="{n}"', nh, count=1)
        nh = re.sub(r'(<p class="ss-crumb">.*?)<span>SeaStorm</span></p>', lambda mm: mm.group(1) + f'<a href="{p}/seastorm/">SeaStorm</a><span>·</span><span>{n}</span></p>', nh, count=1, flags=re.S)
        nh = re.sub(r'<h1>.*?</h1>', f'<h1>{n}</h1>', nh, count=1, flags=re.S)
        nh = re.sub(r'<p class="lead">.*?</p>', f'<p class="lead">{html.escape(dtext, quote=False)}</p>', nh, count=1, flags=re.S)
        nh = re.sub(r'(<p class="ss-hprice"><small>[^<]*</small> )[^<]*', lambda mm: mm.group(1) + eur(m[12], l), nh, count=1)
        nh = re.sub(r'(<a class="ss-btn ghost" href=")[^"]*', lambda mm: mm.group(1) + re.search(r'<a class="ss-btn wa" href="([^"]*)"', art).group(1), nh, count=1)
        body = body.replace(hero, nh, 1)
        # modelos: solo este, sin tarjetas de elección
        sec = re.search(r'<section class="ss-sec" id="modelos">.*?</section>', body, re.S).group(0)
        newsec = (f'<section class="ss-sec" id="modelos">\n  <div class="wrap">\n    <p class="ss-kick">{t["kick"].format(n=n)}</p><h2>{t["h2m"]}</h2>\n'
                  f'{art}\n  </div>\n</section>')
        body = body.replace(sec, newsec, 1)
        for sid in ('comparar', 'video'):
            body = cut(body, sid)
        body = re.sub(r'<section class="ss-sec ss-alt" id="video">.*?</section>\n?', '', body, count=1, flags=re.S)
        # configurador con el modelo marcado
        body = re.sub(r'(<input type="radio" name="cfg_m" value="[\w-]+")( checked)?', r'\1', body)
        body = body.replace(f'<input type="radio" name="cfg_m" value="{slug}"', f'<input type="radio" name="cfg_m" value="{slug}" checked', 1)
        # preguntas del modelo
        items = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{a}</p></details>' for q, a in fq)
        body = re.sub(r'(<section class="ss-sec ss-faq" id="faq">\s*<div class="wrap">)<h2[^>]*>.*?</div>\s*</section>',
                      lambda mm: mm.group(1) + f'<h2 style="margin-bottom:14px">{t["faq_h"].format(n=n)}</h2>{items}</div>\n</section>', body, count=1, flags=re.S)
        # otros modelos
        oth = ''.join(c for s2, c in cards.items() if s2 != slug)
        oth = re.sub(r'href="(?:#seastorm-|' + re.escape(p) + r'/seastorm/)([\w-]+)/?"', lambda mm: f'href="{p}/seastorm/{mm.group(1)}/"', oth)
        osec = f'<section class="ss-sec ss-oth" id="otros">{FAQ_CSS}<div class="wrap"><h2>{t["others"]}</h2><div class="ss-choose">{oth}</div></div></section>\n'
        body = body.replace('<section class="ss-sec ss-alt" id="presupuesto"', osec + '<section class="ss-sec ss-alt" id="presupuesto"', 1)
        # submenú: quitar anclas a secciones que ya no están
        body = re.sub(r'<a href="#(comparar|video)">[^<]*</a>', '', body)
        os.makedirs(f'.{p}/seastorm/{slug}', exist_ok=True)
        open(f'.{p}/seastorm/{slug}/index.html', 'w', encoding='utf-8').write(head + '</head>' + body)
    # en la página de marca, las tarjetas llevan a cada modelo
    hub2 = re.sub(r'<a class="ss-card" href="#seastorm-([\w-]+)">', lambda mm: f'<a class="ss-card" href="{p}/seastorm/{mm.group(1)}/">', hub)
    if hub2 != hub:
        open(src, 'w', encoding='utf-8').write(hub2)
    print(l, 'ok')
