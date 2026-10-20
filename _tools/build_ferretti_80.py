"""Genera la ficha del Ferretti 80 (2002, refit 2020) en ES/CA/EN/FR a partir de la ficha del Gallart 10.50 Fly como plantilla,
y añade su tarjeta al catálogo /barcos/ de los 4 idiomas (idempotente).
Uso: python3 _tools/build_ferretti_80.py   (desde cualquier sitio)
Después: python3 _tools/ficha_v2.py ferretti-80 (diseño v2), PM_ROOT=<repo> python3 _tools/build_pdfs.py ferretti-80
y python3 _tools/build_search_index.py. (No hace falta build_similares.js: el bloque de similares se rellena en el navegador.)
Datos: dossier del vendedor (eslora, manga, calado, GT, motores, velocidades, alojamiento, tripulación, bandera, zona, refit).
Lo que el dossier no trae va como "se confirma con la documentación"; al llegar, editar D y regenerar.
No se muestra el nombre de la embarcación ni el puerto exacto (solo "Grecia (Atenas)")."""
import re, os, html, json
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'ferretti-80'
TPL = 'gallart-1050'
TPL_NAME = 'Gallart 10.50 Fly'
NAME = 'Ferretti 80'
N_PHOTOS = 15
W1 = 1369  # ancho real de ferretti-80-1.jpg

