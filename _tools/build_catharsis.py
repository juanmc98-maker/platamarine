#!/usr/bin/env python3
"""Genera /catharsis/ en ES/CA/EN/FR a partir de la plantilla de /barcos-nuevos/.
Uso: python3 _tools/build_catharsis.py  (desde la raíz del repo)"""
import re, json, html, urllib.parse, os

ROOT = '.'
BASE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
WA = '34633742973'
SLUG = 'catharsis'
NPH = 10
PRICE = 103990  # PVP sin IVA y sin motores (confirmado por Juan, 20 oct 2026)

def eur(n, lang):
    s = f'{n:,}'
    if lang == 'en':
        return s
    if lang == 'fr':
        return s.replace(',', '\u202f')
    return s.replace(',', '.')

SPEC = {  # dato: (es, ca, en, fr) etiqueta, valor común
 'loa': (('Eslora total', 'Eslora total', 'Length overall', 'Longueur hors tout'), '9,30 m'),
 'lh': (('Eslora de casco', 'Eslora de buc', 'Hull length', 'Longueur de coque'), '9,10 m'),
 'beam': (('Manga', 'Mànega', 'Beam', 'Largeur'), '3,00 m'),
 'draft': (('Calado', 'Calat', 'Draft', 'Tirant d\'eau'), '0,70 – 0,80 m'),
 'head': (('Altura en cabina', 'Alçada a cabina', 'Cabin headroom', 'Hauteur sous barrots'), '1,90 m'),
 'pax': (('Personas', 'Persones', 'People', 'Personnes'), '8'),
 'ce': (('Marcado CE', 'Marcatge CE', 'CE marking', 'Marquage CE'), ('Categoría C (según el astillero)', 'Categoria C (segons la drassana)', 'Category C (as stated by the builder)', 'Catégorie C (selon le chantier)')),
 'fuel': (('Combustible', 'Combustible', 'Fuel', 'Carburant'), '2 × 225 l'),
 'water': (('Agua dulce', 'Aigua dolça', 'Fresh water', 'Eau douce'), '300 l'),
 'black': (('Aguas negras', 'Aigües negres', 'Black water', 'Eaux noires'), '140 l'),
 'weight': (('Peso sin motores', 'Pes sense motors', 'Weight without engines', 'Poids sans moteurs'), ('4.200 kg', '4.200 kg', '4,200 kg', '4\u202f200 kg')),
 'power': (('Potencia máxima admitida', 'Potència màxima admesa', 'Maximum rated power', 'Puissance maximale admise'), ('447 kW (≈ 600 cv)', '447 kW (≈ 600 CV)', '447 kW (≈ 600 hp)', '447 kW (≈ 600 ch)')),
}
LI = ['es', 'ca', 'en', 'fr']

