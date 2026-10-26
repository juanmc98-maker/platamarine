#!/usr/bin/env python3
"""Genera /kattum/ en ES/CA/EN/FR a partir de la plantilla de /barcos-nuevos/.
Datos: catálogos y tarifas 2026 que mandó Kattum Yachts (Daniel, 26 oct 2026).
Uso: python3 _tools/build_kattum.py  (desde la raíz del repo)"""
import re, json, html, urllib.parse, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_catharsis import CSS as CT_CSS, JS, eur, LANGS, BASE, WA
from kattum_config import cfg as kcfg

ROOT = '.'
SLUG = 'kattum'
LI = ['es', 'ca', 'en', 'fr']
F = f'/{SLUG}/fotos/kattum-'

# Precios de tarifa 2026 del astillero, sin IVA (se dejan tal cual vienen en la tarifa)
MODELS = [
 dict(id='k30-open', name='Kattum K30 Open', price=175000, eng=False, hero='k30-1',
      ph=['k30-2', 'k30-3', 'k30-11', 'k30-4', 'k30-5', 'k30-6', 'k30-7', 'k30-8', 'k30-9', 'k30-10'],
      spec=dict(lh='7,98 m', loa='9,38 m', beam='3,40 m', disp='4.100 kg', ce='B', pax='12 + 2', cab=None, wc='1', water='2 × 75 l', fuel='2 × 198 l', prec='2 × 200 cv', pmax='600 cv')),
 dict(id='k30-cruiser', name='Kattum K30 Cruiser', price=215000, eng=False, hero='k30c-2',
      ph=['k30c-1', 'k30c-3', 'k30c-4', 'k30c-5', 'k30c-6', 'k30c-7', 'k30c-8', 'k30c-9', 'k30c-10', 'k30c-11', 'k30c-12', 'k30c-13'],
      spec=dict(lh='7,98 m', loa='9,38 m', beam='3,40 m', disp='4.400 kg', ce='B', pax='12 + 2', cab='1', wc='1', water='2 × 75 l', fuel='2 × 198 l', prec='2 × 200 cv', pmax='600 cv')),
 dict(id='k40', name='Kattum K40 Open', price=500000, eng=True, hero='k40-plano', ph=[],
      spec=dict(lh='9,98 m', loa='11,10 m', beam='4,25 m', disp='7.000 kg', ce='B', pax='12 + 2', cab='2', wc='2', water='2 × 100 l', fuel='2 × 450 l', prec='2 × 350 cv', pmax='1.200 cv')),
]
GAL = MODELS[0]['ph'][:0] + ['k30-1'] + MODELS[0]['ph'] + ['k30c-2'] + MODELS[1]['ph']

