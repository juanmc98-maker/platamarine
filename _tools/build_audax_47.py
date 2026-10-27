"""Genera la ficha del Audax 47 (velero cúter de construcción propia, registro 2011, botadura 2012) en ES/CA/EN/FR
a partir de la ficha del Monterey 278 SS como plantilla, y añade su tarjeta al catálogo /barcos/ de los 4 idiomas (idempotente).
Uso: python3 _tools/build_audax_47.py
Después: python3 _tools/ficha_v2.py audax-47, python3 _tools/coste_v2.py, PM_ROOT=<repo> python3 _tools/build_pdfs.py audax-47
y python3 _tools/build_search_index.py.
Datos: los que dio el propietario por WhatsApp (eslora total y de registro, motor y horas, bandera, zona, precio, IVA, sin cargas).
Lo que no consta va como "se confirma con la documentación". Sin nombre de la embarcación ni puerto exacto (solo "Castellón").
Fotos: las del propietario, con el nombre y la matrícula del casco difuminados."""
import re, os, html, json
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'audax-47'
TPL = 'monterey-278-ss'
TPL_NAME = 'Monterey 278 SS'
NAME = 'Audax 47'
N_PHOTOS = 11
W1 = 1600

D = {
 'es': dict(
  title='Velero Audax 47 en venta · 279.000 € · Plata Marine',
  desc='Velero cúter Audax 47 de 15,47 m (14,50 m de registro), construido por su propietario y botado en 2012. Volvo Penta D3 de 110 cv, bandera polaca. En Castellón, 279.000 €.',
  ogtitle='Velero Audax 47 en venta · 279.000 €',
  ldname='Audax 47 (2012)',
  lddesc='Velero cúter Audax 47 de construcción propia: registrado en 2011 y botado en 2012. Eslora total 15,47 m y 14,50 m de registro. Motor Volvo Penta D3 de 110 cv diésel con unas 1.300 horas según el propietario. Cubierta de doussié. Bandera polaca. En Castellón. Precio 279.000 € con el IVA pagado según el propietario.',
  sub=['Botadura 2012', '15,47 m de eslora', 'Volvo Penta D3 110 cv', 'Castellón'],
  price='279.000 €', vat='IVA pagado',
  pdf='audax-47.pdf', pdftxt='Descargar ficha completa (PDF)', pdfbtn='Descargar ficha PDF',
  wa='Hola Juan, me interesa el velero Audax 47 que tenéis en venta. ¿Podemos hablar?',
  wa_visit='Hola Juan, me gustaría ver en persona el velero Audax 47 de vuestra web. ¿Qué días se podría?',
  wa_share='Mira este barco: velero Audax 47 — https://www.platamarine.com/barcos/audax-47.html',
  alt='Velero Audax 47 amarrado en el pantalán al atardecer', photo='foto',
  specs=[('Tipo', 'Velero cúter de construcción propia'), ('Año', 'Registrado en 2011 · botado en 2012'),
         ('Eslora total', '15,47 m'), ('Eslora de registro', '14,50 m'),
         ('Motor', 'Volvo Penta D3 de 110 cv, diésel'), ('Horas', 'Unas 1.300 (según el propietario)'),
         ('Cubierta', 'Doussié'), ('Manga, calado, depósitos y plazas', 'Se confirma con la documentación'),
         ('Velas y electrónica', 'Se confirma con el propietario'),
         ('Titulación', 'PER con prácticas de vela o superior (eslora de registro 14,50 m)'),
         ('Bandera', 'Polaca'), ('Cargas', 'Ninguna, según el propietario; se comprueba antes de reservar'),
         ('Ubicación', 'Castellón'),
         ('Impuestos', 'IVA pagado, según el propietario; se confirma con la documentación antes de reservar. Si resides en España y lo vas a matricular o usar aquí, consulta el impuesto de matriculación con tu gestoría')],
  h2='Cómo lo veo',
  paras=[
   'Un Audax 47 que no es un barco de serie: lo diseñó y lo construyó su propietario, que es diseñador de veleros y navegante. Se registró en 2011 y se botó en 2012. Tiene 15,47 m de eslora total y 14,50 m de registro, aparejo de cúter y cubierta de doussié, con la caseta de portillos redondos que se ve en las fotos.',
   'Lleva un motor Volvo Penta D3 de 110 cv diésel con unas 1.300 horas, según el propietario. El historial de mantenimiento, el estado de las velas y la electrónica se piden al propietario y se revisan con la documentación antes de reservar.',
   'Tiene bandera polaca y está en Castellón. Con titulación española basta el PER con prácticas de vela o un título superior, porque la eslora de registro es de 14,50 m. El precio son 279.000 €, con el IVA pagado según el propietario.',
   'Las fotos son del propietario. Del interior todavía no tengo fotos: si te interesa el barco, pídemelas y te paso lo que haya.',
  ],
  equip_h='Equipamiento',
  equip=['Aparejo de cúter', 'Volvo Penta D3 110 cv', 'Cubierta de doussié', 'Caseta con portillos redondos', 'Escotillas en cubierta', 'Bandera polaca'],
  card=dict(alt='Velero Audax 47 amarrado en el pantalán al atardecer', sub='2012 · 15,47 m · cúter · Volvo Penta D3 110 cv · Castellón',
            tb='Titulación: PER con prácticas de vela o superior',
            desc='Velero cúter de construcción propia, botado en 2012: 15,47 m, cubierta de doussié y Volvo Penta D3 de 110 cv con unas 1.300 horas. Bandera polaca. Se puede ver con cita previa.',
            ask='Preguntar por WhatsApp', see='Ver ficha'),
 ),
 'ca': dict(
  title='Veler Audax 47 en venda · 279.000 € · Plata Marine',
  desc="Veler cúter Audax 47 de 15,47 m (14,50 m de registre), construït pel seu propietari i avarat el 2012. Volvo Penta D3 de 110 cv, bandera polonesa. A Castelló, 279.000 €.",
  ogtitle='Veler Audax 47 en venda · 279.000 €',
  ldname='Audax 47 (2012)',
  lddesc="Veler cúter Audax 47 de construcció pròpia: registrat el 2011 i avarat el 2012. Eslora total 15,47 m i 14,50 m de registre. Motor Volvo Penta D3 de 110 cv dièsel amb unes 1.300 hores segons el propietari. Coberta de doussié. Bandera polonesa. A Castelló. Preu 279.000 € amb l'IVA pagat segons el propietari.",
  sub=['Avarada 2012', "15,47 m d'eslora", 'Volvo Penta D3 110 cv', 'Castelló'],
  price='279.000 €', vat='IVA pagat',
  pdf='/barcos/audax-47-ca.pdf', pdftxt='Descarregar la fitxa completa (PDF)', pdfbtn='Descarregar fitxa PDF (en català)',
  wa="Hola Juan, m'interessa el veler Audax 47 que teniu en venda. Podem parlar?",
  wa_visit="Hola Juan, m'agradaria veure en persona el veler Audax 47 de la vostra web. Quins dies es podria?",
  wa_share='Mira aquest vaixell: veler Audax 47 — https://www.platamarine.com/ca/barcos/audax-47.html',
  alt='Veler Audax 47 amarrat al pantalà a la posta de sol', photo='foto',
  specs=[('Tipus', 'Veler cúter de construcció pròpia'), ('Any', 'Registrat el 2011 · avarat el 2012'),
         ('Eslora total', '15,47 m'), ('Eslora de registre', '14,50 m'),
         ('Motor', 'Volvo Penta D3 de 110 cv, dièsel'), ('Hores', 'Unes 1.300 (segons el propietari)'),
         ('Coberta', 'Doussié'), ('Mànega, calat, dipòsits i places', 'Es confirma amb la documentació'),
         ('Veles i electrònica', 'Es confirma amb el propietari'),
         ('Titulació', 'PER amb pràctiques de vela o superior (eslora de registre 14,50 m)'),
         ('Bandera', 'Polonesa'), ('Càrregues', 'Cap, segons el propietari; es comprova abans de reservar'),
         ('Ubicació', 'Castelló'),
         ('Impostos', "IVA pagat, segons el propietari; es confirma amb la documentació abans de reservar. Si resideixes a Espanya i el matricularàs o el faràs servir aquí, consulta l'impost de matriculació amb la teva gestoria")],
  h2='Com el veig',
  paras=[
   "Un Audax 47 que no és un vaixell de sèrie: el va dissenyar i construir el seu propietari, que és dissenyador de velers i navegant. Es va registrar el 2011 i es va avarar el 2012. Té 15,47 m d'eslora total i 14,50 m de registre, aparell de cúter i coberta de doussié, amb la caseta de portells rodons que es veu a les fotos.",
   "Porta un motor Volvo Penta D3 de 110 cv dièsel amb unes 1.300 hores, segons el propietari. L'historial de manteniment, l'estat de les veles i l'electrònica es demanen al propietari i es revisen amb la documentació abans de reservar.",
   "Té bandera polonesa i és a Castelló. Amb titulació espanyola n'hi ha prou amb el PER amb pràctiques de vela o un títol superior, perquè l'eslora de registre és de 14,50 m. El preu són 279.000 €, amb l'IVA pagat segons el propietari.",
   "Les fotos són del propietari. De l'interior encara no tinc fotos: si t'interessa el vaixell, demana-me-les i et passo el que hi hagi.",
  ],
  equip_h='Equipament',
  equip=['Aparell de cúter', 'Volvo Penta D3 110 cv', 'Coberta de doussié', 'Caseta amb portells rodons', 'Escotilles a coberta', 'Bandera polonesa'],
  card=dict(alt='Veler Audax 47 amarrat al pantalà a la posta de sol', sub='2012 · 15,47 m · cúter · Volvo Penta D3 110 cv · Castelló',
            tb='Titulació: PER amb pràctiques de vela o superior',
            desc="Veler cúter de construcció pròpia, avarat el 2012: 15,47 m, coberta de doussié i Volvo Penta D3 de 110 cv amb unes 1.300 hores. Bandera polonesa. Es pot veure amb cita prèvia.",
            ask='Preguntar per WhatsApp', see='Veure fitxa'),
 ),
 'en': dict(
  title='Audax 47 sailing yacht for sale · €279,000 · Plata Marine',
  desc='Audax 47 cutter, 15.47 m (14.50 m registered length), built by her owner and launched in 2012. Volvo Penta D3 110 hp, Polish flag. In Castellón, €279,000.',
  ogtitle='Audax 47 sailing yacht for sale · €279,000',
  ldname='Audax 47 (2012)',
  lddesc='Owner-built Audax 47 cutter: registered in 2011 and launched in 2012. Length overall 15.47 m, registered length 14.50 m. Volvo Penta D3 110 hp diesel with about 1,300 hours according to the owner. Doussie deck. Polish flag. In Castellón. Price €279,000 with VAT paid according to the owner.',
  sub=['Launched 2012', '15.47 m length', 'Volvo Penta D3 110 hp', 'Castellón'],
  price='€279,000', vat='VAT paid',
  pdf='/barcos/audax-47-en.pdf', pdftxt='Download full spec sheet (PDF)', pdfbtn='Download PDF listing (in English)',
  wa="Hi Juan, I'm interested in the Audax 47 sailing yacht you have for sale. Can we talk?",
  wa_visit="Hi Juan, I'd like to see the Audax 47 sailing yacht from your website in person. Which days would work?",
  wa_share='Check out this boat: Audax 47 sailing yacht — https://www.platamarine.com/en/barcos/audax-47.html',
  alt='Audax 47 sailing yacht moored on the pontoon at sunset', photo='photo',
  specs=[('Type', 'Owner-built cutter-rigged sailing yacht'), ('Year', 'Registered in 2011 · launched in 2012'),
         ('Length overall', '15.47 m'), ('Registered length', '14.50 m'),
         ('Engine', 'Volvo Penta D3 110 hp, diesel'), ('Hours', 'About 1,300 (according to the owner)'),
         ('Deck', 'Doussie'), ('Beam, draft, tanks and berths', 'To be confirmed from the documentation'),
         ('Sails and electronics', 'To be confirmed with the owner'),
         ('Licence', 'Spanish PER with sailing endorsement, or higher (registered length 14.50 m)'),
         ('Flag', 'Polish'), ('Charges', 'None, according to the owner; checked before you reserve'),
         ('Location', 'Castellón'),
         ('Taxes', 'VAT paid, according to the owner; confirmed from the documentation before you reserve. If you live in Spain and will register or use it here, check the registration tax with your agent (gestoría)')],
  h2='My take',
  paras=[
   "This Audax 47 is not a production boat: she was designed and built by her owner, a yacht designer and sailor. She was registered in 2011 and launched in 2012. She is 15.47 m overall with a registered length of 14.50 m, cutter-rigged, with a doussie deck and the deckhouse with round portholes you can see in the photos.",
   "She has a Volvo Penta D3 110 hp diesel with about 1,300 hours, according to the owner. The maintenance history and the condition of the sails and electronics are requested from the owner and checked against the documentation before you reserve.",
   "She is under the Polish flag and is in Castellón. With a Spanish licence, the PER with sailing endorsement or a higher licence is enough, as the registered length is 14.50 m. The price is €279,000, with VAT paid according to the owner.",
   "The photos are the owner's. I don't have interior photos yet: if you're interested, ask me and I'll send you whatever there is.",
  ],
  equip_h='Equipment',
  equip=['Cutter rig', 'Volvo Penta D3 110 hp', 'Doussie deck', 'Deckhouse with round portholes', 'Deck hatches', 'Polish flag'],
  card=dict(alt='Audax 47 sailing yacht moored on the pontoon at sunset', sub='2012 · 15.47 m · cutter · Volvo Penta D3 110 hp · Castellón',
            tb='Licence: PER with sailing endorsement or higher',
            desc='Owner-built cutter launched in 2012: 15.47 m, doussie deck and Volvo Penta D3 110 hp with about 1,300 hours. Polish flag. Viewing by appointment.',
            ask='Ask on WhatsApp', see='See listing'),
 ),
 'fr': dict(
  title='Voilier Audax 47 à vendre · 279 000 € · Plata Marine',
  desc="Voilier cotre Audax 47 de 15,47 m (14,50 m d'immatriculation), construit par son propriétaire et mis à l'eau en 2012. Volvo Penta D3 de 110 ch, pavillon polonais. À Castellón, 279 000 €.",
  ogtitle='Voilier Audax 47 à vendre · 279 000 €',
  ldname='Audax 47 (2012)',
  lddesc="Voilier cotre Audax 47 construit par son propriétaire : immatriculé en 2011 et mis à l'eau en 2012. Longueur hors tout 15,47 m, longueur d'immatriculation 14,50 m. Moteur Volvo Penta D3 de 110 ch diesel, environ 1 300 heures selon le propriétaire. Pont en doussié. Pavillon polonais. À Castellón. Prix 279 000 €, TVA payée selon le propriétaire.",
  sub=["Mise à l'eau 2012", '15,47 m de longueur', 'Volvo Penta D3 110 ch', 'Castellón'],
  price='279 000 €', vat='TVA payée',
  pdf='/barcos/audax-47-fr.pdf', pdftxt='Télécharger la fiche complète (PDF)', pdfbtn='Télécharger la fiche PDF (en français)',
  wa="Bonjour Juan, le voilier Audax 47 que vous avez à vendre m'intéresse. Pouvons-nous en parler ?",
  wa_visit="Bonjour Juan, j'aimerais voir sur place le voilier Audax 47 de votre site. Quels jours seraient possibles ?",
  wa_share='Regardez ce bateau : voilier Audax 47 — https://www.platamarine.com/fr/barcos/audax-47.html',
  alt='Voilier Audax 47 amarré au ponton au coucher du soleil', photo='photo',
  specs=[('Type', 'Voilier gréé en cotre, construit par son propriétaire'), ('Année', "Immatriculé en 2011 · mis à l'eau en 2012"),
         ('Longueur hors tout', '15,47 m'), ("Longueur d'immatriculation", '14,50 m'),
         ('Moteur', 'Volvo Penta D3 de 110 ch, diesel'), ('Heures', 'Environ 1 300 (selon le propriétaire)'),
         ('Pont', 'Doussié'), ('Largeur, tirant d’eau, réservoirs et places', 'À confirmer avec les documents'),
         ('Voiles et électronique', 'À confirmer avec le propriétaire'),
         ('Permis', "PER espagnol avec l'habilitation voile, ou supérieur (longueur d'immatriculation 14,50 m)"),
         ('Pavillon', 'Polonais'), ('Charges', 'Aucune, selon le propriétaire ; vérifié avant la réservation'),
         ('Emplacement', 'Castellón'),
         ('Taxes', "TVA payée, selon le propriétaire ; confirmé avec les documents avant la réservation. Si vous résidez en Espagne et allez l'immatriculer ou l'utiliser ici, renseignez-vous sur la taxe d'immatriculation auprès de votre gestoría")],
  h2='Mon avis',
  paras=[
   "Cet Audax 47 n'est pas un bateau de série : il a été dessiné et construit par son propriétaire, architecte de voiliers et navigateur. Immatriculé en 2011, il a été mis à l'eau en 2012. Il mesure 15,47 m hors tout pour 14,50 m d'immatriculation, gréé en cotre, avec un pont en doussié et le rouf à hublots ronds que l'on voit sur les photos.",
   "Il est équipé d'un Volvo Penta D3 de 110 ch diesel avec environ 1 300 heures, selon le propriétaire. L'historique d'entretien, l'état des voiles et l'électronique sont demandés au propriétaire et vérifiés avec les documents avant la réservation.",
   "Il est sous pavillon polonais et se trouve à Castellón. Avec un permis espagnol, le PER avec l'habilitation voile ou un permis supérieur suffit, car la longueur d'immatriculation est de 14,50 m. Le prix est de 279 000 €, TVA payée selon le propriétaire.",
   "Les photos sont celles du propriétaire. Je n'ai pas encore de photos de l'intérieur : si le bateau vous intéresse, demandez-les-moi et je vous enverrai ce qu'il y a.",
  ],
  equip_h='Équipement',
  equip=['Gréement de cotre', 'Volvo Penta D3 110 ch', 'Pont en doussié', 'Rouf à hublots ronds', 'Panneaux de pont', 'Pavillon polonais'],
  card=dict(alt='Voilier Audax 47 amarré au ponton au coucher du soleil', sub='2012 · 15,47 m · cotre · Volvo Penta D3 110 ch · Castellón',
            tb="Permis : PER avec l'habilitation voile ou supérieur",
            desc="Cotre construit par son propriétaire, mis à l'eau en 2012 : 15,47 m, pont en doussié et Volvo Penta D3 de 110 ch, environ 1 300 heures. Pavillon polonais. Visite sur rendez-vous.",
            ask='Demander sur WhatsApp', see='Voir la fiche'),
 ),
}

