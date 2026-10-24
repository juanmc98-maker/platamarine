#!/usr/bin/env python3
"""Genera una página por modelo de Mar.Co (/marco/<modelo>/) en ES/CA/EN/FR con:
galería completa (fotos del astillero), configurador con la tarifa pública (versión, motores, opcionales,
total al momento, enlace para compartir y resumen imprimible), equipamiento de serie, ficha técnica,
vídeos oficiales (se cargan solo al dar al play), cómo se compra, presupuesto y otros modelos.
Datos: _tools/marco_data/tarifa.json (tarifa 09/2026), strings_tr.json (traducciones),
existing.json (textos y fichas ya publicados en /marco/), photos.json (fotos por modelo).
Cabecera, menú y pie se copian de /marco/ de cada idioma. Uso: python3 _tools/build_marco_modelos.py"""
import json, re, html, os

ROOT = '.'
D = os.path.join(ROOT, '_tools', 'marco_data')
TAR = {m['name']: m for m in json.load(open(os.path.join(D, 'tarifa.json')))}
TR = json.load(open(os.path.join(D, 'strings_tr.json')))
EX = json.load(open(os.path.join(D, 'existing.json')))
PH = json.load(open(os.path.join(D, 'photos.json')))
# Bloque 'Para quién es' (para_quien.json): para quién, frente al modelo hermano y motores
PQ = json.load(open(os.path.join(D, 'para_quien.json'))) if os.path.exists(os.path.join(D, 'para_quien.json')) else {}
PQ_KICK = {'es': '¿Es para ti?', 'ca': 'És per a tu?', 'en': 'Is it for you?', 'fr': 'Est-ce pour vous ?'}
PQ_CSS = '.mm-pq{border-top:1px solid var(--line)}.mm-who{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.mm-who>div{border:1px solid var(--line);border-radius:14px;padding:18px 20px;background:#fff}.mm-who h3{font-family:var(--display);font-size:1.08rem;font-weight:700;margin:0 0 8px;color:var(--ink)}.mm-who p{margin:0;line-height:1.6;color:var(--ink-2);font-size:.96rem}@media(max-width:900px){.mm-who{grid-template-columns:1fr}}'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
SITE = 'https://www.platamarine.com'
V = '20261024b'

# slug, nombre, clave tarifa, tipo (cab/open), eslora m, vídeos oficiales, foto de portada (n), foto de cierre
IEDMT = {'e-motion-36', 'r-evolution-x36', 'r-evolution-35', 'e-motion-32'}  # eslora en papeles > 8 m seguro (tarifa: 9,98 m homologada o más)
MODELS = [
 ('e-motion-44', 'E-Motion 44', None, 'cab', 13.50, [], 3, 14),
 ('e-motion-36', 'E-Motion 36', 'E-MOTION 36', 'cab', 10.70, ['Bf60mN_Imvk', '2n4Izcv3VIg'], 1, 7),
 ('r-evolution-x36', 'R-Evolution X36', 'R-EVOLUTION X36', 'open', 10.65, ['LywzlrPQT1k', 'yq5nMzLWBd8'], 3, 9),
 ('r-evolution-35', 'R-Evolution 35', 'R-EVOLUTION 35', 'open', 10.65, ['YS0CTXe5z3Q'], 1, 24),
 ('e-motion-32', 'E-Motion 32', 'E-MOTION 32', 'cab', 9.98, ['C2jDaDK_BaM', 'zdKBghH66ig'], 1, 5),
 ('e-motion-29', 'E-Motion 29', 'E-MOTION 29', 'cab', 8.90, [], 0, 0),
 ('r-evolution-x27', 'R-Evolution X27', 'R-EVOLUTION X27', 'open', 8.32, [], 1, 6),
 ('r-evolution-26', 'R-Evolution 26', 'R-EVOLUTION 26', 'open', 8.02, ['9QvIuItHTEc', 'ggqrN0KX6Gc'], 1, 22),
 ('twentysix', 'TwentySix', 'TWENTYSIX', 'open', 8.43, [], 0, 0),
 ('twentythree', 'TwentyThree', 'TWENTYTHREE', 'open', 7.40, [], 1, 3),
]
OLD_FOTO = {'e-motion-29': '/marco/fotos/marco-e-motion-29-01', 'twentysix': '/marco/fotos/marco-twentysix-01'}

# E-Motion 44: sin tarifa en la lista de 09/2026; datos de la web del astillero
E44 = {
 'es': {'p': ['La cabinada más grande de Mar.Co: 13,50 m, dos camarotes con cuatro plazas para dormir y plataformas laterales abatibles que abren la manga hasta 5,60 m.'],
        'dl': {'Eslora total': '13,50 m', 'Eslora de casco': '13,37 m', 'Manga': '4,55 m', 'Manga con plataformas abiertas': '5,60 m', 'Camarotes': '2 (4 plazas)', 'Peso en seco': '10.000 kg', 'Ángulo de la V': '22°', 'Combustible': '1.700 l', 'Agua dulce': '290 l', 'Potencia máxima': '2.000 hp', 'Categoría de diseño CE': 'B', 'Titulación': 'PER o superior'}},
 'ca': {'p': ['La cabinada més gran de Mar.Co: 13,50 m, dues cabines amb quatre places per dormir i plataformes laterals abatibles que obren la mànega fins a 5,60 m.'],
        'dl': {'Eslora total': '13,50 m', 'Eslora de buc': '13,37 m', 'Mànega': '4,55 m', 'Mànega amb plataformes obertes': '5,60 m', 'Cabines': '2 (4 places)', 'Pes en sec': '10.000 kg', 'Angle de la V': '22°', 'Combustible': '1.700 l', 'Aigua dolça': '290 l', 'Potència màxima': '2.000 hp', 'Categoria de disseny CE': 'B', 'Titulació': 'PER o superior'}},
 'en': {'p': ['The largest Mar.Co cabin RIB: 13.50 m, two cabins sleeping four and fold-down side platforms that widen the beam to 5.60 m.'],
        'dl': {'Length overall': '13.50 m', 'Hull length': '13.37 m', 'Beam': '4.55 m', 'Beam with platforms open': '5.60 m', 'Cabins': '2 (4 berths)', 'Dry weight': '10,000 kg', 'Deadrise': '22°', 'Fuel': '1,700 l', 'Fresh water': '290 l', 'Maximum power': '2,000 hp', 'CE design category': 'B', 'Licence': 'Spanish PER or higher'}},
 'fr': {'p': ['Le plus grand semi-rigide cabine de Mar.Co : 13,50 m, deux cabines avec quatre couchages et des plateformes latérales rabattables qui portent la largeur à 5,60 m.'],
        'dl': {'Longueur hors tout': '13,50 m', 'Longueur de coque': '13,37 m', 'Largeur': '4,55 m', 'Largeur plateformes ouvertes': '5,60 m', 'Cabines': '2 (4 couchages)', 'Poids à sec': '10 000 kg', 'Angle de V': '22°', 'Carburant': '1 700 l', 'Eau douce': '290 l', 'Puissance maximale': '2 000 hp', 'Catégorie de conception CE': 'B', 'Permis': 'PER espagnol ou supérieur'}},
}