SPEC_L = {
 'lh': ('Eslora de casco', 'Eslora de buc', 'Hull length', 'Longueur de coque'),
 'loa': ('Eslora total', 'Eslora total', 'Length overall', 'Longueur hors tout'),
 'beam': ('Manga', 'Mànega', 'Beam', 'Largeur'),
 'disp': ('Desplazamiento', 'Desplaçament', 'Displacement', 'Déplacement'),
 'ce': ('Categoría de diseño CE', 'Categoria de disseny CE', 'CE design category', 'Catégorie de conception CE'),
 'pax': ('Personas', 'Persones', 'People', 'Personnes'),
 'cab': ('Camarotes dobles', 'Camarots dobles', 'Double cabins', 'Cabines doubles'),
 'wc': ('Aseos', 'Lavabos', 'Heads', 'Toilettes'),
 'water': ('Agua dulce', 'Aigua dolça', 'Fresh water', 'Eau douce'),
 'fuel': ('Combustible', 'Combustible', 'Fuel', 'Carburant'),
 'prec': ('Potencia recomendada', 'Potència recomanada', 'Recommended power', 'Puissance recommandée'),
 'pmax': ('Potencia máxima', 'Potència màxima', 'Maximum power', 'Puissance maximale'),
}

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
  title='Kattum: catamaranes a motor nuevos, precios y fotos',
  desc='Catamaranes a motor Kattum K30 Open, K30 Cruiser y K40, de 9,38 a 11,10 m. Desde 175.000 € + impuestos. Distribuidor para Baleares.',
  eyebrow='Barcos nuevos', kick='Distribuidor para Baleares', h1='Kattum: catamaranes a motor',
  sub=['De 9,38 a 11,10 m', 'Fueraborda', 'Categoría B', 'Bajo pedido'],
  price_from='Desde', vat='+ impuestos', vat_note='K30 Open, sin motores', see='Ver los modelos', cta='Pedir presupuesto',
  intro='Kattum Yachts fabrica catamaranes a motor con dos cascos: navegan planos y estables, y la bañera es mucho más ancha que la de una lancha de la misma eslora. Se piden a fábrica y se configuran a medida. Soy su distribuidor para Baleares: te ayudo a elegir modelo, motores y equipamiento, y me encargo de la compra.',
  note='Fotos del astillero. Pueden mostrar equipamiento opcional.',
  side=['La marca', 'K30 Open', 'K30 Cruiser', 'K40', 'Configurar', 'Equipamiento', 'Fotos', 'Presupuesto'],
  mh='Tres modelos', mh_l='El mismo concepto en tres tamaños: tú eliges cuánto espacio quieres dentro.',
  m={'k30-open': ('Para el día, con todo el espacio fuera', 'Catamarán open con T-top sobre el puesto de mando, asientos modulables, solárium y una plataforma de baño ampliada que se aprovecha mucho cuando se fondea. Lleva un aseo bajo la consola.'),
     'k30-cruiser': ('El K30 con camarote', 'La misma base que el K30 Open, con un camarote doble y un baño completo dentro. Mantiene la bañera amplia y la plataforma de baño, y permite pasar la noche a bordo.'),
     'k40': ('Más grande, para hacer crucero', 'El modelo mayor: 11,10 m, dos camarotes dobles y dos aseos independientes, y de serie con dos motores Mercury de 400 cv. El astillero aún no me ha pasado fotos reales del K40; si te interesa, te paso el catálogo por WhatsApp.')},
  eng_no='sin motores', eng_yes='con 2 × Mercury 400 cv',
  eng_k30='Motores: de 2 × 200 a 2 × 300 cv, Suzuki o Mercury, desde 40.000 € + impuestos (2 × Suzuki 200).',
  eng_k40='De serie lleva 2 × Mercury 400 cv. Opción de 2 × 600 cv.',
  wa_m='Hola Juan, me interesa el {}.', go='Pedir precio de este modelo',
  e_h='Qué lleva de serie y qué es opcional', std_h='De serie (K30)', k40_h='Además, en el K40', opt_h='Opcional',
  std=['Domótica', 'Cubierta Seadeck', 'Molinete eléctrico de 1.000 W con ancla y cadena', 'Equipo de navegación Raymarine de 9"', 'Equipo de música JL Audio (4 altavoces)', 'T-top', 'Plataforma de popa', 'Mesa abatible en popa', 'Escalera de baño', 'Nevera de 49 l', 'Dos duchas de agua dulce', 'WC químico', 'Dirección hidráulica', '3 baterías con desconectadores remotos', 'Luces de navegación LED, de cortesía y en el T-top', 'Enchufe de 12 V y USB en consola', 'Cornamusas retráctiles', 'Casco gris'],
  k40=['2 motores Mercury de 400 cv', 'Dirección electrohidráulica', 'Raymarine de 12"', 'Dos aseos con ducha y WC eléctrico', 'Camarote doble con portillos', 'Dos neveras', 'Luces subacuáticas', 'Cargador de baterías', 'T-top de aluminio'],
  opt=['Cubierta de teca', 'Toldo eléctrico', 'Tapicería premium', 'Joystick', 'Piloto automático', 'Hélice de proa', 'VHF', 'Luces subacuáticas', 'Neveras adicionales', 'Placas solares', 'WC eléctrico con tanque de aguas negras', 'Casco y cubierta en color', 'Preósmosis y antiincrustante', 'K40: aire acondicionado, generador, auxiliar de 2 m con motor eléctrico'],
  e_note='Te paso el precio de cada opción por escrito.',
  f_h='Ficha técnica', lic_label='Titulación', lic_k30='PNB o superior (eslora de casco 7,98 m)', lic_k40='PER o superior', dlv_label='Plazo de entrega', dlv='A consultar: se confirma siempre por escrito antes del pedido',
  g_h='Todas las fotos', g_l='K30 Open y K30 Cruiser. Toca una foto para verla en grande.',
  how_h='Cómo se compra', how=['Me dices qué modelo, motores y opciones te interesan.', 'Te paso el presupuesto por escrito: barco, opciones, motores, transporte e impuestos.', 'Se hace el pedido con la señal que marque el contrato y el astillero lo fabrica.', 'Transporte, matriculación y entrega.'],
  why_h='Cómo lo veo', why='Me gusta el proyecto: un catamarán de 9 metros tiene la bañera de una lancha bastante más grande, navega plano y se mueve menos fondeado, algo que se agradece en las calas de Baleares. Con fuerabordas el mantenimiento suele ser más sencillo. Si dudas entre el Open y el Cruiser, la pregunta es si vas a dormir a bordo.',
  end_h='¿Te preparo un presupuesto?', end_p='Dime qué modelo, motores y opciones te interesan y te paso el precio por escrito, sin compromiso.',
  wa_end='Hola Juan, me interesa un Kattum. ¿Me preparas un presupuesto?', used_a='Ver barcos de segunda mano →',
  small='Precios de la tarifa 2026 del astillero, sin IVA, en fábrica: K30 Open y K30 Cruiser sin motores; K40 con 2 motores Mercury de 400 cv. No incluyen equipamiento opcional, transporte, matriculación ni el IEDMT cuando corresponda. Pueden cambiar y no son vinculantes; el precio final es el del presupuesto por escrito. Fotos y ficha técnica del fabricante; las fotos pueden mostrar equipamiento opcional. La titulación es orientativa y depende de la eslora que conste en la documentación: confírmala con tu escuela o con Capitanía. Podemos equivocarnos; si ves un error, avísanos.',
  alt=['Kattum K30 Open navegando', 'Dos Kattum K30 Open navegando', 'Kattum K30 Open de costado', 'Dos Kattum K30 navegando', 'Popa con plataforma y motores', 'Puesto de mando', 'Asientos del puesto de mando', 'Solárium de proa', 'Bañera con sofá', 'Tapicería', 'Pantalla de domótica', 'Kattum K30 Cruiser navegando', 'Kattum K30 Cruiser visto desde arriba', 'Kattum K30 Cruiser navegando', 'Kattum K30 Cruiser de costado', 'Kattum K30 Cruiser navegando', 'Solárium de proa', 'Asientos del puesto de mando', 'Bañera con mesa', 'Bañera y solárium', 'Camarote', 'Baño', 'Camarote doble', 'Cama del camarote'],
  plano='Plano del Kattum K40', close='Cerrar', prev='Anterior', next='Siguiente',
  crumbs=('Inicio', 'Barcos en venta', 'Barcos nuevos'),
 ),
 'ca': dict(
  title='Kattum: catamarans a motor nous, preus i fotos',
  desc='Catamarans a motor Kattum K30 Open, K30 Cruiser i K40, de 9,38 a 11,10 m. Des de 175.000 € + impostos. Distribuïdor per a les Balears.',
  eyebrow='Vaixells nous', kick='Distribuïdor per a les Balears', h1='Kattum: catamarans a motor',
  sub=['De 9,38 a 11,10 m', 'Fora borda', 'Categoria B', 'Per encàrrec'],
  price_from='Des de', vat='+ impostos', vat_note='K30 Open, sense motors', see='Veure els models', cta='Demanar pressupost',
  intro='Kattum Yachts fabrica catamarans a motor de dos bucs: naveguen plans i estables, i la banyera és molt més ampla que la d\'una llanxa de la mateixa eslora. Es demanen a fàbrica i es configuren a mida. En sóc el distribuïdor per a les Balears: t\'ajudo a triar model, motors i equipament, i m\'encarrego de la compra.',
  note='Fotos de la drassana. Poden mostrar equipament opcional.',
  side=['La marca', 'K30 Open', 'K30 Cruiser', 'K40', 'Configurar', 'Equipament', 'Fotos', 'Pressupost'],
  mh='Tres models', mh_l='El mateix concepte en tres mides: tu tries quant espai vols a dins.',
  m={'k30-open': ('Per al dia, amb tot l\'espai a fora', 'Catamarà open amb T-top sobre el lloc de comandament, seients modulables, solàrium i una plataforma de bany ampliada que s\'aprofita molt quan es fondeja. Porta un lavabo sota la consola.'),
     'k30-cruiser': ('El K30 amb camarot', 'La mateixa base que el K30 Open, amb un camarot doble i un bany complet a dins. Manté la banyera àmplia i la plataforma de bany, i permet passar la nit a bord.'),
     'k40': ('Més gran, per fer creuer', 'El model més gran: 11,10 m, dos camarots dobles i dos lavabos independents, i de sèrie amb dos motors Mercury de 400 CV. La drassana encara no m\'ha passat fotos reals del K40; si t\'interessa, et passo el catàleg per WhatsApp.')},
  eng_no='sense motors', eng_yes='amb 2 × Mercury 400 CV',
  eng_k30='Motors: de 2 × 200 a 2 × 300 CV, Suzuki o Mercury, des de 40.000 € + impostos (2 × Suzuki 200).',
  eng_k40='De sèrie porta 2 × Mercury 400 CV. Opció de 2 × 600 CV.',
  wa_m='Hola Juan, m\'interessa el {}.', go='Demanar preu d\'aquest model',
  e_h='Què porta de sèrie i què és opcional', std_h='De sèrie (K30)', k40_h='A més, al K40', opt_h='Opcional',
  std=['Domòtica', 'Coberta Seadeck', 'Molinet elèctric de 1.000 W amb àncora i cadena', 'Equip de navegació Raymarine de 9"', 'Equip de música JL Audio (4 altaveus)', 'T-top', 'Plataforma de popa', 'Taula abatible a popa', 'Escala de bany', 'Nevera de 49 l', 'Dues dutxes d\'aigua dolça', 'WC químic', 'Direcció hidràulica', '3 bateries amb desconnectadors remots', 'Llums de navegació LED, de cortesia i al T-top', 'Endoll de 12 V i USB a la consola', 'Cornamuses retràctils', 'Buc gris'],
  k40=['2 motors Mercury de 400 CV', 'Direcció electrohidràulica', 'Raymarine de 12"', 'Dos lavabos amb dutxa i WC elèctric', 'Camarot doble amb portells', 'Dues neveres', 'Llums subaquàtics', 'Carregador de bateries', 'T-top d\'alumini'],
  opt=['Coberta de teca', 'Tendal elèctric', 'Tapisseria prèmium', 'Joystick', 'Pilot automàtic', 'Hèlix de proa', 'VHF', 'Llums subaquàtics', 'Neveres addicionals', 'Plaques solars', 'WC elèctric amb dipòsit d\'aigües negres', 'Buc i coberta en color', 'Preosmosi i antiincrustant', 'K40: aire condicionat, generador, auxiliar de 2 m amb motor elèctric'],
  e_note='Et passo el preu de cada opció per escrit.',
  f_h='Fitxa tècnica', lic_label='Titulació', lic_k30='PNB o superior (eslora de buc 7,98 m)', lic_k40='PER o superior', dlv_label='Termini de lliurament', dlv='A consultar: es confirma sempre per escrit abans de la comanda',
  g_h='Totes les fotos', g_l='K30 Open i K30 Cruiser. Toca una foto per veure-la en gran.',
  how_h='Com es compra', how=['Em dius quin model, motors i opcions t\'interessen.', 'Et passo el pressupost per escrit: vaixell, opcions, motors, transport i impostos.', 'Es fa la comanda amb el senyal que marqui el contracte i la drassana el fabrica.', 'Transport, matriculació i lliurament.'],
  why_h='Com el veig', why='M\'agrada el projecte: un catamarà de 9 metres té la banyera d\'una llanxa força més gran, navega pla i es mou menys fondejat, cosa que s\'agraeix a les cales de les Balears. Amb fora bordes el manteniment sol ser més senzill. Si dubtes entre l\'Open i el Cruiser, la pregunta és si dormiràs a bord.',
  end_h='Et preparo un pressupost?', end_p='Digues-me quin model, motors i opcions t\'interessen i et passo el preu per escrit, sense compromís.',
  wa_end='Hola Juan, m\'interessa un Kattum. Em prepares un pressupost?', used_a='Veure vaixells de segona mà →',
  small='Preus de la tarifa 2026 de la drassana, sense IVA, a fàbrica: K30 Open i K30 Cruiser sense motors; K40 amb 2 motors Mercury de 400 CV. No inclouen equipament opcional, transport, matriculació ni l\'IEDMT quan correspongui. Poden canviar i no són vinculants; el preu final és el del pressupost per escrit. Fotos i fitxa tècnica del fabricant; les fotos poden mostrar equipament opcional. La titulació és orientativa i depèn de l\'eslora que consti a la documentació: confirma-la amb la teva escola o amb Capitania. Ens podem equivocar; si hi veus un error, avisa\'ns.',
  alt=['Kattum K30 Open navegant', 'Dos Kattum K30 Open navegant', 'Kattum K30 Open de costat', 'Dos Kattum K30 navegant', 'Popa amb plataforma i motors', 'Lloc de comandament', 'Seients del lloc de comandament', 'Solàrium de proa', 'Banyera amb sofà', 'Tapisseria', 'Pantalla de domòtica', 'Kattum K30 Cruiser navegant', 'Kattum K30 Cruiser vist des de dalt', 'Kattum K30 Cruiser navegant', 'Kattum K30 Cruiser de costat', 'Kattum K30 Cruiser navegant', 'Solàrium de proa', 'Seients del lloc de comandament', 'Banyera amb taula', 'Banyera i solàrium', 'Camarot', 'Bany', 'Camarot doble', 'Llit del camarot'],
  plano='Plànol del Kattum K40', close='Tancar', prev='Anterior', next='Següent',
  crumbs=('Inici', 'Vaixells en venda', 'Vaixells nous'),
 ),
 'en': dict(
  title='Kattum: new power catamarans, prices and photos',
  desc='Kattum K30 Open, K30 Cruiser and K40 power catamarans, 9.38 to 11.10 m. From €175,000 + taxes. Dealer for the Balearic Islands.',
  eyebrow='New boats', kick='Dealer for the Balearic Islands', h1='Kattum: power catamarans',
  sub=['9.38 to 11.10 m', 'Outboard', 'Category B', 'Built to order'],
  price_from='From', vat='+ taxes', vat_note='K30 Open, without engines', see='See the models', cta='Request a quote',
  intro='Kattum Yachts builds twin-hull power catamarans: they run flat and stable, and the cockpit is much wider than on a motorboat of the same length. They are ordered from the factory and configured to order. I am their dealer for the Balearic Islands: I help you choose model, engines and equipment, and I handle the purchase.',
  note='Builder\'s photos. They may show optional equipment.',
  side=['The brand', 'K30 Open', 'K30 Cruiser', 'K40', 'Configure', 'Equipment', 'Photos', 'Quote'],
  mh='Three models', mh_l='The same concept in three sizes: you choose how much space you want inside.',
  m={'k30-open': ('For day trips, with all the space outside', 'Open catamaran with a T-top over the helm, modular seating, sunbed and an extended swim platform that really pays off at anchor. There is a toilet under the console.'),
     'k30-cruiser': ('The K30 with a cabin', 'The same base as the K30 Open, with a double cabin and a full bathroom inside. It keeps the wide cockpit and the swim platform, and lets you spend the night on board.'),
     'k40': ('Bigger, for cruising', 'The largest model: 11.10 m, two double cabins and two separate heads, with twin 400 hp Mercury engines as standard. The builder has not sent me real photos of the K40 yet; if you are interested, I can send you the brochure on WhatsApp.')},
  eng_no='without engines', eng_yes='with 2 × Mercury 400 hp',
  eng_k30='Engines: from 2 × 200 to 2 × 300 hp, Suzuki or Mercury, from €40,000 + taxes (2 × Suzuki 200).',
  eng_k40='Standard with 2 × Mercury 400 hp. 2 × 600 hp available as an option.',
  wa_m='Hi Juan, I am interested in the {}.', go='Ask for this model\'s price',
  e_h='What is standard and what is optional', std_h='Standard (K30)', k40_h='On the K40, also', opt_h='Optional',
  std=['Home automation', 'Seadeck deck', '1,000 W electric windlass with anchor and chain', '9" Raymarine navigation', 'JL Audio music system (4 speakers)', 'T-top', 'Stern platform', 'Folding cockpit table', 'Swim ladder', '49 l fridge', 'Two fresh-water showers', 'Chemical toilet', 'Hydraulic steering', '3 batteries with remote switches', 'LED navigation, courtesy and T-top lights', '12 V and USB socket at the console', 'Retractable cleats', 'Grey hull'],
  k40=['Twin 400 hp Mercury engines', 'Electro-hydraulic steering', '12" Raymarine', 'Two heads with shower and electric toilet', 'Double cabin with opening portholes', 'Two fridges', 'Underwater lights', 'Battery charger', 'Aluminium T-top'],
  opt=['Teak deck', 'Electric awning', 'Premium upholstery', 'Joystick', 'Autopilot', 'Bow thruster', 'VHF', 'Underwater lights', 'Extra fridges', 'Solar panels', 'Electric toilet with holding tank', 'Coloured hull and deck', 'Osmosis protection and antifouling', 'K40: air conditioning, generator, 2 m tender with electric motor'],
  e_note='I will send you the price of each option in writing.',
  f_h='Specifications', lic_label='Licence', lic_k30='Spanish PNB or higher (hull length 7.98 m)', lic_k40='Spanish PER or higher', dlv_label='Delivery time', dlv='On request: always confirmed in writing before ordering',
  g_h='All photos', g_l='K30 Open and K30 Cruiser. Tap a photo to see it larger.',
  how_h='How buying works', how=['You tell me which model, engines and options you want.', 'I send you a written quote: boat, options, engines, transport and taxes.', 'The order is placed with the deposit set in the contract and the builder builds the boat.', 'Transport, registration and handover.'],
  why_h='How I see it', why='I like the project: a 9-metre catamaran has the cockpit of a much bigger motorboat, runs flat and moves less at anchor, which you appreciate in the Balearic coves. With outboards, maintenance is usually simpler. If you are torn between the Open and the Cruiser, the question is whether you will sleep on board.',
  end_h='Shall I prepare a quote?', end_p='Tell me which model, engines and options you are interested in and I will send you the price in writing, with no obligation.',
  wa_end='Hi Juan, I am interested in a Kattum. Could you prepare a quote?', used_a='See used boats →',
  small='Prices from the builder\'s 2026 price list, ex-works, excluding VAT: K30 Open and K30 Cruiser without engines; K40 with twin 400 hp Mercury engines. They do not include optional equipment, transport, registration or Spanish registration tax (IEDMT) where applicable. They may change and are not binding; the final price is the one in the written quote. Photos and specifications from the builder; photos may show optional equipment. The licence shown is indicative and depends on the registered length: please confirm it with your school or the Harbour Master. We may be wrong; if you spot an error, let us know.',
  alt=['Kattum K30 Open underway', 'Two Kattum K30 Open underway', 'Kattum K30 Open side view', 'Two Kattum K30 underway', 'Stern with platform and engines', 'Helm', 'Helm seats', 'Bow sunbed', 'Cockpit sofa', 'Upholstery', 'Home automation screen', 'Kattum K30 Cruiser underway', 'Kattum K30 Cruiser from above', 'Kattum K30 Cruiser underway', 'Kattum K30 Cruiser side view', 'Kattum K30 Cruiser underway', 'Bow sunbed', 'Helm seats', 'Cockpit with table', 'Cockpit and sunbed', 'Cabin', 'Bathroom', 'Double cabin', 'Cabin bed'],
  plano='Kattum K40 drawing', close='Close', prev='Previous', next='Next',
  crumbs=('Home', 'Boats for sale', 'New boats'),
 ),
 'fr': dict(
  title='Kattum : catamarans à moteur neufs, prix et photos',
  desc='Catamarans à moteur Kattum K30 Open, K30 Cruiser et K40, de 9,38 à 11,10 m. À partir de 175 000 € + taxes. Distributeur pour les Baléares.',
  eyebrow='Bateaux neufs', kick='Distributeur pour les Baléares', h1='Kattum : catamarans à moteur',
  sub=['De 9,38 à 11,10 m', 'Hors-bord', 'Catégorie B', 'Sur commande'],
  price_from='À partir de', vat='+ taxes', vat_note='K30 Open, sans moteurs', see='Voir les modèles', cta='Demander un devis',
  intro='Kattum Yachts construit des catamarans à moteur à deux coques : ils naviguent à plat et stables, et le cockpit est bien plus large que celui d\'un bateau à moteur de même longueur. Ils sont commandés à l\'usine et configurés sur mesure. Je suis leur distributeur pour les Baléares : je vous aide à choisir le modèle, les moteurs et l\'équipement, et je m\'occupe de l\'achat.',
  note='Photos du chantier. Elles peuvent montrer des options.',
  side=['La marque', 'K30 Open', 'K30 Cruiser', 'K40', 'Configurer', 'Équipement', 'Photos', 'Devis'],
  mh='Trois modèles', mh_l='Le même concept en trois tailles : vous choisissez l\'espace que vous voulez à l\'intérieur.',
  m={'k30-open': ('Pour la journée, tout l\'espace dehors', 'Catamaran open avec T-top au-dessus du poste de pilotage, sièges modulables, bain de soleil et une plateforme de bain agrandie, très utile au mouillage. Toilettes sous la console.'),
     'k30-cruiser': ('Le K30 avec cabine', 'La même base que le K30 Open, avec une cabine double et une salle d\'eau complète. Il garde le grand cockpit et la plateforme de bain, et permet de passer la nuit à bord.'),
     'k40': ('Plus grand, pour la croisière', 'Le plus grand modèle : 11,10 m, deux cabines doubles et deux toilettes séparées, avec deux moteurs Mercury de 400 ch de série. Le chantier ne m\'a pas encore envoyé de vraies photos du K40 ; s\'il vous intéresse, je vous envoie la brochure sur WhatsApp.')},
  eng_no='sans moteurs', eng_yes='avec 2 × Mercury 400 ch',
  eng_k30='Moteurs : de 2 × 200 à 2 × 300 ch, Suzuki ou Mercury, à partir de 40 000 € + taxes (2 × Suzuki 200).',
  eng_k40='De série : 2 × Mercury 400 ch. Option 2 × 600 ch.',
  wa_m='Bonjour Juan, le {} m\'intéresse.', go='Demander le prix de ce modèle',
  e_h='Ce qui est de série et ce qui est en option', std_h='De série (K30)', k40_h='En plus, sur le K40', opt_h='En option',
  std=['Domotique', 'Pont Seadeck', 'Guindeau électrique 1 000 W avec ancre et chaîne', 'Électronique Raymarine 9"', 'Système audio JL Audio (4 haut-parleurs)', 'T-top', 'Plateforme arrière', 'Table rabattable au cockpit', 'Échelle de bain', 'Réfrigérateur 49 l', 'Deux douches eau douce', 'WC chimique', 'Direction hydraulique', '3 batteries avec coupe-circuits à distance', 'Feux de navigation LED, éclairage de courtoisie et du T-top', 'Prise 12 V et USB à la console', 'Taquets escamotables', 'Coque grise'],
  k40=['2 moteurs Mercury de 400 ch', 'Direction électro-hydraulique', 'Raymarine 12"', 'Deux toilettes avec douche et WC électrique', 'Cabine double avec hublots ouvrants', 'Deux réfrigérateurs', 'Éclairage sous-marin', 'Chargeur de batteries', 'T-top en aluminium'],
  opt=['Pont en teck', 'Taud électrique', 'Sellerie premium', 'Joystick', 'Pilote automatique', 'Propulseur d\'étrave', 'VHF', 'Éclairage sous-marin', 'Réfrigérateurs supplémentaires', 'Panneaux solaires', 'WC électrique avec cuve à eaux noires', 'Coque et pont en couleur', 'Traitement anti-osmose et antifouling', 'K40 : climatisation, groupe électrogène, annexe de 2 m à moteur électrique'],
  e_note='Je vous envoie le prix de chaque option par écrit.',
  f_h='Fiche technique', lic_label='Permis', lic_k30='PNB espagnol ou supérieur (longueur de coque 7,98 m)', lic_k40='PER espagnol ou supérieur', dlv_label='Délai de livraison', dlv='Sur demande : toujours confirmé par écrit avant la commande',
  g_h='Toutes les photos', g_l='K30 Open et K30 Cruiser. Touchez une photo pour l\'agrandir.',
  how_h='Comment acheter', how=['Vous me dites quel modèle, quels moteurs et quelles options vous intéressent.', 'Je vous envoie un devis écrit : bateau, options, moteurs, transport et taxes.', 'La commande est passée avec l\'acompte prévu au contrat et le chantier construit le bateau.', 'Transport, immatriculation et livraison.'],
  why_h='Mon avis', why='J\'aime le projet : un catamaran de 9 mètres a le cockpit d\'un bateau à moteur bien plus grand, navigue à plat et bouge moins au mouillage, ce qui se remarque dans les criques des Baléares. Avec des hors-bord, l\'entretien est en général plus simple. Si vous hésitez entre l\'Open et le Cruiser, la question est de savoir si vous dormirez à bord.',
  end_h='Je vous prépare un devis ?', end_p='Dites-moi quel modèle, quels moteurs et quelles options vous intéressent et je vous envoie le prix par écrit, sans engagement.',
  wa_end='Bonjour Juan, un Kattum m\'intéresse. Pouvez-vous me préparer un devis ?', used_a='Voir les bateaux d\'occasion →',
  small='Prix de la liste 2026 du chantier, départ usine, hors TVA : K30 Open et K30 Cruiser sans moteurs ; K40 avec 2 moteurs Mercury de 400 ch. Ils n\'incluent pas les options, le transport, l\'immatriculation ni la taxe d\'immatriculation espagnole (IEDMT) le cas échéant. Ils peuvent changer et ne sont pas contractuels ; le prix final est celui du devis écrit. Photos et fiche technique du constructeur ; les photos peuvent montrer des options. Le permis indiqué est indicatif et dépend de la longueur enregistrée : vérifiez-le auprès de votre école ou de la Capitainerie. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous. Nous ne parlons pas français : nous utilisons un traducteur, merci de votre indulgence.',
  alt=['Kattum K30 Open en navigation', 'Deux Kattum K30 Open en navigation', 'Kattum K30 Open de profil', 'Deux Kattum K30 en navigation', 'Arrière avec plateforme et moteurs', 'Poste de pilotage', 'Sièges du poste de pilotage', 'Bain de soleil avant', 'Cockpit avec banquette', 'Sellerie', 'Écran de domotique', 'Kattum K30 Cruiser en navigation', 'Kattum K30 Cruiser vu d\'en haut', 'Kattum K30 Cruiser en navigation', 'Kattum K30 Cruiser de profil', 'Kattum K30 Cruiser en navigation', 'Bain de soleil avant', 'Sièges du poste de pilotage', 'Cockpit avec table', 'Cockpit et bain de soleil', 'Cabine', 'Salle d\'eau', 'Cabine double', 'Lit de la cabine'],
  plano='Plan du Kattum K40', close='Fermer', prev='Précédent', next='Suivant',
  crumbs=('Accueil', 'Bateaux à vendre', 'Bateaux neufs'),
 ),
}

