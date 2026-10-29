"""Genera la ficha de la Beneteau Swift Trawler 34 (2015) en ES/CA/EN/FR. Basado en build_barracuda_8.py.
Parte de la ficha del Monterey 278 SS como plantilla, prepara las fotos (<slug>-N.jpg, -m.jpg, -t.jpg), añade la tarjeta
al catálogo /barcos/ de los 4 idiomas, la entrada de inventario.js y las 4 URL del sitemap (todo idempotente).
Después lanza el resto: _tools/ficha_v2.py swift-trawler-34 (datos en _tools/ficha_v2_boats/swift_trawler_34.py),
_tools/coste_v2.py, PM_ROOT=<repo> _tools/build_pdfs.py swift-trawler-34 y _tools/build_search_index.py.

Uso, con las fotos definitivas (JPG numerados en el orden de la galería; la 1 es la de portada y tarjeta):
    python3 _tools/build_swift_trawler_34.py --fotos /ruta/a/la/carpeta
Sin --fotos usa la carpeta y el orden de PRUEBA (TEST_DIR / TEST_ORDER).
Al cambiar las fotos, revisar PH y SPOTS_XY en _tools/ficha_v2_boats/swift_trawler_34.py (números de foto de cada bloque).

Datos: hoja de encargo y propietario (año, precio, motor y horas, zona, amarre) y fabricante (medidas, depósitos, plazas,
distribución). Lo que no consta va como "se confirma con la documentación". Sin nombre de la embarcación ni puerto exacto
(solo "Cambrils"). Vende un particular: el IVA no se afirma."""
import re, os, sys, html, json, glob, datetime, subprocess
from urllib.parse import quote
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'swift-trawler-34'
TPL = 'monterey-278-ss'
TPL_NAME = 'Monterey 278 SS'
NAME = 'Beneteau Swift Trawler 34'
PRICE = 179990
W1 = 1600

TEST_DIR = '/mnt/user-data/uploads/fran'
TEST_ORDER = ['fran_05.jpg', 'fran_02.jpg', 'fran_26.jpg', 'fran_25.jpg', 'fran_06.jpg', 'fran_07.jpg', 'fran_08.jpg', 'fran_14.jpg',
              'fran_16.jpg', 'fran_13.jpg', 'fran_23.jpg', 'fran_24.jpg', 'fran_10.jpg', 'fran_09.jpg', 'fran_22.jpg', 'fran_21.jpg',
              'fran_19.jpg', 'fran_18.jpg', 'fran_20.jpg']

TAX = {
 'es': 'Vende un particular: normalmente el comprador paga el ITP de su comunidad. La situación del IVA del barco se confirma con la documentación antes de reservar',
 'ca': "Ven un particular: normalment el comprador paga l'ITP de la seva comunitat. La situació de l'IVA del vaixell es confirma amb la documentació abans de reservar",
 'en': "Private seller: the buyer normally pays the transfer tax (ITP) of their region. The boat's VAT status is confirmed with the papers before reserving",
 'fr': "Vendeur particulier : l'acheteur paie normalement l'impôt sur les transmissions (ITP) de sa région. La situation de la TVA du bateau est confirmée avec les documents avant la réservation",
}