T = {
 'es': dict(
  title='Catharsis 930 nuevo: precio, ficha y fotos · Plata Marine',
  desc='Catharsis 930, crucero fueraborda de 9,30 m fabricado por Avila Marin. Desde 103.990 € +IVA sin motores. Agente en Cataluña.',
  eyebrow='Barcos nuevos', h1='Catharsis 930: crucero fueraborda de 9,30 metros',
  intro='Un barco con timonera, dos camarotes y baño, pensado para pasar el día o unos días a bordo con la familia. Lo fabrica Avila Marin y se pide a fábrica: te ayudo a elegir motores y equipamiento. Soy su agente en Cataluña.',
  kick='Agente en Cataluña', h2='El barco',
  facts=['Fabricado por Avila Marin', 'Casco por infusión al vacío', 'Dos camarotes, baño con ducha y cocina', 'Para dos motores fueraborda: no incluidos, se montan a tu elección con presupuesto aparte', 'Entrega: unos 90 días desde el pedido, más el transporte', 'Transporte desde fábrica hasta Barcelona: no incluido, se presupuesta aparte'],
  d='Timonera con puerta corredera de aluminio de tres hojas, bañera con mesa telescópica y ducha, camarote de proa con cama doble y camarote de invitados. De serie lleva molinete eléctrico, nevera, cocina de dos fuegos, WC eléctrico, focos LED, baterías de servicio y depósitos de acero inoxidable.',
  lic='PER o superior', lic_label='Titulación', price_from='Desde', no_eng='sin motores',
  cta='Pedir presupuesto', wa_txt='Hola Juan, me interesa el Catharsis 930.', photos='Fotos del Catharsis 930',
  opt_h='Equipamiento opcional', opt='Teca sintética, plataforma para auxiliar, luces submarinas, hélice de proa, flaps automáticos, calefacción diésel, toldos de verano e invierno, plotters Raymarine de 9" o 12", equipo de sonido Fusion y placas solares (420 W), entre otros. Te paso el precio de cada opción por escrito.',
  spec_h='Ficha técnica',
  used_h='¿Buscas un barco de ocasión?', used_a='Ver barcos de segunda mano →',
  small='Precio orientativo de octubre de 2026, sin IVA, en fábrica: no incluye motores, equipamiento opcional, transporte, impuesto de matriculación (IEDMT) ni matriculación. El transporte desde fábrica hasta Barcelona no está incluido y se presupuesta aparte. Los motores tampoco están incluidos: se montan a elección del cliente, con presupuesto aparte. Puede cambiar y no es vinculante; el precio final es el del presupuesto por escrito. Ficha técnica según el fabricante; el marcado CE de categoría C es el que indica el astillero. La titulación es orientativa según la eslora: confírmala con tu escuela o con Capitanía. Podemos equivocarnos; si ves un error, avísanos.',
 ),
 'ca': dict(
  title='Catharsis 930 nou: preu, fitxa i fotos · Plata Marine',
  desc='Catharsis 930, creuer fora borda de 9,30 m fabricat per Avila Marin. Des de 103.990 € +IVA sense motors. Agent a Catalunya.',
  eyebrow='Vaixells nous', h1='Catharsis 930: creuer fora borda de 9,30 metres',
  intro='Un vaixell amb timonera, dos camarots i bany, pensat per passar el dia o uns dies a bord amb la família. El fabrica Avila Marin i es demana a fàbrica: t\'ajudo a triar motors i equipament. En sóc l\'agent a Catalunya.',
  kick='Agent a Catalunya', h2='El vaixell',
  facts=['Fabricat per Avila Marin', 'Buc per infusió al buit', 'Dos camarots, bany amb dutxa i cuina', 'Per a dos motors fora borda: no inclosos, es munten a la teva elecció amb pressupost a part', 'Lliurament: uns 90 dies des de la comanda, més el transport', 'Transport des de fàbrica fins a Barcelona: no inclòs, es pressuposta a part'],
  d='Timonera amb porta corredissa d\'alumini de tres fulles, banyera amb taula telescòpica i dutxa, camarot de proa amb llit doble i camarot de convidats. De sèrie porta molinet elèctric, nevera, cuina de dos focs, WC elèctric, focus LED, bateries de servei i dipòsits d\'acer inoxidable.',
  lic='PER o superior', lic_label='Titulació', price_from='Des de', no_eng='sense motors',
  cta='Demanar pressupost', wa_txt='Hola Juan, m\'interessa el Catharsis 930.', photos='Fotos del Catharsis 930',
  opt_h='Equipament opcional', opt='Teca sintètica, plataforma per a auxiliar, llums submarins, hèlix de proa, flaps automàtics, calefacció dièsel, tendals d\'estiu i d\'hivern, plotters Raymarine de 9" o 12", equip de so Fusion i plaques solars (420 W), entre d\'altres. Et passo el preu de cada opció per escrit.',
  spec_h='Fitxa tècnica',
  used_h='Busques un vaixell d\'ocasió?', used_a='Veure vaixells de segona mà →',
  small='Preu orientatiu d\'octubre de 2026, sense IVA, a fàbrica: no inclou motors, equipament opcional, transport, impost de matriculació (IEDMT) ni matriculació. El transport des de fàbrica fins a Barcelona no està inclòs i es pressuposta a part. Els motors tampoc no hi estan inclosos: es munten a elecció del client, amb pressupost a part. Pot canviar i no és vinculant; el preu final és el del pressupost per escrit. Fitxa tècnica segons el fabricant; el marcatge CE de categoria C és el que indica la drassana. La titulació és orientativa segons l\'eslora: confirma-la amb la teva escola o amb Capitania. Ens podem equivocar; si hi veus un error, avisa\'ns.',
 ),
 'en': dict(
  title='New Catharsis 930: price, specs and photos · Plata Marine',
  desc='Catharsis 930, a 9.30 m outboard cruiser built by Avila Marin. From €103,990 +VAT without engines. Agent in Catalonia.',
  eyebrow='New boats', h1='Catharsis 930: a 9.30-metre outboard cruiser',
  intro='A boat with a wheelhouse, two cabins and a bathroom, made for day trips or a few days on board with the family. Built by Avila Marin and ordered from the factory: I help you choose engines and equipment. I am their agent in Catalonia.',
  kick='Agent in Catalonia', h2='The boat',
  facts=['Built by Avila Marin', 'Vacuum-infused hull', 'Two cabins, bathroom with shower and galley', 'For twin outboard engines: not included, fitted to your choice and quoted separately', 'Delivery: about 90 days from order, plus transport', 'Transport from the factory to Barcelona: not included, quoted separately'],
  d='Wheelhouse with a three-panel sliding aluminium door, cockpit with telescopic table and shower, forward cabin with double bed and a guest cabin. Standard equipment includes electric windlass, fridge, two-burner hob, electric toilet, LED searchlight, service batteries and stainless steel tanks.',
  lic='Spanish PER or higher', lic_label='Licence', price_from='From', no_eng='without engines',
  cta='Request a quote', wa_txt='Hi Juan, I am interested in the Catharsis 930.', photos='Photos of the Catharsis 930',
  opt_h='Optional equipment', opt='Synthetic teak, tender platform, underwater lights, bow thruster, automatic trim tabs, diesel heater, summer and winter covers, 9" or 12" Raymarine plotters, Fusion sound system and solar panels (420 W), among others. I will send you the price of each option in writing.',
  spec_h='Specifications',
  used_h='Looking for a used boat?', used_a='See used boats →',
  small='Indicative price as of October 2026, ex-works, excluding VAT: it does not include engines, optional equipment, transport, Spanish registration tax (IEDMT) or registration. Transport from the factory to Barcelona is not included and is quoted separately. Engines are not included either: they are fitted to the customer\'s choice and quoted separately. It may change and is not binding; the final price is the one in the written quote. Specifications as stated by the builder; the CE category C marking is as declared by the builder. The licence shown is indicative, based on length under Spanish rules: please confirm it with your school or the Harbour Master. We may be wrong; if you spot an error, let us know.',
 ),
 'fr': dict(
  title='Catharsis 930 neuf : prix, fiche et photos · Plata Marine',
  desc='Catharsis 930, cruiser hors-bord de 9,30 m construit par Avila Marin. À partir de 103 990 € HT sans moteurs. Agent en Catalogne.',
  eyebrow='Bateaux neufs', h1='Catharsis 930 : cruiser hors-bord de 9,30 mètres',
  intro='Un bateau avec timonerie, deux cabines et salle d\'eau, pensé pour la journée ou quelques jours à bord en famille. Construit par Avila Marin et commandé à l\'usine : je vous aide à choisir les moteurs et l\'équipement. Je suis leur agent en Catalogne.',
  kick='Agent en Catalogne', h2='Le bateau',
  facts=['Construit par Avila Marin', 'Coque en infusion sous vide', 'Deux cabines, salle d\'eau avec douche et cuisine', 'Pour deux moteurs hors-bord : non inclus, montés selon votre choix sur devis séparé', 'Livraison : environ 90 jours après la commande, plus le transport', 'Transport de l\'usine jusqu\'à Barcelone : non inclus, sur devis séparé'],
  d='Timonerie avec porte coulissante en aluminium à trois vantaux, cockpit avec table télescopique et douche, cabine avant avec lit double et cabine invités. En série : guindeau électrique, réfrigérateur, réchaud deux feux, WC électrique, projecteur LED, batteries de service et réservoirs en inox.',
  lic='PER espagnol ou supérieur', lic_label='Permis', price_from='À partir de', no_eng='sans moteurs',
  cta='Demander un devis', wa_txt='Bonjour Juan, le Catharsis 930 m\'intéresse.', photos='Photos du Catharsis 930',
  opt_h='Options', opt='Teck synthétique, plateforme pour annexe, éclairage sous-marin, propulseur d\'étrave, flaps automatiques, chauffage diesel, tauds été et hiver, traceurs Raymarine 9" ou 12", système audio Fusion et panneaux solaires (420 W), entre autres. Je vous envoie le prix de chaque option par écrit.',
  spec_h='Fiche technique',
  used_h='Vous cherchez un bateau d\'occasion ?', used_a='Voir les bateaux d\'occasion →',
  small='Prix indicatif d\'octobre 2026, départ usine, hors TVA : il n\'inclut pas les moteurs, les options, le transport, la taxe d\'immatriculation espagnole (IEDMT) ni l\'immatriculation. Le transport de l\'usine jusqu\'à Barcelone n\'est pas inclus et fait l\'objet d\'un devis séparé. Les moteurs ne sont pas inclus non plus : ils sont montés selon le choix du client, sur devis séparé. Il peut changer et n\'est pas contractuel ; le prix final est celui du devis écrit. Fiche technique selon le constructeur ; le marquage CE catégorie C est celui déclaré par le chantier. Le permis indiqué est indicatif, selon la longueur d\'après les règles espagnoles : vérifiez-le auprès de votre école ou de la Capitainerie. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous. Nous ne parlons pas français : nous utilisons un traducteur, merci de votre indulgence.',
 ),
}
VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': 'HT'}
HINT = {'es': 'Desliza para ver más fotos →', 'ca': 'Llisca per veure més fotos →', 'en': 'Swipe for more photos →', 'fr': 'Faites glisser pour plus de photos →'}

# ---- Ficha completa (v2, 21 oct 2026): fotos del astillero, interior, equipamiento del catálogo Avila (16 oct 2026) ----
NPH = 28
GAL = list(range(1, NPH + 1))
SPOTS_XY = [(25, 64), (33, 44), (50, 50), (62, 70), (77, 50), (18, 52)]

