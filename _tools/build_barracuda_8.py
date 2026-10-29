"""Genera la ficha de la Beneteau Barracuda 8 (hoja firmada 29 oct 2026). Basado en build_audax_47.py.
Antes: Audax 47 (velero cúter de construcción propia, registro 2011, botadura 2012) en ES/CA/EN/FR
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
SLUG = 'barracuda-8'
TPL = 'monterey-278-ss'
TPL_NAME = 'Monterey 278 SS'
NAME = 'Beneteau Barracuda 8'
N_PHOTOS = 2
W1 = 1600

D = {
 'es': dict(
  title='Beneteau Barracuda 8 en venta · 57.990 € · Plata Marine',
  desc='Beneteau Barracuda 8 de 2016 con dos Suzuki DF150 (unas 1.050 h cada uno). Pilothouse para pesca y paseo en la Costa Daurada (Tarragona). 57.990 €, IVA pagado.',
  ogtitle='Beneteau Barracuda 8 en venta · 57.990 €',
  ldname='Beneteau Barracuda 8 (2016)',
  lddesc='Beneteau Barracuda 8 de 2016, pilothouse con timonera cerrada. Dos motores fueraborda Suzuki DF150 de 150 cv con 1.054 y 1.052 horas. Eslora de 7,99 m según el fabricante. En la Costa Daurada (Tarragona). Precio 57.990 € con el IVA pagado según el propietario.',
  sub=['2016', '7,99 m de eslora', '2 × Suzuki DF150', 'Costa Daurada'],
  price='57.990 €', vat='IVA pagado',
  pdf='barracuda-8.pdf', pdftxt='Descargar ficha completa (PDF)', pdfbtn='Descargar ficha PDF',
  wa='Hola Juan, me interesa la Beneteau Barracuda 8 que tenéis en venta. ¿Podemos hablar?',
  wa_visit='Hola Juan, me gustaría ver en persona la Beneteau Barracuda 8 de vuestra web. ¿Qué días se podría?',
  wa_share='Mira este barco: Beneteau Barracuda 8 — https://www.platamarine.com/barcos/barracuda-8',
  alt='Beneteau Barracuda 8 fondeada en una cala', photo='foto',
  specs=[('Tipo', 'Pilothouse con timonera cerrada, para pesca y paseo'), ('Año', '2016'),
         ('Eslora', '7,99 m (fabricante)'),
         ('Motores', '2 × Suzuki DF150'), ('Horas', '1.054 y 1.052 h'),
         ('Electrónica', 'Lowrance HDS-7 y pantalla Furuno'),
         ('Manga, depósitos y plazas', 'Se confirma con la documentación'),
         ('Titulación', 'PNB o superior'), ('Amarre', 'De alquiler, no se incluye en la venta'),
         ('Ubicación', 'Costa Daurada (Tarragona)'),
         ('Impuestos', 'IVA pagado, según el propietario; se confirma con la documentación antes de reservar')],
  h2='Cómo lo veo',
  paras=[
   'Una Barracuda 8 de 2016, el pilothouse de Beneteau pensado para pescar y para salir en familia: timonera cerrada con el puesto de mando protegido y una bañera despejada para moverse alrededor de todo el barco.',
   'Lleva dos fueraborda Suzuki DF150 con 1.054 y 1.052 horas, según la foto de los cuentahoras. Para un barco de 2016 es un uso normal. La última factura de mantenimiento la pido al propietario y se revisa antes de reservar.',
   'Está en la Costa Daurada (Tarragona), con un amarre de alquiler que no entra en la venta. Con 7,99 m de eslora según el fabricante basta el PNB o un título superior; la eslora de registro se confirma con la documentación. El precio son 57.990 €, con el IVA pagado según el propietario.',
   'Las fotos son del propietario. Pronto añadiré más del exterior y del interior; si te interesa antes, escríbeme y te paso lo que haya.',
  ],
  equip_h='Equipamiento',
  equip=['Timonera cerrada', '2 × Suzuki DF150', 'Lowrance HDS-7', 'Pantalla Furuno', 'Bañera para pesca', 'IVA pagado'],
  card=dict(alt='Beneteau Barracuda 8 fondeada en una cala', sub='2016 · 7,99 m · pilothouse · 2 × Suzuki 150 cv · Costa Daurada',
            tb='Titulación: PNB o superior',
            desc='Pilothouse de 2016 para pesca y paseo, con dos Suzuki DF150 de unas 1.050 horas cada uno y el IVA pagado. Se puede ver con cita previa.',
            ask='Preguntar por WhatsApp', see='Ver ficha'),
 ),
 'ca': dict(
  title='Beneteau Barracuda 8 en venda · 57.990 € · Plata Marine',
  desc='Beneteau Barracuda 8 del 2016 amb dos Suzuki DF150 (unes 1.050 h cadascun). Pilothouse per a pesca i passeig a la Costa Daurada (Tarragona). 57.990 €, IVA pagat.',
  ogtitle='Beneteau Barracuda 8 en venda · 57.990 €',
  ldname='Beneteau Barracuda 8 (2016)',
  lddesc="Beneteau Barracuda 8 del 2016, pilothouse amb timonera tancada. Dos motors fora borda Suzuki DF150 de 150 cv amb 1.054 i 1.052 hores. Eslora de 7,99 m segons el fabricant. A la Costa Daurada (Tarragona). Preu 57.990 € amb l'IVA pagat segons el propietari.",
  sub=['2016', '7,99 m d’eslora', '2 × Suzuki DF150', 'Costa Daurada'],
  price='57.990 €', vat='IVA pagat',
  pdf='/barcos/barracuda-8-ca.pdf', pdftxt='Descarregar la fitxa completa (PDF)', pdfbtn='Descarregar la fitxa PDF',
  wa="Hola Juan, m'interessa la Beneteau Barracuda 8 que teniu en venda. En podem parlar?",
  wa_visit="Hola Juan, m'agradaria veure en persona la Beneteau Barracuda 8 del vostre web. Quins dies es podria?",
  wa_share='Mira aquest vaixell: Beneteau Barracuda 8 — https://www.platamarine.com/ca/barcos/barracuda-8',
  alt='Beneteau Barracuda 8 fondejada en una cala', photo='foto',
  specs=[('Tipus', 'Pilothouse amb timonera tancada, per a pesca i passeig'), ('Any', '2016'),
         ('Eslora', '7,99 m (fabricant)'),
         ('Motors', '2 × Suzuki DF150'), ('Hores', '1.054 i 1.052 h'),
         ('Electrònica', 'Lowrance HDS-7 i pantalla Furuno'),
         ('Mànega, dipòsits i places', 'Es confirma amb la documentació'),
         ('Titulació', 'PNB o superior'), ('Amarrament', "De lloguer, no s'inclou en la venda"),
         ('Ubicació', 'Costa Daurada (Tarragona)'),
         ('Impostos', 'IVA pagat, segons el propietari; es confirma amb la documentació abans de reservar')],
  h2='Com ho veig',
  paras=[
   'Una Barracuda 8 del 2016, el pilothouse de Beneteau pensat per pescar i sortir en família: timonera tancada amb el lloc de comandament protegit i una banyera lliure per moure’s al voltant de tot el vaixell.',
   'Porta dos fora borda Suzuki DF150 amb 1.054 i 1.052 hores, segons la foto dels comptahores. Per a un vaixell del 2016 és un ús normal. L’última factura de manteniment la demano al propietari i es revisa abans de reservar.',
   'És a la Costa Daurada (Tarragona), amb un amarrament de lloguer que no entra en la venda. Amb 7,99 m d’eslora segons el fabricant n’hi ha prou amb el PNB o un títol superior; l’eslora de registre es confirma amb la documentació. El preu és de 57.990 €, amb l’IVA pagat segons el propietari.',
   'Les fotos són del propietari. Aviat n’afegiré més de l’exterior i de l’interior; si t’interessa abans, escriu-me i et passo el que hi hagi.',
  ],
  equip_h='Equipament',
  equip=['Timonera tancada', '2 × Suzuki DF150', 'Lowrance HDS-7', 'Pantalla Furuno', 'Banyera per a pesca', 'IVA pagat'],
  card=dict(alt='Beneteau Barracuda 8 fondejada en una cala', sub='2016 · 7,99 m · pilothouse · 2 × Suzuki 150 cv · Costa Daurada',
            tb='Titulació: PNB o superior',
            desc='Pilothouse del 2016 per a pesca i passeig, amb dos Suzuki DF150 d’unes 1.050 hores cadascun i l’IVA pagat. Es pot veure amb cita prèvia.',
            ask='Preguntar per WhatsApp', see='Veure fitxa'),
 ),
 'en': dict(
  title='Beneteau Barracuda 8 for sale · €57,990 · Plata Marine',
  desc='2016 Beneteau Barracuda 8 with twin Suzuki DF150 (about 1,050 h each). Pilothouse for fishing and cruising on the Costa Daurada (Tarragona). €57,990, VAT paid.',
  ogtitle='Beneteau Barracuda 8 for sale · €57,990',
  ldname='Beneteau Barracuda 8 (2016)',
  lddesc='2016 Beneteau Barracuda 8 pilothouse with enclosed wheelhouse. Twin Suzuki DF150 150 hp outboards with 1,054 and 1,052 hours. Length 7.99 m according to the builder. On the Costa Daurada (Tarragona). Price €57,990, VAT paid according to the owner.',
  sub=['2016', '7.99 m length', '2 × Suzuki DF150', 'Costa Daurada'],
  price='€57,990', vat='VAT paid',
  pdf='/barcos/barracuda-8-en.pdf', pdftxt='Download the full listing (PDF)', pdfbtn='Download PDF listing',
  wa="Hi Juan, I'm interested in the Beneteau Barracuda 8 you have for sale. Can we talk?",
  wa_visit="Hi Juan, I'd like to see the Beneteau Barracuda 8 from your website in person. Which days would work?",
  wa_share='Look at this boat: Beneteau Barracuda 8 — https://www.platamarine.com/en/barcos/barracuda-8',
  alt='Beneteau Barracuda 8 at anchor in a cove', photo='photo',
  specs=[('Type', 'Pilothouse with enclosed wheelhouse, for fishing and cruising'), ('Year', '2016'),
         ('Length', '7.99 m (builder)'),
         ('Engines', '2 × Suzuki DF150'), ('Hours', '1,054 and 1,052 h'),
         ('Electronics', 'Lowrance HDS-7 and Furuno display'),
         ('Beam, tanks and capacity', 'To be confirmed with the papers'),
         ('Licence', 'Spanish PNB or higher'), ('Berth', 'Rented, not included in the sale'),
         ('Location', 'Costa Daurada (Tarragona)'),
         ('Taxes', 'VAT paid, according to the owner; confirmed with the papers before reserving')],
  h2='How I see it',
  paras=[
   "A 2016 Barracuda 8, Beneteau's pilothouse designed for fishing and family days out: an enclosed wheelhouse with a sheltered helm and a clear cockpit so you can move all around the boat.",
   'It has twin Suzuki DF150 outboards with 1,054 and 1,052 hours, according to the photo of the hour meters. That is normal use for a 2016 boat. I ask the owner for the latest service invoice and it is checked before reserving.',
   'It is on the Costa Daurada (Tarragona), with a rented berth that is not part of the sale. At 7.99 m according to the builder, the Spanish PNB licence or higher is enough; the registered length is confirmed with the papers. The price is €57,990, VAT paid according to the owner.',
   "The photos are the owner's. I will add more of the exterior and interior soon; if you're interested before then, message me and I'll send you what there is.",
  ],
  equip_h='Equipment',
  equip=['Enclosed wheelhouse', '2 × Suzuki DF150', 'Lowrance HDS-7', 'Furuno display', 'Fishing cockpit', 'VAT paid'],
  card=dict(alt='Beneteau Barracuda 8 at anchor in a cove', sub='2016 · 7.99 m · pilothouse · 2 × Suzuki 150 hp · Costa Daurada',
            tb='Licence: PNB or higher',
            desc='2016 pilothouse for fishing and cruising, with twin Suzuki DF150 of about 1,050 hours each and VAT paid. Viewing by appointment.',
            ask='Ask on WhatsApp', see='See listing'),
 ),
 'fr': dict(
  title='Beneteau Barracuda 8 à vendre · 57 990 € · Plata Marine',
  desc='Beneteau Barracuda 8 de 2016 avec deux Suzuki DF150 (environ 1 050 h chacun). Pilothouse pour la pêche et la promenade sur la Costa Daurada (Tarragone). 57 990 €, TVA payée.',
  ogtitle='Beneteau Barracuda 8 à vendre · 57 990 €',
  ldname='Beneteau Barracuda 8 (2016)',
  lddesc="Beneteau Barracuda 8 de 2016, pilothouse avec timonerie fermée. Deux hors-bord Suzuki DF150 de 150 ch avec 1 054 et 1 052 heures. Longueur 7,99 m selon le constructeur. Sur la Costa Daurada (Tarragone). Prix 57 990 €, TVA payée selon le propriétaire.",
  sub=['2016', '7,99 m de longueur', '2 × Suzuki DF150', 'Costa Daurada'],
  price='57 990 €', vat='TVA payée',
  pdf='/barcos/barracuda-8-fr.pdf', pdftxt='Télécharger la fiche complète (PDF)', pdfbtn='Télécharger la fiche PDF (en français)',
  wa="Bonjour Juan, le Beneteau Barracuda 8 que vous avez à vendre m'intéresse. Pouvons-nous en parler ?",
  wa_visit="Bonjour Juan, j'aimerais voir sur place le Beneteau Barracuda 8 de votre site. Quels jours seraient possibles ?",
  wa_share='Regardez ce bateau : Beneteau Barracuda 8 — https://www.platamarine.com/fr/barcos/barracuda-8',
  alt='Beneteau Barracuda 8 au mouillage dans une crique', photo='photo',
  specs=[('Type', 'Pilothouse avec timonerie fermée, pour la pêche et la promenade'), ('Année', '2016'),
         ('Longueur', '7,99 m (constructeur)'),
         ('Moteurs', '2 × Suzuki DF150'), ('Heures', '1 054 et 1 052 h'),
         ('Électronique', 'Lowrance HDS-7 et écran Furuno'),
         ('Largeur, réservoirs et places', 'À confirmer avec les documents'),
         ('Permis', 'PNB espagnol ou supérieur'), ('Amarrage', 'En location, non inclus dans la vente'),
         ('Emplacement', 'Costa Daurada (Tarragone)'),
         ('Taxes', 'TVA payée, selon le propriétaire ; confirmé avec les documents avant la réservation')],
  h2='Mon avis',
  paras=[
   "Un Barracuda 8 de 2016, le pilothouse de Beneteau pensé pour la pêche et les sorties en famille : timonerie fermée avec un poste de pilotage abrité et un cockpit dégagé pour circuler tout autour du bateau.",
   "Il est équipé de deux hors-bord Suzuki DF150 avec 1 054 et 1 052 heures, d'après la photo des compteurs. C'est une utilisation normale pour un bateau de 2016. Je demande au propriétaire la dernière facture d'entretien, vérifiée avant la réservation.",
   "Il se trouve sur la Costa Daurada (Tarragone), avec un amarrage en location qui n'est pas inclus dans la vente. Avec 7,99 m selon le constructeur, le PNB espagnol ou un permis supérieur suffit ; la longueur d'immatriculation est confirmée avec les documents. Le prix est de 57 990 €, TVA payée selon le propriétaire.",
   "Les photos sont celles du propriétaire. J'en ajouterai bientôt d'autres de l'extérieur et de l'intérieur ; si le bateau vous intéresse avant, écrivez-moi et je vous enverrai ce qu'il y a.",
  ],
  equip_h='Équipement',
  equip=['Timonerie fermée', '2 × Suzuki DF150', 'Lowrance HDS-7', 'Écran Furuno', 'Cockpit de pêche', 'TVA payée'],
  card=dict(alt='Beneteau Barracuda 8 au mouillage dans une crique', sub='2016 · 7,99 m · pilothouse · 2 × Suzuki 150 ch · Costa Daurada',
            tb='Permis : PNB ou supérieur',
            desc='Pilothouse de 2016 pour la pêche et la promenade, avec deux Suzuki DF150 d’environ 1 050 heures chacun et TVA payée. Visite sur rendez-vous.',
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
    t = t.replace('"price": "49990"', '"price": "57990"')
    t = re.sub(r'"brand": \{\s*"@type": "Brand",\s*"name": "Monterey"\s*\},\s*"model": "278 SS"', '"brand": {\n    "@type": "Brand",\n    "name": "Beneteau"\n  },\n  "model": "Barracuda 8"', t, count=1)
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
    return ('      <article data-pm-boat="{s}" class="bcard" data-sold="0" data-tipo="motor" data-titulo="2" data-precio="57990" data-zona="cataluna" data-comb="gasolina" data-motor="fuera" data-anyo="2016" data-i="0.5">\n'
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
