"""Genera la ficha de la Lexsia XS20 (2008) en ES/CA/EN/FR a partir de la ficha de la Barracuda 8 como plantilla,
y añade su tarjeta al catálogo /barcos/ de los 4 idiomas (idempotente).
Uso: python3 _tools/build_lexsia_xs20.py
Después: python3 _tools/ficha_v2.py lexsia-xs20, PM_ROOT=<repo> python3 _tools/build_pdfs.py lexsia-xs20,
node _tools/build_pmlists.js, node _tools/build_similares.js y python3 _tools/build_search_index.py.
Venta entre particulares (sin IVA). Sin nombre de la embarcación ni matrícula."""
import re, os, html, json
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'lexsia-xs20'
TPL = 'barracuda-8'
TPL_NAME = 'Beneteau Barracuda 8'
NAME = 'Lexsia XS20'
N_PHOTOS = 10
W1 = 1448

EQ_ES = ['Suzuki DF115 4 tiempos', 'Mantenimiento al día', 'Molinete eléctrico con mando', 'Garmin GPSMAP 922xs', 'Humminbird Helix 5',
         'VHF fijo', 'Dos baterías con desconectador en paralelo', 'Achique automático', 'Ducha de popa', 'Suelo de bañera en gelcoat',
         'Tapicería de bañera nueva', 'Bimini', 'Lona de fondeo', 'Luces de cortesía en la bañera', 'Luces de navegación', 'Camarote en proa']