T2 = {
 'es': dict(
  side=['El barco', 'Cubierta', 'Bañera y proa', 'Timonera', 'Interior', 'Motores', 'Equipamiento', 'Ficha técnica', 'Fotos', 'Presupuesto'],
  sub=['Barco nuevo, bajo pedido', '9,30 m con timonera', '2 camarotes y baño', 'Motor fueraborda a elegir'],
  vat_note='sin motores · transporte aparte', see='Ver los datos',
  note='Fotos del astillero: unidad de muestra, algunas hechas en un salón náutico. Pueden mostrar equipamiento opcional.',
  cub_k='Cubierta', cub_h='Un vistazo desde arriba', cub_l='Toca los números para ver qué hay en cada zona.',
  spots=[('Plataforma de popa', 'Plataforma de baño a los dos lados de los motores, con escalera telescópica de 4 peldaños en acero inoxidable.'),
         ('Bañera', 'Sofá, mesa telescópica y ducha. En las fotos lleva el toldo de verano, que es opcional.'),
         ('Timonera', 'Cerrada, con puerta corredera de aluminio de tres hojas. Las placas solares del techo son opcionales.'),
         ('Pasillos laterales', 'Para ir a proa por los dos costados, con candeleros y pasamanos de acero 316.'),
         ('Solárium de proa', 'Zona para tumbarse delante de la timonera, con el molinete eléctrico en la punta.'),
         ('Motores', 'La unidad de las fotos lleva dos fuerabordas. Los motores no van incluidos: se eligen y se presupuestan aparte.')],
  b_k='Bañera y proa', b_h='Fuera se está a gusto',
  b1_h='Bañera con mesa', b1='Sofá en U con mesa telescópica de pie cromado, ducha de bañera y luces de cortesía en los peldaños. Desde aquí se entra a la timonera por la puerta corredera, que se abre del todo.',
  b2_h='Proa y pasillos', b2='Solárium en proa y molinete eléctrico de 900 W con pulsadores de pie y roldana de acero 316. Se llega por los pasillos laterales, con pasamanos a lo largo de la timonera.',
  t_k='Timonera', t_h='Un salón cerrado con vistas',
  t1_h='Salón con cocina', t1='Mesa telescópica, sofá y cocina con dos fuegos, fregadero y nevera de 65 litros. Suelo laminado marino, luz LED en techo y suelo, y enchufes USB, 12 V y 220 V.',
  t2_h='Puesto de mando', t2='Asiento del patrón de doble posición y abatible, limpiaparabrisas con lavado y foco LED con mando a distancia. El plotter Raymarine de 9" o 12" es opcional.',
  mid='¿Te preparo un presupuesto con los motores y las opciones que quieras?', mid_b='Pedir presupuesto por WhatsApp',
  i_k='Interior', i_h='Para dormir a bordo',
  i1_h='Camarote principal', i1='Cama doble con almacenaje debajo, armario, escotilla de 50 × 50 cm y dos portillos. Además hay un camarote de invitados con cama, armario y portillo.',
  i2_h='Baño', i2='WC eléctrico de taza grande, lavabo, grifo con ducha y portillo. Paneles de madera en paredes y puertas.',
  m_k='Motores', m_h='Tú eliges la motorización',
  m1='Puedes pedir el 930 sin motores o con dos fuerabordas de 250 cv (Mercury o Suzuki) ya montados por 49.490 € + impuestos; lo configuras más abajo. Si prefieres otra marca o potencia, te paso el presupuesto por escrito. La potencia máxima admitida es de 447 kW (unos 600 cv). La unidad de las fotos lleva dos fuerabordas Mercury.',
  m2='El astillero no publica velocidades ni consumos, porque dependen mucho de los motores que se monten. Si te interesa una motorización concreta, se los pido por escrito.',
  e_k='Equipamiento', e_h='Qué lleva de serie y qué es opcional',
  std_h='De serie', opt_h='Opcional',
  std=['Molinete eléctrico de 900 W con pulsadores de pie', 'Puerta corredera de aluminio de tres hojas', 'Asiento del patrón de doble posición', 'Mesa telescópica en timonera y en bañera', 'Cocina de dos fuegos y fregadero', 'Nevera de 65 l', 'WC eléctrico y grifo con ducha', 'Ducha de bañera', 'Escalera de baño de 4 peldaños', 'Foco LED con mando a distancia', 'Limpiaparabrisas con lavado', 'Luz LED en techo, suelo y peldaños', 'Enchufes USB, 12 V y 220 V', 'Toma de corriente de puerto con cable', 'Batería de motor de 100 Ah y 3 baterías de servicio de 200 Ah', 'Indicadores de nivel de depósitos', 'Luces de navegación y de fondeo', 'Candeleros y pasamanos de acero 316', 'Equipo de música', 'Portacañas cromado'],
  opt=['Teca sintética en cubierta', 'Hélice de proa', 'Flaps', 'Luces subacuáticas', 'Calefacción', 'Placas solares', 'Toldos de verano e invierno', 'Cortinas', 'Equipo de sonido Fusion', 'Plotter Raymarine de 9" o 12"', 'VHF', 'Televisión', 'Nevera extra de 30 l', 'Boiler', 'Antiincrustante', 'Techo solar', 'Ancla', 'Vivero'],
  e_note='Te paso el precio de cada opción por escrito.',
  f_k='Ficha técnica', f_h='Los datos', f_pax='personas', f_ce='Categoría CE',
  extra=[('Construcción', 'Poliéster compuesto, casco por infusión al vacío'), ('Camarotes', '2 (principal y de invitados)'), ('Baños', '1'), ('Plazo de entrega', 'A consultar: se confirma siempre por escrito antes del pedido'), ('Transporte', 'Desde fábrica hasta Barcelona, aparte (se presupuesta)')],
  g_h='Todas las fotos', g_l='Toca una foto para verla en grande.',
  how_h='Cómo se compra', how=['Me dices qué motores y opciones te interesan.', 'Te paso el presupuesto por escrito: barco, opciones, motores, transporte e impuestos.', 'Se hace el pedido con la señal que marque el contrato y el astillero lo fabrica.', 'Transporte, matriculación y entrega en Cataluña.'],
  why_h='Cómo lo veo', why='Lo veo para una pareja o una familia que quiera pasar el día en calas y alguna noche a bordo, con la timonera cerrada para alargar la temporada. Con fuerabordas el motor queda fuera del barco y el mantenimiento suele ser más sencillo. Para gobernarlo hace falta el PER o un título superior.',
  end_h='¿Te preparo un presupuesto?', end_p='Dime qué motores y opciones te interesan y te paso el precio por escrito, sin compromiso.',
  end_b='Pedir presupuesto', wa_ctx_txt='Hola Juan, me interesa el Catharsis 930. ¿Me preparas un presupuesto?',
  photo_alt=['Catharsis 930 navegando', 'Catharsis 930 visto desde arriba', 'Timonera con salón y cocina', 'Puesto de mando', 'Bañera y entrada a la timonera', 'Bañera con sofá y mesa', 'Camarote principal', 'Baño', 'Interior de madera', 'Solárium de proa', 'Pasillo lateral y proa', 'Popa con plataforma y motores'],
  photo='foto', close='Cerrar', prev='Anterior', next='Siguiente',
 ),
 'ca': dict(
  side=['El vaixell', 'Coberta', 'Banyera i proa', 'Timonera', 'Interior', 'Motors', 'Equipament', 'Fitxa tècnica', 'Fotos', 'Pressupost'],
  sub=['Vaixell nou, per encàrrec', '9,30 m amb timonera', '2 camarots i bany', 'Motor fora borda a triar'],
  vat_note='sense motors · transport a part', see='Veure les dades',
  note='Fotos de la drassana: unitat de mostra, algunes fetes en un saló nàutic. Poden mostrar equipament opcional.',
  cub_k='Coberta', cub_h='Un cop d\'ull des de dalt', cub_l='Toca els números per veure què hi ha a cada zona.',
  spots=[('Plataforma de popa', 'Plataforma de bany als dos costats dels motors, amb escala telescòpica de 4 graons d\'acer inoxidable.'),
         ('Banyera', 'Sofà, taula telescòpica i dutxa. A les fotos porta el tendal d\'estiu, que és opcional.'),
         ('Timonera', 'Tancada, amb porta corredissa d\'alumini de tres fulles. Les plaques solars del sostre són opcionals.'),
         ('Passadissos laterals', 'Per anar a proa pels dos costats, amb candeleros i passamans d\'acer 316.'),
         ('Solàrium de proa', 'Zona per estirar-se davant de la timonera, amb el molinet elèctric a la punta.'),
         ('Motors', 'La unitat de les fotos porta dos fora bordes. Els motors no hi estan inclosos: es trien i es pressuposten a part.')],
  b_k='Banyera i proa', b_h='A fora s\'hi està bé',
  b1_h='Banyera amb taula', b1='Sofà en U amb taula telescòpica de peu cromat, dutxa de banyera i llums de cortesia als graons. Des d\'aquí s\'entra a la timonera per la porta corredissa, que s\'obre del tot.',
  b2_h='Proa i passadissos', b2='Solàrium a proa i molinet elèctric de 900 W amb polsadors de peu i corriola d\'acer 316. S\'hi arriba pels passadissos laterals, amb passamans al llarg de la timonera.',
  t_k='Timonera', t_h='Un saló tancat amb vistes',
  t1_h='Saló amb cuina', t1='Taula telescòpica, sofà i cuina amb dos focs, aigüera i nevera de 65 litres. Terra laminat marí, llum LED al sostre i al terra, i endolls USB, 12 V i 220 V.',
  t2_h='Lloc de comandament', t2='Seient del patró de doble posició i abatible, eixugaparabrisa amb rentat i focus LED amb comandament a distància. El plotter Raymarine de 9" o 12" és opcional.',
  mid='Et preparo un pressupost amb els motors i les opcions que vulguis?', mid_b='Demanar pressupost per WhatsApp',
  i_k='Interior', i_h='Per dormir a bord',
  i1_h='Camarot principal', i1='Llit doble amb emmagatzematge a sota, armari, escotilla de 50 × 50 cm i dos portells. A més hi ha un camarot de convidats amb llit, armari i portell.',
  i2_h='Bany', i2='WC elèctric de tassa gran, lavabo, aixeta amb dutxa i portell. Panells de fusta a les parets i a les portes.',
  m_k='Motors', m_h='Tu tries la motorització',
  m1='Pots demanar el 930 sense motors o amb dos fora bordes de 250 CV (Mercury o Suzuki) ja muntats per 49.490 € + impostos; el configures més avall. Si prefereixes una altra marca o potència, et passo el pressupost per escrit. La potència màxima admesa és de 447 kW (uns 600 CV). La unitat de les fotos porta dos fora bordes Mercury.',
  m2='La drassana no publica velocitats ni consums, perquè depenen molt dels motors que s\'hi muntin. Si t\'interessa una motorització concreta, te\'ls demano per escrit.',
  e_k='Equipament', e_h='Què porta de sèrie i què és opcional',
  std_h='De sèrie', opt_h='Opcional',
  std=['Molinet elèctric de 900 W amb polsadors de peu', 'Porta corredissa d\'alumini de tres fulles', 'Seient del patró de doble posició', 'Taula telescòpica a la timonera i a la banyera', 'Cuina de dos focs i aigüera', 'Nevera de 65 l', 'WC elèctric i aixeta amb dutxa', 'Dutxa de banyera', 'Escala de bany de 4 graons', 'Focus LED amb comandament a distància', 'Eixugaparabrisa amb rentat', 'Llum LED al sostre, al terra i als graons', 'Endolls USB, 12 V i 220 V', 'Presa de corrent de port amb cable', 'Bateria de motor de 100 Ah i 3 bateries de servei de 200 Ah', 'Indicadors de nivell dels dipòsits', 'Llums de navegació i de fondeig', 'Candeleros i passamans d\'acer 316', 'Equip de música', 'Portacanyes cromat'],
  opt=['Teca sintètica a coberta', 'Hèlix de proa', 'Flaps', 'Llums subaquàtics', 'Calefacció', 'Plaques solars', 'Tendals d\'estiu i d\'hivern', 'Cortines', 'Equip de so Fusion', 'Plotter Raymarine de 9" o 12"', 'VHF', 'Televisió', 'Nevera extra de 30 l', 'Boiler', 'Antiincrustant', 'Sostre solar', 'Àncora', 'Viver'],
  e_note='Et passo el preu de cada opció per escrit.',
  f_k='Fitxa tècnica', f_h='Les dades', f_pax='persones', f_ce='Categoria CE',
  extra=[('Construcció', 'Polièster compost, buc per infusió al buit'), ('Camarots', '2 (principal i de convidats)'), ('Banys', '1'), ('Termini de lliurament', 'A consultar: es confirma sempre per escrit abans de la comanda'), ('Transport', 'Des de fàbrica fins a Barcelona, a part (es pressuposta)')],
  g_h='Totes les fotos', g_l='Toca una foto per veure-la en gran.',
  how_h='Com es compra', how=['Em dius quins motors i opcions t\'interessen.', 'Et passo el pressupost per escrit: vaixell, opcions, motors, transport i impostos.', 'Es fa la comanda amb el senyal que marqui el contracte i la drassana el fabrica.', 'Transport, matriculació i lliurament a Catalunya.'],
  why_h='Com el veig', why='El veig per a una parella o una família que vulgui passar el dia a les cales i alguna nit a bord, amb la timonera tancada per allargar la temporada. Amb fora bordes el motor queda fora del vaixell i el manteniment sol ser més senzill. Per governar-lo cal el PER o un títol superior.',
  end_h='Et preparo un pressupost?', end_p='Digues-me quins motors i opcions t\'interessen i et passo el preu per escrit, sense compromís.',
  end_b='Demanar pressupost', wa_ctx_txt='Hola Juan, m\'interessa el Catharsis 930. Em prepares un pressupost?',
  photo_alt=['Catharsis 930 navegant', 'Catharsis 930 vist des de dalt', 'Timonera amb saló i cuina', 'Lloc de comandament', 'Banyera i entrada a la timonera', 'Banyera amb sofà i taula', 'Camarot principal', 'Bany', 'Interior de fusta', 'Solàrium de proa', 'Passadís lateral i proa', 'Popa amb plataforma i motors'],
  photo='foto', close='Tancar', prev='Anterior', next='Següent',
 ),
 'en': dict(
  side=['The boat', 'Deck', 'Cockpit and bow', 'Wheelhouse', 'Interior', 'Engines', 'Equipment', 'Specifications', 'Photos', 'Quote'],
  sub=['New boat, built to order', '9.30 m with wheelhouse', '2 cabins and bathroom', 'Outboard engines of your choice'],
  vat_note='without engines · transport extra', see='See the specs',
  note='Builder\'s photos: a demo unit, some taken at a boat show. They may show optional equipment.',
  cub_k='Deck', cub_h='A look from above', cub_l='Tap the numbers to see each area.',
  spots=[('Stern platform', 'Swim platform on both sides of the engines, with a telescopic 4-step stainless steel ladder.'),
         ('Cockpit', 'Sofa, telescopic table and shower. The photos show the optional summer awning.'),
         ('Wheelhouse', 'Enclosed, with a three-panel sliding aluminium door. The solar panels on the roof are optional.'),
         ('Side decks', 'To walk forward on both sides, with 316 stainless guardrails and handrails.'),
         ('Bow sunbed', 'A place to lie in the sun ahead of the wheelhouse, with the electric windlass at the bow.'),
         ('Engines', 'The boat in the photos has twin outboards. Engines are not included: you choose them and they are quoted separately.')],
  b_k='Cockpit and bow', b_h='Good to be outside',
  b1_h='Cockpit with table', b1='U-shaped sofa with a telescopic chrome-leg table, cockpit shower and LED step lights. The sliding door into the wheelhouse opens fully.',
  b2_h='Bow and side decks', b2='Bow sunbed and a 900 W electric windlass with foot switches and a 316 stainless bow roller. You get there along the side decks, with handrails along the wheelhouse.',
  t_k='Wheelhouse', t_h='An enclosed saloon with a view',
  t1_h='Saloon and galley', t1='Telescopic table, sofa and a galley with two-burner hob, sink and 65-litre fridge. Marine laminate floor, LED ceiling and floor lights, and USB, 12 V and 220 V sockets.',
  t2_h='Helm', t2='Dual-position folding helm seat, windscreen wiper with washer and a remote-controlled LED searchlight. A 9" or 12" Raymarine plotter is optional.',
  mid='Shall I prepare a quote with the engines and options you want?', mid_b='Ask for a quote on WhatsApp',
  i_k='Interior', i_h='To sleep on board',
  i1_h='Master cabin', i1='Double bed with storage underneath, wardrobe, 50 × 50 cm hatch and two portholes. There is also a guest cabin with bed, wardrobe and porthole.',
  i2_h='Bathroom', i2='Large-bowl electric toilet, washbasin, mixer tap with shower head and porthole. Wood panels on walls and doors.',
  m_k='Engines', m_h='You choose the engines',
  m1='You can order the 930 without engines or with twin 250 hp outboards (Mercury or Suzuki) fitted for €49,490 + taxes; configure it below. If you prefer another brand or power, I will send you a written quote. Maximum rated power is 447 kW (about 600 hp). The boat in the photos has twin Mercury outboards.',
  m2='The builder does not publish speed or fuel figures, as they depend heavily on the engines fitted. If you are interested in a specific set-up, I will ask for them in writing.',
  e_k='Equipment', e_h='What is standard and what is optional',
  std_h='Standard', opt_h='Optional',
  std=['900 W electric windlass with foot switches', 'Three-panel sliding aluminium door', 'Dual-position helm seat', 'Telescopic tables in wheelhouse and cockpit', 'Two-burner hob and sink', '65 l fridge', 'Electric toilet and shower tap', 'Cockpit shower', '4-step swim ladder', 'Remote-controlled LED searchlight', 'Windscreen wiper with washer', 'LED ceiling, floor and step lights', 'USB, 12 V and 220 V sockets', 'Shore power socket and cable', '100 Ah engine battery and 3 × 200 Ah service batteries', 'Tank level indicators', 'Navigation and anchor lights', '316 stainless guardrails and handrails', 'Music system', 'Chrome rod holder'],
  opt=['Synthetic teak deck', 'Bow thruster', 'Trim tabs', 'Underwater lights', 'Cabin heater', 'Solar panels', 'Summer and winter awnings', 'Curtains', 'Fusion sound system', '9" or 12" Raymarine plotter', 'VHF radio', 'TV', 'Extra 30 l fridge', 'Water heater', 'Antifouling', 'Sunroof', 'Anchor', 'Live bait tank'],
  e_note='I will send you the price of each option in writing.',
  f_k='Specifications', f_h='The figures', f_pax='people', f_ce='CE category',
  extra=[('Construction', 'Composite polyester, vacuum-infused hull'), ('Cabins', '2 (master and guest)'), ('Bathrooms', '1'), ('Delivery time', 'On request: always confirmed in writing before ordering'), ('Transport', 'From the factory to Barcelona, extra (quoted separately)')],
  g_h='All photos', g_l='Tap a photo to see it larger.',
  how_h='How buying works', how=['You tell me which engines and options you want.', 'I send you a written quote: boat, options, engines, transport and taxes.', 'The order is placed with the deposit set in the contract and the builder builds the boat.', 'Transport, registration and handover in Catalonia.'],
  why_h='How I see it', why='I see it for a couple or a family who want days in coves and the odd night on board, with an enclosed wheelhouse to stretch the season. With outboards the engines sit outside the boat and maintenance is usually simpler. Under Spanish rules it needs the PER licence or higher.',
  end_h='Shall I prepare a quote?', end_p='Tell me which engines and options you are interested in and I will send you the price in writing, with no obligation.',
  end_b='Request a quote', wa_ctx_txt='Hi Juan, I am interested in the Catharsis 930. Could you prepare a quote?',
  photo_alt=['Catharsis 930 underway', 'Catharsis 930 from above', 'Wheelhouse with saloon and galley', 'Helm', 'Cockpit and wheelhouse entrance', 'Cockpit with sofa and table', 'Master cabin', 'Bathroom', 'Wooden interior', 'Bow sunbed', 'Side deck and bow', 'Stern with platform and engines'],
  photo='photo', close='Close', prev='Previous', next='Next',
 ),
 'fr': dict(
  side=['Le bateau', 'Pont', 'Cockpit et proue', 'Timonerie', 'Intérieur', 'Moteurs', 'Équipement', 'Fiche technique', 'Photos', 'Devis'],
  sub=['Bateau neuf, sur commande', '9,30 m avec timonerie', '2 cabines et salle d\'eau', 'Hors-bord au choix'],
  vat_note='sans moteurs · transport en sus', see='Voir les données',
  note='Photos du chantier : unité de démonstration, certaines prises dans un salon nautique. Elles peuvent montrer des options.',
  cub_k='Pont', cub_h='Vu d\'en haut', cub_l='Touchez les numéros pour voir chaque zone.',
  spots=[('Plateforme arrière', 'Plateforme de bain de chaque côté des moteurs, avec échelle télescopique inox à 4 marches.'),
         ('Cockpit', 'Banquette, table télescopique et douche. Sur les photos, le taud d\'été, en option.'),
         ('Timonerie', 'Fermée, avec porte coulissante en aluminium à trois vantaux. Les panneaux solaires du toit sont en option.'),
         ('Passavants', 'Pour aller à l\'avant des deux côtés, avec filières et mains courantes en inox 316.'),
         ('Bain de soleil avant', 'Pour s\'allonger devant la timonerie, avec le guindeau électrique à la proue.'),
         ('Moteurs', 'L\'unité des photos a deux hors-bord. Les moteurs ne sont pas inclus : vous les choisissez, sur devis séparé.')],
  b_k='Cockpit et proue', b_h='On est bien dehors',
  b1_h='Cockpit avec table', b1='Banquette en U avec table télescopique à pied chromé, douche de cockpit et éclairage LED des marches. La porte coulissante de la timonerie s\'ouvre entièrement.',
  b2_h='Proue et passavants', b2='Bain de soleil à l\'avant et guindeau électrique de 900 W avec commandes au pied et davier inox 316. On y accède par les passavants, avec mains courantes le long de la timonerie.',
  t_k='Timonerie', t_h='Un carré fermé avec vue',
  t1_h='Carré et cuisine', t1='Table télescopique, banquette et cuisine avec réchaud deux feux, évier et réfrigérateur de 65 litres. Sol stratifié marine, éclairage LED au plafond et au sol, prises USB, 12 V et 220 V.',
  t2_h='Poste de pilotage', t2='Siège pilote double position rabattable, essuie-glace avec lave-glace et projecteur LED télécommandé. Le traceur Raymarine 9" ou 12" est en option.',
  mid='Je vous prépare un devis avec les moteurs et les options de votre choix ?', mid_b='Demander un devis sur WhatsApp',
  i_k='Intérieur', i_h='Pour dormir à bord',
  i1_h='Cabine principale', i1='Lit double avec rangement dessous, penderie, écoutille de 50 × 50 cm et deux hublots. Il y a aussi une cabine invités avec lit, penderie et hublot.',
  i2_h='Salle d\'eau', i2='WC électrique grande cuvette, lavabo, mitigeur avec douchette et hublot. Panneaux en bois sur les cloisons et les portes.',
  m_k='Moteurs', m_h='Vous choisissez la motorisation',
  m1='Vous pouvez commander le 930 sans moteurs ou avec deux hors-bord de 250 ch (Mercury ou Suzuki) installés pour 49 490 € + taxes ; configurez-le plus bas. Si vous préférez une autre marque ou puissance, je vous envoie un devis écrit. Puissance maximale admise : 447 kW (environ 600 ch). L\'unité des photos a deux hors-bord Mercury.',
  m2='Le chantier ne publie ni vitesses ni consommations, car elles dépendent beaucoup des moteurs. Si une motorisation vous intéresse, je les demande par écrit.',
  e_k='Équipement', e_h='Ce qui est de série et ce qui est en option',
  std_h='De série', opt_h='En option',
  std=['Guindeau électrique 900 W avec commandes au pied', 'Porte coulissante en aluminium à trois vantaux', 'Siège pilote double position', 'Tables télescopiques en timonerie et au cockpit', 'Réchaud deux feux et évier', 'Réfrigérateur 65 l', 'WC électrique et mitigeur avec douchette', 'Douche de cockpit', 'Échelle de bain 4 marches', 'Projecteur LED télécommandé', 'Essuie-glace avec lave-glace', 'Éclairage LED plafond, sol et marches', 'Prises USB, 12 V et 220 V', 'Prise de quai avec câble', 'Batterie moteur 100 Ah et 3 batteries de service 200 Ah', 'Jauges de réservoirs', 'Feux de navigation et de mouillage', 'Filières et mains courantes inox 316', 'Système audio', 'Porte-cannes chromé'],
  opt=['Teck synthétique', 'Propulseur d\'étrave', 'Flaps', 'Éclairage sous-marin', 'Chauffage', 'Panneaux solaires', 'Tauds été et hiver', 'Rideaux', 'Système audio Fusion', 'Traceur Raymarine 9" ou 12"', 'VHF', 'Télévision', 'Réfrigérateur supplémentaire 30 l', 'Chauffe-eau', 'Antifouling', 'Toit ouvrant', 'Ancre', 'Vivier'],
  e_note='Je vous envoie le prix de chaque option par écrit.',
  f_k='Fiche technique', f_h='Les données', f_pax='personnes', f_ce='Catégorie CE',
  extra=[('Construction', 'Polyester composite, coque en infusion sous vide'), ('Cabines', '2 (principale et invités)'), ('Salles d\'eau', '1'), ('Délai de livraison', 'Sur demande : toujours confirmé par écrit avant la commande'), ('Transport', 'De l\'usine jusqu\'à Barcelone, en sus (sur devis)')],
  g_h='Toutes les photos', g_l='Touchez une photo pour l\'agrandir.',
  how_h='Comment acheter', how=['Vous me dites quels moteurs et options vous intéressent.', 'Je vous envoie le devis écrit : bateau, options, moteurs, transport et taxes.', 'La commande se fait avec l\'acompte prévu au contrat et le chantier construit le bateau.', 'Transport, immatriculation et livraison en Catalogne.'],
  why_h='Mon avis', why='Je le vois pour un couple ou une famille qui veut passer la journée dans les criques et quelques nuits à bord, avec une timonerie fermée pour prolonger la saison. Avec des hors-bord, le moteur est à l\'extérieur et l\'entretien est en général plus simple. En Espagne, il faut le permis PER ou supérieur.',
  end_h='Je vous prépare un devis ?', end_p='Dites-moi quels moteurs et options vous intéressent et je vous envoie le prix par écrit, sans engagement.',
  end_b='Demander un devis', wa_ctx_txt='Bonjour Juan, le Catharsis 930 m\'intéresse. Pouvez-vous me préparer un devis ?',
  photo_alt=['Catharsis 930 en navigation', 'Catharsis 930 vu d\'en haut', 'Timonerie avec carré et cuisine', 'Poste de pilotage', 'Cockpit et entrée de la timonerie', 'Cockpit avec banquette et table', 'Cabine principale', 'Salle d\'eau', 'Intérieur en bois', 'Bain de soleil avant', 'Passavant et proue', 'Arrière avec plateforme et moteurs'],
  photo='photo', close='Fermer', prev='Précédente', next='Suivante',
 ),
}
for _l in T2:
    T[_l]['small'] = T[_l]['small'].replace('Ficha técnica según el fabricante', 'Fotos y ficha técnica del fabricante; las fotos pueden mostrar equipamiento opcional').replace('Fitxa tècnica segons el fabricant', 'Fotos i fitxa tècnica del fabricant; les fotos poden mostrar equipament opcional').replace('Specifications as stated by the builder', 'Photos and specifications from the builder; photos may show optional equipment').replace('Fiche technique selon le constructeur', 'Photos et fiche technique du constructeur ; les photos peuvent montrer des options')

VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': 'HT'}

CSS = """
.ct .v2-hero-in .price small{display:block;font-size:14px;font-weight:500;color:rgba(255,255,255,.85);margin-top:4px}
.ct .vat{color:#ff8a80;font-size:.62em;font-weight:700;margin-left:4px}
.ct-two{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.ct-two h3{font-size:1.15rem;margin:0 0 10px}
.ct-tags{list-style:none;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:8px}
.ct-tags li{background:#fff;border:1px solid rgba(14,48,66,.16);border-radius:999px;padding:6px 12px;font-size:14px;line-height:1.3}
.ct-tags.opt li{background:transparent;border-style:dashed}
.ct-gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px}
.ct-gal button{padding:0;border:0;background:none;cursor:zoom-in;border-radius:8px;overflow:hidden;aspect-ratio:4/3}
.ct-gal img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .25s}
.ct-gal button:hover img{transform:scale(1.04)}
.ct-gal button:focus-visible{outline:3px solid var(--wa);outline-offset:2px}
.ct-lb{position:fixed;inset:0;z-index:100;background:rgba(5,15,22,.94);display:flex;align-items:center;justify-content:center}
.ct-lb[hidden]{display:none}
.ct-lb img{max-width:92vw;max-height:84vh;object-fit:contain;border-radius:6px}
.ct-lb button{position:absolute;background:rgba(255,255,255,.12);color:#fff;border:0;border-radius:50%;width:46px;height:46px;font-size:26px;line-height:1;cursor:pointer}
.ct-lb .x{top:14px;right:14px}.ct-lb .p{left:12px;top:50%;transform:translateY(-50%)}.ct-lb .n{right:12px;top:50%;transform:translateY(-50%)}
.ct-lb p{position:absolute;bottom:14px;left:0;right:0;text-align:center;color:rgba(255,255,255,.8);font-size:14px;margin:0}
.ct-how{counter-reset:s;list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.ct-how li{counter-increment:s;background:#fff;border:1px solid rgba(14,48,66,.12);border-radius:12px;padding:16px;font-size:15px;line-height:1.45}
.ct-how li:before{content:counter(s);display:flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:var(--wa);color:#fff;font-weight:700;margin-bottom:8px}
.ct-why{max-width:760px;font-size:1.05rem;line-height:1.6;color:var(--ink-2)}
@media (max-width:820px){.ct-two{grid-template-columns:1fr}.ct-how{grid-template-columns:1fr 1fr}}
@media (max-width:520px){.ct-how{grid-template-columns:1fr}.ct-gal{grid-template-columns:repeat(2,1fr)}}
"""

