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
 ('stx',   [('kw-stx-310rx', 'STX 310RX', 310, None), ('kw-stx-310r', 'STX 310R', 310, None), ('kw-stx-160lx-2027', 'STX 160LX', 152, 3), ('kw-stx-160lx-s-2027', 'STX 160LX-S', 152, 3), ('kw-stx-160r-2027', 'STX 160R', 152, 3), ('kw-stx-160x-2027', 'STX 160X', 152, 3)]),
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
  ask='Precio a consultar', btn='Pedir precio', jump_sd='Ver gama Sea-Doo', jump_kw='Ver gama Kawasaki',
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
  ask='Preu a consultar', btn='Demanar preu', jump_sd='Veure gamma Sea-Doo', jump_kw='Veure gamma Kawasaki',
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
  ask='Price on request', btn='Ask for price', jump_sd='See Sea-Doo range', jump_kw='See Kawasaki range',
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
  ask='Prix sur demande', btn='Demander le prix', jump_sd='Voir la gamme Sea-Doo', jump_kw='Voir la gamme Kawasaki',
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

ADD = {'es': {'note': 'Precio a consultar: te paso el presupuesto por escrito con la versión, el equipamiento, los impuestos, el transporte y el plazo de entrega.', 'fil_l': 'Filtrar motos', 'fil': [('all', 'Todas'), ('sea-doo', 'Sea-Doo'), ('kawasaki', 'Kawasaki'), ('ini', 'Para empezar'), ('fam', 'Familia'), ('trav', 'Travesía'), ('dep', 'Deportivas'), ('agua', 'Pesca y arrastre'), ('pie', 'De pie')], 'vs_h': 'Sea-Doo o Kawasaki: modelos que se comparan', 'vs_p': 'Si dudas entre las dos marcas, estos son los modelos que suelen compararse. Las diferencias de equipamiento y precio te las detallo en el presupuesto.', 'vs': [('Familia', 'Sea-Doo GTI SE 170', '170 cv · 3 plazas', 'Kawasaki STX 160LX', '152 cv · 3 plazas'), ('Travesía', 'Sea-Doo GTX 230', '230 cv · 3 plazas', 'Kawasaki Ultra 160LX', '152 cv · 3 plazas'), ('Lo más completo', 'Sea-Doo GTX Limited 350', '350 cv · 3 plazas', 'Kawasaki Ultra 310LX', '300 cv · 3 plazas'), ('Deportivas', 'Sea-Doo RXT-X 350', '350 cv · 3 plazas', 'Kawasaki STX 310RX', '310 cv')]}, 'ca': {'note': "Preu a consultar: et passo el pressupost per escrit amb la versió, l'equipament, els impostos, el transport i el termini de lliurament.", 'fil_l': 'Filtrar motos', 'fil': [('all', 'Totes'), ('sea-doo', 'Sea-Doo'), ('kawasaki', 'Kawasaki'), ('ini', 'Per començar'), ('fam', 'Família'), ('trav', 'Travessia'), ('dep', 'Esportives'), ('agua', 'Pesca i arrossegament'), ('pie', 'Dempeus')], 'vs_h': 'Sea-Doo o Kawasaki: models que es comparen', 'vs_p': "Si dubtes entre les dues marques, aquests són els models que se solen comparar. Les diferències d'equipament i preu te les detallo al pressupost.", 'vs': [('Família', 'Sea-Doo GTI SE 170', '170 cv · 3 places', 'Kawasaki STX 160LX', '152 cv · 3 places'), ('Travessia', 'Sea-Doo GTX 230', '230 cv · 3 places', 'Kawasaki Ultra 160LX', '152 cv · 3 places'), ('El més complet', 'Sea-Doo GTX Limited 350', '350 cv · 3 places', 'Kawasaki Ultra 310LX', '300 cv · 3 places'), ('Esportives', 'Sea-Doo RXT-X 350', '350 cv · 3 places', 'Kawasaki STX 310RX', '310 cv')]}, 'en': {'note': 'Price on request: I send you a written quote with version, equipment, taxes, transport and delivery time.', 'fil_l': 'Filter jet skis', 'fil': [('all', 'All'), ('sea-doo', 'Sea-Doo'), ('kawasaki', 'Kawasaki'), ('ini', 'Beginners'), ('fam', 'Family'), ('trav', 'Touring'), ('dep', 'Sporty'), ('agua', 'Fishing & towing'), ('pie', 'Stand-up')], 'vs_h': 'Sea-Doo or Kawasaki: models people compare', 'vs_p': 'If you are torn between the two brands, these are the models usually compared. I detail equipment and price differences in the quote.', 'vs': [('Family', 'Sea-Doo GTI SE 170', '170 hp · 3 seats', 'Kawasaki STX 160LX', '152 hp · 3 seats'), ('Touring', 'Sea-Doo GTX 230', '230 hp · 3 seats', 'Kawasaki Ultra 160LX', '152 hp · 3 seats'), ('Top of the range', 'Sea-Doo GTX Limited 350', '350 hp · 3 seats', 'Kawasaki Ultra 310LX', '300 hp · 3 seats'), ('Sporty', 'Sea-Doo RXT-X 350', '350 hp · 3 seats', 'Kawasaki STX 310RX', '310 hp')]}, 'fr': {'note': 'Prix sur demande : je vous envoie un devis écrit avec la version, l’équipement, les taxes, le transport et le délai de livraison.', 'fil_l': 'Filtrer les jet-skis', 'fil': [('all', 'Tous'), ('sea-doo', 'Sea-Doo'), ('kawasaki', 'Kawasaki'), ('ini', 'Pour débuter'), ('fam', 'Famille'), ('trav', 'Randonnée'), ('dep', 'Sportifs'), ('agua', 'Pêche et traction'), ('pie', 'Debout')], 'vs_h': 'Sea-Doo ou Kawasaki : modèles comparables', 'vs_p': 'Si vous hésitez entre les deux marques, voici les modèles souvent comparés. Je détaille les différences d’équipement et de prix dans le devis.', 'vs': [('Famille', 'Sea-Doo GTI SE 170', '170 ch · 3 places', 'Kawasaki STX 160LX', '152 ch · 3 places'), ('Randonnée', 'Sea-Doo GTX 230', '230 ch · 3 places', 'Kawasaki Ultra 160LX', '152 ch · 3 places'), ('Le plus complet', 'Sea-Doo GTX Limited 350', '350 ch · 3 places', 'Kawasaki Ultra 310LX', '300 ch · 3 places'), ('Sportifs', 'Sea-Doo RXT-X 350', '350 ch · 3 places', 'Kawasaki STX 310RX', '310 ch')]}}
for _l in ADD: X[_l].update(ADD[_l])