FORBIDDEN = r'Monterey|monterey|278 SS|GXi|Gelabert|49\.?990|49,990|49 990|lista 7|llista 7|liste 7'


def wa(txt):
    return 'https://wa.me/34633742973?text=' + quote(txt, safe='')


def json_s(s):
    return json.dumps(s, ensure_ascii=False)


def build(lang):
    pre = '' if lang == 'es' else lang + '/'
    t = open(os.path.join(ROOT, pre, 'barcos', TPL + '.html'), encoding='utf-8').read()
    d = D[lang]
    e = html.escape
    t = re.sub(r'<title>.*?</title>', '<title>' + e(d['title']) + '</title>', t, count=1)
    t = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="' + e(d['desc'], quote=True) + '">', t, count=1)
    t = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="' + e(d['ogtitle'], quote=True) + '">', t, count=1)
    t = re.sub(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="' + e(d['desc'], quote=True) + '">', t, count=1)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Monterey[^"]*(?:hablar|parlar|talk|parler)[^"]*', lambda m: wa(d['wa']), t)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Monterey[^"]*', lambda m: wa(d['wa_visit']), t)
    t = re.sub(r'https://wa\.me/\?text=[^"]*', lambda m: 'https://wa.me/?text=' + quote(d['wa_share'], safe=''), t)
    t = t.replace(TPL, SLUG)
    imgs = ',\n'.join('    "https://www.platamarine.com/%s-%d.jpg"' % (SLUG, i) for i in range(1, N_PHOTOS + 1))
    t = re.sub(r'"image": \[.*?\]', lambda m: '"image": [\n' + imgs + '\n  ]', t, count=1, flags=re.S)
    t = re.sub(r'"name": "Monterey 278 SS \(2011\)"', lambda m: '"name": ' + json_s(d['ldname']), t, count=1)
    t = re.sub(r'"description": ".*?",(\s*)"offers"', lambda m: '"description": ' + json_s(d['lddesc']) + ',' + m.group(1) + '"offers"', t, count=1, flags=re.S)
    t = t.replace('"price": "49990"', '"price": "279000"')
    t = re.sub(r'"brand": \{\s*"@type": "Brand",\s*"name": "Monterey"\s*\},\s*"model": "278 SS"', '"brand": {\n    "@type": "Brand",\n    "name": "Audax"\n  },\n  "model": "47"', t, count=1)
    t = re.sub(r'<div class="sub">.*?</div>', lambda m: '<div class="sub">' + ''.join('<span>%s</span>' % e(s) for s in d['sub']) + '</div>', t, count=1, flags=re.S)
    t = re.sub(r'<p class="price">[^<]*</p>', lambda m: '<p class="price">%s <span class="vat paid">%s</span></p>' % (d['price'], e(d['vat'])), t, count=1)
    t = re.sub(r'<a class="pdf-link" href="[^"]*" download>[^<]*</a>', lambda m: '<a class="pdf-link" href="%s" download>%s</a>' % (d['pdf'], e(d['pdftxt'])), t, count=1)
    t = re.sub(r'<a class="btn btn-ghost" href="[^"]*\.pdf" download>[^<]*</a>', lambda m: '<a class="btn btn-ghost" href="%s" download>%s</a>' % (d['pdf'], e(d['pdfbtn'])), t, count=1)
    t = re.sub(r'<img class="main" id="main" [^>]*>', lambda m: '<img class="main" id="main" src="/%s-1.jpg" srcset="/%s-1-m.jpg 1000w, /%s-1.jpg %dw" sizes="(max-width: 1100px) 100vw, 1100px" alt="%s">' % (SLUG, SLUG, SLUG, W1, e(d['alt'], quote=True)), t, count=1)
    thumbs = ''.join('<img src="/%s-%d-t.jpg" data-full="/%s-%d.jpg" alt="%s – %s %d" loading="lazy" data-i="%d"%s>' % (SLUG, i, SLUG, i, NAME, d['photo'], i, i - 1, ' class="on"' if i == 1 else '') for i in range(1, N_PHOTOS + 1))
    t = re.sub(r'<div class="thumbs">.*?</div>', lambda m: '<div class="thumbs">' + thumbs + '</div>', t, count=1, flags=re.S)
    dl = '<dl class="specs">' + ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in d['specs']) + '</dl>'
    t = re.sub(r'<dl class="specs">.*?</dl>', lambda m: dl, t, count=1, flags=re.S)
    prose = '<div class="prose">\n<h2>%s</h2>\n%s\n<h3 class="equip-h">%s</h3><ul class="equip-tags">%s</ul>\n</div>' % (
        e(d['h2']), '\n'.join('<p>%s</p>' % e(p) for p in d['paras']), e(d['equip_h']), ''.join('<li>%s</li>' % e(x) for x in d['equip']))
    t = re.sub(r'<div class="prose">.*?</div>\n(\s*)</div>', lambda m: prose + '\n' + m.group(1) + '</div>', t, count=1, flags=re.S)
    t = t.replace(TPL_NAME, NAME)
    assert '<!--pm-sim-->' in t and '"slug":"%s"' % SLUG in t
    left = re.findall(r'.{30}(?:%s).{30}' % FORBIDDEN, t)
    assert not left, left[:5]
    out = os.path.join(ROOT, pre, 'barcos', SLUG + '.html')
    open(out, 'w', encoding='utf-8').write(t)
    print('ok', out, len(t))


