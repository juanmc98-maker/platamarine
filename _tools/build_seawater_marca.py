"""Página de marca /seawater/ (ES/CA/EN/FR). Toma cabecera, estilos y pie de una página de modelo ya generada
(_tools/build_seawater_modelos.py) y monta: portada con logo, rejilla de modelos (de más premium a más económico),
cómo se compra, preguntas y cierre. Uso: python3 _tools/build_seawater_marca.py"""
import json, os, re, html, urllib.parse
ROOT = '.'; SITE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
D = os.path.join(ROOT, '_tools', 'seawater_data')
TAR = {m['slug']: m for m in json.load(open(os.path.join(D, 'tarifa.json')))}
META = json.load(open(os.path.join(D, 'meta.json')))
EX = json.load(open(os.path.join(D, 'existing.json')))
E = html.escape
ORDER = sorted(TAR, key=lambda s: -TAR[s]['price'])
CAB = {'kymera-53', 'phantom-500', 'kymera-43', 'phantom-500-yachting'}
def eur(n, lg):
    s = f'{n:,}'
    return '€' + s if lg == 'en' else (s.replace(',', ' ') + ' €' if lg == 'fr' else s.replace(',', '.') + ' €')
def m2(v, lg): return (f'{v:.2f}'.replace('.', ',') if lg != 'en' else f'{v:.2f}') + ' m'
T = {
'es': dict(title='Sea Water y Kymera: precios y configurador · Plata Marine',
  desc='Semirrígidas Sea Water (Phantom y Ghost) y Kymera nuevas, bajo pedido: 11 modelos de 7 a 16 m con fotos, ficha técnica y configurador con la tarifa oficial.',
  home='Inicio', boats='Barcos en venta', new='Barcos nuevos', kick='Semirrígidas · bajo pedido',
  lead='Las semirrígidas Phantom y Ghost y los Kymera 43 y 53: once modelos de 7 a 16 metros, con el equipamiento de serie, la ficha técnica y un configurador con los precios de la tarifa oficial.',
  cta='Ver los modelos', cta2='Pedir presupuesto', from_='Desde', vat='+ impuestos', noeng='sin motores', kind={'cab': 'Con camarote', 'open': 'Open'},
  g_k='La gama', g_h='Elige tu modelo', g_s='Ordenados de mayor a menor. En cada modelo tienes fotos, lo que lleva de serie, la ficha técnica y el configurador con los opcionales.',
  how_h='Cómo se compra', how=[('Lo hablamos', 'Me cuentas cómo vas a usarla y te ayudo a elegir modelo, motores y opcionales.'), ('Presupuesto por escrito', 'Con tu configuración te paso el precio cerrado: barco, opcionales, motores y transporte.'), ('Pedido a fábrica', 'Se fabrica bajo pedido. Yo me ocupo del pedido y del seguimiento.'), ('Entrega', 'Te acompaño en la entrega, los papeles y la matriculación.')],
  faq_h='Preguntas frecuentes', faq=[('¿Qué incluyen los precios?', 'El barco con el equipamiento de serie, en fábrica y sin impuestos. Los motores, el transporte, el IVA, el impuesto de matriculación (en barcos de más de 8 m de casco) y la matriculación van aparte y te los detallo en el presupuesto.'),
   ('¿Y los motores?', 'Se presupuestan aparte, según el modelo y la potencia que elijas (Mercury o Yamaha). Dime qué uso le vas a dar y te preparo la propuesta.'),
   ('¿Qué titulación necesito?', 'Depende de la eslora de casco de cada modelo: la Phantom 230 y la 260 se llevan con PNB o superior; el resto, con PER o superior (el Kymera 53, con PER ampliado a 24 m). Es orientativo: confírmalo con tu escuela o con Capitanía.'),
   ('¿Cuál es el plazo de entrega?', 'A consultar: depende del modelo, de los opcionales y de la carga del astillero en el momento del pedido. Te lo confirmo por escrito con el presupuesto.')],
  end_h='¿Hablamos de tu Sea Water?', end_p='Escríbeme y lo vemos con calma. Sin compromiso.', wa='Escribir por WhatsApp', wa_txt='Hola Juan, me interesa una Sea Water.',
  small='Precios de la tarifa del astillero 2026, sin IVA, sin motores y en fábrica. No incluyen motores, transporte, impuesto de matriculación ni matriculación. Pueden cambiar y no son vinculantes: el precio final es el del presupuesto por escrito. Fotos y datos técnicos del fabricante; las fotos pueden mostrar equipamiento opcional. Podemos equivocarnos; si ves un error, avísanos.'),
'ca': dict(title='Sea Water i Kymera: preus i configurador · Plata Marine',
  desc='Semirígides Sea Water (Phantom i Ghost) i Kymera noves, per encàrrec: 11 models de 7 a 16 m amb fotos, fitxa tècnica i configurador amb la tarifa oficial.',
  home='Inici', boats='Vaixells en venda', new='Vaixells nous', kick='Semirígides · per encàrrec',
  lead='Les semirígides Phantom i Ghost i els Kymera 43 i 53: onze models de 7 a 16 metres, amb l’equipament de sèrie, la fitxa tècnica i un configurador amb els preus de la tarifa oficial.',
  cta='Veure els models', cta2='Demanar pressupost', from_='Des de', vat='+ impostos', noeng='sense motors', kind={'cab': 'Amb cabina', 'open': 'Open'},
  g_k='La gamma', g_h='Tria el teu model', g_s='Ordenats de més gran a més petit. A cada model hi tens fotos, el que porta de sèrie, la fitxa tècnica i el configurador amb els opcionals.',
  how_h='Com es compra', how=[('Ho parlem', 'M’expliques com la faràs servir i t’ajudo a triar model, motors i opcionals.'), ('Pressupost per escrit', 'Amb la teva configuració et passo el preu tancat: vaixell, opcionals, motors i transport.'), ('Comanda a fàbrica', 'Es fabrica per encàrrec. Jo m’ocupo de la comanda i del seguiment.'), ('Lliurament', 'T’acompanyo en el lliurament, els papers i la matriculació.')],
  faq_h='Preguntes freqüents', faq=[('Què inclouen els preus?', 'El vaixell amb l’equipament de sèrie, a fàbrica i sense impostos. Els motors, el transport, l’IVA, l’impost de matriculació (en vaixells de més de 8 m de buc) i la matriculació van a part i te’ls detallo al pressupost.'),
   ('I els motors?', 'Es pressuposten a part, segons el model i la potència que triïs (Mercury o Yamaha). Digues-me quin ús li donaràs i et preparo la proposta.'),
   ('Quina titulació necessito?', 'Depèn de l’eslora de buc de cada model: la Phantom 230 i la 260 es porten amb PNB o superior; la resta, amb PER o superior (el Kymera 53, amb PER ampliat a 24 m). És orientatiu: confirma-ho amb la teva escola o amb Capitania.'),
   ('Quin és el termini de lliurament?', 'A consultar: depèn del model, dels opcionals i de la càrrega de la drassana en el moment de la comanda. T’ho confirmo per escrit amb el pressupost.')],
  end_h='Parlem de la teva Sea Water?', end_p='Escriu-me i ho mirem amb calma. Sense compromís.', wa='Escriure per WhatsApp', wa_txt='Hola Juan, m’interessa una Sea Water.',
  small='Preus de la tarifa de la drassana 2026, sense IVA, sense motors i a fàbrica. No inclouen motors, transport, impost de matriculació ni matriculació. Poden canviar i no són vinculants: el preu final és el del pressupost per escrit. Fotos i dades tècniques del fabricant; les fotos poden mostrar equipament opcional. Ens podem equivocar; si veus un error, avisa’ns.'),
'en': dict(title='Sea Water and Kymera: prices and configurator · Plata Marine',
  desc='New Sea Water (Phantom and Ghost) and Kymera RIBs, built to order: 11 models from 7 to 16 m with photos, specifications and a configurator with the official price list.',
  home='Home', boats='Boats for sale', new='New boats', kick='RIBs · built to order',
  lead='The Phantom and Ghost RIBs and the Kymera 43 and 53: eleven models from 7 to 16 metres, with standard equipment, specifications and a configurator with the official price list.',
  cta='See the models', cta2='Ask for a quote', from_='From', vat='+ taxes', noeng='without engines', kind={'cab': 'With cabin', 'open': 'Open'},
  g_k='The range', g_h='Choose your model', g_s='From largest to smallest. Each model has photos, standard equipment, specifications and the configurator with the options.',
  how_h='How to buy', how=[('We talk', 'Tell me how you will use it and I will help you choose model, engines and options.'), ('Written quote', 'With your configuration I send you a firm price: boat, options, engines and transport.'), ('Factory order', 'Built to order. I handle the order and follow it up.'), ('Delivery', 'I am with you at delivery, with the paperwork and the registration.')],
  faq_h='Frequently asked questions', faq=[('What do the prices include?', 'The boat with standard equipment, ex works, excluding taxes. Engines, transport, VAT, the Spanish registration tax (for hulls over 8 m) and registration are extra and detailed in the quote.'),
   ('What about the engines?', 'They are quoted separately, depending on the model and the power you choose (Mercury or Yamaha). Tell me how you will use the boat and I will prepare a proposal.'),
   ('Which licence do I need?', 'It depends on each model’s hull length: the Phantom 230 and 260 need a Spanish PNB licence or higher; the rest a PER or higher (the Kymera 53, PER extended to 24 m). This is a guide only: please check with your sailing school or the harbour authority.'),
   ('What is the delivery time?', 'On request: it depends on the model, the options and the yard’s workload when the order is placed. I will confirm it in writing with the quote.')],
  end_h='Shall we talk about your Sea Water?', end_p='Write to me and we will look at it calmly. No commitment.', wa='Message on WhatsApp', wa_txt='Hi Juan, I am interested in a Sea Water.',
  small='Prices from the 2026 shipyard price list, excluding VAT and engines, ex works. They do not include engines, transport, registration tax or registration. They may change and are not binding: the final price is the one in the written quote. Photos and technical data from the manufacturer; photos may show optional equipment. We may make mistakes; if you spot one, please let us know.'),
'fr': dict(title='Sea Water et Kymera : prix et configurateur · Plata Marine',
  desc='Semi-rigides Sea Water (Phantom et Ghost) et Kymera neufs, sur commande : 11 modèles de 7 à 16 m avec photos, fiche technique et configurateur au tarif officiel.',
  home='Accueil', boats='Bateaux à vendre', new='Bateaux neufs', kick='Semi-rigides · sur commande',
  lead='Les semi-rigides Phantom et Ghost et les Kymera 43 et 53 : onze modèles de 7 à 16 mètres, avec l’équipement de série, la fiche technique et un configurateur au tarif officiel.',
  cta='Voir les modèles', cta2='Demander un devis', from_='À partir de', vat='+ taxes', noeng='sans moteurs', kind={'cab': 'Avec cabine', 'open': 'Open'},
  g_k='La gamme', g_h='Choisissez votre modèle', g_s='Du plus grand au plus petit. Chaque modèle a ses photos, l’équipement de série, la fiche technique et le configurateur avec les options.',
  how_h='Comment acheter', how=[('On en parle', 'Vous me dites comment vous l’utiliserez et je vous aide à choisir modèle, moteurs et options.'), ('Devis écrit', 'Avec votre configuration, je vous envoie un prix ferme : bateau, options, moteurs et transport.'), ('Commande usine', 'Construit sur commande. Je m’occupe de la commande et du suivi.'), ('Livraison', 'Je vous accompagne à la livraison, pour les papiers et l’immatriculation.')],
  faq_h='Questions fréquentes', faq=[('Que comprennent les prix ?', 'Le bateau avec l’équipement de série, départ usine, hors taxes. Les moteurs, le transport, la TVA, la taxe d’immatriculation espagnole (coques de plus de 8 m) et l’immatriculation sont en sus et détaillés dans le devis.'),
   ('Et les moteurs ?', 'Ils sont chiffrés à part, selon le modèle et la puissance choisie (Mercury ou Yamaha). Dites-moi l’usage prévu et je prépare une proposition.'),
   ('Quel permis faut-il ?', 'Cela dépend de la longueur de coque de chaque modèle : les Phantom 230 et 260 se conduisent avec le PNB espagnol ou supérieur ; les autres avec le PER ou supérieur (le Kymera 53, PER étendu à 24 m). C’est indicatif : vérifiez auprès de votre école ou de la Capitainerie.'),
   ('Quel est le délai de livraison ?', 'Sur demande : il dépend du modèle, des options et de la charge du chantier au moment de la commande. Je vous le confirme par écrit avec le devis.')],
  end_h='On parle de votre Sea Water ?', end_p='Écrivez-moi et on regarde ça tranquillement. Sans engagement.', wa='Écrire sur WhatsApp', wa_txt='Bonjour Juan, je suis intéressé par un Sea Water.',
  small='Prix du tarif chantier 2026, hors TVA, sans moteurs, départ usine. Ils n’incluent pas les moteurs, le transport, la taxe d’immatriculation ni l’immatriculation. Ils peuvent changer et ne sont pas contractuels : le prix final est celui du devis écrit. Photos et données techniques du constructeur ; les photos peuvent montrer des options. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous.'),
}
for lg, P in LANGS.items():
    t = T[lg]
    src = open(os.path.join(ROOT, P.lstrip('/'), 'seawater', 'phantom-300', 'index.html')).read()
    url = f'{SITE}{P}/seawater/'
    head = src[:src.find('</head>') + 7]
    head = re.sub(r'<title>.*?</title>', f'<title>{E(t["title"])}</title>', head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{E(t["desc"])}">', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{E(t["title"])}">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{E(t["desc"])}">', head)
    head = head.replace('/seawater/phantom-300/', '/seawater/')
    head = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{SITE}/seawater/fotos/ghost-420/01.jpg">', head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    crumbs = [(t['home'], f'{SITE}{P}/'), (t['boats'], f'{SITE}{P}/barcos/'), (t['new'], f'{SITE}{P}/barcos-nuevos/'), ('Sea Water', url)]
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}
    il = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{SITE}{P}/seawater/{s}/'} for i, s in enumerate(ORDER)]}
    head = head.replace('</head>', f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n<script type="application/ld+json">{json.dumps(il, ensure_ascii=False)}</script>\n</head>')
    b0 = src.find('<body'); hdr = src[b0:src.find('</header>') + 9].replace('/seawater/phantom-300/', '/seawater/')
    foot = src[src.find('<footer'):]
    cards = ''
    for s in ORDER:
        m = TAR[s]; name = m['name']; full = name if name.startswith('Kymera') else 'Sea Water ' + name
        cards += (f'<a href="{P}/seawater/{s}/"><img src="/seawater/fotos/{s}/01-m.jpg" alt="{E(full)}" loading="lazy"><div><b>{E(name)}</b>'
                  f'<span>{t["kind"]["cab" if s in CAB else "open"]} · {m2(META[s]["loa"], lg)} · {t["from_"]} {eur(m["price"], lg)}<span class="vat">{t["vat"]}</span></span></div></a>')
    how = ''.join(f'<li><b>{a}</b>{b}</li>' for a, b in t['how'])
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in t['faq'])
    wa = 'https://wa.me/34633742973?text=' + urllib.parse.quote(t['wa_txt'])
    main = f'''
<main class="mm">
<section class="mm-hero" id="barco"><img src="/seawater/fotos/ghost-420/01.jpg" srcset="/seawater/fotos/ghost-420/01-m.jpg 640w, /seawater/fotos/ghost-420/01.jpg 1600w" sizes="100vw" alt="Sea Water Ghost 420" fetchpriority="high"><div class="wrap">
<img class="mm-blogo" src="/barcos-nuevos/logos/seawater-blanco.png" alt="Sea Water" width="900" height="231" data-nolb><p class="mm-kick">{t["kick"]}</p>
<h1>Sea Water</h1><p class="d">{E(t["lead"])}</p><div class="mm-ctas"><a class="mm-btn pri" href="#modelos">{t["cta"]}</a><a class="mm-btn gho" href="#presupuesto">{t["cta2"]}</a></div></div></section>
<section class="mm-sec" id="modelos"><div class="wrap"><p class="k">{t["g_k"]}</p><h2>{t["g_h"]}</h2><p class="s">{t["g_s"]}</p><div class="mm-others">{cards}</div></div></section>
<section class="mm-sec alt"><div class="wrap"><h2 style="margin-bottom:26px">{t["how_h"]}</h2><ol class="mm-how">{how}</ol></div></section>
<section class="mm-sec mm-faq" id="preguntas"><div class="wrap"><h2 style="margin-bottom:14px">{t["faq_h"]}</h2>{faq}</div></section>
<section class="mm-end" id="presupuesto"><img src="/seawater/fotos/phantom-300/02-m.jpg" srcset="/seawater/fotos/phantom-300/02-m.jpg 640w, /seawater/fotos/phantom-300/02.jpg 1600w" sizes="100vw" alt="" loading="lazy" data-nolb><div class="wrap"><h2>{t["end_h"]}</h2><p>{t["end_p"]}</p><div class="mm-ctas"><a class="mm-btn pri" href="{wa}" target="_blank" rel="noopener" data-wa-context="seawater">{t["wa"]}</a></div></div></section>
<div class="wrap"><p class="mm-small">{t["small"]}</p></div>
<script src="/seawater/seawater-form.js?v=20261106a" defer></script>
</main>
'''
    out = head + '\n' + hdr + main + foot
    dst = os.path.join(ROOT, P.lstrip('/'), 'seawater') if P else os.path.join(ROOT, 'seawater')
    open(os.path.join(dst, 'index.html'), 'w').write(out)
print('ok 4')
