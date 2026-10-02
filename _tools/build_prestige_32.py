"""Genera la ficha de la Jeanneau Prestige 32 (ES/CA/EN) a partir de la ficha de la Starfisher 840 como plantilla.
Uso: python3 _tools/build_prestige_32.py   (desde cualquier sitio)
Los datos pendientes del propietario van como "se confirma con la documentación"; al llegar, editar D y regenerar."""
import re, os, html, json
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'prestige-32'
TPL = 'starfisher-840'
N_PHOTOS = 18

D = {
 'es': dict(
  title='Jeanneau Prestige 32 2006 en venta · 89.000 € · Plata Marine',
  desc='Jeanneau Prestige 32 de 2006 con flybridge, Volvo Penta D4 260 cv diésel (aprox. 1.500 h), dos camarotes, salón con cocina y baño, auxiliar en pescante. En Menorca. 89.000 €. Ficha completa.',
  ogtitle='Jeanneau Prestige 32 2006 en venta · 89.000 €',
  ldname='Jeanneau Prestige 32 (2006)',
  lddesc='Jeanneau Prestige 32 de 2006, motor con flybridge y doble puesto de gobierno, Volvo Penta D4 de 260 cv diésel (aprox. 1.500 h). Dos camarotes, salón con cocina y TV, baño, plataforma de baño y auxiliar en pescante. Con base en Menorca. Precio 89.000 €.',
  crumb='Prestige 32',
  sub=['Año 2006', 'Volvo Penta D4 260 cv', 'Diésel, flybridge', 'Menorca'],
  price='89.000 €', vat='',
  pdf='prestige-32.pdf', pdftxt='Descargar ficha completa (PDF)', pdfbtn='Descargar ficha PDF',
  wa='Hola Juan, me interesa la Jeanneau Prestige 32 de 2006 que tenéis en venta. ¿Podemos hablar?',
  wa_visit='Hola Juan, me gustaría ver en persona la Jeanneau Prestige 32 (2006) de vuestra web. ¿Qué días se podría?',
  wa_share='Mira este barco: Jeanneau Prestige 32 — https://www.platamarine.com/barcos/prestige-32.html',
  alt='Jeanneau Prestige 32 fondeada en una cala, vista de costado con el auxiliar en el pescante',
  specs=[('Año', '2006'), ('Tipo', 'Motor con flybridge'), ('Eslora', '10,65 m (dato del fabricante)'), ('Manga', '3,52 m (dato del fabricante)'),
         ('Capacidad', 'Se confirma con la documentación'),
         ('Motor', 'Volvo Penta D4 260 cv, diésel'), ('Horas', 'Aprox. 1.500'),
         ('Camarotes', '2 (proa y camarote con TV)'), ('Baños', '1'),
         ('Cubierta', 'Flybridge con bimini y segundo puesto de gobierno · solárium de proa · plataforma de baño · pescante con auxiliar y fueraborda'),
         ('Electrónica', 'Plotter/sonda · VHF · instrumentación del motor en ambos puestos'),
         ('Amarre', 'Se confirma con el propietario'),
         ('Titulación', 'PER o superior'), ('Bandera', 'Española'),
         ('ITB', 'Se confirma con la documentación'),
         ('Impuestos', 'Vende un particular: no lleva IVA; el comprador paga el ITP de su comunidad')],
  h2='Cómo lo veo',
  paras=[
   'Una Jeanneau Prestige 32 de 2006, el modelo con el que el astillero francés hizo famosa su gama de flybridge compactos: un barco de 10,65 metros que se maneja como uno pequeño y se vive como uno grande. Tiene dos puestos de gobierno, el interior y el del flybridge, que lleva bimini y espacio para ir arriba todos los de a bordo.',
   'Monta un único Volvo Penta D4 de 260 CV diésel con unas 1.500 horas, una motorización conocida y con buen servicio en toda la costa. Un solo motor significa menos mantenimiento y menos consumo que un bimotor, y para navegar entre islas o por la costa va sobrado.',
   'Por dentro lleva un salón con mesa, sofá y cocina, dos camarotes (el de proa y un segundo camarote con televisión) y un baño completo. Las fotos muestran una tapicería y una madera cuidadas, y la plataforma de baño con el pescante y el auxiliar con fueraborda, que es lo que marca la diferencia cuando fondeas en una cala.',
   'A quien la veo encajar es a una pareja o una familia que quiera un barco para fines de semana y vacaciones por Baleares, con cabina de verdad y un flybridge para disfrutar la navegación. Se puede gobernar con el PER o un título superior. Está en Menorca y se puede ver con cita previa. El precio son 89.000 €, y como vende un particular no lleva IVA.',
  ],
  equip_h='Equipamiento',
  equip=['Volvo Penta D4 260 cv diésel', 'Flybridge con bimini', 'Doble puesto de gobierno', 'Solárium de proa', 'Plataforma de baño', 'Pescante con auxiliar y fueraborda', 'Salón con mesa y cocina', 'Televisión', '2 camarotes', 'Baño completo', 'Plotter/sonda', 'VHF', 'Defensas y cabos'],
 ),
 'ca': dict(
  title='Jeanneau Prestige 32 2006 en venda · 89.000 € · Plata Marine',
  desc='Jeanneau Prestige 32 del 2006 amb flybridge, Volvo Penta D4 260 cv dièsel (aprox. 1.500 h), dues cabines, saló amb cuina i bany, auxiliar al pescant. A Menorca. 89.000 €. Fitxa completa.',
  ogtitle='Jeanneau Prestige 32 2006 en venda · 89.000 €',
  ldname='Jeanneau Prestige 32 (2006)',
  lddesc='Jeanneau Prestige 32 del 2006, motor amb flybridge i doble lloc de govern, Volvo Penta D4 de 260 cv dièsel (aprox. 1.500 h). Dues cabines, saló amb cuina i TV, bany, plataforma de bany i auxiliar al pescant. Amb base a Menorca. Preu 89.000 €.',
  crumb='Prestige 32',
  sub=['Any 2006', 'Volvo Penta D4 260 cv', 'Dièsel, flybridge', 'Menorca'],
  price='89.000 €', vat='',
  pdf='/barcos/prestige-32-ca.pdf', pdftxt='Descarregar la fitxa completa (PDF)', pdfbtn='Descarregar fitxa PDF (en català)',
  wa="Hola Juan, m'interessa la Jeanneau Prestige 32 del 2006 que teniu en venda. Podem parlar?",
  wa_visit="Hola Juan, m'agradaria veure en persona la Jeanneau Prestige 32 (2006) de la vostra web. Quins dies es podria?",
  wa_share='Mira aquest vaixell: Jeanneau Prestige 32 — https://www.platamarine.com/ca/barcos/prestige-32.html',
  alt='Jeanneau Prestige 32 fondejada en una cala, vista de costat amb l\'auxiliar al pescant',
  specs=[('Any', '2006'), ('Tipus', 'Motor amb flybridge'), ('Eslora', '10,65 m (dada del fabricant)'), ('Mànega', '3,52 m (dada del fabricant)'),
         ('Capacitat', 'Es confirma amb la documentació'),
         ('Motor', 'Volvo Penta D4 260 cv, dièsel'), ('Hores', 'Aprox. 1.500'),
         ('Cabines', '2 (proa i cabina amb TV)'), ('Banys', '1'),
         ('Coberta', 'Flybridge amb bimini i segon lloc de govern · solàrium de proa · plataforma de bany · pescant amb auxiliar i forabord'),
         ('Electrònica', 'Plotter/sonda · VHF · instrumentació del motor als dos llocs'),
         ('Amarratge', 'Es confirma amb el propietari'),
         ('Titulació', 'PER o superior'), ('Bandera', 'Espanyola'),
         ('ITB', 'Es confirma amb la documentació'),
         ('Impostos', 'Ven un particular: no porta IVA; el comprador paga l\'ITP de la seva comunitat')],
  h2='Com el veig',
  paras=[
   'Una Jeanneau Prestige 32 del 2006, el model amb què la drassana francesa va fer famosa la seva gamma de flybridge compactes: un vaixell de 10,65 metres que es maneja com un de petit i es viu com un de gran. Té dos llocs de govern, l\'interior i el del flybridge, que porta bimini i espai perquè hi pugin tots els de bord.',
   'Munta un únic Volvo Penta D4 de 260 CV dièsel amb unes 1.500 hores, una motorització coneguda i amb bon servei a tota la costa. Un sol motor vol dir menys manteniment i menys consum que un bimotor, i per navegar entre illes o per la costa va sobrat.',
   'Per dins porta un saló amb taula, sofà i cuina, dues cabines (la de proa i una segona cabina amb televisió) i un bany complet. Les fotos mostren una tapisseria i una fusta cuidades, i la plataforma de bany amb el pescant i l\'auxiliar amb forabord, que és el que marca la diferència quan fondeges en una cala.',
   'A qui el veig encaixar és a una parella o una família que vulgui un vaixell per a caps de setmana i vacances per les Balears, amb cabina de debò i un flybridge per gaudir de la navegació. Es pot governar amb el PER o un títol superior. És a Menorca i es pot veure amb cita prèvia. El preu són 89.000 €, i com que ven un particular no porta IVA.',
  ],
  equip_h='Equipament',
  equip=['Volvo Penta D4 260 cv dièsel', 'Flybridge amb bimini', 'Doble lloc de govern', 'Solàrium de proa', 'Plataforma de bany', 'Pescant amb auxiliar i forabord', 'Saló amb taula i cuina', 'Televisió', '2 cabines', 'Bany complet', 'Plotter/sonda', 'VHF', 'Defenses i caps'],
 ),
 'en': dict(
  title='2006 Jeanneau Prestige 32 for sale · €89,000 · Plata Marine',
  desc='2006 Jeanneau Prestige 32 flybridge with a Volvo Penta D4 260 hp diesel (approx. 1,500 h), two cabins, saloon with galley and heads, tender on davits. Based in Menorca. €89,000. Full listing.',
  ogtitle='2006 Jeanneau Prestige 32 for sale · €89,000',
  ldname='Jeanneau Prestige 32 (2006)',
  lddesc='2006 Jeanneau Prestige 32, flybridge motor boat with two helm positions, single Volvo Penta D4 260 hp diesel (approx. 1,500 h). Two cabins, saloon with galley and TV, heads, bathing platform and tender on davits. Based in Menorca. Price €89,000.',
  crumb='Prestige 32',
  sub=['Year 2006', 'Volvo Penta D4 260 hp', 'Diesel, flybridge', 'Menorca'],
  price='€89,000', vat='',
  pdf='/barcos/prestige-32-en.pdf', pdftxt='Download full spec sheet (PDF)', pdfbtn='Download PDF listing (in English)',
  wa="Hi Juan, I'm interested in the 2006 Jeanneau Prestige 32 you have for sale. Can we talk?",
  wa_visit="Hi Juan, I'd like to see the Jeanneau Prestige 32 (2006) from your website in person. Which days would work?",
  wa_share='Check out this boat: Jeanneau Prestige 32 — https://www.platamarine.com/en/barcos/prestige-32.html',
  alt='Jeanneau Prestige 32 at anchor in a cove, side view with the tender on the davits',
  specs=[('Year', '2006'), ('Type', 'Flybridge motor boat'), ('Length', '10.65 m (manufacturer figure)'), ('Beam', '3.52 m (manufacturer figure)'),
         ('Capacity', 'Confirmed from the documentation'),
         ('Engine', 'Volvo Penta D4 260 hp, diesel'), ('Hours', 'Approx. 1,500'),
         ('Cabins', '2 (forward cabin and a second cabin with TV)'), ('Heads', '1'),
         ('Deck', 'Flybridge with bimini and second helm · bow sunpad · bathing platform · davits with tender and outboard'),
         ('Electronics', 'Chartplotter/sounder · VHF · engine instruments at both helms'),
         ('Berth', 'To be confirmed with the owner'),
         ('Licence', 'PER or higher'), ('Flag', 'Spanish'),
         ('ITB', 'Confirmed from the documentation'),
         ('Taxes', 'Private seller: no VAT; the buyer pays the transfer tax (ITP) of their region')],
  h2='My take',
  paras=[
   'A 2006 Jeanneau Prestige 32, the model that made the French yard\'s range of compact flybridge boats famous: a 10.65-metre boat that handles like a small one and lives like a big one. It has two helm positions, inside and up on the flybridge, which has a bimini and room for everyone on board to sit up top.',
   'It is powered by a single Volvo Penta D4 260 hp diesel with around 1,500 hours, a well-known engine with good service support all along the coast. One engine means less maintenance and lower fuel consumption than a twin, and for hopping between islands or cruising the coast it has plenty in hand.',
   'Below there is a saloon with table, sofa and galley, two cabins (the forward cabin and a second cabin with a television) and a full heads compartment. The photos show well-kept upholstery and woodwork, and the bathing platform with the davits and the tender with its outboard, which is what makes the difference when you anchor in a cove.',
   'Who I see it suiting is a couple or a family wanting a boat for weekends and holidays around the Balearics, with a proper cabin and a flybridge to enjoy the trip. It can be skippered with the Spanish PER or a higher qualification. It is in Menorca and can be viewed by appointment. The price is €89,000, and as it is a private sale there is no VAT.',
  ],
  equip_h='Equipment',
  equip=['Volvo Penta D4 260 hp diesel', 'Flybridge with bimini', 'Two helm positions', 'Bow sunpad', 'Bathing platform', 'Davits with tender and outboard', 'Saloon with table and galley', 'Television', '2 cabins', 'Full heads', 'Chartplotter/sounder', 'VHF', 'Fenders and lines'],
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
    t = t.replace('"price": "50900"', '"price": "89000"')
    t = re.sub(r'"brand": \{\n"@type": "Brand",\n"name": "Starfisher"\n\},\n"model": "840 R"', '"brand": {\n"@type": "Brand",\n"name": "Jeanneau"\n},\n"model": "Prestige 32"', t, 1)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Starfisher[^"]*(?:hablar|parlar|talk)[^"]*', wa(d['wa']), t)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Starfisher[^"]*', wa(d['wa_visit']), t)
    t = re.sub(r'https://wa\.me/\?text=[^"]*', 'https://wa.me/?text=' + quote(d['wa_share'], safe=''), t)
    t = re.sub(r'(<p class="crumb">.*?· )Starfisher 840 R(</p>)', r'\g<1>' + d['crumb'] + r'\2', t, 1)
    t = t.replace('<h1>Starfisher 840 R</h1>', '<h1>Jeanneau Prestige 32</h1>')
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