T = {
'es': dict(
 home='Inicio', boats='Barcos en venta', new='Barcos nuevos', vat='+ impuestos', noeng='sin motores', from_='Desde', ask='Precio bajo consulta',
 nav=['Fotos', 'Configurar', 'De serie', 'Ficha', 'Presupuesto'],
 t_title='Mar.Co {n}: precio y configurador · Plata Marine',
 t_desc='Mar.Co {n} nuevo, bajo pedido: {k} fotos, ficha técnica y configurador con la tarifa oficial. {p}',
 t_desc_ask='Mar.Co {n} nuevo, bajo pedido: fotos del astillero y ficha técnica. Precio bajo consulta.',
 kind={'cab': 'Cabinada', 'open': 'Open'}, h_cta='Configúrala', h_ph='Ver las {k} fotos',
 g_k='Fotos', g_h='La {n}, por dentro y por fuera', g_sub='Fotos oficiales del astillero. Toca cualquiera para verla en grande y pasa de una a otra con las flechas. Pueden mostrar equipamiento opcional.',
 g_more='Ver las {k} fotos',
 c_k='Configurador', c_h='Configura tu {n}', c_sub='Elige versión, motores y opcionales con los precios de la tarifa oficial de Mar.Co. El total se actualiza al momento y puedes enviármelo para que te prepare el presupuesto por escrito.',
 c_s1='1. Versión', c_s2='2. Motores', c_s3='3. Equipamiento opcional', c_std='Estándar', c_inf='Laminado por infusión', c_inf_d='Más ligera y rígida',
 c_std_d='Fibra laminada a mano',
 e_mer='Mercury', e_mer_d='Los que monta el astillero', e_oth='Otra marca', e_oth_d='Yamaha, Suzuki, Honda…', e_adv='Aconséjame', e_adv_d='Lo vemos según el uso',
 e_note='Potencia máxima homologada: {p}. Los motores no están en la tarifa del astillero: te los presupuesto aparte.',
 cats={'top': 'Hard-Top, roll-bar y toldos', 'deck': 'Revestimientos de cubierta', 'paint': 'Pintura', 'comfort': 'Confort a bordo', 'elec': 'Electrónica, luz y sonido', 'gear': 'Maniobra, fondeo y popa', 'cover': 'Fundas', 'other': 'Otros'},
 one='Solo una opción de este grupo', sum_h='Tu {n}', sum_base='Barco', sum_opts='Opcionales', sum_none='Ninguno',
 sum_tot='Total sin impuestos', sum_iva='Con IVA (21 %)', sum_eng='Motores', sum_extra='Motores, transporte desde fábrica e impuesto de matriculación, aparte.',
 b_send='Pedir presupuesto con esta configuración', b_share='Copiar enlace', b_copied='Enlace copiado', b_reset='Empezar de nuevo',
 s_k='Equipamiento de serie', s_h='Lo que lleva de serie', f_k='Ficha técnica', f_h='Datos técnicos',
 v_k='Vídeo', v_h='La {n} en el agua', v_sub='Vídeos oficiales de Mar.Co. Se cargan desde YouTube solo cuando le das al play.', v_play='Reproducir el vídeo',
 how_h='Cómo se compra una Mar.Co', how=[('Lo hablamos', 'Me cuentas cómo vas a usarla y te ayudo a elegir modelo, motores y opcionales.'), ('Presupuesto por escrito', 'Con tu configuración te paso el precio cerrado: barco, opcionales, motores y transporte.'), ('Pedido a fábrica', 'Se fabrica a tu medida en Italia. Yo me ocupo del pedido y del seguimiento.'), ('Entrega', 'Te acompaño en la entrega, los papeles y la matriculación.')],
 q_h='Pide tu presupuesto', q_sub='Si has configurado tu {n}, la configuración va incluida en el mensaje. Te contesto con el presupuesto por escrito.',
 q_name='Nombre', q_tel='Teléfono', q_email='Email', q_zone='Zona o puerto', q_when='¿Para cuándo?', q_msg='Cuéntame', q_opt='(opcional)',
 q_when_o=['Sin prisa / informándome', 'Temporada 2027', 'Lo antes posible'], q_cfg='Tu configuración',
 q_msg_ph='Uso, número de personas, colores, motores…', q_send='Solicitar presupuesto',
 q_priv='Responsable: Juan Morante (Plata Marine). Usaré estos datos solo para contestarte y preparar tu presupuesto. Si avanzamos, los compartiré con Mar.Co para emitir el pedido. Puedes ejercer tus derechos en juan@platamarine.com.',
 q_privl='Política de privacidad', q_cons='He leído la información de privacidad y acepto que uses estos datos para contestarme.', q_req='Los campos con * son obligatorios.',
 faq_h='Preguntas frecuentes',
 faq=[('¿Qué titulación necesito?', '{lic}, por su eslora de {l}. Es orientativo: confírmalo con tu escuela náutica o con Capitanía.'),
      ('¿Qué incluye el precio?', 'El barco con el equipamiento de serie, en fábrica (Italia) y sin impuestos. Los motores, el transporte hasta Barcelona, el IVA, el impuesto de matriculación y la matriculación van aparte y te los detallo en el presupuesto.'),
      ('¿Puedo elegir colores y acabados?', 'Sí. Cada Mar.Co se fabrica bajo pedido: además de las opciones de la tarifa, el astillero hace acabados a medida. Dime qué tienes en mente y lo consulto.'),
      ('¿Y si ya tengo motores?', 'Se puede estudiar. Lo importante es que la potencia y el tipo de pata encajen con el barco: lo vemos con el astillero antes del pedido.')],
 others='Los otros modelos Mar.Co', all='Ver toda la gama →', see='Ver el modelo →',
 end_h='¿Hablamos de tu {n}?', end_p='Escríbeme y lo vemos con calma. Sin compromiso.', wa='Escribir por WhatsApp',
 wa_txt='Hola Juan, me interesa la Mar.Co {n}.',
 small='Precios de la tarifa pública del astillero (revisión 09/2026), sin IVA, sin motores y en fábrica (EXW, Italia). No incluyen motores, transporte, impuesto de matriculación (IEDMT) ni matriculación. El IVA mostrado es orientativo (21 %). Pueden cambiar y no son vinculantes: el precio final es el del presupuesto por escrito. Fotos, vídeos y datos técnicos del fabricante; las fotos pueden mostrar equipamiento opcional. La titulación es orientativa: confírmala con tu escuela o con Capitanía. Podemos equivocarnos; si ves un error, avísanos.',
  b_print='Descargar oferta en PDF',
 ie_l='Impuesto de matriculación (12 %)', ie_all='Total con IVA e impuesto de matriculación', ie_note='Calculado sobre barco y opcionales. Motores y transporte, aparte.', ie_unk='Impuesto de matriculación: depende de la eslora que figure en los papeles del barco; te lo confirmo en el presupuesto.',
 why={'ht':'Requiere el Hard-Top','rb':'Requiere el roll-bar','br':'Requiere el soporte de motores (bracket)','aft':'Requiere un toldo de popa','win':'Requiere el molinete','plot':'Requiere un GPS Garmin','aud':'Requiere un equipo de audio','lp':'Requiere los puntos de izado','x_ht':'Con Hard-Top, elige la versión para Hard-Top','x_rb':'Solo sin roll-bar','x_br':'Con bracket, elige la versión con bracket','x_fullcov':'Incluida en la funda completa','x_chcov':'Incluida en la funda de consola y banco'},
 dl_h='Descarga tu oferta en PDF', dl_p='Déjame tus datos y te descargas la oferta con tu configuración y un número de oferta, para que lo hablemos cuando quieras.', dl_btn='Descargar PDF', dl_wait='Preparando tu oferta…', dl_close='Cerrar',
 sh_offer='Oferta', sh_for='Preparada para', sh_date='Fecha', sh_cfg='Tu configuración', sh_specs='Datos principales', sh_scan='Escanea el código para ver o cambiar esta configuración en la web',
 sh_valid='Oferta orientativa con los precios de la tarifa oficial del astillero (revisión 09/2026). No es vinculante: el precio final es el del presupuesto por escrito. Motores, transporte desde fábrica y gastos de matriculación, aparte.',
 sh_lic='Titulación',
 print_h='Resumen de configuración', print_d='Fecha', print_c='Plata Marine · Juan Morante · +34 633 742 973 · juan@platamarine.com · www.platamarine.com',
 nophoto='Fotos de este modelo, próximamente', e44_note='Te paso el precio y la lista de opcionales del E-Motion 44 por escrito.',
 lic_per='PER o superior', lic_pnb='PNB o superior',
 eng_label={'mer': 'Mercury', 'oth': 'Otra marca', 'adv': 'Aconséjame'},
),
'ca': dict(
 home='Inici', boats='Vaixells en venda', new='Vaixells nous', vat='+ impostos', noeng='sense motors', from_='Des de', ask='Preu a consultar',
 nav=['Fotos', 'Configurar', 'De sèrie', 'Fitxa', 'Pressupost'],
 t_title='Mar.Co {n}: preu i configurador · Plata Marine',
 t_desc='Mar.Co {n} nova, per encàrrec: {k} fotos, fitxa tècnica i configurador amb la tarifa oficial. {p}',
 t_desc_ask='Mar.Co {n} nova, per encàrrec: fotos de la drassana i fitxa tècnica. Preu a consultar.',
 kind={'cab': 'Cabinada', 'open': 'Open'}, h_cta='Configura-la', h_ph='Veure les {k} fotos',
 g_k='Fotos', g_h='La {n}, per dins i per fora', g_sub='Fotos oficials de la drassana. Toca qualsevol per veure-la en gran i passa d’una a l’altra amb les fletxes. Poden mostrar equipament opcional.',
 g_more='Veure les {k} fotos',
 c_k='Configurador', c_h='Configura la teva {n}', c_sub='Tria versió, motors i opcionals amb els preus de la tarifa oficial de Mar.Co. El total s’actualitza al moment i me’l pots enviar perquè et prepari el pressupost per escrit.',
 c_s1='1. Versió', c_s2='2. Motors', c_s3='3. Equipament opcional', c_std='Estàndard', c_inf='Laminat per infusió', c_inf_d='Més lleugera i rígida',
 c_std_d='Fibra laminada a mà',
 e_mer='Mercury', e_mer_d='Els que munta la drassana', e_oth='Una altra marca', e_oth_d='Yamaha, Suzuki, Honda…', e_adv='Aconsella’m', e_adv_d='Ho veiem segons l’ús',
 e_note='Potència màxima homologada: {p}. Els motors no són a la tarifa de la drassana: te’ls pressuposto a part.',
 cats={'top': 'Hard-Top, roll-bar i tendals', 'deck': 'Revestiments de coberta', 'paint': 'Pintura', 'comfort': 'Confort a bord', 'elec': 'Electrònica, llum i so', 'gear': 'Maniobra, fondeig i popa', 'cover': 'Fundes', 'other': 'Altres'},
 one='Només una opció d’aquest grup', sum_h='La teva {n}', sum_base='Vaixell', sum_opts='Opcionals', sum_none='Cap',
 sum_tot='Total sense impostos', sum_iva='Amb IVA (21 %)', sum_eng='Motors', sum_extra='Motors, transport des de fàbrica i impost de matriculació, a part.',
 b_send='Demanar pressupost amb aquesta configuració', b_share='Copiar l’enllaç', b_copied='Enllaç copiat', b_reset='Tornar a començar',
 s_k='Equipament de sèrie', s_h='El que porta de sèrie', f_k='Fitxa tècnica', f_h='Dades tècniques',
 v_k='Vídeo', v_h='La {n} a l’aigua', v_sub='Vídeos oficials de Mar.Co. Es carreguen des de YouTube només quan li dones al play.', v_play='Reproduir el vídeo',
 how_h='Com es compra una Mar.Co', how=[('Ho parlem', 'M’expliques com la faràs servir i t’ajudo a triar model, motors i opcionals.'), ('Pressupost per escrit', 'Amb la teva configuració et passo el preu tancat: vaixell, opcionals, motors i transport.'), ('Comanda a fàbrica', 'Es fabrica a mida a Itàlia. Jo m’ocupo de la comanda i del seguiment.'), ('Entrega', 'T’acompanyo a l’entrega, els papers i la matriculació.')],
 q_h='Demana el teu pressupost', q_sub='Si has configurat la teva {n}, la configuració va inclosa al missatge. Et contesto amb el pressupost per escrit.',
 q_name='Nom', q_tel='Telèfon', q_email='Correu', q_zone='Zona o port', q_when='Per a quan?', q_msg='Explica-m’ho', q_opt='(opcional)',
 q_when_o=['Sense pressa / informant-me', 'Temporada 2027', 'Com més aviat millor'], q_cfg='La teva configuració',
 q_msg_ph='Ús, nombre de persones, colors, motors…', q_send='Sol·licitar pressupost',
 q_priv='Responsable: Juan Morante (Plata Marine). Faré servir aquestes dades només per contestar-te i preparar el teu pressupost. Si avancem, les compartiré amb Mar.Co per emetre la comanda. Pots exercir els teus drets a juan@platamarine.com.',
 q_privl='Política de privacitat', q_cons='He llegit la informació de privacitat i accepto que facis servir aquestes dades per contestar-me.', q_req='Els camps amb * són obligatoris.',
 faq_h='Preguntes freqüents',
 faq=[('Quina titulació necessito?', '{lic}, per la seva eslora de {l}. És orientatiu: confirma-ho amb la teva escola nàutica o amb Capitania.'),
      ('Què inclou el preu?', 'El vaixell amb l’equipament de sèrie, a fàbrica (Itàlia) i sense impostos. Els motors, el transport fins a Barcelona, l’IVA, l’impost de matriculació i la matriculació van a part i te’ls detallo al pressupost.'),
      ('Puc triar colors i acabats?', 'Sí. Cada Mar.Co es fabrica per encàrrec: a més de les opcions de la tarifa, la drassana fa acabats a mida. Digues-me què tens al cap i ho consulto.'),
      ('I si ja tinc motors?', 'Es pot estudiar. L’important és que la potència i el tipus de cua encaixin amb el vaixell: ho mirem amb la drassana abans de la comanda.')],
 others='Els altres models Mar.Co', all='Veure tota la gamma →', see='Veure el model →',
 end_h='En parlem, de la teva {n}?', end_p='Escriu-me i ho mirem amb calma. Sense compromís.', wa='Escriure per WhatsApp',
 wa_txt='Hola Juan, m’interessa la Mar.Co {n}.',
 small='Preus de la tarifa pública de la drassana (revisió 09/2026), sense IVA, sense motors i a fàbrica (EXW, Itàlia). No inclouen motors, transport, impost de matriculació (IEDMT) ni matriculació. L’IVA que es mostra és orientatiu (21 %). Poden canviar i no són vinculants: el preu final és el del pressupost per escrit. Fotos, vídeos i dades tècniques del fabricant; les fotos poden mostrar equipament opcional. La titulació és orientativa: confirma-la amb la teva escola o amb Capitania. Ens podem equivocar; si veus un error, avisa’ns.',
  b_print='Descarregar oferta en PDF',
 ie_l='Impost de matriculació (12 %)', ie_all='Total amb IVA i impost de matriculació', ie_note='Calculat sobre vaixell i opcionals. Motors i transport, a part.', ie_unk='Impost de matriculació: depèn de l’eslora que consti als papers del vaixell; t’ho confirmo al pressupost.',
 why={'ht':'Requereix el Hard-Top','rb':'Requereix el roll-bar','br':'Requereix el suport de motors (bracket)','aft':'Requereix un tendal de popa','win':'Requereix el molinet','plot':'Requereix un GPS Garmin','aud':'Requereix un equip d’àudio','lp':'Requereix els punts d’hissada','x_ht':'Amb Hard-Top, tria la versió per a Hard-Top','x_rb':'Només sense roll-bar','x_br':'Amb bracket, tria la versió amb bracket','x_fullcov':'Inclosa a la funda completa','x_chcov':'Inclosa a la funda de consola i banc'},
 dl_h='Descarrega la teva oferta en PDF', dl_p='Deixa’m les teves dades i et descarregues l’oferta amb la teva configuració i un número d’oferta, perquè en parlem quan vulguis.', dl_btn='Descarregar PDF', dl_wait='Preparant la teva oferta…', dl_close='Tancar',
 sh_offer='Oferta', sh_for='Preparada per a', sh_date='Data', sh_cfg='La teva configuració', sh_specs='Dades principals', sh_scan='Escaneja el codi per veure o canviar aquesta configuració al web',
 sh_valid='Oferta orientativa amb els preus de la tarifa oficial de la drassana (revisió 09/2026). No és vinculant: el preu final és el del pressupost per escrit. Motors, transport des de fàbrica i despeses de matriculació, a part.',
 sh_lic='Titulació',
 print_h='Resum de configuració', print_d='Data', print_c='Plata Marine · Juan Morante · +34 633 742 973 · juan@platamarine.com · www.platamarine.com',
 nophoto='Fotos d’aquest model, aviat', e44_note='Et passo el preu i la llista d’opcionals de l’E-Motion 44 per escrit.',
 lic_per='PER o superior', lic_pnb='PNB o superior',
 eng_label={'mer': 'Mercury', 'oth': 'Una altra marca', 'adv': 'Aconsella’m'},
),
'en': dict(
 home='Home', boats='Boats for sale', new='New boats', vat='+ taxes', noeng='without engines', from_='From', ask='Price on request',
 nav=['Photos', 'Configure', 'Standard', 'Specs', 'Quote'],
 t_title='Mar.Co {n}: price & configurator · Plata Marine',
 t_desc='New Mar.Co {n}, built to order: {k} photos, specs and a configurator with the official price list. {p}',
 t_desc_ask='New Mar.Co {n}, built to order: shipyard photos and specifications. Price on request.',
 kind={'cab': 'Cabin RIB', 'open': 'Open RIB'}, h_cta='Configure yours', h_ph='See all {k} photos',
 g_k='Photos', g_h='The {n}, inside and out', g_sub='Official shipyard photos. Tap any of them to enlarge it and move between them with the arrows. They may show optional equipment.',
 g_more='See all {k} photos',
 c_k='Configurator', c_h='Configure your {n}', c_sub='Choose version, engines and options with the prices from the official Mar.Co price list. The total updates instantly and you can send it to me so I can prepare a written quote.',
 c_s1='1. Version', c_s2='2. Engines', c_s3='3. Optional equipment', c_std='Standard', c_inf='Infusion laminated', c_inf_d='Lighter and stiffer',
 c_std_d='Hand-laid fibreglass',
 e_mer='Mercury', e_mer_d='Fitted by the shipyard', e_oth='Another brand', e_oth_d='Yamaha, Suzuki, Honda…', e_adv='Advise me', e_adv_d='Depending on how you use it',
 e_note='Maximum rated power: {p}. Engines are not in the shipyard price list: I quote them separately.',
 cats={'top': 'Hard-Top, roll-bar and sunshades', 'deck': 'Deck coverings', 'paint': 'Paint', 'comfort': 'Comfort on board', 'elec': 'Electronics, lighting and audio', 'gear': 'Anchoring, handling and stern', 'cover': 'Covers', 'other': 'Other'},
 one='Only one option in this group', sum_h='Your {n}', sum_base='Boat', sum_opts='Options', sum_none='None',
 sum_tot='Total excl. taxes', sum_iva='Incl. VAT (21%)', sum_eng='Engines', sum_extra='Engines, transport from the factory and registration tax are extra.',
 b_send='Request a quote for this configuration', b_share='Copy link', b_copied='Link copied', b_reset='Start again',
 s_k='Standard equipment', s_h='What comes as standard', f_k='Specifications', f_h='Technical data',
 v_k='Video', v_h='The {n} on the water', v_sub='Official Mar.Co videos. They only load from YouTube when you press play.', v_play='Play the video',
 how_h='How to buy a Mar.Co', how=[('We talk', 'Tell me how you will use it and I will help you choose model, engines and options.'), ('Written quote', 'With your configuration I send you a firm price: boat, options, engines and transport.'), ('Factory order', 'It is built to order in Italy. I handle the order and follow it up.'), ('Delivery', 'I am with you at delivery, with the paperwork and the registration.')],
 q_h='Request your quote', q_sub='If you have configured your {n}, the configuration is included in the message. I will reply with a written quote.',
 q_name='Name', q_tel='Phone', q_email='Email', q_zone='Area or marina', q_when='When for?', q_msg='Tell me more', q_opt='(optional)',
 q_when_o=['No rush / just looking', '2027 season', 'As soon as possible'], q_cfg='Your configuration',
 q_msg_ph='Use, number of people, colours, engines…', q_send='Request a quote',
 q_priv='Data controller: Juan Morante (Plata Marine). I will only use these details to reply and prepare your quote. If we go ahead, I will share them with Mar.Co to place the order. You can exercise your rights at juan@platamarine.com.',
 q_privl='Privacy policy', q_cons='I have read the privacy information and agree that you use these details to reply to me.', q_req='Fields marked * are required.',
 faq_h='Frequently asked questions',
 faq=[('Which licence do I need?', '{lic}, given its {l} length. This is a guide only: please check with your sailing school or the harbour authority.'),
      ('What does the price include?', 'The boat with its standard equipment, ex works (Italy) and excluding taxes. Engines, transport to Barcelona, VAT, registration tax and registration are extra and detailed in the quote.'),
      ('Can I choose colours and finishes?', 'Yes. Every Mar.Co is built to order: besides the options in the price list, the shipyard does bespoke finishes. Tell me what you have in mind and I will ask.'),
      ('What if I already have engines?', 'It can be looked at. What matters is that the power and shaft length suit the boat: we check it with the shipyard before ordering.')],
 others='The other Mar.Co models', all='See the whole range →', see='See the model →',
 end_h='Shall we talk about your {n}?', end_p='Write to me and we will look at it calmly. No commitment.', wa='Message on WhatsApp',
 wa_txt='Hi Juan, I am interested in the Mar.Co {n}.',
 small='Prices from the shipyard’s public price list (revision 09/2026), excluding VAT, without engines and ex works (EXW, Italy). They do not include engines, transport, Spanish registration tax (IEDMT) or registration. The VAT shown is a guide (21%). They may change and are not binding: the final price is the one in the written quote. Photos, videos and technical data from the manufacturer; photos may show optional equipment. The licence is a guide only: please check with your school or the harbour authority. We may make mistakes; if you spot one, please let us know.',
  b_print='Download offer as PDF',
 ie_l='Spanish registration tax (12%)', ie_all='Total incl. VAT and registration tax', ie_note='Calculated on boat and options. Engines and transport are extra.', ie_unk='Registration tax: depends on the length stated in the boat’s papers; I will confirm it in the quote.',
 why={'ht':'Requires the Hard-Top','rb':'Requires the roll-bar','br':'Requires the engine bracket','aft':'Requires an aft sunshade','win':'Requires the windlass','plot':'Requires a Garmin GPS','aud':'Requires an audio system','lp':'Requires the lifting points','x_ht':'With the Hard-Top, choose the Hard-Top version','x_rb':'Only without roll-bar','x_br':'With the bracket, choose the bracket version','x_fullcov':'Included in the full cover','x_chcov':'Included in the console and helm bench cover'},
 dl_h='Download your offer as PDF', dl_p='Leave me your details and download the offer with your configuration and an offer number, so we can talk about it whenever you like.', dl_btn='Download PDF', dl_wait='Preparing your offer…', dl_close='Close',
 sh_offer='Offer', sh_for='Prepared for', sh_date='Date', sh_cfg='Your configuration', sh_specs='Main data', sh_scan='Scan the code to view or change this configuration on the website',
 sh_valid='Indicative offer based on the shipyard’s official price list (revision 09/2026). Not binding: the final price is the one in the written quote. Engines, transport from the factory and registration fees are extra.',
 sh_lic='Licence',
 print_h='Configuration summary', print_d='Date', print_c='Plata Marine · Juan Morante · +34 633 742 973 · juan@platamarine.com · www.platamarine.com',
 nophoto='Photos of this model coming soon', e44_note='I will send you the E-Motion 44 price and options list in writing.',
 lic_per='Spanish PER or higher', lic_pnb='Spanish PNB or higher',
 eng_label={'mer': 'Mercury', 'oth': 'Another brand', 'adv': 'Advise me'},
),
'fr': dict(
 home='Accueil', boats='Bateaux à vendre', new='Bateaux neufs', vat='+ taxes', noeng='sans moteurs', from_='À partir de', ask='Prix sur demande',
 nav=['Photos', 'Configurer', 'De série', 'Fiche', 'Devis'],
 t_title='Mar.Co {n} : prix et configurateur · Plata Marine',
 t_desc='Mar.Co {n} neuf, sur commande : {k} photos, fiche technique et configurateur au tarif officiel. {p}',
 t_desc_ask='Mar.Co {n} neuf, sur commande : photos du chantier et fiche technique. Prix sur demande.',
 kind={'cab': 'Semi-rigide cabine', 'open': 'Semi-rigide open'}, h_cta='Configurez-le', h_ph='Voir les {k} photos',
 g_k='Photos', g_h='Le {n}, dedans et dehors', g_sub='Photos officielles du chantier. Touchez-en une pour l’agrandir et passez de l’une à l’autre avec les flèches. Elles peuvent montrer des options.',
 g_more='Voir les {k} photos',
 c_k='Configurateur', c_h='Configurez votre {n}', c_sub='Choisissez version, moteurs et options avec les prix du tarif officiel Mar.Co. Le total se met à jour aussitôt et vous pouvez me l’envoyer pour que je prépare un devis écrit.',
 c_s1='1. Version', c_s2='2. Moteurs', c_s3='3. Équipement optionnel', c_std='Standard', c_inf='Stratifié par infusion', c_inf_d='Plus léger et plus rigide',
 c_std_d='Stratification au contact',
 e_mer='Mercury', e_mer_d='Montés par le chantier', e_oth='Autre marque', e_oth_d='Yamaha, Suzuki, Honda…', e_adv='Conseillez-moi', e_adv_d='Selon votre usage',
 e_note='Puissance maximale homologuée : {p}. Les moteurs ne figurent pas au tarif du chantier : je vous les chiffre à part.',
 cats={'top': 'Hard-Top, roll-bar et tauds', 'deck': 'Revêtements de pont', 'paint': 'Peinture', 'comfort': 'Confort à bord', 'elec': 'Électronique, éclairage et audio', 'gear': 'Mouillage, manœuvre et poupe', 'cover': 'Housses', 'other': 'Autres'},
 one='Une seule option dans ce groupe', sum_h='Votre {n}', sum_base='Bateau', sum_opts='Options', sum_none='Aucune',
 sum_tot='Total hors taxes', sum_iva='TVA espagnole incl. (21 %)', sum_eng='Moteurs', sum_extra='Moteurs, transport depuis l’usine et taxe d’immatriculation en sus.',
 b_send='Demander un devis pour cette configuration', b_share='Copier le lien', b_copied='Lien copié', b_reset='Recommencer',
 s_k='Équipement de série', s_h='Ce qui est de série', f_k='Fiche technique', f_h='Caractéristiques techniques',
 v_k='Vidéo', v_h='Le {n} sur l’eau', v_sub='Vidéos officielles de Mar.Co. Elles ne se chargent depuis YouTube que lorsque vous appuyez sur lecture.', v_play='Lire la vidéo',
 how_h='Comment acheter un Mar.Co', how=[('On en parle', 'Vous me dites comment vous allez l’utiliser et je vous aide à choisir modèle, moteurs et options.'), ('Devis écrit', 'Avec votre configuration je vous envoie un prix ferme : bateau, options, moteurs et transport.'), ('Commande à l’usine', 'Il est construit sur commande en Italie. Je m’occupe de la commande et du suivi.'), ('Livraison', 'Je vous accompagne à la livraison, pour les papiers et l’immatriculation.')],
 q_h='Demandez votre devis', q_sub='Si vous avez configuré votre {n}, la configuration est jointe au message. Je vous réponds avec un devis écrit.',
 q_name='Nom', q_tel='Téléphone', q_email='E-mail', q_zone='Zone ou port', q_when='Pour quand ?', q_msg='Dites-m’en plus', q_opt='(facultatif)',
 q_when_o=['Pas pressé / je me renseigne', 'Saison 2027', 'Dès que possible'], q_cfg='Votre configuration',
 q_msg_ph='Usage, nombre de personnes, couleurs, moteurs…', q_send='Demander un devis',
 q_priv='Responsable : Juan Morante (Plata Marine). J’utiliserai ces données uniquement pour vous répondre et préparer votre devis. Si nous avançons, je les transmettrai à Mar.Co pour passer la commande. Vous pouvez exercer vos droits à juan@platamarine.com.',
 q_privl='Politique de confidentialité', q_cons='J’ai lu les informations de confidentialité et j’accepte que vous utilisiez ces données pour me répondre.', q_req='Les champs marqués * sont obligatoires.',
 faq_h='Questions fréquentes',
 faq=[('Quel permis faut-il ?', '{lic}, vu sa longueur de {l}. C’est indicatif : vérifiez auprès de votre école ou de la Capitainerie.'),
      ('Que comprend le prix ?', 'Le bateau avec son équipement de série, départ usine (Italie) et hors taxes. Les moteurs, le transport jusqu’à Barcelone, la TVA, la taxe d’immatriculation et l’immatriculation sont en sus et détaillés dans le devis.'),
      ('Puis-je choisir couleurs et finitions ?', 'Oui. Chaque Mar.Co est construit sur commande : en plus des options du tarif, le chantier réalise des finitions sur mesure. Dites-moi ce que vous avez en tête et je me renseigne.'),
      ('Et si j’ai déjà des moteurs ?', 'C’est envisageable. L’essentiel est que la puissance et la longueur d’arbre conviennent au bateau : on le vérifie avec le chantier avant la commande.')],
 others='Les autres modèles Mar.Co', all='Voir toute la gamme →', see='Voir le modèle →',
 end_h='On parle de votre {n} ?', end_p='Écrivez-moi et on regarde ça tranquillement. Sans engagement.', wa='Écrire sur WhatsApp',
 wa_txt='Bonjour Juan, le Mar.Co {n} m’intéresse.',
 small='Prix du tarif public du chantier (révision 09/2026), hors TVA, sans moteurs et départ usine (EXW, Italie). Ils n’incluent pas les moteurs, le transport, la taxe d’immatriculation espagnole (IEDMT) ni l’immatriculation. La TVA affichée est indicative (21 %). Ils peuvent changer et ne sont pas contractuels : le prix final est celui du devis écrit. Photos, vidéos et données techniques du constructeur ; les photos peuvent montrer des options. Le permis est indicatif : vérifiez auprès de votre école ou de la Capitainerie. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous.',
  b_print='Télécharger l’offre en PDF',
 ie_l='Taxe d’immatriculation espagnole (12 %)', ie_all='Total TVA et taxe d’immatriculation incl.', ie_note='Calculé sur le bateau et les options. Moteurs et transport en sus.', ie_unk='Taxe d’immatriculation : dépend de la longueur indiquée dans les papiers du bateau ; je vous la confirme dans le devis.',
 why={'ht':'Nécessite le Hard-Top','rb':'Nécessite le roll-bar','br':'Nécessite le support moteurs (bracket)','aft':'Nécessite un taud arrière','win':'Nécessite le guindeau','plot':'Nécessite un GPS Garmin','aud':'Nécessite un système audio','lp':'Nécessite les points de levage','x_ht':'Avec le Hard-Top, choisissez la version Hard-Top','x_rb':'Uniquement sans roll-bar','x_br':'Avec le bracket, choisissez la version avec bracket','x_fullcov':'Incluse dans la housse complète','x_chcov':'Incluse dans la housse console et banquette'},
 dl_h='Téléchargez votre offre en PDF', dl_p='Laissez-moi vos coordonnées et téléchargez l’offre avec votre configuration et un numéro d’offre, pour en parler quand vous voulez.', dl_btn='Télécharger le PDF', dl_wait='Préparation de votre offre…', dl_close='Fermer',
 sh_offer='Offre', sh_for='Préparée pour', sh_date='Date', sh_cfg='Votre configuration', sh_specs='Données principales', sh_scan='Scannez le code pour voir ou modifier cette configuration sur le site',
 sh_valid='Offre indicative basée sur le tarif officiel du chantier (révision 09/2026). Non contractuelle : le prix final est celui du devis écrit. Moteurs, transport depuis l’usine et frais d’immatriculation en sus.',
 sh_lic='Permis',
 print_h='Résumé de configuration', print_d='Date', print_c='Plata Marine · Juan Morante · +34 633 742 973 · juan@platamarine.com · www.platamarine.com',
 nophoto='Photos de ce modèle bientôt', e44_note='Je vous envoie par écrit le prix et la liste d’options de l’E-Motion 44.',
 lic_per='PER espagnol ou supérieur', lic_pnb='PNB espagnol ou supérieur',
 eng_label={'mer': 'Mercury', 'oth': 'Autre marque', 'adv': 'Conseillez-moi'},
),
}

