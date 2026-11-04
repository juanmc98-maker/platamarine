"""Genera la ficha del Mascot 33 (1988) en ES/CA/EN/FR. Basado en build_swift_trawler_34.py.
Parte de la ficha de la Beneteau Barracuda 8 como plantilla (ficha clásica que después pasa a v2), prepara las fotos
(<slug>-N.jpg, -m.jpg, -t.jpg), añade la tarjeta al catálogo /barcos/ de los 4 idiomas, la entrada de inventario.js
y las 4 URL del sitemap (todo idempotente).
Después lanza el resto: _tools/ficha_v2.py mascot-33 (datos en _tools/ficha_v2_boats/mascot_33.py, con la estructura
de los veleros: cubierta, navegar, interior), PM_ROOT=<repo> _tools/build_pdfs.py mascot-33,
_tools/build_search_index.py y _tools/clean_urls.py.
Los bloques "Barcos parecidos" y las listas de /comprar/ se refrescan en el navegador desde inventario.js.

Uso: python3 _tools/build_mascot_33.py            (fotos de SRC_DIR en el orden de ORDER; la 1 es portada y tarjeta)
     python3 _tools/build_mascot_33.py --fotos /ruta/a/la/carpeta   (JPG numerados ya en el orden de la galería)
Al cambiar las fotos, revisar PH y SPOTS_XY en _tools/ficha_v2_boats/mascot_33.py.

Datos: hoja de encargo del 4 nov 2026 (modelo, año, motor Volvo Penta MD31A de 90 cv, 719 h desde 2023 según el
propietario, depósito de gasoil nuevo de 2023 de 85 l con el original anulado, equipamiento del Anexo I, amarre de
alquiler que no se transmite, precio 46.990 € IVA incluido). Vende una sociedad: precio con IVA incluido y factura con IVA.
Eslora, manga y calado: datos de la serie Mascot 33; la eslora de registro se confirma con la documentación.
Sin nombre de la embarcación, puerto exacto ni propietario (solo "Barcelona"). Las cargas del Anexo I no se publican."""
import re, os, sys, html, json, glob, datetime, subprocess
from urllib.parse import quote
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'mascot-33'
TPL = 'barracuda-8'
TPL_NAME = 'Beneteau Barracuda 8'
NAME = 'Mascot 33'
PRICE = 46990
W1 = 1600

SRC_DIR = '/mnt/user-data/uploads/Downloads'
ORDER = [2, 1, 3, 16, 17, 4, 5, 6, 7, 8, 18, 10, 11, 12, 13, 14, 15, 9]
# La portada (fondeado en una cala) es vertical: se recorta en horizontal para la tarjeta, la cabecera y las redes
COVER_CROP = (0, 430, 1086, 1245)

TAX = {
 'es': 'IVA incluido en el precio (vende una sociedad, con factura con IVA). El desglose se confirma con la documentación antes de reservar',
 'ca': "IVA inclòs en el preu (ven una societat, amb factura amb IVA). El desglossament es confirma amb la documentació abans de reservar",
 'en': 'VAT included in the price (sold by a company, with a VAT invoice). The breakdown is confirmed from the documentation before you reserve',
 'fr': "TVA incluse dans le prix (vendu par une société, avec facture avec TVA). Le détail est confirmé avec les documents avant la réservation",
}
VAT = {'es': 'IVA incluido', 'ca': 'IVA inclòs', 'en': 'VAT included', 'fr': 'TVA incluse'}

