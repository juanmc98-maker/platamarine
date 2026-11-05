#!/usr/bin/env python3
"""Genera /motos-de-agua-nuevas/ en ES/CA/EN/FR (Sea-Doo y Kawasaki, precios a consultar).
Cabecera y pie se copian de /remolques/ de cada idioma. Uso: python3 _tools/build_motos_agua_nuevas.py"""
import json, os, re, html
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'motos-de-agua-nuevas'
BASE = 'https://www.platamarine.com'
LANGS = ['es', 'ca', 'en', 'fr']
PFX = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}

# (clave foto, nombre, cv, plazas) — plazas 0 = de pie; cv None = no se muestra
SEADOO = [
 ('perf', [('sd-rxp-x-senna', 'RXP-X 350 Senna', 350, 2), ('sd-rxp-x-350-solar-orange', 'RXP-X 350', 350, 2), ('sd-rxt-x-350-solar-orange', 'RXT-X 350', 350, 3)]),
 ('tour', [('sd-gtx-limited', 'GTX Limited 350', 350, 3), ('sd-gtx-230', 'GTX 230', 230, 3), ('sd-gtx', 'GTX 170', 170, 3)]),
 ('adv',  [('sd-fishpro-trophy', 'Fish Pro Trophy 170', 170, 3), ('sd-explorer-pro', 'Explorer Pro 230', 230, 3), ('sd-wake-pro-230', 'Wake Pro 230', 230, 3), ('sd-wake-170', 'Wake 170', 170, 3)]),
 ('rec',  [('sd-gti-se-teal-blue', 'GTI SE 170', 170, 3), ('sd-gti', 'GTI 130', 130, 3)]),
 ('lite', [('sd-trixx-for3-blue-mist', 'Spark Trixx 110', 110, 3), ('sd-spark-x', 'Spark X 110', 110, 3), ('sd-spark', 'Spark', None, 2)]),
]
KAWA = [
 ('ultra', [('kw-ultra-310lx-2027', 'Ultra 310LX', 300, 3), ('kw-ultra-310lx-s-2027', 'Ultra 310LX-S', 300, 3), ('kw-ultra-160lx-s-wakesport', 'Ultra 160LX-S Wakesport', 152, 3), ('kw-ultra-160lx-2027', 'Ultra 160LX', 152, 3), ('kw-ultra-160lx-s-2027', 'Ultra 160LX-S', 152, 3)]),
 ('stx',   [('kw-stx-310rx', 'STX 310RX', 300, 3), ('kw-stx-310r', 'STX 310R', 300, 3), ('kw-stx-160lx-2027', 'STX 160LX', 152, 3), ('kw-stx-160lx-s-2027', 'STX 160LX-S', 152, 3), ('kw-stx-160r-2027', 'STX 160R', 152, 3), ('kw-stx-160x-2027', 'STX 160X', 152, 3)]),
 ('sx',    [('kw-sx-r-160', 'SX-R 160', 152, 0), ('kw-sx-x-160', 'SX-X 160', None, 0)]),
]