def eur(n, lg):
    if n is None: return ''
    s = f'{n:,}'
    if lg == 'en': return '€' + s
    if lg == 'fr': return s.replace(',', ' ') + ' €'
    return s.replace(',', '.') + ' €'

def tr(s, lg):
    d = TR.get(s)
    return d[lg] if d else s

E = html.escape

CATRX = [
 ('cover', r'canvas|cover for|^cover\b|cover$'),
 ('paint', r'paint'),
 ('deck', r'decking|panelling|flooring|teak for'),
 ('top', r'hard-top|t-top|roll-bar|sunshade|bimini|awning|curtain|totem|handrails|hinge'),
 ('elec', r'garmin|gps|audio|speaker|stereo|hertz|spotlight|inverter|charger|light|sd card|vhf'),
 ('gear', r'winch|windlass|anchor|thruster|ski|lifting|slings|bracket|fuel tank|chain counter|controller'),
 ('comfort', r'fridge|refrigerator|cooktop|stove|heater|cushion|faucet|tap|wc|water disposal|toilet|sink'),
]
CATORDER = ['top', 'deck', 'paint', 'comfort', 'elec', 'gear', 'cover', 'other']
EXCL = [
 ('deck', r'decking|panelling'),
 ('plot', r'garmin (9013|1223|923)|echomap'),
 ('audio', r'^audio:|stereo system'),
 ('charg', r'battery charger'),
 ('lift', r'lifting points|lifting slings|2 lifting points'),
 ('aft', r'^aft sunshade|^aft bimini|rear sunshade awning|rear sun awning'),
 ('hardtop', r'hard-top with|^fiberglass roll-bar'),
 ('frg', r'^42 l drawer fridge|^42 l top-down fridge'),
]
# Compatibilidades (revisadas a mano sobre la tarifa 09/2026): qué aporta cada opción y qué necesita / con qué choca
PROV = [
 ('ht', r'hard-top with'), ('rb', r'^fiberglass roll-bar'), ('br', r'^fiberglass bracket'),
 ('aft', r'^aft sunshade|^aft bimini|rear sunshade awning|rear sun awning'),
 ('win', r'^electrical winch|^electric winch'), ('plot', r'garmin (9013|1223|923)|echomap'),
 ('aud', r'^audio:|stereo system'), ('lp', r'^2 lifting points'),
 ('fullcov', r'^full canvas cover|^cover for inflated'), ('chcov', r'^console and helm bench canvas cover'),
]
REQ = [
 (r'\(with hard-top\)|\(hard-top\)|for hard-top|on hard-top|windshield wiper|for t-top', ['ht']),
 (r'^4 extra speakers', ['ht', 'aud']),
 (r'\(roll-bar\)|roll-bar lowering|hinges kit for fiberglass roll-bar|handrails for roll-bar', ['rb']),
 (r'\(with bracket\)', ['br']),
 (r'side and aft sunshade extension|side sunshade extension|rear sunshade extension', ['aft']),
 (r'windlass remote|hand-held controller for winch', ['win']),
 (r'sd card reader', ['plot']),
 (r'^lifting slings', ['lp']),
]
NOREQ = [
 (r'\(no roll-bar\)', ['rb']),
 (r'^lifting points & slings kit$', ['br']),
 (r'^aft sunshade with 4 carbon poles|^aft bimini with 4 stainless', ['ht']),
 (r'^console canvas cover|^helm.bench canvas cover|^cover for console and driving seat', ['fullcov', 'chcov']),
 (r'^console and helm bench canvas cover', ['fullcov']),
]
def rules(names):
    low = [n.lower() for n in names]
    have = set(k for k, rx in PROV for l in low if re.search(rx, l))
    out = []
    for l in low:
        pv = [k for k, rx in PROV if re.search(rx, l)]
        rq = [k for rx, ks in REQ if re.search(rx, l) for k in ks if k in have and k not in pv]
        nr = [k for rx, ks in NOREQ if re.search(rx, l) for k in ks if k in have]
        out.append((pv, rq, nr))
    return out