D = {
 'es': dict(
  title='Mascot 33 en venta · 46.990 € · Plata Marine',
  desc='Velero Mascot 33 de 1988 con timonera, Volvo Penta de 90 cv, radar, piloto automático, hélice de proa y calefacción. En Barcelona. 46.990 € IVA incl.',
  ogtitle='Mascot 33 en venta · 46.990 € IVA incluido',
  ldname='Mascot 33 (1988)',
  lddesc='Velero Mascot 33 de 1988, de crucero, con timonera y puesto de gobierno interior. Motor diésel Volvo Penta MD31A de 90 cv con 719 horas desde 2023 según el propietario. Radar, plotter, VHF, piloto automático, instrumentos de viento, hélice de proa, molinete eléctrico, calefacción, inversor y auxiliar con fueraborda. Eslora de 9,95 m según los datos de la serie. En Barcelona. Precio 46.990 €, IVA incluido.',
  sub=['1988', '9,95 m de eslora', 'Volvo Penta 90 cv', 'Barcelona'],
  price='46.990 €',
  pdf='mascot-33.pdf', pdftxt='Descargar ficha completa (PDF)', pdfbtn='Descargar ficha PDF',
  wa='Hola Juan, me interesa el Mascot 33 que tenéis en venta. ¿Podemos hablar?',
  wa_visit='Hola Juan, me gustaría ver en persona el Mascot 33 de vuestra web. ¿Qué días se podría?',
  wa_share='Mira este barco: Mascot 33 — https://www.platamarine.com/barcos/mascot-33',
  alt='Velero Mascot 33 fondeado en una cala de agua turquesa', photo='foto',
  specs=[('Tipo', 'Velero de crucero con timonera y puesto de gobierno interior'), ('Año', '1988'),
         ('Eslora', '9,95 m (dato de la serie); la de registro se confirma con la documentación'),
         ('Manga', '3,40 m (dato de la serie)'), ('Calado', 'Aprox. 1,50 m (dato de la serie)'),
         ('Motor', '1 × Volvo Penta MD31A, diésel, 90 cv (66 kW)'),
         ('Horas', '719 desde 2023 según el propietario; el historial se confirma con la documentación'),
         ('Depósito', 'Gasoil: depósito nuevo de 2023, de 85 l; el original está anulado (según el propietario)'),
         ('Maniobra', 'Hélice de proa y molinete eléctrico'),
         ('Electrónica', 'Radar, plotter Raymarine, VHF, piloto automático e instrumentos de viento'),
         ('Confort', 'Calefacción e inversor'),
         ('Seguridad', 'Radiobaliza, balsa salvavidas y extintores; equipo de seguridad al día según el propietario'),
         ('Auxiliar', 'Zodiac de fondo rígido (4 personas) con fueraborda Yamaha de 4 cv'),
         ('Titulación', 'PER con prácticas de vela o superior'), ('ITB', 'Se confirma con la documentación'),
         ('Amarre', 'De alquiler; no entra en la venta'),
         ('Ubicación', 'Barcelona'),
         ('Impuestos', TAX['es'])],
  h2='Cómo lo veo',
  paras=[
   'Un Mascot 33 de 1988, un velero de crucero con timonera: el puesto de gobierno, con rueda, está dentro y a cubierto, algo que se agradece en invierno y en los días de viento. Por las fotos, la madera del interior se ve cuidada.',
   'Lleva un motor diésel Volvo Penta MD31A de 90 cv, con 719 horas desde 2023 según el propietario. El historial de mantenimiento se confirma con la documentación, que pido al propietario para revisarla antes de reservar. El depósito de gasoil original está anulado y lleva uno nuevo de 2023, de 85 litros, según el propietario.',
   'Está bien equipado para salir a navegar: radar, plotter Raymarine, VHF, piloto automático, instrumentos de viento, hélice de proa y molinete eléctrico. Tiene también calefacción e inversor, y según el propietario el equipo de seguridad está al día, con radiobaliza y balsa salvavidas. Se vende con una auxiliar Zodiac de fondo rígido para 4 personas y su fueraborda Yamaha de 4 cv.',
   'Está en Barcelona; el amarre es de alquiler y no entra en la venta. Con 9,95 m de eslora según los datos de la serie hace falta el PER con prácticas de vela o un título superior; la eslora de registro se confirma con la documentación. El precio son 46.990 €, IVA incluido: vende una sociedad, con factura con IVA.',
   'Antes de reservar, yo haría prueba de mar y un peritaje independiente.',
  ],
  equip_h='Equipamiento',
  equip=['Gobierno interior', 'Volvo Penta 90 cv', 'Radar', 'Plotter Raymarine', 'VHF', 'Piloto automático', 'Instrumentos de viento', 'Hélice de proa', 'Molinete eléctrico', 'Calefacción', 'Inversor', 'Radiobaliza', 'Balsa salvavidas', 'Auxiliar con fueraborda'],
  card=dict(alt='Velero Mascot 33 fondeado en una cala de agua turquesa', sub='1988 · 9,95 m · velero con timonera · Volvo Penta 90 cv · Barcelona',
            tb='Titulación: PER con prácticas de vela o superior',
            desc='Velero de crucero de 1988 con gobierno interior, radar, piloto automático, hélice de proa, calefacción y auxiliar con fueraborda. En Barcelona, se puede ver con cita previa.',
            ask='Preguntar por WhatsApp', see='Ver ficha'),
  inv='9,95 m · Volvo Penta MD31A 90 cv · Barcelona',
 ),
 'ca': dict(
  title='Mascot 33 en venda · 46.990 € · Plata Marine',
  desc="Veler Mascot 33 del 1988 amb timonera, Volvo Penta de 90 cv, radar, pilot automàtic, hèlix de proa i calefacció. A Barcelona. 46.990 € IVA inclòs.",
  ogtitle='Mascot 33 en venda · 46.990 € IVA inclòs',
  ldname='Mascot 33 (1988)',
  lddesc="Veler Mascot 33 del 1988, de creuer, amb timonera i lloc de govern interior. Motor dièsel Volvo Penta MD31A de 90 cv amb 719 hores des del 2023 segons el propietari. Radar, plotter, VHF, pilot automàtic, instruments de vent, hèlix de proa, molinet elèctric, calefacció, inversor i auxiliar amb forabord. Eslora de 9,95 m segons les dades de la sèrie. A Barcelona. Preu 46.990 €, IVA inclòs.",
  sub=['1988', '9,95 m d’eslora', 'Volvo Penta 90 cv', 'Barcelona'],
  price='46.990 €',
  pdf='/barcos/mascot-33-ca.pdf', pdftxt='Descarregar la fitxa completa (PDF)', pdfbtn='Descarregar la fitxa PDF',
  wa="Hola Juan, m'interessa el Mascot 33 que teniu en venda. En podem parlar?",
  wa_visit="Hola Juan, m'agradaria veure en persona el Mascot 33 del vostre web. Quins dies es podria?",
  wa_share="Mira aquest vaixell: Mascot 33 — https://www.platamarine.com/ca/barcos/mascot-33",
  alt="Veler Mascot 33 fondejat en una cala d'aigua turquesa", photo='foto',
  specs=[('Tipus', 'Veler de creuer amb timonera i lloc de govern interior'), ('Any', '1988'),
         ('Eslora', '9,95 m (dada de la sèrie); la de registre es confirma amb la documentació'),
         ('Mànega', '3,40 m (dada de la sèrie)'), ('Calat', 'Aprox. 1,50 m (dada de la sèrie)'),
         ('Motor', '1 × Volvo Penta MD31A, dièsel, 90 cv (66 kW)'),
         ('Hores', "719 des del 2023 segons el propietari; l'historial es confirma amb la documentació"),
         ('Dipòsit', "Gasoil: dipòsit nou del 2023, de 85 l; l'original està anul·lat (segons el propietari)"),
         ('Maniobra', 'Hèlix de proa i molinet elèctric'),
         ('Electrònica', 'Radar, plotter Raymarine, VHF, pilot automàtic i instruments de vent'),
         ('Confort', 'Calefacció i inversor'),
         ('Seguretat', 'Radiobalisa, bot salvavides i extintors; equip de seguretat al dia segons el propietari'),
         ('Auxiliar', 'Zodiac de fons rígid (4 persones) amb forabord Yamaha de 4 cv'),
         ('Titulació', 'PER amb pràctiques de vela o superior'), ('ITB', 'Es confirma amb la documentació'),
         ('Amarrament', 'De lloguer; no entra en la venda'),
         ('Ubicació', 'Barcelona'),
         ('Impostos', TAX['ca'])],
  h2='Com ho veig',
  paras=[
   "Un Mascot 33 del 1988, un veler de creuer amb timonera: el lloc de govern, amb roda, és a dins i a cobert, cosa que s'agraeix a l'hivern i els dies de vent. Per les fotos, la fusta de l'interior es veu cuidada.",
   "Porta un motor dièsel Volvo Penta MD31A de 90 cv, amb 719 hores des del 2023 segons el propietari. L'historial de manteniment es confirma amb la documentació, que demano al propietari per revisar-la abans de reservar. El dipòsit de gasoil original està anul·lat i en porta un de nou del 2023, de 85 litres, segons el propietari.",
   "Està ben equipat per sortir a navegar: radar, plotter Raymarine, VHF, pilot automàtic, instruments de vent, hèlix de proa i molinet elèctric. També té calefacció i inversor, i segons el propietari l'equip de seguretat està al dia, amb radiobalisa i bot salvavides. Es ven amb una auxiliar Zodiac de fons rígid per a 4 persones i el seu forabord Yamaha de 4 cv.",
   "És a Barcelona; l'amarrament és de lloguer i no entra en la venda. Amb 9,95 m d'eslora segons les dades de la sèrie cal el PER amb pràctiques de vela o un títol superior; l'eslora de registre es confirma amb la documentació. El preu és de 46.990 €, IVA inclòs: ven una societat, amb factura amb IVA.",
   'Abans de reservar, jo faria prova de mar i un peritatge independent.',
  ],
  equip_h='Equipament',
  equip=['Govern interior', 'Volvo Penta 90 cv', 'Radar', 'Plotter Raymarine', 'VHF', 'Pilot automàtic', 'Instruments de vent', 'Hèlix de proa', 'Molinet elèctric', 'Calefacció', 'Inversor', 'Radiobalisa', 'Bot salvavides', 'Auxiliar amb forabord'],
  card=dict(alt="Veler Mascot 33 fondejat en una cala d'aigua turquesa", sub='1988 · 9,95 m · veler amb timonera · Volvo Penta 90 cv · Barcelona',
            tb='Titulació: PER amb pràctiques de vela o superior',
            desc='Veler de creuer del 1988 amb govern interior, radar, pilot automàtic, hèlix de proa, calefacció i auxiliar amb forabord. A Barcelona, es pot veure amb cita prèvia.',
            ask='Preguntar per WhatsApp', see='Veure fitxa'),
  inv='9,95 m · Volvo Penta MD31A 90 cv · Barcelona',
 ),
 'en': dict(
  title='Mascot 33 for sale · €46,990 · Plata Marine',
  desc='1988 Mascot 33 sailboat with wheelhouse, 90 hp Volvo Penta, radar, autopilot, bow thruster and heating. In Barcelona, Spain. €46,990 VAT included.',
  ogtitle='Mascot 33 for sale · €46,990 VAT included',
  ldname='Mascot 33 (1988)',
  lddesc="1988 Mascot 33 cruising sailboat with a wheelhouse and inside steering. Volvo Penta MD31A 90 hp diesel with 719 hours since 2023 according to the owner. Radar, chartplotter, VHF, autopilot, wind instruments, bow thruster, electric windlass, heating, inverter and a tender with outboard. Length 9.95 m according to the class data. In Barcelona. Price €46,990, VAT included.",
  sub=['1988', '9.95 m length', 'Volvo Penta 90 hp', 'Barcelona'],
  price='€46,990',
  pdf='/barcos/mascot-33-en.pdf', pdftxt='Download the full listing (PDF)', pdfbtn='Download PDF listing',
  wa="Hi Juan, I'm interested in the Mascot 33 you have for sale. Can we talk?",
  wa_visit="Hi Juan, I'd like to see the Mascot 33 from your website in person. Which days would work?",
  wa_share='Look at this boat: Mascot 33 — https://www.platamarine.com/en/barcos/mascot-33',
  alt='Mascot 33 sailboat at anchor in a cove with turquoise water', photo='photo',
  specs=[('Type', 'Cruising sailboat with wheelhouse and inside steering'), ('Year', '1988'),
         ('Length', '9.95 m (class data); the registered length is confirmed with the papers'),
         ('Beam', '3.40 m (class data)'), ('Draft', 'Approx. 1.50 m (class data)'),
         ('Engine', '1 × Volvo Penta MD31A, diesel, 90 hp (66 kW)'),
         ('Hours', '719 since 2023 according to the owner; the history is confirmed with the papers'),
         ('Tank', 'Diesel: new 85 l tank from 2023; the original one is disconnected (according to the owner)'),
         ('Manoeuvring', 'Bow thruster and electric windlass'),
         ('Electronics', 'Radar, Raymarine chartplotter, VHF, autopilot and wind instruments'),
         ('Comfort', 'Heating and inverter'),
         ('Safety', 'EPIRB, liferaft and extinguishers; safety gear up to date according to the owner'),
         ('Tender', 'Rigid-floor Zodiac (4 people) with a 4 hp Yamaha outboard'),
         ('Licence', 'PER with sailing practice or higher'), ('ITB inspection', 'To be confirmed with the papers'),
         ('Berth', 'Rented; not included in the sale'),
         ('Location', 'Barcelona'),
         ('Taxes', TAX['en'])],
  h2='How I see it',
  paras=[
   "A 1988 Mascot 33, a cruising sailboat with a wheelhouse: the wheel steering position is inside and under cover, which you appreciate in winter and on windy days. From the photos, the interior woodwork looks well kept.",
   "It has a Volvo Penta MD31A 90 hp diesel with 719 hours since 2023 according to the owner. The maintenance history is confirmed with the papers, which I ask the owner for so they can be checked before reserving. The original diesel tank is disconnected and a new 85-litre tank was fitted in 2023, according to the owner.",
   "It is well equipped for sailing: radar, Raymarine chartplotter, VHF, autopilot, wind instruments, bow thruster and electric windlass. It also has heating and an inverter, and according to the owner the safety gear is up to date, with an EPIRB and a liferaft. It comes with a rigid-floor Zodiac tender for 4 people and its 4 hp Yamaha outboard.",
   "It is in Barcelona; the berth is rented and is not included in the sale. At 9.95 m according to the class data, you need the Spanish PER with sailing practice or a higher licence; the registered length is confirmed with the papers. The price is €46,990, VAT included: it is sold by a company, with a VAT invoice.",
   'Before reserving, I would do a sea trial and an independent survey.',
  ],
  equip_h='Equipment',
  equip=['Inside steering', 'Volvo Penta 90 hp', 'Radar', 'Raymarine chartplotter', 'VHF', 'Autopilot', 'Wind instruments', 'Bow thruster', 'Electric windlass', 'Heating', 'Inverter', 'EPIRB', 'Liferaft', 'Tender with outboard'],
  card=dict(alt='Mascot 33 sailboat at anchor in a cove with turquoise water', sub='1988 · 9.95 m · sailboat with wheelhouse · Volvo Penta 90 hp · Barcelona',
            tb='Licence: PER with sailing practice or higher',
            desc='1988 cruising sailboat with inside steering, radar, autopilot, bow thruster, heating and a tender with outboard. In Barcelona, viewing by appointment.',
            ask='Ask on WhatsApp', see='See listing'),
  inv='9.95 m · Volvo Penta MD31A 90 hp · Barcelona',
 ),
 'fr': dict(
  title='Mascot 33 à vendre · 46 990 € · Plata Marine',
  desc="Voilier Mascot 33 de 1988 avec timonerie, Volvo Penta 90 ch, radar, pilote automatique, propulseur d'étrave et chauffage. Barcelone. 46 990 € TTC.",
  ogtitle='Mascot 33 à vendre · 46 990 € TVA incluse',
  ldname='Mascot 33 (1988)',
  lddesc="Voilier de croisière Mascot 33 de 1988, avec timonerie et poste de barre intérieur. Moteur diesel Volvo Penta MD31A de 90 ch avec 719 heures depuis 2023 selon le propriétaire. Radar, traceur, VHF, pilote automatique, instruments de vent, propulseur d'étrave, guindeau électrique, chauffage, convertisseur et annexe avec hors-bord. Longueur 9,95 m selon les données de la série. À Barcelone. Prix 46 990 €, TVA incluse.",
  sub=['1988', '9,95 m de longueur', 'Volvo Penta 90 ch', 'Barcelone'],
  price='46 990 €',
  pdf='/barcos/mascot-33-fr.pdf', pdftxt='Télécharger la fiche complète (PDF)', pdfbtn='Télécharger la fiche PDF (en français)',
  wa="Bonjour Juan, le Mascot 33 que vous avez à vendre m'intéresse. Pouvons-nous en parler ?",
  wa_visit="Bonjour Juan, j'aimerais voir sur place le Mascot 33 de votre site. Quels jours seraient possibles ?",
  wa_share='Regardez ce bateau : Mascot 33 — https://www.platamarine.com/fr/barcos/mascot-33',
  alt="Voilier Mascot 33 au mouillage dans une crique à l'eau turquoise", photo='photo',
  specs=[('Type', 'Voilier de croisière avec timonerie et poste de barre intérieur'), ('Année', '1988'),
         ('Longueur', "9,95 m (données de la série) ; la longueur d'immatriculation est confirmée avec les documents"),
         ('Largeur', '3,40 m (données de la série)'), ('Tirant d’eau', 'Env. 1,50 m (données de la série)'),
         ('Moteur', '1 × Volvo Penta MD31A, diesel, 90 ch (66 kW)'),
         ('Heures', "719 depuis 2023 selon le propriétaire ; l'historique est confirmé avec les documents"),
         ('Réservoir', "Gazole : réservoir neuf de 2023, de 85 l ; l'original est condamné (selon le propriétaire)"),
         ('Manœuvre', "Propulseur d'étrave et guindeau électrique"),
         ('Électronique', 'Radar, traceur Raymarine, VHF, pilote automatique et instruments de vent'),
         ('Confort', 'Chauffage et convertisseur'),
         ('Sécurité', 'Balise de détresse, radeau de survie et extincteurs ; armement de sécurité à jour selon le propriétaire'),
         ('Annexe', 'Zodiac à fond rigide (4 personnes) avec hors-bord Yamaha de 4 ch'),
         ('Permis', 'PER avec pratiques de voile ou supérieur'), ('ITB', 'À confirmer avec les documents'),
         ('Amarrage', 'En location ; non inclus dans la vente'),
         ('Emplacement', 'Barcelone'),
         ('Taxes', TAX['fr'])],
  h2='Mon avis',
  paras=[
   "Un Mascot 33 de 1988, un voilier de croisière avec timonerie : le poste de barre, à roue, est à l'intérieur et à l'abri, ce qui est appréciable en hiver et les jours de vent. Sur les photos, les boiseries intérieures paraissent bien entretenues.",
   "Il a un moteur diesel Volvo Penta MD31A de 90 ch, avec 719 heures depuis 2023 selon le propriétaire. L'historique d'entretien est confirmé avec les documents, que je demande au propriétaire pour les vérifier avant la réservation. Le réservoir de gazole d'origine est condamné et un réservoir neuf de 85 litres a été installé en 2023, selon le propriétaire.",
   "Il est bien équipé pour naviguer : radar, traceur Raymarine, VHF, pilote automatique, instruments de vent, propulseur d'étrave et guindeau électrique. Il a aussi le chauffage et un convertisseur, et selon le propriétaire l'armement de sécurité est à jour, avec balise de détresse et radeau de survie. Il est vendu avec une annexe Zodiac à fond rigide pour 4 personnes et son hors-bord Yamaha de 4 ch.",
   "Il se trouve à Barcelone ; la place de port est en location et n'est pas incluse dans la vente. Avec 9,95 m selon les données de la série, il faut le PER espagnol avec pratiques de voile ou un permis supérieur ; la longueur d'immatriculation est confirmée avec les documents. Le prix est de 46 990 €, TVA incluse : il est vendu par une société, avec facture avec TVA.",
   "Avant de réserver, je ferais un essai en mer et une expertise indépendante.",
  ],
  equip_h='Équipement',
  equip=['Barre intérieure', 'Volvo Penta 90 ch', 'Radar', 'Traceur Raymarine', 'VHF', 'Pilote automatique', 'Instruments de vent', "Propulseur d'étrave", 'Guindeau électrique', 'Chauffage', 'Convertisseur', 'Balise de détresse', 'Radeau de survie', 'Annexe avec hors-bord'],
  card=dict(alt="Voilier Mascot 33 au mouillage dans une crique à l'eau turquoise", sub='1988 · 9,95 m · voilier avec timonerie · Volvo Penta 90 ch · Barcelone',
            tb='Permis : PER avec pratiques de voile ou supérieur',
            desc="Voilier de croisière de 1988 avec barre intérieure, radar, pilote automatique, propulseur d'étrave, chauffage et annexe avec hors-bord. À Barcelone, visite sur rendez-vous.",
            ask='Demander sur WhatsApp', see='Voir la fiche'),
  inv='9,95 m · Volvo Penta MD31A 90 ch · Barcelone',
 ),
}