T = {
 'es': dict(
  tit='Titulación: Licencia de Navegación o superior.',
  title='Motos de agua nuevas 2027: Sea-Doo y Kawasaki en Barcelona',
  desc='Motos de agua nuevas Sea-Doo y Kawasaki 2027: Spark, GTI, GTX, RXP-X, Ultra, STX y SX-R. Compara modelos y pide presupuesto por WhatsApp en Barcelona.',
  home='Inicio', nb='Barcos nuevos', crumb='Motos de agua nuevas',
  kick='Motos de agua nuevas', h1='Motos de agua nuevas Sea-Doo y Kawasaki 2027',
  lead='La gama 2027 de las dos marcas, de la Spark para empezar a la Ultra para hacer millas. Me dices cuál te interesa y te paso el precio por escrito, con lo que incluye y el plazo de entrega.',
  ask='Precio a consultar', btn='Pedir presupuesto', jump_sd='Ver gama Sea-Doo', jump_kw='Ver gama Kawasaki',
  cv='cv', seats='{n} plazas', stand='De pie',
  wa='Hola Juan, quiero presupuesto de la moto de agua nueva {m} (2027). Te digo mi provincia y si necesito remolque: ', wa_gen='Hola Juan, quiero información sobre una moto de agua nueva.',
  fam={'perf': ('Performance', 'Las más deportivas: casco y motor pensados para correr y girar fuerte.'),
       'tour': ('Touring', 'Para salir con acompañante y hacer millas cómodo: más estabilidad, asiento grande y guantera.'),
       'adv': ('Aventura, pesca y arrastre', 'Modelos con equipamiento para travesía, pesca o tirar de esquí y wakeboard.'),
       'rec': ('Recreativas', 'El punto medio: fáciles de llevar, para toda la familia y uso de verano.'),
       'lite': ('Spark', 'Las más ligeras y económicas de Sea-Doo; ideales para empezar.'),
       'ultra': ('Ultra', 'La gama de travesía de Kawasaki: grandes, estables y con mucha autonomía.'),
       'stx': ('STX', 'Recreativas de tres plazas, equilibradas entre comodidad y prestaciones.'),
       'sx': ('SX', 'Motos de pie (stand-up) para pilotar en solitario.')},
  how_h='Cómo funciona', how=[('Me dices qué buscas', 'Modelo, o cómo la vas a usar: sola, en pareja, con niños, para tirar de esquí…'),
       ('Te paso el precio por escrito', 'Con la versión, color y extras, lo que incluye y el plazo de entrega.'),
       ('Te acompaño hasta el agua', 'Te oriento con la matrícula, el remolque y dónde guardarla.')],
  faq_h='Preguntas frecuentes',
  faq=[('¿Por qué el precio es a consultar?', 'Porque cambia según versión, color, extras y las promociones de cada momento. Prefiero pasarte la cifra cerrada por escrito, detallando qué incluye.'),
       ('¿Qué titulación necesito?', 'Licencia de Navegación o superior. Tienes un resumen en <a href="/titulaciones/">titulaciones náuticas</a>.'),
       ('¿Cuánto tarda en llegar?', 'Depende del modelo, el color y las unidades disponibles. El plazo es a consultar y te lo confirmo por escrito antes de que decidas.'),
       ('¿Tienes motos de agua de segunda mano?', 'Sí, cuando hay alguna en cartera. Mira las <a href="/comprar/motos-de-agua-segunda-mano">motos de agua de segunda mano</a> o dime qué buscas y te aviso.')],
  end_h='¿Cuál te interesa?', used='Motos de agua de segunda mano',
  small='Modelos y datos de la gama 2027 de cada fabricante, que pueden cambiar sin aviso. Precio, colores, disponibilidad y plazo de entrega a consultar y confirmados por escrito. Información orientativa: podemos equivocarnos y no es vinculante.',
  list_name='Motos de agua nuevas Sea-Doo y Kawasaki'),
 'ca': dict(
  tit='Titulació: Llicència de Navegació o superior.',
  title="Motos d'aigua noves 2027: Sea-Doo i Kawasaki a Barcelona",
  desc="Motos d'aigua noves Sea-Doo i Kawasaki 2027: Spark, GTI, GTX, RXP-X, Ultra, STX i SX-R. Compara models i demana pressupost per WhatsApp a Barcelona.",
  home='Inici', nb='Vaixells nous', crumb="Motos d'aigua noves",
  kick="Motos d'aigua noves", h1="Motos d'aigua noves Sea-Doo i Kawasaki 2027",
  lead="La gamma 2027 de les dues marques, de la Spark per començar a la Ultra per fer milles. Em dius quina t'interessa i et passo el preu per escrit, amb el que inclou i el termini de lliurament.",
  ask='Preu a consultar', btn='Demanar pressupost', jump_sd='Veure gamma Sea-Doo', jump_kw='Veure gamma Kawasaki',
  cv='cv', seats='{n} places', stand='Dempeus',
  wa="Hola Juan, vull pressupost de la moto d'aigua nova {m} (2027). Et dic la meva província i si necessito remolc: ", wa_gen="Hola Juan, vull informació sobre una moto d'aigua nova.",
  fam={'perf': ('Performance', 'Les més esportives: buc i motor pensats per córrer i girar fort.'),
       'tour': ('Touring', 'Per sortir acompanyat i fer milles còmode: més estabilitat, seient gran i guantera.'),
       'adv': ('Aventura, pesca i arrossegament', "Models amb equipament per a travessia, pesca o per tirar d'esquí i wakeboard."),
       'rec': ('Recreatives', "El punt mitjà: fàcils de portar, per a tota la família i ús d'estiu."),
       'lite': ('Spark', 'Les més lleugeres i econòmiques de Sea-Doo; ideals per començar.'),
       'ultra': ('Ultra', 'La gamma de travessia de Kawasaki: grans, estables i amb molta autonomia.'),
       'stx': ('STX', 'Recreatives de tres places, equilibrades entre comoditat i prestacions.'),
       'sx': ('SX', 'Motos dempeus (stand-up) per pilotar en solitari.')},
  how_h='Com funciona', how=[('Em dius què busques', "Model, o com la faràs servir: sol, en parella, amb nens, per tirar d'esquí…"),
       ('Et passo el preu per escrit', 'Amb la versió, color i extres, el que inclou i el termini de lliurament.'),
       ("T'acompanyo fins a l'aigua", "T'oriento amb la matrícula, el remolc i on guardar-la.")],
  faq_h='Preguntes freqüents',
  faq=[('Per què el preu és a consultar?', "Perquè canvia segons versió, color, extres i les promocions de cada moment. Prefereixo passar-te la xifra tancada per escrit, detallant què inclou."),
       ('Quina titulació necessito?', "Llicència de Navegació o superior. Tens un resum a <a href=\"/ca/titulaciones/\">titulacions nàutiques</a>."),
       ('Quant triga a arribar?', "Depèn del model, el color i les unitats disponibles. El termini és a consultar i te'l confirmo per escrit abans que decideixis."),
       ("Tens motos d'aigua de segona mà?", "Sí, quan n'hi ha alguna en cartera. Mira les <a href=\"/ca/comprar/motos-de-agua-segunda-mano\">motos d'aigua de segona mà</a> o digues-me què busques i t'aviso.")],
  end_h="Quina t'interessa?", used="Motos d'aigua de segona mà",
  small="Models i dades de la gamma 2027 de cada fabricant, que poden canviar sense avís. Preu, colors, disponibilitat i termini de lliurament a consultar i confirmats per escrit. Informació orientativa: ens podem equivocar i no és vinculant.",
  list_name="Motos d'aigua noves Sea-Doo i Kawasaki"),
 'en': dict(
  tit='Licence: Spanish Licencia de Navegación (LN) or higher.',
  title='New 2027 Sea-Doo and Kawasaki jet skis in Barcelona',
  desc='New 2027 Sea-Doo and Kawasaki jet skis: Spark, GTI, GTX, RXP-X, Ultra, STX and SX-R. Compare models and ask for a quote on WhatsApp in Barcelona.',
  home='Home', nb='New boats', crumb='New jet skis',
  kick='New jet skis', h1='New 2027 Sea-Doo and Kawasaki jet skis',
  lead="The 2027 range from both brands, from the Spark to get started to the Ultra for long rides. Tell me which one you like and I'll send you the price in writing, with what it includes and the delivery time.",
  ask='Price on request', btn='Ask for a quote', jump_sd='See Sea-Doo range', jump_kw='See Kawasaki range',
  cv='hp', seats='{n} seats', stand='Stand-up',
  wa="Hi Juan, I'd like a quote for the new {m} jet ski (2027). My area and whether I need a trailer: ", wa_gen="Hi Juan, I'd like information about a new jet ski.",
  fam={'perf': ('Performance', 'The sportiest ones: hull and engine built to go fast and turn hard.'),
       'tour': ('Touring', 'For riding two-up and covering miles in comfort: more stability, a big seat and storage.'),
       'adv': ('Adventure, fishing and tow sports', 'Models equipped for long trips, fishing or pulling skis and wakeboards.'),
       'rec': ('Recreation', 'The middle ground: easy to ride, for the whole family and summer use.'),
       'lite': ('Spark', "Sea-Doo's lightest and most affordable; ideal to get started."),
       'ultra': ('Ultra', "Kawasaki's touring range: big, stable and with plenty of range."),
       'stx': ('STX', 'Three-seat recreation models, balanced between comfort and performance.'),
       'sx': ('SX', 'Stand-up jet skis for riding solo.')},
  how_h='How it works', how=[('Tell me what you need', 'A model, or how you will use it: alone, as a couple, with kids, for towing skis…'),
       ("I send you the price in writing", 'With version, colour and extras, what it includes and the delivery time.'),
       ("I help you all the way to the water", 'Guidance on registration, trailer and where to keep it.')],
  faq_h='FAQ',
  faq=[('Why is the price on request?', 'Because it changes with version, colour, extras and current promotions. I prefer to give you a closed figure in writing, detailing what it includes.'),
       ('What licence do I need?', 'The Spanish Licencia de Navegación (LN) or higher. There is a summary in <a href="/en/titulaciones/">boating licences</a>.'),
       ('How long does delivery take?', 'It depends on the model, colour and available units. Delivery time is on request and I confirm it in writing before you decide.'),
       ('Do you have used jet skis?', 'Yes, when there are some in the portfolio. See <a href="/en/comprar/motos-de-agua-segunda-mano">used jet skis</a> or tell me what you are looking for and I will let you know.')],
  end_h='Which one do you like?', used='Used jet skis',
  small="Models and data from each manufacturer's 2027 range, which may change without notice. Price, colours, availability and delivery time on request and confirmed in writing. Indicative information: we may be wrong and it is not binding.",
  list_name='New Sea-Doo and Kawasaki jet skis'),
 'fr': dict(
  tit='Permis : Licencia de Navegación espagnole (LN) ou supérieure.',
  title='Jet-skis neufs 2027 Sea-Doo et Kawasaki à Barcelone',
  desc='Jet-skis neufs Sea-Doo et Kawasaki 2027 : Spark, GTI, GTX, RXP-X, Ultra, STX et SX-R. Comparez les modèles et demandez un devis par WhatsApp à Barcelone.',
  home='Accueil', nb='Bateaux neufs', crumb='Jet-skis neufs',
  kick='Jet-skis neufs', h1='Jet-skis neufs Sea-Doo et Kawasaki 2027',
  lead="La gamme 2027 des deux marques, du Spark pour débuter à l'Ultra pour faire des milles. Dites-moi lequel vous intéresse et je vous envoie le prix par écrit, avec ce qui est inclus et le délai de livraison.",
  ask='Prix sur demande', btn='Demander un devis', jump_sd='Voir la gamme Sea-Doo', jump_kw='Voir la gamme Kawasaki',
  cv='ch', seats='{n} places', stand='Debout',
  wa='Bonjour Juan, je voudrais un devis pour le jet-ski neuf {m} (2027). Ma région et si j’ai besoin d’une remorque : ', wa_gen="Bonjour Juan, je voudrais des informations sur un jet-ski neuf.",
  fam={'perf': ('Performance', 'Les plus sportifs : coque et moteur pensés pour aller vite et virer fort.'),
       'tour': ('Touring', 'Pour sortir à deux et faire des milles confortablement : plus de stabilité, grande selle et rangement.'),
       'adv': ('Aventure, pêche et traction', 'Modèles équipés pour la randonnée, la pêche ou tracter ski nautique et wakeboard.'),
       'rec': ('Loisir', "Le juste milieu : faciles à piloter, pour toute la famille et l'été."),
       'lite': ('Spark', 'Les plus légers et abordables de Sea-Doo ; idéaux pour débuter.'),
       'ultra': ('Ultra', 'La gamme randonnée de Kawasaki : grands, stables et avec beaucoup d’autonomie.'),
       'stx': ('STX', 'Modèles de loisir trois places, équilibrés entre confort et performances.'),
       'sx': ('SX', 'Jet-skis à bras (stand-up) pour piloter seul.')},
  how_h='Comment ça marche', how=[('Vous me dites ce que vous cherchez', 'Un modèle, ou votre usage : seul, à deux, avec des enfants, pour tracter…'),
       ('Je vous envoie le prix par écrit', 'Avec version, couleur et options, ce qui est inclus et le délai de livraison.'),
       ("Je vous accompagne jusqu'à l'eau", 'Conseils sur l’immatriculation, la remorque et où le garder.')],
  faq_h='Questions fréquentes',
  faq=[('Pourquoi le prix est-il sur demande ?', 'Parce qu’il change selon la version, la couleur, les options et les promotions du moment. Je préfère vous donner un chiffre ferme par écrit, en détaillant ce qui est inclus.'),
       ('Quel permis me faut-il ?', 'La Licencia de Navegación espagnole (LN) ou supérieure. Résumé dans <a href="/fr/titulaciones/">permis bateau</a>.'),
       ('Quel est le délai de livraison ?', 'Cela dépend du modèle, de la couleur et des unités disponibles. Le délai est sur demande et je vous le confirme par écrit avant que vous décidiez.'),
       ("Avez-vous des jet-skis d'occasion ?", "Oui, quand il y en a en portefeuille. Voir les <a href=\"/fr/comprar/motos-de-agua-segunda-mano\">jet-skis d'occasion</a> ou dites-moi ce que vous cherchez et je vous préviens.")],
  end_h='Lequel vous intéresse ?', used="Jet-skis d'occasion",
  small="Modèles et données de la gamme 2027 de chaque fabricant, susceptibles de changer sans préavis. Prix, couleurs, disponibilité et délai de livraison sur demande et confirmés par écrit. Information indicative : nous pouvons nous tromper et elle n’est pas contractuelle. Nous ne parlons pas français : nous utilisons un traducteur.",
  list_name='Jet-skis neufs Sea-Doo et Kawasaki'),
}

