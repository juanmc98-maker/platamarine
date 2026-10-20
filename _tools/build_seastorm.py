#!/usr/bin/env python3
"""Genera /seastorm/ en ES/CA/EN/FR: página de marca SeaStorm (dealer en Cataluña).
Cabecera y pie salen de /barcos-nuevos/ de cada idioma; el <main> es propio (mismo lenguaje visual que /skipper/).
Uso (desde la raíz del repo):
  python3 _tools/build_seastorm.py                  -> genera las 4 páginas con las fotos que haya en /seastorm/fotos/
  python3 _tools/build_seastorm.py --fotos CARPETA  -> antes prepara las fotos: CARPETA/<slug>-<n>.(jpg|png|webp)
                                                       (p. ej. 17-1.jpg, 13-s-1.jpg…) y CARPETA/logo.png (fondo transparente, letras claras)
                                                       y opcional CARPETA/hero.jpg (portada ya encuadrada)
Las fotos se guardan sin EXIF: <slug>-<n>.jpg (1200 px) y <slug>-<n>-m.jpg (800 px); portada 1000x600.
Un modelo sin fotos se muestra con una tarjeta con el logo (nunca con la foto de otro modelo).

Fuentes (octubre de 2026):
- Datos técnicos, motor recomendado, colores y garantía: fichas y página de garantía de seastorm-boat.com.
- Vídeo: canal oficial de YouTube "SeaStorm Boats" (@SeaStormBoats), id cJr6jiFQrH4 (el que tiene incrustado su web).
- PVP: "Dealers Price List 2027" de Ceranos Invest OÜ, columna "RRP w/o VAT", configuración ADVANTAGE (la única de la tarifa),
  redondeado hacia arriba a .990 por decisión de Juan. RRP original: 17 -> 10.928, 14 -> 7.253, 13s -> 6.683, 12 -> 4.454.
- Titulación: RD 875/2014, art. 10.1.a en la redacción del RD 1188/2025 (vigente desde el 1 de octubre de 2026):
  sin título solo uso privado, motor hasta 5 m de eslora y potencia nominal máxima de 15 CV sin dispositivo reductor,
  de día y a no más de 2 millas de la salida, mayor de 18 años. Licencia de Navegación: hasta 6 m de eslora."""
import re, json, html, urllib.parse, os, sys, glob

ROOT = '.'
BASE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
WA = '34633742973'
FOTOS = f'{ROOT}/seastorm/fotos'
F = '/seastorm/fotos/'
YT = 'cJr6jiFQrH4'
IVA = 0.21

# slug, nombre, eslora, manga, peso casco kg, calado cm, carga kg, pers. C, pers. D, CV máx, kW máx, CV recomendados, PVP sin IVA, eslora>5 m
M = [
 ('12',   'SeaStorm 12',   '3,66', '1,67', 200, 18, 380, 4, 6, 30, 22, '25–30', 4990, False),
 ('13-s', 'SeaStorm 13 S', '4,00', '1,90', 250, 20, 475, 5, 5, 60, 44, '40', 6990, False),
 ('14',   'SeaStorm 14',   '4,28', '1,86', 260, 18, 475, 5, 6, 40, 30, '30–40', 7990, False),
 ('17',   'SeaStorm 17',   '5,17', '1,97', 380, 22, 610, 6, 8, 80, 60, '60', 10990, True),
]
HERO = '17-3'      # foto de portada (fondo del hero)
VIDEO_POSTER = '17-1'
ADV_IMG = '14-4'
TECH_IMG = '14-3'
KEY_IMG = '12-2'   # barcos SeaStorm sobre remolques: para el bloque llave en mano
END_IMG = '17-4'
COLORS = [('#F4F5F2', 'white'), ('#B9BEC2', 'lgrey'), ('#4D555B', 'dgrey'), ('#2F6B3A', 'green'), ('#9BD31F', 'lime'), ('#C62828', 'red'), ('#F2C511', 'yellow')]


def eur(n, lang):
    s = f'{n:,}'
    if lang == 'en':
        return '€' + s
    if lang == 'fr':
        return s.replace(',', ' ') + ' €'
    return s.replace(',', '.') + ' €'


def num(s, lang):
    return s.replace(',', '.') if lang == 'en' else s


def kg(n, lang):
    return f'{n} kg'