JS = '''<script>(function(){var bs=document.querySelectorAll('.mj-fil button');function go(f){bs.forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-f')===f?'true':'false')});document.querySelectorAll('.mj-c').forEach(function(c){var ok=f==='all'||c.getAttribute('data-use')===f||c.getAttribute('data-brand')===f;c.hidden=!ok});document.querySelectorAll('.mj-fam').forEach(function(m){m.hidden=!m.querySelector('.mj-c:not([hidden])')});document.querySelectorAll('#sea-doo,#kawasaki').forEach(function(sec){sec.hidden=!sec.querySelector('.mj-c:not([hidden])')})}bs.forEach(function(b){b.addEventListener('click',function(){go(b.getAttribute('data-f'))})})})();</script>'''

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
</style>"""


def wa(text):
    return 'https://wa.me/34633742973?text=' + quote(text, safe='')


USE = {'sd-spark':'ini','sd-spark-x':'ini','sd-trixx-for3-blue-mist':'ini','sd-gti':'fam','sd-gti-se-teal-blue':'fam',
 'sd-gtx':'trav','sd-gtx-230':'trav','sd-gtx-limited':'trav','sd-explorer-pro':'trav','sd-rxp-x-350-solar-orange':'dep','sd-rxp-x-senna':'dep',
 'sd-rxt-x-350-solar-orange':'dep','sd-fishpro-trophy':'agua','sd-wake-170':'agua','sd-wake-pro-230':'agua',
 'kw-ultra-310lx-2027':'trav','kw-ultra-310lx-s-2027':'trav','kw-ultra-160lx-2027':'trav','kw-ultra-160lx-s-2027':'trav','kw-ultra-160lx-s-wakesport':'agua',
 'kw-stx-310rx':'dep','kw-stx-310r':'dep','kw-stx-160lx-2027':'fam','kw-stx-160lx-s-2027':'fam','kw-stx-160r-2027':'fam','kw-stx-160x-2027':'fam',
 'kw-sx-r-160':'pie','kw-sx-x-160':'pie'}


def card(t, key, name, brand, cv, seats):
    full = f'{brand} {name}'
    sp = []
    if cv: sp.append(f'{cv} {t["cv"]}')
    if seats == 0: sp.append(t['stand'])
    elif seats: sp.append(t['seats'].format(n=seats))
    e = html.escape
    return (f'<article class="mj-c" data-use="{USE[key]}" data-brand="{brand.lower()}"><img src="/{SLUG}/fotos/{key}.jpg" alt="{e(full)}" width="900" height="675" loading="lazy">'
            f'<div><h4>{e(full)}</h4><p class="sp">{" · ".join(sp)}</p><p class="pr">{t["ask"]}</p>'
            f'<a class="btn btn-wa" href="{e(wa(t["wa"].format(m=full)))}" target="_blank" rel="noopener" data-wa-context="moto_agua_nueva">{t["btn"]}</a></div></article>')


def brand_sec(t, bid, brand, logo, fams):
    out = [f'<section class="rm-sec" id="{bid}"><div class="wrap"><img class="mj-blogo{' sd' if bid=='sea-doo' else ''}" src="/barcos-nuevos/logos/{logo}" alt="{brand}"><h2 class="mj-bh">{t['gama'].format(b=brand)}</h2>']
    for fk, models in fams:
        n, d = t['fam'][fk]
        out.append(f'<div class="mj-fam"><h3>{brand} {n}</h3><p>{d}</p><div class="mj-grid">' +
                   ''.join(card(t, k, m, brand, cv, s) for k, m, cv, s in models) + '</div></div>')
    out.append('</div></section>')
    return ''.join(out)


def build(lang):
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
            f'<div class="wrap"><p class="rm-crumb"><a href="{p}/">{t["home"]}</a> · <a href="{p}/barcos-nuevos/">{t["nb"]}</a> · {t["crumb"]}</p></div>',
            f'<section class="wrap rm-hero"><div><div class="mj-brand"><img class="sd" src="/barcos-nuevos/logos/sea-doo.png" alt="Sea-Doo" width="900" height="97"><img src="/barcos-nuevos/logos/kawasaki.png" alt="Kawasaki" width="319" height="88"></div>'
            f'<p class="k">{t["kick"]}</p><h1>{t["h1"]}</h1><p class="lead">{t["lead"]}</p><p style="font-weight:600;margin:0 0 16px">{t["tit"]}</p>'
            f'<div class="mj-jump"><a class="btn btn-wa" href="{e(wa(t["wa_gen"]))}" target="_blank" rel="noopener" data-wa-context="moto_agua_nueva">{t["btn"]}</a>'
            f'<a class="btn" href="#sea-doo">{t["jump_sd"]}</a><a class="btn" href="#kawasaki">{t["jump_kw"]}</a></div></div>'
            f'<div><img class="mj-hero-img" src="/{SLUG}/fotos/sd-gtx-limited.jpg" alt="Sea-Doo GTX Limited 350" width="900" height="636"></div></section>',
            f'<div class="wrap" id="catalogo"><p class="mj-note">{X[lang]["note"]}</p><div class="mj-fil" role="group" aria-label="{X[lang]["fil_l"]}">' +
            ''.join(f'<button type="button" data-f="{k}"{" aria-pressed=\"true\"" if k=="all" else " aria-pressed=\"false\""}>{v}</button>' for k, v in X[lang]['fil']) + '</div></div>',
            brand_sec(t, 'sea-doo', 'Sea-Doo', 'sea-doo.png', SEADOO),
            brand_sec(t, 'kawasaki', 'Kawasaki', 'kawasaki.png', KAWA),
            f'<section class="rm-sec" id="comparar"><div class="wrap"><h2>{X[lang]["vs_h"]}</h2><p>{X[lang]["vs_p"]}</p><div class="mj-vs">' +
            ''.join(f'<div><p class="u">{u}</p><p><b>{a}</b><span>{ad}</span></p><p class="o">vs</p><p><b>{b}</b><span>{bd}</span></p></div>' for u, a, ad, b, bd in X[lang]['vs']) + '</div></div></section>',
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