FORBIDDEN = r'Barracuda|barracuda|Suzuki|DF150|Lowrance|Furuno|57\.?990|57,990|57 990|Daurada|Vaporetto|Ol[íi]mpic|PETIT|Petit|Curti|BA-1|105522|IVA pagado|IVA pagat|VAT paid|TVA payée'


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
    return [os.path.join(SRC_DIR, 'mascot33-ed-%02d.png' % n) for n in ORDER]


def build_photos(srcs, crop_cover=True):
    """<slug>-N.jpg (lado mayor 1600 px), <slug>-N-m.jpg (1000 px de ancho) y <slug>-N-t.jpg (480 px), sin EXIF."""
    for i, src in enumerate(srcs, 1):
        im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
        if i == 1 and crop_cover and im.height > im.width:
            im = im.crop(COVER_CROP)
        base = os.path.join(ROOT, '%s-%d' % (SLUG, i))
        big = im.copy(); big.thumbnail((W1, W1), Image.LANCZOS)
        big.save(base + '.jpg', 'JPEG', quality=82, optimize=True, progressive=True)
        for suf, w, q in (('-m', 1000, 80), ('-t', 480, 76)):
            r = im.copy(); r.thumbnail((w, 10000), Image.LANCZOS)
            r.save(base + suf + '.jpg', 'JPEG', quality=q, optimize=True, progressive=True)
        print('foto', i, os.path.basename(src), big.size)
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
    t = re.sub(r'"brand": \{\s*"@type": "Brand",\s*"name": "Beneteau"\s*\},\s*"model": "Barracuda 8"', '"brand": {\n    "@type": "Brand",\n    "name": "Mascot"\n  },\n  "model": "33"', t, count=1)
    t = re.sub(r'<div class="sub">.*?</div>', lambda m: '<div class="sub">' + ''.join('<span>%s</span>' % e(s) for s in d['sub']) + '</div>', t, count=1, flags=re.S)
    t = re.sub(r'<p class="price">.*?</p>', lambda m: '<p class="price">%s <span class="vat paid">%s</span></p>' % (d['price'], VAT[lang]), t, count=1)
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
    return ('      <article data-pm-boat="{s}" class="bcard" data-sold="0" data-tipo="vela" data-titulo="3" data-precio="{pr}" data-zona="cataluna" data-comb="diesel" data-motor="intra" data-anyo="1988" data-i="0.4">\n'
            '        <a class="bimg" href="{s}"><img src="/{s}-1-m.jpg" srcset="/{s}-1-m.jpg 1000w, /{s}-1.jpg {w}w" sizes="(max-width: 820px) 100vw, 560px" alt="{alt}" loading="lazy" width="{w}" height="{h}"><span class="status available">{st}</span></a>\n'
            '        <div class="bbody">\n'
            '          <div class="head" style="margin:0 0 6px"><h2><a href="{s}">{n}</a></h2><p class="price">{p} <span class="vat paid">{vat}</span></p></div>\n'
            '          <p class="sub" style="margin:0">{sub}</p>\n'
            '          <span class="tbadge">{tb}</span>\n'
            '          <p class="bdesc">{desc}</p>\n'
            '          <div class="bcta"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{ask}</a><a class="btn btn-ghost" href="{s}">{see}</a></div>\n'
            '        </div>\n'
            '      </article>\n').format(s=SLUG, w=w, h=h, pr=PRICE, alt=e(c['alt'], quote=True), st={'en': 'Available', 'fr': 'Disponible'}.get(lang, 'Disponible'), n=NAME,
                                       p=d['price'], vat=VAT[lang], sub=e(c['sub']), tb=e(c['tb']), desc=e(c['desc']), wa=wa(d['wa']), ask=c['ask'], see=c['see'])


