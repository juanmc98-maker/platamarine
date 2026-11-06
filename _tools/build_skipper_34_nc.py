"""Genera la ficha de la SKIPPER 34 NC (2023) en ES/CA/EN/FR. Basado en build_swift_trawler_34.py (plantilla Monterey 278 SS).
Prepara las fotos (<slug>-N.jpg, -m.jpg, -t.jpg), añade la tarjeta al catálogo /barcos/ de los 4 idiomas, la entrada de
inventario.js y las 4 URL del sitemap (idempotente). Después: _tools/ficha_v2.py skipper-34-nc, _tools/coste_v2.py,
PM_ROOT=<repo> _tools/build_pdfs.py skipper-34-nc y _tools/build_search_index.py.

Uso: python3 _tools/build_skipper_34_nc.py --fotos /ruta/a/la/carpeta   (JPG numerados; la 1 es la de portada)

Datos: mandato de venta y folleto del vendedor (año, precio, motores, horas, equipo, ubicación, admisión temporal) y
fabricante (eslora, manga, depósitos, plazas). Sin nombre de la embarcación. Vende una sociedad; precio sin IVA
(admisión temporal en la UE hasta abril de 2028 según el vendedor)."""
import re, os, sys, html, json, glob, datetime, subprocess
from urllib.parse import quote
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'skipper-34-nc'
TPL = 'barracuda-8'
TPL_NAME = 'Beneteau Barracuda 8'
NAME = 'SKIPPER 34 NC'
PRICE = 179990
W1 = 1600
TEST_DIR = ''
TEST_ORDER = []

VAT = {'es': 'sin IVA', 'ca': 'sense IVA', 'en': 'excl. VAT', 'fr': 'HT'}

TAX = {
 'es': 'Vende una sociedad. Precio sin IVA: según el vendedor, el barco está en admisión temporal en la UE hasta abril de 2028, así que el IVA no está pagado. Si lo compras para usarlo o matricularlo en la UE, hay que importarlo y pagar el IVA y, en su caso, los derechos de importación. Orientativo: confírmalo con tu gestoría',
 'ca': "Ven una societat. Preu sense IVA: segons el venedor, el vaixell és en admissió temporal a la UE fins a l'abril del 2028, així que l'IVA no està pagat. Si el compres per fer-lo servir o matricular-lo a la UE, cal importar-lo i pagar l'IVA i, si escau, els drets d'importació. Orientatiu: confirma-ho amb la teva gestoria",
 'en': 'Sold by a company. Price excluding VAT: according to the seller, the boat is under temporary admission in the EU until April 2028, so VAT has not been paid. If you buy it to use or register it in the EU, it must be imported and VAT and, where applicable, import duties paid. For guidance only: check with your adviser',
 'fr': "Vendu par une société. Prix hors TVA : selon le vendeur, le bateau est en admission temporaire dans l'UE jusqu'en avril 2028, la TVA n'est donc pas payée. Si vous l'achetez pour l'utiliser ou l'immatriculer dans l'UE, il faut l'importer et payer la TVA et, le cas échéant, les droits d'importation. À titre indicatif : vérifiez avec votre conseiller",
}

