#!/usr/bin/env python3
"""Fichas de modelo de motos de agua nuevas (ES/CA/EN/FR): /motos-de-agua-nuevas/<slug>/.
Datos técnicos del fabricante (fichas oficiales); precio "desde" = PVP recomendado 2027.
Uso: python3 _tools/build_motos_agua_fichas.py  (después: clean_urls.py)"""
import json, os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_motos_agua_nuevas as B

ROOT, SLUG, BASE, PFX, LANGS = B.ROOT, B.SLUG, B.BASE, B.PFX, B.LANGS
e = html.escape

L = {  # etiquetas comunes
 'es': dict(home='Inicio', sec='Motos de agua nuevas', btn='Pedir presupuesto', all='Ver todas las motos de agua', tit='Titulación: Licencia de Navegación o superior.',
            pvp='PVP recomendado por el fabricante, con IVA e impuesto de matriculación. Puede variar según la comunidad autónoma, la versión y los extras.',
            who='Para quién es', spec='Ficha técnica', eq='Equipamiento destacado', cmp='Si dudas, compárala con', see='Ver la comparativa',
            sell='¿Tienes una moto de agua para vender o dar a cambio?', sell_l='Te la gestiono o te la compro',
            small='Datos técnicos publicados por el fabricante para la gama actual; pueden variar en la versión 2027 y te los confirmo por escrito con el presupuesto. Información orientativa: podemos equivocarnos y no es vinculante.',
            wa='Hola Juan, quiero presupuesto de la moto de agua nueva {m} (2027). Te digo mi provincia y si necesito remolque: ',
            rows=['Motor', 'Potencia', 'Eslora', 'Manga', 'Altura', 'Peso en seco', 'Depósito', 'Almacenamiento', 'Plazas', 'Casco']),
 'ca': dict(home='Inici', sec="Motos d'aigua noves", btn='Demanar pressupost', all="Veure totes les motos d'aigua", tit='Titulació: Llicència de Navegació o superior.',
            pvp="PVP recomanat pel fabricant, amb IVA i impost de matriculació. Pot variar segons la comunitat autònoma, la versió i els extres.",
            who='Per a qui és', spec='Fitxa tècnica', eq='Equipament destacat', cmp='Si dubtes, compara-la amb', see='Veure la comparativa',
            sell="Tens una moto d'aigua per vendre o donar a canvi?", sell_l='Te la gestiono o te la compro',
            small="Dades tècniques publicades pel fabricant per a la gamma actual; poden variar en la versió 2027 i te les confirmo per escrit amb el pressupost. Informació orientativa: ens podem equivocar i no és vinculant.",
            wa="Hola Juan, vull pressupost de la moto d'aigua nova {m} (2027). Et dic la meva província i si necessito remolc: ",
            rows=['Motor', 'Potència', 'Eslora', 'Mànega', 'Alçada', 'Pes en sec', 'Dipòsit', 'Emmagatzematge', 'Places', 'Buc']),
 'en': dict(home='Home', sec='New jet skis', btn='Ask for a quote', all='See all jet skis', tit='Licence: Spanish Licencia de Navegación (LN) or higher.',
            pvp="Manufacturer's recommended retail price, including Spanish VAT and registration tax. It may vary by region, version and extras.",
            who="Who it's for", spec='Specifications', eq='Key equipment', cmp='If in doubt, compare it with', see='See the comparison',
            sell='Got a jet ski to sell or trade in?', sell_l='I can sell it for you or buy it',
            small="Technical data published by the manufacturer for the current range; it may vary on the 2027 version and I confirm it in writing with the quote. Indicative information: we may be wrong and it is not binding.",
            wa="Hi Juan, I'd like a quote for the new {m} jet ski (2027). My area and whether I need a trailer: ",
            rows=['Engine', 'Power', 'Length', 'Width', 'Height', 'Dry weight', 'Fuel tank', 'Storage', 'Seats', 'Hull']),
 'fr': dict(home='Accueil', sec='Jet-skis neufs', btn='Demander un devis', all='Voir tous les jet-skis', tit='Permis : Licencia de Navegación espagnole (LN) ou supérieure.',
            pvp='Prix de vente conseillé par le fabricant, TVA espagnole et taxe d’immatriculation incluses. Il peut varier selon la région, la version et les options.',
            who='Pour qui', spec='Fiche technique', eq='Équipement principal', cmp='Si vous hésitez, comparez-le avec', see='Voir le comparatif',
            sell='Un jet-ski à vendre ou à reprendre ?', sell_l='Je gère la vente ou je vous l’achète',
            small="Données techniques publiées par le fabricant pour la gamme actuelle ; elles peuvent varier sur la version 2027 et je vous les confirme par écrit avec le devis. Information indicative : nous pouvons nous tromper et elle n’est pas contractuelle. Nous ne parlons pas français : nous utilisons un traducteur.",
            wa='Bonjour Juan, je voudrais un devis pour le jet-ski neuf {m} (2027). Ma région et si j’ai besoin d’une remorque : ',
            rows=['Moteur', 'Puissance', 'Longueur', 'Largeur', 'Hauteur', 'Poids à sec', 'Réservoir', 'Rangement', 'Places', 'Coque'])}