T = {
 'es': dict(
  title='SeaStorm en Cataluña: barcos de polietileno desde 4.990 € · Plata Marine',
  desc='Barcos SeaStorm 12, 13 S, 14 y 17 de polietileno (HDPE), de 3,66 a 5,17 m, con 20 años de garantía de casco. Desde 4.990 € +IVA. Dealer en Cataluña: presupuesto llave en mano.',
  crumbs=('Inicio', 'Barcos nuevos'),
  eyebrow='Dealer SeaStorm en Cataluña',
  h1='Barcos de polietileno con 20 años de garantía de casco',
  lead='Cuatro modelos de 3,66 a 5,17 m, fabricados en una sola pieza. Ligeros, pensados para golpes, roces y sol, y sin gelcoat que pulir. Te ayudo a elegir modelo y motor, y te preparo el presupuesto con todo.',
  hfrom='Desde', hnote='versión Advantage, sin motor',
  cta='Pedir presupuesto', cta_wa='Hablar con Juan',
  wa_gen='Hola Juan, me interesa un SeaStorm. ¿Me ayudas a elegir modelo?',
  wa_m='Hola Juan, me interesa el {m}. ¿Me preparas presupuesto?',
  wa_key='Hola Juan, quiero un SeaStorm llave en mano (barco, motor, remolque y matriculación). ¿Me preparas presupuesto?',
  stats=[('20 años', 'de garantía de casco'), ('1 pieza', 'casco de polietileno rotomoldeado'), ('18–22 cm', 'de calado'), ('200–380 kg', 'de peso del casco')],
  nav=[('modelos', 'Modelos'), ('comparar', 'Comparar'), ('llave-en-mano', 'Llave en mano'), ('colores', 'Colores'), ('video', 'Vídeo'), ('faq', 'Preguntas'), ('presupuesto', 'Presupuesto')],
  choose_k='Cuál es el tuyo', choose_h='Cuatro tamaños, el mismo casco duro',
  choose_p='Toca un modelo para ver su ficha, fotos y precio.',
  see='Ver ficha →',
  tag={'12': 'Primer barco o auxiliar', '13-s': 'El deportivo', '14': 'Para todo', '17': 'Familia y pesca'},
  d={'12': 'El más pequeño y el más ligero: 200 kg de casco. Un primer barco para salir cerca de la costa, o una auxiliar que se mueve bien con poco motor.',
     '13-s': 'Casco con dos redanes diseñado por Mannerfeldt Design: planea con motores pequeños y admite hasta 60 CV. Estiba bajo los asientos de proa y popa.',
     '14': 'Líneas clásicas, consola con volante y cofres a proa y popa. Con 18 cm de calado se acerca bien a la playa.',
     '17': 'El más grande de la gama: hasta 8 personas en categoría D, 610 kg de carga y motor de hasta 80 CV. Para salir en familia, pescar o bucear.'},
  lab=dict(loa='Eslora', beam='Manga', w='Peso del casco', dr='Calado', cap='Carga máxima', pax='Personas', hp='Potencia máx.', rec='Motor recomendado', lic='Titulación'),
  pax_v='{c} (cat. C) · {d} (cat. D)', hp_v='{h} CV ({k} kW)', rec_v='{r} CV, eje largo',
  lic_long='Licencia de Navegación o superior', lic_short='Licencia de Navegación o superior',
  lic_note='Sin título, solo con motor de hasta 15 CV (uso privado, de día y a 2 millas como máximo). <a href="{p}/seastorm/#faq-titulo">Ver más</a>',
  from_='Desde', vinc='{v} con IVA', adv='Advantage, sin motor',
  ask_m='Pedir presupuesto', nophoto='Fotos del 13 S, en cuanto las tenga',
  cmp_k='Comparar', cmp_h='Los cuatro, cara a cara', cmp_model='Modelo', cmp_from='Desde (+IVA)',
  adv_k='Versión Advantage', adv_h='Qué incluye el precio',
  adv_p='Los precios son de la versión Advantage, la de la tarifa de fábrica. Viene con:',
  adv_list=['Consola con volante', 'Parabrisas', 'Cojines con respaldo', 'Barandillas laterales', 'Placa de motor'],
  adv_note='El motor, el remolque, el transporte y la matriculación van aparte. Si quieres, te los presupuesto juntos.',
  key_k='Llave en mano', key_h='Barco, motor, remolque y papeles, en un solo presupuesto',
  key_p='Si lo prefieres, te lo dejo listo para echarlo al agua. Te preparo un presupuesto cerrado y por escrito con:',
  key_list=['El SeaStorm que elijas, en versión Advantage', 'El motor recomendado para ese modelo', 'Un remolque adecuado a su peso y a tu coche', 'El transporte desde fábrica', 'La matriculación y los papeles'],
  key_cta='Pídeme presupuesto llave en mano', key_note='El precio depende del motor y del remolque que elijas: te lo doy cerrado antes de pedir nada.',
  tech_k='Polietileno HDPE', tech_h='Por qué un casco de polietileno', tech_p='Cómo están hechos, según el fabricante.',
  tech=[('Una sola pieza', 'Se fabrican por rotomoldeo: el casco sale del molde en una pieza, sin uniones ni pegados.'),
        ('Pensado para golpes y sol', 'Polietileno con estabilizadores UV, resistente a golpes, roces, cambios de temperatura y sol fuerte.'),
        ('Poco mantenimiento', 'No lleva gelcoat que pulir ni repintar.'),
        ('Casco doble y autovaciante', 'Doble casco, autovaciante y de poco calado (de 18 a 22 cm) para acercarte a la playa.'),
        ('Materiales reciclables', 'SeaStorm usa materiales reciclables en sus modelos actuales.'),
        ('20 años de garantía de casco', 'Para el primer comprador, frente a defectos de materiales y fabricación, según las condiciones de SeaStorm.')],
  tech_note='Información del fabricante.',
  col_k='Colores', col_h='Siete colores de casco', col_p='Colores disponibles en los cuatro modelos, según la web del fabricante. En pantalla, los tonos son orientativos.',
  col={'white': 'Blanco', 'lgrey': 'Gris claro', 'dgrey': 'Gris oscuro', 'green': 'Verde', 'lime': 'Verde lima', 'red': 'Rojo', 'yellow': 'Amarillo'},
  vid_k='Vídeo', vid_h='SeaStorm en vídeo', vid_p='Vídeo oficial de SeaStorm. Se carga desde YouTube solo cuando le das al play.', vid_play='Reproducir el vídeo de SeaStorm',
  how_h='Cómo se compra un SeaStorm',
  steps=[('Lo hablamos', 'Me cuentas cómo vas a usarlo y elegimos modelo, motor y color.'),
         ('Presupuesto por escrito', 'Con todo lo que quieras incluir: barco, motor, remolque, transporte y papeles.'),
         ('Pedido a fábrica', 'Se fabrica bajo pedido. El plazo te lo confirmo por escrito.'),
         ('Entrega', 'Coordino el transporte y la matriculación hasta que lo tienes listo.')],
  form_h='Pide tu presupuesto', form_p='Dime qué modelo te interesa y cómo lo vas a usar. Te contesto con el presupuesto por escrito, sin compromiso.',
  f_alt='¿Prefieres escribirme directamente? Por WhatsApp también te contesto.',
  f_model='Modelo', f_dunno='Aún no lo sé', f_need='¿Qué necesitas?', f_needs=[('barco', 'Solo el barco'), ('motor', 'Barco y motor'), ('llave', 'Llave en mano: barco, motor, remolque y matriculación')],
  f_color='Color', f_any='Me da igual / no lo sé', f_name='Nombre', f_tel='Teléfono', f_email='Email', f_zone='Zona o puerto', f_zone_ph='Costa Brava, Barcelona, Tarragona…',
  f_msg='Cuéntame', f_msg_ph='Uso, número de personas, motor, si tienes remolque…', f_opt='(opcional)',
  f_priv='Responsable: Juan Morante (Plata Marine). Usaré estos datos solo para contestarte y preparar tu presupuesto. Puedes ejercer tus derechos en juan@platamarine.com. <a href="/privacidad.html">Política de privacidad</a>.',
  f_consent='He leído la información de privacidad y acepto que uses estos datos para contestarme.', f_send='Pedir presupuesto', f_req='Los campos con * son obligatorios.',
  faq_h='Preguntas frecuentes',
  faq=[('faq-titulo', '¿Necesito titulación?',
        'Desde el 1 de octubre de 2026, sin título solo se puede llevar, para uso privado, un barco de hasta 5 m con un motor de hasta 15 CV (sin limitador de potencia), de día, sin alejarse más de 2 millas de la salida y siendo mayor de 18 años. El 12, el 13 S y el 14 miden menos de 5 m: con un motor de 15 CV no necesitas título, pero con el motor que recomienda la marca (de 25 a 60 CV) necesitas la Licencia de Navegación o superior. El 17 mide 5,17 m, así que siempre necesita Licencia de Navegación o superior. <a href="{p}/titulaciones/">Ver titulaciones</a>.'),
       (None, '¿Cuánto pesa con remolque? ¿Me vale el carnet B?',
        'El casco pesa 200 kg (12), 250 kg (13 S), 260 kg (14) y 380 kg (17), sin motor. A eso súmale el motor, el depósito y el propio remolque. Con el carnet B puedes llevar un remolque de hasta 750 kg de masa máxima autorizada, o uno más pesado si el coche y el remolque juntos no pasan de 3.500 kg. Te digo qué remolque encaja con tu barco y con tu coche.'),
       (None, '¿Qué motor le pongo?',
        'La marca recomienda 25–30 CV para el 12, 40 CV para el 13 S, 30–40 CV para el 14 y 60 CV para el 17, todos con eje largo. Nunca por encima de la potencia máxima de su placa CE (30, 60, 40 y 80 CV). Si quieres llevarlo sin título, el límite es 15 CV.'),
       (None, '¿Cuánto tarda la entrega?',
        'Se fabrican bajo pedido. El plazo depende de la fábrica y de la época del año: te lo confirmo por escrito en el presupuesto, antes de pedir nada.'),
       (None, '¿El transporte desde fábrica está incluido?',
        'No. Llegan en camión desde fábrica y el transporte va aparte. Orientativo: unos 2.090 € un envío compartido (por ejemplo, un 17 y un 13 S) y unos 4.390 € un camión completo. El importe real va en tu presupuesto.'),
       (None, '¿Qué garantía tiene?',
        'SeaStorm da 20 años de garantía en el casco frente a defectos de materiales y fabricación, al primer comprador que lo compra a la marca o a un dealer autorizado y con un uso normal. Los recambios tienen 2 años. El motor, el remolque y los accesorios tienen la garantía de su propio fabricante. No cubre, por ejemplo, poner más potencia o más carga de la que marca la placa CE, accidentes o competición.'),
       (None, '¿Pagan impuesto de matriculación?',
        'No. El impuesto especial de matriculación (IEDMT) solo se aplica a embarcaciones de recreo de más de 8 m de eslora. Sí hay tasas de matriculación, que van en el presupuesto.'),
       (None, '¿El precio incluye IVA y motor?',
        'No. Los precios son sin IVA, de la versión Advantage y sin motor. Junto al precio ves también el importe con el IVA general del 21 %.')],
  about_h='Quién hay detrás',
  about_ss='SeaStorm fabrica barcos de polietileno de una sola pieza y los vende en más de 60 países.',
  about_me_h='Juan Morante',
  about_me='Llevo 12 años de cara al público, ayudando a cada cliente a encontrar lo que necesita. Soy el dealer de SeaStorm en Cataluña: te acompaño desde la primera duda hasta la entrega.',
  end_h='¿Lo vemos?', end_p='Escríbeme y lo hablamos con calma. Sin compromiso.',
  used='¿Buscas un barco de ocasión? <a href="{p}/barcos/#segunda-mano">Ver barcos de segunda mano →</a>',
  float='Pedir presupuesto',
  small='Precios orientativos, sin IVA, según el PVP recomendado de la tarifa 2027 de SeaStorm, versión Advantage, en fábrica: no incluyen motor, equipamiento opcional, remolque, transporte ni matriculación. El importe con IVA se calcula al 21 % como referencia. Transporte y plazos orientativos: dependen de la carga y de la fábrica. Datos técnicos, colores y garantía según la web del fabricante (octubre de 2026). La titulación es orientativa, según el Real Decreto 875/2014 en su redacción vigente desde el 1 de octubre de 2026: confírmala con tu escuela o con Capitanía. Pueden cambiar y no son vinculantes; el precio final es el del presupuesto por escrito. Podemos equivocarnos; si ves un error, avísanos.',
 ),
 'ca': dict(
  title='SeaStorm a Catalunya: vaixells de polietilè des de 4.990 € · Plata Marine',
  desc='Vaixells SeaStorm 12, 13 S, 14 i 17 de polietilè (HDPE), de 3,66 a 5,17 m, amb 20 anys de garantia de buc. Des de 4.990 € +IVA. Dealer a Catalunya: pressupost clau en mà.',
  crumbs=('Inici', 'Vaixells nous'),
  eyebrow='Dealer SeaStorm a Catalunya',
  h1='Vaixells de polietilè amb 20 anys de garantia de buc',
  lead='Quatre models de 3,66 a 5,17 m, fabricats d\'una sola peça. Lleugers, pensats per a cops, fregades i sol, i sense gelcoat per polir. T\'ajudo a triar model i motor, i et preparo el pressupost amb tot.',
  hfrom='Des de', hnote='versió Advantage, sense motor',
  cta='Demanar pressupost', cta_wa='Parlar amb en Juan',
  wa_gen='Hola Juan, m\'interessa un SeaStorm. M\'ajudes a triar model?',
  wa_m='Hola Juan, m\'interessa el {m}. Em prepares pressupost?',
  wa_key='Hola Juan, vull un SeaStorm clau en mà (vaixell, motor, remolc i matriculació). Em prepares pressupost?',
  stats=[('20 anys', 'de garantia de buc'), ('1 peça', 'buc de polietilè rotomodelat'), ('18–22 cm', 'de calat'), ('200–380 kg', 'de pes del buc')],
  nav=[('modelos', 'Models'), ('comparar', 'Comparar'), ('llave-en-mano', 'Clau en mà'), ('colores', 'Colors'), ('video', 'Vídeo'), ('faq', 'Preguntes'), ('presupuesto', 'Pressupost')],
  choose_k='Quin és el teu', choose_h='Quatre mides, el mateix buc dur',
  choose_p='Toca un model per veure\'n la fitxa, les fotos i el preu.',
  see='Veure fitxa →',
  tag={'12': 'Primer vaixell o auxiliar', '13-s': 'L\'esportiu', '14': 'Per a tot', '17': 'Família i pesca'},
  d={'12': 'El més petit i el més lleuger: 200 kg de buc. Un primer vaixell per sortir a prop de la costa, o un auxiliar que es mou bé amb poc motor.',
     '13-s': 'Buc amb dos redans dissenyat per Mannerfeldt Design: planeja amb motors petits i admet fins a 60 CV. Estiba sota els seients de proa i popa.',
     '14': 'Línies clàssiques, consola amb volant i cofres a proa i popa. Amb 18 cm de calat s\'acosta bé a la platja.',
     '17': 'El més gran de la gamma: fins a 8 persones en categoria D, 610 kg de càrrega i motor de fins a 80 CV. Per sortir en família, pescar o bussejar.'},
  lab=dict(loa='Eslora', beam='Mànega', w='Pes del buc', dr='Calat', cap='Càrrega màxima', pax='Persones', hp='Potència màx.', rec='Motor recomanat', lic='Titulació'),
  pax_v='{c} (cat. C) · {d} (cat. D)', hp_v='{h} CV ({k} kW)', rec_v='{r} CV, eix llarg',
  lic_long='Llicència de Navegació o superior', lic_short='Llicència de Navegació o superior',
  lic_note='Sense títol, només amb motor de fins a 15 CV (ús privat, de dia i a 2 milles com a màxim). <a href="{p}/seastorm/#faq-titulo">Més informació</a>',
  from_='Des de', vinc='{v} amb IVA', adv='Advantage, sense motor',
  ask_m='Demanar pressupost', nophoto='Fotos del 13 S, tan aviat com les tingui',
  cmp_k='Comparar', cmp_h='Els quatre, cara a cara', cmp_model='Model', cmp_from='Des de (+IVA)',
  adv_k='Versió Advantage', adv_h='Què inclou el preu',
  adv_p='Els preus són de la versió Advantage, la de la tarifa de fàbrica. Porta:',
  adv_list=['Consola amb volant', 'Parabrisa', 'Coixins amb respatller', 'Baranes laterals', 'Placa de motor'],
  adv_note='El motor, el remolc, el transport i la matriculació van a part. Si vols, te\'ls pressuposto junts.',
  key_k='Clau en mà', key_h='Vaixell, motor, remolc i papers, en un sol pressupost',
  key_p='Si ho prefereixes, te\'l deixo a punt per posar-lo a l\'aigua. Et preparo un pressupost tancat i per escrit amb:',
  key_list=['El SeaStorm que triïs, en versió Advantage', 'El motor recomanat per a aquest model', 'Un remolc adequat al seu pes i al teu cotxe', 'El transport des de fàbrica', 'La matriculació i els papers'],
  key_cta='Demana\'m pressupost clau en mà', key_note='El preu depèn del motor i del remolc que triïs: te\'l dono tancat abans de demanar res.',
  tech_k='Polietilè HDPE', tech_h='Per què un buc de polietilè', tech_p='Com estan fets, segons el fabricant.',
  tech=[('Una sola peça', 'Es fabriquen per rotomodelat: el buc surt del motlle d\'una peça, sense unions ni encolats.'),
        ('Pensat per a cops i sol', 'Polietilè amb estabilitzadors UV, resistent a cops, fregades, canvis de temperatura i sol fort.'),
        ('Poc manteniment', 'No porta gelcoat per polir ni repintar.'),
        ('Buc doble i autobuidant', 'Doble buc, autobuidant i de poc calat (de 18 a 22 cm) per acostar-te a la platja.'),
        ('Materials reciclables', 'SeaStorm fa servir materials reciclables en els models actuals.'),
        ('20 anys de garantia de buc', 'Per al primer comprador, davant de defectes de materials i fabricació, segons les condicions de SeaStorm.')],
  tech_note='Informació del fabricant.',
  col_k='Colors', col_h='Set colors de buc', col_p='Colors disponibles en els quatre models, segons la web del fabricant. En pantalla, els tons són orientatius.',
  col={'white': 'Blanc', 'lgrey': 'Gris clar', 'dgrey': 'Gris fosc', 'green': 'Verd', 'lime': 'Verd llima', 'red': 'Vermell', 'yellow': 'Groc'},
  vid_k='Vídeo', vid_h='SeaStorm en vídeo', vid_p='Vídeo oficial de SeaStorm. Es carrega des de YouTube només quan li dones al play.', vid_play='Reproduir el vídeo de SeaStorm',
  how_h='Com es compra un SeaStorm',
  steps=[('Ho parlem', 'M\'expliques com el faràs servir i triem model, motor i color.'),
         ('Pressupost per escrit', 'Amb tot el que vulguis incloure: vaixell, motor, remolc, transport i papers.'),
         ('Comanda a fàbrica', 'Es fabrica per encàrrec. El termini te\'l confirmo per escrit.'),
         ('Entrega', 'Coordino el transport i la matriculació fins que el tens a punt.')],
  form_h='Demana el teu pressupost', form_p='Digues-me quin model t\'interessa i com el faràs servir. Et contesto amb el pressupost per escrit, sense compromís.',
  f_alt='Prefereixes escriure\'m directament? Per WhatsApp també et contesto.',
  f_model='Model', f_dunno='Encara no ho sé', f_need='Què necessites?', f_needs=[('barco', 'Només el vaixell'), ('motor', 'Vaixell i motor'), ('llave', 'Clau en mà: vaixell, motor, remolc i matriculació')],
  f_color='Color', f_any='M\'és igual / no ho sé', f_name='Nom', f_tel='Telèfon', f_email='Correu electrònic', f_zone='Zona o port', f_zone_ph='Costa Brava, Barcelona, Tarragona…',
  f_msg='Explica-m\'ho', f_msg_ph='Ús, nombre de persones, motor, si tens remolc…', f_opt='(opcional)',
  f_priv='Responsable: Juan Morante (Plata Marine). Faré servir aquestes dades només per contestar-te i preparar el teu pressupost. Pots exercir els teus drets a juan@platamarine.com. <a href="/privacidad.html">Política de privacitat</a>.',
  f_consent='He llegit la informació de privacitat i accepto que facis servir aquestes dades per contestar-me.', f_send='Demanar pressupost', f_req='Els camps amb * són obligatoris.',
  faq_h='Preguntes freqüents',
  faq=[('faq-titulo', 'Necessito titulació?',
        'Des de l\'1 d\'octubre de 2026, sense títol només es pot portar, per a ús privat, un vaixell de fins a 5 m amb un motor de fins a 15 CV (sense limitador de potència), de dia, sense allunyar-se més de 2 milles de la sortida i sent major de 18 anys. El 12, el 13 S i el 14 fan menys de 5 m: amb un motor de 15 CV no necessites títol, però amb el motor que recomana la marca (de 25 a 60 CV) necessites la Llicència de Navegació o superior. El 17 fa 5,17 m, així que sempre necessita Llicència de Navegació o superior. <a href="{p}/titulaciones/">Veure titulacions</a>.'),
       (None, 'Quant pesa amb remolc? Em serveix el carnet B?',
        'El buc pesa 200 kg (12), 250 kg (13 S), 260 kg (14) i 380 kg (17), sense motor. A això suma-hi el motor, el dipòsit i el remolc mateix. Amb el carnet B pots portar un remolc de fins a 750 kg de massa màxima autoritzada, o un de més pesat si el cotxe i el remolc junts no passen de 3.500 kg. Et dic quin remolc encaixa amb el teu vaixell i el teu cotxe.'),
       (None, 'Quin motor li poso?',
        'La marca recomana 25–30 CV per al 12, 40 CV per al 13 S, 30–40 CV per al 14 i 60 CV per al 17, tots amb eix llarg. Mai per sobre de la potència màxima de la placa CE (30, 60, 40 i 80 CV). Si el vols portar sense títol, el límit és 15 CV.'),
       (None, 'Quant triga l\'entrega?',
        'Es fabriquen per encàrrec. El termini depèn de la fàbrica i de l\'època de l\'any: te\'l confirmo per escrit al pressupost, abans de demanar res.'),
       (None, 'El transport des de fàbrica està inclòs?',
        'No. Arriben en camió des de fàbrica i el transport va a part. Orientatiu: uns 2.090 € un enviament compartit (per exemple, un 17 i un 13 S) i uns 4.390 € un camió complet. L\'import real va al teu pressupost.'),
       (None, 'Quina garantia té?',
        'SeaStorm dona 20 anys de garantia al buc davant de defectes de materials i fabricació, al primer comprador que el compra a la marca o a un dealer autoritzat i amb un ús normal. Els recanvis tenen 2 anys. El motor, el remolc i els accessoris tenen la garantia del seu fabricant. No cobreix, per exemple, posar més potència o més càrrega de la que marca la placa CE, accidents o competició.'),
       (None, 'Paguen impost de matriculació?',
        'No. L\'impost especial de matriculació (IEDMT) només s\'aplica a embarcacions d\'esbarjo de més de 8 m d\'eslora. Sí que hi ha taxes de matriculació, que van al pressupost.'),
       (None, 'El preu inclou IVA i motor?',
        'No. Els preus són sense IVA, de la versió Advantage i sense motor. Al costat del preu també veus l\'import amb l\'IVA general del 21 %.')],
  about_h='Qui hi ha darrere',
  about_ss='SeaStorm fabrica vaixells de polietilè d\'una sola peça i els ven en més de 60 països.',
  about_me_h='Juan Morante',
  about_me='Fa 12 anys que treballo de cara al públic, ajudant cada client a trobar el que necessita. Soc el dealer de SeaStorm a Catalunya: t\'acompanyo des del primer dubte fins a l\'entrega.',
  end_h='Ho mirem?', end_p='Escriu-me i ho parlem amb calma. Sense compromís.',
  used='Busques un vaixell d\'ocasió? <a href="{p}/barcos/#segunda-mano">Veure vaixells de segona mà →</a>',
  float='Demanar pressupost',
  small='Preus orientatius, sense IVA, segons el PVP recomanat de la tarifa 2027 de SeaStorm, versió Advantage, a fàbrica: no inclouen motor, equipament opcional, remolc, transport ni matriculació. L\'import amb IVA es calcula al 21 % com a referència. Transport i terminis orientatius: depenen de la càrrega i de la fàbrica. Dades tècniques, colors i garantia segons la web del fabricant (octubre de 2026). La titulació és orientativa, segons el Reial decret 875/2014 en la redacció vigent des de l\'1 d\'octubre de 2026: confirma-la amb la teva escola o amb Capitania. Poden canviar i no són vinculants; el preu final és el del pressupost per escrit. Ens podem equivocar; si hi veus un error, avisa\'ns.',
 ),
 'en': dict(
  title='SeaStorm in Catalonia: polyethylene boats from €4,990 · Plata Marine',
  desc='SeaStorm 12, 13 S, 14 and 17 polyethylene (HDPE) boats, 3.66 to 5.17 m, with a 20-year hull warranty. From €4,990 +VAT. Dealer in Catalonia: turnkey quotes.',
  crumbs=('Home', 'New boats'),
  eyebrow='SeaStorm dealer in Catalonia',
  h1='Polyethylene boats with a 20-year hull warranty',
  lead='Four models from 3.66 to 5.17 m, built in one piece. Light, made to take knocks, scrapes and sun, with no gelcoat to polish. I help you choose model and engine, and prepare a quote with everything included.',
  hfrom='From', hnote='Advantage version, without engine',
  cta='Request a quote', cta_wa='Talk to Juan',
  wa_gen='Hi Juan, I am interested in a SeaStorm. Can you help me choose a model?',
  wa_m='Hi Juan, I am interested in the {m}. Could you prepare a quote?',
  wa_key='Hi Juan, I would like a turnkey SeaStorm (boat, engine, trailer and registration). Could you prepare a quote?',
  stats=[('20 years', 'hull warranty'), ('1 piece', 'rotomoulded polyethylene hull'), ('18–22 cm', 'draught'), ('200–380 kg', 'hull weight')],
  nav=[('modelos', 'Models'), ('comparar', 'Compare'), ('llave-en-mano', 'Turnkey'), ('colores', 'Colours'), ('video', 'Video'), ('faq', 'FAQ'), ('presupuesto', 'Quote')],
  choose_k='Which one is yours', choose_h='Four sizes, the same tough hull',
  choose_p='Tap a model to see its specs, photos and price.',
  see='See details →',
  tag={'12': 'First boat or tender', '13-s': 'The sporty one', '14': 'All-rounder', '17': 'Family and fishing'},
  d={'12': 'The smallest and lightest: a 200 kg hull. A first boat for coastal trips, or a tender that runs well on a small engine.',
     '13-s': 'Twin-step hull designed by Mannerfeldt Design: planes with small engines and takes up to 60 hp. Storage under the bow and rear seats.',
     '14': 'Classic lines, console with steering wheel and lockers fore and aft. With an 18 cm draught it gets close to the beach.',
     '17': 'The largest in the range: up to 8 people in category D, 610 kg payload and engines up to 80 hp. For family days, fishing or diving.'},
  lab=dict(loa='Length', beam='Beam', w='Hull weight', dr='Draught', cap='Max. load', pax='People', hp='Max. power', rec='Recommended engine', lic='Licence (Spain)'),
  pax_v='{c} (cat. C) · {d} (cat. D)', hp_v='{h} hp ({k} kW)', rec_v='{r} hp, long shaft',
  lic_long='Licencia de Navegación or higher', lic_short='Licencia de Navegación or higher',
  lic_note='No licence only with an engine up to 15 hp (private use, daytime, within 2 miles). <a href="{p}/seastorm/#faq-titulo">More</a>',
  from_='From', vinc='{v} inc. VAT', adv='Advantage, without engine',
  ask_m='Request a quote', nophoto='Photos of the 13 S coming soon',
  cmp_k='Compare', cmp_h='All four, side by side', cmp_model='Model', cmp_from='From (+VAT)',
  adv_k='Advantage version', adv_h='What the price includes',
  adv_p='Prices are for the Advantage version, the one in the factory price list. It comes with:',
  adv_list=['Console with steering wheel', 'Windscreen', 'Cushions with backrests', 'Side rails', 'Motor plate'],
  adv_note='Engine, trailer, transport and registration are extra. If you like, I quote them together.',
  key_k='Turnkey', key_h='Boat, engine, trailer and paperwork in one quote',
  key_p='If you prefer, I get it ready to launch. I prepare a closed, written quote with:',
  key_list=['The SeaStorm you choose, Advantage version', 'The recommended engine for that model', 'A trailer suited to its weight and your car', 'Transport from the factory', 'Registration and paperwork'],
  key_cta='Ask me for a turnkey quote', key_note='The price depends on the engine and trailer you choose: you get it closed before anything is ordered.',
  tech_k='HDPE polyethylene', tech_h='Why a polyethylene hull', tech_p='How they are built, according to the manufacturer.',
  tech=[('One piece', 'Rotomoulded: the hull comes out of the mould in one piece, with no joints or bonding.'),
        ('Made for knocks and sun', 'UV-stabilised polyethylene, resistant to impacts, scrapes, temperature changes and strong sunlight.'),
        ('Low maintenance', 'No gelcoat to polish or repaint.'),
        ('Double, self-draining hull', 'Double hull, self-draining, with a shallow draught (18 to 22 cm) to get close to the beach.'),
        ('Recyclable materials', 'SeaStorm uses recyclable materials in its current models.'),
        ('20-year hull warranty', 'For the original buyer, against defects in materials and workmanship, under SeaStorm\'s terms.')],
  tech_note='Manufacturer\'s information.',
  col_k='Colours', col_h='Seven hull colours', col_p='Colours available on all four models, according to the manufacturer\'s website. On screen, shades are approximate.',
  col={'white': 'White', 'lgrey': 'Light grey', 'dgrey': 'Dark grey', 'green': 'Green', 'lime': 'Lime green', 'red': 'Red', 'yellow': 'Yellow'},
  vid_k='Video', vid_h='SeaStorm on video', vid_p='Official SeaStorm video. It only loads from YouTube when you press play.', vid_play='Play the SeaStorm video',
  how_h='How to buy a SeaStorm',
  steps=[('We talk', 'You tell me how you will use it and we choose model, engine and colour.'),
         ('Written quote', 'With everything you want included: boat, engine, trailer, transport and paperwork.'),
         ('Factory order', 'Built to order. I confirm the lead time in writing.'),
         ('Delivery', 'I coordinate transport and registration until it is ready.')],
  form_h='Request your quote', form_p='Tell me which model you like and how you will use it. I reply with a written quote, no commitment.',
  f_alt='Prefer to message me directly? I also reply on WhatsApp.',
  f_model='Model', f_dunno='Not sure yet', f_need='What do you need?', f_needs=[('barco', 'Just the boat'), ('motor', 'Boat and engine'), ('llave', 'Turnkey: boat, engine, trailer and registration')],
  f_color='Colour', f_any='Any / not sure', f_name='Name', f_tel='Phone', f_email='Email', f_zone='Area or port', f_zone_ph='Costa Brava, Barcelona, Tarragona…',
  f_msg='Tell me more', f_msg_ph='Use, number of people, engine, whether you have a trailer…', f_opt='(optional)',
  f_priv='Controller: Juan Morante (Plata Marine). I will only use these details to reply and prepare your quote. You can exercise your rights at juan@platamarine.com. <a href="/privacidad.html">Privacy policy</a>.',
  f_consent='I have read the privacy information and agree to you using these details to reply to me.', f_send='Request a quote', f_req='Fields marked * are required.',
  faq_h='Frequently asked questions',
  faq=[('faq-titulo', 'Do I need a licence?',
        'Under Spanish rules, since 1 October 2026 you can only skipper without a licence, for private use, a boat up to 5 m with an engine up to 15 hp (no power limiter), in daylight, within 2 miles of where you set off and if you are over 18. The 12, 13 S and 14 are under 5 m: with a 15 hp engine you need no licence, but with the engine the brand recommends (25 to 60 hp) you need the Licencia de Navegación or higher. The 17 is 5.17 m long, so it always needs the Licencia de Navegación or higher. <a href="{p}/titulaciones/">See licences</a>.'),
       (None, 'How much does it weigh on a trailer? Is a car licence enough?',
        'The hull weighs 200 kg (12), 250 kg (13 S), 260 kg (14) and 380 kg (17), without engine. Add the engine, the fuel tank and the trailer itself. With a Spanish B licence you can tow a trailer of up to 750 kg gross weight, or a heavier one if car and trailer together do not exceed 3,500 kg. I tell you which trailer suits your boat and your car.'),
       (None, 'Which engine should I fit?',
        'The brand recommends 25–30 hp for the 12, 40 hp for the 13 S, 30–40 hp for the 14 and 60 hp for the 17, all long shaft. Never above the maximum power on the CE plate (30, 60, 40 and 80 hp). To use it without a licence, the limit is 15 hp.'),
       (None, 'How long is delivery?',
        'They are built to order. The lead time depends on the factory and the time of year: I confirm it in writing in the quote, before anything is ordered.'),
       (None, 'Is transport from the factory included?',
        'No. They come by truck from the factory and transport is extra. As a guide: about €2,090 for a shared load (e.g. a 17 and a 13 S) and about €4,390 for a full truck. The actual amount is in your quote.'),
       (None, 'What warranty does it have?',
        'SeaStorm gives a 20-year hull warranty against defects in materials and workmanship, to the original buyer who purchases from the brand or an authorised dealer, under normal use. Spare parts have 2 years. The engine, trailer and accessories carry their own manufacturer\'s warranty. It does not cover, for example, more power or load than the CE plate allows, accidents or racing.'),
       (None, 'Is there a registration tax?',
        'No. The Spanish special registration tax (IEDMT) only applies to recreational boats over 8 m long. There are registration fees, which are included in the quote.'),
       (None, 'Does the price include VAT and engine?',
        'No. Prices exclude VAT and are for the Advantage version without engine. Next to each price you also see the amount with Spain\'s standard 21% VAT.')],
  about_h='Who is behind it',
  about_ss='SeaStorm builds one-piece polyethylene boats and sells them in more than 60 countries.',
  about_me_h='Juan Morante',
  about_me='I have spent 12 years working with customers, helping each one find what they need. I am the SeaStorm dealer in Catalonia: I am with you from the first question to delivery.',
  end_h='Shall we look at it?', end_p='Message me and we will go through it calmly. No commitment.',
  used='Looking for a used boat? <a href="{p}/barcos/#segunda-mano">See used boats →</a>',
  float='Request a quote',
  small='Indicative prices, excluding VAT, based on the recommended retail price in SeaStorm\'s 2027 price list, Advantage version, ex-works: they do not include engine, optional equipment, trailer, transport or registration. The VAT-inclusive amount uses 21% as a reference. Transport and lead times are indicative and depend on the load and the factory. Technical data, colours and warranty from the manufacturer\'s website (October 2026). The licence shown is indicative, based on Spanish Royal Decree 875/2014 as worded since 1 October 2026: please confirm it with your school or the Harbour Master. They may change and are not binding; the final price is the one in the written quote. We may be wrong; if you spot an error, let us know.',
 ),
 'fr': dict(
  title='SeaStorm en Catalogne : bateaux en polyéthylène dès 4 990 € · Plata Marine',
  desc='Bateaux SeaStorm 12, 13 S, 14 et 17 en polyéthylène (HDPE), de 3,66 à 5,17 m, coque garantie 20 ans. À partir de 4 990 € HT. Concessionnaire en Catalogne : devis clé en main.',
  crumbs=('Accueil', 'Bateaux neufs'),
  eyebrow='Concessionnaire SeaStorm en Catalogne',
  h1='Bateaux en polyéthylène, coque garantie 20 ans',
  lead='Quatre modèles de 3,66 à 5,17 m, fabriqués d\'une seule pièce. Légers, conçus pour les chocs, les frottements et le soleil, sans gelcoat à polir. Je vous aide à choisir le modèle et le moteur, et je vous prépare un devis complet.',
  hfrom='À partir de', hnote='version Advantage, sans moteur',
  cta='Demander un devis', cta_wa='Parler à Juan',
  wa_gen='Bonjour Juan, un SeaStorm m\'intéresse. Pouvez-vous m\'aider à choisir le modèle ?',
  wa_m='Bonjour Juan, le {m} m\'intéresse. Pouvez-vous me préparer un devis ?',
  wa_key='Bonjour Juan, je souhaite un SeaStorm clé en main (bateau, moteur, remorque et immatriculation). Pouvez-vous me préparer un devis ?',
  stats=[('20 ans', 'de garantie coque'), ('1 pièce', 'coque en polyéthylène rotomoulé'), ('18–22 cm', 'de tirant d\'eau'), ('200–380 kg', 'poids de la coque')],
  nav=[('modelos', 'Modèles'), ('comparar', 'Comparer'), ('llave-en-mano', 'Clé en main'), ('colores', 'Couleurs'), ('video', 'Vidéo'), ('faq', 'Questions'), ('presupuesto', 'Devis')],
  choose_k='Lequel est le vôtre', choose_h='Quatre tailles, la même coque robuste',
  choose_p='Touchez un modèle pour voir sa fiche, ses photos et son prix.',
  see='Voir la fiche →',
  tag={'12': 'Premier bateau ou annexe', '13-s': 'Le sportif', '14': 'Polyvalent', '17': 'Famille et pêche'},
  d={'12': 'Le plus petit et le plus léger : 200 kg de coque. Un premier bateau pour les sorties côtières, ou une annexe qui avance bien avec un petit moteur.',
     '13-s': 'Coque à deux redans dessinée par Mannerfeldt Design : elle déjauge avec de petits moteurs et accepte jusqu\'à 60 ch. Rangements sous les sièges avant et arrière.',
     '14': 'Lignes classiques, console avec volant et coffres à l\'avant et à l\'arrière. Avec 18 cm de tirant d\'eau, il s\'approche bien de la plage.',
     '17': 'Le plus grand de la gamme : jusqu\'à 8 personnes en catégorie D, 610 kg de charge et moteur jusqu\'à 80 ch. Pour les sorties en famille, la pêche ou la plongée.'},
  lab=dict(loa='Longueur', beam='Largeur', w='Poids de la coque', dr='Tirant d\'eau', cap='Charge max.', pax='Personnes', hp='Puissance max.', rec='Moteur conseillé', lic='Permis (Espagne)'),
  pax_v='{c} (cat. C) · {d} (cat. D)', hp_v='{h} ch ({k} kW)', rec_v='{r} ch, arbre long',
  lic_long='Licencia de Navegación ou supérieur', lic_short='Licencia de Navegación ou supérieur',
  lic_note='Sans permis, seulement avec un moteur jusqu\'à 15 ch (usage privé, de jour et à 2 milles maximum). <a href="{p}/seastorm/#faq-titulo">En savoir plus</a>',
  from_='À partir de', vinc='{v} TTC', adv='Advantage, sans moteur',
  ask_m='Demander un devis', nophoto='Photos du 13 S bientôt disponibles',
  cmp_k='Comparer', cmp_h='Les quatre, côte à côte', cmp_model='Modèle', cmp_from='À partir de (HT)',
  adv_k='Version Advantage', adv_h='Ce que comprend le prix',
  adv_p='Les prix sont ceux de la version Advantage, celle du tarif usine. Elle comprend :',
  adv_list=['Console avec volant', 'Pare-brise', 'Coussins avec dossiers', 'Mains courantes latérales', 'Plaque moteur'],
  adv_note='Le moteur, la remorque, le transport et l\'immatriculation sont en supplément. Si vous le souhaitez, je vous les chiffre ensemble.',
  key_k='Clé en main', key_h='Bateau, moteur, remorque et papiers dans un seul devis',
  key_p='Si vous préférez, je vous le livre prêt à mettre à l\'eau. Je vous prépare un devis ferme et écrit avec :',
  key_list=['Le SeaStorm de votre choix, version Advantage', 'Le moteur conseillé pour ce modèle', 'Une remorque adaptée à son poids et à votre voiture', 'Le transport depuis l\'usine', 'L\'immatriculation et les papiers'],
  key_cta='Demandez-moi un devis clé en main', key_note='Le prix dépend du moteur et de la remorque choisis : vous l\'avez ferme avant toute commande.',
  tech_k='Polyéthylène HDPE', tech_h='Pourquoi une coque en polyéthylène', tech_p='Comment ils sont fabriqués, selon le constructeur.',
  tech=[('Une seule pièce', 'Rotomoulage : la coque sort du moule d\'une seule pièce, sans joints ni collages.'),
        ('Conçu pour les chocs et le soleil', 'Polyéthylène stabilisé aux UV, résistant aux chocs, aux frottements, aux écarts de température et au soleil intense.'),
        ('Peu d\'entretien', 'Pas de gelcoat à polir ni à repeindre.'),
        ('Double coque autovideuse', 'Double coque, autovideuse, à faible tirant d\'eau (de 18 à 22 cm) pour s\'approcher de la plage.'),
        ('Matériaux recyclables', 'SeaStorm utilise des matériaux recyclables pour ses modèles actuels.'),
        ('Coque garantie 20 ans', 'Pour le premier acheteur, contre les défauts de matériaux et de fabrication, selon les conditions de SeaStorm.')],
  tech_note='Informations du constructeur.',
  col_k='Couleurs', col_h='Sept couleurs de coque', col_p='Couleurs disponibles sur les quatre modèles, selon le site du constructeur. À l\'écran, les teintes sont indicatives.',
  col={'white': 'Blanc', 'lgrey': 'Gris clair', 'dgrey': 'Gris foncé', 'green': 'Vert', 'lime': 'Vert citron', 'red': 'Rouge', 'yellow': 'Jaune'},
  vid_k='Vidéo', vid_h='SeaStorm en vidéo', vid_p='Vidéo officielle de SeaStorm. Elle ne se charge depuis YouTube que lorsque vous appuyez sur lecture.', vid_play='Lire la vidéo SeaStorm',
  how_h='Comment acheter un SeaStorm',
  steps=[('On en parle', 'Vous me dites comment vous l\'utiliserez et nous choisissons modèle, moteur et couleur.'),
         ('Devis écrit', 'Avec tout ce que vous voulez inclure : bateau, moteur, remorque, transport et papiers.'),
         ('Commande à l\'usine', 'Fabriqué sur commande. Je vous confirme le délai par écrit.'),
         ('Livraison', 'Je coordonne le transport et l\'immatriculation jusqu\'à ce qu\'il soit prêt.')],
  form_h='Demandez votre devis', form_p='Dites-moi quel modèle vous intéresse et comment vous l\'utiliserez. Je vous réponds avec un devis écrit, sans engagement.',
  f_alt='Vous préférez m\'écrire directement ? Je réponds aussi sur WhatsApp.',
  f_model='Modèle', f_dunno='Je ne sais pas encore', f_need='De quoi avez-vous besoin ?', f_needs=[('barco', 'Le bateau seul'), ('motor', 'Bateau et moteur'), ('llave', 'Clé en main : bateau, moteur, remorque et immatriculation')],
  f_color='Couleur', f_any='Peu importe / je ne sais pas', f_name='Nom', f_tel='Téléphone', f_email='E-mail', f_zone='Zone ou port', f_zone_ph='Costa Brava, Barcelone, Tarragone…',
  f_msg='Dites-m\'en plus', f_msg_ph='Usage, nombre de personnes, moteur, si vous avez une remorque…', f_opt='(facultatif)',
  f_priv='Responsable : Juan Morante (Plata Marine). J\'utiliserai ces données uniquement pour vous répondre et préparer votre devis. Vous pouvez exercer vos droits à juan@platamarine.com. <a href="/privacidad.html">Politique de confidentialité</a>.',
  f_consent='J\'ai lu les informations sur la confidentialité et j\'accepte que vous utilisiez ces données pour me répondre.', f_send='Demander un devis', f_req='Les champs marqués * sont obligatoires.',
  faq_h='Questions fréquentes',
  faq=[('faq-titulo', 'Faut-il un permis ?',
        'Selon les règles espagnoles, depuis le 1er octobre 2026, on ne peut piloter sans permis, pour un usage privé, qu\'un bateau de 5 m maximum avec un moteur de 15 ch maximum (sans bridage), de jour, à 2 milles maximum du point de départ et à partir de 18 ans. Les 12, 13 S et 14 mesurent moins de 5 m : avec un moteur de 15 ch, pas besoin de permis, mais avec le moteur conseillé par la marque (de 25 à 60 ch) il faut la Licencia de Navegación ou supérieur. Le 17 mesure 5,17 m : il faut toujours la Licencia de Navegación ou supérieur. <a href="{p}/titulaciones/">Voir les permis</a>.'),
       (None, 'Combien pèse-t-il sur remorque ? Le permis B suffit-il ?',
        'La coque pèse 200 kg (12), 250 kg (13 S), 260 kg (14) et 380 kg (17), sans moteur. Il faut y ajouter le moteur, le réservoir et la remorque elle-même. Avec le permis B espagnol, vous pouvez tracter une remorque jusqu\'à 750 kg de PTAC, ou plus lourde si la voiture et la remorque ensemble ne dépassent pas 3 500 kg. Je vous indique la remorque adaptée à votre bateau et à votre voiture.'),
       (None, 'Quel moteur choisir ?',
        'La marque conseille 25–30 ch pour le 12, 40 ch pour le 13 S, 30–40 ch pour le 14 et 60 ch pour le 17, tous en arbre long. Jamais au-dessus de la puissance maximale de la plaque CE (30, 60, 40 et 80 ch). Pour le piloter sans permis, la limite est de 15 ch.'),
       (None, 'Quel est le délai de livraison ?',
        'Ils sont fabriqués sur commande. Le délai dépend de l\'usine et de la saison : je vous le confirme par écrit dans le devis, avant toute commande.'),
       (None, 'Le transport depuis l\'usine est-il inclus ?',
        'Non. Ils arrivent en camion depuis l\'usine et le transport est en supplément. À titre indicatif : environ 2 090 € pour un envoi partagé (par exemple un 17 et un 13 S) et environ 4 390 € pour un camion complet. Le montant réel figure dans votre devis.'),
       (None, 'Quelle garantie ?',
        'SeaStorm garantit la coque 20 ans contre les défauts de matériaux et de fabrication, pour le premier acheteur qui l\'achète à la marque ou à un concessionnaire agréé, en usage normal. Les pièces détachées sont garanties 2 ans. Le moteur, la remorque et les accessoires ont la garantie de leur propre fabricant. Elle ne couvre pas, par exemple, une puissance ou une charge supérieure à la plaque CE, les accidents ou la compétition.'),
       (None, 'Y a-t-il une taxe d\'immatriculation ?',
        'Non. La taxe spéciale espagnole d\'immatriculation (IEDMT) ne s\'applique qu\'aux bateaux de plaisance de plus de 8 m. Il y a des frais d\'immatriculation, inclus dans le devis.'),
       (None, 'Le prix comprend-il la TVA et le moteur ?',
        'Non. Les prix sont HT, pour la version Advantage sans moteur. À côté de chaque prix, vous voyez aussi le montant TTC avec la TVA espagnole de 21 %.')],
  about_h='Qui est derrière',
  about_ss='SeaStorm fabrique des bateaux en polyéthylène d\'une seule pièce et les vend dans plus de 60 pays.',
  about_me_h='Juan Morante',
  about_me='Je travaille depuis 12 ans au contact des clients, en aidant chacun à trouver ce dont il a besoin. Je suis le concessionnaire SeaStorm en Catalogne : je vous accompagne de la première question jusqu\'à la livraison.',
  end_h='On en parle ?', end_p='Écrivez-moi et nous en parlerons tranquillement. Sans engagement.',
  used='Vous cherchez un bateau d\'occasion ? <a href="{p}/barcos/#segunda-mano">Voir les bateaux d\'occasion →</a>',
  float='Demander un devis',
  small='Prix indicatifs, hors TVA, selon le prix de vente conseillé du tarif 2027 de SeaStorm, version Advantage, départ usine : ils n\'incluent pas le moteur, les options, la remorque, le transport ni l\'immatriculation. Le montant TTC est calculé à 21 % à titre indicatif. Transport et délais indicatifs : ils dépendent du chargement et de l\'usine. Caractéristiques, couleurs et garantie selon le site du constructeur (octobre 2026). Le permis indiqué est indicatif, selon le décret royal espagnol 875/2014 dans sa rédaction en vigueur depuis le 1er octobre 2026 : vérifiez-le auprès de votre école ou de la Capitainerie. Ils peuvent changer et ne sont pas contractuels ; le prix final est celui du devis écrit. Nous pouvons nous tromper ; si vous voyez une erreur, dites-le-nous. Nous ne parlons pas français : nous utilisons un traducteur, merci de votre indulgence.',
 ),
}
VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': 'HT'}

WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z"/></svg>'

CSS = r"""
.ss{--ink:#0E3042;--sea:#0B766B;--sea2:#2BB3A3;--night:#06080b;--line:rgba(14,48,66,.12);--soft:#F3F6F7;background:#fff;color:var(--ink);overflow-x:clip}
.ss *{box-sizing:border-box}
.ss h1,.ss h2,.ss h3{font-family:var(--display);letter-spacing:-.01em;font-stretch:normal}
.ss .wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.ss-hero{position:relative;min-height:min(86vh,780px);display:flex;align-items:flex-end;color:#fff;background:var(--night);overflow:hidden}
.ss-hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:55% 55%}
.ss-hero:after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(6,8,11,.9) 0,rgba(6,8,11,.45) 45%,rgba(6,8,11,.08) 78%),linear-gradient(90deg,rgba(6,8,11,.5),transparent 62%)}
.ss-hero .wrap{position:relative;z-index:1;width:100%;padding-bottom:64px}
.ss-crumb{font-size:13.5px;margin:0 0 18px;color:rgba(255,255,255,.75);display:flex;flex-wrap:wrap;gap:6px}
.ss-crumb a{color:#fff;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.35)}
.ss-logo{width:min(360px,72vw);height:auto;display:block;margin:0 0 20px}
.ss-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;margin:0 0 16px;padding:7px 12px;border:1px solid rgba(255,255,255,.3);border-radius:999px;backdrop-filter:blur(6px)}
.ss-eyebrow:before{content:"";width:7px;height:7px;border-radius:50%;background:var(--sea2)}
.ss-hero h1{color:#fff!important;font-size:clamp(32px,5vw,58px);line-height:1.04;font-weight:800;margin:0 0 14px;max-width:820px}
.ss-hero .lead{font-size:clamp(16.5px,2vw,19px);line-height:1.55;max-width:620px;margin:0 0 20px;color:rgba(255,255,255,.88)}
.ss-hprice{font-family:var(--display);font-size:clamp(22px,2.6vw,30px);font-weight:800;margin:0 0 26px;color:#fff}
.ss-hprice small{font-weight:600;font-size:15px;opacity:.75}
.ss-hprice .vat{font-size:.62em}
.ss-hprice .hn{display:block;font-size:14px;font-weight:500;opacity:.72;margin-top:4px;font-family:inherit}
.ss-btns{display:flex;gap:12px;flex-wrap:wrap}
.ss-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;font-weight:700;border-radius:999px;padding:14px 24px;text-decoration:none;font-size:16px;line-height:1.2;transition:transform .15s,background .15s;border:0;cursor:pointer;font-family:inherit;text-align:center}
.ss-btn:hover{transform:translateY(-1px)}
.ss-btn.pri{background:var(--sea);color:#fff}.ss-btn.pri:hover{background:#085C53}
.ss-btn.ghost{border:1px solid rgba(255,255,255,.55);color:#fff;background:transparent}.ss-btn.ghost:hover{background:rgba(255,255,255,.1)}
.ss-btn.line{border:1px solid rgba(14,48,66,.3);color:var(--ink);background:#fff}.ss-btn.line:hover{background:var(--soft)}
.ss-btn svg{width:19px;height:19px;fill:currentColor;flex:none}
.vat{color:#C62828;font-weight:800;font-size:.8em;margin-left:6px;white-space:nowrap}
.vatinc{display:block;font-size:13px;font-weight:500;color:#5B6B75;font-family:inherit;margin-top:3px;white-space:nowrap}
.ss-stats{background:var(--night);color:#fff;border-top:1px solid rgba(255,255,255,.08)}
.ss-stats .wrap{display:grid;grid-template-columns:repeat(4,1fr)}
.ss-stats div{padding:24px 10px;border-right:1px solid rgba(255,255,255,.08)}.ss-stats div:last-child{border-right:0}
.ss-stats b{display:block;font-family:var(--display);font-size:clamp(24px,3.2vw,36px);font-weight:800;line-height:1.05}
.ss-stats span{font-size:13.5px;opacity:.68}
.ss-subnav{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.ss-subnav .wrap{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none}
.ss-subnav .wrap::-webkit-scrollbar{display:none}
.ss-subnav a{white-space:nowrap;padding:14px 11px;font-size:14px;font-weight:700;color:var(--ink);text-decoration:none;opacity:.7;border-bottom:2px solid transparent}
.ss-subnav a:hover,.ss-subnav a.on{opacity:1;border-bottom-color:var(--sea)}
.ss-sec{padding:64px 0;scroll-margin-top:56px}
.ss-alt{background:var(--soft)}
.ss-kick{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--sea);font-weight:700;margin:0 0 10px}
.ss-sec h2{font-size:clamp(26px,3.2vw,38px);line-height:1.1;margin:0 0 10px;color:var(--ink);font-weight:800}
.ss-sub{font-size:16px;line-height:1.55;opacity:.78;margin:0 0 26px;max-width:660px}
.ss-choose{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.ss-card{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:18px;overflow:hidden;text-decoration:none;color:inherit;background:#fff;transition:transform .2s,box-shadow .2s;min-width:0}
.ss-card:hover{transform:translateY(-3px);box-shadow:0 24px 40px -28px rgba(14,48,66,.5)}
.ss-card>img,.ss-card>.ph0{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block;background:var(--night)}
.ss-card>div{padding:16px 16px 18px;display:flex;flex-direction:column;gap:5px;flex:1}
.ss-card .tg{font-size:12px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:var(--sea)}
.ss-card h3{margin:0;font-size:21px;color:var(--ink)}
.ss-card p{margin:0;font-size:14px;line-height:1.45;opacity:.75;flex:1}
.ss-card .pr{font-family:var(--display);font-weight:800;font-size:17px;margin-top:6px}
.ss-card .go{font-size:14px;font-weight:700;color:var(--sea)}
.ph0{display:flex!important;flex-direction:column;align-items:center;justify-content:center;gap:10px;color:#fff;background:radial-gradient(120% 90% at 30% 20%,#123a50 0,#06080b 70%)!important;padding:18px;text-align:center}
.ph0 img{width:70%!important;max-width:260px;height:auto!important;aspect-ratio:auto!important;background:none!important;object-fit:contain!important}
.ph0 b{font-family:var(--display);font-size:clamp(30px,4vw,46px);font-weight:800;line-height:1;letter-spacing:.02em}
.ph0 span{font-size:13px;opacity:.7}
.ss-model{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);border:1px solid var(--line);border-radius:22px;overflow:hidden;background:#fff;margin:0 0 22px;scroll-margin-top:64px;box-shadow:0 30px 60px -44px rgba(14,48,66,.45)}
.ss-media{padding:16px;min-width:0}
.ss-media>.main{display:block;width:100%;height:auto!important;aspect-ratio:4/3;object-fit:cover;border-radius:14px;background:var(--soft)}
.ss-media>.ph0{border-radius:14px;aspect-ratio:4/3;width:100%}
.ss-thumbs{display:flex;gap:8px;margin-top:10px;overflow-x:auto;padding-bottom:4px}
.ss-thumbs button{flex:none;width:84px;height:63px;border-radius:9px;border:2px solid transparent;opacity:.72;padding:0;overflow:hidden;cursor:pointer;background:#000}
.ss-thumbs button[aria-pressed=true]{border-color:var(--sea);opacity:1}
.ss-thumbs img{width:100%;height:100%;object-fit:cover;display:block}
.ss-info{padding:24px 26px 24px 10px;display:flex;flex-direction:column;gap:12px;min-width:0}
.ss-info .tg{font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--sea);margin:0}
.ss-info h3{margin:0;font-size:30px;color:var(--ink)}
.ss-info p.d{margin:0;font-size:15.5px;line-height:1.55;opacity:.8}
.ss-spec{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--line);border-radius:12px;margin:0;overflow:hidden}
.ss-spec div{padding:9px 11px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);min-width:0}
.ss-spec div:nth-child(3n){border-right:0}
.ss-spec div.w2{grid-column:span 3;border-right:0}
.ss-spec dt{font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;opacity:.58;margin:0 0 2px;line-height:1.3}
.ss-spec dd{margin:0;font-weight:700;color:var(--ink);font-size:14px;line-height:1.35}
.ss-spec div:last-child{border-bottom:0}
.ss-lic{font-size:13px;line-height:1.45;opacity:.72;margin:-4px 0 0}
.ss-lic a{color:var(--sea);font-weight:700}
.ss-buy{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:14px;margin-top:auto}
.ss-buy small{display:block;font-size:12.5px;opacity:.62;margin-bottom:2px}
.ss-buy strong{font-family:var(--display);font-size:30px;color:var(--ink);line-height:1}
.ss-buy .ss-btns{gap:8px}
.ss-buy .ss-btn{padding:12px 18px;font-size:15px}
.ss-buy .ss-btn.wa{background:#fff;color:var(--sea);border:1px solid rgba(11,118,107,.45)}
.ss-cmp.specs{display:block;padding:0;margin:0;border:0;background:none;border-radius:0}
.ss-cmp table{width:100%;border-collapse:collapse;font-size:14.5px;border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#fff}
.ss-cmp th,.ss-cmp td{padding:11px 14px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
.ss-cmp thead th{background:var(--ink);color:#fff;font-family:var(--display);font-size:13px;letter-spacing:.05em;text-transform:uppercase;font-weight:700}
.ss-cmp tbody th{font-family:var(--display);font-size:17px;color:var(--ink);white-space:nowrap}
.ss-cmp tbody th a{color:inherit;text-decoration:none}
.ss-cmp td.pr{font-family:var(--display);font-weight:800;white-space:nowrap}
.ss-cmp tr:last-child td,.ss-cmp tr:last-child th{border-bottom:0}
.ss-split{display:grid;grid-template-columns:1fr 1.1fr;gap:44px;align-items:center}
.ss-split>img{width:100%;height:auto!important;aspect-ratio:4/3;object-fit:cover;border-radius:18px;display:block;background:var(--night)}
.ss-chips{display:flex;flex-wrap:wrap;gap:9px;margin:0 0 18px;padding:0;list-style:none}
.ss-chips li{border:1px solid var(--line);border-radius:999px;padding:7px 13px;font-size:14px;font-weight:600;color:var(--ink);background:#F7FAFB}
.ss-chips li:before{content:"✓";color:var(--sea);margin-right:7px;font-weight:800}
.ss-note{font-size:13px;opacity:.6;margin:12px 0 0;line-height:1.5}
.ss-dark{background:var(--night);color:#fff}.ss-dark h2{color:#fff!important}.ss-dark .ss-sub{color:rgba(255,255,255,.78);opacity:1}.ss-dark .ss-kick{color:var(--sea2)}
.ss-key{display:grid;grid-template-columns:1.05fr 1fr;border-radius:22px;overflow:hidden;background:var(--ink);color:#fff;box-shadow:0 30px 60px -40px rgba(14,48,66,.6)}
.ss-key>img{width:100%;height:100%;min-height:320px;object-fit:cover;display:block;background:var(--night)}
.ss-key>div{padding:34px 34px;display:flex;flex-direction:column;justify-content:center}
.ss-key .ss-kick{color:var(--sea2)}
.ss-key h2{color:#fff!important;margin:0 0 12px}
.ss-key p{font-size:16px;line-height:1.55;margin:0 0 14px;color:rgba(255,255,255,.86)}
.ss-key ul{list-style:none;margin:0 0 22px;padding:0}
.ss-key li{padding:7px 0 7px 28px;position:relative;font-size:15.5px;border-top:1px solid rgba(255,255,255,.1)}
.ss-key li:before{content:"✓";position:absolute;left:2px;color:var(--sea2);font-weight:800}
.ss-key .ss-btn{align-self:flex-start}
.ss-key small{display:block;font-size:13px;opacity:.65;margin-top:12px;line-height:1.5}
.ss-tech{display:grid;grid-template-columns:1.1fr 1fr;gap:44px;align-items:center}
.ss-tech img{width:100%;height:auto!important;aspect-ratio:4/3;object-fit:cover;border-radius:16px;display:block}
.ss-tech ol{list-style:none;margin:0;padding:0;counter-reset:t}
.ss-tech li{counter-increment:t;padding:12px 0 12px 44px;position:relative;border-top:1px solid rgba(255,255,255,.12)}
.ss-tech li:before{content:"0" counter(t);position:absolute;left:0;top:12px;font-family:var(--display);font-weight:800;font-size:18px;color:var(--sea2)}
.ss-tech b{display:block;font-size:16px;margin-bottom:3px}.ss-tech span{color:rgba(255,255,255,.74);line-height:1.5;font-size:14.5px}
.ss-dark .ss-note{color:rgba(255,255,255,.6);opacity:1}
.ss-colors{display:grid;grid-template-columns:repeat(7,1fr);gap:12px;list-style:none;margin:0;padding:0}
.ss-colors li{display:flex;flex-direction:column;align-items:center;gap:8px;font-size:13.5px;font-weight:600;text-align:center}
.ss-colors i{display:block;width:100%;max-width:92px;aspect-ratio:1;border-radius:50%;border:1px solid rgba(14,48,66,.18);box-shadow:inset 0 -10px 18px rgba(0,0,0,.12)}
.ss-video{position:relative;aspect-ratio:16/9;border-radius:18px;overflow:hidden;background:#000;max-width:1000px}
.ss-video>button{position:absolute;inset:0;width:100%;height:100%;border:0;padding:0;margin:0;background:#000;cursor:pointer;display:block}
.ss-video>button img{width:100%;height:100%;object-fit:cover;display:block;opacity:.8;transition:opacity .2s}
.ss-video>button:hover img{opacity:.95}
.ss-video .play{position:absolute;left:50%;top:50%;width:84px;height:84px;margin:-42px 0 0 -42px;border-radius:50%;background:rgba(11,118,107,.94);display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,.4)}
.ss-video .play svg{width:34px;height:34px;fill:#fff;margin-left:5px}
.ss-video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.ss-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;counter-reset:s;list-style:none;margin:0;padding:0}
.ss-steps li{counter-increment:s;border-top:3px solid var(--ink);padding-top:18px}
.ss-steps li:before{content:"0" counter(s);font-family:var(--display);font-weight:800;font-size:24px;color:var(--sea);display:block;margin-bottom:6px}
.ss-steps b{display:block;font-size:16px;color:var(--ink);margin-bottom:4px}.ss-steps span{font-size:14.5px;opacity:.78;line-height:1.5}
.ss-form{display:grid;grid-template-columns:1fr 1fr;gap:14px 16px;margin:22px 0 8px;max-width:780px}
.ss-form .span2{grid-column:1/-1}
.ss-form label{display:block;font-weight:600;font-size:14px;margin-bottom:6px}
.ss-form label small{font-weight:400;opacity:.75}
.ss-form label i{color:#C62828;font-style:normal}
.ss-form input,.ss-form select,.ss-form textarea{width:100%;font:inherit;font-size:16px;padding:11px 12px;border:1px solid rgba(14,48,66,.25);border-radius:8px;background:#fff;color:var(--ink)}
.ss-form textarea{min-height:110px;resize:vertical}
.ss-form input:focus-visible,.ss-form select:focus-visible,.ss-form textarea:focus-visible{outline:2px solid var(--sea);outline-offset:1px}
.ss-form .help{font-size:13.5px;line-height:1.5;opacity:.85;margin:0}
.ss-form .help a{color:var(--sea)}
.ss-form .chk{display:flex;gap:10px;align-items:flex-start;font-weight:400;font-size:14.5px;line-height:1.45;margin:0;cursor:pointer}
.ss-form .chk input{width:20px;height:20px;min-width:20px;margin:1px 0 0;padding:0;accent-color:var(--sea)}
.ss-form button{font:inherit;font-weight:700;background:var(--sea);color:#fff;border:0;border-radius:999px;padding:14px 26px;cursor:pointer;font-size:16px}
.ss-form button:disabled{opacity:.6;cursor:default}
.ss-formbox{display:grid;grid-template-columns:1fr 1.5fr;gap:44px;align-items:start}
.ss-formbox .alt{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px}
.ss-formbox .alt p{margin:0 0 14px;font-size:15px;line-height:1.55}
.ss-faq details{border-bottom:1px solid var(--line);scroll-margin-top:64px}
.ss-faq summary{cursor:pointer;font-weight:700;font-size:16.5px;padding:18px 34px 18px 0;list-style:none;position:relative;color:var(--ink)}
.ss-faq summary::-webkit-details-marker{display:none}
.ss-faq summary:after{content:"+";position:absolute;right:4px;top:14px;font-size:24px;color:var(--sea)}
.ss-faq details[open] summary:after{content:"–"}
.ss-faq p{margin:0 0 18px;line-height:1.6;opacity:.86;max-width:800px}
.ss-faq p a{color:var(--sea);font-weight:700}
.ss-about{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.ss-about>div{border-radius:16px;padding:24px;background:var(--soft)}
.ss-about>div:first-child{background:var(--ink);color:#fff}
.ss-about img{width:200px;max-width:70%;height:auto;margin-bottom:16px;display:block}
.ss-about p{margin:0;font-size:15px;line-height:1.55}
.ss-about b{font-family:var(--display);display:block;font-size:20px;margin-bottom:14px;color:var(--ink)}
.ss-end{position:relative;color:#fff;text-align:center;overflow:hidden;background:var(--night)}
.ss-end>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.42}
.ss-end .wrap{position:relative}
.ss-end h2{color:#fff!important}.ss-end .ss-sub{color:rgba(255,255,255,.86);opacity:1;margin:0 auto 26px}
.ss-end .ss-btns{justify-content:center}
.ss-end .used{margin:26px 0 0;font-size:15px;color:rgba(255,255,255,.85)}
.ss-end .used a{color:#fff;font-weight:700}
.ss-small{font-size:12.5px;color:rgba(255,255,255,.62);max-width:820px;margin:30px auto 0;line-height:1.55}
.ss-float{display:none}
@media (max-width:1020px){.ss-choose{grid-template-columns:1fr 1fr}.ss-model{grid-template-columns:1fr}.ss-media{padding:12px 12px 0}.ss-info{padding:18px 18px 22px}.ss-split,.ss-tech,.ss-formbox{grid-template-columns:1fr;gap:30px}.ss-key{grid-template-columns:1fr}.ss-key>img{min-height:0;height:auto;aspect-ratio:16/10}.ss-steps{grid-template-columns:1fr 1fr}.ss-colors{grid-template-columns:repeat(4,1fr)}}
@media (max-width:760px){
.ss-cmp table,.ss-cmp tbody,.ss-cmp tr,.ss-cmp th,.ss-cmp td{display:block;width:100%}
.ss-cmp table{border:0;background:none;border-radius:0;overflow:visible}
.ss-cmp thead{display:none}
.ss-cmp tr{border:1px solid var(--line);border-radius:14px;margin:0 0 12px;background:#fff;overflow:hidden}
.ss-cmp tbody th{background:var(--ink);color:#fff;padding:12px 14px}
.ss-cmp td{display:flex;justify-content:space-between;gap:14px;padding:9px 14px;text-align:right}
.ss-cmp td:before{content:attr(data-l);font-weight:600;opacity:.65;text-align:left;font-family:inherit}
.ss-cmp td.pr{white-space:normal}
.ss-cmp tr:last-child td{border-bottom:1px solid var(--line)}.ss-cmp tr td:last-child{border-bottom:0}
.ss-float{display:inline-flex;align-items:center;justify-content:center;position:fixed;left:50%;bottom:calc(14px + env(safe-area-inset-bottom,0px));z-index:60;max-width:calc(100vw - 32px);background:var(--sea);color:#fff;font-weight:700;font-size:15px;line-height:1.2;padding:13px 22px;border-radius:999px;text-decoration:none;white-space:nowrap;box-shadow:0 12px 28px -10px rgba(6,8,11,.6);opacity:0;transform:translate(-50%,24px);pointer-events:none;transition:opacity .2s,transform .2s;visibility:hidden}
.ss-float.on{opacity:1;transform:translate(-50%,0);pointer-events:auto;visibility:visible}}
@media (max-width:640px){.ss .wrap{padding:0 16px}.ss-hero{min-height:86vh}.ss-hero .wrap{padding-bottom:40px}
.ss-stats .wrap{grid-template-columns:1fr 1fr;padding:0 6px}.ss-stats div{padding:18px 10px}.ss-stats div:nth-child(2){border-right:0}.ss-stats div:nth-child(-n+2){border-bottom:1px solid rgba(255,255,255,.08)}
.ss-sec{padding:44px 0}.ss-choose{grid-template-columns:1fr 1fr;gap:10px}.ss-card>div{padding:12px 12px 14px}.ss-card h3{font-size:17px}.ss-card p{display:none}.ss-card .pr{font-size:14.5px}.ss-card .vatinc{font-size:12px;white-space:normal}
.ss-info h3{font-size:25px}.ss-spec{grid-template-columns:1fr 1fr}.ss-spec div:nth-child(3n){border-right:1px solid var(--line)}.ss-spec div:nth-child(2n){border-right:0}.ss-spec div.w2{grid-column:span 2}
.ss-thumbs button{width:66px;height:50px}.ss-buy .ss-btns,.ss-buy .ss-btn{width:100%}
.ss-btns .ss-btn{width:100%}.ss-key>div{padding:24px 18px}.ss-key .ss-btn{align-self:stretch}
.ss-steps,.ss-about{grid-template-columns:1fr}.ss-form{grid-template-columns:1fr}.ss-colors{grid-template-columns:repeat(4,1fr);gap:10px}.ss-colors li{font-size:12.5px}}
@media (prefers-reduced-motion:reduce){.ss-btn,.ss-card,.ss-float{transition:none}}
"""