D = {
 'es': dict(
  title='Beneteau Swift Trawler 34 en venta, 179.990 € · Plata Marine',
  desc='Beneteau Swift Trawler 34 de 2015 con flybridge y un Cummins de 425 cv diésel (unas 2.800 h). Dos camarotes y baño con ducha. En Cambrils. 179.990 €.',
  ogtitle='Beneteau Swift Trawler 34 en venta · 179.990 €',
  ldname='Beneteau Swift Trawler 34 (2015)',
  lddesc='Beneteau Swift Trawler 34 de 2015, trawler de motor con flybridge. Un motor Cummins QSB 6.7 de 425 cv, diésel e intraborda, con unas 2.800 horas según el propietario. Eslora de 10,98 m y manga de 3,98 m según el fabricante. Dos camarotes y un baño con ducha separada. En Cambrils (Tarragona). Precio 179.990 €.',
  sub=['2015', '10,98 m de eslora', 'Cummins 425 cv, diésel', 'Cambrils'],
  price='179.990 €',
  pdf='swift-trawler-34.pdf', pdftxt='Descargar ficha completa (PDF)', pdfbtn='Descargar ficha PDF',
  wa='Hola Juan, me interesa la Beneteau Swift Trawler 34 que tenéis en venta. ¿Podemos hablar?',
  wa_visit='Hola Juan, me gustaría ver en persona la Beneteau Swift Trawler 34 de vuestra web. ¿Qué días se podría?',
  wa_share='Mira este barco: Beneteau Swift Trawler 34 — https://www.platamarine.com/barcos/swift-trawler-34',
  alt='Beneteau Swift Trawler 34 con el flybridge y el bimini', photo='foto',
  specs=[('Tipo', 'Trawler de motor con flybridge'), ('Año', '2015'),
         ('Eslora', '10,98 m (dato del fabricante); la de registro se confirma con la documentación'),
         ('Manga', '3,98 m (dato del fabricante)'), ('Calado', 'Aprox. 1,0 m (dato del fabricante)'),
         ('Motor', '1 × Cummins QSB 6.7 de 425 cv, diésel, intraborda'),
         ('Horas', 'Unas 2.800 según el propietario; se confirman con la foto del cuentahoras y la documentación'),
         ('Depósitos', '800 l de combustible y 320 l de agua (dato del fabricante)'),
         ('Capacidad', 'Hasta 11 personas según el fabricante; se confirma con la documentación'),
         ('Camarotes', '2: armador en proa con cama doble e invitados con literas'),
         ('Baños', '1, con ducha separada'),
         ('Puestos de gobierno', 'Interior y en el flybridge, con bimini'),
         ('Electrónica', 'Radar; el resto se confirma con la documentación'),
         ('Titulación', 'PER o superior'), ('ITB', 'Se confirma con la documentación'),
         ('Amarre', 'De alquiler, no se incluye en la venta'),
         ('Ubicación', 'Cambrils (Costa Daurada, Tarragona)'),
         ('Impuestos', TAX['es'])],
  h2='Cómo lo veo',
  paras=[
   'Una Swift Trawler 34 de 2015, el trawler con flybridge de Beneteau. Tiene dos puestos de gobierno, el interior junto al salón y el del flybridge con bimini, y una bañera de popa que se cierra con lona.',
   'Lleva un solo motor, un Cummins QSB 6.7 de 425 cv, diésel e intraborda, con unas 2.800 horas según el propietario. Las horas se confirman con la foto del cuentahoras y con la documentación, y el historial de mantenimiento lo pido al propietario para revisarlo antes de reservar.',
   'Por dentro, según el fabricante, tiene el camarote del armador en proa con cama doble, un camarote de invitados con literas, un baño con ducha separada y un salón con sofá convertible y cocina. En las fotos se ve la madera cálida de todo el interior, el radar y la televisión del camarote.',
   'Está en Cambrils (Costa Daurada, Tarragona), con un amarre de alquiler que no entra en la venta. Con 10,98 m de eslora según el fabricante hace falta el PER o un título superior; la eslora de registro se confirma con la documentación. El precio son 179.990 €. Vende un particular, así que normalmente el comprador paga el ITP de su comunidad; la situación del IVA del barco se confirma con la documentación.',
   'Antes de reservar, yo haría prueba de mar y un peritaje independiente.',
  ],
  equip_h='Equipamiento',
  equip=['Flybridge con bimini', 'Puesto de gobierno interior', 'Radar', 'Cummins QSB 6.7 de 425 cv', 'Lona de bañera', '2 camarotes', 'Baño con ducha separada', 'Televisión en el camarote'],
  card=dict(alt='Beneteau Swift Trawler 34 con el flybridge y el bimini', sub='2015 · 10,98 m · trawler con flybridge · Cummins 425 cv · Cambrils',
            tb='Titulación: PER o superior',
            desc='Trawler con flybridge de 2015, con un Cummins de 425 cv diésel, dos camarotes y baño con ducha separada. En Cambrils, se puede ver con cita previa.',
            ask='Preguntar por WhatsApp', see='Ver ficha'),
  inv='10,98 m · Cummins 425 cv · Cambrils (Tarragona)',
 ),
 'ca': dict(
  title='Beneteau Swift Trawler 34 en venda, 179.990 € · Plata Marine',
  desc="Beneteau Swift Trawler 34 del 2015 amb flybridge i un Cummins de 425 cv dièsel (unes 2.800 h). Dues cabines i bany amb dutxa. A Cambrils. 179.990 €.",
  ogtitle='Beneteau Swift Trawler 34 en venda · 179.990 €',
  ldname='Beneteau Swift Trawler 34 (2015)',
  lddesc="Beneteau Swift Trawler 34 del 2015, trawler de motor amb flybridge. Un motor Cummins QSB 6.7 de 425 cv, dièsel i intrabord, amb unes 2.800 hores segons el propietari. Eslora de 10,98 m i mànega de 3,98 m segons el fabricant. Dues cabines i un bany amb dutxa separada. A Cambrils (Tarragona). Preu 179.990 €.",
  sub=['2015', '10,98 m d’eslora', 'Cummins 425 cv, dièsel', 'Cambrils'],
  price='179.990 €',
  pdf='/barcos/swift-trawler-34-ca.pdf', pdftxt='Descarregar la fitxa completa (PDF)', pdfbtn='Descarregar la fitxa PDF',
  wa="Hola Juan, m'interessa la Beneteau Swift Trawler 34 que teniu en venda. En podem parlar?",
  wa_visit="Hola Juan, m'agradaria veure en persona la Beneteau Swift Trawler 34 del vostre web. Quins dies es podria?",
  wa_share='Mira aquest vaixell: Beneteau Swift Trawler 34 — https://www.platamarine.com/ca/barcos/swift-trawler-34',
  alt='Beneteau Swift Trawler 34 amb el flybridge i el bimini', photo='foto',
  specs=[('Tipus', 'Trawler de motor amb flybridge'), ('Any', '2015'),
         ('Eslora', '10,98 m (dada del fabricant); la de registre es confirma amb la documentació'),
         ('Mànega', '3,98 m (dada del fabricant)'), ('Calat', 'Aprox. 1,0 m (dada del fabricant)'),
         ('Motor', '1 × Cummins QSB 6.7 de 425 cv, dièsel, intrabord'),
         ('Hores', 'Unes 2.800 segons el propietari; es confirmen amb la foto del comptahores i la documentació'),
         ('Dipòsits', "800 l de combustible i 320 l d'aigua (dada del fabricant)"),
         ('Capacitat', 'Fins a 11 persones segons el fabricant; es confirma amb la documentació'),
         ('Cabines', "2: armador a proa amb llit doble i convidats amb lliteres"),
         ('Banys', '1, amb dutxa separada'),
         ('Llocs de govern', 'Interior i al flybridge, amb bimini'),
         ('Electrònica', 'Radar; la resta es confirma amb la documentació'),
         ('Titulació', 'PER o superior'), ('ITB', 'Es confirma amb la documentació'),
         ('Amarrament', "De lloguer, no s'inclou en la venda"),
         ('Ubicació', 'Cambrils (Costa Daurada, Tarragona)'),
         ('Impostos', TAX['ca'])],
  h2='Com ho veig',
  paras=[
   "Una Swift Trawler 34 del 2015, el trawler amb flybridge de Beneteau. Té dos llocs de govern, l'interior al costat del saló i el del flybridge amb bimini, i una banyera de popa que es tanca amb lona.",
   "Porta un sol motor, un Cummins QSB 6.7 de 425 cv, dièsel i intrabord, amb unes 2.800 hores segons el propietari. Les hores es confirmen amb la foto del comptahores i amb la documentació, i l'historial de manteniment el demano al propietari per revisar-lo abans de reservar.",
   "Per dins, segons el fabricant, té la cabina de l'armador a proa amb llit doble, una cabina de convidats amb lliteres, un bany amb dutxa separada i un saló amb sofà convertible i cuina. A les fotos es veu la fusta càlida de tot l'interior, el radar i la televisió de la cabina.",
   "És a Cambrils (Costa Daurada, Tarragona), amb un amarrament de lloguer que no entra en la venda. Amb 10,98 m d'eslora segons el fabricant cal el PER o un títol superior; l'eslora de registre es confirma amb la documentació. El preu és de 179.990 €. Ven un particular, així que normalment el comprador paga l'ITP de la seva comunitat; la situació de l'IVA del vaixell es confirma amb la documentació.",
   'Abans de reservar, jo faria prova de mar i un peritatge independent.',
  ],
  equip_h='Equipament',
  equip=['Flybridge amb bimini', 'Lloc de govern interior', 'Radar', 'Cummins QSB 6.7 de 425 cv', 'Lona de banyera', '2 cabines', 'Bany amb dutxa separada', 'Televisió a la cabina'],
  card=dict(alt='Beneteau Swift Trawler 34 amb el flybridge i el bimini', sub='2015 · 10,98 m · trawler amb flybridge · Cummins 425 cv · Cambrils',
            tb='Titulació: PER o superior',
            desc='Trawler amb flybridge del 2015, amb un Cummins de 425 cv dièsel, dues cabines i bany amb dutxa separada. A Cambrils, es pot veure amb cita prèvia.',
            ask='Preguntar per WhatsApp', see='Veure fitxa'),
  inv='10,98 m · Cummins 425 cv · Cambrils (Tarragona)',
 ),
 'en': dict(
  title='Beneteau Swift Trawler 34 for sale · €179,990 · Plata Marine',
  desc='2015 Beneteau Swift Trawler 34 with flybridge and a Cummins 425 hp diesel (about 2,800 h). Two cabins, bathroom with shower. In Cambrils, Spain. €179,990.',
  ogtitle='Beneteau Swift Trawler 34 for sale · €179,990',
  ldname='Beneteau Swift Trawler 34 (2015)',
  lddesc="2015 Beneteau Swift Trawler 34, motor trawler with flybridge. A single Cummins QSB 6.7 425 hp inboard diesel with about 2,800 hours according to the owner. Length 10.98 m and beam 3.98 m according to the builder. Two cabins and one bathroom with a separate shower. In Cambrils (Tarragona). Price €179,990.",
  sub=['2015', '10.98 m length', 'Cummins 425 hp, diesel', 'Cambrils'],
  price='€179,990',
  pdf='/barcos/swift-trawler-34-en.pdf', pdftxt='Download the full listing (PDF)', pdfbtn='Download PDF listing',
  wa="Hi Juan, I'm interested in the Beneteau Swift Trawler 34 you have for sale. Can we talk?",
  wa_visit="Hi Juan, I'd like to see the Beneteau Swift Trawler 34 from your website in person. Which days would work?",
  wa_share='Look at this boat: Beneteau Swift Trawler 34 — https://www.platamarine.com/en/barcos/swift-trawler-34',
  alt='Beneteau Swift Trawler 34 with its flybridge and bimini', photo='photo',
  specs=[('Type', 'Motor trawler with flybridge'), ('Year', '2015'),
         ('Length', '10.98 m (builder); the registered length is confirmed with the papers'),
         ('Beam', '3.98 m (builder)'), ('Draft', 'Approx. 1.0 m (builder)'),
         ('Engine', '1 × Cummins QSB 6.7 425 hp, diesel, inboard'),
         ('Hours', 'About 2,800 according to the owner; confirmed with the photo of the hour meter and the papers'),
         ('Tanks', '800 l fuel and 320 l water (builder)'),
         ('Capacity', 'Up to 11 people according to the builder; confirmed with the papers'),
         ('Cabins', "2: owner's forward with double bed and guest cabin with bunks"),
         ('Bathrooms', '1, with separate shower'),
         ('Helm stations', 'Lower helm and flybridge, with bimini'),
         ('Electronics', 'Radar; the rest is confirmed with the papers'),
         ('Licence', 'Spanish PER or higher'), ('ITB inspection', 'To be confirmed with the papers'),
         ('Berth', 'Rented, not included in the sale'),
         ('Location', 'Cambrils (Costa Daurada, Tarragona)'),
         ('Taxes', TAX['en'])],
  h2='How I see it',
  paras=[
   "A 2015 Swift Trawler 34, Beneteau's flybridge trawler. It has two helm stations, the lower one next to the saloon and the flybridge helm with bimini, and an aft cockpit that closes with canvas.",
   "It has a single engine, a Cummins QSB 6.7 425 hp inboard diesel, with about 2,800 hours according to the owner. The hours are confirmed with the photo of the hour meter and the papers, and I ask the owner for the maintenance history so it can be checked before reserving.",
   "Inside, according to the builder, there is the owner's cabin forward with a double bed, a guest cabin with bunks, a bathroom with a separate shower and a saloon with a convertible sofa and galley. The photos show the warm woodwork throughout, the radar and the TV in the cabin.",
   "It is in Cambrils (Costa Daurada, Tarragona), with a rented berth that is not part of the sale. At 10.98 m according to the builder, you need the Spanish PER licence or higher; the registered length is confirmed with the papers. The price is €179,990. It is a private sale, so the buyer normally pays the transfer tax (ITP) of their region; the boat's VAT status is confirmed with the papers.",
   'Before reserving, I would do a sea trial and an independent survey.',
  ],
  equip_h='Equipment',
  equip=['Flybridge with bimini', 'Lower helm station', 'Radar', 'Cummins QSB 6.7 425 hp', 'Cockpit canvas', '2 cabins', 'Bathroom with separate shower', 'TV in the cabin'],
  card=dict(alt='Beneteau Swift Trawler 34 with its flybridge and bimini', sub='2015 · 10.98 m · flybridge trawler · Cummins 425 hp · Cambrils',
            tb='Licence: PER or higher',
            desc='2015 flybridge trawler with a Cummins 425 hp diesel, two cabins and a bathroom with separate shower. In Cambrils, viewing by appointment.',
            ask='Ask on WhatsApp', see='See listing'),
  inv='10.98 m · Cummins 425 hp · Cambrils (Tarragona)',
 ),
 'fr': dict(
  title='Beneteau Swift Trawler 34 à vendre, 179 990 € · Plata Marine',
  desc="Beneteau Swift Trawler 34 de 2015 avec flybridge et un Cummins de 425 ch diesel (environ 2 800 h). Deux cabines, douche. À Cambrils. 179 990 €.",
  ogtitle='Beneteau Swift Trawler 34 à vendre · 179 990 €',
  ldname='Beneteau Swift Trawler 34 (2015)',
  lddesc="Beneteau Swift Trawler 34 de 2015, trawler à moteur avec flybridge. Un moteur Cummins QSB 6.7 de 425 ch, diesel in-bord, avec environ 2 800 heures selon le propriétaire. Longueur 10,98 m et largeur 3,98 m selon le constructeur. Deux cabines et une salle d'eau avec douche séparée. À Cambrils (Tarragone). Prix 179 990 €.",
  sub=['2015', '10,98 m de longueur', 'Cummins 425 ch, diesel', 'Cambrils'],
  price='179 990 €',
  pdf='/barcos/swift-trawler-34-fr.pdf', pdftxt='Télécharger la fiche complète (PDF)', pdfbtn='Télécharger la fiche PDF (en français)',
  wa="Bonjour Juan, le Beneteau Swift Trawler 34 que vous avez à vendre m'intéresse. Pouvons-nous en parler ?",
  wa_visit="Bonjour Juan, j'aimerais voir sur place le Beneteau Swift Trawler 34 de votre site. Quels jours seraient possibles ?",
  wa_share='Regardez ce bateau : Beneteau Swift Trawler 34 — https://www.platamarine.com/fr/barcos/swift-trawler-34',
  alt='Beneteau Swift Trawler 34 avec son flybridge et son bimini', photo='photo',
  specs=[('Type', 'Trawler à moteur avec flybridge'), ('Année', '2015'),
         ('Longueur', "10,98 m (constructeur) ; la longueur d'immatriculation est confirmée avec les documents"),
         ('Largeur', '3,98 m (constructeur)'), ('Tirant d’eau', 'Env. 1,0 m (constructeur)'),
         ('Moteur', '1 × Cummins QSB 6.7 de 425 ch, diesel, in-bord'),
         ('Heures', 'Environ 2 800 selon le propriétaire ; confirmées avec la photo du compteur et les documents'),
         ('Réservoirs', "800 l de carburant et 320 l d'eau (constructeur)"),
         ('Capacité', "Jusqu'à 11 personnes selon le constructeur ; confirmée avec les documents"),
         ('Cabines', '2 : propriétaire à l’avant avec lit double et cabine invités avec couchettes'),
         ("Salles d'eau", '1, avec douche séparée'),
         ('Postes de pilotage', 'Intérieur et au flybridge, avec bimini'),
         ('Électronique', 'Radar ; le reste est confirmé avec les documents'),
         ('Permis', 'PER espagnol ou supérieur'), ('ITB', 'À confirmer avec les documents'),
         ('Amarrage', 'En location, non inclus dans la vente'),
         ('Emplacement', 'Cambrils (Costa Daurada, Tarragone)'),
         ('Taxes', TAX['fr'])],
  h2='Mon avis',
  paras=[
   "Un Swift Trawler 34 de 2015, le trawler à flybridge de Beneteau. Il a deux postes de pilotage, l'intérieur à côté du carré et celui du flybridge avec bimini, et un cockpit arrière qui se ferme avec un taud.",
   "Il a un seul moteur, un Cummins QSB 6.7 de 425 ch, diesel in-bord, avec environ 2 800 heures selon le propriétaire. Les heures sont confirmées avec la photo du compteur et les documents, et je demande au propriétaire l'historique d'entretien pour le vérifier avant la réservation.",
   "À l'intérieur, selon le constructeur, il y a la cabine du propriétaire à l'avant avec lit double, une cabine invités avec couchettes superposées, une salle d'eau avec douche séparée et un carré avec canapé convertible et cuisine. Les photos montrent les boiseries chaleureuses de tout l'intérieur, le radar et la télévision de la cabine.",
   "Il se trouve à Cambrils (Costa Daurada, Tarragone), avec un amarrage en location qui n'est pas inclus dans la vente. Avec 10,98 m selon le constructeur, il faut le PER espagnol ou un permis supérieur ; la longueur d'immatriculation est confirmée avec les documents. Le prix est de 179 990 €. C'est une vente entre particuliers : l'acheteur paie normalement l'impôt sur les transmissions (ITP) de sa région ; la situation de la TVA du bateau est confirmée avec les documents.",
   "Avant de réserver, je ferais un essai en mer et une expertise indépendante.",
  ],
  equip_h='Équipement',
  equip=['Flybridge avec bimini', 'Poste de pilotage intérieur', 'Radar', 'Cummins QSB 6.7 de 425 ch', 'Taud de cockpit', '2 cabines', "Salle d'eau avec douche séparée", 'Télévision dans la cabine'],
  card=dict(alt='Beneteau Swift Trawler 34 avec son flybridge et son bimini', sub='2015 · 10,98 m · trawler à flybridge · Cummins 425 ch · Cambrils',
            tb='Permis : PER ou supérieur',
            desc="Trawler à flybridge de 2015, avec un Cummins de 425 ch diesel, deux cabines et salle d'eau avec douche séparée. À Cambrils, visite sur rendez-vous.",
            ask='Demander sur WhatsApp', see='Voir la fiche'),
  inv='10,98 m · Cummins 425 ch · Cambrils (Tarragone)',
 ),
}