M = [
 dict(slug='sea-doo-spark', key='sd-spark', brand='Sea-Doo', name='Sea-Doo Spark', price=9899, vs='sea-doo-spark-x',
      spec={'es': ['Rotax 900 ACE, 899 cc', '60 cv o 90 cv', '2,83 m', '1,17 m', '1,06 m', '194-196 kg', '30 l', '44,7 l', '2', 'Polytec'],
            'ca': ['Rotax 900 ACE, 899 cc', '60 cv o 90 cv', '2,83 m', '1,17 m', '1,06 m', '194-196 kg', '30 l', '44,7 l', '2', 'Polytec'],
            'en': ['Rotax 900 ACE, 899 cc', '60 hp or 90 hp', '2.83 m', '1.17 m', '1.06 m', '194-196 kg', '30 l', '44.7 l', '2', 'Polytec'],
            'fr': ['Rotax 900 ACE, 899 cm³', '60 ch ou 90 ch', '2,83 m', '1,17 m', '1,06 m', '194-196 kg', '30 l', '44,7 l', '2', 'Polytec']},
      txt={'es': ('Sea-Doo Spark 2027: precio desde 9.899 € y ficha técnica', 'Sea-Doo Spark 2027 desde 9.899 €: la moto de agua más ligera de Sea-Doo, 60 o 90 cv y 2 plazas. Ficha técnica, equipamiento y presupuesto por WhatsApp.',
                   'La Spark es la moto de agua más ligera y económica de Sea-Doo: pesa menos de 200 kg en seco, se remolca con facilidad y es sencilla de llevar. Es la opción lógica para empezar o para salir con calma en verano. Si vais a ir dos adultos a menudo o queréis más potencia, mira la versión de 90 cv o la Spark X.',
                   ['Freno y marcha atrás iBR', 'Modo ECO (y Sport en la versión de 90 cv)', 'Pantalla digital de 4,5"', 'Casco de Polytec, ligero y resistente', 'Audio portátil BRP opcional'], 'Spark X 110 y Spark Trixx'),
           'ca': ('Sea-Doo Spark 2027: preu des de 9.899 € i fitxa tècnica', "Sea-Doo Spark 2027 des de 9.899 €: la moto d'aigua més lleugera de Sea-Doo, 60 o 90 cv i 2 places. Fitxa tècnica, equipament i pressupost per WhatsApp.",
                   "La Spark és la moto d'aigua més lleugera i econòmica de Sea-Doo: pesa menys de 200 kg en sec, es remolca amb facilitat i és senzilla de portar. És l'opció lògica per començar o per sortir amb calma a l'estiu. Si hi anireu dos adults sovint o voleu més potència, mira la versió de 90 cv o la Spark X.",
                   ['Fre i marxa enrere iBR', 'Mode ECO (i Sport a la versió de 90 cv)', 'Pantalla digital de 4,5"', 'Buc de Polytec, lleuger i resistent', 'Àudio portàtil BRP opcional'], 'Spark X 110 i Spark Trixx'),
           'en': ('Sea-Doo Spark 2027: price from €9,899 and specs', "Sea-Doo Spark 2027 from €9,899: Sea-Doo's lightest jet ski, 60 or 90 hp and 2 seats. Specs, equipment and quote on WhatsApp.",
                   "The Spark is Sea-Doo's lightest and most affordable jet ski: under 200 kg dry, easy to tow and easy to ride. It is the logical choice to get started or for relaxed summer rides. If two adults will ride often or you want more power, look at the 90 hp version or the Spark X.",
                   ['iBR brake and reverse', 'ECO mode (plus Sport on the 90 hp)', '4.5" digital display', 'Light, tough Polytec hull', 'Optional BRP portable audio'], 'Spark X 110 and Spark Trixx'),
           'fr': ('Sea-Doo Spark 2027 : prix dès 9 899 € et fiche technique', 'Sea-Doo Spark 2027 à partir de 9 899 € : le jet-ski le plus léger de Sea-Doo, 60 ou 90 ch et 2 places. Fiche technique, équipement et devis par WhatsApp.',
                   "Le Spark est le jet-ski le plus léger et le plus abordable de Sea-Doo : moins de 200 kg à sec, facile à remorquer et à piloter. C’est le choix logique pour débuter ou pour des sorties tranquilles l’été. Si vous êtes souvent deux adultes ou voulez plus de puissance, regardez la version 90 ch ou le Spark X.",
                   ['Frein et marche arrière iBR', 'Mode ECO (et Sport sur la 90 ch)', 'Écran numérique 4,5"', 'Coque en Polytec, légère et résistante', 'Audio portable BRP en option'], 'Spark X 110 et Spark Trixx')}),
 dict(slug='sea-doo-gtx-170', key='sd-gtx', brand='Sea-Doo', name='Sea-Doo GTX 170', price=24099,
      spec={'es': ['Rotax 1630 ACE, 1.630 cc', '170 cv', '3,45 m', '1,25 m', '1,14 m', '352 kg', '70 l', '98,9 l', '3', 'ST3, fibra de vidrio'],
            'ca': ['Rotax 1630 ACE, 1.630 cc', '170 cv', '3,45 m', '1,25 m', '1,14 m', '352 kg', '70 l', '98,9 l', '3', 'ST3, fibra de vidre'],
            'en': ['Rotax 1630 ACE, 1,630 cc', '170 hp', '3.45 m', '1.25 m', '1.14 m', '352 kg', '70 l', '98.9 l', '3', 'ST3, fibreglass'],
            'fr': ['Rotax 1630 ACE, 1 630 cm³', '170 ch', '3,45 m', '1,25 m', '1,14 m', '352 kg', '70 l', '98,9 l', '3', 'ST3, fibre de verre']},
      txt={'es': ('Sea-Doo GTX 170 2027: precio desde 24.099 € y ficha técnica', 'Sea-Doo GTX 170 2027 desde 24.099 €: Touring de 170 cv, 3 plazas, casco ST3 y 70 l de depósito. Ficha técnica, equipamiento y presupuesto por WhatsApp.',
                   'La GTX 170 es la Touring de entrada de Sea-Doo: tres plazas, casco ST3 estable y un depósito de 70 litros para hacer millas sin estar pendiente de repostar. Es una buena opción para salir en pareja o en familia cuando se busca comodidad antes que velocidad. Si queréis más potencia para tirar de esquí o ir cargados, mira la GTX 230.',
                   ['Motor Rotax 1630 ACE de 170 cv', 'Freno y marcha atrás iBR', 'Control de crucero y modo de baja velocidad', 'Pantalla digital de 7,6"', 'Casco ST3 de fibra, más estable', 'Guantera y 96 l de cofre delantero'], 'Kawasaki Ultra 160LX'),
           'ca': ('Sea-Doo GTX 170 2027: preu des de 24.099 € i fitxa tècnica', 'Sea-Doo GTX 170 2027 des de 24.099 €: Touring de 170 cv, 3 places, buc ST3 i 70 l de dipòsit. Fitxa tècnica, equipament i pressupost per WhatsApp.',
                   "La GTX 170 és la Touring d'entrada de Sea-Doo: tres places, buc ST3 estable i un dipòsit de 70 litres per fer milles sense estar pendent de repostar. És una bona opció per sortir en parella o en família quan es busca comoditat abans que velocitat. Si voleu més potència per arrossegar esquí o anar carregats, mira la GTX 230.",
                   ['Motor Rotax 1630 ACE de 170 cv', 'Fre i marxa enrere iBR', 'Control de creuer i mode de baixa velocitat', 'Pantalla digital de 7,6"', 'Buc ST3 de fibra, més estable', 'Guantera i 96 l de cofre davanter'], 'Kawasaki Ultra 160LX'),
           'en': ('Sea-Doo GTX 170 2027: price from €24,099 and specs', 'Sea-Doo GTX 170 2027 from €24,099: 170 hp touring jet ski, 3 seats, ST3 hull and 70 l tank. Specs, equipment and quote on WhatsApp.',
                   "The GTX 170 is Sea-Doo's entry touring model: three seats, a stable ST3 hull and a 70-litre tank to cover miles without worrying about refuelling. A good choice for riding as a couple or with the family when comfort matters more than speed. If you want more power for towing or riding loaded, look at the GTX 230.",
                   ['Rotax 1630 ACE 170 hp engine', 'iBR brake and reverse', 'Cruise control and slow-speed mode', '7.6" digital display', 'Stable fibreglass ST3 hull', 'Glovebox and 96 l front storage'], 'Kawasaki Ultra 160LX'),
           'fr': ('Sea-Doo GTX 170 2027 : prix dès 24 099 € et fiche technique', 'Sea-Doo GTX 170 2027 à partir de 24 099 € : randonnée 170 ch, 3 places, coque ST3 et réservoir de 70 l. Fiche technique, équipement et devis par WhatsApp.',
                   "Le GTX 170 est le modèle de randonnée d’entrée de Sea-Doo : trois places, une coque ST3 stable et un réservoir de 70 litres pour faire des milles sans penser au plein. Un bon choix à deux ou en famille quand on privilégie le confort à la vitesse. Pour plus de puissance pour tracter ou rouler chargé, regardez le GTX 230.",
                   ['Moteur Rotax 1630 ACE de 170 ch', 'Frein et marche arrière iBR', 'Régulateur de vitesse et mode basse vitesse', 'Écran numérique 7,6"', 'Coque ST3 en fibre, plus stable', 'Boîte à gants et coffre avant de 96 l'], 'Kawasaki Ultra 160LX')}),
 dict(slug='kawasaki-ultra-310lx', key='kw-ultra-310lx-2027', brand='Kawasaki', name='Kawasaki Ultra 310LX', price=30725,
      spec={'es': ['4 cilindros, 1.498 cc, con compresor e intercooler', '300 CV', '3,58 m', '1,195 m', '1,195 m', '452 kg', '80 l', '168,5 l', '3', 'Deep-V'],
            'ca': ['4 cilindres, 1.498 cc, amb compressor i intercooler', '300 CV', '3,58 m', '1,195 m', '1,195 m', '452 kg', '80 l', '168,5 l', '3', 'Deep-V'],
            'en': ['4-cylinder, 1,498 cc, supercharged with intercooler', '300 PS', '3.58 m', '1.195 m', '1.195 m', '452 kg', '80 l', '168.5 l', '3', 'Deep-V'],
            'fr': ['4 cylindres, 1 498 cm³, compresseur et intercooler', '300 ch', '3,58 m', '1,195 m', '1,195 m', '452 kg', '80 l', '168,5 l', '3', 'Deep-V']},
      txt={'es': ('Kawasaki Ultra 310LX 2027: precio desde 30.725 € y ficha', 'Kawasaki Ultra 310LX 2027 desde 30.725 €: 300 CV con compresor, 3 plazas, 80 l de depósito y 168 l de almacenamiento. Ficha técnica y presupuesto por WhatsApp.',
                   'La Ultra 310LX es la moto de agua más completa de Kawasaki: motor de 1.498 cc con compresor, 300 CV, 80 litros de depósito y 168 litros de almacenamiento. Lleva pantalla a color de 7", audio JETSOUND, cámara trasera y marcha atrás. Está pensada para quien sale a menudo, lejos y acompañado.',
                   ['Compresor con intercooler, 300 CV', 'Pantalla TFT a color de 7" con Bluetooth', 'Audio JETSOUND 4s', 'Cámara trasera', 'Marcha atrás inteligente con deceleración (KSRD)', 'Control de crucero', 'Asiento ERGO-FIT LXury de 3 posiciones'], 'Sea-Doo GTX Limited 350'),
           'ca': ('Kawasaki Ultra 310LX 2027: preu des de 30.725 € i fitxa', 'Kawasaki Ultra 310LX 2027 des de 30.725 €: 300 CV amb compressor, 3 places, 80 l de dipòsit i 168 l d\'emmagatzematge. Fitxa tècnica i pressupost per WhatsApp.',
                   "La Ultra 310LX és la moto d'aigua més completa de Kawasaki: motor de 1.498 cc amb compressor, 300 CV, 80 litres de dipòsit i 168 litres d'emmagatzematge. Porta pantalla a color de 7\", àudio JETSOUND, càmera posterior i marxa enrere. Està pensada per a qui surt sovint, lluny i acompanyat.",
                   ['Compressor amb intercooler, 300 CV', 'Pantalla TFT a color de 7" amb Bluetooth', 'Àudio JETSOUND 4s', 'Càmera posterior', 'Marxa enrere intel·ligent amb desacceleració (KSRD)', 'Control de creuer', 'Seient ERGO-FIT LXury de 3 posicions'], 'Sea-Doo GTX Limited 350'),
           'en': ('Kawasaki Ultra 310LX 2027: price from €30,725 and specs', 'Kawasaki Ultra 310LX 2027 from €30,725: 300 PS supercharged, 3 seats, 80 l tank and 168 l of storage. Specs and quote on WhatsApp.',
                   "The Ultra 310LX is Kawasaki's most complete jet ski: a 1,498 cc supercharged engine, 300 PS, an 80-litre tank and 168 litres of storage. It has a 7\" colour display, JETSOUND audio, a rear camera and reverse. Built for riders who go out often, far and with company.",
                   ['Supercharger with intercooler, 300 PS', '7" colour TFT display with Bluetooth', 'JETSOUND 4s audio', 'Rear camera', 'Kawasaki Smart Reverse with Deceleration (KSRD)', 'Cruise control', 'ERGO-FIT LXury seat with 3 positions'], 'Sea-Doo GTX Limited 350'),
           'fr': ('Kawasaki Ultra 310LX 2027 : prix dès 30 725 € et fiche', 'Kawasaki Ultra 310LX 2027 à partir de 30 725 € : 300 ch avec compresseur, 3 places, réservoir de 80 l et 168 l de rangement. Fiche technique et devis par WhatsApp.',
                   "L’Ultra 310LX est le jet-ski le plus complet de Kawasaki : moteur 1 498 cm³ à compresseur, 300 ch, réservoir de 80 litres et 168 litres de rangement. Il a un écran couleur 7\", l’audio JETSOUND, une caméra arrière et la marche arrière. Pensé pour ceux qui sortent souvent, loin et accompagnés.",
                   ['Compresseur avec intercooler, 300 ch', 'Écran TFT couleur 7" avec Bluetooth', 'Audio JETSOUND 4s', 'Caméra arrière', 'Marche arrière intelligente avec décélération (KSRD)', 'Régulateur de vitesse', 'Selle ERGO-FIT LXury 3 positions'], 'Sea-Doo GTX Limited 350')}),
]