JS_INLINE = r"""
(function(){
 /* Galería de cada modelo: la miniatura cambia la foto grande */
 document.querySelectorAll('.ss-media').forEach(function(m){
  var main=m.querySelector('img.main');if(!main)return;
  m.querySelectorAll('.ss-thumbs button').forEach(function(t){t.addEventListener('click',function(){
   main.src=t.dataset.src;main.srcset=t.dataset.srcset;main.alt=t.getAttribute('aria-label')||main.alt;
   m.querySelectorAll('.ss-thumbs button').forEach(function(x){x.setAttribute('aria-pressed',x===t?'true':'false')});});});
 });
 /* Botones "Pedir presupuesto": preseleccionan modelo y tipo en el formulario */
 document.querySelectorAll('a[data-model],a[data-need]').forEach(function(a){a.addEventListener('click',function(){
  var s=document.getElementById('ss_model'),n=document.getElementById('ss_need');
  if(s&&a.dataset.model)s.value=a.dataset.model;if(n&&a.dataset.need)n.value=a.dataset.need;});});
 /* Botón flotante en móvil: aparece tras el hero y se oculta en el formulario */
 var fl=document.querySelector('.ss-float'),hero=document.querySelector('.ss-hero'),form=document.getElementById('presupuesto');
 if(fl&&hero&&form&&'IntersectionObserver' in window){var hv=true,fv=false;
  function u(){var on=!hv&&!fv;fl.classList.toggle('on',on);fl.setAttribute('aria-hidden',on?'false':'true');fl.tabIndex=on?0:-1;}
  new IntersectionObserver(function(e){hv=e[0].isIntersecting;u();}).observe(hero);
  new IntersectionObserver(function(e){fv=e[0].isIntersecting;u();}).observe(form);}
 /* Subnavegación: marca la sección visible */
 var links=document.querySelectorAll('.ss-subnav a');
 if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){links.forEach(function(l){l.classList.toggle('on',l.getAttribute('href')==='#'+en.target.id)})}})},{rootMargin:'-45% 0px -50% 0px'});
  links.forEach(function(l){var s=document.getElementById(l.getAttribute('href').slice(1));if(s)io.observe(s)});}
})();
"""