D = {
 'es': dict(
  title='Ferretti 80 de 2002 en venta · 769.990 € · Plata Marine',
  desc='Ferretti 80 de 2002 con refit en 2020: 24,38 m, flybridge, 2 x Caterpillar de 1.420 cv, 9 invitados en 4 camarotes. En Grecia (Atenas), 769.990 € con IVA pagado.',
  ogtitle='Ferretti 80 de 2002 en venta · 769.990 €',
  ldname='Ferretti 80 (2002)',
  lddesc='Ferretti 80 de 2002 con refit en 2020: 24,38 m de eslora, 6,10 m de manga, flybridge, dos motores Caterpillar de 1.420 cv, 26 nudos de crucero y 31 de máxima según el dossier, 9 invitados en 4 camarotes y 4 tripulantes. Bandera griega, en Grecia (Atenas). Precio 769.990 € con el IVA pagado.',
  sub=['Año 2002 · refit 2020', '24,38 m de eslora', '2 x Caterpillar 1.420 cv', 'Grecia (Atenas)'],
  price='769.990 €', vat='IVA pagado',
  pdf='ferretti-80.pdf', pdftxt='Descargar ficha completa (PDF)', pdfbtn='Descargar ficha PDF',
  wa='Hola Juan, me interesa el Ferretti 80 de 2002 que tenéis en venta. ¿Podemos hablar?',
  wa_visit='Hola Juan, me gustaría ver en persona el Ferretti 80 (2002) de vuestra web. ¿Qué días se podría?',
  wa_share='Mira este barco: Ferretti 80 — https://www.platamarine.com/barcos/ferretti-80.html',
  alt='Ferretti 80 navegando a buen ritmo, vista de costado', photo='foto',
  specs=[('Año', '2002 · refit en 2020'), ('Tipo', 'Yate a motor con flybridge'),
         ('Eslora', '24,38 m (80 pies, según el dossier)'), ('Manga', '6,10 m'), ('Calado', '1,83 m'), ('Arqueo bruto', '75 GT'),
         ('Casco', 'Fibra de vidrio (GRP)'), ('Motores', '2 x Caterpillar de 1.420 cv, diésel'),
         ('Horas', 'Unas 3.800 h en total (según el vendedor)'), ('Velocidad', '26 nudos de crucero y 31 de máxima (según el dossier)'),
         ('Alojamiento', '9 invitados en 4 camarotes'), ('Tripulación', '4 personas'), ('Baños', '3 (según el vendedor)'),
         ('Refit 2020', 'Trabajos realizados: se confirma con la documentación'),
         ('Depósitos, electrónica y clasificación', 'Se confirma con la documentación'),
         ('Titulación', 'Capitán de Yate o superior (según la eslora de registro; se confirma con la documentación)'),
         ('Bandera', 'Griega'),
         ('Impuestos', 'IVA pagado, según el vendedor; se confirma con la documentación antes de reservar. Si resides en España y lo vas a matricular o usar aquí, consulta el impuesto de matriculación con tu gestoría')],
  h2='Cómo lo veo',
  paras=[
   'Un Ferretti 80 de 2002 con refit en 2020. Son 24,38 m de eslora y 6,10 m de manga, con flybridge, y según el dossier del vendedor aloja a 9 invitados en 4 camarotes y tiene sitio para 4 tripulantes.',
   'Lleva dos motores Caterpillar de 1.420 cv. El dossier habla de 26 nudos de crucero y 31 de máxima, y el vendedor calcula unas 3.800 horas en total. El historial de mantenimiento y el detalle de lo que se hizo en el refit de 2020 se piden al vendedor y se revisan con la documentación antes de reservar.',
   'Por fuera tiene un flybridge amplio con mesa, solárium y puesto de gobierno, un comedor exterior en la bañera de popa y una plataforma de baño. Dentro, el salón con sofá en U y el comedor tienen ventanales grandes, con un interiorismo de Zuccon International Project.',
   'Está en Grecia, en la zona de Atenas, con bandera griega, y se puede ver con cita previa. Con titulación española, por su eslora hace falta el Capitán de Yate o un título superior (depende de la eslora de registro; se confirma con la documentación). El precio son 769.990 € con el IVA pagado.',
  ],
  equip_h='Equipamiento',
  equip=['2 x Caterpillar 1.420 cv', 'Flybridge con mesa y solárium', 'Puesto de gobierno en el flybridge', 'Comedor exterior en la bañera de popa', 'Plataforma de baño multiusos', 'Proyector en la cubierta superior', 'Salón con sofá en U', 'Comedor interior', '4 camarotes para 9 invitados', 'Alojamiento para 4 tripulantes', 'Interiorismo de Zuccon International Project', 'Refit en 2020'],
  card=dict(alt='Ferretti 80 navegando, vista de costado', sub='2002 · 24,38 m · flybridge · 2 x Caterpillar 1.420 cv · Grecia (Atenas)',
            tb='Titulación: Capitán de Yate o superior',
            desc='Ferretti 80 de 2002 con refit en 2020: flybridge, dos Caterpillar de 1.420 cv, 9 invitados en 4 camarotes y 4 tripulantes. Está en Grecia (Atenas) y se puede ver con cita previa.',
            ask='Preguntar por WhatsApp', see='Ver ficha'),
 ),
 'ca': dict(
  title='Ferretti 80 del 2002 en venda · 769.990 € · Plata Marine',
  desc='Ferretti 80 del 2002 amb refit el 2020: 24,38 m, flybridge, 2 x Caterpillar de 1.420 cv, 9 convidats en 4 cabines. A Grècia (Atenes), 769.990 € amb l\'IVA pagat.',
  ogtitle='Ferretti 80 del 2002 en venda · 769.990 €',
  ldname='Ferretti 80 (2002)',
  lddesc='Ferretti 80 del 2002 amb refit el 2020: 24,38 m d\'eslora, 6,10 m de mànega, flybridge, dos motors Caterpillar de 1.420 cv, 26 nusos de creuer i 31 de màxima segons el dossier, 9 convidats en 4 cabines i 4 tripulants. Bandera grega, a Grècia (Atenes). Preu 769.990 € amb l\'IVA pagat.',
  sub=['Any 2002 · refit 2020', '24,38 m d\'eslora', '2 x Caterpillar 1.420 cv', 'Grècia (Atenes)'],
  price='769.990 €', vat='IVA pagat',
  pdf='/barcos/ferretti-80-ca.pdf', pdftxt='Descarregar la fitxa completa (PDF)', pdfbtn='Descarregar fitxa PDF (en català)',
  wa="Hola Juan, m'interessa el Ferretti 80 del 2002 que teniu en venda. Podem parlar?",
  wa_visit="Hola Juan, m'agradaria veure en persona el Ferretti 80 (2002) de la vostra web. Quins dies es podria?",
  wa_share='Mira aquest vaixell: Ferretti 80 — https://www.platamarine.com/ca/barcos/ferretti-80.html',
  alt='Ferretti 80 navegant a bon ritme, vist de costat', photo='foto',
  specs=[('Any', '2002 · refit el 2020'), ('Tipus', 'Iot a motor amb flybridge'),
         ('Eslora', '24,38 m (80 peus, segons el dossier)'), ('Mànega', '6,10 m'), ('Calat', '1,83 m'), ('Arqueig brut', '75 GT'),
         ('Buc', 'Fibra de vidre (GRP)'), ('Motors', '2 x Caterpillar de 1.420 cv, dièsel'),
         ('Hores', 'Unes 3.800 h en total (segons el venedor)'), ('Velocitat', '26 nusos de creuer i 31 de màxima (segons el dossier)'),
         ('Allotjament', '9 convidats en 4 cabines'), ('Tripulació', '4 persones'), ('Banys', '3 (segons el venedor)'),
         ('Refit 2020', 'Treballs fets: es confirma amb la documentació'),
         ('Dipòsits, electrònica i classificació', 'Es confirma amb la documentació'),
         ('Titulació', 'Capità de Iot o superior (segons l\'eslora de registre; es confirma amb la documentació)'),
         ('Bandera', 'Grega'),
         ('Impostos', 'IVA pagat, segons el venedor; es confirma amb la documentació abans de reservar. Si resideixes a Espanya i el matricularàs o el faràs servir aquí, consulta l\'impost de matriculació amb la teva gestoria')],
  h2='Com el veig',
  paras=[
   'Un Ferretti 80 del 2002 amb refit el 2020. Són 24,38 m d\'eslora i 6,10 m de mànega, amb flybridge, i segons el dossier del venedor allotja 9 convidats en 4 cabines i té lloc per a 4 tripulants.',
   'Porta dos motors Caterpillar de 1.420 cv. El dossier parla de 26 nusos de creuer i 31 de màxima, i el venedor calcula unes 3.800 hores en total. L\'historial de manteniment i el detall del que es va fer al refit del 2020 es demanen al venedor i es revisen amb la documentació abans de reservar.',
   'Per fora té un flybridge ampli amb taula, solàrium i lloc de govern, un menjador exterior a la banyera de popa i una plataforma de bany. A dins, el saló amb sofà en U i el menjador tenen finestrals grans, amb un interiorisme de Zuccon International Project.',
   'És a Grècia, a la zona d\'Atenes, amb bandera grega, i es pot veure amb cita prèvia. Amb titulació espanyola, per la seva eslora cal el Capità de Iot o un títol superior (depèn de l\'eslora de registre; es confirma amb la documentació). El preu són 769.990 € amb l\'IVA pagat.',
  ],
  equip_h='Equipament',
  equip=['2 x Caterpillar 1.420 cv', 'Flybridge amb taula i solàrium', 'Lloc de govern al flybridge', 'Menjador exterior a la banyera de popa', 'Plataforma de bany multiús', 'Projector a la coberta superior', 'Saló amb sofà en U', 'Menjador interior', '4 cabines per a 9 convidats', 'Allotjament per a 4 tripulants', 'Interiorisme de Zuccon International Project', 'Refit el 2020'],
  card=dict(alt='Ferretti 80 navegant, vist de costat', sub='2002 · 24,38 m · flybridge · 2 x Caterpillar 1.420 cv · Grècia (Atenes)',
            tb='Titulació: Capità de Iot o superior',
            desc='Ferretti 80 del 2002 amb refit el 2020: flybridge, dos Caterpillar de 1.420 cv, 9 convidats en 4 cabines i 4 tripulants. És a Grècia (Atenes) i es pot veure amb cita prèvia.',
            ask='Preguntar per WhatsApp', see='Veure fitxa'),
 ),
 'en': dict(
  title='2002 Ferretti 80 for sale · €769,990 · Plata Marine',
  desc='2002 Ferretti 80, refitted in 2020: 24.38 m, flybridge, twin 1,420 hp Caterpillars, 9 guests in 4 cabins. In Greece (Athens), €769,990 with VAT paid.',
  ogtitle='2002 Ferretti 80 for sale · €769,990',
  ldname='Ferretti 80 (2002)',
  lddesc='2002 Ferretti 80, refitted in 2020: 24.38 m length, 6.10 m beam, flybridge, twin 1,420 hp Caterpillar engines, 26 knots cruising and 31 maximum according to the brochure, 9 guests in 4 cabins and 4 crew. Greek flag, in Greece (Athens). Price €769,990 with VAT paid.',
  sub=['Year 2002 · refit 2020', '24.38 m length', '2 x Caterpillar 1,420 hp', 'Greece (Athens)'],
  price='€769,990', vat='VAT paid',
  pdf='/barcos/ferretti-80-en.pdf', pdftxt='Download full spec sheet (PDF)', pdfbtn='Download PDF listing (in English)',
  wa="Hi Juan, I'm interested in the 2002 Ferretti 80 you have for sale. Can we talk?",
  wa_visit="Hi Juan, I'd like to see the Ferretti 80 (2002) from your website in person. Which days would work?",
  wa_share='Check out this boat: Ferretti 80 — https://www.platamarine.com/en/barcos/ferretti-80.html',
  alt='Ferretti 80 under way at speed, side view', photo='photo',
  specs=[('Year', '2002 · refitted in 2020'), ('Type', 'Flybridge motor yacht'),
         ('Length', '24.38 m (80 ft, according to the brochure)'), ('Beam', '6.10 m'), ('Draft', '1.83 m'), ('Gross tonnage', '75 GT'),
         ('Hull', 'GRP (glass-reinforced plastic)'), ('Engines', '2 x Caterpillar 1,420 hp, diesel'),
         ('Hours', 'About 3,800 h in total (according to the seller)'), ('Speed', '26 knots cruising, 31 maximum (according to the brochure)'),
         ('Accommodation', '9 guests in 4 cabins'), ('Crew', '4 people'), ('Bathrooms', '3 (according to the seller)'),
         ('2020 refit', 'Work carried out: to be confirmed from the documentation'),
         ('Tanks, electronics and classification', 'To be confirmed from the documentation'),
         ('Licence', 'Spanish Capitán de Yate (Yachtmaster) or higher (depends on the registered length; to be confirmed from the documentation)'),
         ('Flag', 'Greek'),
         ('Taxes', 'VAT paid, according to the seller; confirmed from the documentation before you reserve. If you live in Spain and will register or use it here, check the registration tax with your agent (gestoría)')],
  h2='My take',
  paras=[
   'A 2002 Ferretti 80, refitted in 2020. It measures 24.38 m in length with a 6.10 m beam and has a flybridge; according to the seller\'s brochure it sleeps 9 guests in 4 cabins and has room for 4 crew.',
   'It has twin 1,420 hp Caterpillar engines. The brochure gives 26 knots cruising and 31 maximum, and the seller puts the hours at around 3,800 in total. The maintenance history and the details of the 2020 refit are requested from the seller and checked against the documentation before you reserve.',
   'Outside there is a large flybridge with a table, sunpad and helm station, al fresco dining in the aft cockpit and a bathing platform. Inside, the saloon with its U-shaped sofa and the dining area have large windows, with interior design by Zuccon International Project.',
   'It is in Greece, in the Athens area, under the Greek flag, and can be viewed by appointment. With a Spanish licence, its length calls for the Capitán de Yate or a higher qualification (it depends on the registered length; to be confirmed from the documentation). The price is €769,990 with VAT paid.',
  ],
  equip_h='Equipment',
  equip=['2 x Caterpillar 1,420 hp', 'Flybridge with table and sunpad', 'Flybridge helm station', 'Al fresco dining in the aft cockpit', 'Multi-purpose bathing platform', 'Projector on the upper deck', 'Saloon with U-shaped sofa', 'Indoor dining area', '4 cabins for 9 guests', 'Accommodation for 4 crew', 'Interior design by Zuccon International Project', 'Refitted in 2020'],
  card=dict(alt='Ferretti 80 under way, side view', sub='2002 · 24.38 m · flybridge · 2 x Caterpillar 1,420 hp · Greece (Athens)',
            tb='Licence: Capitán de Yate or higher',
            desc='2002 Ferretti 80, refitted in 2020: flybridge, twin 1,420 hp Caterpillars, 9 guests in 4 cabins and 4 crew. It is in Greece (Athens) and can be viewed by appointment.',
            ask='Ask on WhatsApp', see='View listing'),
 ),
 'fr': dict(
  title='Ferretti 80 de 2002 à vendre · 769 990 € · Plata Marine',
  desc='Ferretti 80 de 2002, refit en 2020 : 24,38 m, flybridge, 2 Caterpillar de 1 420 ch, 9 invités en 4 cabines. En Grèce (Athènes), 769 990 €, TVA payée.',
  ogtitle='Ferretti 80 de 2002 à vendre · 769 990 €',
  ldname='Ferretti 80 (2002)',
  lddesc='Ferretti 80 de 2002, refit en 2020 : 24,38 m de longueur, 6,10 m de largeur, flybridge, deux moteurs Caterpillar de 1 420 ch, 26 nœuds de croisière et 31 en pointe selon la brochure, 9 invités en 4 cabines et 4 membres d\'équipage. Pavillon grec, en Grèce (Athènes). Prix 769 990 €, TVA payée.',
  sub=['Année 2002 · refit 2020', '24,38 m de longueur', '2 x Caterpillar 1 420 ch', 'Grèce (Athènes)'],
  price='769 990 €', vat='TVA payée',
  pdf='/barcos/ferretti-80-fr.pdf', pdftxt='Télécharger la fiche complète (PDF)', pdfbtn='Télécharger la fiche PDF (en français)',
  wa='Bonjour Juan, le Ferretti 80 de 2002 que vous avez à vendre m\'intéresse. Pouvons-nous en parler ?',
  wa_visit='Bonjour Juan, j\'aimerais voir en vrai le Ferretti 80 (2002) de votre site. Quels jours seraient possibles ?',
  wa_share='Regarde ce bateau : Ferretti 80 — https://www.platamarine.com/fr/barcos/ferretti-80.html',
  alt='Ferretti 80 en navigation, vue de profil', photo='photo',
  specs=[('Année', '2002 · refit en 2020'), ('Type', 'Yacht à moteur avec flybridge'),
         ('Longueur', '24,38 m (80 pieds, selon la brochure)'), ('Largeur', '6,10 m'), ('Tirant d\'eau', '1,83 m'), ('Jauge brute', '75 GT'),
         ('Coque', 'Polyester renforcé de fibre de verre (GRP)'), ('Moteurs', '2 x Caterpillar de 1 420 ch, diesel'),
         ('Heures', 'Environ 3 800 h au total (selon le vendeur)'), ('Vitesse', '26 nœuds de croisière et 31 en pointe (selon la brochure)'),
         ('Couchages', '9 invités en 4 cabines'), ('Équipage', '4 personnes'), ('Salles d\'eau', '3 (selon le vendeur)'),
         ('Refit 2020', 'Travaux réalisés : à confirmer sur la documentation'),
         ('Réservoirs, électronique et classification', 'À confirmer sur la documentation'),
         ('Permis', 'Permis espagnol Capitán de Yate ou supérieur (selon la longueur d\'immatriculation ; à confirmer sur la documentation)'),
         ('Pavillon', 'Grec'),
         ('Taxes', 'TVA payée, selon le vendeur ; à confirmer sur la documentation avant la réservation. Si vous résidez en Espagne et allez l\'y immatriculer ou l\'y utiliser, vérifiez la taxe d\'immatriculation auprès de votre gestoría')],
  h2='Mon avis',
  paras=[
   'Un Ferretti 80 de 2002, avec un refit en 2020. Il mesure 24,38 m de long pour 6,10 m de large, avec flybridge, et d\'après la brochure du vendeur il accueille 9 invités en 4 cabines et a de la place pour 4 membres d\'équipage.',
   'Il est équipé de deux moteurs Caterpillar de 1 420 ch. La brochure indique 26 nœuds de croisière et 31 en pointe, et le vendeur parle d\'environ 3 800 heures au total. L\'historique d\'entretien et les travaux du refit de 2020 sont demandés au vendeur et vérifiés avant la réservation.',
   'Dehors : un grand flybridge avec table, bain de soleil et poste de pilotage, un espace repas dans le cockpit arrière et une plateforme de bain. À l\'intérieur, le carré avec son canapé en U et la salle à manger ont de grandes baies vitrées, avec un aménagement de Zuccon International Project.',
   'Il se trouve en Grèce, dans la région d\'Athènes, sous pavillon grec, et se visite sur rendez-vous. Avec un permis espagnol, sa longueur demande le Capitán de Yate ou un titre supérieur (cela dépend de la longueur d\'immatriculation ; à confirmer sur la documentation). Le prix est de 769 990 €, TVA payée.',
  ],
  equip_h='Équipement',
  equip=['2 x Caterpillar 1 420 ch', 'Flybridge avec table et bain de soleil', 'Poste de pilotage sur le flybridge', 'Repas en plein air dans le cockpit arrière', 'Plateforme de bain polyvalente', 'Projecteur sur le pont supérieur', 'Carré avec canapé en U', 'Salle à manger intérieure', '4 cabines pour 9 invités', 'Couchages pour 4 membres d\'équipage', 'Aménagement de Zuccon International Project', 'Refit en 2020'],
  card=dict(alt='Ferretti 80 en navigation, vue de profil', sub='2002 · 24,38 m · flybridge · 2 x Caterpillar 1 420 ch · Grèce (Athènes)',
            tb='Permis : Capitán de Yate ou supérieur',
            desc='Ferretti 80 de 2002, refit en 2020 : flybridge, deux Caterpillar de 1 420 ch, 9 invités en 4 cabines et 4 membres d\'équipage. Il se trouve en Grèce (Athènes) et se visite sur rendez-vous.',
            ask='Demander sur WhatsApp', see='Voir la fiche'),
 ),
}