def cat(n):
    l = n.lower()
    for c, rx in CATRX:
        if re.search(rx, l): return c
    return 'other'

def excl(n):
    l = n.lower()
    if 'cabin flooring' in l or 'teak for' in l: return ''
    for g, rx in EXCL:
        if re.search(rx, l): return g
    return ''

def lic(lg, eslora):
    return T[lg]['lic_pnb'] if eslora <= 8.0 else T[lg]['lic_per']

def specs(slug, lg):
    if slug == 'e-motion-44': return E44[lg]['dl']
    return EX['marco-' + slug][lg]['dl']

def desc(slug, lg):
    if slug == 'e-motion-44': return E44[lg]['p'][0]
    return EX['marco-' + slug][lg]['p'][0]

def maxpow(slug, lg):
    d = specs(slug, lg)
    for k, v in d.items():
        if k.lower().startswith(('potencia m', 'potència m', 'maximum power', 'puissance m')): return v
    return ''

def photos(slug):
    return PH.get(slug, [])

def img_url(slug, n, m=False):
    if slug in OLD_FOTO and not photos(slug): return OLD_FOTO[slug] + ('-m' if m else '') + '.jpg'
    return f'/marco/fotos/{slug}/{n:02d}' + ('-m' if m else '') + '.jpg'

def cover(slug, which):
    if slug in OLD_FOTO and not photos(slug): return OLD_FOTO[slug] + '.jpg', OLD_FOTO[slug] + '-m.jpg'
    return img_url(slug, which), img_url(slug, which, True)

