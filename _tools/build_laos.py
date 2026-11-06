#!/usr/bin/env python3
"""Genera /laos/ (LAOS Boats y HydroMarin) en ES/CA/EN/FR a partir de la plantilla de /barcos-nuevos/.
Datos: certificados CE (PRS), folletos, fotos y lista de equipamiento que mandó Karol Bartosiewicz (LAOS Boats), oct-nov 2026.
Precios: de momento, a consultar (Juan, 5 nov 2026).
Uso: python3 _tools/build_laos.py  (desde la raíz del repo)"""
import re, json, html, urllib.parse, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_catharsis import CSS as CT_CSS, JS, LANGS, BASE, WA

ROOT = '.'
SLUG = 'laos'
LI = ['es', 'ca', 'en', 'fr']
F = f'/{SLUG}/fotos/laos-'

# Datos del certificado CE (PRS) y de la web del astillero. Peso sin motor.
MODELS = [
 dict(id='laos-605', name='LAOS 605', brand='LAOS Boats', n=6, t='cab',
      spec=dict(lh='6,05 m', beam='2,45 m', draft='0,40 m', disp='1.050 kg', ce='C', pax='6', load='695 kg', fuel=None, pmax='200 cv (147 kW)', shaft='L')),
 dict(id='hydromarin-5830', name='HydroMarin 5830', brand='HydroMarin', n=8, t='lancha',
      spec=dict(lh='5,60 m', beam='2,26 m', draft='0,30 m', disp='770 kg', ce='C', pax='5', load='700 kg', fuel='100 l', pmax='115 cv (85 kW)', shaft='L')),
 dict(id='hydromarin-6020', name='HydroMarin 6020', brand='HydroMarin', n=8, t='lancha',
      spec=dict(lh='6,07 m', beam='2,35 m', draft='0,30 m', disp='950 kg', ce='C', pax='7', load='750 kg', fuel='115 l', pmax='150 cv (110 kW)', shaft='L')),
 dict(id='hydromarin-6930', name='HydroMarin 6930', brand='HydroMarin', n=3, t='lancha',
      spec=dict(lh='6,83 m', beam='2,50 m', draft='0,35 m', disp='1.260 kg', ce='C', pax='8', load='960 kg', fuel='220 l', pmax='250 cv (184 kW)', shaft='XL')),
]
KEY = {'laos-605': '605', 'hydromarin-5830': '5830', 'hydromarin-6020': '6020', 'hydromarin-6930': '6930'}
GAL = [f'{KEY[m["id"]]}-{i}' for m in MODELS for i in range(1, m['n'] + 1)]
HERO = '605-1'

SPEC_L = {
 'lh': ('Eslora de casco', 'Eslora de buc', 'Hull length', 'Longueur de coque'),
 'beam': ('Manga', 'Mànega', 'Beam', 'Largeur'),
 'draft': ('Calado', 'Calat', 'Draft', 'Tirant d\'eau'),
 'disp': ('Peso sin motor', 'Pes sense motor', 'Weight without engine', 'Poids sans moteur'),
 'ce': ('Categoría de diseño CE', 'Categoria de disseny CE', 'CE design category', 'Catégorie de conception CE'),
 'pax': ('Personas', 'Persones', 'People', 'Personnes'),
 'load': ('Carga máxima', 'Càrrega màxima', 'Maximum load', 'Charge maximale'),
 'fuel': ('Combustible', 'Combustible', 'Fuel', 'Carburant'),
 'pmax': ('Potencia máxima', 'Potència màxima', 'Maximum power', 'Puissance maximale'),
 'shaft': ('Pata del motor', 'Cama del motor', 'Engine shaft', 'Arbre moteur'),
}
FUEL605 = ('105 l o 170 l (depósito opcional)', '105 l o 170 l (dipòsit opcional)', '105 l or 170 l (optional tank)', '105 l ou 170 l (réservoir en option)')


def loc(v, lang):
    if lang == 'en':
        v = v.replace('.', ',') if re.search(r'\d\.\d{3}', v) else v
        v = re.sub(r'(\d),(\d)', r'\1.\2', v)
        v = v.replace(' cv', ' hp')
    elif lang == 'fr':
        v = re.sub(r'(\d)\.(\d{3})', '\\1\u202f\\2', v).replace(' cv', ' ch')
    elif lang == 'ca':
        v = v.replace(' cv', ' CV')
    return v