FORBIDDEN = r'Gallart|gallart|Volvo|Costa Brava|Girona|Gérone|Gerona|polac|polon|Polish|1977|29\.?900|29,900|29 900'


def wa(txt):
    return 'https://wa.me/34633742973?text=' + quote(txt, safe='')


def json_s(s):
    return json.dumps(s, ensure_ascii=False)


def build(lang):
    pre = '' if lang == 'es' else lang + '/'
    t = open(os.path.join(ROOT, pre, 'barcos', TPL + '.html'), encoding='utf-8').read()
    d = D[lang]
    e = html.escape
    # cabecera
    t = re.sub(r'<title>.*?</title>', '<title>' + e(d['title']) + '</title>', t, count=1)
    t = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="' + e(d['desc'], quote=True) + '">', t, count=1)
    t = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="' + e(d['ogtitle'], quote=True) + '">', t, count=1)
    t = re.sub(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="' + e(d['desc'], quote=True) + '">', t, count=1)
    # enlaces de WhatsApp (antes de cambiar el slug: las URL compartidas lo llevan codificado)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Gallart[^"]*(?:hablar|parlar|talk|parler)[^"]*', lambda m: wa(d['wa']), t)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Gallart[^"]*', lambda m: wa(d['wa_visit']), t)
    t = re.sub(r'https://wa\.me/\?text=[^"]*', lambda m: 'https://wa.me/?text=' + quote(d['wa_share'], safe=''), t)
    t = t.replace(TPL, SLUG)
    # datos estructurados
    imgs = ',\n'.join('"https://www.platamarine.com/%s-%d.jpg"' % (SLUG, i) for i in range(1, N_PHOTOS + 1))
    t = re.sub(r'"image": \[.*?\]', lambda m: '"image": [\n' + imgs + '\n]', t, count=1, flags=re.S)
    t = re.sub(r'"name": "Gallart 10\.50 Fly \(1977\)"', lambda m: '"name": ' + json_s(d['ldname']), t, count=1)
    t = re.sub(r'"description": ".*?",\n"offers"', lambda m: '"description": ' + json_s(d['lddesc']) + ',\n"offers"', t, count=1, flags=re.S)
    t = t.replace('"price": "29900"', '"price": "769990"')
    t = re.sub(r'"brand": \{\s*"@type": "Brand",\s*"name": "Gallart"\s*\},\s*"model": "10\.50 Fly"', '"brand": {\n"@type": "Brand",\n"name": "Ferretti"\n},\n"model": "80"', t, count=1)
    # subtítulo y precio
    t = re.sub(r'<div class="sub">.*?</div>', lambda m: '<div class="sub">' + ''.join('<span>%s</span>' % e(s) for s in d['sub']) + '</div>', t, count=1, flags=re.S)
    t = re.sub(r'<p class="price">[^<]*</p>', lambda m: '<p class="price">%s <span class="vat paid">%s</span></p>' % (d['price'], e(d['vat'])), t, count=1)
    # PDF
    t = re.sub(r'<a class="pdf-link" href="[^"]*" download>[^<]*</a>', lambda m: '<a class="pdf-link" href="%s" download>%s</a>' % (d['pdf'], e(d['pdftxt'])), t, count=1)
    t = re.sub(r'<a class="btn btn-ghost" href="[^"]*\.pdf" download>[^<]*</a>', lambda m: '<a class="btn btn-ghost" href="%s" download>%s</a>' % (d['pdf'], e(d['pdfbtn'])), t, count=1)
    # galería
    t = re.sub(r'<img class="main" id="main" [^>]*>', lambda m: '<img class="main" id="main" src="/%s-1.jpg" srcset="/%s-1-m.jpg 1000w, /%s-1.jpg %dw" sizes="(max-width: 1100px) 100vw, 1100px" alt="%s">' % (SLUG, SLUG, SLUG, W1, e(d['alt'], quote=True)), t, count=1)
    thumbs = ''.join('<img src="/%s-%d-t.jpg" data-full="/%s-%d.jpg" alt="%s – %s %d" loading="lazy" data-i="%d"%s>' % (SLUG, i, SLUG, i, NAME, d['photo'], i, i - 1, ' class="on"' if i == 1 else '') for i in range(1, N_PHOTOS + 1))
    t = re.sub(r'<div class="thumbs">.*?</div>', lambda m: '<div class="thumbs">' + thumbs + '</div>', t, count=1, flags=re.S)
    # ficha técnica
    dl = '<dl class="specs">' + ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in d['specs']) + '</dl>'
    t = re.sub(r'<dl class="specs">.*?</dl>', lambda m: dl, t, count=1, flags=re.S)
    # texto
    prose = '<div class="prose">\n<h2>%s</h2>\n%s\n<h3 class="equip-h">%s</h3><ul class="equip-tags">%s</ul>\n</div>' % (
        e(d['h2']), '\n'.join('<p>%s</p>' % e(p) for p in d['paras']), e(d['equip_h']), ''.join('<li>%s</li>' % e(x) for x in d['equip']))
    t = re.sub(r'<div class="prose">.*?</div>\n</div>', lambda m: prose + '\n</div>', t, count=1, flags=re.S)
    # resto de menciones del nombre (miga de pan, JSON de la miga, etc.)
    t = t.replace(TPL_NAME, NAME)
    # bloque de similares: se conserva el de la plantilla (data-ref con el slug nuevo; lo rellena similares.js en el navegador)
    assert '<!--pm-sim-->' in t and '"slug":"%s"' % SLUG in t
    left = re.findall(r'.{30}(?:%s).{30}' % FORBIDDEN, t)
    assert not left, left[:5]
    out = os.path.join(ROOT, pre, 'barcos', SLUG + '.html')
    open(out, 'w', encoding='utf-8').write(t)
    print('ok', out, len(t))