D = {
 'es': dict(
  title='SKIPPER 34 NC en venta, 179.990 € · Plata Marine',
  desc='SKIPPER 34 NC de 2023, semirrígida de 9,95 m con 2 Mercury 300 V8 (unas 635 h) y mucho equipo. En Livorno (Italia). 179.990 € sin IVA.',
  ogtitle='SKIPPER 34 NC en venta · 179.990 €',
  ldname='SKIPPER 34 NC (2023)',
  lddesc='SKIPPER 34 NC de 2023, semirrígida con consola central y T-top. Dos motores fueraborda Mercury 300 Pro XS V8 de gasolina con unas 635 horas y el historial de mantenimiento completo, según el vendedor. Eslora de 9,95 m y manga de 2,90 m según el fabricante. Suelo de teca, pantalla Simrad de 12", hélice de proa y equipo de sonido JL Audio. En Livorno (Italia). Precio 179.990 € sin IVA.',
  sub=['2023', '9,95 m de eslora', '2 × Mercury 300 cv', 'Livorno (Italia)'],
  price='179.990 €',
  pdf='/barcos/skipper-34-nc.pdf', pdftxt='Descargar ficha completa (PDF)', pdfbtn='Descargar ficha PDF',
  wa='Hola Juan, me interesa la SKIPPER 34 NC que tenéis en venta. ¿Podemos hablar?',
  wa_visit='Hola Juan, me gustaría ver en persona la SKIPPER 34 NC de vuestra web. ¿Qué días se podría?',
  wa_share='Mira este barco: SKIPPER 34 NC — https://www.platamarine.com/barcos/skipper-34-nc',
  alt='SKIPPER 34 NC negra navegando', photo='foto',
  specs=[('Tipo', 'Semirrígida con consola central y T-top'), ('Año', '2023'),
         ('Eslora', '9,95 m (dato del fabricante); la de registro se confirma con la documentación'),
         ('Manga', '2,90 m (dato del fabricante)'),
         ('Motores', '2 × Mercury 300 Pro XS V8, fueraborda de gasolina'),
         ('Horas', 'Unas 635 según el vendedor, con el historial de mantenimiento completo; se confirman con la documentación'),
         ('Depósitos', '480 l de combustible y 98 l de agua (dato del fabricante)'),
         ('Capacidad', 'Hasta 10 personas según el fabricante; se confirma con la documentación'),
         ('Electrónica', 'Pantalla Simrad de 12", transductor, VHF, cartografía y AIS'),
         ('Equipo', 'Hélice de proa, molinete, cargador de baterías a puerto, nevera en el banco de popa, WC en la consola'),
         ('Acabado', 'Casco negro RAL 9005, tapicería Maglia Blackcave, suelo de teca maciza y salpicadero de carbono'),
         ('Bandera', 'Reino Unido'),
         ('Titulación', 'PER o superior'),
         ('Amarre', 'No se incluye en la venta'),
         ('Ubicación', 'Livorno (Toscana, Italia)'),
         ('Impuestos', TAX['es'])],
  h2='Cómo lo veo',
  paras=[
   'Una SKIPPER 34 NC de 2023, una semirrígida deportiva de casi 10 m con el casco negro y la tapicería también negra. Consola central con T-top y asientos tipo jockey en dos filas, banco de popa y solárium en proa.',
   'Lleva dos Mercury 300 Pro XS V8, fueraborda de gasolina, con unas 635 horas y el historial de mantenimiento completo, según el vendedor. Las horas y el mantenimiento se confirman con la documentación antes de reservar.',
   'Viene muy equipada: suelo de teca maciza, salpicadero de carbono, pantalla Simrad de 12" con VHF, cartografía y AIS, sonido JL Audio con subwoofer, hélice de proa y molinete, nevera en el banco de popa, WC en la consola, ducha de agua dulce, toldo de popa con palos de carbono y fundas.',
   'Está en Livorno (Italia) y la vende una sociedad. El precio, 179.990 €, es sin IVA: según el vendedor está en admisión temporal en la UE hasta abril de 2028, así que si la compras para usarla en la UE hay que importarla y pagar el IVA y, en su caso, los derechos de importación. Con 9,95 m de eslora según el fabricante hace falta el PER o un título superior; la eslora de registro se confirma con la documentación.',
   'Antes de reservar, yo haría prueba de mar y un peritaje independiente.',
  ],
  equip_h='Equipamiento',
  equip=['2 × Mercury 300 Pro XS V8', 'T-top', 'Suelo de teca', 'Simrad 12"', 'VHF y AIS', 'JL Audio', 'Hélice de proa', 'Molinete', 'Nevera', 'WC en consola', 'Toldo de popa'],
  card=dict(alt='SKIPPER 34 NC negra navegando', sub='2023 · 9,95 m · semirrígida · 2 × Mercury 300 cv · Livorno (Italia)',
            tb='Titulación: PER o superior',
            desc='Semirrígida de 2023 con dos Mercury 300 V8 (unas 635 h), T-top, teca y mucho equipo. En Livorno (Italia). Precio sin IVA.',
            ask='Preguntar por WhatsApp', see='Ver ficha'),
  inv='9,95 m · 2 x Mercury 300 cv · Livorno (Italia)',
 ),
 'ca': dict(
  title='SKIPPER 34 NC en venda, 179.990 € · Plata Marine',
  desc="SKIPPER 34 NC del 2023, semirígida de 9,95 m amb 2 Mercury 300 V8 (unes 635 h) i molt d'equip. A Livorno (Itàlia). 179.990 € sense IVA.",
  ogtitle='SKIPPER 34 NC en venda · 179.990 €',
  ldname='SKIPPER 34 NC (2023)',
  lddesc="SKIPPER 34 NC del 2023, semirígida amb consola central i T-top. Dos motors forabord Mercury 300 Pro XS V8 de gasolina amb unes 635 hores i l'historial de manteniment complet, segons el venedor. Eslora de 9,95 m i mànega de 2,90 m segons el fabricant. Terra de teca, pantalla Simrad de 12\", hèlix de proa i equip de so JL Audio. A Livorno (Itàlia). Preu 179.990 € sense IVA.",
  sub=['2023', '9,95 m d’eslora', '2 × Mercury 300 cv', 'Livorno (Itàlia)'],
  price='179.990 €',
  pdf='/barcos/skipper-34-nc-ca.pdf', pdftxt='Descarregar la fitxa completa (PDF)', pdfbtn='Descarregar la fitxa PDF',
  wa="Hola Juan, m'interessa la SKIPPER 34 NC que teniu en venda. En podem parlar?",
  wa_visit="Hola Juan, m'agradaria veure en persona la SKIPPER 34 NC del vostre web. Quins dies es podria?",
  wa_share='Mira aquest vaixell: SKIPPER 34 NC — https://www.platamarine.com/ca/barcos/skipper-34-nc',
  alt='SKIPPER 34 NC negra navegant', photo='foto',
  specs=[('Tipus', 'Semirígida amb consola central i T-top'), ('Any', '2023'),
         ('Eslora', '9,95 m (dada del fabricant); la de registre es confirma amb la documentació'),
         ('Mànega', '2,90 m (dada del fabricant)'),
         ('Motors', '2 × Mercury 300 Pro XS V8, forabord de gasolina'),
         ('Hores', "Unes 635 segons el venedor, amb l'historial de manteniment complet; es confirmen amb la documentació"),
         ('Dipòsits', "480 l de combustible i 98 l d'aigua (dada del fabricant)"),
         ('Capacitat', 'Fins a 10 persones segons el fabricant; es confirma amb la documentació'),
         ('Electrònica', 'Pantalla Simrad de 12", transductor, VHF, cartografia i AIS'),
         ('Equip', 'Hèlix de proa, molinet, carregador de bateries a port, nevera al banc de popa, WC a la consola'),
         ('Acabat', 'Buc negre RAL 9005, tapisseria Maglia Blackcave, terra de teca massissa i tauler de carboni'),
         ('Bandera', 'Regne Unit'),
         ('Titulació', 'PER o superior'),
         ('Amarrament', "No s'inclou en la venda"),
         ('Ubicació', 'Livorno (Toscana, Itàlia)'),
         ('Impostos', TAX['ca'])],
  h2='Com ho veig',
  paras=[
   "Una SKIPPER 34 NC del 2023, una semirígida esportiva de gairebé 10 m amb el buc negre i la tapisseria també negra. Consola central amb T-top i seients tipus jockey en dues files, banc de popa i solàrium a proa.",
   "Porta dos Mercury 300 Pro XS V8, forabord de gasolina, amb unes 635 hores i l'historial de manteniment complet, segons el venedor. Les hores i el manteniment es confirmen amb la documentació abans de reservar.",
   "Ve molt equipada: terra de teca massissa, tauler de carboni, pantalla Simrad de 12\" amb VHF, cartografia i AIS, so JL Audio amb subwoofer, hèlix de proa i molinet, nevera al banc de popa, WC a la consola, dutxa d'aigua dolça, tendal de popa amb pals de carboni i fundes.",
   "És a Livorno (Itàlia) i la ven una societat. El preu, 179.990 €, és sense IVA: segons el venedor és en admissió temporal a la UE fins a l'abril del 2028, així que si la compres per fer-la servir a la UE cal importar-la i pagar l'IVA i, si escau, els drets d'importació. Amb 9,95 m d'eslora segons el fabricant cal el PER o un títol superior; l'eslora de registre es confirma amb la documentació.",
   'Abans de reservar, jo faria prova de mar i un peritatge independent.',
  ],
  equip_h='Equipament',
  equip=['2 × Mercury 300 Pro XS V8', 'T-top', 'Terra de teca', 'Simrad 12"', 'VHF i AIS', 'JL Audio', 'Hèlix de proa', 'Molinet', 'Nevera', 'WC a la consola', 'Tendal de popa'],
  card=dict(alt='SKIPPER 34 NC negra navegant', sub='2023 · 9,95 m · semirígida · 2 × Mercury 300 cv · Livorno (Itàlia)',
            tb='Titulació: PER o superior',
            desc="Semirígida del 2023 amb dos Mercury 300 V8 (unes 635 h), T-top, teca i molt d'equip. A Livorno (Itàlia). Preu sense IVA.",
            ask='Preguntar per WhatsApp', see='Veure fitxa'),
  inv='9,95 m · 2 x Mercury 300 cv · Livorno (Itàlia)',
 ),
 'en': dict(
  title='SKIPPER 34 NC for sale · €179,990 · Plata Marine',
  desc='2023 SKIPPER 34 NC, 9.95 m RIB with twin Mercury 300 V8 (about 635 h) and lots of kit. In Livorno, Italy. €179,990 excluding VAT.',
  ogtitle='SKIPPER 34 NC for sale · €179,990',
  ldname='SKIPPER 34 NC (2023)',
  lddesc='2023 SKIPPER 34 NC, centre-console RIB with T-top. Twin Mercury 300 Pro XS V8 petrol outboards with about 635 hours and full service history, according to the seller. Length 9.95 m and beam 2.90 m according to the builder. Teak flooring, 12" Simrad display, bow thruster and JL Audio sound system. In Livorno, Italy. Price €179,990 excluding VAT.',
  sub=['2023', '9.95 m length', '2 × Mercury 300 hp', 'Livorno (Italy)'],
  price='€179,990',
  pdf='/barcos/skipper-34-nc-en.pdf', pdftxt='Download the full listing (PDF)', pdfbtn='Download PDF listing',
  wa="Hi Juan, I'm interested in the SKIPPER 34 NC you have for sale. Can we talk?",
  wa_visit="Hi Juan, I'd like to see the SKIPPER 34 NC from your website in person. Which days would work?",
  wa_share='Look at this boat: SKIPPER 34 NC — https://www.platamarine.com/en/barcos/skipper-34-nc',
  alt='Black SKIPPER 34 NC under way', photo='photo',
  specs=[('Type', 'Centre-console RIB with T-top'), ('Year', '2023'),
         ('Length', '9.95 m (builder); the registered length is confirmed with the papers'),
         ('Beam', '2.90 m (builder)'),
         ('Engines', '2 × Mercury 300 Pro XS V8, petrol outboards'),
         ('Hours', 'About 635 according to the seller, with full service history; confirmed with the papers'),
         ('Tanks', '480 l fuel and 98 l water (builder)'),
         ('Capacity', 'Up to 10 people according to the builder; confirmed with the papers'),
         ('Electronics', '12" Simrad display, transducer, VHF, charts and AIS'),
         ('Equipment', 'Bow thruster, anchor windlass, shore-power battery charger, fridge in the aft bench, toilet in the console'),
         ('Finish', 'Black RAL 9005 hull, Maglia Blackcave upholstery, solid teak flooring and carbon-fibre dashboard'),
         ('Flag', 'United Kingdom'),
         ('Licence', 'Spanish PER or higher'),
         ('Berth', 'Not included in the sale'),
         ('Location', 'Livorno (Tuscany, Italy)'),
         ('Taxes', TAX['en'])],
  h2='How I see it',
  paras=[
   'A 2023 SKIPPER 34 NC, a sporty RIB of almost 10 m with a black hull and black upholstery. Centre console with T-top and jockey seats in two rows, aft bench and bow sunpad.',
   'It has twin Mercury 300 Pro XS V8 petrol outboards, with about 635 hours and full service history, according to the seller. The hours and maintenance are confirmed with the papers before reserving.',
   'It comes very well equipped: solid teak flooring, carbon-fibre dashboard, 12" Simrad display with VHF, charts and AIS, JL Audio sound with subwoofer, bow thruster and windlass, fridge in the aft bench, toilet in the console, freshwater shower, aft sun cover with carbon poles and covers.',
   'It is in Livorno, Italy, and is sold by a company. The price, €179,990, excludes VAT: according to the seller it is under temporary admission in the EU until April 2028, so if you buy it to use in the EU it must be imported and VAT and, where applicable, import duties paid. At 9.95 m according to the builder, you need the Spanish PER licence or higher; the registered length is confirmed with the papers.',
   'Before reserving, I would do a sea trial and an independent survey.',
  ],
  equip_h='Equipment',
  equip=['2 × Mercury 300 Pro XS V8', 'T-top', 'Teak flooring', 'Simrad 12"', 'VHF and AIS', 'JL Audio', 'Bow thruster', 'Windlass', 'Fridge', 'Toilet in console', 'Aft sun cover'],
  card=dict(alt='Black SKIPPER 34 NC under way', sub='2023 · 9.95 m · RIB · 2 × Mercury 300 hp · Livorno (Italy)',
            tb='Licence: PER or higher',
            desc='2023 RIB with twin Mercury 300 V8 (about 635 h), T-top, teak and lots of kit. In Livorno, Italy. Price excluding VAT.',
            ask='Ask on WhatsApp', see='See listing'),
  inv='9.95 m · twin Mercury 300 hp · Livorno (Italy)',
 ),
 'fr': dict(
  title='SKIPPER 34 NC à vendre, 179 990 € · Plata Marine',
  desc="SKIPPER 34 NC de 2023, semi-rigide de 9,95 m avec 2 Mercury 300 V8 (environ 635 h) et très équipée. À Livourne (Italie). 179 990 € HT.",
  ogtitle='SKIPPER 34 NC à vendre · 179 990 €',
  ldname='SKIPPER 34 NC (2023)',
  lddesc="SKIPPER 34 NC de 2023, semi-rigide à console centrale avec T-top. Deux hors-bord Mercury 300 Pro XS V8 essence avec environ 635 heures et un historique d'entretien complet, selon le vendeur. Longueur 9,95 m et largeur 2,90 m selon le constructeur. Pont en teck, écran Simrad 12\", propulseur d'étrave et système audio JL Audio. À Livourne (Italie). Prix 179 990 € hors TVA.",
  sub=['2023', '9,95 m de longueur', '2 × Mercury 300 ch', 'Livourne (Italie)'],
  price='179 990 €',
  pdf='/barcos/skipper-34-nc-fr.pdf', pdftxt='Télécharger la fiche complète (PDF)', pdfbtn='Télécharger la fiche PDF (en français)',
  wa="Bonjour Juan, le SKIPPER 34 NC que vous avez à vendre m'intéresse. Pouvons-nous en parler ?",
  wa_visit="Bonjour Juan, j'aimerais voir sur place le SKIPPER 34 NC de votre site. Quels jours seraient possibles ?",
  wa_share='Regardez ce bateau : SKIPPER 34 NC — https://www.platamarine.com/fr/barcos/skipper-34-nc',
  alt='SKIPPER 34 NC noir en navigation', photo='photo',
  specs=[('Type', 'Semi-rigide à console centrale avec T-top'), ('Année', '2023'),
         ('Longueur', "9,95 m (constructeur) ; la longueur d'immatriculation est confirmée avec les documents"),
         ('Largeur', '2,90 m (constructeur)'),
         ('Moteurs', '2 × Mercury 300 Pro XS V8, hors-bord essence'),
         ('Heures', "Environ 635 selon le vendeur, avec historique d'entretien complet ; confirmées avec les documents"),
         ('Réservoirs', "480 l de carburant et 98 l d'eau (constructeur)"),
         ('Capacité', "Jusqu'à 10 personnes selon le constructeur ; confirmée avec les documents"),
         ('Électronique', 'Écran Simrad 12", sonde, VHF, cartographie et AIS'),
         ('Équipement', "Propulseur d'étrave, guindeau, chargeur de batteries au quai, réfrigérateur dans la banquette arrière, WC dans la console"),
         ('Finition', 'Coque noire RAL 9005, sellerie Maglia Blackcave, pont en teck massif et tableau de bord en carbone'),
         ('Pavillon', 'Royaume-Uni'),
         ('Permis', 'PER espagnol ou supérieur'),
         ('Amarrage', 'Non inclus dans la vente'),
         ('Emplacement', 'Livourne (Toscane, Italie)'),
         ('Taxes', TAX['fr'])],
  h2='Mon avis',
  paras=[
   "Un SKIPPER 34 NC de 2023, un semi-rigide sportif de près de 10 m avec une coque noire et une sellerie noire elle aussi. Console centrale avec T-top et sièges jockey sur deux rangs, banquette arrière et bain de soleil à l'avant.",
   "Il a deux hors-bord Mercury 300 Pro XS V8 essence, avec environ 635 heures et un historique d'entretien complet, selon le vendeur. Les heures et l'entretien sont confirmés avec les documents avant la réservation.",
   "Il est très bien équipé : pont en teck massif, tableau de bord en carbone, écran Simrad 12\" avec VHF, cartographie et AIS, audio JL Audio avec caisson de basses, propulseur d'étrave et guindeau, réfrigérateur dans la banquette arrière, WC dans la console, douche d'eau douce, taud arrière avec mâts en carbone et housses.",
   "Il se trouve à Livourne (Italie) et il est vendu par une société. Le prix, 179 990 €, est hors TVA : selon le vendeur il est en admission temporaire dans l'UE jusqu'en avril 2028 ; si vous l'achetez pour l'utiliser dans l'UE, il faut l'importer et payer la TVA et, le cas échéant, les droits d'importation. Avec 9,95 m selon le constructeur, il faut le PER espagnol ou un permis supérieur ; la longueur d'immatriculation est confirmée avec les documents.",
   "Avant de réserver, je ferais un essai en mer et une expertise indépendante.",
  ],
  equip_h='Équipement',
  equip=['2 × Mercury 300 Pro XS V8', 'T-top', 'Pont en teck', 'Simrad 12"', 'VHF et AIS', 'JL Audio', "Propulseur d'étrave", 'Guindeau', 'Réfrigérateur', 'WC dans la console', 'Taud arrière'],
  card=dict(alt='SKIPPER 34 NC noir en navigation', sub='2023 · 9,95 m · semi-rigide · 2 × Mercury 300 ch · Livourne (Italie)',
            tb='Permis : PER ou supérieur',
            desc="Semi-rigide de 2023 avec deux Mercury 300 V8 (environ 635 h), T-top, teck et très équipé. À Livourne (Italie). Prix hors TVA.",
            ask='Demander sur WhatsApp', see='Voir la fiche'),
  inv='9,95 m · 2 x Mercury 300 ch · Livourne (Italie)',
 ),
}