D = {
 'es': dict(
  title='Lexsia XS20 2008 en venta · 22.990 € · Plata Marine',
  desc='Lexsia XS20 de 2008, lancha cabinada de 5,84 m con Suzuki DF115 de 4 tiempos (unas 500 h, mantenimiento al día). Molinete eléctrico, 2 plotters y tapicería nueva. En Blanes (Costa Brava). 22.990 €.',
  ogtitle='Lexsia XS20 2008 en venta · 22.990 €',
  ldname='Lexsia XS20 (2008)',
  lddesc='Lexsia XS20 de 2008, lancha cabinada de 5,84 m con motor fueraborda Suzuki DF115 de 4 tiempos (unas 500 horas, mantenimiento al día). Molinete eléctrico con mando, Garmin GPSMAP 922xs y Humminbird Helix 5, VHF fijo, ducha de popa, suelo de bañera en gelcoat y tapicería de bañera nueva. Despachada para 6 personas. En Blanes (Costa Brava), con amarre de alquiler con posible subrogación. Precio 22.990 €, venta entre particulares.',
  sub=['2008', '5,84 m de eslora', 'Suzuki DF115 4T', 'Blanes (Costa Brava)'],
  price='22.990 €',
  pdf='lexsia-xs20.pdf', pdftxt='Descargar ficha completa (PDF)', pdfbtn='Descargar ficha PDF',
  wa='Hola Juan, me interesa la Lexsia XS20 que tenéis en venta. ¿Podemos hablar?',
  wa_visit='Hola Juan, me gustaría ver en persona la Lexsia XS20 de vuestra web. ¿Qué días se podría?',
  wa_share='Mira este barco: Lexsia XS20 — https://www.platamarine.com/barcos/lexsia-xs20',
  alt='Lexsia XS20 amarrada en el pantalán, vista de proa', photo='foto',
  headnote='Venta entre particulares: los datos se comprueban con la documentación antes de reservar.',
  note='Venta entre particulares. Los datos de esta ficha son orientativos; los definitivos serán los del contrato de compraventa. Recomendamos prueba de mar y un peritaje independiente antes de reservar. Antes de cualquier pago recibirás el desglose de precio, impuestos y gastos de cambio de titularidad.',
  specs=[('Tipo', 'Lancha cabinada con camarote en proa'), ('Año', '2008'), ('Eslora', '5,84 m'),
         ('Motor', 'Suzuki DF115, fueraborda de gasolina de 4 tiempos'), ('Horas', 'Unas 500 h, mantenimiento al día'),
         ('Capacidad', 'Despachada para 6 personas'), ('Electrónica', 'Garmin GPSMAP 922xs, Humminbird Helix 5 y VHF fijo'),
         ('Propietarios', '3'), ('Titulación', 'Licencia de Navegación o superior'), ('ITB', 'Exenta'),
         ('Amarre', 'De alquiler en Blanes, con posible subrogación'), ('Ubicación', 'Blanes (Costa Brava, Girona)'),
         ('Visitas', 'Con cita previa'),
         ('Impuestos', 'Vende un particular: no lleva IVA; el comprador paga el ITP de su comunidad')],
  h2='Cómo lo veo',
  paras=[
   'Una Lexsia XS20 de 2008: lancha cabinada de 5,84 m con bañera amplia, solárium en proa y un pequeño camarote para guardar el equipo o resguardarse un rato. Es un barco cómodo para salir a calas en el día, fácil de llevar y de mantener.',
   'Lleva un Suzuki DF115 de cuatro tiempos con unas 500 horas y el mantenimiento al día. Ha tenido tres propietarios.',
   'Está muy equipada: molinete eléctrico con mando a distancia, dos plotters (Garmin GPSMAP 922xs y Humminbird Helix 5), VHF fijo, dos baterías con desconectador en paralelo, achique automático y ducha de popa. El suelo de la bañera es de gelcoat, la tapicería de la bañera es nueva y lleva bimini, lona de fondeo, luces de cortesía en la bañera y luces de navegación. El piloto automático Simrad está actualmente no operativo.',
   'Está despachada para 6 personas, exenta de ITB y se gobierna con la Licencia de Navegación o un título superior. Tiene amarre de alquiler en Blanes, con posible subrogación. El precio son 22.990 €; vende un particular, así que no lleva IVA y el comprador paga el ITP de su comunidad.',
  ],
  equip_h='Equipamiento', equip=EQ_ES,
  card=dict(alt='Lexsia XS20 amarrada en el pantalán', sub='2008 · 5,84 m · lancha cabinada · Suzuki 115 cv · Costa Brava',
            tb='Titulación: Licencia de Navegación o superior',
            desc='Lancha cabinada de 2008 con Suzuki DF115 de 4 tiempos (unas 500 h, mantenimiento al día), molinete eléctrico y dos plotters. En Blanes, con amarre de alquiler con posible subrogación.',
            ask='Preguntar por WhatsApp', see='Ver ficha'),
 ),
 'ca': dict(
  title='Lexsia XS20 2008 en venda · 22.990 € · Plata Marine',
  desc="Lexsia XS20 del 2008, llanxa amb cabina de 5,84 m amb Suzuki DF115 de 4 temps (unes 500 h, manteniment al dia). Molinet elèctric, 2 plotters i tapisseria nova. A Blanes (Costa Brava). 22.990 €.",
  ogtitle='Lexsia XS20 2008 en venda · 22.990 €',
  ldname='Lexsia XS20 (2008)',
  lddesc="Lexsia XS20 del 2008, llanxa amb cabina de 5,84 m amb motor forabord Suzuki DF115 de 4 temps (unes 500 hores, manteniment al dia). Molinet elèctric amb comandament, Garmin GPSMAP 922xs i Humminbird Helix 5, VHF fix, dutxa de popa, terra de banyera en gelcoat i tapisseria de banyera nova. Despatxada per a 6 persones. A Blanes (Costa Brava), amb amarrament de lloguer amb possible subrogació. Preu 22.990 €, venda entre particulars.",
  sub=['2008', '5,84 m d’eslora', 'Suzuki DF115 4T', 'Blanes (Costa Brava)'],
  price='22.990 €',
  pdf='/barcos/lexsia-xs20-ca.pdf', pdftxt='Descarregar la fitxa completa (PDF)', pdfbtn='Descarregar la fitxa PDF',
  wa="Hola Juan, m'interessa la Lexsia XS20 que teniu en venda. En podem parlar?",
  wa_visit="Hola Juan, m'agradaria veure en persona la Lexsia XS20 del vostre web. Quins dies es podria?",
  wa_share='Mira aquest vaixell: Lexsia XS20 — https://www.platamarine.com/ca/barcos/lexsia-xs20',
  alt='Lexsia XS20 amarrada al pantalà, vista de proa', photo='foto',
  headnote='Venda entre particulars: les dades es comproven amb la documentació abans de reservar.',
  note="Venda entre particulars. Les dades d'aquesta fitxa són orientatives; les definitives seran les del contracte de compravenda. Recomanem prova de mar i un peritatge independent abans de reservar. Abans de qualsevol pagament rebràs el desglossament de preu, impostos i despeses de canvi de titularitat.",
  specs=[('Tipus', 'Llanxa amb cabina a proa'), ('Any', '2008'), ('Eslora', '5,84 m'),
         ('Motor', 'Suzuki DF115, forabord de gasolina de 4 temps'), ('Hores', 'Unes 500 h, manteniment al dia'),
         ('Capacitat', 'Despatxada per a 6 persones'), ('Electrònica', 'Garmin GPSMAP 922xs, Humminbird Helix 5 i VHF fix'),
         ('Propietaris', '3'), ('Titulació', 'Llicència de Navegació o superior'), ('ITB', 'Exempta'),
         ('Amarrament', 'De lloguer a Blanes, amb possible subrogació'), ('Ubicació', 'Blanes (Costa Brava, Girona)'),
         ('Visites', 'Amb cita prèvia'),
         ('Impostos', "Ven un particular: no porta IVA; el comprador paga l'ITP de la seva comunitat")],
  h2='Com ho veig',
  paras=[
   "Una Lexsia XS20 del 2008: llanxa amb cabina de 5,84 m amb banyera àmplia, solàrium a proa i una petita cabina per guardar l'equip o resguardar-se una estona. És un vaixell còmode per sortir a cales durant el dia, fàcil de portar i de mantenir.",
   'Porta un Suzuki DF115 de quatre temps amb unes 500 hores i el manteniment al dia. Ha tingut tres propietaris.',
   "Està molt equipada: molinet elèctric amb comandament a distància, dos plotters (Garmin GPSMAP 922xs i Humminbird Helix 5), VHF fix, dues bateries amb desconnectador en paral·lel, buidatge automàtic i dutxa de popa. El terra de la banyera és de gelcoat, la tapisseria de la banyera és nova i porta bimini, lona de fondeig, llums de cortesia a la banyera i llums de navegació. El pilot automàtic Simrad actualment no és operatiu.",
   "Està despatxada per a 6 persones, exempta d'ITB i es governa amb la Llicència de Navegació o un títol superior. Té amarrament de lloguer a Blanes, amb possible subrogació. El preu són 22.990 €; ven un particular, així que no porta IVA i el comprador paga l'ITP de la seva comunitat.",
  ],
  equip_h='Equipament',
  equip=['Suzuki DF115 4 temps', 'Manteniment al dia', 'Molinet elèctric amb comandament', 'Garmin GPSMAP 922xs', 'Humminbird Helix 5',
         'VHF fix', 'Dues bateries amb desconnectador en paral·lel', 'Buidatge automàtic', 'Dutxa de popa', 'Terra de banyera en gelcoat',
         'Tapisseria de banyera nova', 'Bimini', 'Lona de fondeig', 'Llums de cortesia a la banyera', 'Llums de navegació', 'Cabina a proa'],
  card=dict(alt='Lexsia XS20 amarrada al pantalà', sub='2008 · 5,84 m · llanxa amb cabina · Suzuki 115 cv · Costa Brava',
            tb='Titulació: Llicència de Navegació o superior',
            desc="Llanxa amb cabina del 2008 amb Suzuki DF115 de 4 temps (unes 500 h, manteniment al dia), molinet elèctric i dos plotters. A Blanes, amb amarrament de lloguer amb possible subrogació.",
            ask='Preguntar per WhatsApp', see='Veure fitxa'),
 ),
 'en': dict(
  title='Lexsia XS20 2008 for sale · €22,990 · Plata Marine',
  desc='2008 Lexsia XS20, 5.84 m cuddy cabin boat with a Suzuki DF115 four-stroke (about 500 h, servicing up to date). Electric windlass, 2 chartplotters and new upholstery. In Blanes (Costa Brava). €22,990.',
  ogtitle='Lexsia XS20 2008 for sale · €22,990',
  ldname='Lexsia XS20 (2008)',
  lddesc='2008 Lexsia XS20, 5.84 m cuddy cabin boat with a Suzuki DF115 four-stroke outboard (about 500 hours, servicing up to date). Electric windlass with remote, Garmin GPSMAP 922xs and Humminbird Helix 5, fixed VHF, transom shower, gelcoat cockpit floor and new cockpit upholstery. Licensed for 6 people. In Blanes (Costa Brava), with a rented berth that may be transferred. Price €22,990, private sale.',
  sub=['2008', '5.84 m length', 'Suzuki DF115 4-stroke', 'Blanes (Costa Brava)'],
  price='€22,990',
  pdf='/barcos/lexsia-xs20-en.pdf', pdftxt='Download full spec sheet (PDF)', pdfbtn='Download PDF listing',
  wa="Hi Juan, I'm interested in the Lexsia XS20 you have for sale. Can we talk?",
  wa_visit="Hi Juan, I'd like to see the Lexsia XS20 from your website in person. Which days would work?",
  wa_share='Have a look at this boat: Lexsia XS20 — https://www.platamarine.com/en/barcos/lexsia-xs20',
  alt='Lexsia XS20 moored at the pontoon, bow view', photo='photo',
  headnote='Private sale: the details are checked against the documentation before you reserve.',
  note="Private sale. The details on this page are indicative; the final ones will be those of the sale contract. We recommend a sea trial and an independent survey before reserving. Before any payment you will receive a breakdown of the price, taxes and ownership-transfer costs.",
  specs=[('Type', 'Cuddy cabin boat with bow cabin'), ('Year', '2008'), ('Length', '5.84 m'),
         ('Engine', 'Suzuki DF115, four-stroke petrol outboard'), ('Hours', 'About 500 h, servicing up to date'),
         ('Capacity', 'Licensed for 6 people'), ('Electronics', 'Garmin GPSMAP 922xs, Humminbird Helix 5 and fixed VHF'),
         ('Owners', '3'), ('Licence', 'Navigation Licence or higher'), ('ITB (Spanish inspection)', 'Exempt'),
         ('Berth', 'Rented in Blanes, may be transferred'), ('Location', 'Blanes (Costa Brava, Girona)'),
         ('Viewings', 'By appointment'),
         ('Taxes', 'Private seller: no VAT; the buyer pays the transfer tax (ITP) of their region')],
  h2='How I see it',
  paras=[
   'A 2008 Lexsia XS20: a 5.84 m cuddy cabin boat with a roomy cockpit, a bow sunbed and a small cabin to stow gear or get out of the sun for a while. A comfortable day boat for trips to coves, easy to handle and to maintain.',
   'It has a Suzuki DF115 four-stroke with about 500 hours and servicing up to date. It has had three owners.',
   'It is very well equipped: electric windlass with remote, two chartplotters (Garmin GPSMAP 922xs and Humminbird Helix 5), fixed VHF, two batteries with a parallel switch, automatic bilge pump and transom shower. The cockpit floor is gelcoat, the cockpit upholstery is new, and it has a bimini, anchoring cover, cockpit courtesy lights and navigation lights. The Simrad autopilot is currently not working.',
   'It is licensed for 6 people, exempt from the ITB inspection and can be skippered with the Navigation Licence or a higher licence. It has a rented berth in Blanes that may be transferred. The price is €22,990; it is a private sale, so there is no VAT and the buyer pays the transfer tax (ITP) of their region.',
  ],
  equip_h='Equipment',
  equip=['Suzuki DF115 four-stroke', 'Servicing up to date', 'Electric windlass with remote', 'Garmin GPSMAP 922xs', 'Humminbird Helix 5',
         'Fixed VHF', 'Two batteries with parallel switch', 'Automatic bilge pump', 'Transom shower', 'Gelcoat cockpit floor',
         'New cockpit upholstery', 'Bimini', 'Anchoring cover', 'Cockpit courtesy lights', 'Navigation lights', 'Bow cabin'],
  card=dict(alt='Lexsia XS20 moored at the pontoon', sub='2008 · 5.84 m · cuddy cabin · Suzuki 115 hp · Costa Brava',
            tb='Licence: Navigation Licence or higher',
            desc='2008 cuddy cabin boat with a Suzuki DF115 four-stroke (about 500 h, servicing up to date), electric windlass and two chartplotters. In Blanes, with a rented berth that may be transferred.',
            ask='Ask on WhatsApp', see='See details'),
 ),
 'fr': dict(
  title='Lexsia XS20 2008 à vendre · 22 990 € · Plata Marine',
  desc='Lexsia XS20 de 2008, bateau cabine de 5,84 m avec Suzuki DF115 4 temps (environ 500 h, entretien à jour). Guindeau électrique, 2 traceurs et sellerie neuve. À Blanes (Costa Brava). 22 990 €.',
  ogtitle='Lexsia XS20 2008 à vendre · 22 990 €',
  ldname='Lexsia XS20 (2008)',
  lddesc='Lexsia XS20 de 2008, bateau cabine de 5,84 m avec moteur hors-bord Suzuki DF115 4 temps (environ 500 heures, entretien à jour). Guindeau électrique avec télécommande, Garmin GPSMAP 922xs et Humminbird Helix 5, VHF fixe, douche de poupe, sol de cockpit en gelcoat et sellerie de cockpit neuve. Homologué pour 6 personnes. À Blanes (Costa Brava), avec une place de port en location pouvant être transférée. Prix 22 990 €, vente entre particuliers.',
  sub=['2008', '5,84 m de longueur', 'Suzuki DF115 4 temps', 'Blanes (Costa Brava)'],
  price='22 990 €',
  pdf='/barcos/lexsia-xs20-fr.pdf', pdftxt='Télécharger la fiche complète (PDF)', pdfbtn='Télécharger la fiche PDF',
  wa="Bonjour Juan, le Lexsia XS20 que vous avez à vendre m'intéresse. Pouvons-nous en parler ?",
  wa_visit="Bonjour Juan, j'aimerais voir sur place le Lexsia XS20 de votre site. Quels jours seraient possibles ?",
  wa_share='Regarde ce bateau : Lexsia XS20 — https://www.platamarine.com/fr/barcos/lexsia-xs20',
  alt='Lexsia XS20 amarré au ponton, vue de l’avant', photo='photo',
  headnote='Vente entre particuliers : les données sont vérifiées par rapport à la documentation avant la réservation.',
  note="Vente entre particuliers. Les données de cette page sont indicatives ; les définitives seront celles du contrat de vente. Nous recommandons un essai en mer et une expertise indépendante avant de réserver. Avant tout paiement, vous recevrez le détail du prix, des taxes et des frais de changement de propriétaire.",
  specs=[('Type', 'Bateau cabine avec cabine avant'), ('Année', '2008'), ('Longueur', '5,84 m'),
         ('Moteur', 'Suzuki DF115, hors-bord essence 4 temps'), ('Heures', 'Environ 500 h, entretien à jour'),
         ('Capacité', 'Homologué pour 6 personnes'), ('Électronique', 'Garmin GPSMAP 922xs, Humminbird Helix 5 et VHF fixe'),
         ('Propriétaires', '3'), ('Permis', 'Licencia de Navegación ou supérieur'), ('ITB (contrôle espagnol)', 'Exempté'),
         ('Place de port', 'En location à Blanes, peut être transférée'), ('Emplacement', 'Blanes (Costa Brava, Gérone)'),
         ('Visites', 'Sur rendez-vous'),
         ('Taxes', "Vendeur particulier : pas de TVA ; l'acheteur paie l'ITP de sa région")],
  h2='Mon avis',
  paras=[
   "Un Lexsia XS20 de 2008 : bateau cabine de 5,84 m avec un cockpit spacieux, un bain de soleil à l'avant et une petite cabine pour ranger le matériel ou se mettre à l'abri un moment. Un bateau confortable pour aller en crique à la journée, facile à mener et à entretenir.",
   'Il est équipé d’un Suzuki DF115 4 temps avec environ 500 heures et un entretien à jour. Il a eu trois propriétaires.',
   "Il est très bien équipé : guindeau électrique avec télécommande, deux traceurs (Garmin GPSMAP 922xs et Humminbird Helix 5), VHF fixe, deux batteries avec coupleur en parallèle, pompe de cale automatique et douche de poupe. Le sol du cockpit est en gelcoat, la sellerie du cockpit est neuve et il dispose d’un bimini, d’une bâche de mouillage, de lumières de courtoisie dans le cockpit et de feux de navigation. Le pilote automatique Simrad n’est actuellement pas opérationnel.",
   "Il est homologué pour 6 personnes, exempté de l’ITB et se pilote avec la Licencia de Navegación ou un titre supérieur. Il a une place de port en location à Blanes, qui peut être transférée. Le prix est de 22 990 € ; c’est une vente entre particuliers, donc sans TVA, et l’acheteur paie l’ITP de sa région.",
  ],
  equip_h='Équipement',
  equip=['Suzuki DF115 4 temps', 'Entretien à jour', 'Guindeau électrique avec télécommande', 'Garmin GPSMAP 922xs', 'Humminbird Helix 5',
         'VHF fixe', 'Deux batteries avec coupleur', 'Pompe de cale automatique', 'Douche de poupe', 'Sol de cockpit en gelcoat',
         'Sellerie de cockpit neuve', 'Bimini', 'Bâche de mouillage', 'Lumières de courtoisie', 'Feux de navigation', 'Cabine avant'],
  card=dict(alt='Lexsia XS20 amarré au ponton', sub='2008 · 5,84 m · bateau cabine · Suzuki 115 ch · Costa Brava',
            tb='Permis : Licencia de Navegación ou supérieur',
            desc="Bateau cabine de 2008 avec Suzuki DF115 4 temps (environ 500 h, entretien à jour), guindeau électrique et deux traceurs. À Blanes, avec une place de port en location pouvant être transférée.",
            ask='Demander sur WhatsApp', see='Voir la fiche'),
 ),
}

