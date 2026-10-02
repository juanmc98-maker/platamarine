"""Genera la ficha de la Rio 550 Cruiser (ES/CA/EN) a partir de la ficha de la Starfisher 840 como plantilla.
Uso: python3 _tools/build_rio_550_cruiser.py   (desde cualquier sitio)
Los datos pendientes del propietario van como "se confirma con la documentación"; al llegar, editar D y regenerar."""
import re, os, html, json
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'rio-550-cruiser'
TPL = 'starfisher-840'
N_PHOTOS = 5

D = {
 'es': dict(
  title='Rio 550 Cruiser 2001 en venta · 28.000 € · Plata Marine',
  desc='Rio 550 Cruiser de 2001, lancha cabinada con motor Suzuki 150 cv fueraborda de 2025 (aprox. 30 h, en garantía). Bimini, lona de bañera y cabina en proa. En Barcelona. 28.000 €. Ficha completa.',
  ogtitle='Rio 550 Cruiser 2001 en venta · 28.000 €',
  ldname='Rio 550 Cruiser (2001)',
  lddesc='Rio 550 Cruiser de 2001, lancha cabinada con motor fueraborda Suzuki 150 cv de 2025 (aprox. 30 h, en garantía), bimini, lona de bañera, asientos de piloto y copiloto, sofá de popa y cabina en proa. En tierra en la zona del Vallès (Barcelona). Precio 28.000 €.',
  crumb='Rio 550 Cruiser',
  sub=['Año 2001', 'Suzuki 150 cv de 2025', 'Gasolina, fueraborda', 'Barcelona (Vallès)'],
  price='28.000 €', vat='',
  pdf='rio-550-cruiser.pdf', pdftxt='Descargar ficha completa (PDF)', pdfbtn='Descargar ficha PDF',
  wa='Hola Juan, me interesa la Rio 550 Cruiser de 2001 que tenéis en venta. ¿Podemos hablar?',
  wa_visit='Hola Juan, me gustaría ver en persona la Rio 550 Cruiser (2001) de vuestra web. ¿Qué días se podría?',
  wa_share='Mira este barco: Rio 550 Cruiser — https://www.platamarine.com/barcos/rio-550-cruiser.html',
  alt='Rio 550 Cruiser fondeada en una cala, vista de proa',
  specs=[('Año', '2001'), ('Tipo', 'Lancha cabinada'), ('Eslora', 'Aprox. 5,50 m (se confirma con la documentación)'),
         ('Capacidad', 'Se confirma con la documentación'), ('Motor', 'Suzuki 150 cv, gasolina fueraborda · de 2025, en garantía'),
         ('Horas', 'Aprox. 30 (motor)'),
         ('Cubierta', 'Bimini · lona de bañera · asientos de piloto y copiloto · sofá de popa · suelo de bañera tipo teca · cabina en proa'),
         ('Ubicación', 'En tierra, zona del Vallès (Barcelona)'),
         ('Amarre', 'No incluido'), ('Remolque', 'No incluido'),
         ('Titulación', 'Licencia de Navegación o superior'), ('Bandera', 'Española'),
         ('ITB', 'Se confirma con la documentación'),
         ('Visitas', 'Con cita previa; la prueba en el agua, tras dejar una señal'),
         ('Impuestos', 'Vende un particular: no lleva IVA; el comprador paga el ITP de su comunidad')],
  h2='Cómo lo veo',
  paras=[
   'Una Rio 550 Cruiser de 2001, la lancha cabinada pequeña del astillero italiano Rio: bañera con asientos de piloto y copiloto, sofá en popa y una cabina en proa para guardar el equipo o resguardarse un rato. Es un barco de día, fácil de manejar y de mantener.',
   'Lo que más pesa en este barco es el motor: un Suzuki fueraborda de 150 CV de 2025, con unas 30 horas y todavía en garantía. En una lancha de este tamaño es una potencia holgada, y en un casco de estos años tener el motor prácticamente nuevo es lo que más tranquilidad da al comprador.',
   'Lleva bimini, lona de bañera y suelo de bañera tipo teca. Ahora está en tierra en la zona del Vallès (Barcelona); el precio no incluye amarre ni remolque. Se puede ver con cita previa, y la prueba en el agua se hace después de dejar una señal.',
   'Por eslora se puede gobernar con la Licencia de Navegación o un título superior. Los datos de capacidad e ITB se confirman con la documentación. El precio son 28.000 €; vende un particular, así que no lleva IVA y el comprador paga el ITP de su comunidad.',
  ],
  equip_h='Equipamiento',
  equip=['Suzuki 150 cv fueraborda de 2025, en garantía', 'Aprox. 30 horas de motor', 'Bimini', 'Lona de bañera', 'Asientos de piloto y copiloto', 'Sofá de popa', 'Suelo de bañera tipo teca', 'Cabina en proa', 'Parabrisas envolvente'],
 ),
 'ca': dict(
  title='Rio 550 Cruiser 2001 en venda · 28.000 € · Plata Marine',
  desc='Rio 550 Cruiser del 2001, llanxa amb cabina i motor Suzuki 150 cv forabord del 2025 (aprox. 30 h, en garantia). Bimini, lona de banyera i cabina a proa. A Barcelona. 28.000 €. Fitxa completa.',
  ogtitle='Rio 550 Cruiser 2001 en venda · 28.000 €',
  ldname='Rio 550 Cruiser (2001)',
  lddesc='Rio 550 Cruiser del 2001, llanxa amb cabina i motor forabord Suzuki 150 cv del 2025 (aprox. 30 h, en garantia), bimini, lona de banyera, seients de pilot i copilot, sofà de popa i cabina a proa. En terra a la zona del Vallès (Barcelona). Preu 28.000 €.',
  crumb='Rio 550 Cruiser',
  sub=['Any 2001', 'Suzuki 150 cv del 2025', 'Gasolina, forabord', 'Barcelona (Vallès)'],
  price='28.000 €', vat='',
  pdf='/barcos/rio-550-cruiser-ca.pdf', pdftxt='Descarregar la fitxa completa (PDF)', pdfbtn='Descarregar fitxa PDF (en català)',
  wa="Hola Juan, m'interessa la Rio 550 Cruiser del 2001 que teniu en venda. Podem parlar?",
  wa_visit="Hola Juan, m'agradaria veure en persona la Rio 550 Cruiser (2001) de la vostra web. Quins dies es podria?",
  wa_share='Mira aquest vaixell: Rio 550 Cruiser — https://www.platamarine.com/ca/barcos/rio-550-cruiser.html',
  alt='Rio 550 Cruiser fondejada en una cala, vista de proa',
  specs=[('Any', '2001'), ('Tipus', 'Llanxa amb cabina'), ('Eslora', 'Aprox. 5,50 m (es confirma amb la documentació)'),
         ('Capacitat', 'Es confirma amb la documentació'), ('Motor', 'Suzuki 150 cv, gasolina forabord · del 2025, en garantia'),
         ('Hores', 'Aprox. 30 (motor)'),
         ('Coberta', 'Bimini · lona de banyera · seients de pilot i copilot · sofà de popa · terra de banyera tipus teca · cabina a proa'),
         ('Ubicació', 'En terra, zona del Vallès (Barcelona)'),
         ('Amarratge', 'No inclòs'), ('Remolc', 'No inclòs'),
         ('Titulació', 'Llicència de Navegació o superior'), ('Bandera', 'Espanyola'),
         ('ITB', 'Es confirma amb la documentació'),
         ('Visites', "Amb cita prèvia; la prova a l'aigua, després de deixar un senyal"),
         ('Impostos', "Ven un particular: no porta IVA; el comprador paga l'ITP de la seva comunitat")],
  h2='Com el veig',
  paras=[
   'Una Rio 550 Cruiser del 2001, la llanxa amb cabina petita de la drassana italiana Rio: banyera amb seients de pilot i copilot, sofà a popa i una cabina a proa per guardar l\'equip o resguardar-se una estona. És un vaixell de dia, fàcil de manejar i de mantenir.',
   'El que més pesa en aquest vaixell és el motor: un Suzuki forabord de 150 CV del 2025, amb unes 30 hores i encara en garantia. En una llanxa d\'aquesta mida és una potència folgada, i en un buc d\'aquests anys tenir el motor pràcticament nou és el que dona més tranquil·litat al comprador.',
   'Porta bimini, lona de banyera i terra de banyera tipus teca. Ara és en terra a la zona del Vallès (Barcelona); el preu no inclou amarratge ni remolc. Es pot veure amb cita prèvia, i la prova a l\'aigua es fa després de deixar un senyal.',
   'Per eslora es pot governar amb la Llicència de Navegació o un títol superior. Les dades de capacitat i ITB es confirmen amb la documentació. El preu són 28.000 €; ven un particular, de manera que no porta IVA i el comprador paga l\'ITP de la seva comunitat.',
  ],
  equip_h='Equipament',
  equip=['Suzuki 150 cv forabord del 2025, en garantia', 'Aprox. 30 hores de motor', 'Bimini', 'Lona de banyera', 'Seients de pilot i copilot', 'Sofà de popa', 'Terra de banyera tipus teca', 'Cabina a proa', 'Parabrisa envoltant'],
 ),
 'en': dict(
  title='2001 Rio 550 Cruiser for sale · €28,000 · Plata Marine',
  desc='2001 Rio 550 Cruiser, small cabin boat with a 2025 Suzuki 150 hp outboard (approx. 30 h, under warranty). Bimini, cockpit cover and bow cabin. Near Barcelona. €28,000. Full listing.',
  ogtitle='2001 Rio 550 Cruiser for sale · €28,000',
  ldname='Rio 550 Cruiser (2001)',
  lddesc='2001 Rio 550 Cruiser, small cabin boat with a 2025 Suzuki 150 hp outboard (approx. 30 h, under warranty), bimini, cockpit cover, helm and co-pilot seats, aft sofa and bow cabin. Ashore in the Vallès area (Barcelona). Price €28,000.',
  crumb='Rio 550 Cruiser',
  sub=['Year 2001', '2025 Suzuki 150 hp', 'Petrol, outboard', 'Barcelona (Vallès)'],
  price='€28,000', vat='',
  pdf='/barcos/rio-550-cruiser-en.pdf', pdftxt='Download full spec sheet (PDF)', pdfbtn='Download PDF listing (in English)',
  wa="Hi Juan, I'm interested in the 2001 Rio 550 Cruiser you have for sale. Can we talk?",
  wa_visit="Hi Juan, I'd like to see the Rio 550 Cruiser (2001) from your website in person. Which days would work?",
  wa_share='Check out this boat: Rio 550 Cruiser — https://www.platamarine.com/en/barcos/rio-550-cruiser.html',
  alt='Rio 550 Cruiser at anchor in a cove, bow view',
  specs=[('Year', '2001'), ('Type', 'Small cabin boat'), ('Length', 'Approx. 5.50 m (confirmed from the documentation)'),
         ('Capacity', 'Confirmed from the documentation'), ('Engine', 'Suzuki 150 hp petrol outboard · 2025, under warranty'),
         ('Hours', 'Approx. 30 (engine)'),
         ('Deck', 'Bimini · cockpit cover · helm and co-pilot seats · aft sofa · teak-style cockpit floor · bow cabin'),
         ('Location', 'Ashore, Vallès area (Barcelona)'),
         ('Berth', 'Not included'), ('Trailer', 'Not included'),
         ('Licence', 'Navigation Licence or higher'), ('Flag', 'Spanish'),
         ('ITB', 'Confirmed from the documentation'),
         ('Viewings', 'By appointment; sea trial after a deposit'),
         ('Taxes', 'Private seller: no VAT; the buyer pays the transfer tax (ITP) of their region')],
  h2='My take',
  paras=[
   'A 2001 Rio 550 Cruiser, the small cabin boat from the Italian yard Rio: a cockpit with helm and co-pilot seats, an aft sofa and a bow cabin to stow gear or get out of the sun for a while. It is a day boat that is easy to handle and to look after.',
   'What matters most on this boat is the engine: a 2025 Suzuki 150 hp outboard with around 30 hours, still under warranty. On a boat of this size that is plenty of power, and on a hull of this age having a practically new engine is what gives a buyer the most peace of mind.',
   'It has a bimini, a cockpit cover and a teak-style cockpit floor. It is currently ashore in the Vallès area (Barcelona); the price does not include a berth or a trailer. It can be viewed by appointment, and the sea trial takes place after a deposit has been paid.',
   'By length it can be skippered with the Navigation Licence or a higher qualification. Capacity and ITB details are confirmed from the documentation. The price is €28,000; it is a private sale, so there is no VAT and the buyer pays the transfer tax (ITP) of their region.',
  ],
  equip_h='Equipment',
  equip=['2025 Suzuki 150 hp outboard, under warranty', 'Approx. 30 engine hours', 'Bimini', 'Cockpit cover', 'Helm and co-pilot seats', 'Aft sofa', 'Teak-style cockpit floor', 'Bow cabin', 'Wraparound windscreen'],
 ),
}