CFH = {'es': ('Configura tu Kattum', 'Elige modelo, motores y opcionales y ve el precio al momento. Cuando lo tengas, pídeme el presupuesto por escrito.'), 'ca': ('Configura el teu Kattum', "Tria model, motors i opcionals i veu el preu al moment. Quan el tinguis, demana'm el pressupost per escrit."), 'en': ('Configure your Kattum', 'Choose model, engines and options and see the price instantly. When you are ready, ask me for the written quote.'), 'fr': ('Configurez votre Kattum', 'Choisissez le modèle, les moteurs et les options et voyez le prix immédiatement. Ensuite, demandez-moi le devis écrit.')}

CSS = CT_CSS + """
.kt-model{display:grid;grid-template-columns:1.15fr 1fr;gap:28px;align-items:start;padding:28px 0;border-top:1px solid rgba(14,48,66,.12)}
.kt-model:first-of-type{border-top:0}
.kt-model .kt-ph img{width:100%;height:auto;border-radius:12px;display:block}
.kt-model .kt-ph.plano{background:#0b1a24;border-radius:12px;padding:24px}
.kt-model h3{font-size:1.5rem;margin:0 0 4px}
.kt-model .kt-tag{color:var(--ink-2);font-weight:600;margin:0 0 10px}
.kt-model .kt-pr{font-size:1.35rem;font-weight:700;margin:14px 0 4px}
.kt-model .kt-pr .vat{color:#d93025;font-size:.7em;margin-left:4px}
.kt-model .kt-pr small{display:block;font-size:14px;font-weight:500;color:var(--ink-2)}
.kt-model dl{display:grid;grid-template-columns:1fr;gap:2px;margin:14px 0;font-size:14px}
.kt-model dl div{display:flex;justify-content:space-between;gap:8px;border-bottom:1px dashed rgba(14,48,66,.15);padding:4px 0}
.kt-model dt{color:var(--ink-2)}.kt-model dd{margin:0;font-weight:600;text-align:right}
.kt-eng{font-size:14px;color:var(--ink-2);margin:6px 0 12px}
.kt-logo{height:56px;width:auto;margin:0 0 10px;display:block}
@media (max-width:820px){.kt-model{grid-template-columns:1fr}.kt-model dl{grid-template-columns:1fr}}
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
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', f'\\g<1>{BASE}{F}k30-1.jpg', head)
    head = re.sub(r'<meta property="og:image:width"[^>]*>\n?<meta property="og:image:height"[^>]*>', '<meta property="og:image:width" content="1600">\n<meta property="og:image:height" content="899">', head)
    head = head.replace('/barcos-nuevos/', f'/{SLUG}/')
    cr = t['crumbs']
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f"{BASE}{p}/"},
            {"@type": "ListItem", "position": 2, "name": cr[1], "item": f"{BASE}{p}/barcos/"},
            {"@type": "ListItem", "position": 3, "name": cr[2], "item": f"{BASE}{p}/barcos-nuevos/"},
            {"@type": "ListItem", "position": 4, "name": "Kattum", "item": url}]}]
    for m in MODELS:
        ld.append({"@context": "https://schema.org", "@type": "Product", "name": m['name'], "brand": {"@type": "Brand", "name": "Kattum Yachts"},
                   "image": [f"{BASE}{F}{m['hero']}.jpg"], "description": t['m'][m['id']][1],
                   "offers": {"@type": "Offer", "price": str(m['price']), "priceCurrency": "EUR", "availability": "https://schema.org/PreOrder", "url": url + '#' + m['id'],
                              "priceSpecification": {"@type": "PriceSpecification", "price": str(m['price']), "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}})
    head = head.replace('<style>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '<style>', 1)
    head = head.replace('</style>', CSS + '</style>', 1)
    head += '<link rel="stylesheet" href="/barcos/ficha-v2.css?v=20261011b">\n<script src="/barcos/ficha-v2.js?v=20261011" defer></script>\n'

    body = rest.replace('/barcos-nuevos/" aria-current', f'/{SLUG}/" aria-current')
    body = re.sub(r'(<div class="langsw".*?</div>)', lambda m: m.group(1).replace('/barcos-nuevos/', f'/{SLUG}/'), body, flags=re.S)

    def wa(txt):
        return f'https://wa.me/{WA}?text=' + urllib.parse.quote(txt)
    def wbtn(txt, ctx, msg, cls='btn btn-wa'):
        return f'<a class="{cls}" href="{wa(msg)}" target="_blank" rel="noopener" data-wa-context="{ctx}">{html.escape(txt)}</a>'

    ids = ['marca', 'k30-open', 'k30-cruiser', 'k40', 'configurar', 'equipamiento', 'fotos', 'presupuesto']
    side = ''.join(f'<a href="#{i}"><span>{html.escape(s)}</span><i></i></a>' for i, s in zip(ids, t['side']))
    sub = ''.join(f'<span>{html.escape(s)}</span>' for s in t['sub'])
    A = t['alt']
    altmap = dict(zip(GAL, A))

    models = ''
    for k, m in enumerate(MODELS):
        tag, txt = t['m'][m['id']]
        s = m['spec']
        rows = ''
        for key in ['lh', 'loa', 'beam', 'disp', 'ce', 'pax', 'cab', 'wc', 'water', 'fuel', 'prec', 'pmax']:
            v = s[key]
            if v is None:
                continue
            rows += f'<div><dt>{html.escape(SPEC_L[key][li])}</dt><dd>{html.escape(loc(v, lang))}</dd></div>'
        lic = t['lic_k40'] if m['id'] == 'k40' else t['lic_k30']
        rows += f'<div><dt>{html.escape(t["lic_label"])}</dt><dd>{html.escape(lic)}</dd></div>'
        if m['id'] == 'k40':
            phh = f'<div class="kt-ph plano"><img src="{F}k40-plano.jpg" alt="{html.escape(t["plano"])}" width="748" height="310" loading="lazy" decoding="async"></div>'
        else:
            phh = '<div class="kt-ph">' + img(m['hero'], altmap.get(m['hero'], m['name'])) + '</div>'
        eng = t['eng_k40'] if m['eng'] else t['eng_k30']
        models += (f'<article class="kt-model" id="{m["id"]}">{phh}<div><h3>{m["name"].replace("Kattum ", "")}</h3><p class="kt-tag">{html.escape(tag)}</p><p>{html.escape(txt)}</p>'
                   f'<p class="kt-pr">{t["price_from"]} {eur(m["price"], lang)} €<span class="vat">{t["vat"]}</span><small>{html.escape(t["eng_yes"] if m["eng"] else t["eng_no"])}</small></p>'
                   f'<p class="kt-eng">{html.escape(eng)} {html.escape(t["dlv_label"])}: {html.escape(t["dlv"][0].lower() + t["dlv"][1:])}.</p><dl class="specs">{rows}</dl>'
                   f'<div class="v2-ctas">{wbtn(t["go"], "ficha_" + m["id"], t["wa_m"].format(m["name"]))}</div></div></article>')

    std = ''.join(f'<li>{html.escape(x)}</li>' for x in t['std'])
    k40 = ''.join(f'<li>{html.escape(x)}</li>' for x in t['k40'])
    opt = ''.join(f'<li>{html.escape(x)}</li>' for x in t['opt'])
    how = ''.join(f'<li>{html.escape(x)}</li>' for x in t['how'])
    gal = ''.join(f'<button type="button" data-full="{F}{n}.jpg"><img src="{F}{n}-m.jpg" alt="{html.escape(altmap[n])}" loading="lazy" decoding="async"></button>' for n in GAL)
    main = f'''<main class="boat v2 ct">
<div class="wrap v2-crumb"><p class="crumb"><a href="{p}/">{cr[0]}</a> · <a href="{p}/barcos/">{cr[1]}</a> · <a href="{p}/barcos-nuevos/">{cr[2]}</a> · Kattum</p></div>
<nav class="v2-side" aria-label="{html.escape(t['side'][0])}">{side}</nav>
<section class="v2-hero" id="marca">
<img class="v2-hero-img" src="{F}k30-1.jpg" srcset="{F}k30-1-m.jpg 900w, {F}k30-1.jpg 1600w" sizes="100vw" alt="{html.escape(A[0])}" width="1600" height="899" fetchpriority="high" decoding="async">
<div class="v2-hero-in wrap head"><div><p class="eyebrow" style="color:rgba(255,255,255,.85)">{t['eyebrow']} · {t['kick']}</p><h1>{html.escape(t['h1'])}</h1><div class="sub">{sub}</div></div>
<div class="price-box"><p class="price">{t['price_from']} {eur(175000, lang)} €<span class="vat">{t['vat']}</span><small>{html.escape(t['vat_note'])}</small></p>
<div class="v2-ctas">{wbtn(t['cta'], 'ficha_precio', t['wa_end'])}<a class="btn v2-ghost" href="#k30-open">{html.escape(t['see'])}</a></div></div></div>
</section>
<div class="wrap v2-note"><img class="kt-logo" src="/barcos-nuevos/logos/kattum.png" alt="Kattum Yachts" width="547" height="145"><p class="muted head-note">{html.escape(t['intro'])} {html.escape(t['note'])}</p></div>
<section class="v2-sec" id="modelos"><div class="wrap">
<p class="v2-k">{html.escape(t['kick'])}</p><h2>{html.escape(t['mh'])}</h2><p class="v2-lead">{html.escape(t['mh_l'])}</p>
{models}
</div></section>
<section class="v2-sec v2-band" id="configurar"><div class="wrap">
<h2>{html.escape(CFH[lang][0])}</h2><p class="v2-lead">{html.escape(CFH[lang][1])}</p>
<div id="pm-cfg"></div>
</div></section>
<script>window.PM_CFG={json.dumps(kcfg(li), ensure_ascii=False)};</script>
<section class="v2-sec" id="equipamiento"><div class="wrap">
<h2>{html.escape(t['e_h'])}</h2>
<div class="ct-two"><div><h3>{t['std_h']}</h3><ul class="ct-tags">{std}</ul><h3 style="margin-top:20px">{t['k40_h']}</h3><ul class="ct-tags">{k40}</ul></div><div><h3>{t['opt_h']}</h3><ul class="ct-tags opt">{opt}</ul><p class="v2-small" style="margin-top:12px">{html.escape(t['e_note'])}</p></div></div>
</div></section>
<section class="v2-sec" id="fotos"><div class="wrap">
<h2>{html.escape(t['g_h'])}</h2><p class="v2-lead">{html.escape(t['g_l'])}</p>
<div class="ct-gal" id="ct-gal">{gal}</div>
</div></section>
<div class="ct-lb" id="ct-lb" hidden role="dialog" aria-modal="true" aria-label="{html.escape(t['g_h'])}"><button type="button" class="x" aria-label="{t['close']}">&times;</button><button type="button" class="p" aria-label="{t['prev']}">&#8249;</button><img alt=""><button type="button" class="n" aria-label="{t['next']}">&#8250;</button><p></p></div>
<section class="v2-sec v2-band"><div class="wrap">
<h2>{html.escape(t['how_h'])}</h2><ol class="ct-how">{how}</ol>
<h2 style="margin-top:36px">{html.escape(t['why_h'])}</h2><p class="ct-why">{html.escape(t['why'])}</p>
</div></section>
<section class="v2-end" id="presupuesto" style="--bg:url('{F}k30-11-m.jpg')"><div class="wrap">
<h2>{html.escape(t['end_h'])}</h2><p>{html.escape(t['end_p'])}</p>
<div class="v2-ctas">{wbtn(t['cta'], 'ficha_cierre', t['wa_end'])}<a class="btn v2-ghost" href="{p}/barcos/#segunda-mano">{html.escape(t['used_a'])}</a></div>
</div></section>
<div class="wrap"><p class="nv-small">{html.escape(t['small'])}</p></div>
</main>{JS}<script src="/submit-confirmed.js?v=20261011" defer></script><script src="/barcos-nuevos/pm-config.js?v=20261026" defer></script>'''
    body = re.sub(r'<main class="boat">.*?</main>', lambda m: main, body, flags=re.S)
    out = head + '</head>' + body
    os.makedirs(f'{ROOT}{p}/{SLUG}', exist_ok=True)
    open(f'{ROOT}{p}/{SLUG}/index.html', 'w', encoding='utf-8').write(out)
    print('ok', lang, len(out))


if __name__ == '__main__':
    for l in LANGS:
        build(l)