FORBIDDEN = r'Barracuda|barracuda|Beneteau|57\.?990|57,990|57 990|DF150|Furuno|Lowrance|Daurada|pilothouse|Pilothouse|IVA pagad|IVA pagat|VAT paid|TVA payée|intermedi|Intermedi|Brokerage|Courtage'


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
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Barracuda[^"]*(?:hablar|parlar|talk|parler)[^"]*', lambda m: wa(d['wa']), t)
    t = re.sub(r'https://wa\.me/34633742973\?text=[^"]*Barracuda[^"]*', lambda m: wa(d['wa_visit']), t)
    t = re.sub(r'https://wa\.me/\?text=[^"]*', lambda m: 'https://wa.me/?text=' + quote(d['wa_share'], safe=''), t)
    t = t.replace(TPL, SLUG)
    imgs = ',\n'.join('    "https://www.platamarine.com/%s-%d.jpg"' % (SLUG, i) for i in range(1, N_PHOTOS + 1))
    t = re.sub(r'"image": \[.*?\]', lambda m: '"image": [\n' + imgs + '\n  ]', t, count=1, flags=re.S)
    t = re.sub(r'"name": "Beneteau Barracuda 8 \(2016\)"', lambda m: '"name": ' + json_s(d['ldname']), t, count=1)
    t = re.sub(r'"description": ".*?",(\s*)"offers"', lambda m: '"description": ' + json_s(d['lddesc']) + ',' + m.group(1) + '"offers"', t, count=1, flags=re.S)
    t = t.replace('"price": "57990"', '"price": "22990"')
    t = re.sub(r'"brand": \{\s*"@type": "Brand",\s*"name": "Beneteau"\s*\},\s*"model": "Barracuda 8"', '"brand": {\n    "@type": "Brand",\n    "name": "Lexsia"\n  },\n  "model": "XS20"', t, count=1)
    t = re.sub(r'<div class="sub">.*?</div>', lambda m: '<div class="sub">' + ''.join('<span>%s</span>' % e(s) for s in d['sub']) + '</div>', t, count=1, flags=re.S)
    t = re.sub(r'<p class="price">.*?</p>', lambda m: '<p class="price">%s</p>' % d['price'], t, count=1)
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
    t = re.sub(r'<p class="muted head-note">.*?</p>', lambda m: '<p class="muted head-note">%s</p>' % e(d['headnote']), t, count=1, flags=re.S)
    t = re.sub(r'<p class="note">.*?</p>', lambda m: '<p class="note">%s</p>' % e(d['note']), t, count=1, flags=re.S)
    t = t.replace(TPL_NAME, NAME)
    t = re.sub(r'(<div class="pm-sim" data-ref=\'\{"slug":"%s"\}\'>).*?</div>' % SLUG, lambda m: m.group(1) + '</div>', t, count=1, flags=re.S)
    assert '"slug":"%s"' % SLUG in t
    left = re.findall(r'.{30}(?:%s).{30}' % FORBIDDEN, t)
    assert not left, left[:5]
    out = os.path.join(ROOT, pre, 'barcos', SLUG + '.html')
    open(out, 'w', encoding='utf-8').write(t)
    print('ok', out, len(t))