JS = """<script>
(function(){var g=document.getElementById('ct-gal');if(!g)return;var b=g.querySelectorAll('button'),lb=document.getElementById('ct-lb'),im=lb.querySelector('img'),c=lb.querySelector('p'),i=0,last=null;
function show(k){i=(k+b.length)%b.length;im.src=b[i].getAttribute('data-full');im.alt=b[i].querySelector('img').alt;c.textContent=(i+1)+' / '+b.length}
function open(k){last=document.activeElement;show(k);lb.hidden=false;document.body.style.overflow='hidden';lb.querySelector('.x').focus()}
function close(){lb.hidden=true;document.body.style.overflow='';if(last)last.focus()}
for(var k=0;k<b.length;k++)(function(k){b[k].addEventListener('click',function(){open(k)})})(k);
lb.querySelector('.x').onclick=close;lb.querySelector('.p').onclick=function(){show(i-1)};lb.querySelector('.n').onclick=function(){show(i+1)};
lb.addEventListener('click',function(e){if(e.target===lb)close()});
var sx=null;lb.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});lb.addEventListener('touchend',function(e){if(sx===null)return;var d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>40)show(i+(d<0?1:-1));sx=null});
document.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
})();
</script>"""


def ph(i, alt, sizes='(max-width:820px) 100vw, 560px', lazy=True):
    return (f'<img src="/{SLUG}/fotos/catharsis-930-{i}-m.jpg" srcset="/{SLUG}/fotos/catharsis-930-{i}-m.jpg 900w, /{SLUG}/fotos/catharsis-930-{i}.jpg 1600w" '
            f'sizes="{sizes}" alt="{html.escape(alt)}"' + (' loading="lazy"' if lazy else '') + ' decoding="async">')