def add_catalog(lang, w, h):
    pre = '' if lang == 'es' else lang + '/'
    p = os.path.join(ROOT, pre, 'barcos', 'index.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'      <article data-pm-boat="%s".*?</article>\n' % SLUG, '', s, flags=re.S)
    anchor = '      <article data-pm-boat="arvor-250"'
    if anchor not in s: anchor = '      <article data-pm-boat="audax-47"'
    assert s.count(anchor) == 1
    s = s.replace(anchor, card(lang, w, h) + anchor, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('catálogo', p)


def add_inventory():
    p = os.path.join(ROOT, 'inventario.js')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r"      \{slug: '%s'.*?\}\},\n" % SLUG, '', s, flags=re.S)
    q = lambda x: x.replace("'", "\\'")
    entry = ("      {slug: '%s', name: '%s', year: 1988, kind: 'vela', types: ['velero'], length: 9.95, price: %d, zone: 'cataluna', area: 'barcelona', title: 3, status: 'available',\n"
             "        d: {%s}},\n") % (SLUG, NAME, PRICE, ', '.join("%s: '%s'" % (l, q(D[l]['inv'])) for l in ('es', 'ca', 'en', 'fr')))
    anchor = "      {slug: 'arvor-250'"
    if anchor not in s: anchor = "      {slug: 'barracuda-8'"
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
        s = re.sub(r'    <url><loc>%s(?:\.html)?</loc>.*?</url>\n' % re.escape(loc), '', s)
        m = (re.search(r'    <url><loc>https://www\.platamarine\.com/%sbarcos/arvor-250(?:\.html)?</loc>.*?</url>\n' % re.escape(pre), s)
             or re.search(r'    <url><loc>https://www\.platamarine\.com/%sbarcos/barracuda-8(?:\.html)?</loc>.*?</url>\n' % re.escape(pre), s))
        assert m, pre
        s = s[:m.start()] + line + s[m.start():]
    open(p, 'w', encoding='utf-8').write(s)
    print('sitemap ok')


def pipeline():
    py = sys.executable
    run = lambda args, **kw: subprocess.run(args, cwd=ROOT, check=True, **kw)
    run([py, '_tools/ficha_v2.py', SLUG])
    run([py, '_tools/build_pdfs.py', SLUG], env=dict(os.environ, PM_ROOT=ROOT))
    run([py, '_tools/build_search_index.py'])
    run([py, '_tools/clean_urls.py'])


if __name__ == '__main__':
    srcs = photo_sources(sys.argv)
    w, h = build_photos(srcs, '--fotos' not in sys.argv)
    for lang in ('es', 'ca', 'en', 'fr'):
        pre = '' if lang == 'es' else lang + '/'
        if not os.path.exists(os.path.join(ROOT, pre, 'barcos', SLUG + '.html')):
            build(lang, len(srcs))
        add_catalog(lang, w, h)
    add_inventory()
    add_sitemap()
    if '--sin-resto' not in sys.argv:
        pipeline()