def page(m, lang):
    t, l, p = B.T[lang], L[lang], PFX[lang]
    title, desc, who, eq, alt = m['txt'][lang]
    url = f'{BASE}{p}/{SLUG}/{m["slug"]}/'
    pr = B.FROM[lang].format(p=B.money(m['price'], lang))
    src = open(os.path.join(ROOT, p.lstrip('/'), SLUG, 'index.html'), encoding='utf-8').read()
    head_top = src[:src.index('<title>')]
    styles = src[src.index('<style>'):src.index('</head>')]
    body_top = src[src.index('</head>'):src.index('<main')]
    for l2 in LANGS:  # selector de idioma a la ficha
        body_top = body_top.replace(f'{BASE}{PFX[l2]}/{SLUG}/"', f'{BASE}{PFX[l2]}/{SLUG}/{m["slug"]}/"')
    foot = src[src.index('</main>'):]
    alt_links = ''.join(f'<link rel="alternate" hreflang="{x}" href="{BASE}{PFX[x]}/{SLUG}/{m["slug"]}/">\n' for x in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{BASE}/{SLUG}/{m["slug"]}/">\n'
    img = f'{BASE}/{SLUG}/fotos/{m["key"]}.jpg'
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f'{BASE}{p}/'},
            {"@type": "ListItem", "position": 2, "name": l['sec'], "item": f'{BASE}{p}/{SLUG}/'},
            {"@type": "ListItem", "position": 3, "name": m['name'] + ' 2027', "item": url}]},
          {"@context": "https://schema.org", "@type": "Product", "name": m['name'] + ' 2027', "brand": {"@type": "Brand", "name": m['brand']},
           "image": [img], "description": desc,
           "offers": {"@type": "Offer", "price": str(m['price']), "priceCurrency": "EUR", "availability": "https://schema.org/PreOrder", "url": url,
                      "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(m['price']), "priceCurrency": "EUR", "valueAddedTaxIncluded": True}}}]
    head = (head_top + f'<title>{e(title)}</title>\n<meta name="description" content="{e(desc)}">\n<link rel="canonical" href="{url}">\n{alt_links}'
            f'<meta property="og:title" content="{e(title)}">\n<meta property="og:description" content="{e(desc)}">\n<meta property="og:type" content="product">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{img}">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<link rel="icon" type="image/png" href="/logo-plata-marine.png">\n<link rel="stylesheet" href="/barcos/barcos.css">\n'
            '<script src="/consent.js?v=20261006" defer></script>\n<script src="/analytics.js?v=20261006" defer></script>\n<link rel="stylesheet" href="/nav.css?v=20261019">\n'
            + ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + styles +
            '<style>.mf-dl{display:grid;grid-template-columns:1fr 1fr;gap:0 28px;max-width:760px;margin-top:14px}.mf-dl div{display:flex;justify-content:space-between;gap:12px;padding:11px 0;border-bottom:1px solid #e3e9ec}.mf-dl dt{color:#5b6b75}.mf-dl dd{margin:0;font-weight:600;text-align:right}.mf-ul{columns:2;gap:28px;max-width:760px;padding-left:18px;line-height:1.7;color:#33474f}.mf-pr{font-size:1.5rem;font-weight:700;margin:4px 0 2px}.mf-pvp{font-size:.82rem;color:#5b6b75;margin:0 0 18px;max-width:52ch}@media(max-width:700px){.mf-dl{grid-template-columns:1fr}.mf-ul{columns:1}}</style>\n')
    wa = B.wa(l['wa'].format(m=m['name']))
    vs_href = f'{p}/{SLUG}/#comparar' if m['slug'] != 'sea-doo-spark' else f'{p}/{SLUG}/#sea-doo'
    main = ('<main class="rm">'
            f'<div class="wrap"><p class="rm-crumb"><a href="{p}/">{l["home"]}</a> · <a href="{p}/{SLUG}/">{l["sec"]}</a> · {e(m["name"])} 2027</p></div>'
            f'<section class="wrap rm-hero"><div><p class="k">{e(m["brand"])} · 2027</p><h1>{e(m["name"])} 2027</h1>'
            f'<p class="mf-pr">{pr}</p><p class="mf-pvp">{l["pvp"]}</p><p style="font-weight:600;margin:0 0 16px">{l["tit"]}</p>'
            f'<div class="mj-jump"><a class="btn btn-wa" href="{e(wa)}" target="_blank" rel="noopener" data-wa-context="moto_agua_ficha">{l["btn"]}</a>'
            f'<a class="btn" href="{p}/{SLUG}/">{l["all"]}</a></div></div>'
            f'<div><img class="mj-hero-img" src="/{SLUG}/fotos/{m["key"]}.jpg" alt="{e(m["name"])} 2027" width="900" height="675"></div></section>'
            f'<section class="rm-sec"><div class="wrap"><h2>{l["who"]}</h2><p>{who}</p></div></section>'
            f'<section class="rm-sec"><div class="wrap"><h2>{l["spec"]}</h2><dl class="mf-dl">'
            + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in zip(l['rows'], m['spec'][lang])) + '</dl></div></section>'
            f'<section class="rm-sec"><div class="wrap"><h2>{l["eq"]}</h2><ul class="mf-ul">' + ''.join(f'<li>{x}</li>' for x in eq) + '</ul>'
            f'<p style="margin-top:18px"><b>{l["cmp"]}:</b> {alt}. <a href="{vs_href}">{l["see"]} →</a></p></div></section>'
            f'<div class="wrap"><div class="rm-end"><h2>{e(m["name"])} 2027 · {pr}</h2><a class="btn btn-wa" href="{e(wa)}" target="_blank" rel="noopener" data-wa-context="moto_agua_ficha">{l["btn"]}</a></div>'
            f'<p style="text-align:center;margin:-16px 0 28px">{l["sell"]} <a href="{p}/{SLUG}/#vender">{l["sell_l"]}</a></p>'
            f'<p class="rm-small">{B.T[lang]["small"].split(". ")[0]}. {l["small"]}</p></div>\n')
    out = head + body_top + main + foot
    d = os.path.join(ROOT, p.lstrip('/'), SLUG, m['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
    return d


if __name__ == '__main__':
    for m in M:
        for lang in LANGS: print(page(m, lang))