def build(lang):
    p = LANGS[lang]
    li = LI.index(lang)
    tpl = open(f'{ROOT}{p}/barcos-nuevos/index.html', encoding='utf-8').read()
    t = T[lang]; u = T2[lang]
    url = f'{BASE}{p}/{SLUG}/'
    head, rest = tpl.split('</head>', 1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(t["title"])}</title>', head)
    for k in ('name="description"', 'property="og:description"'):
        head = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc']), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(t['title']), head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', f'\\g<1>{BASE}/{SLUG}/fotos/catharsis-930-1.jpg', head)
    head = re.sub(r'<meta property="og:image:width"[^>]*>\n?<meta property="og:image:height"[^>]*>', '<meta property="og:image:width" content="1600">\n<meta property="og:image:height" content="900">', head)
    head = head.replace('/barcos-nuevos/', f'/{SLUG}/')
    crumbs = {'es': ('Inicio', 'Barcos en venta', 'Barcos nuevos'), 'ca': ('Inici', 'Vaixells en venda', 'Vaixells nous'), 'en': ('Home', 'Boats for sale', 'New boats'), 'fr': ('Accueil', 'Bateaux à vendre', 'Bateaux neufs')}[lang]
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f"{BASE}{p}/"},
            {"@type": "ListItem", "position": 2, "name": crumbs[1], "item": f"{BASE}{p}/barcos/"},
            {"@type": "ListItem", "position": 3, "name": crumbs[2], "item": f"{BASE}{p}/barcos-nuevos/"},
            {"@type": "ListItem", "position": 4, "name": "Catharsis 930", "item": url}]},
        {"@context": "https://schema.org", "@type": "Product", "name": "Catharsis 930", "brand": {"@type": "Brand", "name": "Catharsis"},
         "manufacturer": {"@type": "Organization", "name": "Avila Marin"}, "image": [f"{BASE}/{SLUG}/fotos/catharsis-930-{i}.jpg" for i in (1, 3, 7)], "description": t['d'],
         "offers": {"@type": "Offer", "price": str(PRICE), "priceCurrency": "EUR", "availability": "https://schema.org/PreOrder", "url": url,
                    "priceSpecification": {"@type": "PriceSpecification", "price": str(PRICE), "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}},
    ]
    head = head.replace('<style>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '<style>', 1)
    head = head.replace('</style>', CSS + '</style>', 1)
    head += '<link rel="stylesheet" href="/barcos/ficha-v2.css?v=20261011b">\n<script src="/barcos/ficha-v2.js?v=20261011" defer></script>\n<script src="/catharsis/cath-config.js?v=20261028" defer></script>\n'

    body = rest.replace('/barcos-nuevos/" aria-current', f'/{SLUG}/" aria-current')
    body = re.sub(r'(<div class="langsw".*?</div>)', lambda m: m.group(1).replace('/barcos-nuevos/', f'/{SLUG}/'), body, flags=re.S)
    A = u['photo_alt']
    wa = f'https://wa.me/{WA}?text=' + urllib.parse.quote(u['wa_ctx_txt'])
    def wbtn(txt, ctx, cls='btn btn-wa'):
        return f'<a class="{cls}" href="{wa}" target="_blank" rel="noopener" data-wa-context="{ctx}">{html.escape(txt)}</a>'
    ids = ['barco', 'cubierta', 'banera', 'timonera', 'interior', 'motores', 'equipamiento', 'ficha', 'fotos', 'presupuesto']
    side = ''.join(f'<a href="#{i}"><span>{html.escape(s)}</span><i></i></a>' for i, s in zip(ids, u['side']))
    spots_json = html.escape(json.dumps(u['spots'], ensure_ascii=False))
    dots = ''.join(f'<button type="button" class="v2-dot" style="left:{x}%;top:{y}%" data-t="{k}" aria-expanded="false" aria-label="{html.escape(u["spots"][k][0])}">{k + 1}</button>' for k, (x, y) in enumerate(SPOTS_XY))
    legend = ''.join(f'<li><b>{k + 1} · {html.escape(a)}.</b> {html.escape(b)}</li>' for k, (a, b) in enumerate(u['spots']))
    def alt(i):
        return A[i - 1] if i <= len(A) else f'Catharsis 930 – {u["photo"]} {i}'
    def blk(imgs, h3, txt, rev=False):
        duo = ' v2-duo' if len(imgs) > 1 else ''
        return f'<div class="v2-alt{" rev" if rev else ""}"><div class="v2-ph{duo}">' + ''.join(ph(i, alt(i)) for i in imgs) + f'</div><div><h3>{html.escape(h3)}</h3><p>{html.escape(txt)}</p></div></div>'
    big = [(SPEC['loa'][1], SPEC['loa'][0][li]), (SPEC['beam'][1], SPEC['beam'][0][li]), (SPEC['pax'][1], u['f_pax']), ('C', u['f_ce'])]
    if lang == 'en':
        big = [(v.replace(',', '.'), l) for v, l in big]
    bigh = ''.join(f'<div><b>{html.escape(v)}</b><span>{html.escape(l)}</span></div>' for v, l in big)
    rows = [(lab[li], (val[li] if isinstance(val, tuple) else (val.replace(',', '.') if lang == 'en' else val))) for k, (lab, val) in SPEC.items()]
    rows += [(t['lic_label'], t['lic'])] + u['extra']
    spec = ''.join(f'<div><dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd></div>' for a, b in rows)
    gal = ''.join(f'<button type="button" data-full="/{SLUG}/fotos/catharsis-930-{i}.jpg"><img src="/{SLUG}/fotos/catharsis-930-{i}-m.jpg" alt="{html.escape(alt(i))}" loading="lazy" decoding="async"></button>' for i in GAL)
    std = ''.join(f'<li>{html.escape(x)}</li>' for x in u['std'])
    opt = ''.join(f'<li>{html.escape(x)}</li>' for x in u['opt'])
    how = ''.join(f'<li>{html.escape(x)}</li>' for x in u['how'])
    sub = ''.join(f'<span>{html.escape(s)}</span>' for s in u['sub'])
    main = f'''<main class="boat v2 ct">
<div class="wrap v2-crumb"><p class="crumb"><a href="{p}/">{crumbs[0]}</a> · <a href="{p}/barcos/">{crumbs[1]}</a> · <a href="{p}/barcos-nuevos/">{crumbs[2]}</a> · Catharsis 930</p></div>
<nav class="v2-side" aria-label="{html.escape(u['side'][0])}">{side}</nav>
<section class="v2-hero" id="barco">
<img class="v2-hero-img" src="/{SLUG}/fotos/catharsis-930-1.jpg" srcset="/{SLUG}/fotos/catharsis-930-1-m.jpg 900w, /{SLUG}/fotos/catharsis-930-1.jpg 1600w" sizes="100vw" alt="{html.escape(alt(1))}" width="1600" height="900" fetchpriority="high" decoding="async">
<div class="v2-hero-in wrap head"><div><p class="eyebrow" style="color:rgba(255,255,255,.85)">{t['eyebrow']}</p><h1>Catharsis 930</h1><div class="sub">{sub}</div></div>
<div class="price-box"><p class="price">{t['price_from']} {eur(PRICE, lang)} €<span class="vat">{VAT[lang]}</span><small>{html.escape(u['vat_note'])}</small></p>
<div class="v2-ctas">{wbtn(t['cta'], 'ficha_precio')}<a class="btn v2-ghost" href="#ficha">{html.escape(u['see'])}</a></div></div></div>
</section>
<div class="wrap v2-note"><p class="muted head-note">{html.escape(t['intro'])} {html.escape(u['note'])}</p></div>
<section class="v2-sec" id="cubierta"><div class="wrap">
<p class="v2-k">{u['cub_k']}</p><h2>{html.escape(u['cub_h'])}</h2><p class="v2-lead">{html.escape(u['cub_l'])}</p>
<div class="v2-spots" data-spots="{spots_json}">{ph(2, alt(2), '(max-width:1100px) 100vw, 1100px')}{dots}</div>
<ol class="v2-legend">{legend}</ol>
</div></section>
<section class="v2-sec v2-band" id="banera"><div class="wrap">
<p class="v2-k">{u['b_k']}</p><h2>{html.escape(u['b_h'])}</h2>
{blk([5, 6], u['b1_h'], u['b1'])}
{blk([10, 11], u['b2_h'], u['b2'], True)}
</div></section>
<section class="v2-sec" id="timonera"><div class="wrap">
<p class="v2-k">{u['t_k']}</p><h2>{html.escape(u['t_h'])}</h2>
{blk([3, 9], u['t1_h'], u['t1'])}
{blk([4], u['t2_h'], u['t2'], True)}
<div class="v2-mid"><p>{html.escape(u['mid'])}</p>{wbtn(u['mid_b'], 'ficha_presupuesto')}</div>
</div></section>
<section class="v2-sec v2-band" id="interior"><div class="wrap">
<p class="v2-k">{u['i_k']}</p><h2>{html.escape(u['i_h'])}</h2>
{blk([7], u['i1_h'], u['i1'])}
{blk([8], u['i2_h'], u['i2'], True)}
</div></section>
<section class="v2-sec" id="motores"><div class="wrap">
<p class="v2-k">{u['m_k']}</p><h2>{html.escape(u['m_h'])}</h2>
{blk([12], u['side'][5], u['m1'] + ' ' + u['m2'])}
</div></section>
<section class="v2-sec v2-band" id="equipamiento"><div class="wrap">
<p class="v2-k">{u['e_k']}</p><h2>{html.escape(u['e_h'])}</h2>
<div class="ct-two"><div><h3>{u['std_h']}</h3><ul class="ct-tags">{std}</ul></div><div><h3>{u['opt_h']}</h3><ul class="ct-tags opt">{opt}</ul><p class="v2-small" style="margin-top:12px">{html.escape(u['e_note'])}</p></div></div>
</div></section>
<section class="v2-sec v2-dark" id="ficha"><div class="wrap">
<p class="v2-k">{u['f_k']}</p><h2>{html.escape(u['f_h'])}</h2>
<div class="v2-big">{bigh}</div>
<dl class="specs">{spec}</dl>
<div class="v2-ctas">{wbtn(t['cta'], 'ficha_datos')}</div>
</div></section>
<section class="v2-sec" id="fotos"><div class="wrap">
<h2>{html.escape(u['g_h'])}</h2><p class="v2-lead">{html.escape(u['g_l'])}</p>
<div class="ct-gal" id="ct-gal">{gal}</div>
</div></section>
<div class="ct-lb" id="ct-lb" hidden role="dialog" aria-modal="true" aria-label="{html.escape(u['g_h'])}"><button type="button" class="x" aria-label="{u['close']}">&times;</button><button type="button" class="p" aria-label="{u['prev']}">&#8249;</button><img alt=""><button type="button" class="n" aria-label="{u['next']}">&#8250;</button><p></p></div>
<section class="v2-sec v2-band"><div class="wrap">
<h2>{html.escape(u['how_h'])}</h2><ol class="ct-how">{how}</ol>
<h2 style="margin-top:36px">{html.escape(u['why_h'])}</h2><p class="ct-why">{html.escape(u['why'])}</p>
</div></section>
<section class="v2-end" id="presupuesto" style="--bg:url('/{SLUG}/fotos/catharsis-930-19-m.jpg')"><div class="wrap">
<h2>{html.escape(u['end_h'])}</h2><p>{html.escape(u['end_p'])}</p>
<div class="v2-ctas">{wbtn(u['end_b'], 'ficha_cierre')}<a class="btn v2-ghost" href="{p}/barcos/#segunda-mano">{html.escape(t['used_a'])}</a></div>
</div></section>
<div class="wrap"><p class="nv-small">{html.escape(t['small'])}</p></div>
</main>{JS}'''
    body = re.sub(r'<main class="boat">.*?</main>', lambda m: main, body, flags=re.S)
    out = head + '</head>' + body
    os.makedirs(f'{ROOT}{p}/{SLUG}', exist_ok=True)
    open(f'{ROOT}{p}/{SLUG}/index.html', 'w', encoding='utf-8').write(out)
    print('ok', lang, len(out))


if __name__ == '__main__':
    for l in LANGS:
        build(l)
