"""Genera la ficha del Cattleya X6 (ES/CA/EN) a partir de la ficha de la Starfisher 840 como plantilla.
Uso: python3 _tools/build_cattleya_x6.py   (desde cualquier sitio)
Los datos pendientes del propietario van como "se confirma con la documentación"; al llegar, editar D y regenerar."""
import re, os, html
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'cattleya-x6'
TPL = 'starfisher-840'
N_PHOTOS = 8

D = {
 'es': dict(
  title='Cattleya X6 2021 en venta · 55.000 € + IVA · Plata Marine',
  desc='Cattleya X6 de 2021 con motor Tohatsu 150 cv nuevo de 2026 (aprox. 145 h), equipada para chárter en Ibiza: hard-top inox, solárium, música Fusion, luces LED, molinete eléctrico. 55.000 € + IVA. Ficha completa.',
  ogtitle='Cattleya X6 2021 en venta · 55.000 € + IVA',
  ldname='Cattleya X6 (2021)',
  lddesc='Cattleya X6 de 2021, lancha open con motor fueraborda Tohatsu 150 cv nuevo de junio de 2026 (aprox. 145 h), hard-top inox a medida, solárium y tapicería nuevas 2026, mesa de madera, música Bluetooth con altavoces Fusion, luces LED, molinete eléctrico. Explotada en chárter en Ibiza, con posibilidad de subrogarse en el amarre y el negocio. Precio 55.000 € + IVA.',
  crumb='Cattleya X6',
  sub=['Año 2021', 'Motor Tohatsu 150 cv, nuevo 2026', 'Gasolina, fueraborda', 'Ibiza'],
  price='55.000 €', vat='+IVA',
  pdf='cattleya-x6.pdf', pdftxt='Descargar ficha completa (PDF)', pdfbtn='Descargar ficha PDF',
  wa='Hola Juan, me interesa la Cattleya X6 de 2021 que tenéis en venta. ¿Podemos hablar?',
  wa_visit='Hola Juan, me gustaría ver en persona la Cattleya X6 (2021) de vuestra web. ¿Qué días se podría?',
  wa_share='Mira este barco: Cattleya X6 — https://www.platamarine.com/barcos/cattleya-x6.html',
  alt='Cattleya X6 fondeada junto a un acantilado en Ibiza',
  specs=[('Año', '2021'), ('Tipo', 'Lancha open con hard-top'), ('Eslora', '5,98 m'), ('Manga', '2,45 m'), ('Categoría de diseño', 'C'),
         ('Capacidad', '8 personas'), ('Motor', 'Tohatsu 150 cv, gasolina fueraborda · nuevo de junio de 2026'),
         ('Horas', 'Aprox. 145 (motor)'), ('Mantenimiento', 'Motor nuevo 2026 · molinete eléctrico nuevo 2026 · tapicería y colchonetas nuevas 2026'),
         ('Electrónica', 'Sonda/GPS multifunción · equipo de música Bluetooth con 4 altavoces Fusion'),
         ('Cubierta', 'Hard-top inox fijo a medida · solárium de proa · mesa desmontable de madera · ducha de agua dulce · trampolín lateral · luces LED ambientales y subacuáticas · 2 baterías'),
         ('Uso', 'Explotada en chárter en Ibiza; posibilidad de continuar con el amarre y el negocio (condiciones a tratar con el propietario)'),
         ('Amarre', 'De alquiler en Ibiza; según el propietario, con posibilidad de subrogación'),
         ('Titulación', 'Licencia de Navegación o superior'), ('Bandera', 'Española'),
         ('ITB', 'Se entrega recién pasada (el propietario la está tramitando ahora)'), ('Garantía', 'Motor con garantía de fábrica hasta mayo de 2028, transferible al comprador'),
         ('Impuestos', 'Precio sin IVA (vende una sociedad); el desglose se confirma con la documentación antes de reservar')],
  h2='Cómo lo veo',
  paras=[
   'Una Cattleya X6 de 2021 que ha trabajado en chárter en Ibiza y se nota en cómo está preparada: hard-top de acero inoxidable hecho a medida, solárium de proa con colchonetas y tapicería nuevas de 2026, mesa desmontable de madera y ducha de agua dulce. Es una lancha de día, sencilla y con espacio, pensada para salir a las calas.',
   'El motor es un Tohatsu de 150 CV fueraborda montado nuevo en junio de 2026 y con unas 145 horas, así que la parte mecánica está casi a estrenar. El molinete eléctrico también es de 2026. Lleva sonda/GPS multifunción, equipo de música Bluetooth con cuatro altavoces Fusion, luces LED ambientales y subacuáticas y dos baterías.',
   'A quien la veo encajar es a alguien que quiera seguir con la actividad de chárter: el propietario habla de unas 80 salidas por temporada, y existe la posibilidad de subrogarse en el amarre de alquiler en Ibiza y en el negocio tal como está montado. Esas condiciones se explican a quien esté interesado; el precio del anuncio es por el barco. También sirve, claro, para uso particular.',
   'Mide 5,98 m de eslora por 2,45 m de manga, está despachada para 8 personas y se puede gobernar con la Licencia de Navegación o un título superior. El motor conserva la garantía de fábrica hasta mayo de 2028 y se puede pasar al comprador, y el barco se entrega con la ITB recién pasada. Está en Ibiza y se puede ver con cita previa. El precio son 55.000 € más IVA.',
  ],
  equip_h='Equipamiento',
  equip=['Tohatsu 150 cv fueraborda, nuevo junio 2026', 'Hard-top inox fijo a medida', 'Solárium de proa', 'Colchonetas y tapicería nuevas 2026', 'Mesa desmontable de madera natural', 'Ducha de agua dulce', 'Sonda/GPS multifunción', 'Música Bluetooth con 4 altavoces Fusion', 'Luces LED ambientales', 'Luces LED subacuáticas', 'Molinete eléctrico nuevo 2026', 'Trampolín lateral a medida', '2 baterías', 'Escalera de baño'],
 ),
 'ca': dict(
  title='Cattleya X6 2021 en venda · 55.000 € + IVA · Plata Marine',
  desc='Cattleya X6 del 2021 amb motor Tohatsu 150 cv nou del 2026 (aprox. 145 h), equipada per a xàrter a Eivissa: hard-top inox, solàrium, música Fusion, llums LED, molinet elèctric. 55.000 € + IVA. Fitxa completa.',
  ogtitle='Cattleya X6 2021 en venda · 55.000 € + IVA',
  ldname='Cattleya X6 (2021)',
  lddesc='Cattleya X6 del 2021, llanxa open amb motor forabord Tohatsu 150 cv nou del juny del 2026 (aprox. 145 h), hard-top inox a mida, solàrium i tapisseria noves 2026, taula de fusta, música Bluetooth amb altaveus Fusion, llums LED, molinet elèctric. Explotada en xàrter a Eivissa, amb possibilitat de subrogar-se en l\'amarratge i el negoci. Preu 55.000 € + IVA.',
  crumb='Cattleya X6',
  sub=['Any 2021', 'Motor Tohatsu 150 cv, nou 2026', 'Gasolina, forabord', 'Eivissa'],
  price='55.000 €', vat='+IVA',
  pdf='/barcos/cattleya-x6-ca.pdf', pdftxt='Descarregar la fitxa completa (PDF)', pdfbtn='Descarregar fitxa PDF (en català)',
  wa="Hola Juan, m'interessa la Cattleya X6 del 2021 que teniu en venda. Podem parlar?",
  wa_visit="Hola Juan, m'agradaria veure en persona la Cattleya X6 (2021) de la vostra web. Quins dies es podria?",
  wa_share='Mira aquest vaixell: Cattleya X6 — https://www.platamarine.com/ca/barcos/cattleya-x6.html',
  alt='Cattleya X6 fondejada al costat d\'un penya-segat a Eivissa',
  specs=[('Any', '2021'), ('Tipus', 'Llanxa open amb hard-top'), ('Eslora', '5,98 m'), ('Mànega', '2,45 m'), ('Categoria de disseny', 'C'),
         ('Capacitat', '8 persones'), ('Motor', 'Tohatsu 150 cv, gasolina forabord · nou del juny del 2026'),
         ('Hores', 'Aprox. 145 (motor)'), ('Manteniment', 'Motor nou 2026 · molinet elèctric nou 2026 · tapisseria i matalassets nous 2026'),
         ('Electrònica', 'Sonda/GPS multifunció · equip de música Bluetooth amb 4 altaveus Fusion'),
         ('Coberta', 'Hard-top inox fix a mida · solàrium de proa · taula desmuntable de fusta · dutxa d\'aigua dolça · trampolí lateral · llums LED ambientals i subaquàtics · 2 bateries'),
         ('Ús', 'Explotada en xàrter a Eivissa; possibilitat de continuar amb l\'amarratge i el negoci (condicions a tractar amb el propietari)'),
         ('Amarratge', 'De lloguer a Eivissa; segons el propietari, amb possibilitat de subrogació'),
         ('Titulació', 'Llicència de Navegació o superior'), ('Bandera', 'Espanyola'),
         ('ITB', "Es lliura acabada de passar (el propietari l'està tramitant ara)"), ('Garantia', 'Motor amb garantia de fàbrica fins al maig del 2028, transferible al comprador'),
         ('Impostos', 'Preu sense IVA (ven una societat); el desglossament es confirma amb la documentació abans de reservar')],
  h2='Com el veig',
  paras=[
   'Una Cattleya X6 del 2021 que ha treballat en xàrter a Eivissa i es nota en com està preparada: hard-top d\'acer inoxidable fet a mida, solàrium de proa amb matalassets i tapisseria nous del 2026, taula desmuntable de fusta i dutxa d\'aigua dolça. És una llanxa de dia, senzilla i amb espai, pensada per anar a les cales.',
   'El motor és un Tohatsu de 150 CV forabord muntat nou el juny del 2026 i amb unes 145 hores, de manera que la part mecànica està gairebé per estrenar. El molinet elèctric també és del 2026. Porta sonda/GPS multifunció, equip de música Bluetooth amb quatre altaveus Fusion, llums LED ambientals i subaquàtics i dues bateries.',
   'A qui la veig encaixar és a algú que vulgui continuar amb l\'activitat de xàrter: el propietari parla d\'unes 80 sortides per temporada, i hi ha la possibilitat de subrogar-se en l\'amarratge de lloguer a Eivissa i en el negoci tal com està muntat. Aquestes condicions s\'expliquen a qui hi estigui interessat; el preu de l\'anunci és pel vaixell. També serveix, és clar, per a ús particular.',
   'Fa 5,98 m d\'eslora per 2,45 m de mànega, està despatxada per a 8 persones i es pot governar amb la Llicència de Navegació o un títol superior. El motor conserva la garantia de fàbrica fins al maig del 2028 i es pot passar al comprador, i el vaixell es lliura amb la ITB acabada de passar. És a Eivissa i es pot veure amb cita prèvia. El preu són 55.000 € més IVA.',
  ],
  equip_h='Equipament',
  equip=['Tohatsu 150 cv forabord, nou juny 2026', 'Hard-top inox fix a mida', 'Solàrium de proa', 'Matalassets i tapisseria nous 2026', 'Taula desmuntable de fusta natural', 'Dutxa d\'aigua dolça', 'Sonda/GPS multifunció', 'Música Bluetooth amb 4 altaveus Fusion', 'Llums LED ambientals', 'Llums LED subaquàtics', 'Molinet elèctric nou 2026', 'Trampolí lateral a mida', '2 bateries', 'Escala de bany'],
 ),
 'en': dict(
  title='2021 Cattleya X6 for sale · €55,000 + VAT · Plata Marine',
  desc='2021 Cattleya X6 with a new 2026 Tohatsu 150 hp outboard (approx. 145 h), set up for charter in Ibiza: stainless hard-top, sunbed, Fusion audio, LED lights, electric windlass. €55,000 + VAT. Full listing.',
  ogtitle='2021 Cattleya X6 for sale · €55,000 + VAT',
  ldname='Cattleya X6 (2021)',
  lddesc='2021 Cattleya X6 open day boat with a Tohatsu 150 hp outboard fitted new in June 2026 (approx. 145 h), custom stainless hard-top, new 2026 sunbed cushions and upholstery, wooden table, Bluetooth audio with Fusion speakers, LED lights, electric windlass. Run as a charter boat in Ibiza, with the option of taking over the berth and the business. Price €55,000 + VAT.',
  crumb='Cattleya X6',
  sub=['Year 2021', 'Tohatsu 150 hp, new 2026', 'Petrol, outboard', 'Ibiza'],
  price='€55,000', vat='+VAT',
  pdf='/barcos/cattleya-x6-en.pdf', pdftxt='Download full spec sheet (PDF)', pdfbtn='Download PDF listing (in English)',
  wa="Hi Juan, I'm interested in the 2021 Cattleya X6 you have for sale. Can we talk?",
  wa_visit="Hi Juan, I'd like to see the Cattleya X6 (2021) from your website in person. Which days would work?",
  wa_share='Check out this boat: Cattleya X6 — https://www.platamarine.com/en/barcos/cattleya-x6.html',
  alt='Cattleya X6 at anchor beside a cliff in Ibiza',
  specs=[('Year', '2021'), ('Type', 'Open day boat with hard-top'), ('Length', '5.98 m'), ('Beam', '2.45 m'), ('Design category', 'C'),
         ('Capacity', '8 people'), ('Engine', 'Tohatsu 150 hp petrol outboard · fitted new in June 2026'),
         ('Hours', 'Approx. 145 (engine)'), ('Maintenance', 'New engine 2026 · new electric windlass 2026 · new upholstery and cushions 2026'),
         ('Electronics', 'Multifunction sounder/GPS · Bluetooth audio with 4 Fusion speakers'),
         ('Deck', 'Custom fixed stainless hard-top · bow sunbed · removable wooden table · fresh-water shower · side trampoline · ambient and underwater LED lights · 2 batteries'),
         ('Use', 'Run as a charter boat in Ibiza; option to continue with the berth and the business (terms to be agreed with the owner)'),
         ('Berth', 'Rented berth in Ibiza; according to the owner it can be taken over'),
         ('Licence', 'Navigation Licence or higher'), ('Flag', 'Spanish'),
         ('ITB', 'Delivered with a freshly passed ITB (the owner is arranging it now)'), ('Warranty', 'Engine under factory warranty until May 2028, transferable to the buyer'),
         ('Taxes', 'Price excludes VAT (sold by a company); the breakdown is confirmed from the documentation before you reserve')],
  h2='My take',
  paras=[
   'A 2021 Cattleya X6 that has been working as a charter boat in Ibiza, and you can tell from how it is set up: a custom stainless-steel hard-top, a bow sunbed with cushions and upholstery new in 2026, a removable wooden table and a fresh-water shower. It is a simple, roomy day boat made for going out to the coves.',
   'The engine is a Tohatsu 150 hp outboard fitted new in June 2026 with around 145 hours, so the mechanical side is close to brand new. The electric windlass is also from 2026. It carries a multifunction sounder/GPS, Bluetooth audio with four Fusion speakers, ambient and underwater LED lights and two batteries.',
   'Who I see it suiting is someone who wants to carry on with the charter activity: the owner talks about around 80 outings a season, and there is the option of taking over the rented berth in Ibiza and the business as it is set up. Those terms are explained to anyone interested; the advertised price is for the boat. It also works, of course, for private use.',
   'It measures 5.98 m in length with a 2.45 m beam, is certified for 8 people and can be skippered with the Navigation Licence or a higher qualification. The engine is still under factory warranty until May 2028, which can be passed on to the buyer, and the boat is delivered with a freshly passed ITB. It is in Ibiza and can be viewed by appointment. The price is €55,000 plus VAT.',
  ],
  equip_h='Equipment',
  equip=['Tohatsu 150 hp outboard, new June 2026', 'Custom fixed stainless hard-top', 'Bow sunbed', 'New 2026 cushions and upholstery', 'Removable natural-wood table', 'Fresh-water shower', 'Multifunction sounder/GPS', 'Bluetooth audio with 4 Fusion speakers', 'Ambient LED lights', 'Underwater LED lights', 'New 2026 electric windlass', 'Custom side trampoline', '2 batteries', 'Boarding ladder'],
 ),
}