for _l, _g in (('es', 'Gama {b} 2027'), ('ca', 'Gamma {b} 2027'), ('en', '{b} 2027 range'), ('fr', 'Gamme {b} 2027')):
    T[_l]['gama'] = _g

X = {
 'es': dict(
  uso_h='¿Qué moto de agua comprar según el uso?',
  uso=[('Para empezar o salir de vez en cuando', 'Sea-Doo Spark y Spark X: ligeras, fáciles de llevar y de remolcar. Si buscas algo más juguetón, la Spark Trixx.'),
       ('Para la familia y el verano', 'Sea-Doo GTI 130 y GTI SE 170, o Kawasaki STX 160: tres plazas, estables y cómodas para dar vueltas cerca de la costa.'),
       ('Para hacer millas en pareja', 'Sea-Doo GTX 170 y GTX 230, o Kawasaki Ultra 160LX: más asiento, más estabilidad y más capacidad de depósito.'),
       ('Lo más cómodo y potente', 'Sea-Doo GTX Limited 350 y Kawasaki Ultra 310LX: el equipamiento más completo de cada marca para quien sale a menudo y lejos.'),
       ('Deportivas', 'Sea-Doo RXP-X 350 y RXT-X 350, Kawasaki STX 310R: pensadas para acelerar y girar fuerte. No son las más cómodas para pasear.'),
       ('Esquí, wake, pesca y travesía', 'Sea-Doo Wake 170 y Wake Pro 230 o Kawasaki Ultra 160LX-S Wakesport para tirar; Fish Pro Trophy 170 para pescar; Explorer Pro 230 para rutas largas.')],
  sell_h='¿Quieres vender tu moto de agua?',
  sell='Tengas una Sea-Doo, una Kawasaki, una Yamaha u otra marca: te la gestiono o te la compro, según el modelo, el año y el estado. Mándame fotos y las horas y te digo cómo lo vemos.',
  b_g='Que me la gestionéis', b_c='Que me hagáis una oferta',
  wa_g='Hola Juan, quiero vender mi moto de agua y que me gestionéis la venta.', wa_c='Hola Juan, quiero vender mi moto de agua y que me hagáis una oferta de compra.',
  faq2=[('¿Qué gastos hay además del precio de la moto?', 'La matriculación, el seguro de responsabilidad civil (obligatorio), el remolque si la vas a llevar tú, el mantenimiento anual y dónde guardarla. Te lo detallo en el presupuesto para que no haya sorpresas. Si necesitas remolque, mira los <a href="/remolques/">remolques Goliath</a>.'),
        ('¿Sois concesionario oficial?', 'No. Te ayudo a elegir y gestiono el pedido con un concesionario oficial de la marca. En el presupuesto por escrito consta quién factura y entrega la moto, y la garantía es la del fabricante.')]),
 'ca': dict(
  uso_h="Quina moto d'aigua comprar segons l'ús?",
  uso=[('Per començar o sortir de tant en tant', 'Sea-Doo Spark i Spark X: lleugeres, fàcils de portar i de remolcar. Si busques alguna cosa més juganera, la Spark Trixx.'),
       ("Per a la família i l'estiu", 'Sea-Doo GTI 130 i GTI SE 170, o Kawasaki STX 160: tres places, estables i còmodes per voltar a prop de la costa.'),
       ('Per fer milles en parella', 'Sea-Doo GTX 170 i GTX 230, o Kawasaki Ultra 160LX: més seient, més estabilitat i més capacitat de dipòsit.'),
       ('El més còmode i potent', "Sea-Doo GTX Limited 350 i Kawasaki Ultra 310LX: l'equipament més complet de cada marca per a qui surt sovint i lluny."),
       ('Esportives', 'Sea-Doo RXP-X 350 i RXT-X 350, Kawasaki STX 310R: pensades per accelerar i girar fort. No són les més còmodes per passejar.'),
       ('Esquí, wake, pesca i travessia', 'Sea-Doo Wake 170 i Wake Pro 230 o Kawasaki Ultra 160LX-S Wakesport per arrossegar; Fish Pro Trophy 170 per pescar; Explorer Pro 230 per a rutes llargues.')],
  sell_h="Vols vendre la teva moto d'aigua?",
  sell="Tant si tens una Sea-Doo, una Kawasaki, una Yamaha o una altra marca: te la gestiono o te la compro, segons el model, l'any i l'estat. Envia'm fotos i les hores i et dic com ho veiem.",
  b_g="Que me la gestioneu", b_c="Que em feu una oferta",
  wa_g="Hola Juan, vull vendre la meva moto d'aigua i que me'n gestioneu la venda.", wa_c="Hola Juan, vull vendre la meva moto d'aigua i que em feu una oferta de compra.",
  faq2=[('Quines despeses hi ha a més del preu de la moto?', 'La matriculació, l\'assegurança de responsabilitat civil (obligatòria), el remolc si la portaràs tu, el manteniment anual i on guardar-la. T\'ho detallo al pressupost perquè no hi hagi sorpreses. Si necessites remolc, mira els <a href="/ca/remolques/">remolcs Goliath</a>.'),
        ('Sou concessionari oficial?', 'No. T\'ajudo a triar i gestiono la comanda amb un concessionari oficial de la marca. Al pressupost per escrit hi consta qui factura i lliura la moto, i la garantia és la del fabricant.')]),
 'en': dict(
  uso_h='Which jet ski should you buy for your use?',
  uso=[('To get started or ride now and then', 'Sea-Doo Spark and Spark X: light and easy to ride and tow. If you want something more playful, the Spark Trixx.'),
       ('For the family and summer', 'Sea-Doo GTI 130 and GTI SE 170, or Kawasaki STX 160: three seats, stable and comfortable for rides near the coast.'),
       ('For long rides two-up', 'Sea-Doo GTX 170 and GTX 230, or Kawasaki Ultra 160LX: bigger seat, more stability and a larger fuel tank.'),
       ('Maximum comfort and power', "Sea-Doo GTX Limited 350 and Kawasaki Ultra 310LX: each brand's most complete equipment for those who ride often and far."),
       ('Sporty', 'Sea-Doo RXP-X 350 and RXT-X 350, Kawasaki STX 310R: built to accelerate and turn hard. Not the most comfortable for cruising.'),
       ('Skiing, wake, fishing and touring', 'Sea-Doo Wake 170 and Wake Pro 230 or Kawasaki Ultra 160LX-S Wakesport for towing; Fish Pro Trophy 170 for fishing; Explorer Pro 230 for long trips.')],
  sell_h='Want to sell your jet ski?',
  sell='Whether it is a Sea-Doo, a Kawasaki, a Yamaha or another brand: I can sell it for you or buy it from you, depending on model, year and condition. Send me photos and the engine hours and I will tell you what we think.',
  b_g='Sell it for me', b_c='Make me an offer',
  wa_g="Hi Juan, I'd like to sell my jet ski and have you handle the sale.", wa_c="Hi Juan, I'd like to sell my jet ski and get a purchase offer from you.",
  faq2=[('What costs are there besides the price?', 'Registration, third-party liability insurance (mandatory), a trailer if you will tow it yourself, yearly servicing and storage. I detail it in the quote so there are no surprises. If you need a trailer, see the <a href="/en/remolques/">Goliath trailers</a>.'),
        ('Are you an official dealer?', 'No. I help you choose and handle the order with an official dealer of the brand. The written quote states who invoices and delivers the jet ski, and the warranty is the manufacturer\'s.')]),
 'fr': dict(
  uso_h='Quel jet-ski acheter selon votre usage ?',
  uso=[('Pour débuter ou sortir de temps en temps', 'Sea-Doo Spark et Spark X : légers, faciles à piloter et à remorquer. Pour plus de jeu, le Spark Trixx.'),
       ("Pour la famille et l'été", 'Sea-Doo GTI 130 et GTI SE 170, ou Kawasaki STX 160 : trois places, stables et confortables pour se balader près de la côte.'),
       ('Pour faire des milles à deux', 'Sea-Doo GTX 170 et GTX 230, ou Kawasaki Ultra 160LX : selle plus grande, plus de stabilité et plus grand réservoir.'),
       ('Le plus confortable et puissant', "Sea-Doo GTX Limited 350 et Kawasaki Ultra 310LX : l'équipement le plus complet de chaque marque pour qui sort souvent et loin."),
       ('Sportifs', 'Sea-Doo RXP-X 350 et RXT-X 350, Kawasaki STX 310R : faits pour accélérer et virer fort. Pas les plus confortables pour se balader.'),
       ('Ski, wake, pêche et randonnée', 'Sea-Doo Wake 170 et Wake Pro 230 ou Kawasaki Ultra 160LX-S Wakesport pour tracter ; Fish Pro Trophy 170 pour pêcher ; Explorer Pro 230 pour les longues sorties.')],
  sell_h='Vous voulez vendre votre jet-ski ?',
  sell="Sea-Doo, Kawasaki, Yamaha ou autre marque : je m'occupe de la vente ou je vous l'achète, selon le modèle, l'année et l'état. Envoyez-moi des photos et les heures moteur et je vous dis ce qu'on en pense.",
  b_g='Que vous gériez la vente', b_c='Recevoir une offre',
  wa_g="Bonjour Juan, je voudrais vendre mon jet-ski et que vous gériez la vente.", wa_c="Bonjour Juan, je voudrais vendre mon jet-ski et recevoir une offre d'achat.",
  faq2=[('Quels frais en plus du prix ?', 'L\'immatriculation, l\'assurance responsabilité civile (obligatoire), une remorque si vous le transportez vous-même, l\'entretien annuel et le stockage. Je le détaille dans le devis pour éviter les surprises. Pour une remorque, voir les <a href="/fr/remolques/">remorques Goliath</a>.'),
        ('Êtes-vous concessionnaire officiel ?', 'Non. Je vous aide à choisir et je gère la commande avec un concessionnaire officiel de la marque. Le devis écrit indique qui facture et livre le jet-ski, et la garantie est celle du fabricant.')]),
}