# ---------- CSS propio de las páginas de modelo ----------
CSS = """
.mm{--line:rgba(127,146,158,.28)}
.mm .wrap{max-width:var(--max);margin:0 auto;padding:0 var(--pad)}
.mm-hero{position:relative;min-height:min(82vh,720px);display:flex;align-items:flex-end;color:#fff;background:#0b1620;overflow:hidden}
.mm-hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.mm-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(6,10,14,.82) 0,rgba(6,10,14,.25) 55%,rgba(6,10,14,.1) 100%)}
.mm-hero .wrap{position:relative;z-index:1;padding-bottom:clamp(28px,6vw,64px);width:100%}
.mm-kick{font-family:var(--display);font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--plata);margin:0 0 8px}
.mm-blogo{display:block;height:clamp(34px,5vw,52px);width:auto;margin:0 0 14px}
.mm-hero h1{font-family:var(--display);font-size:clamp(2.4rem,7vw,4.6rem);line-height:.98;font-weight:800;font-stretch:90%;margin:0;color:#fff}
.mm-hero p.d{max-width:58ch;margin:14px 0 0;font-size:1.05rem;line-height:1.55;color:rgba(255,255,255,.9)}
.mm-price{font-family:var(--display);font-size:clamp(1.3rem,3vw,1.7rem);font-weight:700;margin:18px 0 0}
.mm-price small{font-size:.55em;font-weight:500;color:rgba(255,255,255,.8);margin-left:6px}
.mm .vat{color:#C62828;font-weight:800;font-size:.62em;margin-left:6px}
.mm-hero .vat{color:#ff8a80}
.mm-ctas{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.mm-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font-family:var(--display);font-weight:600;font-size:1rem;padding:13px 22px;border-radius:999px;border:0;cursor:pointer;text-decoration:none;line-height:1.1;transition:background .15s,transform .15s}
.mm-btn.pri{background:var(--wa);color:#fff}.mm-btn.pri:hover{background:var(--wa-hover)}
.mm-btn.gho{background:rgba(255,255,255,.14);color:#fff;border:1px solid rgba(255,255,255,.4)}.mm-btn.gho:hover{background:rgba(255,255,255,.24)}
.mm-btn.ink{background:var(--ink);color:#fff}.mm-btn.ink:hover{background:var(--sea)}
.mm-btn.lin{background:#fff;color:var(--ink);border:1px solid var(--line)}.mm-btn.lin:hover{border-color:var(--ink)}
.mm-keys{display:grid;grid-template-columns:repeat(5,1fr);border-bottom:1px solid var(--line);background:#fff}
.mm-keys div{padding:18px 16px;border-right:1px solid var(--line);text-align:center}
.mm-keys div:last-child{border-right:0}
.mm-keys b{display:block;font-family:var(--display);font-size:1.25rem;font-weight:700;color:var(--ink)}
.mm-keys span{font-size:.78rem;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-2)}
.mm-sub{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.mm-sub .wrap{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none}
.mm-sub .wrap::-webkit-scrollbar{display:none}
.mm-sub a{flex:none;padding:13px 14px;font-family:var(--display);font-weight:600;font-size:.92rem;color:var(--ink-2);text-decoration:none;border-bottom:2px solid transparent}
.mm-sub a:hover,.mm-sub a.on{color:var(--ink);border-bottom-color:var(--wa)}
.mm-sub .q{margin-left:auto;color:var(--wa)}
.mm-sec{padding:clamp(44px,7vw,84px) 0;scroll-margin-top:48px;background:#fff}
.mm-sec.alt{background:var(--paper)}
.mm-sec.dark{background:var(--ink);color:#fff}
.mm-sec.dark h2{color:#fff}
.mm-sec h2{font-family:var(--display);font-size:clamp(1.7rem,4vw,2.5rem);font-weight:800;font-stretch:92%;line-height:1.05;margin:0 0 10px}
.mm-sec .k{font-family:var(--display);font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--sea);margin:0 0 8px}
.mm-sec.dark .k{color:var(--plata)}
.mm-sec p.s{max-width:70ch;color:var(--ink-2);margin:0 0 24px;line-height:1.6}
.mm-sec.dark p.s{color:rgba(255,255,255,.78)}
.mm-gal{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.mm-gal figure{margin:0;border-radius:8px;overflow:hidden;background:var(--paper-2);aspect-ratio:4/3}
.mm-gal figure:first-child{grid-column:span 2;grid-row:span 2}
.mm-gal img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .3s}
.mm-gal img:hover{transform:scale(1.03)}
.mm-gal.fold figure:nth-child(n+12){display:none}
.mm-more{margin-top:18px}
.mm-cfg{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:32px;align-items:start}
.mm-step{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 20px 8px;margin-bottom:16px}
.mm-step h3{font-family:var(--display);font-size:1.15rem;font-weight:700;margin:0 0 14px}
.mm-choice{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin-bottom:12px}
.mm-choice label{position:relative;display:flex;flex-direction:column;gap:3px;padding:14px 14px 13px;border:1.5px solid var(--line);border-radius:12px;cursor:pointer;background:#fff;transition:border-color .15s,box-shadow .15s}
.mm-choice input{position:absolute;opacity:0;pointer-events:none}
.mm-choice label:has(input:checked){border-color:var(--wa);box-shadow:0 0 0 3px rgba(11,118,107,.14)}
.mm-choice label:has(input:focus-visible){outline:2px solid var(--wa);outline-offset:2px}
.mm-choice b{font-family:var(--display);font-size:1rem}
.mm-choice span{font-size:.86rem;color:var(--ink-2)}
.mm-choice em{font-style:normal;font-family:var(--display);font-weight:700;font-size:.95rem;color:var(--ink);margin-top:4px}
.mm-note{font-size:.86rem;color:var(--ink-2);margin:0 0 12px;line-height:1.5}
.mm-cat{border-top:1px solid var(--line);padding:4px 0}
.mm-cat summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;padding:12px 0;font-family:var(--display);font-weight:700;font-size:1rem}
.mm-cat summary::-webkit-details-marker{display:none}
.mm-cat summary i{font-style:normal;font-weight:600;font-size:.8rem;color:var(--wa);background:rgba(11,118,107,.1);border-radius:999px;padding:3px 9px;margin-left:8px}
.mm-cat summary::after{content:"+";font-size:1.3rem;color:var(--ink-2);margin-left:auto;padding-left:12px}
.mm-cat[open] summary::after{content:"−"}
.mm-opt{display:flex;align-items:flex-start;gap:12px;padding:10px 0;border-top:1px dashed rgba(127,146,158,.25);cursor:pointer;font-size:.95rem;line-height:1.4}
.mm-opt input{width:20px;height:20px;min-width:20px;margin:1px 0 0;accent-color:var(--wa)}
.mm-opt span{flex:1}
.mm-opt small{display:block;color:var(--ink-2);font-size:.78rem}
.mm-opt b{font-family:var(--display);white-space:nowrap}
.mm-opt.off{opacity:.45;cursor:not-allowed}.mm-opt .mm-why{color:#b45309}
.mm-sum{position:sticky;top:64px;background:var(--ink);color:#fff;border-radius:16px;padding:22px;box-shadow:0 30px 60px -40px rgba(13,28,39,.7)}
.mm-sum img{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:10px;margin-bottom:14px;display:block}
.mm-sum h3{font-family:var(--display);font-size:1.25rem;font-weight:800;margin:0 0 12px;color:#fff}
.mm-sum dl{margin:0;display:grid;grid-template-columns:1fr auto;gap:6px 12px;font-size:.92rem}
.mm-sum dt{color:rgba(255,255,255,.75)}
.mm-sum dd{margin:0;text-align:right;font-family:var(--display);font-weight:600}
.mm-sum ul{list-style:none;margin:8px 0 0;padding:0;font-size:.82rem;color:rgba(255,255,255,.75);max-height:180px;overflow:auto}
.mm-sum ul li{display:flex;justify-content:space-between;gap:10px;padding:3px 0;border-top:1px solid rgba(255,255,255,.08)}
.mm-tot{border-top:1px solid rgba(255,255,255,.2);margin-top:14px;padding-top:14px}
.mm-tot .big{font-family:var(--display);font-size:1.9rem;font-weight:800;line-height:1.1}
.mm-tot .big .vat{color:#ff8a80}
.mm-tot p{margin:4px 0 0;font-size:.85rem;color:rgba(255,255,255,.75)}
.mm-tot p.mm-all{color:#fff;font-size:.95rem}.mm-tot p.mm-all b{font-family:var(--display)}
.mm-sum .mm-btn{width:100%;margin-top:12px}
.mm-acts{display:flex;gap:8px;margin-top:8px}
.mm-acts button{flex:1;background:transparent;color:#fff;border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:9px 8px;font:600 .82rem var(--display);cursor:pointer}
.mm-acts button:hover{background:rgba(255,255,255,.1)}
.mm-bar{display:none}
.mm-std{columns:2;column-gap:36px;list-style:none;padding:0;margin:0}
.mm-std li{break-inside:avoid;padding:9px 0 9px 26px;border-bottom:1px solid var(--line);position:relative;line-height:1.45}
.mm-std li::before{content:"";position:absolute;left:2px;top:15px;width:12px;height:7px;border-left:2px solid var(--wa);border-bottom:2px solid var(--wa);transform:rotate(-45deg)}
.mm-spec{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-top:1px solid var(--line)}
.mm-spec div{padding:16px 0;border-bottom:1px solid var(--line);padding-right:14px}
.mm-spec dt{font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.mm-spec dd{margin:4px 0 0;font-family:var(--display);font-size:1.15rem;font-weight:700}
.mm-vids{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.mm-video{position:relative;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:#000}
.mm-video button{position:absolute;inset:0;border:0;padding:0;background:none;cursor:pointer}
.mm-video button img{width:100%;height:100%;object-fit:cover;opacity:.75;display:block}
.mm-video .play{position:absolute;left:50%;top:50%;width:74px;height:74px;margin:-37px 0 0 -37px;border-radius:50%;background:rgba(255,255,255,.92);display:flex;align-items:center;justify-content:center}
.mm-video .play svg{width:30px;height:30px;fill:var(--ink);margin-left:4px}
.mm-video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.mm-how{counter-reset:s;list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.mm-how li{counter-increment:s;background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px;line-height:1.45;font-size:.95rem;color:var(--ink-2)}
.mm-how li b{display:block;color:var(--ink);font-family:var(--display);font-size:1.02rem;margin-bottom:4px}
.mm-how li::before{content:counter(s);display:flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;background:var(--wa);color:#fff;font-weight:700;margin-bottom:10px}
.mm-form{display:grid;grid-template-columns:1fr 1fr;gap:14px 16px;max-width:780px}
.mm-form .span2{grid-column:1/-1}
.mm-form label{display:block;font-weight:600;font-size:14px;margin-bottom:6px}
.mm-form label small{font-weight:400;opacity:.75}
.mm-form input,.mm-form select,.mm-form textarea{width:100%;box-sizing:border-box;font:inherit;font-size:16px;padding:11px 12px;border:1px solid rgba(14,48,66,.25);border-radius:8px;background:#fff;color:#0E3042}
.mm-form textarea{min-height:110px;resize:vertical}
.mm-form textarea[readonly]{background:var(--paper);font-size:14px;min-height:90px}
.mm-form .help{font-size:13.5px;line-height:1.5;opacity:.85;margin:0}
.mm-form button{font:inherit;font-weight:600;background:var(--wa);color:#fff;border:0;border-radius:999px;padding:13px 26px;cursor:pointer}
.mm-form button:disabled{opacity:.6;cursor:default}
.mm-faq details{border-bottom:1px solid var(--line);padding:4px 0}
.mm-faq summary{cursor:pointer;padding:14px 0;font-family:var(--display);font-weight:700;font-size:1.05rem}
.mm-faq p{margin:0 0 14px;color:var(--ink-2);line-height:1.6;max-width:75ch}
.mm-others{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}
.mm-others a{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:12px;overflow:hidden;text-decoration:none;color:inherit;background:#fff;transition:transform .15s,box-shadow .15s}
.mm-others a:hover{transform:translateY(-2px);box-shadow:0 18px 30px -24px rgba(13,28,39,.5)}
.mm-others img,.mm-others .np{width:100%;aspect-ratio:16/10;object-fit:cover;display:block;background:var(--sea-deep)}
.mm-others div{padding:12px 14px 14px}
.mm-others b{display:block;font-family:var(--display);font-size:1.08rem}
.mm-others span{font-size:.88rem;color:var(--ink-2)}
.mm-end{position:relative;color:#fff;background:#0b1620;overflow:hidden;text-align:center}
.mm-end>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.45}
.mm-end .wrap{position:relative;padding:clamp(60px,10vw,120px) var(--pad)}
.mm-end h2{color:#fff}
.mm-end p{color:rgba(255,255,255,.85);margin:0 0 22px}
.mm-end .mm-ctas{justify-content:center}
.mm-small{font-size:.8rem;line-height:1.55;color:var(--ink-2);margin:28px auto 48px;max-width:90ch}

@media (max-width:1000px){.mm-cfg{grid-template-columns:1fr}.mm-sum{position:static}.mm-how{grid-template-columns:1fr 1fr}
 .mm-bar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:40;background:var(--ink);color:#fff;padding:10px 16px calc(10px + env(safe-area-inset-bottom));align-items:center;gap:12px;box-shadow:0 -10px 30px rgba(0,0,0,.25);transform:translateY(110%);transition:transform .25s}
 .mm-bar.on{transform:none}.mm-bar div{flex:1;line-height:1.2}.mm-bar small{display:block;font-size:.72rem;color:rgba(255,255,255,.7)}
 .mm-bar b{font-family:var(--display);font-size:1.15rem}.mm-bar .vat{color:#ff8a80}.mm-bar a{background:var(--wa);color:#fff;text-decoration:none;font:600 .9rem var(--display);padding:10px 16px;border-radius:999px;white-space:nowrap}}
@media (max-width:760px){.mm-keys{grid-template-columns:repeat(3,1fr)}.mm-keys div:nth-child(3){border-right:0}.mm-keys div:nth-child(n+4){border-top:1px solid var(--line)}
 .mm-gal{grid-template-columns:repeat(2,1fr)}.mm-gal.fold figure:nth-child(n+8){display:none}.mm-std{columns:1}.mm-spec{grid-template-columns:1fr 1fr}.mm-form{grid-template-columns:1fr}.mm-how{grid-template-columns:1fr}.mm-hero{min-height:74vh}}
.mm-dl{position:fixed;inset:0;z-index:2147483001;background:rgba(6,10,14,.6);display:flex;align-items:center;justify-content:center;padding:16px}
.mm-dl[hidden]{display:none}
.mm-dl>div{background:#fff;border-radius:16px;max-width:460px;width:100%;padding:24px 22px;box-shadow:0 30px 80px rgba(0,0,0,.35);max-height:92vh;overflow:auto;position:relative}
.mm-dl h3{font-family:var(--display);font-size:1.3rem;margin:0 0 8px;padding-right:30px}
.mm-dl p.i{color:var(--ink-2);font-size:.93rem;line-height:1.5;margin:0 0 14px}
.mm-dl .x{position:absolute;top:10px;right:12px;border:0;background:none;font-size:26px;cursor:pointer;color:var(--ink-2)}
.mm-dl .mm-form{grid-template-columns:1fr}
#mm-sheet{display:none}
@media print{@page{size:A4;margin:0}
 html,body{background:#fff!important}body>*:not(#mm-sheet){display:none!important}
 #mm-sheet{display:block;color:#0D1C27;font:9.5pt/1.4 "Helvetica Neue",Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
 #mm-sheet .pg{width:210mm;box-sizing:border-box;padding:10mm 13mm 8mm;position:relative}
 #mm-sheet .hd{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #B58A2C;padding-bottom:5mm}
 #mm-sheet .hd img{height:10mm;width:auto}#mm-sheet .hd img.b{height:9mm}
 #mm-sheet .meta{display:flex;justify-content:space-between;align-items:flex-end;margin:4mm 0 3mm}
 #mm-sheet .meta .k{font-size:7.5pt;letter-spacing:.14em;text-transform:uppercase;color:#17465F;font-weight:700}
 #mm-sheet .meta h1{font-size:23pt;line-height:1.05;margin:1.5mm 0 1mm;font-weight:800}
 #mm-sheet .meta .s{color:#44545F}
 #mm-sheet .ref{text-align:right;border:1px solid #0D1C27;border-radius:3mm;padding:2.5mm 4mm}
 #mm-sheet .ref b{display:block;font-size:12pt;letter-spacing:.04em}
 #mm-sheet .ref span{font-size:7.5pt;color:#44545F;display:block}
 #mm-sheet .hero{width:100%;height:62mm;object-fit:cover;border-radius:3mm;display:block}
 #mm-sheet .th{display:grid;grid-template-columns:repeat(3,1fr);gap:2.5mm;margin-top:2.5mm}
 #mm-sheet .th img{width:100%;height:21mm;object-fit:cover;border-radius:2mm;display:block}
 #mm-sheet .cols{display:grid;grid-template-columns:1.55fr 1fr;gap:7mm;margin-top:4.5mm;font-size:8.6pt}
 #mm-sheet h2{font-size:8pt;letter-spacing:.14em;text-transform:uppercase;color:#17465F;margin:0 0 2mm;font-weight:700}
 #mm-sheet table{width:100%;border-collapse:collapse}
 #mm-sheet td{padding:1.1mm 0;border-bottom:.3mm solid #dfe4e7;vertical-align:top}
 #mm-sheet td:last-child{text-align:right;white-space:nowrap;padding-left:3mm;font-weight:600}
 #mm-sheet dl{margin:0;display:grid;grid-template-columns:1fr auto;gap:1.4mm 3mm}
 #mm-sheet dt{color:#44545F}#mm-sheet dd{margin:0;text-align:right;font-weight:700}
 #mm-sheet .tot{margin-top:4mm;background:#0D1C27;color:#fff;border-radius:3mm;padding:4.5mm 5mm;display:flex;justify-content:space-between;align-items:center;page-break-inside:avoid}
 #mm-sheet .tot .l{font-size:8pt;letter-spacing:.12em;text-transform:uppercase;color:#B7C3CB}
 #mm-sheet .tot .v{font-size:20pt;font-weight:800}
 #mm-sheet .tot .vat{color:#ff8a80;font-size:10pt;font-weight:800;margin-left:2mm}
 #mm-sheet .tot .iva{font-size:8pt;color:#B7C3CB;text-align:right;max-width:75mm;line-height:1.5}
 #mm-sheet .ft{display:flex;gap:6mm;align-items:center;margin-top:4mm;page-break-inside:avoid}
 #mm-sheet .ft .qr{width:24mm;height:24mm;flex:none}#mm-sheet .ft .qr svg{width:100%;height:100%;display:block}
 #mm-sheet .ft .c b{font-size:11pt;display:block}#mm-sheet .ft .c{line-height:1.55}
 #mm-sheet .ft .c small{display:block;color:#44545F;font-size:7.5pt}
 #mm-sheet .sm{font-size:6.8pt;color:#6b7a84;margin-top:3mm;line-height:1.4}
 #mm-sheet.many .th{display:none}#mm-sheet.many .hero{height:52mm}
}
"""