T = {
 'es': dict(
  title='LAOS 605 y HydroMarin: lanchas nuevas, modelos y fotos',
  desc='LAOS 605 y HydroMarin 5830, 6020 y 6930: lanchas de 5,60 a 6,83 m con motor Suzuki montado en fábrica. Precio a consultar. Distribuidor para Cataluña.',
  eyebrow='Barcos nuevos', kick='Distribuidor para Cataluña', h1='LAOS y HydroMarin: lanchas de 5,6 a 6,8 m',
  sub=['De 5,60 a 6,83 m', 'Fueraborda', 'Categoría C', 'Bajo pedido'],
  see='Ver los modelos', cta='Pedir presupuesto',
  intro='LAOS Boats es el astillero que fabrica sus propias lanchas LAOS y la gama HydroMarin. Son barcos de poliéster de 5,6 a 6,8 m, sencillos y bien acabados, que se piden a fábrica y se pueden entregar con el motor Suzuki ya montado. Soy su distribuidor para Cataluña: te ayudo a elegir modelo, motor y opciones, y me encargo de la compra, el transporte y la matriculación.',
  note='Fotos del astillero. Pueden mostrar equipamiento opcional.',
  side=['La marca', 'LAOS 605', 'HydroMarin 5830', 'HydroMarin 6020', 'HydroMarin 6930', 'Opciones', 'Fotos', 'Presupuesto'],
  mh='Cuatro modelos', mh_l='Una lancha con cabina cerrada y tres HydroMarin: dos con camarote en proa y una open para el día.',
  m={'laos-605': ('Pilothouse: cabina cerrada para cualquier tiempo', 'El modelo más nuevo del astillero. Timonera cerrada con puerta corredera, ventanas laterales que se abren y mucho cristal para ver bien desde el puesto de mando. Fuera, bañera con bancos y plataformas de baño. Pensada para pesca, para salir en primavera y otoño y para quien quiere ir a cubierto.'),
     'hydromarin-5830': ('Day cruiser pequeño, con camarote', 'La más compacta: 5,60 m con un camarote tapizado en proa, dos ventanas y escotilla. Dos asientos giratorios, dos mesas plegables y solárium de serie. Con 115 cv como máximo, es la más fácil de mover y de remolcar.'),
     'hydromarin-6020': ('Bowrider: open para el día', 'Lancha abierta de 6,07 m con asientos en proa, dos butacas giratorias en el puesto de mando y dos mesas plegables. Mucha bañera para bañarse, hacer esquí o pescar. Admite hasta 150 cv.'),
     'hydromarin-6930': ('El day cruiser grande', 'La mayor de la gama: 6,83 m y 2,50 m de manga, para 8 personas. Camarote tapizado en proa, solárium, asientos doble e individual, dirección hidráulica y depósito de 220 l de serie. Admite hasta 250 cv.')},
  std={'laos-605': ['Dirección mecánica (hasta 125 cv)', 'Barandillas completas', 'Escalera de baño', 'Plataformas de baño', 'Asiento del piloto con base', 'Bancos laterales', 'Instalación eléctrica', 'Luces de cubierta', 'Cornamusas y cáncamos', 'Bomba de achique eléctrica y manual', 'Ventanas laterales correderas'],
       'hydromarin-5830': ['Depósito de aluminio', 'Barandillas', 'Cornamusas', 'Escalera de baño', 'Colchonetas', 'Dirección', 'Instalación eléctrica', 'Soporte de extintor', 'Dos asientos giratorios', 'Dos mesas plegables', 'Camarote tapizado', 'Dos ventanas y escotilla de 50 × 50 cm', 'Solárium'],
       'hydromarin-6020': ['Depósito de aluminio de 115 l', 'Barandillas', 'Cornamusas', 'Escalera de baño', 'Colchonetas', 'Dirección', 'Instalación eléctrica', 'Soporte de extintor', 'Dos asientos giratorios', 'Dos mesas plegables'],
       'hydromarin-6930': ['Depósito de aluminio de 220 l', 'Dirección hidráulica', 'Barandillas', 'Escalera de baño', 'Colchonetas y solárium', 'Asientos doble e individual', 'Camarote tapizado', 'Ventanas laterales', 'Dos bombas de achique', 'Luces de cubierta', 'Instalación eléctrica', 'Soporte de extintor']},
  std_h='De serie', eng_l='Motor', eng={'laos-605': 'Suzuki montado en fábrica, hasta 200 cv, o sin motor.', 'hydromarin-5830': 'Suzuki montado en fábrica, hasta 115 cv, o sin motor.', 'hydromarin-6020': 'Suzuki montado en fábrica, hasta 150 cv, o sin motor.', 'hydromarin-6930': 'Suzuki montado en fábrica, hasta 250 cv, o sin motor.'},
  ask='Precio a consultar', ask_s='Te paso el precio por escrito, sin compromiso.',
  wa_m='Hola Juan, me interesa la {}.', go='Pedir precio de este modelo',
  e_h='Opciones', e_l='Se eligen al hacer el pedido y se montan en fábrica. No todas existen para todos los modelos.',
  opt=['Dirección hidráulica', 'Bimini de acero inoxidable', 'Funda o lona de amarre', 'Antiincrustante', 'Molinete eléctrico', 'Ducha y grifo', 'WC eléctrico (6930)', 'Nevera de 45 l (6930)', 'Suelo EVA imitación teca', 'Cerramiento cabrio con bimini (6930)', 'Control de trimado ZipWake (6930)', 'Luces subacuáticas', 'Barra de esquí', 'Cojines de solárium', 'Mesa', 'Limpiaparabrisas', 'Depósito de 105 o 170 l (605)', 'Molinete Lofrans de 500 W (605)'],
  e_note='Te paso el precio de cada opción por escrito.',
  lic_label='Titulación', lic={'laos-605': 'PNB o superior', 'hydromarin-5830': 'Licencia de navegación o superior', 'hydromarin-6020': 'PNB o superior', 'hydromarin-6930': 'PNB o superior'},
  dlv_label='Plazo', dlv='a consultar; se confirma siempre por escrito antes del pedido',
  g_h='Todas las fotos', g_l='LAOS 605, HydroMarin 5830, 6020 y 6930. Toca una foto para verla en grande.',
  how_h='Cómo se compra', how=['Me dices qué modelo, motor y opciones te interesan.', 'Te paso el presupuesto por escrito: barco, motor montado, opciones, transporte e impuestos.', 'Se hace el pedido con la señal que marque el contrato y el astillero lo fabrica.', 'Transporte, matriculación y entrega.'],
  wty_h='Garantía y papeles', wty='2 años de garantía del astillero. Marcado CE certificado por un organismo notificado (n.º 1463). Los arreglos pequeños se resuelven aquí, con un taller de la zona, sin esperar a fábrica.',
  why_h='Cómo lo veo', why='Son barcos sin lujos innecesarios y a buen precio para su tamaño. Me gusta que vengan con el motor ya montado de fábrica. Si sales sobre todo de día con familia o amigos, la 6020 es la más práctica; si quieres un rincón para guardar cosas o echarte una siesta, la 5830 o la 6930; y si pescas o sales cuando hace fresco, la LAOS 605.',
  end_h='¿Te preparo un presupuesto?', end_p='Dime qué modelo, motor y opciones te interesan y te paso el precio por escrito, sin compromiso.',
  wa_end='Hola Juan, me interesa una lancha LAOS / HydroMarin. ¿Me preparas un presupuesto?', used_a='Ver barcos de segunda mano →',
  small='Fotos, ficha técnica y equipamiento del fabricante; las fotos pueden mostrar equipamiento opcional. Datos del certificado CE. La titulación es orientativa y depende de la eslora y la potencia que consten en la documentación: confírmala con tu escuela o con Capitanía. Podemos equivocarnos; si ves un error, avísanos.',
  alt={'605': ['LAOS 605 amarrada en el puerto', 'LAOS 605 en el puerto', 'LAOS 605 de costado', 'LAOS 605 vista de proa', 'Puesto de mando de la LAOS 605', 'Interior de la cabina de la LAOS 605'],
       '5830': ['HydroMarin 5830 navegando', 'HydroMarin 5830 en el agua', 'HydroMarin 5830 en el remolque', 'HydroMarin 5830 de costado', 'Asientos del puesto de mando', 'Puesto de mando de la HydroMarin 5830', 'Asiento giratorio y mesa', 'Interior del camarote'],
       '6020': ['HydroMarin 6020 de costado', 'Bañera de la HydroMarin 6020', 'Proa con asientos', 'Puesto de mando', 'Dos asientos giratorios', 'Asientos y consola', 'Popa y espejo', 'Cofre de popa'],
       '6930': ['HydroMarin 6930 con bimini', 'HydroMarin 6930 de costado', 'HydroMarin 6930 en el remolque']},
  close='Cerrar', prev='Anterior', next='Siguiente',
  crumbs=('Inicio', 'Barcos en venta', 'Barcos nuevos'),
 ),
 'ca': dict(
  title='LAOS 605 i HydroMarin: llanxes noves, models i fotos',
  desc='LAOS 605 i HydroMarin 5830, 6020 i 6930: llanxes de 5,60 a 6,83 m amb motor Suzuki muntat a fàbrica. Preu a consultar. Distribuïdor per a Catalunya.',
  eyebrow='Vaixells nous', kick='Distribuïdor per a Catalunya', h1='LAOS i HydroMarin: llanxes de 5,6 a 6,8 m',
  sub=['De 5,60 a 6,83 m', 'Fora borda', 'Categoria C', 'Per encàrrec'],
  see='Veure els models', cta='Demanar pressupost',
  intro='LAOS Boats és la drassana que fabrica les seves pròpies llanxes LAOS i la gamma HydroMarin. Són vaixells de polièster de 5,6 a 6,8 m, senzills i ben acabats, que es demanen a fàbrica i es poden lliurar amb el motor Suzuki ja muntat. En sóc el distribuïdor per a Catalunya: t\'ajudo a triar model, motor i opcions, i m\'encarrego de la compra, el transport i la matriculació.',
  note='Fotos de la drassana. Poden mostrar equipament opcional.',
  side=['La marca', 'LAOS 605', 'HydroMarin 5830', 'HydroMarin 6020', 'HydroMarin 6930', 'Opcions', 'Fotos', 'Pressupost'],
  mh='Quatre models', mh_l='Una llanxa amb cabina tancada i tres HydroMarin: dues amb camarot a proa i una open per al dia.',
  m={'laos-605': ('Pilothouse: cabina tancada per a qualsevol temps', 'El model més nou de la drassana. Timonera tancada amb porta corredissa, finestres laterals que s\'obren i molt vidre per veure-hi bé des del lloc de comandament. A fora, banyera amb bancs i plataformes de bany. Pensada per a pesca, per sortir a la primavera i a la tardor i per a qui vol anar a cobert.'),
     'hydromarin-5830': ('Day cruiser petit, amb camarot', 'La més compacta: 5,60 m amb un camarot entapissat a proa, dues finestres i escotilla. Dos seients giratoris, dues taules plegables i solàrium de sèrie. Amb 115 CV com a màxim, és la més fàcil de moure i de remolcar.'),
     'hydromarin-6020': ('Bowrider: open per al dia', 'Llanxa oberta de 6,07 m amb seients a proa, dues butaques giratòries al lloc de comandament i dues taules plegables. Molta banyera per banyar-se, fer esquí o pescar. Admet fins a 150 CV.'),
     'hydromarin-6930': ('El day cruiser gran', 'La més gran de la gamma: 6,83 m i 2,50 m de mànega, per a 8 persones. Camarot entapissat a proa, solàrium, seients doble i individual, direcció hidràulica i dipòsit de 220 l de sèrie. Admet fins a 250 CV.')},
  std={'laos-605': ['Direcció mecànica (fins a 125 CV)', 'Baranes completes', 'Escala de bany', 'Plataformes de bany', 'Seient del pilot amb base', 'Bancs laterals', 'Instal·lació elèctrica', 'Llums de coberta', 'Cornamuses i càncams', 'Bomba de buidatge elèctrica i manual', 'Finestres laterals corredisses'],
       'hydromarin-5830': ['Dipòsit d\'alumini', 'Baranes', 'Cornamuses', 'Escala de bany', 'Matalassets', 'Direcció', 'Instal·lació elèctrica', 'Suport d\'extintor', 'Dos seients giratoris', 'Dues taules plegables', 'Camarot entapissat', 'Dues finestres i escotilla de 50 × 50 cm', 'Solàrium'],
       'hydromarin-6020': ['Dipòsit d\'alumini de 115 l', 'Baranes', 'Cornamuses', 'Escala de bany', 'Matalassets', 'Direcció', 'Instal·lació elèctrica', 'Suport d\'extintor', 'Dos seients giratoris', 'Dues taules plegables'],
       'hydromarin-6930': ['Dipòsit d\'alumini de 220 l', 'Direcció hidràulica', 'Baranes', 'Escala de bany', 'Matalassets i solàrium', 'Seients doble i individual', 'Camarot entapissat', 'Finestres laterals', 'Dues bombes de buidatge', 'Llums de coberta', 'Instal·lació elèctrica', 'Suport d\'extintor']},
  std_h='De sèrie', eng_l='Motor', eng={'laos-605': 'Suzuki muntat a fàbrica, fins a 200 CV, o sense motor.', 'hydromarin-5830': 'Suzuki muntat a fàbrica, fins a 115 CV, o sense motor.', 'hydromarin-6020': 'Suzuki muntat a fàbrica, fins a 150 CV, o sense motor.', 'hydromarin-6930': 'Suzuki muntat a fàbrica, fins a 250 CV, o sense motor.'},
  ask='Preu a consultar', ask_s='Et passo el preu per escrit, sense compromís.',
  wa_m='Hola Juan, m\'interessa la {}.', go='Demanar preu d\'aquest model',
  e_h='Opcions', e_l='Es trien en fer la comanda i es munten a fàbrica. No totes existeixen per a tots els models.',
  opt=['Direcció hidràulica', 'Bimini d\'acer inoxidable', 'Funda o lona d\'amarratge', 'Antiincrustant', 'Molinet elèctric', 'Dutxa i aixeta', 'WC elèctric (6930)', 'Nevera de 45 l (6930)', 'Terra EVA imitació teca', 'Tancament cabrio amb bimini (6930)', 'Control de trimat ZipWake (6930)', 'Llums subaquàtics', 'Barra d\'esquí', 'Coixins de solàrium', 'Taula', 'Eixugaparabrises', 'Dipòsit de 105 o 170 l (605)', 'Molinet Lofrans de 500 W (605)'],
  e_note='Et passo el preu de cada opció per escrit.',
  lic_label='Titulació', lic={'laos-605': 'PNB o superior', 'hydromarin-5830': 'Llicència de navegació o superior', 'hydromarin-6020': 'PNB o superior', 'hydromarin-6930': 'PNB o superior'},
  dlv_label='Termini', dlv='a consultar; es confirma sempre per escrit abans de la comanda',
  g_h='Totes les fotos', g_l='LAOS 605, HydroMarin 5830, 6020 i 6930. Toca una foto per veure-la en gran.',
  how_h='Com es compra', how=['Em dius quin model, motor i opcions t\'interessen.', 'Et passo el pressupost per escrit: vaixell, motor muntat, opcions, transport i impostos.', 'Es fa la comanda amb el senyal que marqui el contracte i la drassana el fabrica.', 'Transport, matriculació i lliurament.'],
  wty_h='Garantia i papers', wty='2 anys de garantia de la drassana. Marcatge CE certificat per un organisme notificat (núm. 1463). Les reparacions petites es resolen aquí, amb un taller de la zona, sense esperar la fàbrica.',
  why_h='Com ho veig', why='Són vaixells sense luxes innecessaris i a bon preu per a la seva mida. M\'agrada que vinguin amb el motor ja muntat de fàbrica. Si surts sobretot de dia amb família o amics, la 6020 és la més pràctica; si vols un racó per guardar coses o fer la migdiada, la 5830 o la 6930; i si pesques o surts quan fa fresca, la LAOS 605.',
  end_h='Et preparo un pressupost?', end_p='Digues-me quin model, motor i opcions t\'interessen i et passo el preu per escrit, sense compromís.',
  wa_end='Hola Juan, m\'interessa una llanxa LAOS / HydroMarin. Em prepares un pressupost?', used_a='Veure vaixells de segona mà →',
  small='Fotos, fitxa tècnica i equipament del fabricant; les fotos poden mostrar equipament opcional. Dades del certificat CE. La titulació és orientativa i depèn de l\'eslora i la potència que constin a la documentació: confirma-la amb la teva escola o amb Capitania. Ens podem equivocar; si hi veus un error, avisa\'ns.',
  alt={'605': ['LAOS 605 amarrada al port', 'LAOS 605 al port', 'LAOS 605 de costat', 'LAOS 605 vista de proa', 'Lloc de comandament de la LAOS 605', 'Interior de la cabina de la LAOS 605'],
       '5830': ['HydroMarin 5830 navegant', 'HydroMarin 5830 a l\'aigua', 'HydroMarin 5830 al remolc', 'HydroMarin 5830 de costat', 'Seients del lloc de comandament', 'Lloc de comandament de la HydroMarin 5830', 'Seient giratori i taula', 'Interior del camarot'],
       '6020': ['HydroMarin 6020 de costat', 'Banyera de la HydroMarin 6020', 'Proa amb seients', 'Lloc de comandament', 'Dos seients giratoris', 'Seients i consola', 'Popa i mirall', 'Cofre de popa'],
       '6930': ['HydroMarin 6930 amb bimini', 'HydroMarin 6930 de costat', 'HydroMarin 6930 al remolc']},
  close='Tancar', prev='Anterior', next='Següent',
  crumbs=('Inici', 'Vaixells en venda', 'Vaixells nous'),
 ),
 'en': dict(
  title='LAOS 605 and HydroMarin: new day boats, models and photos',
  desc='LAOS 605 and HydroMarin 5830, 6020 and 6930: 5.60 to 6.83 m boats with a factory-fitted Suzuki outboard. Price on request. Dealer for Catalonia.',
  eyebrow='New boats', kick='Dealer for Catalonia', h1='LAOS and HydroMarin: 5.6 to 6.8 m boats',
  sub=['5.60 to 6.83 m', 'Outboard', 'Category C', 'Built to order'],
  see='See the models', cta='Request a quote',
  intro='LAOS Boats is the yard that builds its own LAOS boats and the HydroMarin range. They are 5.6 to 6.8 m GRP boats, simple and well finished, ordered from the factory and available with the Suzuki outboard already fitted. I am their dealer for Catalonia: I help you choose model, engine and options, and I handle the purchase, transport and registration.',
  note='Builder\'s photos. They may show optional equipment.',
  side=['The brand', 'LAOS 605', 'HydroMarin 5830', 'HydroMarin 6020', 'HydroMarin 6930', 'Options', 'Photos', 'Quote'],
  mh='Four models', mh_l='One boat with an enclosed wheelhouse and three HydroMarins: two with a bow cabin and one open day boat.',
  m={'laos-605': ('Pilothouse: an enclosed cabin for any weather', 'The yard\'s newest model. Enclosed wheelhouse with a sliding door, opening side windows and plenty of glass for good visibility from the helm. Outside, a cockpit with benches and swim platforms. Made for fishing, for spring and autumn trips and for anyone who wants to stay under cover.'),
     'hydromarin-5830': ('Small day cruiser with a cabin', 'The most compact one: 5.60 m with an upholstered bow cabin, two windows and a hatch. Two swivel seats, two folding tables and a sunbed as standard. With 115 hp maximum, it is the easiest to handle and to tow.'),
     'hydromarin-6020': ('Bowrider: open day boat', 'Open 6.07 m boat with bow seating, two swivel helm seats and two folding tables. A big cockpit for swimming, skiing or fishing. Rated up to 150 hp.'),
     'hydromarin-6930': ('The big day cruiser', 'The largest in the range: 6.83 m with a 2.50 m beam, for 8 people. Upholstered bow cabin, sunbed, double and single seats, hydraulic steering and a 220 l tank as standard. Rated up to 250 hp.')},
  std={'laos-605': ['Mechanical steering (up to 125 hp)', 'Full railings', 'Swim ladder', 'Swim platforms', 'Helm seat with base', 'Side benches', 'Electrical system', 'Deck lights', 'Cleats and mooring eyes', 'Electric and manual bilge pumps', 'Sliding side windows'],
       'hydromarin-5830': ['Aluminium fuel tank', 'Railings', 'Cleats', 'Swim ladder', 'Cushions', 'Steering', 'Electrical system', 'Fire extinguisher holder', 'Two swivel seats', 'Two folding tables', 'Upholstered cabin', 'Two windows and 50 × 50 cm hatch', 'Sunbed'],
       'hydromarin-6020': ['115 l aluminium fuel tank', 'Railings', 'Cleats', 'Swim ladder', 'Cushions', 'Steering', 'Electrical system', 'Fire extinguisher holder', 'Two swivel seats', 'Two folding tables'],
       'hydromarin-6930': ['220 l aluminium fuel tank', 'Hydraulic steering', 'Railings', 'Swim ladder', 'Cushions and sunbed', 'Double and single seats', 'Upholstered cabin', 'Side windows', 'Two bilge pumps', 'Deck lights', 'Electrical system', 'Fire extinguisher holder']},
  std_h='Standard', eng_l='Engine', eng={'laos-605': 'Suzuki fitted at the factory, up to 200 hp, or without engine.', 'hydromarin-5830': 'Suzuki fitted at the factory, up to 115 hp, or without engine.', 'hydromarin-6020': 'Suzuki fitted at the factory, up to 150 hp, or without engine.', 'hydromarin-6930': 'Suzuki fitted at the factory, up to 250 hp, or without engine.'},
  ask='Price on request', ask_s='I will send you the price in writing, with no obligation.',
  wa_m='Hi Juan, I am interested in the {}.', go='Ask for this model\'s price',
  e_h='Options', e_l='Chosen when ordering and fitted at the factory. Not every option is available on every model.',
  opt=['Hydraulic steering', 'Stainless steel bimini', 'Cover or mooring cover', 'Antifouling', 'Electric windlass', 'Shower and tap', 'Electric toilet (6930)', '45 l fridge (6930)', 'EVA teak-style flooring', 'Cabrio enclosure with bimini (6930)', 'ZipWake trim control (6930)', 'Underwater lights', 'Ski tow bar', 'Sunbed cushions', 'Table', 'Windscreen wiper', '105 or 170 l tank (605)', 'Lofrans 500 W windlass (605)'],
  e_note='I will send you the price of each option in writing.',
  lic_label='Licence', lic={'laos-605': 'Spanish PNB or higher', 'hydromarin-5830': 'Spanish navigation licence (LN) or higher', 'hydromarin-6020': 'Spanish PNB or higher', 'hydromarin-6930': 'Spanish PNB or higher'},
  dlv_label='Delivery', dlv='on request; always confirmed in writing before ordering',
  g_h='All photos', g_l='LAOS 605, HydroMarin 5830, 6020 and 6930. Tap a photo to see it larger.',
  how_h='How buying works', how=['You tell me which model, engine and options you want.', 'I send you a written quote: boat, fitted engine, options, transport and taxes.', 'The order is placed with the deposit set in the contract and the yard builds the boat.', 'Transport, registration and handover.'],
  wty_h='Warranty and paperwork', wty='2-year builder\'s warranty. CE marking certified by a notified body (no. 1463). Small fixes are handled here, with a local yard, without waiting for the factory.',
  why_h='How I see it', why='No unnecessary frills and a good price for their size. I like that they come with the engine already fitted at the factory. If you mostly go out for the day with family or friends, the 6020 is the most practical; if you want a corner to store things or take a nap, the 5830 or the 6930; and if you fish or go out when it is cool, the LAOS 605.',
  end_h='Shall I prepare a quote?', end_p='Tell me which model, engine and options you are interested in and I will send you the price in writing, with no obligation.',
  wa_end='Hi Juan, I am interested in a LAOS / HydroMarin boat. Could you prepare a quote?', used_a='See used boats →',
  small='Photos, specifications and equipment from the builder; photos may show optional equipment. Figures from the CE certificate. The licence shown is indicative and depends on the registered length and power: please confirm it with your school or the Harbour Master. We may be wrong; if you spot an error, let us know.',
  alt={'605': ['LAOS 605 moored in the harbour', 'LAOS 605 in the harbour', 'LAOS 605 side view', 'LAOS 605 bow view', 'LAOS 605 helm', 'LAOS 605 cabin interior'],
       '5830': ['HydroMarin 5830 underway', 'HydroMarin 5830 on the water', 'HydroMarin 5830 on its trailer', 'HydroMarin 5830 side view', 'Helm seats', 'HydroMarin 5830 helm', 'Swivel seat and table', 'Cabin interior'],
       '6020': ['HydroMarin 6020 side view', 'HydroMarin 6020 cockpit', 'Bow seating', 'Helm', 'Two swivel seats', 'Seats and console', 'Stern and transom', 'Stern locker'],
       '6930': ['HydroMarin 6930 with bimini', 'HydroMarin 6930 side view', 'HydroMarin 6930 on its trailer']},
  close='Close', prev='Previous', next='Next',
  crumbs=('Home', 'Boats for sale', 'New boats'),
 ),
 'fr': dict(
  title='LAOS 605 et HydroMarin : bateaux neufs, modèles et photos',
  desc='LAOS 605 et HydroMarin 5830, 6020 et 6930 : bateaux de 5,60 à 6,83 m avec hors-bord Suzuki monté en usine. Prix sur demande. Distributeur pour la Catalogne.',
  eyebrow='Bateaux neufs', kick='Distributeur pour la Catalogne', h1='LAOS et HydroMarin : bateaux de 5,6 à 6,8 m',
  sub=['De 5,60 à 6,83 m', 'Hors-bord', 'Catégorie C', 'Sur commande'],
  see='Voir les modèles', cta='Demander un devis',
  intro='LAOS Boats est le chantier qui construit ses propres bateaux LAOS et la gamme HydroMarin. Ce sont des bateaux en polyester de 5,6 à 6,8 m, simples et bien finis, commandés à l\'usine et livrables avec le hors-bord Suzuki déjà monté. Je suis leur distributeur pour la Catalogne : je vous aide à choisir le modèle, le moteur et les options, et je m\'occupe de l\'achat, du transport et de l\'immatriculation.',
  note='Photos du chantier. Elles peuvent montrer des options.',
  side=['La marque', 'LAOS 605', 'HydroMarin 5830', 'HydroMarin 6020', 'HydroMarin 6930', 'Options', 'Photos', 'Devis'],
  mh='Quatre modèles', mh_l='Un bateau à timonerie fermée et trois HydroMarin : deux avec cabine avant et un open pour la journée.',
  m={'laos-605': ('Pilothouse : cabine fermée par tous les temps', 'Le modèle le plus récent du chantier. Timonerie fermée avec porte coulissante, vitres latérales ouvrantes et beaucoup de vitrage pour bien voir depuis le poste de pilotage. Dehors, cockpit avec banquettes et plateformes de bain. Idéal pour la pêche, pour sortir au printemps et en automne et pour ceux qui veulent rester à l\'abri.'),
     'hydromarin-5830': ('Petit day cruiser avec cabine', 'Le plus compact : 5,60 m avec une cabine avant garnie, deux hublots et un panneau de pont. Deux sièges pivotants, deux tables pliantes et un bain de soleil de série. Avec 115 ch maximum, c\'est le plus facile à manœuvrer et à remorquer.'),
     'hydromarin-6020': ('Bowrider : open pour la journée', 'Bateau ouvert de 6,07 m avec places assises à l\'avant, deux sièges pivotants au poste de pilotage et deux tables pliantes. Grand cockpit pour la baignade, le ski ou la pêche. Jusqu\'à 150 ch.'),
     'hydromarin-6930': ('Le grand day cruiser', 'Le plus grand de la gamme : 6,83 m et 2,50 m de large, pour 8 personnes. Cabine avant garnie, bain de soleil, sièges double et simple, direction hydraulique et réservoir de 220 l de série. Jusqu\'à 250 ch.')},
  std={'laos-605': ['Direction mécanique (jusqu\'à 125 ch)', 'Balcons et mains courantes complets', 'Échelle de bain', 'Plateformes de bain', 'Siège pilote sur socle', 'Banquettes latérales', 'Circuit électrique', 'Éclairage de pont', 'Taquets et anneaux d\'amarrage', 'Pompes de cale électrique et manuelle', 'Vitres latérales coulissantes'],
       'hydromarin-5830': ['Réservoir en aluminium', 'Mains courantes', 'Taquets', 'Échelle de bain', 'Coussins', 'Direction', 'Circuit électrique', 'Support d\'extincteur', 'Deux sièges pivotants', 'Deux tables pliantes', 'Cabine garnie', 'Deux hublots et panneau de 50 × 50 cm', 'Bain de soleil'],
       'hydromarin-6020': ['Réservoir en aluminium de 115 l', 'Mains courantes', 'Taquets', 'Échelle de bain', 'Coussins', 'Direction', 'Circuit électrique', 'Support d\'extincteur', 'Deux sièges pivotants', 'Deux tables pliantes'],
       'hydromarin-6930': ['Réservoir en aluminium de 220 l', 'Direction hydraulique', 'Mains courantes', 'Échelle de bain', 'Coussins et bain de soleil', 'Sièges double et simple', 'Cabine garnie', 'Vitres latérales', 'Deux pompes de cale', 'Éclairage de pont', 'Circuit électrique', 'Support d\'extincteur']},
  std_h='De série', eng_l='Moteur', eng={'laos-605': 'Suzuki monté en usine, jusqu\'à 200 ch, ou sans moteur.', 'hydromarin-5830': 'Suzuki monté en usine, jusqu\'à 115 ch, ou sans moteur.', 'hydromarin-6020': 'Suzuki monté en usine, jusqu\'à 150 ch, ou sans moteur.', 'hydromarin-6930': 'Suzuki monté en usine, jusqu\'à 250 ch, ou sans moteur.'},
  ask='Prix sur demande', ask_s='Je vous envoie le prix par écrit, sans engagement.',
  wa_m='Bonjour Juan, le {} m\'intéresse.', go='Demander le prix de ce modèle',
  e_h='Options', e_l='Choisies à la commande et montées en usine. Toutes ne sont pas disponibles sur tous les modèles.',
  opt=['Direction hydraulique', 'Bimini en inox', 'Taud ou bâche de mouillage', 'Antifouling', 'Guindeau électrique', 'Douche et robinet', 'WC électrique (6930)', 'Réfrigérateur 45 l (6930)', 'Sol EVA imitation teck', 'Capote cabrio avec bimini (6930)', 'Correcteur d\'assiette ZipWake (6930)', 'Éclairage sous-marin', 'Arceau de ski', 'Coussins de bain de soleil', 'Table', 'Essuie-glace', 'Réservoir de 105 ou 170 l (605)', 'Guindeau Lofrans 500 W (605)'],
  e_note='Je vous envoie le prix de chaque option par écrit.',
  lic_label='Permis', lic={'laos-605': 'PNB espagnol ou supérieur', 'hydromarin-5830': 'Licence de navigation espagnole (LN) ou supérieur', 'hydromarin-6020': 'PNB espagnol ou supérieur', 'hydromarin-6930': 'PNB espagnol ou supérieur'},
  dlv_label='Délai', dlv='sur demande ; toujours confirmé par écrit avant la commande',
  g_h='Toutes les photos', g_l='LAOS 605, HydroMarin 5830, 6020 et 6930. Touchez une photo pour l\'agrandir.',
  how_h='Comment acheter', how=['Vous me dites quel modèle, quel moteur et quelles options vous intéressent.', 'Je vous envoie un devis écrit : bateau, moteur monté, options, transport et taxes.', 'La commande est passée avec l\'acompte prévu au contrat et le chantier construit le bateau.', 'Transport, immatriculation et livraison.'],
  wty_h='Garantie et papiers', wty='Garantie constructeur de 2 ans. Marquage CE certifié par un organisme notifié (n° 1463). Les petites réparations se font ici, avec un atelier local, sans attendre l\'usine.',
  why_h='Mon avis', why='Pas de luxe inutile et un bon prix pour leur taille. J\'aime qu\'ils arrivent avec le moteur déjà monté en usine. Si vous sortez surtout à la journée en famille ou entre amis, le 6020 est le plus pratique ; si vous voulez un coin pour ranger ou faire la sieste, le 5830 ou le 6930 ; et si vous pêchez ou sortez quand il fait frais, le LAOS 605.',
  end_h='Je vous prépare un devis ?', end_p='Dites-moi quel modèle, quel moteur et quelles options vous intéressent et je vous envoie le prix par écrit, sans engagement.',
  wa_end='Bonjour Juan, un bateau LAOS / HydroMarin m\'intéresse. Pouvez-vous me préparer un devis ?', used_a='Voir les bateaux d\'occasion →',
  small='Photos, fiche technique et équipement du constructeur ; les photos peuvent montrer des options. Données du certificat CE. Le permis indiqué est indicatif et dépend de la longueur et de la puissance enregistrées : vérifiez-le auprès de votre école ou de la Capitainerie. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous. Nous ne parlons pas français : nous utilisons un traducteur, merci de votre indulgence.',
  alt={'605': ['LAOS 605 amarré au port', 'LAOS 605 au port', 'LAOS 605 de profil', 'LAOS 605 vu de l\'avant', 'Poste de pilotage du LAOS 605', 'Intérieur de la cabine du LAOS 605'],
       '5830': ['HydroMarin 5830 en navigation', 'HydroMarin 5830 sur l\'eau', 'HydroMarin 5830 sur sa remorque', 'HydroMarin 5830 de profil', 'Sièges du poste de pilotage', 'Poste de pilotage du HydroMarin 5830', 'Siège pivotant et table', 'Intérieur de la cabine'],
       '6020': ['HydroMarin 6020 de profil', 'Cockpit du HydroMarin 6020', 'Places assises à l\'avant', 'Poste de pilotage', 'Deux sièges pivotants', 'Sièges et console', 'Arrière et tableau', 'Coffre arrière'],
       '6930': ['HydroMarin 6930 avec bimini', 'HydroMarin 6930 de profil', 'HydroMarin 6930 sur sa remorque']},
  close='Fermer', prev='Précédent', next='Suivant',
  crumbs=('Accueil', 'Bateaux à vendre', 'Bateaux neufs'),
 ),
}