ADD = {'es': {'note': 'Precio a consultar: te paso el presupuesto por escrito con la versión, el equipamiento, los impuestos, el transporte y el plazo de entrega.', 'fil_l': 'Filtrar motos', 'fil': [('all', 'Todas'), ('sea-doo', 'Sea-Doo'), ('kawasaki', 'Kawasaki'), ('ini', 'Para empezar'), ('fam', 'Familia'), ('trav', 'Travesía'), ('dep', 'Deportivas'), ('agua', 'Pesca y arrastre'), ('pie', 'De pie')], 'vs_h': 'Sea-Doo o Kawasaki: modelos que se comparan', 'vs_p': 'Si dudas entre las dos marcas, estos son los modelos que suelen compararse. Las diferencias de equipamiento y precio te las detallo en el presupuesto.', 'vs': [('Familia', 'Sea-Doo GTI SE 170', '170 cv · 3 plazas', 'Kawasaki STX 160LX', '152 cv · 3 plazas'), ('Travesía', 'Sea-Doo GTX 230', '230 cv · 3 plazas', 'Kawasaki Ultra 160LX', '152 cv · 3 plazas'), ('Lo más completo', 'Sea-Doo GTX Limited 350', '350 cv · 3 plazas', 'Kawasaki Ultra 310LX', '300 cv · 3 plazas'), ('Deportivas', 'Sea-Doo RXT-X 350', '350 cv · 3 plazas', 'Kawasaki STX 310RX', '300 CV · 3 plazas')]}, 'ca': {'note': "Preu a consultar: et passo el pressupost per escrit amb la versió, l'equipament, els impostos, el transport i el termini de lliurament.", 'fil_l': 'Filtrar motos', 'fil': [('all', 'Totes'), ('sea-doo', 'Sea-Doo'), ('kawasaki', 'Kawasaki'), ('ini', 'Per començar'), ('fam', 'Família'), ('trav', 'Travessia'), ('dep', 'Esportives'), ('agua', 'Pesca i arrossegament'), ('pie', 'Dempeus')], 'vs_h': 'Sea-Doo o Kawasaki: models que es comparen', 'vs_p': "Si dubtes entre les dues marques, aquests són els models que se solen comparar. Les diferències d'equipament i preu te les detallo al pressupost.", 'vs': [('Família', 'Sea-Doo GTI SE 170', '170 cv · 3 places', 'Kawasaki STX 160LX', '152 cv · 3 places'), ('Travessia', 'Sea-Doo GTX 230', '230 cv · 3 places', 'Kawasaki Ultra 160LX', '152 cv · 3 places'), ('El més complet', 'Sea-Doo GTX Limited 350', '350 cv · 3 places', 'Kawasaki Ultra 310LX', '300 cv · 3 places'), ('Esportives', 'Sea-Doo RXT-X 350', '350 cv · 3 places', 'Kawasaki STX 310RX', '300 CV · 3 places')]}, 'en': {'note': 'Price on request: I send you a written quote with version, equipment, taxes, transport and delivery time.', 'fil_l': 'Filter jet skis', 'fil': [('all', 'All'), ('sea-doo', 'Sea-Doo'), ('kawasaki', 'Kawasaki'), ('ini', 'Beginners'), ('fam', 'Family'), ('trav', 'Touring'), ('dep', 'Sporty'), ('agua', 'Fishing & towing'), ('pie', 'Stand-up')], 'vs_h': 'Sea-Doo or Kawasaki: models people compare', 'vs_p': 'If you are torn between the two brands, these are the models usually compared. I detail equipment and price differences in the quote.', 'vs': [('Family', 'Sea-Doo GTI SE 170', '170 hp · 3 seats', 'Kawasaki STX 160LX', '152 hp · 3 seats'), ('Touring', 'Sea-Doo GTX 230', '230 hp · 3 seats', 'Kawasaki Ultra 160LX', '152 hp · 3 seats'), ('Top of the range', 'Sea-Doo GTX Limited 350', '350 hp · 3 seats', 'Kawasaki Ultra 310LX', '300 hp · 3 seats'), ('Sporty', 'Sea-Doo RXT-X 350', '350 hp · 3 seats', 'Kawasaki STX 310RX', '300 PS · 3 seats')]}, 'fr': {'note': 'Prix sur demande : je vous envoie un devis écrit avec la version, l’équipement, les taxes, le transport et le délai de livraison.', 'fil_l': 'Filtrer les jet-skis', 'fil': [('all', 'Tous'), ('sea-doo', 'Sea-Doo'), ('kawasaki', 'Kawasaki'), ('ini', 'Pour débuter'), ('fam', 'Famille'), ('trav', 'Randonnée'), ('dep', 'Sportifs'), ('agua', 'Pêche et traction'), ('pie', 'Debout')], 'vs_h': 'Sea-Doo ou Kawasaki : modèles comparables', 'vs_p': 'Si vous hésitez entre les deux marques, voici les modèles souvent comparés. Je détaille les différences d’équipement et de prix dans le devis.', 'vs': [('Famille', 'Sea-Doo GTI SE 170', '170 ch · 3 places', 'Kawasaki STX 160LX', '152 ch · 3 places'), ('Randonnée', 'Sea-Doo GTX 230', '230 ch · 3 places', 'Kawasaki Ultra 160LX', '152 ch · 3 places'), ('Le plus complet', 'Sea-Doo GTX Limited 350', '350 ch · 3 places', 'Kawasaki Ultra 310LX', '300 ch · 3 places'), ('Sportifs', 'Sea-Doo RXT-X 350', '350 ch · 3 places', 'Kawasaki STX 310RX', '300 ch · 3 places')]}}
for _l in ADD: X[_l].update(ADD[_l])

# --- Precios "desde" (PVP recomendado del fabricante, gama 2027; fuente: tarifa publicada por el concesionario oficial, nov 2026) ---
PRICE = {'sd-rxp-x-senna': 39899, 'sd-rxp-x-350-solar-orange': 34799, 'sd-rxt-x-350-solar-orange': 34599, 'sd-gtx-limited': 36099,
 'sd-gtx-230': 26899, 'sd-gtx': 24099, 'sd-fishpro-trophy': 31699, 'sd-explorer-pro': 28999, 'sd-wake-pro-230': 27799, 'sd-wake-170': 22299,
 'sd-gti-se-teal-blue': 19999, 'sd-gti': 17099, 'sd-trixx-for3-blue-mist': 16499, 'sd-spark-x': 15999, 'sd-spark': 9899,
 'kw-ultra-310lx-2027': 30725, 'kw-ultra-310lx-s-2027': 28690, 'kw-ultra-160lx-s-wakesport': 25375, 'kw-ultra-160lx-2027': 24425, 'kw-ultra-160lx-s-2027': 23725,
 'kw-stx-310rx': 24350, 'kw-stx-310r': 22850, 'kw-stx-160lx-2027': 21975, 'kw-stx-160lx-s-2027': 20450, 'kw-stx-160r-2027': 20450, 'kw-stx-160x-2027': 19175,
 'kw-sx-r-160': 14175, 'kw-sx-x-160': 14175}
FICHA = {'sd-spark': 'sea-doo-spark', 'sd-gtx': 'sea-doo-gtx-170', 'kw-ultra-310lx-2027': 'kawasaki-ultra-310lx'}
import motos_agua_modelos as _MM
FICHA.update({r[0]: r[1] for r in _MM.SD + _MM.KW})