def wa(txt):
    return 'https://wa.me/34633742973?text=' + quote(txt, safe='')

def build(lang):
    pre = '' if lang == 'es' else lang + '/'
    tpl = os.path.join(ROOT, pre, 'barcos', TPL + '.html')
    t = open(tpl, encoding='utf-8').read()
    d = D[lang]
    e = html.escape
    # head
    t = re.sub(r'<title>.*?</title>', '<title>' + e(d['title']) + '</title>', t, 1)
    t = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="' + e(d['desc'], quote=True) + '">', t, 1)
    t = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="' + e(d['ogtitle'], quote=True) + '">', t, 1)
    t = re.sub(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="' + e(d['desc'], quote=True) + '">', t, 1)
    t = t.replace(TPL, SLUG)
    # JSON-LD
    imgs = ',\n'.join('"https://www.platamarine.com/%s-%d.jpg"' % (SLUG, i) for i in range(1, N_PHOTOS + 1))
    t = re.sub(r'"image": \[.*?\]', '"image": [\n' + imgs + '\n]', t, 1, re.S)
    t = re.sub(r'"name": "Starfisher 840 R \(2004\)"', '"name": ' + json_s(d['ldname']), t, 1)
    t = re.sub(r'"description": ".*?",\n"offers"', '"description": ' + json_s(d['lddesc']) + ',\n"offers"', t, 1, re.S)
    t = t.replace('"price": "50900"', '"price": "55000"')
    t = re.sub(r'"brand": \{\n"@type": "Brand",\n"name": "Starfisher"\n\},\n"model": "840 R"', '"brand": {\n"@type": "Brand",\n"name": "Boats Mak"\n},\n"model": "Cattleya X6"', t, 1)
    # whatsapp links (all variants of the starfisher texts)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Starfisher[^"]*(?:hablar|parlar|talk)[^"]*', wa(d['wa']), t)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Starfisher[^"]*', wa(d['wa_visit']), t)
    t = re.sub(r'https://wa\.me/\?text=[^"]*', 'https://wa.me/?text=' + quote(d['wa_share'], safe=''), t)
    # crumb, h1, sub
    t = re.sub(r'(<p class="crumb">.*?· )Starfisher 840 R(</p>)', r'\g<1>' + d['crumb'] + r'\2', t, 1)
    t = t.replace('<h1>Starfisher 840 R</h1>', '<h1>Cattleya X6</h1>')
    t = re.sub(r'<div class="sub">.*?</div>', '<div class="sub">' + ''.join('<span>%s</span>' % e(s) for s in d['sub']) + '</div>', t, 1)
    # price
    t = re.sub(r'<p class="price">[^<]*</p>', '<p class="price">%s <span class="vat">%s</span></p>' % (d['price'], d['vat']), t, 1)
    # pdf links
    t = re.sub(r'<a class="pdf-link" href="[^"]*" download>[^<]*</a>', '<a class="pdf-link" href="%s" download>%s</a>' % (d['pdf'], e(d['pdftxt'])), t, 1)
    t = re.sub(r'<a class="btn btn-ghost" href="[^"]*\.pdf" download>[^<]*</a>', '<a class="btn btn-ghost" href="%s" download>%s</a>' % (d['pdf'], e(d['pdfbtn'])), t, 1)
    # gallery
    t = re.sub(r'(<img class="main" id="main" [^>]*alt=")[^"]*(")', r'\g<1>' + e(d['alt'], quote=True) + r'\2', t, 1)
    thumbs = ''.join('<img src="/%s-%d-t.jpg" data-full="/%s-%d.jpg" alt="" loading="lazy" data-i="%d"%s>' % (SLUG, i, SLUG, i, i - 1, ' class="on"' if i == 1 else '') for i in range(1, N_PHOTOS + 1))
    t = re.sub(r'<div class="thumbs">.*?</div>', '<div class="thumbs">' + thumbs + '</div>', t, 1, re.S)
    # specs
    dl = '<dl class="specs">' + ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in d['specs']) + '</dl>'
    t = re.sub(r'<dl class="specs">.*?</dl>', dl, t, 1, re.S)
    # prose
    prose = '<div class="prose">\n<h2>%s</h2>\n%s\n<h3 class="equip-h">%s</h3><ul class="equip-tags">%s</ul>\n</div>' % (
        e(d['h2']), '\n'.join('<p>%s</p>' % e(p) for p in d['paras']), e(d['equip_h']), ''.join('<li>%s</li>' % e(x) for x in d['equip']))
    t = re.sub(r'<div class="prose">.*?</div>\n</div>', prose + '\n</div>', t, 1, re.S)
    # similares block: leave the marker for build_similares.js
    t = re.sub(r'<!--pm-sim-->.*?<!--/pm-sim-->', '<!--pm-sim--><!--/pm-sim-->', t, 1, re.S)
    assert 'Starfisher' not in t and 'starfisher' not in t and 'Yanmar' not in t and 'Galicia' not in t, [m for m in re.findall(r'.{30}(?:Starfisher|starfisher|Yanmar|Galicia).{30}', t)][:5]
    out = os.path.join(ROOT, pre, 'barcos', SLUG + '.html')
    open(out, 'w', encoding='utf-8').write(t)
    print('ok', out, len(t))

def json_s(s):
    import json
    return json.dumps(s, ensure_ascii=False)

for lang in ('es', 'ca', 'en'):
    build(lang)