CSS = CT_CSS + """
.kt-model{display:grid;grid-template-columns:1.15fr 1fr;gap:28px;align-items:start;padding:28px 0;border-top:1px solid rgba(14,48,66,.12)}
.kt-model:first-of-type{border-top:0}
.kt-model .kt-ph img{width:100%;height:auto;border-radius:12px;display:block}
.kt-model .kt-ph .kt-mini{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:8px}
.kt-mb{padding:0;border:0;background:none;cursor:zoom-in;display:block}
.kt-model .kt-ph .kt-mini img{aspect-ratio:4/3;object-fit:cover;border-radius:8px}
.kt-model h3{font-size:1.5rem;margin:0 0 4px}
.kt-model .kt-brand{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-2);margin:0 0 2px}
.kt-model .kt-tag{color:var(--ink-2);font-weight:600;margin:0 0 10px}
.kt-model .kt-pr{font-size:1.35rem;font-weight:700;margin:14px 0 4px}
.kt-model .kt-pr small{display:block;font-size:14px;font-weight:500;color:var(--ink-2)}
.kt-model dl{display:grid;grid-template-columns:1fr;gap:2px;margin:14px 0;font-size:14px}
.kt-model dl div{display:flex;justify-content:space-between;gap:8px;border-bottom:1px dashed rgba(14,48,66,.15);padding:4px 0}
.kt-model dt{color:var(--ink-2)}.kt-model dd{margin:0;font-weight:600;text-align:right}
.kt-eng{font-size:14px;color:var(--ink-2);margin:6px 0 12px}
.kt-std{font-size:14px;margin:10px 0 0}
.kt-std summary{cursor:pointer;font-weight:600}
.kt-std ul{margin:8px 0 0;padding-left:18px;columns:2;column-gap:20px}
.kt-logo{height:56px;width:auto;margin:0 0 10px;display:block;max-width:100%}
@media (max-width:820px){.kt-model{grid-template-columns:1fr}.kt-std ul{columns:1}}
"""