FORBIDDEN = r'Monterey|monterey|278 SS|GXi|Gelabert|49\.?990|49,990|49 990|Barracuda|barracuda|57\.990|Beneteau|lista 7|llista 7|liste 7|FUGIT|Fugit|fugit|fran_|Claude|NG TOY|ng-yacht|Barnard'


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
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Barracuda[^"]*(?:hablar|parlar|talk|parler)[^"]*', lambda m: wa(d['wa']), t)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Barracuda[^"]*', lambda m: wa(d['wa_visit']), t)
    t = re.sub(r'https://wa\.me/\?text=[^"]*', lambda m: 'https://wa.me/?text=' + quote(d['wa_share'], safe=''), t)
    t = t.replace(TPL, SLUG)
    imgs = ',\n'.join('    "https://www.platamarine.com/%s-%d.jpg"' % (SLUG, i) for i in range(1, min(n_photos, 6) + 1))
    t = re.sub(r'"image": \[.*?\]', lambda m: '"image": [\n' + imgs + '\n  ]', t, count=1, flags=re.S)
    t = re.sub(r'"name": "Beneteau Barracuda 8 \(2016\)"', lambda m: '"name": ' + json_s(d['ldname']), t, count=1)
    t = re.sub(r'"description": ".*?",(\s*)"offers"', lambda m: '"description": ' + json_s(d['lddesc']) + ',' + m.group(1) + '"offers"', t, count=1, flags=re.S)
    t = t.replace('"price": "57990"', '"price": "%d"' % PRICE)
    t = re.sub(r'"brand": \{\s*"@type": "Brand",\s*"name": "Beneteau"\s*\},\s*"model": "Barracuda 8"', '"brand": {\n    "@type": "Brand",\n    "name": "SKIPPER"\n  },\n  "model": "34 NC"', t, count=1)
    t = re.sub(r'<div class="sub">.*?</div>', lambda m: '<div class="sub">' + ''.join('<span>%s</span>' % e(s) for s in d['sub']) + '</div>', t, count=1, flags=re.S)
    t = re.sub(r'<p class="price">[^<]*(?:<span class="vat[^"]*">[^<]*</span>)?</p>', lambda m: '<p class="price">%s <span class="vat">%s</span></p>' % (d['price'], VAT[lang]), t)
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
    # el bloque v2 de la plantilla lo reescribe _tools/ficha_v2.py; la comprobación final va después del pipeline
    assert len(d['title']) <= 60 and len(d['desc']) <= 155, (lang, len(d['title']), len(d['desc']))
    out = os.path.join(ROOT, pre, 'barcos', SLUG + '.html')
    open(out, 'w', encoding='utf-8').write(t)
    print('ok', out, len(t))