def card(lang):
    d = D[lang]; c = d['card']; e = html.escape
    return ('      <article data-pm-boat="{s}" class="bcard" data-sold="0" data-tipo="motor" data-titulo="1" data-precio="22990" data-zona="cataluna" data-comb="gasolina" data-motor="fuera" data-anyo="2008" data-i="0.5">\n'
            '        <a class="bimg" href="{s}.html"><img src="/{s}-1-m.jpg" srcset="/{s}-1-m.jpg 1000w, /{s}-1.jpg {w}w" sizes="(max-width: 820px) 100vw, 560px" alt="{alt}" loading="lazy" width="{w}" height="1086"><span class="status available">{st}</span></a>\n'
            '        <div class="bbody">\n'
            '          <div class="head" style="margin:0 0 6px"><h2><a href="{s}.html">{n}</a></h2><p class="price">{p}</p></div>\n'
            '          <p class="sub" style="margin:0">{sub}</p>\n'
            '          <span class="tbadge">{tb}</span>\n'
            '          <p class="bdesc">{desc}</p>\n'
            '          <div class="bcta"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{ask}</a><a class="btn btn-ghost" href="{s}.html">{see}</a></div>\n'
            '        </div>\n'
            '      </article>\n').format(s=SLUG, w=W1, alt=e(c['alt'], quote=True), st={'en': 'Available', 'fr': 'Disponible'}.get(lang, 'Disponible'), n=NAME,
                                       p=d['price'], sub=e(c['sub']), tb=e(c['tb']), desc=e(c['desc']), wa=wa(d['wa']), ask=c['ask'], see=c['see'])