def money(n, lang):
    if lang == 'en': return f'€{n:,}'
    if lang == 'fr': return f'{n:,}'.replace(',', ' ') + ' €'
    return f'{n:,}'.replace(',', '.') + ' €'


INC = {'es': 'IVA y matriculación incluidos', 'ca': 'IVA i matriculació inclosos', 'en': 'VAT and registration tax included', 'fr': 'TVA et immatriculation incluses'}
OK3 = {'es': ['Te ayudo a elegir entre Sea-Doo y Kawasaki', 'Precio final cerrado, sin sorpresas', 'Te acompaño hasta la entrega'],
 'ca': ['T\'ajudo a triar entre Sea-Doo i Kawasaki', 'Preu final tancat, sense sorpreses', 'T\'acompanyo fins al lliurament'],
 'en': ['I help you choose between Sea-Doo and Kawasaki', 'Final closed price, no surprises', 'I am with you until delivery'],
 'fr': ['Je vous aide à choisir entre Sea-Doo et Kawasaki', 'Prix final ferme, sans surprise', 'Je vous accompagne jusqu\'à la livraison']}
ALLM = {'es': 'Ver los {n} modelos', 'ca': 'Veure els {n} models', 'en': 'See all {n} models', 'fr': 'Voir les {n} modèles'}
FROM = {'es': 'Desde {p}', 'ca': 'Des de {p}', 'en': 'From {p}', 'fr': 'À partir de {p}'}
FICHA_T = {'es': 'Ver ficha', 'ca': 'Veure fitxa', 'en': 'See specs', 'fr': 'Voir la fiche'}
CMP = {'es': ('Comparar', 'Comparar ({n}/3)', 'Quitar', 'Precio desde', 'Potencia', 'Plazas', 'Marca', 'Cerrar', 'Elige hasta 3 motos con «Comparar» para verlas lado a lado.'),
       'ca': ('Comparar', 'Comparar ({n}/3)', 'Treure', 'Preu des de', 'Potència', 'Places', 'Marca', 'Tancar', 'Tria fins a 3 motos amb «Comparar» per veure-les una al costat de l’altra.'),
       'en': ('Compare', 'Compare ({n}/3)', 'Remove', 'Price from', 'Power', 'Seats', 'Brand', 'Close', 'Pick up to 3 jet skis with “Compare” to see them side by side.'),
       'fr': ('Comparer', 'Comparer ({n}/3)', 'Retirer', 'Prix dès', 'Puissance', 'Places', 'Marque', 'Fermer', 'Choisissez jusqu’à 3 jet-skis avec « Comparer » pour les voir côte à côte.')}

T['es'].update(title='Motos de agua nuevas 2027: Sea-Doo y Kawasaki desde 9.899 €',
  desc='Motos de agua nuevas Sea-Doo y Kawasaki 2027 desde 9.899 €: Spark, GTI, GTX, RXP-X, Ultra, STX y SX-R. Compara modelos y pide presupuesto por WhatsApp.',
  small='Precios «desde»: PVP recomendado por cada fabricante para la versión de entrada de cada modelo, con IVA e impuesto de matriculación; pueden variar según la comunidad autónoma, la versión, el color y los extras. Modelos y datos de la gama 2027, que pueden cambiar sin aviso. El precio final, la disponibilidad y el plazo de entrega se confirman por escrito. Información orientativa: podemos equivocarnos y no es vinculante.')
T['es']['faq'][0] = ('¿El precio que veo es el final?', 'Es el precio «desde»: el PVP recomendado por el fabricante para la versión de entrada, con IVA e impuesto de matriculación. Según la versión, el color, los extras y tu comunidad autónoma puede variar, así que te paso el presupuesto cerrado por escrito, detallando qué incluye.')
T['ca'].update(title="Motos d'aigua noves 2027: Sea-Doo i Kawasaki des de 9.899 €",
  desc="Motos d'aigua noves Sea-Doo i Kawasaki 2027 des de 9.899 €: Spark, GTI, GTX, RXP-X, Ultra, STX i SX-R. Compara models i demana pressupost per WhatsApp.",
  small="Preus «des de»: PVP recomanat per cada fabricant per a la versió d'entrada de cada model, amb IVA i impost de matriculació; poden variar segons la comunitat autònoma, la versió, el color i els extres. Models i dades de la gamma 2027, que poden canviar sense avís. El preu final, la disponibilitat i el termini de lliurament es confirmen per escrit. Informació orientativa: ens podem equivocar i no és vinculant.")
T['ca']['faq'][0] = ('El preu que veig és el final?', "És el preu «des de»: el PVP recomanat pel fabricant per a la versió d'entrada, amb IVA i impost de matriculació. Segons la versió, el color, els extres i la teva comunitat autònoma pot variar, així que et passo el pressupost tancat per escrit, detallant què inclou.")
T['en'].update(title='New 2027 Sea-Doo and Kawasaki jet skis from €9,899',
  desc='New 2027 Sea-Doo and Kawasaki jet skis from €9,899: Spark, GTI, GTX, RXP-X, Ultra, STX and SX-R. Compare models and ask for a quote on WhatsApp in Barcelona.',
  small="“From” prices: each manufacturer's recommended retail price for the entry version of each model, including Spanish VAT and registration tax; they may vary by region, version, colour and extras. Models and data from the 2027 range, which may change without notice. Final price, availability and delivery time are confirmed in writing. Indicative information: we may be wrong and it is not binding.")
T['en']['faq'][0] = ('Is the price shown the final price?', "It is the “from” price: the manufacturer's recommended retail price for the entry version, including Spanish VAT and registration tax. It can change with version, colour, extras and region, so I send you a closed written quote detailing what it includes.")
T['fr'].update(title='Jet-skis neufs 2027 Sea-Doo et Kawasaki dès 9 899 €',
  desc='Jet-skis neufs Sea-Doo et Kawasaki 2027 à partir de 9 899 € : Spark, GTI, GTX, RXP-X, Ultra, STX et SX-R. Comparez et demandez un devis par WhatsApp.',
  small="Prix « à partir de » : prix de vente conseillé par chaque fabricant pour la version d’entrée de chaque modèle, TVA espagnole et taxe d’immatriculation incluses ; ils peuvent varier selon la région, la version, la couleur et les options. Modèles et données de la gamme 2027, susceptibles de changer sans préavis. Le prix final, la disponibilité et le délai de livraison sont confirmés par écrit. Information indicative : nous pouvons nous tromper et elle n’est pas contractuelle. Nous ne parlons pas français : nous utilisons un traducteur.")
T['fr']['faq'][0] = ('Le prix affiché est-il le prix final ?', "C’est le prix « à partir de » : le prix conseillé par le fabricant pour la version d’entrée, TVA espagnole et taxe d’immatriculation incluses. Il peut varier selon la version, la couleur, les options et la région ; je vous envoie donc un devis ferme par écrit, en détaillant ce qui est inclus.")
X['es']['note'] = 'Precios «desde» con IVA e impuesto de matriculación. Te paso el presupuesto cerrado por escrito: versión, equipamiento, transporte y plazo de entrega.'
X['ca']['note'] = "Preus «des de» amb IVA i impost de matriculació. Et passo el pressupost tancat per escrit: versió, equipament, transport i termini de lliurament."
X['en']['note'] = '“From” prices include Spanish VAT and registration tax. I send you a closed written quote: version, equipment, transport and delivery time.'
X['fr']['note'] = 'Prix « à partir de » TVA espagnole et taxe d’immatriculation incluses. Je vous envoie un devis ferme par écrit : version, équipement, transport et délai de livraison.'
for _l in X:
    X[_l]['vs'] = [tuple(v) for v in X[_l]['vs']]

def vsp(name, lang):
    for brand, fams in (('Sea-Doo', SEADOO), ('Kawasaki', KAWA)):
        for _, ms in fams:
            for k, m, _, _ in ms:
                if f'{brand} {m}' == name: return FROM[lang].format(p=money(PRICE[k], lang))
    return ''