FORBIDDEN = r'Monterey|monterey|278 SS|GXi|Gelabert|49\.?990|49,990|49 990|lista 7|llista 7|liste 7|FUGIT|Fugit|fugit|fran_|Claude'


def wa(txt):
    return 'https://wa.me/34633742973?text=' + quote(txt, safe='')


def json_s(s):
    return json.dumps(s, ensure_ascii=False)


# ---------- fotos ----------
def natkey(s):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)', s)]


def photo_sources(argv):
    if '--fotos' in argv:
        d = os.path.abspath(argv[argv.index('--fotos') + 1])
        fs = sorted((f for f in os.listdir(d) if f.lower().endswith(('.jpg', '.jpeg'))), key=natkey)
        assert fs, 'No hay JPG en ' + d
        return [os.path.join(d, f) for f in fs]
    return [os.path.join(TEST_DIR, f) for f in TEST_ORDER]


def build_photos(srcs):
    """<slug>-N.jpg (lado mayor 1600 px), <slug>-N-m.jpg (1000 px de ancho) y <slug>-N-t.jpg (480 px), sin EXIF."""
    for i, src in enumerate(srcs, 1):
        im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
        base = os.path.join(ROOT, '%s-%d' % (SLUG, i))
        big = im.copy(); big.thumbnail((W1, W1), Image.LANCZOS)
        big.save(base + '.jpg', 'JPEG', quality=82, optimize=True, progressive=True)
        for suf, w, q in (('-m', 1000, 80), ('-t', 480, 76)):
            r = im.copy(); r.thumbnail((w, 10000), Image.LANCZOS)
            r.save(base + suf + '.jpg', 'JPEG', quality=q, optimize=True, progressive=True)
        print('foto', i, os.path.basename(src), big.size)
    # quitar fotos sobrantes de una tanda anterior con más fotos
    for f in glob.glob(os.path.join(ROOT, SLUG + '-*.jpg')):
        m = re.fullmatch(re.escape(SLUG) + r'-(\d+)(?:-m|-t)?\.jpg', os.path.basename(f))
        if m and int(m.group(1)) > len(srcs):
            os.remove(f); print('borrada', os.path.basename(f))
    return Image.open(os.path.join(ROOT, SLUG + '-1.jpg')).size