def card(lang, w, h):
    d = D[lang]; c = d['card']; e = html.escape
    return ('      <article data-pm-boat="{s}" class="bcard" data-sold="0" data-tipo="motor" data-titulo="3" data-precio="{pr}" data-zona="extranjero" data-comb="gasolina" data-motor="fuera" data-anyo="2023" data-i="0.5">\n'
            '        <a class="bimg" href="{s}.html"><img src="/{s}-1-m.jpg" srcset="/{s}-1-m.jpg 1000w, /{s}-1.jpg {w}w" sizes="(max-width: 820px) 100vw, 560px" alt="{alt}" loading="lazy" width="{w}" height="{h}"><span class="status available">{st}</span></a>\n'
            '        <div class="bbody">\n'
            '          <div class="head" style="margin:0 0 6px"><h2><a href="{s}.html">{n}</a></h2><p class="price">{p} <span class="vat">{vat}</span></p></div>\n'
            '          <p class="sub" style="margin:0">{sub}</p>\n'
            '          <span class="tbadge">{tb}</span>\n'
            '          <p class="bdesc">{desc}</p>\n'
            '          <div class="bcta"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{ask}</a><a class="btn btn-ghost" href="{s}.html">{see}</a></div>\n'
            '        </div>\n'
            '      </article>\n').format(s=SLUG, w=w, h=h, pr=PRICE, alt=e(c['alt'], quote=True), st={'en': 'Available', 'fr': 'Disponible'}.get(lang, 'Disponible'), n=NAME,
                                       p=d['price'], vat=VAT[lang], sub=e(c['sub']), tb=e(c['tb']), desc=e(c['desc']), wa=wa(d['wa']), ask=c['ask'], see=c['see'])


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
    entry = ("      {slug: '%s', name: '%s', year: 2023, kind: 'motor', types: ['rib'], length: 9.95, price: %d, vat: true, zone: 'extranjero', area: 'italia', title: 3, status: 'available',\n"
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
        loc = 'https://www.platamarine.com/%sbarcos/%s' % (pre, SLUG)
        line = '    <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n' % (loc, today, prio)
        s = re.sub(r'    <url><loc>%s</loc>.*?</url>\n' % re.escape(loc), '', s)
        m = re.search(r'    <url><loc>https://www\.platamarine\.com/%sbarcos/barracuda-8</loc>.*?</url>\n' % re.escape(pre), s)
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
    for lang in ('es', 'ca', 'en', 'fr'):
        pre = '' if lang == 'es' else lang + '/'
        t = open(os.path.join(ROOT, pre, 'barcos', SLUG + '.html'), encoding='utf-8').read()
        left = re.findall(r'.{30}(?:%s).{30}' % FORBIDDEN, t)
        print(lang, 'restos de la plantilla:', left[:5])