JS = '''<script>(function(){var bar=document.querySelector('.mj-bar'),dlg=document.querySelector('.mj-dlg');if(!bar)return;var cbs=document.querySelectorAll('.mj-cmp input');function sel(){return [].filter.call(cbs,function(c){return c.checked})}function upd(){var s=sel();cbs.forEach(function(c){c.disabled=!c.checked&&s.length>=3});bar.hidden=!s.length;bar.querySelector('span').textContent=bar.querySelector('span').getAttribute('data-t').replace('{n}',s.length)}cbs.forEach(function(c){c.addEventListener('change',upd)});bar.querySelector('.mj-clr').addEventListener('click',function(){cbs.forEach(function(c){c.checked=false});upd()});bar.querySelector('.mj-go').addEventListener('click',function(){var h='';sel().forEach(function(c){h+='<div><img src="'+c.getAttribute('data-img')+'" alt=""><b>'+c.getAttribute('data-cmp')+'</b><p class="pr">'+c.getAttribute('data-p')+'</p><p>'+c.getAttribute('data-cv')+'</p></div>'});dlg.querySelector('.mj-cols').innerHTML=h;dlg.hidden=false});dlg.addEventListener('click',function(e){if(e.target===dlg||e.target.classList.contains('mj-x'))dlg.hidden=true});document.addEventListener('keydown',function(e){if(e.key==='Escape')dlg.hidden=true})})();</script><script>(function(){var bs=document.querySelectorAll('.mj-fil button');function go(f){bs.forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-f')===f?'true':'false')});document.querySelectorAll('.mj-c').forEach(function(c){var ok=f==='all'||c.getAttribute('data-use')===f||c.getAttribute('data-brand')===f;c.hidden=!ok});document.querySelectorAll('.mj-fam').forEach(function(m){m.hidden=!m.querySelector('.mj-c:not([hidden])')});document.querySelectorAll('#sea-doo,#kawasaki').forEach(function(sec){sec.hidden=!sec.querySelector('.mj-c:not([hidden])')})}bs.forEach(function(b){b.addEventListener('click',function(){go(b.getAttribute('data-f'))})})})();</script>'''

CSS = """<style>
.mj-brand{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin:0 0 6px}.mj-brand img{height:30px;width:auto;max-width:44%}.mj-brand img.sd{height:22px}
.mj-blogo{display:block;height:40px;width:auto;max-width:70%;margin:0 0 4px}.mj-blogo.sd{height:28px}
.rm img{max-width:100%}
.mj-jump{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.mj-fam{margin-top:26px}.mj-fam h3{font-size:1.2rem;margin:0 0 4px}.mj-fam>p{color:#33474f;margin:0 0 12px;max-width:70ch}
.mj-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.mj-c{display:flex;flex-direction:column;border:1px solid #e3e9ec;border-radius:14px;overflow:hidden;background:#fff}
.mj-c img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:contain;background:#fff;padding:8px}
.mj-c>div{padding:12px 14px 14px;display:flex;flex-direction:column;gap:4px;flex:1}
.mj-c h4{font-size:1.05rem;margin:0}.mj-c .sp{font-size:.9rem;color:#5b6b75;flex:1}.mj-c .pr{font-weight:700;font-size:.95rem}
.mj-c .btn{margin-top:8px;text-align:center;padding:9px 12px;font-size:.92rem}
.mj-c .mj-fl{font-weight:600;color:#0B766B;font-size:.9rem;text-decoration:none}.mj-cmp{display:flex;align-items:center;gap:6px;font-size:.85rem;color:#33474f;margin-top:4px;cursor:pointer}
.mj-bar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:60;background:#0E3042;color:#fff;border-radius:999px;padding:8px 10px 8px 18px;display:flex;align-items:center;gap:10px;box-shadow:0 10px 30px -10px rgba(0,0,0,.5);max-width:calc(100% - 32px)}.mj-bar[hidden],.mj-dlg[hidden]{display:none}.mj-bar .btn{padding:8px 14px}.mj-clr{background:none;border:0;color:#cfe;text-decoration:underline;cursor:pointer}
.mj-dlg{position:fixed;inset:0;z-index:80;background:rgba(6,15,22,.7);display:flex;align-items:center;justify-content:center;padding:16px}.mj-dlg-in{background:#fff;border-radius:16px;max-width:980px;width:100%;max-height:90vh;overflow:auto;padding:20px;position:relative}.mj-x{position:absolute;top:8px;right:12px;border:0;background:none;font-size:28px;cursor:pointer}.mj-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}.mj-cols img{width:100%;aspect-ratio:4/3;object-fit:contain}.mj-cols b{display:block;margin-top:6px}.mj-cols p{margin:4px 0;color:#33474f}
.mj-note{margin:8px 0 10px;font-weight:600;color:#0E3042}
.mj-fil{display:flex;flex-wrap:wrap;gap:8px;position:sticky;top:64px;z-index:5;background:#F4F6F7;padding:8px 0}.mj-fil button{font:600 .9rem/1 var(--display,inherit);padding:9px 14px;border-radius:999px;border:1px solid rgba(14,48,66,.25);background:#fff;color:#0E3042;cursor:pointer}.mj-fil button[aria-pressed="true"]{background:#0E3042;color:#fff;border-color:#0E3042}
.mj-c[hidden],.mj-fam[hidden],section[hidden]{display:none}
.mj-vs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:14px}.mj-vs>div{border:1px solid #e3e9ec;border-radius:14px;padding:14px 16px;background:#fff;display:grid;grid-template-columns:1fr auto 1fr;gap:6px 12px;align-items:center}.mj-vs .u{grid-column:1/-1;margin:0 0 4px;font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:#5b6b75}.mj-vs p{margin:0}.mj-vs b{display:block}.mj-vs span{font-size:.88rem;color:#5b6b75}.mj-vs .o{font-weight:700;color:#0B766B}
@media(max-width:820px){.mj-vs{grid-template-columns:1fr}.mj-fil{top:56px}}
.mj-bh{font-size:1.5rem;margin:10px 0 0}
.mj-uso{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:16px}.mj-uso>div{border:1px solid #e3e9ec;border-radius:14px;padding:16px;background:#fff}.mj-uso h3{font-size:1.02rem;margin:0 0 6px}.mj-uso p{margin:0;color:#33474f;line-height:1.5;font-size:.95rem}
.mj-sell{background:#fff;border-left:3px solid #0B766B;border-radius:0 14px 14px 0;padding:22px 24px;max-width:780px}.mj-sell h2{margin:0 0 8px}.mj-sell p{color:#33474f;line-height:1.6;margin:0 0 6px}
@media(max-width:820px){.mj-uso{grid-template-columns:1fr}}
.mj-hero-img{width:100%;height:auto;border-radius:14px;background:#fff}
@media(max-width:980px){.mj-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:720px){.mj-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:420px){.mj-c h4{font-size:.98rem}.mj-c>div{padding:10px}}

/* v2 diseño */
.mj-hero{background:radial-gradient(120% 140% at 75% 30%,#1d5470 0,#0E3042 55%,#081d29 100%);color:#fff;padding:22px 0 48px;margin-bottom:8px}
.mj-hin{display:grid;grid-template-columns:1.05fr 1fr;gap:28px;align-items:center}
.mj-crumb{font-size:.8rem;color:rgba(255,255,255,.65);margin:0 0 22px}.mj-crumb a{color:inherit}
.mj-hero .mj-brand img{filter:none;height:22px}.mj-hero .mj-brand img+img{height:32px}
.mj-hero h1{font-family:var(--display);font-weight:800;font-stretch:72%;text-transform:uppercase;font-size:clamp(2.3rem,5.4vw,4.1rem);line-height:.98;letter-spacing:-.005em;margin:14px 0 10px;color:#fff}
.mj-from{font-family:var(--display);font-weight:800;font-size:1.6rem;margin:0 0 12px;color:#7FE3D0}
.mj-hero .lead{color:rgba(255,255,255,.85);font-size:1.05rem;line-height:1.6;max-width:56ch;margin:0 0 10px}
.mj-tit{color:rgba(255,255,255,.75);font-size:.92rem;margin:0 0 20px}
.mj-hbt{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.mj-gh{color:#fff;font-family:var(--display);font-weight:600;font-size:.95rem;padding:11px 16px;border:1px solid rgba(255,255,255,.35);border-radius:999px;text-decoration:none}.mj-gh:hover{background:rgba(255,255,255,.1)}
.mj-himg{background:#fff;border-radius:22px;padding:18px;box-shadow:0 30px 60px -25px rgba(0,0,0,.6)}.mj-himg img{width:100%;height:auto;display:block}
.mj-wa{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:#25D366;color:#06281a;font-family:var(--display);font-weight:700;font-size:.98rem;padding:12px 18px;border-radius:999px;text-decoration:none;transition:filter .15s}.mj-wa:hover{filter:brightness(.95)}
.mj-note{font-size:.9rem;color:#33474f;font-weight:500;margin:18px 0 10px}
.mj-fil{background:transparent;padding:10px 0;backdrop-filter:blur(6px)}.mj-fil button{font-family:var(--display);text-transform:uppercase;letter-spacing:.04em;font-size:.78rem;font-weight:700;padding:9px 14px;background:#fff}
.mj-bhd{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin:6px 0 4px}.mj-bhd .mj-blogo{margin:0}
.mj-bh{font-family:var(--display);font-weight:800;font-stretch:72%;text-transform:uppercase;font-size:clamp(1.7rem,3.4vw,2.4rem);margin:0;line-height:1}
.mj-fam{margin-top:34px}.mj-fh{display:flex;align-items:center;gap:16px;margin-bottom:6px}.mj-fh h3{font-family:var(--display);font-weight:800;font-stretch:72%;text-transform:uppercase;font-size:1.45rem;margin:0;white-space:nowrap}.mj-fh span{flex:1;height:2px;background:linear-gradient(90deg,#7FE3D0,rgba(127,227,208,0))}
.mj-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.mj-c{border:0;border-radius:16px;background:#fff;box-shadow:0 1px 2px rgba(14,48,66,.06),0 12px 30px -18px rgba(14,48,66,.35);transition:transform .2s,box-shadow .2s}.mj-c:hover{transform:translateY(-3px);box-shadow:0 1px 2px rgba(14,48,66,.06),0 22px 40px -20px rgba(14,48,66,.45)}
.mj-ph{position:relative;background:#fff;border-radius:16px 16px 0 0;overflow:hidden}.mj-ph img{display:block;width:100%;aspect-ratio:4/3;object-fit:contain;padding:14px;background:none}
.mj-c .mj-cmp{position:absolute;top:10px;right:10px;margin:0;font-family:var(--display);font-weight:600;font-size:.78rem;color:#0E3042;background:#fff;border:1px solid rgba(14,48,66,.2);border-radius:999px;padding:5px 11px}.mj-cmp input{position:absolute;opacity:0;pointer-events:none}.mj-cmp:has(input:checked){background:#0E3042;color:#fff}.mj-cmp:has(input:disabled:not(:checked)){opacity:.4}
.mj-bd{padding:16px 18px 18px;display:flex;flex-direction:column;gap:4px;flex:1}
.mj-k{font-family:var(--display);font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#0B766B;margin:0}
.mj-c h4{font-family:var(--display);font-weight:800;font-stretch:72%;text-transform:uppercase;font-size:1.55rem;line-height:1.05;margin:2px 0 0}
.mj-c .sp{color:#5b6b75;font-size:.92rem;flex:1;margin:0}.mj-c .pr{font-family:var(--display);font-weight:800;font-size:1.2rem;margin:8px 0 12px;color:#0E3042}
.mj-c .mj-wa{width:100%}.mj-c .mj-fl{text-align:center;margin-top:10px;color:#0E3042;text-decoration:underline;font-weight:600;font-size:.9rem}
.mj-uso>div,.mj-vs>div{border:0;box-shadow:0 1px 2px rgba(14,48,66,.06),0 12px 30px -20px rgba(14,48,66,.35)}
.rm-sec h2{font-family:var(--display);font-weight:800;font-stretch:72%;text-transform:uppercase;letter-spacing:0}
.mj-sell{border-left-color:#25D366}.mj-sell .mj-jump a.btn-wa{background:#25D366;color:#06281a}
@media(max-width:900px){.mj-hin{grid-template-columns:1fr}.mj-himg{order:-1;max-width:340px;margin:0 auto}.mj-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.mj-grid{grid-template-columns:1fr}.mj-hero{padding-bottom:32px}.mj-fh h3{font-size:1.2rem}.mj-c h4{font-size:1.4rem}}
/* v3 */
.mj-hero h1{font-size:clamp(2.2rem,4.6vw,3.6rem)}
.mj-himg{background:radial-gradient(circle at 50% 42%,#fff 0,#e8eff3 55%,#c9d7df 100%);border-radius:28px;padding:14px}.mj-himg img{mix-blend-mode:multiply}
.mj-ok{list-style:none;padding:0;margin:0 0 20px;display:grid;gap:7px;color:#fff;font-size:.97rem}.mj-ok li{display:flex;gap:9px;align-items:center}.mj-ok li:before{content:"";flex:0 0 18px;height:18px;border-radius:50%;background:#7FE3D0 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z' fill='%230E3042'/%3E%3C/svg%3E") center/13px no-repeat}
.mj-wa{white-space:nowrap}.mf-tx .mj-hbt{flex-wrap:wrap}.mj-hbt{flex-wrap:nowrap}.mj-hbt .mj-wa{padding:13px 22px;font-size:1.02rem}
.mj-c .sp{flex:0 0 auto;font-size:.95rem}.mj-c .pr{margin:auto 0 0;padding-top:12px;font-size:1.45rem;line-height:1.1}.mj-c .pr small{display:block;font-family:var(--body,inherit);font-weight:400;font-size:.76rem;color:#5b6b75;margin-top:3px}
.mj-c .mj-wa{margin-top:14px;min-height:48px;border-radius:12px}
.mj-c .mj-cmp{min-height:34px;padding:7px 13px;font-size:.82rem;display:inline-flex;align-items:center}
.mj-grid{gap:20px}.rm-grid>*{min-width:0;overflow-wrap:break-word}
@media(max-width:560px){.mj-fh h3{white-space:normal;line-height:1.05}.mj-ph img{aspect-ratio:auto;height:215px;padding:10px}.mj-bd{padding:14px 16px 16px}.mj-hbt{flex-wrap:wrap}.mj-hbt .mj-wa{flex:1 1 100%}.mj-hero h1{font-size:2.05rem}}
/* v4 foto */
.mj-photo{position:relative;overflow:hidden;padding:40px 0 64px;min-height:600px;display:flex;align-items:center}.mj-photo .mj-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:68% 50%;z-index:0}
.mj-photo:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,rgba(8,29,41,.94) 0,rgba(8,29,41,.82) 38%,rgba(8,29,41,.25) 68%,rgba(8,29,41,0) 100%)}
.mj-photo .mj-hin{position:relative;z-index:2;grid-template-columns:minmax(0,620px);width:100%}
@media(max-width:900px){.mj-photo{min-height:0;padding:16px 0 36px;background:#0b2433}.mj-photo:before{background:linear-gradient(180deg,rgba(8,29,41,.25) 0,rgba(8,29,41,.1) 150px,rgba(8,29,41,.85) 270px,#0b2433 330px)}.mj-photo .mj-bg{object-position:58% 50%;height:330px;bottom:auto}.mj-photo .mj-htx{padding-top:215px}}
</style>"""