# ---------- ficha ----------
def build(lang, n_photos):
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
    imgs = ',\n'.join('    "https://www.platamarine.com/%s-%d.jpg"' % (SLUG, i) for i in range(1, min(n_photos, 6) + 1))
    t = re.sub(r'"image": \[.*?\]', lambda m: '"image": [\n' + imgs + '\n  ]', t, count=1, flags=re.S)
    t = re.sub(r'"name": "Monterey 278 SS \(2011\)"', lambda m: '"name": ' + json_s(d['ldname']), t, count=1)
    t = re.sub(r'"description": ".*?",(\s*)"offers"', lambda m: '"description": ' + json_s(d['lddesc']) + ',' + m.group(1) + '"offers"', t, count=1, flags=re.S)
    t = t.replace('"price": "49990"', '"price": "%d"' % PRICE)
    t = re.sub(r'"brand": \{\s*"@type": "Brand",\s*"name": "Monterey"\s*\},\s*"model": "278 SS"', '"brand": {\n    "@type": "Brand",\n    "name": "Beneteau"\n  },\n  "model": "Swift Trawler 34"', t, count=1)
    t = re.sub(r'<div class="sub">.*?</div>', lambda m: '<div class="sub">' + ''.join('<span>%s</span>' % e(s) for s in d['sub']) + '</div>', t, count=1, flags=re.S)
    t = re.sub(r'<p class="price">[^<]*</p>', lambda m: '<p class="price">%s</p>' % d['price'], t, count=1)
    t = re.sub(r'<a class="pdf-link" href="[^"]*" download>[^<]*</a>', lambda m: '<a class="pdf-link" href="%s" download>%s</a>' % (d['pdf'], e(d['pdftxt'])), t, count=1)
    t = re.sub(r'<a class="btn btn-ghost" href="[^"]*\.pdf" download>[^<]*</a>', lambda m: '<a class="btn btn-ghost" href="%s" download>%s</a>' % (d['pdf'], e(d['pdfbtn'])), t, count=1)
    t = re.sub(r'<img class="main" id="main" [^>]*>', lambda m: '<img class="main" id="main" src="/%s-1.jpg" srcset="/%s-1-m.jpg 1000w, /%s-1.jpg %dw" sizes="(max-width: 1100px) 100vw, 1100px" alt="%s">' % (SLUG, SLUG, SLUG, W1, e(d['alt'], quote=True)), t, count=1)
    thumbs = ''.join('<img src="/%s-%d-t.jpg" data-full="/%s-%d.jpg" alt="%s – %s %d" loading="lazy" data-i="%d"%s>' % (SLUG, i, SLUG, i, NAME, d['photo'], i, i - 1, ' class="on"' if i == 1 else '') for i in range(1, n_photos + 1))
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
    assert len(d['title']) <= 60 and len(d['desc']) <= 155, (lang, len(d['title']), len(d['desc']))
    out = os.path.join(ROOT, pre, 'barcos', SLUG + '.html')
    open(out, 'w', encoding='utf-8').write(t)
    print('ok', out, len(t))