def page(lg, mi):
    slug, name, tkey, kind, eslora, vids, cov, endp = MODELS[mi]
    t = T[lg]; P = LANGS[lg]; full = 'Mar.Co ' + name
    tar = TAR.get(tkey) if tkey else None
    ph = photos(slug)
    src = open(os.path.join(ROOT, P.lstrip('/'), 'marco', 'index.html') if P else os.path.join(ROOT, 'marco', 'index.html')).read()
    head_end = src.find('</head>')
    _i = src.find('<style>'); base_style = src[_i:src.find('</style>', _i) + 8] if 0 <= _i < head_end else ''
    body0 = src.find('<body'); hdr_end = src.find('</header>') + len('</header>')
    header = src[body0:hdr_end]
    for l2, p2 in LANGS.items():
        header = header.replace(f'href="{SITE}{p2}/marco/"', f'href="{SITE}{p2}/marco/{slug}/"')
    foot = src[src.find('<footer'):]
    url = f'{SITE}{P}/marco/{slug}/'
    price = tar['price'] if tar else None
    k = len(ph)
    pstr = (f"{t['from_']} {eur(price, lg)} {t['vat']} {t['noeng']}." if price else '')
    title = t['t_title'].format(n=name)
    if not tar:  # sin configurador (E-Motion 44)
        title = title.replace('precio y configurador', 'precio y ficha técnica').replace('preu i configurador', 'preu i fitxa tècnica').replace('price & configurator', 'price and specifications').replace('prix et configurateur', 'prix et fiche technique')
    if len(title) > 60: title = title.replace(' et configurateur', ', configurateur')
    dsc = (t['t_desc'].format(n=name, k=k, p=pstr) if price and k else (t['t_desc_ask'].format(n=name) if not price else t['t_desc'].format(n=name, k=k, p=pstr).replace(' 0 ', ' ')))
    if price and not k:
        dsc = {'es': f'Mar.Co {name} nueva, bajo pedido: ficha técnica, equipamiento de serie y configurador con la tarifa oficial. {pstr}',
               'ca': f'Mar.Co {name} nova, per encàrrec: fitxa tècnica, equipament de sèrie i configurador amb la tarifa oficial. {pstr}',
               'en': f'New Mar.Co {name}, built to order: specifications and a configurator with the official price list. {pstr}',
               'fr': f'Mar.Co {name} neuf, sur commande : fiche technique et configurateur avec le tarif officiel. {pstr}'}[lg]
    hero_big, hero_m = cover(slug, cov or 1)
    og = SITE + hero_big
    alts = ''.join(f'<link rel="alternate" hreflang="{l2}" href="{SITE}{p2}/marco/{slug}/">\n' for l2, p2 in LANGS.items()) + f'<link rel="alternate" hreflang="x-default" href="{SITE}/marco/{slug}/">\n'
    crumbs = [(t['home'], f'{SITE}{P}/'), (t['boats'], f'{SITE}{P}/barcos/'), (t['new'], f'{SITE}{P}/barcos-nuevos/'), ('Mar.Co', f'{SITE}{P}/marco/'), (name, url)]
    ld_b = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}
    prod = {"@context": "https://schema.org", "@type": "Product", "name": full, "brand": {"@type": "Brand", "name": "Mar.Co"}, "url": url,
            "image": [SITE + img_url(slug, n) for n, _, _ in ph[:6]] or [og], "description": desc(slug, lg)}
    if not price:  # sin precio no es un Product válido para Google: página sobre la marca
        prod["@type"] = "WebPage"; prod["about"] = prod.pop("brand")
    if price:
        prod["offers"] = {"@type": "Offer", "priceCurrency": "EUR", "price": price, "availability": "https://schema.org/PreOrder", "url": url,
                          "priceSpecification": {"@type": "UnitPriceSpecification", "price": price, "priceCurrency": "EUR", "valueAddedTaxIncluded": False}, "itemCondition": "https://schema.org/NewCondition"}
    head = f'''<!doctype html>
<html lang="{lg}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(dsc)}">
<link rel="canonical" href="{url}">
{alts}<link rel="icon" type="image/png" href="/logo-plata-marine.png">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(dsc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/barcos/barcos.css">
<script src="/consent.js?v=20261006" defer></script>
<script src="/analytics.js?v=20261006" defer></script>
<link rel="stylesheet" href="/nav.css?v=20261019">
<script type="application/ld+json">{json.dumps(ld_b, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(prod, ensure_ascii=False)}</script>
{base_style}
<style>{CSS}</style>
<style>{PQ_CSS}</style>
</head>
'''
    sp = specs(slug, lg)
    def sv(*keys):
        for kk, vv in sp.items():
            if kk.lower().startswith(keys): return vv
        return '—'
    keys = [(sv('eslora total', 'length overall', 'longueur hors'), {'es': 'Eslora', 'ca': 'Eslora', 'en': 'Length', 'fr': 'Longueur'}[lg]),
            (sv('manga', 'mànega', 'beam', 'largeur'), {'es': 'Manga', 'ca': 'Mànega', 'en': 'Beam', 'fr': 'Largeur'}[lg]),
            (sv('personas', 'persones', 'people', 'personnes') if slug != 'e-motion-44' else sv('camarotes', 'cabines', 'cabins'), {'es': 'Personas', 'ca': 'Persones', 'en': 'People', 'fr': 'Personnes'}[lg] if slug != 'e-motion-44' else {'es': 'Camarotes', 'ca': 'Cabines', 'en': 'Cabins', 'fr': 'Cabines'}[lg]),
            (maxpow(slug, lg).split(' (')[0] if '(' in maxpow(slug, lg) and 'kW' in maxpow(slug, lg) else maxpow(slug, lg), {'es': 'Potencia máx.', 'ca': 'Potència màx.', 'en': 'Max. power', 'fr': 'Puiss. max.'}[lg]),
            (lic(lg, eslora).replace(' o superior', '').replace(' or higher', '').replace(' ou supérieur', '').replace('Spanish ', '').replace(' espagnol', ''), {'es': 'Titulación', 'ca': 'Titulació', 'en': 'Licence', 'fr': 'Permis'}[lg])]
    # power in cv for kW values
    mp = maxpow(slug, lg)
    m_cv = re.search(r'≈\s*([\d\.]+)\s*(cv|CV|hp)', mp)
    if m_cv: keys[3] = (m_cv.group(1) + ' ' + ('cv' if lg in ('es',) else ('CV' if lg == 'ca' else 'hp')), keys[3][1])
    prc_html = (f'{t["from_"]} {eur(price, lg)}<span class="vat">{t["vat"]}</span><small>{t["noeng"]}</small>' if price else t['ask'])
    navs = [('fotos', t['nav'][0])] if k else []
    navs += [('configurar', t['nav'][1])] if tar else []
    navs += [('serie', t['nav'][2])] if tar else []
    navs += [('ficha', t['nav'][3]), ('presupuesto', t['nav'][4])]
    o = [head, header, '\n<main class="mm">\n']
    o.append(f'<section class="mm-hero" id="barco"><img src="{hero_big}" srcset="{hero_m} 640w, {hero_big} 1600w" sizes="100vw" alt="{E(full)}" fetchpriority="high"><div class="wrap">'
             f'<img class="mm-blogo" src="/barcos-nuevos/logos/marco-blanco.png" alt="Mar.Co" width="447" height="99" data-nolb><p class="mm-kick">{t["kind"][kind]} · {eslora:.2f} m</p>'.replace('.', ',' if lg != 'en' else '.', 0)
             + f'<h1><span class="sr-only">Mar.Co </span>{E(name)}</h1><p class="d">{E(desc(slug, lg))}</p><p class="mm-price">{prc_html}</p><div class="mm-ctas">'
             + (f'<a class="mm-btn pri" href="#configurar">{t["h_cta"]}</a>' if tar else f'<a class="mm-btn pri" href="#presupuesto">{t["nav"][4]}</a>')
             + (f'<a class="mm-btn gho" href="#fotos">{t["h_ph"].format(k=k)}</a>' if k else '') + '</div></div></section>\n')
    o[-1] = o[-1].replace(f'· {eslora:.2f} m', '· ' + (f'{eslora:.2f}'.replace('.', ',') if lg != 'en' else f'{eslora:.2f}') + ' m')
    o.append('<div class="mm-keys">' + ''.join(f'<div><b>{E(v)}</b><span>{E(l)}</span></div>' for v, l in keys) + '</div>\n')
    o.append('<nav class="mm-sub" aria-label="' + E(full) + '"><div class="wrap">' + ''.join(f'<a href="#{a}"{" class=q" if a == "presupuesto" else ""}>{E(b)}</a>' for a, b in navs) + '</div></nav>\n')
    # Galería
    if k:
        figs = ''.join(f'<figure><img src="{img_url(slug, n, True)}" data-full="{img_url(slug, n)}" alt="{E(full)} · {i + 1}/{k}" width="640" height="{round(640 * h / w)}" loading="lazy" decoding="async"></figure>' for i, (n, w, h) in enumerate(ph))
        fold = k > 11
        o.append(f'<section class="mm-sec" id="fotos"><div class="wrap"><p class="k">{t["g_k"]}</p><h2>{E(t["g_h"].format(n=name))}</h2><p class="s">{t["g_sub"]}</p>'
                 f'<div class="mm-gal{" fold" if fold else ""}" id="mm-gal">{figs}</div>'
                 + (f'<div class="mm-more"><button type="button" class="mm-btn lin" id="mm-more">{t["g_more"].format(k=k)}</button></div>' if fold else '') + '</div></section>\n')
    # Configurador
    if tar:
        opts = []
        for i, op in enumerate(tar['opt']):
            opts.append(dict(i=i, n=tr(op['n'], lg), p=op['p'], c=cat(op['n']), x=excl(op['n'])))
        for op, (pv, rq, nr) in zip(opts, rules([o['n'] for o in tar['opt']])):
            op['pv'], op['rq'], op['nr'] = pv, rq, nr
        groups = {}
        for op in opts: groups.setdefault(op['c'], []).append(op)
        # exclusivos: solo si hay 2+ en el grupo
        cnt = {}
        for op in opts:
            if op['x']: cnt[op['x']] = cnt.get(op['x'], 0) + 1
        ver = f'<label><input type="radio" name="mmv" value="0" checked><b>{t["c_std"]}</b><span>{t["c_std_d"]}</span><em>{eur(tar["price"], lg)}</em></label>'
        if tar.get('infusion'):
            ver += f'<label><input type="radio" name="mmv" value="1"><b>{t["c_inf"]}</b><span>{t["c_inf_d"]}</span><em>{eur(tar["infusion"], lg)}</em></label>'
        else:
            ver = ver.replace(f'<span>{t["c_std_d"]}</span>', '')
        eng = ''.join(f'<label><input type="radio" name="mme" value="{v}"{" checked" if v == "adv" else ""}><b>{t["e_" + v]}</b><span>{t["e_" + v + "_d"]}</span></label>' for v in ('mer', 'oth', 'adv'))
        cats_html = ''
        for c in CATORDER:
            if c not in groups: continue
            rows = ''
            one_html = '<small>' + t['one'] + '</small>'
            for op in sorted(groups[c], key=lambda z: z['p'] or 0):
                xg = op['x'] if cnt.get(op['x'], 0) > 1 else ''
                rows += (f'<label class="mm-opt"><input type="checkbox" name="mmo" value="{op["i"]}" data-p="{op["p"] or 0}"{(' data-x="' + xg + '"') if xg else ""}{(' data-pv="' + ' '.join(op['pv']) + '"') if op['pv'] else ''}{(' data-rq="' + ' '.join(op['rq']) + '"') if op['rq'] else ''}{(' data-nr="' + ' '.join(op['nr']) + '"') if op['nr'] else ''}>'
                         f'<span>{E(op["n"])}{one_html if xg else ""}<small class="mm-why" hidden></small></span><b>+{eur(op["p"], lg)}</b></label>')
            cats_html += f'<details class="mm-cat" data-c="{c}"><summary>{t["cats"][c]}<i hidden></i></summary>{rows}</details>'
        ie_html = (f'<p>{t["ie_l"]}: <span id="mm-ie"></span></p><p class="mm-all">{t["ie_all"]}: <b id="mm-ia"></b></p><p>{t["ie_note"]}</p>' if slug in IEDMT else f'<p>{t["ie_unk"]}</p><p>{t["sum_extra"]}</p>')
        o.append(f'''<section class="mm-sec alt" id="configurar"><div class="wrap"><p class="k">{t["c_k"]}</p><h2>{E(t["c_h"].format(n=name))}</h2><p class="s">{t["c_sub"]}</p>
<div class="mm-cfg" id="mm-cfg" data-base="{tar['price']}" data-inf="{tar.get('infusion') or 0}" data-lang="{lg}">
<div>
<div class="mm-step"><h3>{t["c_s1"]}</h3><div class="mm-choice">{ver}</div></div>
<div class="mm-step"><h3>{t["c_s2"]}</h3><div class="mm-choice">{eng}</div><p class="mm-note">{E(t["e_note"].format(p=maxpow(slug, lg)))}</p></div>
<div class="mm-step"><h3>{t["c_s3"]}</h3>{cats_html}</div>
</div>
<aside class="mm-sum" aria-live="polite"><img src="{hero_m}" alt="" loading="lazy" data-nolb><h3>{E(t["sum_h"].format(n=name))}</h3>
<dl><dt>{t["sum_base"]}</dt><dd id="mm-sb"></dd><dt>{t["sum_eng"]}</dt><dd id="mm-se"></dd><dt>{t["sum_opts"]}</dt><dd id="mm-so"></dd></dl><ul id="mm-sl"></ul>
<div class="mm-tot"><div class="big"><span id="mm-st"></span><span class="vat">{t["vat"]}</span></div><p>{t["sum_iva"]}: <span id="mm-si"></span></p>{ie_html}</div>
<a class="mm-btn pri" href="#presupuesto" id="mm-send">{t["b_send"]}</a>
<div class="mm-acts"><button type="button" id="mm-share">{t["b_share"]}</button><button type="button" id="mm-print">{t["b_print"]}</button></div>
<div class="mm-acts"><button type="button" id="mm-reset">{t["b_reset"]}</button></div>
</aside></div></div></section>
<div class="mm-bar" id="mm-bar"><div><small>{t["sum_tot"]}</small><b id="mm-bt"></b><span class="vat">{t["vat"]}</span></div><a href="#presupuesto">{t["nav"][4]}</a></div>
''')
        std = ''.join(f'<li>{E(tr(s, lg))}</li>' for s in tar['std'])
        o.append(f'<section class="mm-sec" id="serie"><div class="wrap"><p class="k">{t["s_k"]}</p><h2>{t["s_h"]}</h2><ul class="mm-std">{std}</ul></div></section>\n')
    elif slug == 'e-motion-44':
        o.append(f'<section class="mm-sec alt" id="configurar"><div class="wrap"><p class="s" style="margin:0">{t["e44_note"]}</p></div></section>\n')
    # Ficha
    lic_key = {'es': 'Titulación', 'ca': 'Titulació', 'en': 'Licence', 'fr': 'Permis'}[lg]
    spd = ''.join(f'<div><dt>{E(kk)}</dt><dd>{E(vv)}</dd></div>' for kk, vv in sp.items())
    o.append(f'<section class="mm-sec{" alt" if not tar else ""}" id="ficha"><div class="wrap"><p class="k">{t["f_k"]}</p><h2>{t["f_h"]}</h2><dl class="mm-spec">{spd}</dl></div></section>\n')
    # Para quién es / frente al modelo hermano / motores
    pq = PQ.get(slug, {}).get(lg)
    if pq:
        cards = ''.join(f'<div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in pq['c'])
        o.append(f'<section class="mm-sec mm-pq" id="para-quien"><div class="wrap"><p class="k">{PQ_KICK[lg]}</p><h2>{E(pq["h"])}</h2><div class="mm-who">{cards}</div></div></section>\n')
    # Vídeos
    if vids:
        poster = [img_url(slug, n) for n, _, _ in ph[1:3]] or [hero_big]
        vv = ''.join(f'<div class="mm-video" data-yt="{v}"><button type="button" aria-label="{t["v_play"]}: {E(full)}"><img src="{poster[i % len(poster)]}" alt="" loading="lazy"><span class="play"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span></button></div>' for i, v in enumerate(vids))
        o.append(f'<section class="mm-sec dark" id="video"><div class="wrap"><p class="k">{t["v_k"]}</p><h2>{E(t["v_h"].format(n=name))}</h2><p class="s">{t["v_sub"]}</p><div class="mm-vids">{vv}</div></div></section>\n')
    # Cómo se compra + formulario
    how = ''.join(f'<li><b>{a}</b>{b}</li>' for a, b in t['how'])
    when = ''.join(f'<option>{E(x)}</option>' for x in t['q_when_o'])
    o.append(f'''<section class="mm-sec alt" id="presupuesto"><div class="wrap"><h2 style="margin-bottom:26px">{t["how_h"]}</h2><ol class="mm-how">{how}</ol>
<h2 style="margin:56px 0 10px">{t["q_h"]}</h2><p class="s">{E(t["q_sub"].format(n=name))}</p>
<form id="mcForm" class="mm-form" novalidate data-contact-intent="marco" data-model="{E(full)}">
<div class="span2" id="mc_cfg_w" hidden><label for="mc_cfg">{t["q_cfg"]}</label><textarea id="mc_cfg" name="mc_cfg" readonly></textarea></div>
<div><label for="mc_name">{t["q_name"]} <i>*</i></label><input id="mc_name" name="mc_name" type="text" required autocomplete="name" maxlength="60"></div>
<div><label for="mc_tel">{t["q_tel"]} <i>*</i></label><input id="mc_tel" name="mc_tel" type="tel" required autocomplete="tel" inputmode="tel" maxlength="20" placeholder="+34 6xx xxx xxx"></div>
<div><label for="mc_email">{t["q_email"]} <i>*</i></label><input id="mc_email" name="mc_email" type="email" required autocomplete="email" maxlength="100"></div>
<div><label for="mc_zone">{t["q_zone"]} <small>{t["q_opt"]}</small></label><input id="mc_zone" name="mc_zone" type="text" maxlength="60"></div>
<div><label for="mc_when">{t["q_when"]} <small>{t["q_opt"]}</small></label><select id="mc_when" name="mc_when"><option value=""></option>{when}</select></div>
<div class="span2"><label for="mc_msg">{t["q_msg"]} <small>{t["q_opt"]}</small></label><textarea id="mc_msg" name="mc_msg" maxlength="1500" placeholder="{E(t["q_msg_ph"])}"></textarea></div>
<p class="help span2">{t["q_priv"]} <a href="{P}/privacidad.html">{t["q_privl"]}</a>.</p>
<div class="span2"><label for="mc_consent" style="display:flex;gap:10px;align-items:flex-start;font-weight:400;font-size:14.5px;line-height:1.45;margin:0;cursor:pointer"><input id="mc_consent" name="mc_consent" type="checkbox" required style="width:20px;height:20px;min-width:20px;margin:1px 0 0;padding:0;accent-color:#0B766B"><span>{t["q_cons"]}&nbsp;<i>*</i></span></label></div>
<div class="span2"><button type="submit" id="mc_send">{t["q_send"]}</button></div>
<p class="help span2">{t["q_req"]}</p><p id="mc_status" class="help span2" role="status" aria-live="polite" hidden></p>
</form></div></section>
''')
    # FAQ
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a.format(lic=lic(lg, eslora), l=(f"{eslora:.2f}".replace(".", ",") if lg != "en" else f"{eslora:.2f}") + " m"))}</p></details>' for q, a in t['faq'])
    o.append(f'<section class="mm-sec mm-faq"><div class="wrap"><h2 style="margin-bottom:14px">{t["faq_h"]}</h2>{faq}</div></section>\n')
    # Otros modelos
    oc = ''
    for s2, n2, tk2, k2, l2_, _, c2, _ in MODELS:
        if s2 == slug: continue
        b2, m2 = cover(s2, c2 or 1)
        pr2 = TAR[tk2]['price'] if tk2 else None
        line = (f'{t["from_"]} {eur(pr2, lg)}<span class="vat">{t["vat"]}</span>' if pr2 else t['ask'])
        oc += f'<a href="{P}/marco/{s2}/"><img src="{m2}" alt="Mar.Co {E(n2)}" loading="lazy"><div><b>{E(n2)}</b><span>{t["kind"][k2]} · {(f"{l2_:.2f}".replace(".", ",") if lg != "en" else f"{l2_:.2f}")} m · {line}</span></div></a>'
    o.append(f'<section class="mm-sec alt"><div class="wrap"><h2 style="margin-bottom:22px">{t["others"]}</h2><div class="mm-others">{oc}</div><p style="margin-top:22px"><a class="mm-btn ink" href="{P}/marco/">{t["all"]}</a></p></div></section>\n')
    # Cierre
    eb, em = cover(slug, endp or cov or 1)
    wa = 'https://wa.me/34633742973?text=' + __import__('urllib.parse').parse.quote(t['wa_txt'].format(n=name))
    o.append(f'<section class="mm-end"><img src="{em}" srcset="{em} 640w, {eb} 1600w" sizes="100vw" alt="" loading="lazy" data-nolb><div class="wrap"><h2>{E(t["end_h"].format(n=name))}</h2><p>{t["end_p"]}</p><div class="mm-ctas">'
             f'<a class="mm-btn pri" href="{wa}" target="_blank" rel="noopener" data-wa-context="marco_{slug}">{t["wa"]}</a>' + (f'<a class="mm-btn gho" href="#configurar">{t["h_cta"]}</a>' if tar else '') + '</div></div></section>\n')
    o.append(f'<div class="wrap"><p class="mm-small">{t["small"]}</p></div>\n')
    # Bloque de impresión
    if tar:
        o.append(f'''<div class="mm-dl" id="mm-dl" hidden role="dialog" aria-modal="true" aria-labelledby="mm-dl-h"><div><button type="button" class="x" aria-label="{t["dl_close"]}">×</button><h3 id="mm-dl-h">{t["dl_h"]}</h3><p class="i">{t["dl_p"]}</p>
<form id="mcDl" class="mm-form" novalidate data-contact-intent="marco_pdf">
<div><label for="dl_name">{t["q_name"]} <i>*</i></label><input id="dl_name" name="dl_name" type="text" required autocomplete="name" maxlength="60"></div>
<div><label for="dl_tel">{t["q_tel"]} <i>*</i></label><input id="dl_tel" name="dl_tel" type="tel" required autocomplete="tel" inputmode="tel" maxlength="20" placeholder="+34 6xx xxx xxx"></div>
<div><label for="dl_email">{t["q_email"]} <i>*</i></label><input id="dl_email" name="dl_email" type="email" required autocomplete="email" maxlength="100"></div>
<p class="help">{t["q_priv"]} <a href="{P}/privacidad.html">{t["q_privl"]}</a>.</p>
<div><label for="dl_consent" style="display:flex;gap:10px;align-items:flex-start;font-weight:400;font-size:14px;line-height:1.45;margin:0;cursor:pointer"><input id="dl_consent" name="dl_consent" type="checkbox" required style="width:20px;height:20px;min-width:20px;margin:1px 0 0;padding:0;accent-color:#0B766B"><span>{t["q_cons"]}&nbsp;<i>*</i></span></label></div>
<div><button type="submit" id="dl_send">{t["dl_btn"]}</button></div>
<p id="dl_status" class="help" role="status" aria-live="polite" hidden></p>
</form></div></div>
''')
        data = {'base': tar['price'], 'inf': tar.get('infusion') or 0, 'name': full, 'lang': lg,
                'opts': [[tr(op['n'], lg), op['p']] for op in tar['opt']],
                'L': {k2: t[k2] for k2 in ('sum_none', 'b_copied', 'b_share', 'c_std', 'c_inf', 'sum_base', 'sum_eng', 'sum_opts', 'sum_tot', 'sum_iva', 'vat', 'noeng', 'dl_wait', 'dl_btn', 'sh_offer', 'sh_for', 'sh_date', 'sh_cfg', 'sh_specs', 'sh_scan', 'sh_valid', 'sh_lic', 'ie_l', 'ie_all', 'ie_unk')}, 'eng': t['eng_label'], 'why': t['why'], 'iedmt': slug in IEDMT,
                'kind': t['kind'][kind] + ' · ' + ((f'{eslora:.2f}'.replace('.', ',') if lg != 'en' else f'{eslora:.2f}') + ' m'),
                'code': ''.join(w[0] for w in name.replace('-', ' ').split()).upper()[:3] + re.sub(r'\\D', '', name)[:2],
                'specs': [[k3, v3] for k3, v3 in list(sp.items())[:9]] + [[t['f_k'] and {'es': 'Titulación', 'ca': 'Titulació', 'en': 'Licence', 'fr': 'Permis'}[lg], lic(lg, eslora)]] if not any(k3.lower().startswith(('titul', 'licence', 'permis')) for k3 in sp) else [[k3, v3] for k3, v3 in list(sp.items()) if not k3.lower().startswith(('compart', 'diámetro', 'diàmetre', 'tube', 'diamètre'))][:10],
                'hero': hero_big, 'thumbs': [img_url(slug, n) for n, _, _ in ph[1:4]], 'brandlogo': '/barcos-nuevos/logos/marco.png'}
        o.append(f'<script>window.MC_CFG={json.dumps(data, ensure_ascii=False)};</script>\n<script src="/marco/marco-config.js?v={V}" defer></script>\n')
    o.append(f'<script src="/submit-confirmed.js" defer></script>\n<script src="/marco/marco-form.js?v={V}" defer></script>\n')
    o.append('</main>\n')
    o.append(foot)
    out = ''.join(o)
    if not out.rstrip().endswith('</html>'):
        out = out.rstrip() + '\n</html>\n'
    dst = os.path.join(ROOT, P.lstrip('/'), 'marco', slug) if P else os.path.join(ROOT, 'marco', slug)
    os.makedirs(dst, exist_ok=True)
    open(os.path.join(dst, 'index.html'), 'w').write(out)

for lg in LANGS:
    for i in range(len(MODELS)):
        page(lg, i)
print('ok', len(LANGS) * len(MODELS), 'páginas')