def wa(txt):
    return 'https://wa.me/34633742973?text=' + quote(txt, safe='')

def json_s(s):
    return json.dumps(s, ensure_ascii=False)

def build(lang):
    pre = '' if lang == 'es' else lang + '/'
    tpl = os.path.join(ROOT, pre, 'barcos', TPL + '.html')
    t = open(tpl, encoding='utf-8').read()
    d = D[lang]
    e = html.escape
    t = re.sub(r'<title>.*?</title>', '<title>' + e(d['title']) + '</title>', t, 1)
    t = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="' + e(d['desc'], quote=True) + '">', t, 1)
    t = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="' + e(d['ogtitle'], quote=True) + '">', t, 1)
    t = re.sub(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="' + e(d['desc'], quote=True) + '">', t, 1)
    t = t.replace(TPL, SLUG)
    imgs = ',\n'.join('"https://www.platamarine.com/%s-%d.jpg"' % (SLUG, i) for i in range(1, N_PHOTOS + 1))
    t = re.sub(r'"image": \[.*?\]', '"image": [\n' + imgs + '\n]', t, 1, re.S)
    t = re.sub(r'"name": "Starfisher 840 R \(2004\)"', '"name": ' + json_s(d['ldname']), t, 1)
    t = re.sub(r'"description": ".*?",\n"offers"', '"description": ' + json_s(d['lddesc']) + ',\n"offers"', t, 1, re.S)
    t = t.replace('"price": "50900"', '"price": "28000"')
    t = re.sub(r'"brand": \{\n"@type": "Brand",\n"name": "Starfisher"\n\},\n"model": "840 R"', '"brand": {\n"@type": "Brand",\n"name": "Rio"\n},\n"model": "550 Cruiser"', t, 1)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Starfisher[^"]*(?:hablar|parlar|talk)[^"]*', wa(d['wa']), t)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Starfisher[^"]*', wa(d['wa_visit']), t)
    t = re.sub(r'https://wa\.me/\?text=[^"]*', 'https://wa.me/?text=' + quote(d['wa_share'], safe=''), t)
    t = re.sub(r'(<p class="crumb">.*?· )Starfisher 840 R(</p>)', r'\g<1>' + d['crumb'] + r'\2', t, 1)
    t = t.replace('<h1>Starfisher 840 R</h1>', '<h1>Rio 550 Cruiser</h1>')
    t = re.sub(r'<div class="sub">.*?</div>', '<div class="sub">' + ''.join('<span>%s</span>' % e(s) for s in d['sub']) + '</div>', t, 1)
    pr = d['price'] + (' <span class="vat">%s</span>' % d['vat'] if d['vat'] else '')
    t = re.sub(r'<p class="price">[^<]*(?:<span class="vat">[^<]*</span>)?</p>', '<p class="price">%s</p>' % pr, t, 1)
    t = re.sub(r'<a class="pdf-link" href="[^"]*" download>[^<]*</a>', '<a class="pdf-link" href="%s" download>%s</a>' % (d['pdf'], e(d['pdftxt'])), t, 1)
    t = re.sub(r'<a class="btn btn-ghost" href="[^"]*\.pdf" download>[^<]*</a>', '<a class="btn btn-ghost" href="%s" download>%s</a>' % (d['pdf'], e(d['pdfbtn'])), t, 1)
    t = re.sub(r'(<img class="main" id="main" [^>]*alt=")[^"]*(")', r'\g<1>' + e(d['alt'], quote=True) + r'\2', t, 1)
    thumbs = ''.join('<img src="/%s-%d-t.jpg" data-full="/%s-%d.jpg" alt="" loading="lazy" data-i="%d"%s>' % (SLUG, i, SLUG, i, i - 1, ' class="on"' if i == 1 else '') for i in range(1, N_PHOTOS + 1))
    t = re.sub(r'<div class="thumbs">.*?</div>', '<div class="thumbs">' + thumbs + '</div>', t, 1, re.S)
    dl = '<dl class="specs">' + ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in d['specs']) + '</dl>'
    t = re.sub(r'<dl class="specs">.*?</dl>', dl, t, 1, re.S)
    prose = '<div class="prose">\n<h2>%s</h2>\n%s\n<h3 class="equip-h">%s</h3><ul class="equip-tags">%s</ul>\n</div>' % (
        e(d['h2']), '\n'.join('<p>%s</p>' % e(p) for p in d['paras']), e(d['equip_h']), ''.join('<li>%s</li>' % e(x) for x in d['equip']))
    t = re.sub(r'<div class="prose">.*?</div>\n</div>', prose + '\n</div>', t, 1, re.S)
    t = re.sub(r'<!--pm-sim-->.*?<!--/pm-sim-->', '<!--pm-sim--><!--/pm-sim-->', t, 1, re.S)
    bad = [m for m in re.findall(r'.{30}(?:Starfisher|starfisher|Yanmar|Galicia|Vigo).{30}', t)]
    assert not bad, bad[:5]
    out = os.path.join(ROOT, pre, 'barcos', SLUG + '.html')
    open(out, 'w', encoding='utf-8').write(t)
    print('ok', out, len(t))

for lang in ('es', 'ca', 'en'):
    build(lang)