def card(lang, w, h):
    d = D[lang]; c = d['card']; e = html.escape
    return ('      <article data-pm-boat="{s}" class="bcard" data-sold="0" data-tipo="motor" data-titulo="3" data-precio="{pr}" data-zona="cataluna" data-comb="diesel" data-motor="intra" data-anyo="2015" data-i="0.5">\n'
            '        <a class="bimg" href="{s}.html"><img src="/{s}-1-m.jpg" srcset="/{s}-1-m.jpg 1000w, /{s}-1.jpg {w}w" sizes="(max-width: 820px) 100vw, 560px" alt="{alt}" loading="lazy" width="{w}" height="{h}"><span class="status available">{st}</span></a>\n'
            '        <div class="bbody">\n'
            '          <div class="head" style="margin:0 0 6px"><h2><a href="{s}.html">{n}</a></h2><p class="price">{p}</p></div>\n'
            '          <p class="sub" style="margin:0">{sub}</p>\n'
            '          <span class="tbadge">{tb}</span>\n'
            '          <p class="bdesc">{desc}</p>\n'
            '          <div class="bcta"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{ask}</a><a class="btn btn-ghost" href="{s}.html">{see}</a></div>\n'
            '        </div>\n'
            '      </article>\n').format(s=SLUG, w=w, h=h, pr=PRICE, alt=e(c['alt'], quote=True), st={'en': 'Available', 'fr': 'Disponible'}.get(lang, 'Disponible'), n=NAME,
                                       p=d['price'], sub=e(c['sub']), tb=e(c['tb']), desc=e(c['desc']), wa=wa(d['wa']), ask=c['ask'], see=c['see'])