def wa(text):
    return 'https://wa.me/34633742973?text=' + quote(text, safe='')


USE = {'sd-spark':'ini','sd-spark-x':'ini','sd-trixx-for3-blue-mist':'ini','sd-gti':'fam','sd-gti-se-teal-blue':'fam',
 'sd-gtx':'trav','sd-gtx-230':'trav','sd-gtx-limited':'trav','sd-explorer-pro':'trav','sd-rxp-x-350-solar-orange':'dep','sd-rxp-x-senna':'dep',
 'sd-rxt-x-350-solar-orange':'dep','sd-fishpro-trophy':'agua','sd-wake-170':'agua','sd-wake-pro-230':'agua',
 'kw-ultra-310lx-2027':'trav','kw-ultra-310lx-s-2027':'trav','kw-ultra-160lx-2027':'trav','kw-ultra-160lx-s-2027':'trav','kw-ultra-160lx-s-wakesport':'agua',
 'kw-stx-310rx':'dep','kw-stx-310r':'dep','kw-stx-160lx-2027':'fam','kw-stx-160lx-s-2027':'fam','kw-stx-160r-2027':'fam','kw-stx-160x-2027':'fam',
 'kw-sx-r-160':'pie','kw-sx-x-160':'pie'}


WAI = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3a.5.5 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4 5.2 5.2 0 0 0 3.2.7 2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'


def card(t, key, name, brand, cv, seats, fk=''):
    full = f'{brand} {name}'
    sp = []
    if cv: sp.append(f'{cv} {t["cv"]}')
    if seats == 0: sp.append(t['stand'])
    elif seats: sp.append(t['seats'].format(n=seats))
    e = html.escape
    L = LANG[0]
    price = FROM[L].format(p=money(PRICE[key], L))
    fam = t['fam'][fk][0] if fk else ''
    href = (f'{PFX[L]}/{SLUG}/{FICHA[key]}' + ('' if key in _MM.SLUGS and key not in _MM.OLD else '/')) if key in FICHA else ''
    img = f'<img src="/{SLUG}/fotos/{key}.jpg" alt="{e(full)}" width="900" height="675" loading="lazy">'
    return (f'<article class="mj-c" data-use="{USE[key]}" data-brand="{brand.lower()}">'
            f'<div class="mj-ph">' + (f'<a href="{href}" tabindex="-1" aria-hidden="true">{img}</a>' if href else img) +
            f'<label class="mj-cmp"><input type="checkbox" data-cmp="{e(full)}" data-p="{e(price)}" data-cv="{e(" · ".join(sp))}" data-img="/{SLUG}/fotos/{key}.jpg"><span>+ {CMP[L][0]}</span></label></div>'
            f'<div class="mj-bd"><p class="mj-k">{e(brand)} {e(fam)} · 2027</p><h4>{e(name)}</h4><p class="sp">{" · ".join(sp)}</p><p class="pr">{price}<small>{INC[L]}</small></p>'
            f'<a class="mj-wa" href="{e(wa(t["wa"].format(m=full)))}" target="_blank" rel="noopener" data-wa-context="moto_agua_nueva">{WAI}{t["btn"]}</a>'
            + (f'<a class="mj-fl" href="{href}">{FICHA_T[L]}</a>' if href else '') + '</div></article>')