def card(lang):
    d = D[lang]; c = d['card']; e = html.escape
    return ('      <article data-pm-boat="{s}" class="bcard" data-sold="0" data-tipo="vela" data-titulo="3" data-precio="279000" data-zona="valencia" data-comb="diesel" data-motor="intra" data-anyo="2012" data-i="0.5">\n'
            '        <a class="bimg" href="{s}.html"><img src="/{s}-1-m.jpg" srcset="/{s}-1-m.jpg 1000w, /{s}-1.jpg {w}w" sizes="(max-width: 820px) 100vw, 560px" alt="{alt}" loading="lazy" width="{w}" height="1200"><span class="status available">{st}</span></a>\n'
            '        <div class="bbody">\n'
            '          <div class="head" style="margin:0 0 6px"><h2><a href="{s}.html">{n}</a></h2><p class="price">{p} <span class="vat paid">{v}</span></p></div>\n'
            '          <p class="sub" style="margin:0">{sub}</p>\n'
            '          <span class="tbadge">{tb}</span>\n'
            '          <p class="bdesc">{desc}</p>\n'
            '          <div class="bcta"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{ask}</a><a class="btn btn-ghost" href="{s}.html">{see}</a></div>\n'
            '        </div>\n'
            '      </article>\n').format(s=SLUG, w=W1, alt=e(c['alt'], quote=True), st={'en': 'Available', 'fr': 'Disponible'}.get(lang, 'Disponible'), n=NAME,
                                       p=d['price'], v=e(d['vat']), sub=e(c['sub']), tb=e(c['tb']), desc=e(c['desc']), wa=wa(d['wa']), ask=c['ask'], see=c['see'])


def add_catalog(lang):
    pre = '' if lang == 'es' else lang + '/'
    p = os.path.join(ROOT, pre, 'barcos', 'index.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'      <article data-pm-boat="%s".*?</article>\n' % SLUG, '', s, flags=re.S)
    anchor = '      <article data-pm-boat="prestige-32"'
    assert s.count(anchor) == 1
    s = s.replace(anchor, card(lang) + anchor, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('catálogo', p)


if __name__ == '__main__':
    for lang in ('es', 'ca', 'en', 'fr'):
        build(lang)
        add_catalog(lang)