def add_catalog(lang):
    pre = '' if lang == 'es' else lang + '/'
    p = os.path.join(ROOT, pre, 'barcos', 'index.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'      <article data-pm-boat="%s".*?</article>\n' % SLUG, '', s, flags=re.S)
    anchor = '      <article data-pm-boat="sacs-535"'
    assert s.count(anchor) == 1
    s = s.replace(anchor, card(lang) + anchor, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('catálogo', p)


# Datos añadidos por el propietario (3 nov 2026, noche)
X = {
 'es': dict(eq=['Escalera de baño', 'Ancla', 'Defensas', 'Depósito de agua dulce'], flag=('Bandera', 'Española, 7ª lista'), trl=('Remolque', 'No incluido'),
            tax='IVA y matriculación pagados. Vende un particular: la venta no lleva IVA y el comprador paga el ITP de su comunidad',
            p3=' También lleva escalera de baño, ancla, defensas y depósito de agua dulce.', p4=' Bandera española, 7ª lista, con el IVA y la matriculación pagados; se vende sin remolque.'),
 'ca': dict(eq=['Escala de bany', 'Àncora', 'Defenses', "Dipòsit d'aigua dolça"], flag=('Bandera', 'Espanyola, 7a llista'), trl=('Remolc', 'No inclòs'),
            tax="IVA i matriculació pagats. Ven un particular: la venda no porta IVA i el comprador paga l'ITP de la seva comunitat",
            p3=" També porta escala de bany, àncora, defenses i dipòsit d'aigua dolça.", p4=" Bandera espanyola, 7a llista, amb l'IVA i la matriculació pagats; es ven sense remolc."),
 'en': dict(eq=['Swim ladder', 'Anchor', 'Fenders', 'Fresh water tank'], flag=('Flag', 'Spanish, 7th list (private use)'), trl=('Trailer', 'Not included'),
            tax="Private seller: no VAT; the boat's VAT and registration tax are paid. The buyer pays the transfer tax (ITP) of their region",
            p3=' It also has a swim ladder, anchor, fenders and a fresh water tank.', p4=" Spanish flag, 7th list (private use), with VAT and registration tax paid; sold without a trailer."),
 'fr': dict(eq=['Échelle de bain', 'Ancre', 'Défenses', "Réservoir d'eau douce"], flag=('Pavillon', 'Espagnol, 7e liste (usage privé)'), trl=('Remorque', 'Non incluse'),
            tax="Vendeur particulier : pas de TVA ; TVA et taxe d'immatriculation du bateau payées. L'acheteur paie l'ITP de sa région",
            p3=" Il dispose aussi d'une échelle de bain, d'une ancre, de défenses et d'un réservoir d'eau douce.", p4=" Pavillon espagnol, 7e liste (usage privé), TVA et taxe d'immatriculation payées ; vendu sans remorque."),
}
for _l, _x in X.items():
    _d = D[_l]
    _d['equip'] = _d['equip'] + _x['eq']
    _sp = [kv for kv in _d['specs']]
    _sp[-1] = (_sp[-1][0], _x['tax'])
    _i = [k for k, (a, b) in enumerate(_sp) if a in ('ITB', 'ITB (Spanish inspection)', 'ITB (contrôle espagnol)')][0]
    _sp[_i + 1:_i + 1] = [_x['flag'], _x['trl']]
    _d['specs'] = _sp
    _d['paras'] = [_d['paras'][0], _d['paras'][1], _d['paras'][2] + _x['p3'], _d['paras'][3] + _x['p4']]


# SEO y puntos fuertes (Juan, 3 nov 2026): fueraborda con camarote, ducha de popa, dos plotters y molinete eléctrico con mando a distancia
KEY = {
 'es': ['Fueraborda con camarote', 'Ducha de popa', 'Dos plotters con sonda', 'Molinete eléctrico con mando a distancia'],
 'ca': ['Forabord amb cabina', 'Dutxa de popa', 'Dos plotters amb sonda', 'Molinet elèctric amb comandament a distància'],
 'en': ['Outboard with cabin', 'Transom shower', 'Two chartplotters with sounder', 'Electric windlass with remote control'],
 'fr': ['Hors-bord avec cabine', 'Douche de poupe', 'Deux traceurs avec sondeur', 'Guindeau électrique télécommandé'],
}
SEO = {
 'es': dict(title='Lexsia XS20 en venta · fueraborda con camarote · 22.990 €',
            desc='Lexsia XS20 de 2008: lancha fueraborda con camarote, ducha de popa, dos plotters y molinete eléctrico con mando a distancia. Suzuki DF115 4T (≈500 h, mantenimiento al día). Blanes, Costa Brava. 22.990 €.',
            ogtitle='Lexsia XS20 · fueraborda con camarote · 22.990 €',
            sub1='Fueraborda con camarote',
            p0='Una Lexsia XS20 de 2008, una lancha fueraborda con camarote de 5,84 m. Lo que la hace especial: camarote en proa para guardar el equipo o resguardarse, ducha de popa, dos plotters con sonda y molinete eléctrico con mando a distancia para fondear sin esfuerzo. Bañera amplia y solárium en proa: un barco cómodo para salir a calas en el día, fácil de llevar y de mantener.',
            card='Lancha fueraborda con camarote de 2008: ducha de popa, dos plotters y molinete eléctrico con mando a distancia. Suzuki DF115 4T (unas 500 h, mantenimiento al día). En Blanes, con amarre de alquiler con posible subrogación.'),
 'ca': dict(title='Lexsia XS20 en venda · forabord amb cabina · 22.990 €',
            desc="Lexsia XS20 del 2008: llanxa forabord amb cabina, dutxa de popa, dos plotters i molinet elèctric amb comandament a distància. Suzuki DF115 4T (≈500 h, manteniment al dia). Blanes, Costa Brava. 22.990 €.",
            ogtitle='Lexsia XS20 · forabord amb cabina · 22.990 €',
            sub1='Forabord amb cabina',
            p0="Una Lexsia XS20 del 2008, una llanxa forabord amb cabina de 5,84 m. El que la fa especial: cabina a proa per guardar l'equip o resguardar-se, dutxa de popa, dos plotters amb sonda i molinet elèctric amb comandament a distància per fondejar sense esforç. Banyera àmplia i solàrium a proa: un vaixell còmode per sortir a cales durant el dia, fàcil de portar i de mantenir.",
            card="Llanxa forabord amb cabina del 2008: dutxa de popa, dos plotters i molinet elèctric amb comandament a distància. Suzuki DF115 4T (unes 500 h, manteniment al dia). A Blanes, amb amarrament de lloguer amb possible subrogació."),
 'en': dict(title='Lexsia XS20 for sale · outboard cuddy cabin · €22,990',
            desc='2008 Lexsia XS20: outboard boat with cabin, transom shower, two chartplotters and an electric windlass with remote control. Suzuki DF115 4-stroke (≈500 h, servicing up to date). Blanes, Costa Brava. €22,990.',
            ogtitle='Lexsia XS20 · outboard cuddy cabin · €22,990',
            sub1='Outboard with cabin',
            p0='A 2008 Lexsia XS20, a 5.84 m outboard boat with a cabin. What makes it stand out: a bow cabin to stow gear or get out of the sun, a transom shower, two chartplotters with sounder and an electric windlass with remote control for effortless anchoring. Roomy cockpit and bow sunbed: a comfortable day boat for trips to coves, easy to handle and to maintain.',
            card='2008 outboard boat with cabin: transom shower, two chartplotters and an electric windlass with remote control. Suzuki DF115 four-stroke (about 500 h, servicing up to date). In Blanes, with a rented berth that may be transferred.'),
 'fr': dict(title='Lexsia XS20 à vendre · hors-bord avec cabine · 22 990 €',
            desc='Lexsia XS20 de 2008 : hors-bord avec cabine, douche de poupe, deux traceurs et guindeau électrique télécommandé. Suzuki DF115 4 temps (≈500 h, entretien à jour). Blanes, Costa Brava. 22 990 €.',
            ogtitle='Lexsia XS20 · hors-bord avec cabine · 22 990 €',
            sub1='Hors-bord avec cabine',
            p0="Un Lexsia XS20 de 2008, un bateau hors-bord avec cabine de 5,84 m. Ce qui le distingue : une cabine avant pour ranger le matériel ou se mettre à l'abri, une douche de poupe, deux traceurs avec sondeur et un guindeau électrique télécommandé pour mouiller sans effort. Cockpit spacieux et bain de soleil à l'avant : un bateau confortable pour aller en crique à la journée, facile à mener et à entretenir.",
            card="Hors-bord avec cabine de 2008 : douche de poupe, deux traceurs et guindeau électrique télécommandé. Suzuki DF115 4 temps (environ 500 h, entretien à jour). À Blanes, avec une place de port en location pouvant être transférée."),
}
for _l, _x in SEO.items():
    _d = D[_l]
    _d['title'], _d['desc'], _d['ogtitle'] = _x['title'], _x['desc'], _x['ogtitle']
    _d['sub'] = [_d['sub'][0], _x['sub1'], _d['sub'][2], _d['sub'][3]]
    _d['paras'] = [_x['p0']] + _d['paras'][1:]
    _d['card'] = dict(_d['card'], desc=_x['card'])
    _d['equip'] = KEY[_l] + [e for e in _d['equip'] if not any(w in e.lower() for w in ('ducha', 'dutxa', 'shower', 'douche', 'molinet', 'windlass', 'guindeau', 'camarote en proa', 'cabina a proa', 'bow cabin', 'cabine avant'))]
    assert len(_x['title']) <= 62, (_l, len(_x['title']))


if __name__ == '__main__':
    for lang in ('es', 'ca', 'en', 'fr'):
        build(lang)
        add_catalog(lang)