def brand_sec(t, bid, brand, logo, fams):
    out = [f'<section class="rm-sec" id="{bid}"><div class="wrap"><div class="mj-bhd"><img class="mj-blogo{' sd' if bid=='sea-doo' else ''}" src="/barcos-nuevos/logos/{logo}" alt="{brand}"><h2 class="mj-bh">{t['gama'].format(b=brand)}</h2></div>']
    for fk, models in fams:
        n, d = t['fam'][fk]
        out.append(f'<div class="mj-fam"><div class="mj-fh"><h3>{brand} {n}</h3><span></span></div><p>{d}</p><div class="mj-grid">' +
                   ''.join(card(t, k, m, brand, cv, s, fk) for k, m, cv, s in models) + '</div></div>')
    out.append('</div></section>')
    return ''.join(out)


LANG = ['es']


def build(lang):
    LANG[0] = lang
    t = T[lang]; p = PFX[lang]
    src = open(os.path.join(ROOT, p.lstrip('/'), 'remolques', 'index.html'), encoding='utf-8').read()
    head_top = src[:src.index('<title>')]
    after_ld = src[src.index('<style>'):src.index('</head>')]
    body_top = src[src.index('</head>'):src.index('<main')].replace('/remolques/', f'/{SLUG}/')
    foot = src[src.index('</main>'):]
    url = f'{BASE}{p}/{SLUG}/'
    e = html.escape
    alt = ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{PFX[l]}/{SLUG}/">\n' for l in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{BASE}/{SLUG}/">\n'
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f'{BASE}{p}/'},
        {"@type": "ListItem", "position": 2, "name": t['nb'], "item": f'{BASE}{p}/barcos-nuevos/'},
        {"@type": "ListItem", "position": 3, "name": t['crumb'], "item": url}]}
    items, i = [], 0
    for brand, fams in (('Sea-Doo', SEADOO), ('Kawasaki', KAWA)):
        for _, ms in fams:
            for _, m, _, _ in ms:
                i += 1; items.append({"@type": "ListItem", "position": i, "name": f'{brand} {m}'})
    ilist = {"@context": "https://schema.org", "@type": "ItemList", "name": t['list_name'], "numberOfItems": i, "itemListElement": items}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in t['faq']+X[lang]['faq2']]}
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (crumbs, ilist, faq))
    head = (head_top + f'<title>{e(t["title"])}</title>\n<meta name="description" content="{e(t["desc"])}">\n'
            f'<link rel="canonical" href="{url}">\n{alt}'
            f'<meta property="og:title" content="{e(t["title"])}">\n<meta property="og:description" content="{e(t["desc"])}">\n'
            f'<meta property="og:type" content="website">\n<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{BASE}/{SLUG}/fotos/sd-gtx-limited.jpg">\n<meta name="twitter:card" content="summary_large_image">\n'
            '<link rel="icon" type="image/png" href="/logo-plata-marine.png">\n<link rel="stylesheet" href="/barcos/barcos.css">\n'
            '<script src="/consent.js?v=20261006" defer></script>\n<script src="/analytics.js?v=20261006" defer></script>\n'
            '<link rel="stylesheet" href="/nav.css?v=20261019">\n' + ld + after_ld + CSS + '\n')
    main = ['<main class="rm">',
            f'<section class="mj-hero mj-photo"><img class="mj-bg" src="/{SLUG}/fotos/g-sd-gtx-limited-4.jpg" alt="" fetchpriority="high"><div class="wrap mj-hin"><div class="mj-htx"><p class="mj-crumb"><a href="{p}/">{t["home"]}</a> · <a href="{p}/barcos-nuevos/">{t["nb"]}</a> · {t["crumb"]}</p>'
            f'<div class="mj-brand"><img class="sd" src="/barcos-nuevos/logos/sea-doo-blanco.png" alt="Sea-Doo" width="900" height="97"><img src="/barcos-nuevos/logos/kawasaki-blanco.png" alt="Kawasaki" width="319" height="88"></div>'
            f'<h1>{t["h1"]}</h1><p class="mj-from">{FROM[lang].format(p=money(9899, lang))}</p><p class="lead">{t["lead"]}</p><ul class="mj-ok">' + ''.join(f'<li>{x}</li>' for x in OK3[lang]) + f'</ul><p class="mj-tit">{t["tit"]}</p>'
            f'<div class="mj-hbt"><a class="mj-wa" href="{e(wa(t["wa_gen"]))}" target="_blank" rel="noopener" data-wa-context="moto_agua_nueva">{WAI}{t["btn"]}</a>'
            f'<a class="mj-gh" href="#catalogo">{ALLM[lang].format(n=i)}</a></div></div>'
            '</div></section>',
            f'<div class="wrap" id="catalogo"><p class="mj-note">{X[lang]["note"]}</p><div class="mj-fil" role="group" aria-label="{X[lang]["fil_l"]}">' +
            ''.join(f'<button type="button" data-f="{k}"{" aria-pressed=\"true\"" if k=="all" else " aria-pressed=\"false\""}>{v}</button>' for k, v in X[lang]['fil']) + '</div></div>',
            f'<div class="mj-bar" hidden><span data-t="{CMP[lang][1]}"></span><button type="button" class="btn btn-wa mj-go">{CMP[lang][0]}</button><button type="button" class="mj-clr">{CMP[lang][2]}</button></div>'
            f'<div class="mj-dlg" hidden role="dialog" aria-modal="true"><div class="mj-dlg-in"><button type="button" class="mj-x" aria-label="{CMP[lang][7]}">×</button><div class="mj-cols"></div></div></div>',
            brand_sec(t, 'sea-doo', 'Sea-Doo', 'sea-doo.png', SEADOO),
            brand_sec(t, 'kawasaki', 'Kawasaki', 'kawasaki.png', KAWA),
            f'<section class="rm-sec" id="comparar"><div class="wrap"><h2>{X[lang]["vs_h"]}</h2><p>{X[lang]["vs_p"]}</p><div class="mj-vs">' +
            ''.join(f'<div><p class="u">{u}</p><p><b>{a}</b><span>{ad}<br>{vsp(a, lang)}</span></p><p class="o">vs</p><p><b>{b}</b><span>{bd}<br>{vsp(b, lang)}</span></p></div>' for u, a, ad, b, bd in X[lang]['vs']) + '</div></div></section>',
            f'<section class="rm-sec" id="cual"><div class="wrap"><h2>{X[lang]["uso_h"]}</h2><div class="mj-uso">' +
            ''.join(f'<div><h3>{h}</h3><p>{d}</p></div>' for h, d in X[lang]['uso']) + '</div></div></section>',
            f'<section class="rm-sec"><div class="wrap"><h2>{t["how_h"]}</h2><div class="rm-grid" style="grid-template-columns:repeat(3,minmax(0,1fr))">' +
            ''.join(f'<div><span class="n">{n}</span><h3>{h}</h3><p>{d}</p></div>' for n, (h, d) in enumerate(t['how'], 1)) + '</div></div></section>',
            f'<section class="rm-sec" id="vender"><div class="wrap"><div class="mj-sell"><h2>{X[lang]["sell_h"]}</h2><p>{X[lang]["sell"]}</p><div class="mj-jump">'
            f'<a class="btn btn-wa" href="{e(wa(X[lang]["wa_g"]))}" target="_blank" rel="noopener" data-wa-context="moto_agua_vender_gestion">{X[lang]["b_g"]}</a>'
            f'<a class="btn btn-wa" href="{e(wa(X[lang]["wa_c"]))}" target="_blank" rel="noopener" data-wa-context="moto_agua_vender_compra">{X[lang]["b_c"]}</a></div></div></div></section>',
            f'<section class="rm-sec rm-faq"><div class="wrap"><h2>{t["faq_h"]}</h2>' +
            ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq']+X[lang]['faq2']) + '</div></section>',
            f'<div class="wrap"><div class="rm-end"><h2>{t["end_h"]}</h2><a class="btn btn-wa" href="{e(wa(t["wa_gen"]))}" target="_blank" rel="noopener" data-wa-context="moto_agua_nueva">{t["btn"]}</a> '
            f'<a class="btn" style="background:#fff;color:#0E3042;margin-left:8px" href="{p}/comprar/motos-de-agua-segunda-mano">{t["used"]}</a></div>',
            f'<p class="rm-small">{t["small"]}</p></div>', JS, '']
    out = head + body_top + '\n'.join(main) + foot
    d = os.path.join(ROOT, p.lstrip('/'), SLUG); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)
    return d


if __name__ == '__main__':
    for l in LANGS: print(build(l))