def img(name, alt, sizes='(max-width:820px) 100vw, 560px', lazy=True):
    return (f'<img src="{F}{name}-m.jpg" srcset="{F}{name}-m.jpg 900w, {F}{name}.jpg 1600w" sizes="{sizes}" alt="{html.escape(alt)}"'
            + (' loading="lazy"' if lazy else '') + ' decoding="async">')


def build(lang):
    p = LANGS[lang]
    li = LI.index(lang)
    t = T[lang]
    tpl = open(f'{ROOT}{p}/barcos-nuevos/index.html', encoding='utf-8').read()
    url = f'{BASE}{p}/{SLUG}/'
    head, rest = tpl.split('</head>', 1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(t["title"])}</title>', head)
    for k in ('name="description"', 'property="og:description"'):
        head = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc']), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(t['title']), head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', f'\\g<1>{BASE}{F}{HERO}.jpg', head)
    head = re.sub(r'<meta property="og:image:width"[^>]*>\n?<meta property="og:image:height"[^>]*>', '<meta property="og:image:width" content="1600">\n<meta property="og:image:height" content="1200">', head)
    head = head.replace('/barcos-nuevos/', f'/{SLUG}/')
    cr = t['crumbs']
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f"{BASE}{p}/"},
            {"@type": "ListItem", "position": 2, "name": cr[1], "item": f"{BASE}{p}/barcos/"},
            {"@type": "ListItem", "position": 3, "name": cr[2], "item": f"{BASE}{p}/barcos-nuevos/"},
            {"@type": "ListItem", "position": 4, "name": "LAOS / HydroMarin", "item": url}]}]
    for m in MODELS:
        ld.append({"@context": "https://schema.org", "@type": "Product", "name": m['name'], "brand": {"@type": "Brand", "name": m['brand']},
                   "image": [f"{BASE}{F}{KEY[m['id']]}-1.jpg"], "description": t['m'][m['id']][1], "url": url + '#' + m['id']})
    head = head.replace('<style>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '<style>', 1)
    head = head.replace('</style>', CSS + '</style>', 1)
    head += '<link rel="stylesheet" href="/barcos/ficha-v2.css?v=20261011b">\n<script src="/barcos/ficha-v2.js?v=20261011" defer></script>\n'

    body = rest.replace('/barcos-nuevos/" aria-current', f'/{SLUG}/" aria-current')
    body = re.sub(r'(<div class="langsw".*?</div>)', lambda m: m.group(1).replace('/barcos-nuevos/', f'/{SLUG}/'), body, flags=re.S)

    def wa(txt):
        return f'https://wa.me/{WA}?text=' + urllib.parse.quote(txt)
    def wbtn(txt, ctx, msg, cls='btn btn-wa'):
        return f'<a class="{cls}" href="{wa(msg)}" target="_blank" rel="noopener" data-wa-context="{ctx}">{html.escape(txt)}</a>'

    ids = ['marca'] + [m['id'] for m in MODELS] + ['opciones', 'fotos', 'presupuesto']
    side = ''.join(f'<a href="#{i}"><span>{html.escape(s)}</span><i></i></a>' for i, s in zip(ids, t['side']))
    sub = ''.join(f'<span>{html.escape(s)}</span>' for s in t['sub'])
    altmap = {f'{k}-{i + 1}': a for k, lst in t['alt'].items() for i, a in enumerate(lst)}

    models = ''
    for m in MODELS:
        k = KEY[m['id']]
        tag, txt = t['m'][m['id']]
        s = dict(m['spec'])
        rows = ''
        for key in ['lh', 'beam', 'draft', 'disp', 'pax', 'load', 'fuel', 'pmax', 'shaft', 'ce']:
            v = s[key]
            if key == 'fuel' and v is None:
                v = FUEL605[li]
            if v is None:
                continue
            rows += f'<div><dt>{html.escape(SPEC_L[key][li])}</dt><dd>{html.escape(loc(v, lang))}</dd></div>'
        rows += f'<div><dt>{html.escape(t["lic_label"])}</dt><dd>{html.escape(t["lic"][m["id"]])}</dd></div>'
        mini = ''.join(f'<button type="button" class="kt-mb" data-full="{F}{k}-{i}.jpg"><img src="{F}{k}-{i}-m.jpg" alt="{html.escape(altmap[f"{k}-{i}"])}" loading="lazy" decoding="async"></button>' for i in range(2, min(m['n'], 4) + 1))
        phh = '<div class="kt-ph">' + img(f'{k}-1', altmap[f'{k}-1']) + (f'<div class="kt-mini">{mini}</div>' if mini else '') + '</div>'
        std = ''.join(f'<li>{html.escape(x)}</li>' for x in t['std'][m['id']])
        models += (f'<article class="kt-model" id="{m["id"]}">{phh}<div><p class="kt-brand">{html.escape(m["brand"])}</p><h3>{html.escape(m["name"])}</h3><p class="kt-tag">{html.escape(tag)}</p><p>{html.escape(txt)}</p>'
                   f'<p class="kt-pr">{html.escape(t["ask"])}<small>{html.escape(t["ask_s"])}</small></p>'
                   f'<p class="kt-eng"><b>{html.escape(t["eng_l"])}:</b> {html.escape(t["eng"][m["id"]])} <b>{html.escape(t["dlv_label"])}:</b> {html.escape(t["dlv"])}.</p><dl class="specs">{rows}</dl>'
                   f'<details class="kt-std"><summary>{html.escape(t["std_h"])}</summary><ul>{std}</ul></details>'
                   f'<div class="v2-ctas" style="margin-top:14px">{wbtn(t["go"], "ficha_" + m["id"], t["wa_m"].format(m["name"]))}</div></div></article>')

    opt = ''.join(f'<li>{html.escape(x)}</li>' for x in t['opt'])
    how = ''.join(f'<li>{html.escape(x)}</li>' for x in t['how'])
    gal = ''.join(f'<button type="button" data-full="{F}{n}.jpg"><img src="{F}{n}-m.jpg" alt="{html.escape(altmap[n])}" loading="lazy" decoding="async"></button>' for n in GAL)
    main = f'''<main class="boat v2 ct">
<div class="wrap v2-crumb"><p class="crumb"><a href="{p}/">{cr[0]}</a> · <a href="{p}/barcos/">{cr[1]}</a> · <a href="{p}/barcos-nuevos/">{cr[2]}</a> · LAOS / HydroMarin</p></div>
<nav class="v2-side" aria-label="{html.escape(t['side'][0])}">{side}</nav>
<section class="v2-hero" id="marca">
<img class="v2-hero-img" src="{F}{HERO}.jpg" srcset="{F}{HERO}-m.jpg 900w, {F}{HERO}.jpg 1600w" sizes="100vw" alt="{html.escape(altmap[HERO])}" width="1600" height="1200" fetchpriority="high" decoding="async">
<div class="v2-hero-in wrap head"><div><p class="eyebrow" style="color:rgba(255,255,255,.85)">{t['eyebrow']} · {t['kick']}</p><h1>{html.escape(t['h1'])}</h1><div class="sub">{sub}</div></div>
<div class="price-box"><p class="price">{html.escape(t['ask'])}<small>{html.escape(t['ask_s'])}</small></p>
<div class="v2-ctas">{wbtn(t['cta'], 'ficha_precio', t['wa_end'])}<a class="btn v2-ghost" href="#{MODELS[0]['id']}">{html.escape(t['see'])}</a></div></div></div>
</section>
<div class="wrap v2-note"><img class="kt-logo" src="/barcos-nuevos/logos/laos-hydromarin.png" alt="LAOS Boats · HydroMarin" width="762" height="120"><p class="muted head-note">{html.escape(t['intro'])} {html.escape(t['note'])}</p></div>
<section class="v2-sec" id="modelos"><div class="wrap">
<p class="v2-k">{html.escape(t['kick'])}</p><h2>{html.escape(t['mh'])}</h2><p class="v2-lead">{html.escape(t['mh_l'])}</p>
{models}
</div></section>
<section class="v2-sec" id="opciones"><div class="wrap">
<h2>{html.escape(t['e_h'])}</h2><p class="v2-lead">{html.escape(t['e_l'])}</p>
<ul class="ct-tags opt">{opt}</ul><p class="v2-small" style="margin-top:12px">{html.escape(t['e_note'])}</p>
</div></section>
<section class="v2-sec" id="fotos"><div class="wrap">
<h2>{html.escape(t['g_h'])}</h2><p class="v2-lead">{html.escape(t['g_l'])}</p>
<div class="ct-gal" id="ct-gal">{gal}</div>
</div></section>
<div class="ct-lb" id="ct-lb" hidden role="dialog" aria-modal="true" aria-label="{html.escape(t['g_h'])}"><button type="button" class="x" aria-label="{t['close']}">&times;</button><button type="button" class="p" aria-label="{t['prev']}">&#8249;</button><img alt=""><button type="button" class="n" aria-label="{t['next']}">&#8250;</button><p></p></div>
<section class="v2-sec v2-band"><div class="wrap">
<h2>{html.escape(t['how_h'])}</h2><ol class="ct-how">{how}</ol>
<h2 style="margin-top:36px">{html.escape(t['wty_h'])}</h2><p class="ct-why">{html.escape(t['wty'])}</p>
<h2 style="margin-top:36px">{html.escape(t['why_h'])}</h2><p class="ct-why">{html.escape(t['why'])}</p>
</div></section>
<section class="v2-end" id="presupuesto" style="--bg:url('{F}5830-1-m.jpg')"><div class="wrap">
<h2>{html.escape(t['end_h'])}</h2><p>{html.escape(t['end_p'])}</p>
<div class="v2-ctas">{wbtn(t['cta'], 'ficha_cierre', t['wa_end'])}<a class="btn v2-ghost" href="{p}/barcos/#segunda-mano">{html.escape(t['used_a'])}</a></div>
</div></section>
<div class="wrap"><p class="nv-small">{html.escape(t['small'])}</p></div>
</main>{JS}<script>document.querySelectorAll('.kt-mb').forEach(function(b){{b.addEventListener('click',function(){{var f=b.getAttribute('data-full');var g=document.querySelector('#ct-gal button[data-full="'+f+'"]');if(g)g.click();}});}});</script><script src="/submit-confirmed.js?v=20261011" defer></script>'''
    body = re.sub(r'<main class="boat">.*?</main>', lambda m: main, body, flags=re.S)
    out = head + '</head>' + body
    os.makedirs(f'{ROOT}{p}/{SLUG}', exist_ok=True)
    open(f'{ROOT}{p}/{SLUG}/index.html', 'w', encoding='utf-8').write(out)
    print('ok', lang, len(out))


if __name__ == '__main__':
    for l in LANGS:
        build(l)