def card(lang):
    d = D[lang]; c = d['card']; e = html.escape
    return ('      <article data-pm-boat="{s}" class="bcard" data-sold="0" data-tipo="motor" data-titulo="4" data-precio="769990" data-zona="extranjero" data-comb="diesel" data-motor="intra" data-anyo="2002" data-i="-0.5">\n'
            '        <a class="bimg" href="{s}.html"><img src="/{s}-1-m.jpg" srcset="/{s}-1-m.jpg 1000w, /{s}-1.jpg {w}w" sizes="(max-width: 820px) 100vw, 560px" alt="{alt}" loading="lazy" width="{w}" height="770"><span class="status available">{st}</span></a>\n'
            '        <div class="bbody">\n'
            '          <div class="head" style="margin:0 0 6px"><h2><a href="{s}.html">{n}</a></h2><p class="price">{p} <span class="vat paid">{v}</span></p></div>\n'
            '          <p class="sub" style="margin:0">{sub}</p>\n'
            '          <span class="tbadge">{tb}</span>\n'
            '          <p class="bdesc">{desc}</p>\n'
            '          <div class="bcta"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{ask}</a><a class="btn btn-ghost" href="{s}.html">{see}</a></div>\n'
            '        </div>\n'
            '      </article>\n').format(s=SLUG, w=W1, alt=e(c['alt'], quote=True), st='Available' if lang == 'en' else 'Disponible', n=NAME,
                                       p=d['price'], v=e(d['vat']), sub=e(c['sub']), tb=e(c['tb']), desc=e(c['desc']), wa=wa(d['wa']), ask=c['ask'], see=c['see'])


def add_catalog(lang):
    pre = '' if lang == 'es' else lang + '/'
    p = os.path.join(ROOT, pre, 'barcos', 'index.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'      <article data-pm-boat="%s".*?</article>\n' % SLUG, '', s, flags=re.S)  # idempotente
    anchor = '      <article data-pm-boat="prestige-32"'
    assert s.count(anchor) == 1
    s = s.replace(anchor, card(lang) + anchor, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('catálogo', p)


if __name__ == '__main__':
    for lang in ('es', 'ca', 'en', 'fr'):
        build(lang)
        add_catalog(lang)