def add_catalog(lang, w, h):
    pre = '' if lang == 'es' else lang + '/'
    p = os.path.join(ROOT, pre, 'barcos', 'index.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'      <article data-pm-boat="%s".*?</article>\n' % SLUG, '', s, flags=re.S)
    anchor = '      <article data-pm-boat="barracuda-8"'
    assert s.count(anchor) == 1
    s = s.replace(anchor, card(lang, w, h) + anchor, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('catálogo', p)


def add_inventory():
    p = os.path.join(ROOT, 'inventario.js')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r"      \{slug: '%s'.*?\}\},\n" % SLUG, '', s, flags=re.S)
    q = lambda x: x.replace("'", "\\'")
    entry = ("      {slug: '%s', name: '%s', year: 2015, kind: 'motor', types: ['fly', 'cabinado'], length: 10.98, price: %d, zone: 'cataluna', area: 'costa-daurada', title: 3, status: 'available',\n"
             "        d: {%s}},\n") % (SLUG, NAME, PRICE, ', '.join("%s: '%s'" % (l, q(D[l]['inv'])) for l in ('es', 'ca', 'en', 'fr')))
    anchor = "      {slug: 'barracuda-8'"
    assert s.count(anchor) == 1
    s = s.replace(anchor, entry + anchor, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('inventario ok')


def add_sitemap():
    p = os.path.join(ROOT, 'sitemap.xml')
    s = open(p, encoding='utf-8').read()
    today = datetime.date.today().isoformat()
    for pre, prio in (('', '0.8'), ('ca/', '0.6'), ('en/', '0.6'), ('fr/', '0.6')):
        loc = 'https://www.platamarine.com/%sbarcos/%s.html' % (pre, SLUG)
        line = '    <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n' % (loc, today, prio)
        s = re.sub(r'    <url><loc>%s</loc>.*?</url>\n' % re.escape(loc), '', s)
        m = re.search(r'    <url><loc>https://www\.platamarine\.com/%sbarcos/barracuda-8\.html</loc>.*?</url>\n' % re.escape(pre), s)
        assert m, pre
        s = s[:m.start()] + line + s[m.start():]
    open(p, 'w', encoding='utf-8').write(s)
    print('sitemap ok')


def pipeline():
    py = sys.executable
    run = lambda args, **kw: subprocess.run(args, cwd=ROOT, check=True, **kw)
    run([py, '_tools/ficha_v2.py', SLUG])
    run([py, '_tools/coste_v2.py'])
    run([py, '_tools/build_pdfs.py', SLUG], env=dict(os.environ, PM_ROOT=ROOT))
    run([py, '_tools/build_search_index.py'])


if __name__ == '__main__':
    srcs = photo_sources(sys.argv)
    w, h = build_photos(srcs)
    for lang in ('es', 'ca', 'en', 'fr'):
        pre = '' if lang == 'es' else lang + '/'
        if not os.path.exists(os.path.join(ROOT, pre, 'barcos', SLUG + '.html')):
            build(lang, len(srcs))
        add_catalog(lang, w, h)
    add_inventory()
    add_sitemap()
    if '--sin-resto' not in sys.argv:
        pipeline()