def wa(text):
    return f'https://wa.me/{WA}?text=' + urllib.parse.quote(text)


def prep_fotos(src):
    """Copia las fotos de fábrica a /seastorm/fotos/ redimensionadas y sin metadatos."""
    from PIL import Image, ImageOps
    os.makedirs(FOTOS, exist_ok=True)
    def save(im, path, w, h=None):
        im = im.convert('RGB')
        im = ImageOps.fit(im, (w, h or w * 3 // 4), Image.LANCZOS)
        im.save(path, 'JPEG', quality=82, optimize=True, progressive=True)  # sin exif
    for slug, *_ in M:
        files = [f for f in glob.glob(f'{src}/{slug}-*') if re.search(rf'/{re.escape(slug)}-\d+\.(jpe?g|png|webp)$', f, re.I)]
        files.sort(key=lambda f: int(re.search(r'-(\d+)\.\w+$', f).group(1)))
        for i, f in enumerate(files, 1):
            im = ImageOps.exif_transpose(Image.open(f))
            save(im, f'{FOTOS}/{slug}-{i}.jpg', 1200)
            save(im, f'{FOTOS}/{slug}-{i}-m.jpg', 800)
    if os.path.exists(f'{src}/hero.jpg'):
        save(Image.open(f'{src}/hero.jpg'), f'{FOTOS}/portada.jpg', 1000, 600)
    logo = f'{src}/logo.png'
    if os.path.exists(logo):
        im = Image.open(logo).convert('RGBA')
        im = im.crop(im.getbbox())
        w = 840
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(f'{FOTOS}/seastorm-logo.png', optimize=True)


GAL_SKIP = {KEY_IMG}  # foto de grupo (varios barcos en remolque): solo para el bloque llave en mano


def fotos(slug):
    n = len(glob.glob(f'{FOTOS}/{slug}-[0-9]*.jpg')) // 2
    return [i for i in range(1, n + 1) if f'{slug}-{i}' not in GAL_SKIP]


def nfotos(slug):
    return len(fotos(slug))


def img(name, alt, sizes='100vw', lazy=True, cls='', extra=''):
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="{F}{name}.jpg" srcset="{F}{name}-m.jpg 800w, {F}{name}.jpg 1200w" sizes="{sizes}" alt="{html.escape(alt)}" '
            f'width="1200" height="900"{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""} decoding="async"{extra}>')


def logo_ph(name, sub=''):
    s = f'<span>{html.escape(sub)}</span>' if sub else ''
    return (f'<div class="ph0" role="img" aria-label="{html.escape(name)}"><img src="{F}seastorm-logo.png" alt="" width="840" height="60" loading="lazy">'
            f'<b>{html.escape(name.replace("SeaStorm ", ""))}</b>{s}</div>')


def build(lang):
    p = LANGS[lang]
    t = T[lang]
    L = t['lab']
    vat = VAT[lang]
    url = f'{BASE}{p}/seastorm/'
    tpl = open(f'{ROOT}{p}/barcos-nuevos/index.html', encoding='utf-8').read()
    head, rest = tpl.split('</head>', 1)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{html.escape(t["title"])}</title>', head)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc']), head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(t['title']), head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc']), head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', f'\\g<1>{BASE}{F}portada.jpg', head)
    head = re.sub(r'<meta property="og:image:width"[^>]*>\n?<meta property="og:image:height"[^>]*>', '<meta property="og:image:width" content="1000">\n<meta property="og:image:height" content="600">', head)
    head = head.replace('/barcos-nuevos/', '/seastorm/')
    head = head.replace('<meta name="twitter:card"', f'<link rel="preload" as="image" href="{F}{HERO}.jpg" imagesrcset="{F}{HERO}-m.jpg 800w, {F}{HERO}.jpg 1200w" imagesizes="100vw">\n<meta name="theme-color" content="#06080b">\n<meta name="twitter:card"', 1)

    # Datos estructurados
    prods = []
    for slug, name, *_r in M:
        price = _r[10]
        it = {"@type": "Product", "name": name, "url": f"{url}#seastorm-{slug}", "brand": {"@type": "Brand", "name": "SeaStorm"},
              "description": t['d'][slug], "category": "Boat"}
        n = nfotos(slug)
        if n:
            it["image"] = [f"{BASE}{F}{slug}-{i}.jpg" for i in fotos(slug)]
        it["offers"] = {"@type": "Offer", "price": price, "priceCurrency": "EUR", "availability": "https://schema.org/PreOrder",
                        "url": f"{url}#seastorm-{slug}", "itemCondition": "https://schema.org/NewCondition",
                        "seller": {"@type": "Organization", "name": "Plata Marine"},
                        "priceSpecification": {"@type": "UnitPriceSpecification", "price": price, "priceCurrency": "EUR", "valueAddedTaxIncluded": False}}
        prods.append(it)
    strip = lambda s: re.sub(r'<[^>]+>', '', s.replace('{p}', p))
    ld = [
        {"@context": "https://schema.org", "@graph": [{"@type": "WebPage", "name": t['title'], "description": t['desc'], "inLanguage": lang, "url": url,
                                                         "publisher": {"@type": "Organization", "name": "Plata Marine"}}, *prods]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f"{BASE}{p}/"},
            {"@type": "ListItem", "position": 2, "name": t['crumbs'][1], "item": f"{BASE}{p}/barcos-nuevos/"},
            {"@type": "ListItem", "position": 3, "name": "SeaStorm", "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for _, q, a in t['faq']]},
    ]
    head = head.replace('<style>', ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld) + '<style>', 1)
    head = head.replace('</style>', CSS + '</style>', 1)

    body = rest
    body = body.replace('/barcos-nuevos/" aria-current', '/seastorm/" aria-current')
    body = re.sub(r'(<div class="langsw".*?</div>)', lambda m: m.group(1).replace('/barcos-nuevos/', '/seastorm/'), body, flags=re.S)
    body = re.sub(r'(<div style="display:flex;align-items:center;gap:12px">\s*<a class="btn btn-wa" href=")[^"]*', lambda m: m.group(1) + html.escape(wa(t['wa_gen'])), body, count=1)

    def price_html(n, big=False):
        inc = eur(round(n * (1 + IVA)), lang)
        return f'{eur(n, lang)}<span class="vat">{vat}</span><span class="vatinc">{t["vinc"].format(v=inc)}</span>'

    # Tarjetas de elección
    cards = []
    for slug, name, *_r in M:
        n = nfotos(slug)
        pic = img(f'{slug}-{fotos(slug)[0]}', name, '(max-width:640px) 50vw, (max-width:1020px) 50vw, 280px') if n else logo_ph(name)
        cards.append(f'<a class="ss-card" href="#seastorm-{slug}">{pic}<div><span class="tg">{t["tag"][slug]}</span><h3>{name}</h3>'
                     f'<p>{html.escape(t["d"][slug])}</p><span class="pr">{t["from_"]} {price_html(_r[10])}</span><span class="go">{t["see"]}</span></div></a>')

    # Fichas por modelo
    models = []
    for slug, name, loa, beam, w, dr, cap, pc, pd, hp, kw, rec, price, over5 in M:
        n = nfotos(slug)
        if n:
            fl = fotos(slug)
            main = img(f'{slug}-{fl[0]}', f'{name} – 1', '(max-width:1020px) 100vw, 620px', cls='main')
            thumbs = '' if n < 2 else '<div class="ss-thumbs">' + ''.join(
                f'<button type="button" aria-pressed="{"true" if i == fl[0] else "false"}" aria-label="{name} – {i}" data-src="{F}{slug}-{i}.jpg" data-srcset="{F}{slug}-{i}-m.jpg 800w, {F}{slug}-{i}.jpg 1200w">'
                f'<img src="{F}{slug}-{i}-m.jpg" alt="" width="800" height="600" loading="lazy" decoding="async"></button>' for i in fl) + '</div>'
            media = main + thumbs
        else:
            media = logo_ph(name, t['nophoto'])
        spec = [(L['loa'], f'{num(loa, lang)} m'), (L['beam'], f'{num(beam, lang)} m'), (L['w'], kg(w, lang)),
                (L['dr'], f'{dr} cm'), (L['cap'], kg(cap, lang)), (L['hp'], t['hp_v'].format(h=hp, k=kw)),
                (L['pax'], t['pax_v'].format(c=pc, d=pd)), (L['rec'], t['rec_v'].format(r=rec))]
        specs = ''.join(f'<div{" class=" + chr(34) + "w2" + chr(34) if i >= 6 else ""}><dt>{a}</dt><dd>{b}</dd></div>' for i, (a, b) in enumerate(spec))
        specs += f'<div class="w2"><dt>{L["lic"]}</dt><dd>{t["lic_long"]}</dd></div>'
        licnote = '' if over5 else f'<p class="ss-lic">{t["lic_note"].format(p=p)}</p>'
        models.append(f'''<article class="ss-model" id="seastorm-{slug}">
  <div class="ss-media">{media}</div>
  <div class="ss-info">
    <p class="tg">{t['tag'][slug]}</p>
    <h3>{name}</h3>
    <p class="d">{html.escape(t['d'][slug])}</p>
    <dl class="ss-spec">{specs}</dl>{licnote}
    <div class="ss-buy"><div><small>{t['from_']} · {t['adv']}</small><strong>{eur(price, lang)}</strong><span class="vat">{vat}</span><span class="vatinc">{t['vinc'].format(v=eur(round(price * (1 + IVA)), lang))}</span></div>
      <div class="ss-btns"><a class="ss-btn pri" href="#presupuesto" data-model="{name}">{t['ask_m']}</a><a class="ss-btn wa" href="{html.escape(wa(t['wa_m'].format(m=name)))}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a></div></div>
  </div>
</article>''')

    # Comparativa (en móvil, cada fila se convierte en tarjeta)
    heads = [t['cmp_model'], t['cmp_from'], L['loa'], L['beam'], L['w'], L['pax'], L['hp'], L['rec']]
    rows = []
    for slug, name, loa, beam, w, dr, cap, pc, pd, hp, kw, rec, price, over5 in M:
        vals = [f'{eur(price, lang)}<span class="vat">{vat}</span>', f'{num(loa, lang)} m', f'{num(beam, lang)} m', kg(w, lang),
                t['pax_v'].format(c=pc, d=pd), t['hp_v'].format(h=hp, k=kw), t['rec_v'].format(r=rec)]
        tds = ''.join(f'<td data-l="{html.escape(h)}"{" class=" + chr(34) + "pr" + chr(34) if i == 0 else ""}>{v}</td>' for i, (h, v) in enumerate(zip(heads[1:], vals)))
        rows.append(f'<tr><th scope="row"><a href="#seastorm-{slug}">{name}</a></th>{tds}</tr>')
    cmp = '<table><thead><tr>' + ''.join(f'<th scope="col">{h}</th>' for h in heads) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'

    stats = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in t['stats'])
    subnav = ''.join(f'<a href="#{i}">{l}</a>' for i, l in t['nav'])
    tech = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in t['tech'])
    steps = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in t['steps'])
    colors = ''.join(f'<li><i style="background:{hx}"></i>{t["col"][k]}</li>' for hx, k in COLORS)
    faq = ''.join(f'<details{" id=" + chr(34) + i + chr(34) if i else ""}><summary>{q}</summary><p>{a.replace("{p}", p)}</p></details>' for i, q, a in t['faq'])
    min_price = min(m[12] for m in M)
    opt = t['f_opt']
    mopts = ''.join(f'<option>{m[1]}</option>' for m in M) + f'<option value="?">{t["f_dunno"]}</option>'
    nopts = ''.join(f'<option value="{v}">{l}</option>' for v, l in t['f_needs'])
    copts = f'<option value="">{t["f_any"]}</option>' + ''.join(f'<option>{t["col"][k]}</option>' for _, k in COLORS)
    form = f'''<form id="ssForm" class="ss-form" novalidate data-contact-intent="seastorm">
<div><label for="ss_model">{t['f_model']} <i>*</i></label><select id="ss_model" name="ss_model" required>{mopts}</select></div>
<div><label for="ss_need">{t['f_need']} <i>*</i></label><select id="ss_need" name="ss_need" required>{nopts}</select></div>
<div><label for="ss_name">{t['f_name']} <i>*</i></label><input id="ss_name" name="ss_name" type="text" required autocomplete="name" maxlength="60"></div>
<div><label for="ss_tel">{t['f_tel']} <i>*</i></label><input id="ss_tel" name="ss_tel" type="tel" required autocomplete="tel" inputmode="tel" maxlength="20" placeholder="+34 6xx xxx xxx"></div>
<div><label for="ss_email">{t['f_email']} <i>*</i></label><input id="ss_email" name="ss_email" type="email" required autocomplete="email" maxlength="100"></div>
<div><label for="ss_color">{t['f_color']} <small>{opt}</small></label><select id="ss_color" name="ss_color">{copts}</select></div>
<div class="span2"><label for="ss_zone">{t['f_zone']} <small>{opt}</small></label><input id="ss_zone" name="ss_zone" type="text" maxlength="60" placeholder="{t['f_zone_ph']}"></div>
<div class="span2"><label for="ss_msg">{t['f_msg']} <small>{opt}</small></label><textarea id="ss_msg" name="ss_msg" maxlength="1500" placeholder="{t['f_msg_ph']}"></textarea></div>
<p class="help span2">{t['f_priv']}</p>
<div class="span2"><label class="chk" for="ss_consent"><input id="ss_consent" name="ss_consent" type="checkbox" required><span>{t['f_consent']}&nbsp;<i>*</i></span></label></div>
<div class="span2"><button type="submit" id="ss_send">{t['f_send']}</button></div>
<p class="help span2">{t['f_req']}</p>
<p id="ss_status" class="help span2" role="status" aria-live="polite" hidden></p>
</form>'''
    logo = f'<img class="ss-logo" src="{F}seastorm-logo.png" alt="SeaStorm" width="840" height="60" decoding="async">'
    btn_quote = f'<a class="ss-btn pri" href="#presupuesto">{t["cta"]}</a>'
    btn_wa = f'<a class="ss-btn ghost" href="{html.escape(wa(t["wa_gen"]))}" target="_blank" rel="noopener">{WA_SVG}{t["cta_wa"]}</a>'
    main = f'''<main class="ss">
<section class="ss-hero">
  {img(HERO, 'SeaStorm 17', lazy=False, extra=' fetchpriority="high"')}
  <div class="wrap">
    <p class="ss-crumb"><a href="{p}/">{t['crumbs'][0]}</a><span>·</span><a href="{p}/barcos-nuevos/">{t['crumbs'][1]}</a><span>·</span><span>SeaStorm</span></p>
    {logo}
    <p class="ss-eyebrow">{t['eyebrow']}</p>
    <h1>{html.escape(t['h1'])}</h1>
    <p class="lead">{html.escape(t['lead'])}</p>
    <p class="ss-hprice"><small>{t['hfrom']}</small> {eur(min_price, lang)}<span class="vat">{vat}</span><span class="hn">{t['hnote']}</span></p>
    <div class="ss-btns">{btn_quote}{btn_wa}</div>
  </div>
</section>
<div class="ss-stats"><div class="wrap">{stats}</div></div>
<nav class="ss-subnav" aria-label="SeaStorm"><div class="wrap">{subnav}</div></nav>
<section class="ss-sec" id="modelos">
  <div class="wrap">
    <p class="ss-kick">{t['choose_k']}</p><h2>{t['choose_h']}</h2><p class="ss-sub">{t['choose_p']}</p>
    <div class="ss-choose">{''.join(cards)}</div>
  </div>
</section>
<section class="ss-sec ss-alt" style="padding-top:44px">
  <div class="wrap">
{chr(10).join(models)}
  </div>
</section>
<section class="ss-sec" id="comparar">
  <div class="wrap"><p class="ss-kick">{t['cmp_k']}</p><h2 style="margin-bottom:24px">{t['cmp_h']}</h2><div class="ss-cmp specs">{cmp}</div></div>
</section>
<section class="ss-sec" style="padding-top:0">
  <div class="wrap ss-split">
    {img(ADV_IMG, 'SeaStorm 14', '(max-width:1020px) 100vw, 540px')}
    <div><p class="ss-kick">{t['adv_k']}</p><h2>{t['adv_h']}</h2><p class="ss-sub" style="margin-bottom:18px">{t['adv_p']}</p>
    <ul class="ss-chips">{''.join(f'<li>{x}</li>' for x in t['adv_list'])}</ul><p class="ss-note">{t['adv_note']}</p></div>
  </div>
</section>
<section class="ss-sec" id="llave-en-mano" style="padding-top:0">
  <div class="wrap"><div class="ss-key">
    {img(KEY_IMG, 'SeaStorm', '(max-width:1020px) 100vw, 580px')}
    <div><p class="ss-kick">{t['key_k']}</p><h2>{t['key_h']}</h2><p>{t['key_p']}</p>
    <ul>{''.join(f'<li>{x}</li>' for x in t['key_list'])}</ul>
    <a class="ss-btn pri" href="#presupuesto" data-need="llave">{t['key_cta']}</a><small>{t['key_note']}</small></div>
  </div></div>
</section>
<section class="ss-sec ss-dark">
  <div class="wrap ss-tech">
    <div><p class="ss-kick">{t['tech_k']}</p><h2>{t['tech_h']}</h2><p class="ss-sub">{t['tech_p']}</p><ol>{tech}</ol><p class="ss-note">{t['tech_note']}</p></div>
    {img(TECH_IMG, 'SeaStorm 14', '(max-width:1020px) 100vw, 560px')}
  </div>
</section>
<section class="ss-sec" id="colores">
  <div class="wrap"><p class="ss-kick">{t['col_k']}</p><h2>{t['col_h']}</h2><p class="ss-sub">{t['col_p']}</p><ul class="ss-colors">{colors}</ul></div>
</section>
<section class="ss-sec ss-alt" id="video">
  <div class="wrap">
    <p class="ss-kick">{t['vid_k']}</p><h2>{t['vid_h']}</h2><p class="ss-sub">{t['vid_p']}</p>
    <div class="ss-video" data-yt="{YT}" data-title="SeaStorm"><button type="button" aria-label="{t['vid_play']}">{img(VIDEO_POSTER, '', '(max-width:1000px) 100vw, 1000px')}<span class="play"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></span></button></div>
  </div>
</section>
<section class="ss-sec" id="comprar">
  <div class="wrap"><h2 style="margin-bottom:30px">{t['how_h']}</h2><ol class="ss-steps">{steps}</ol></div>
</section>
<section class="ss-sec ss-alt" id="presupuesto">
  <div class="wrap ss-formbox">
    <div><p class="ss-kick">{t['nav'][-1][1]}</p><h2>{t['form_h']}</h2><p class="ss-sub">{t['form_p']}</p>
      <div class="alt"><p>{t['f_alt']}</p><a class="ss-btn line" href="{html.escape(wa(t['wa_gen']))}" target="_blank" rel="noopener">{WA_SVG}WhatsApp</a></div></div>
    <div>{form}</div>
  </div>
</section>
<section class="ss-sec ss-faq" id="faq">
  <div class="wrap"><h2 style="margin-bottom:14px">{t['faq_h']}</h2>{faq}</div>
</section>
<section class="ss-sec" style="padding-top:0">
  <div class="wrap"><h2 style="margin-bottom:24px">{t['about_h']}</h2>
    <div class="ss-about"><div><img src="{F}seastorm-logo.png" alt="SeaStorm" width="840" height="60" loading="lazy"><p>{t['about_ss']}</p></div>
    <div><b>{t['about_me_h']} · Plata Marine</b><p>{t['about_me']}</p></div></div>
  </div>
</section>
<section class="ss-sec ss-end">
  {img(END_IMG, 'SeaStorm 17')}
  <div class="wrap">
    <h2>{t['end_h']}</h2><p class="ss-sub">{t['end_p']}</p>
    <div class="ss-btns">{btn_quote}{btn_wa}</div>
    <p class="used">{t['used'].format(p=p)}</p>
    <p class="ss-small">{html.escape(t['small'])}</p>
  </div>
</section>
<a class="ss-float" href="#presupuesto" tabindex="-1" aria-hidden="true">{t['float']}</a>
</main>'''
    body = re.sub(r'<main class="boat">.*?</main>', lambda m: main, body, flags=re.S)
    scripts = (f'<script>{JS_INLINE}</script>\n<script src="/submit-confirmed.js" defer></script>\n'
               '<script src="/seastorm/seastorm.js?v=20261020" defer></script>\n')
    body = body.replace('</body>', scripts + '</body>', 1)
    out = head + '</head>' + body
    os.makedirs(f'{ROOT}{p}/seastorm', exist_ok=True)
    open(f'{ROOT}{p}/seastorm/index.html', 'w', encoding='utf-8').write(out)
    print('ok', lang, len(out))


if __name__ == '__main__':
    if '--fotos' in sys.argv:
        prep_fotos(sys.argv[sys.argv.index('--fotos') + 1])
    sin = [m[1] for m in M if not nfotos(m[0])]
    if sin:
        print('AVISO: sin fotos en', ', '.join(sin), '(se muestra tarjeta con el logo)')
    for l in LANGS:
        build(l)
