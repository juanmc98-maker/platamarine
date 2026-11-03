#!/usr/bin/env python3
"""Página para profesionales: colaboración entre brókers y náuticas (ES/CA/EN/FR).

Uso: python3 _tools/build_colaboracion_brokers.py
Toma como molde /servicios/cambio-titularidad-barco.html de cada idioma (cabecera,
menú, pie, estilos del formulario) y genera /colaboracion-brokers/index.html.
Sin porcentajes ni cifras de comisión: se pactan por escrito en cada operación.
No toca menús, sitemap ni el índice de búsqueda.
"""
import json, re, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SLUG = 'colaboracion-brokers'
SRC = 'cambio-titularidad-barco'
BASE = 'https://www.platamarine.com'
PRE = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
WA = 'https://wa.me/34633742973?text='
JS = f'/{SLUG}/brokers-forms.js?v=20261103'

T = {
 'es': dict(
  title='Colaboración entre brókers náuticos en Cataluña',
  desc='¿Eres bróker o tienes una náutica? Compartamos cartera y comisión en la venta de barcos en Cataluña y Baleares, con todo pactado por escrito.',
  crumb='Colaboración entre brókers', eyebrow='Para profesionales · Colaboración',
  h1='Colaboración entre brókers y náuticas en Cataluña y Baleares',
  meta='<span>Por Juan Morante</span><span>Actualizado en noviembre de 2026</span>',
  lead='Soy Juan Morante, de Plata Marine. Si eres bróker, concesionario o tienes una náutica, en España o en otro país de Europa, y tienes barcos o clientes que pasan por Cataluña y Baleares, me gustaría que trabajáramos juntos. La idea es sencilla: sumar lo que tiene cada uno para cerrar operaciones que por separado costarían más, con las condiciones claras desde el principio.',
  toc=[('quien', 'Para quién es'), ('propuesta', 'Qué te propongo'), ('como', 'Cómo trabajamos'), ('aporto', 'Qué puedo aportar'), ('escribeme', 'Escríbeme')],
  quien=['Brókers y náuticas de otras zonas de España con un barco en venta en Cataluña o Baleares, o con un cliente que busca barco aquí.',
         'Brókers y concesionarios de Francia, Italia y el resto de Europa con compradores que quieren navegar en esta costa, o con barcos amarrados aquí.',
         'Profesionales de Cataluña y Baleares que prefieren compartir cartera antes que competir por el mismo barco.'],
  prop=[('Compartir cartera', 'Te paso los barcos que tengo en venta y lo que buscan mis compradores, y tú me pasas lo tuyo cuando encaje.'),
        ('Operaciones a medias', 'Uno aporta el comprador y el otro el barco, y la comisión de la venta se comparte como lo hayamos pactado.'),
        ('Enseñar barcos por ti en Cataluña', 'Si tienes un barco aquí y te queda lejos, puedo enseñarlo a tu cliente de tu parte y contarte después cómo ha ido.'),
        ('Respeto al cliente de cada uno', 'El cliente que presentas sigue siendo tuyo: no le contacto por mi cuenta ni le ofrezco otros barcos al margen de ti. Y espero lo mismo.')],
  como=[('Por escrito antes de empezar', 'En cada operación dejamos pactado por escrito qué aporta cada uno y cómo se reparte la comisión, antes de presentar ningún cliente ni ningún barco.'),
        ('La autorización del vendedor manda', 'Quien tiene la hoja de encargo o la autorización del vendedor es quien la tiene. El otro no la discute ni intenta sustituirla.'),
        ('Confidencialidad', 'Los datos de clientes, propietarios y precios que nos pasemos se usan solo para esa operación y no salen de ahí.'),
        ('Cada uno habla con su cliente', 'Nos coordinamos entre nosotros y cada uno lleva la relación con el suyo, para que nadie reciba mensajes duplicados.')],
  como_note='No tengo un reparto fijo para todo: cada barco y cada operación son distintos, y prefiero acordarlo contigo caso por caso.',
  aporto_intro='Vengo de la compraventa de vehículos y ahora trabajo como bróker náutico. Esto es lo que puedo poner de mi parte:',
  aporto=[('Estoy en Cataluña', 'Vivo y trabajo cerca de Barcelona, así que puedo ver un barco, enseñarlo o acompañar una prueba sin que nadie tenga que desplazarse desde lejos.'),
          ('Conozco el mercado local de ocasión', 'Qué barcos se mueven aquí, en qué puertos y a qué precios se están cerrando.'),
          ('Una web propia en cuatro idiomas', 'En castellano, catalán, inglés y francés, donde publico los barcos y a la que llegan compradores de aquí y de fuera.'),
          ('Contactos en la zona', 'Gestoría náutica y mantenimiento de confianza en Cataluña y Baleares para lo que pida cada operación.')],
  esc_h='Escríbeme', esc_p='Cuéntame quién eres y qué tienes en mente, y te contesto yo.',
  f=dict(n='Nombre', co='Empresa', e='Email', t='Teléfono', w='Web', wp='www.tuempresa.com', opt='(opcional)', z='Zona en la que trabajas', zp='Costa Azul, Valencia, Mallorca…',
         k='Tipo de colaboración', ko=['Tengo barcos para vender en Cataluña o Baleares', 'Tengo compradores que buscan barco aquí', 'Quiero compartir cartera', 'Otra'],
         m='Mensaje', mp='Qué barcos o clientes tienes y cómo te gustaría trabajar…', send='Enviar',
         legal='Responsable: Juan Morante (Plata Marine), juan@platamarine.com. Finalidad: contestar a tu propuesta de colaboración y, si seguimos adelante, gestionarla. Base legal: tu consentimiento, que puedes retirar cuando quieras. No cedo tus datos a terceros. Conservación: mientras hablemos de la colaboración y, si no sale adelante, doce meses como máximo. Derechos: acceso, rectificación, supresión, oposición y los demás que reconoce el RGPD, escribiendo a juan@platamarine.com; también puedes reclamar ante la AEPD. Más información en la <a href="/privacidad">política de privacidad</a>.',
         ck='He leído la información de privacidad y acepto que uses estos datos para contestarme.', req='Los campos con * son obligatorios.'),
  wa_txt='¿Prefieres WhatsApp?', wa_btn='Escríbeme por WhatsApp', wa_msg='Hola Juan, trabajo en el sector náutico y me interesa colaborar contigo.',
  small='¿Eres particular? Si quieres vender tu barco, mira <a href="/vender-barco/">Vender mi barco</a>; si buscas uno, <a href="/barcos/">los barcos en venta</a>.',
  aside_e='¿Tienes un barco o un cliente aquí?', aside_h='Hablemos de cómo hacerlo.', aside_p='Cuéntame qué tienes y vemos si encaja.', aside_b='Hablar con Juan por WhatsApp',
  toc_e='En esta página', rel_e='También te puede interesar',
  rel=[('/barcos/', 'Barcos en venta'), ('/guias/que-hace-un-broker-nautico', 'Qué hace un bróker náutico'), ('/vender/broker-nautico-barcelona-maresme', 'Vender en Barcelona y Maresme'), ('/servicios/', 'Servicios náuticos')],
 ),
 'ca': dict(
  title='Col·laboració entre brokers nàutics a Catalunya',
  desc='Ets broker o tens una nàutica? Compartim cartera i comissió en la venda de vaixells a Catalunya i Balears, amb tot pactat per escrit.',
  crumb='Col·laboració entre brokers', eyebrow='Per a professionals · Col·laboració',
  h1='Col·laboració entre brokers i nàutiques a Catalunya i Balears',
  meta='<span>Per Juan Morante</span><span>Actualitzat el novembre de 2026</span>',
  lead='Soc Juan Morante, de Plata Marine. Si ets broker, concessionari o tens una nàutica, a Espanya o en un altre país d’Europa, i tens vaixells o clients que passen per Catalunya i Balears, m’agradaria que treballéssim junts. La idea és senzilla: sumar el que té cadascú per tancar operacions que per separat costarien més, amb les condicions clares des del principi.',
  toc=[('quien', 'Per a qui és'), ('propuesta', 'Què et proposo'), ('como', 'Com treballem'), ('aporto', 'Què puc aportar'), ('escribeme', 'Escriu-me')],
  quien=['Brokers i nàutiques d’altres zones d’Espanya amb un vaixell en venda a Catalunya o Balears, o amb un client que busca vaixell aquí.',
         'Brokers i concessionaris de França, Itàlia i la resta d’Europa amb compradors que volen navegar en aquesta costa, o amb vaixells amarrats aquí.',
         'Professionals de Catalunya i Balears que prefereixen compartir cartera abans que competir pel mateix vaixell.'],
  prop=[('Compartir cartera', 'Et passo els vaixells que tinc en venda i el que busquen els meus compradors, i tu em passes el teu quan encaixi.'),
        ('Operacions a mitges', 'Un aporta el comprador i l’altre el vaixell, i la comissió de la venda es comparteix com ho hàgim pactat.'),
        ('Ensenyar vaixells de part teva a Catalunya', 'Si tens un vaixell aquí i et queda lluny, el puc ensenyar al teu client de part teva i explicar-te després com ha anat.'),
        ('Respecte pel client de cadascú', 'El client que presentes continua sent teu: no el contacto pel meu compte ni li ofereixo altres vaixells al marge teu. I espero el mateix.')],
  como=[('Per escrit abans de començar', 'En cada operació deixem pactat per escrit què aporta cadascú i com es reparteix la comissió, abans de presentar cap client ni cap vaixell.'),
        ('L’autorització del venedor mana', 'Qui té el full d’encàrrec o l’autorització del venedor és qui la té. L’altre no la discuteix ni intenta substituir-la.'),
        ('Confidencialitat', 'Les dades de clients, propietaris i preus que ens passem s’usen només per a aquella operació i no en surten.'),
        ('Cadascú parla amb el seu client', 'Ens coordinem entre nosaltres i cadascú porta la relació amb el seu, perquè ningú rebi missatges duplicats.')],
  como_note='No tinc un repartiment fix per a tot: cada vaixell i cada operació són diferents, i prefereixo acordar-ho amb tu cas per cas.',
  aporto_intro='Vinc de la compravenda de vehicles i ara treballo com a broker nàutic. Això és el que puc posar de la meva part:',
  aporto=[('Soc a Catalunya', 'Visc i treballo a prop de Barcelona, així que puc veure un vaixell, ensenyar-lo o acompanyar una prova sense que ningú s’hagi de desplaçar des de lluny.'),
          ('Conec el mercat local d’ocasió', 'Quins vaixells es mouen aquí, en quins ports i a quins preus s’estan tancant.'),
          ('Una web pròpia en quatre idiomes', 'En castellà, català, anglès i francès, on publico els vaixells i on arriben compradors d’aquí i de fora.'),
          ('Contactes a la zona', 'Gestoria nàutica i manteniment de confiança a Catalunya i Balears per al que demani cada operació.')],
  esc_h='Escriu-me', esc_p='Explica’m qui ets i què tens al cap, i et contesto jo.',
  f=dict(n='Nom', co='Empresa', e='Correu electrònic', t='Telèfon', w='Web', wp='www.lateva-empresa.com', opt='(opcional)', z='Zona on treballes', zp='Costa Blava, València, Mallorca…',
         k='Tipus de col·laboració', ko=['Tinc vaixells per vendre a Catalunya o Balears', 'Tinc compradors que busquen vaixell aquí', 'Vull compartir cartera', 'Una altra'],
         m='Missatge', mp='Quins vaixells o clients tens i com t’agradaria treballar…', send='Enviar',
         legal='Responsable: Juan Morante (Plata Marine), juan@platamarine.com. Finalitat: respondre la teva proposta de col·laboració i, si tirem endavant, gestionar-la. Base legal: el teu consentiment, que pots retirar quan vulguis. No cedeixo les teves dades a tercers. Conservació: mentre parlem de la col·laboració i, si no tira endavant, dotze mesos com a màxim. Drets: accés, rectificació, supressió, oposició i la resta que reconeix el RGPD, escrivint a juan@platamarine.com; també pots reclamar davant l’AEPD. Més informació a la <a href="/ca/privacidad">política de privacitat</a>.',
         ck='He llegit la informació de privacitat i accepto que facis servir aquestes dades per contestar-me.', req='Els camps amb * són obligatoris.'),
  wa_txt='Prefereixes WhatsApp?', wa_btn='Escriu-me per WhatsApp', wa_msg='Hola Juan, treballo al sector nàutic i m’interessa col·laborar amb tu.',
  small='Ets particular? Si vols vendre el teu vaixell, mira <a href="/ca/vender-barco/">Vendre el meu vaixell</a>; si en busques un, <a href="/ca/barcos/">els vaixells en venda</a>.',
  aside_e='Tens un vaixell o un client aquí?', aside_h='Parlem de com fer-ho.', aside_p='Explica’m què tens i veiem si encaixa.', aside_b='Parlar amb Juan per WhatsApp',
  toc_e='En aquesta pàgina', rel_e='També et pot interessar',
  rel=[('/ca/barcos/', 'Vaixells en venda'), ('/ca/guias/que-hace-un-broker-nautico', 'Què fa un broker nàutic'), ('/ca/vender/broker-nautico-barcelona-maresme', 'Vendre a Barcelona i el Maresme'), ('/ca/servicios/', 'Serveis nàutics')],
 ),
 'en': dict(
  title='Boat co-brokerage in Catalonia and the Balearics',
  desc='Yacht broker or dealer with boats or buyers in Catalonia and the Balearics, Spain? Let’s share listings and split the commission, agreed in writing.',
  crumb='Broker collaboration', eyebrow='For professionals · Collaboration',
  h1='Co-brokerage with brokers and dealers in Catalonia and the Balearics',
  meta='<span>By Juan Morante</span><span>Updated November 2026</span>',
  lead='I’m Juan Morante, from Plata Marine. If you are a yacht broker, a dealer or run a boat business, in Spain or elsewhere in Europe, and you have boats or clients passing through Catalonia and the Balearics, I’d like us to work together. The idea is simple: put together what each of us has to close deals that would be harder on our own, with the terms clear from the start.',
  toc=[('quien', 'Who this is for'), ('propuesta', 'What I propose'), ('como', 'How we work'), ('aporto', 'What I can bring'), ('escribeme', 'Write to me')],
  quien=['Brokers and boat businesses elsewhere in Spain with a boat for sale in Catalonia or the Balearics, or a client looking for a boat here.',
         'Brokers and dealers in France, Italy and the rest of Europe with buyers who want to sail this coast, or with boats berthed here.',
         'Professionals in Catalonia and the Balearics who would rather share listings than compete for the same boat.'],
  prop=[('Sharing listings', 'I send you the boats I have for sale and what my buyers are looking for, and you send me yours when there is a match.'),
        ('Shared deals', 'One of us brings the buyer and the other the boat, and the commission on the sale is split as we have agreed.'),
        ('Showing boats for you in Catalonia', 'If you have a boat here and it is far for you, I can show it to your client on your behalf and tell you afterwards how it went.'),
        ('Each other’s clients are respected', 'The client you introduce stays yours: I don’t contact them on my own or offer them other boats behind your back. And I expect the same.')],
  como=[('In writing before we start', 'For each deal we agree in writing what each of us brings and how the commission is split, before any client or boat is introduced.'),
        ('The seller’s mandate decides', 'Whoever holds the listing agreement or the seller’s authorisation holds it. The other party does not dispute it or try to replace it.'),
        ('Confidentiality', 'Any client, owner or price details we share are used only for that deal and go no further.'),
        ('Each of us talks to our own client', 'We coordinate between ourselves and each keeps the relationship with their own client, so nobody gets duplicate messages.')],
  como_note='I don’t have a fixed split for everything: every boat and every deal is different, and I prefer to agree it with you case by case.',
  aporto_intro='I come from the used vehicle trade and now work as a yacht broker. This is what I can bring to the table:',
  aporto=[('I’m based in Catalonia', 'I live and work near Barcelona, so I can see a boat, show it or join a sea trial without anyone having to travel a long way.'),
          ('I know the local used boat market', 'Which boats sell here, in which marinas and at what prices deals are closing.'),
          ('My own website in four languages', 'In Spanish, Catalan, English and French, where I list the boats and where buyers from here and abroad find me.'),
          ('Local contacts', 'A trusted nautical agency for paperwork and maintenance people in Catalonia and the Balearics, for whatever each deal needs.')],
  esc_h='Write to me', esc_p='Tell me who you are and what you have in mind, and I’ll reply personally.',
  f=dict(n='Name', co='Company', e='Email', t='Phone', w='Website', wp='www.yourcompany.com', opt='(optional)', z='Area you work in', zp='French Riviera, Valencia, Mallorca…',
         k='Type of collaboration', ko=['I have boats to sell in Catalonia or the Balearics', 'I have buyers looking for a boat here', 'I want to share listings', 'Other'],
         m='Message', mp='What boats or clients you have and how you would like to work…', send='Send',
         legal='Data controller: Juan Morante (Plata Marine), juan@platamarine.com. Purpose: to reply to your collaboration proposal and, if we go ahead, to manage it. Legal basis: your consent, which you can withdraw at any time. I do not share your data with third parties. Retention: while we discuss the collaboration and, if it does not go ahead, twelve months at most. Rights: access, rectification, erasure, objection and the other rights recognised by the GDPR, by writing to juan@platamarine.com; you can also file a complaint with the Spanish data protection authority (AEPD). More information in the <a href="/en/privacidad">privacy policy</a>.',
         ck='I have read the privacy information and agree to you using this data to reply to me.', req='Fields marked * are required.'),
  wa_txt='Prefer WhatsApp?', wa_btn='Message me on WhatsApp', wa_msg='Hi Juan, I work in the boat trade and I am interested in working with you.',
  small='Private seller or buyer? To sell your boat, see <a href="/en/vender-barco/">Sell my boat</a>; to find one, <a href="/en/barcos/">boats for sale</a>.',
  aside_e='Got a boat or a client here?', aside_h='Let’s talk about how.', aside_p='Tell me what you have and we’ll see if it fits.', aside_b='Talk to Juan on WhatsApp',
  toc_e='On this page', rel_e='You may also like',
  rel=[('/en/barcos/', 'Boats for sale'), ('/en/guias/que-hace-un-broker-nautico', 'What a yacht broker does'), ('/en/vender/broker-nautico-barcelona-maresme', 'Selling in Barcelona and the Maresme'), ('/en/servicios/', 'Boat services')],
 ),
 'fr': dict(
  title='Collaboration entre courtiers nautiques en Catalogne',
  desc='Courtier ou concessionnaire nautique ? Partageons annonces et commission sur la vente de bateaux en Catalogne et aux Baléares, avec des conditions écrites.',
  crumb='Collaboration entre courtiers', eyebrow='Pour les professionnels · Collaboration',
  h1='Collaboration entre courtiers et professionnels du nautisme en Catalogne et aux Baléares',
  meta='<span>Par Juan Morante</span><span>Mis à jour en novembre 2026</span>',
  lead='Je suis Juan Morante, de Plata Marine. Si vous êtes courtier, concessionnaire ou professionnel du nautisme, en Espagne ou ailleurs en Europe, et que vous avez des bateaux ou des clients qui passent par la Catalogne et les Baléares, j’aimerais que l’on travaille ensemble. L’idée est simple : mettre en commun ce que chacun a pour conclure des ventes qui seraient plus difficiles seul, avec des conditions claires dès le départ.',
  toc=[('quien', 'Pour qui'), ('propuesta', 'Ce que je propose'), ('como', 'Comment nous travaillons'), ('aporto', 'Ce que je peux apporter'), ('escribeme', 'Écrivez-moi')],
  quien=['Courtiers et professionnels d’autres régions d’Espagne avec un bateau à vendre en Catalogne ou aux Baléares, ou un client qui cherche un bateau ici.',
         'Courtiers et concessionnaires de France, d’Italie et du reste de l’Europe avec des acheteurs qui veulent naviguer sur cette côte, ou des bateaux amarrés ici.',
         'Professionnels de Catalogne et des Baléares qui préfèrent partager leurs annonces plutôt que se disputer le même bateau.'],
  prop=[('Partager nos annonces', 'Je vous transmets les bateaux que j’ai à vendre et ce que cherchent mes acheteurs, et vous me transmettez les vôtres quand ça correspond.'),
        ('Des ventes en commun', 'L’un apporte l’acheteur, l’autre le bateau, et la commission de la vente est partagée comme nous l’avons convenu.'),
        ('Faire visiter vos bateaux en Catalogne', 'Si vous avez un bateau ici et que c’est loin pour vous, je peux le faire visiter à votre client de votre part et vous dire ensuite comment ça s’est passé.'),
        ('Le client de chacun est respecté', 'Le client que vous présentez reste le vôtre : je ne le contacte pas de mon côté et je ne lui propose pas d’autres bateaux sans vous. Et j’attends la même chose.')],
  como=[('Par écrit avant de commencer', 'Pour chaque vente, nous convenons par écrit de ce que chacun apporte et du partage de la commission, avant de présenter le moindre client ou bateau.'),
        ('Le mandat du vendeur prime', 'Celui qui détient le mandat ou l’autorisation du vendeur le détient. L’autre ne le conteste pas et n’essaie pas de le remplacer.'),
        ('Confidentialité', 'Les informations sur les clients, les propriétaires et les prix que nous échangeons servent uniquement à cette vente et ne vont pas plus loin.'),
        ('Chacun parle à son client', 'Nous nous coordonnons entre nous et chacun garde la relation avec le sien, pour que personne ne reçoive de messages en double.')],
  como_note='Je n’ai pas de partage fixe pour tout : chaque bateau et chaque vente sont différents, et je préfère en convenir avec vous au cas par cas.',
  aporto_intro='Je viens du commerce de véhicules d’occasion et je travaille aujourd’hui comme courtier nautique. Voici ce que je peux apporter :',
  aporto=[('Je suis en Catalogne', 'Je vis et travaille près de Barcelone : je peux voir un bateau, le faire visiter ou accompagner un essai sans que personne ait à venir de loin.'),
          ('Je connais le marché local de l’occasion', 'Quels bateaux se vendent ici, dans quels ports et à quels prix les ventes se concluent.'),
          ('Mon propre site en quatre langues', 'En espagnol, catalan, anglais et français, où je publie les bateaux et où arrivent des acheteurs d’ici et d’ailleurs.'),
          ('Des contacts sur place', 'Une agence nautique de confiance pour les démarches et des professionnels de l’entretien en Catalogne et aux Baléares, selon ce que demande chaque vente.')],
  esc_h='Écrivez-moi', esc_p='Dites-moi qui vous êtes et ce que vous avez en tête, je vous réponds personnellement.',
  f=dict(n='Nom', co='Société', e='E-mail', t='Téléphone', w='Site web', wp='www.votre-societe.fr', opt='(facultatif)', z='Zone où vous travaillez', zp='Côte d’Azur, Valence, Majorque…',
         k='Type de collaboration', ko=['J’ai des bateaux à vendre en Catalogne ou aux Baléares', 'J’ai des acheteurs qui cherchent un bateau ici', 'Je veux partager mes annonces', 'Autre'],
         m='Message', mp='Quels bateaux ou clients vous avez et comment vous aimeriez travailler…', send='Envoyer',
         legal='Responsable du traitement : Juan Morante (Plata Marine), juan@platamarine.com. Finalité : répondre à votre proposition de collaboration et, si nous avançons, la gérer. Base juridique : votre consentement, que vous pouvez retirer à tout moment. Je ne cède pas vos données à des tiers. Conservation : le temps de nos échanges sur la collaboration et, si elle ne se fait pas, douze mois au maximum. Droits : accès, rectification, effacement, opposition et les autres droits reconnus par le RGPD, en écrivant à juan@platamarine.com ; vous pouvez aussi déposer une réclamation auprès de l’autorité espagnole de protection des données (AEPD). Plus d’informations dans la <a href="/fr/privacidad">politique de confidentialité</a>.',
         ck='J’ai lu les informations sur la confidentialité et j’accepte que vous utilisiez ces données pour me répondre.', req='Les champs marqués * sont obligatoires.'),
  wa_txt='Vous préférez WhatsApp ?', wa_btn='Écrivez-moi sur WhatsApp', wa_msg='Bonjour Juan, je travaille dans le nautisme et je suis intéressé par une collaboration.',
  small='Vous êtes un particulier ? Pour vendre votre bateau, voyez <a href="/fr/vender-barco/">Vendre mon bateau</a> ; pour en trouver un, <a href="/fr/barcos/">les bateaux à vendre</a>.',
  aside_e='Un bateau ou un client ici ?', aside_h='Parlons-en.', aside_p='Dites-moi ce que vous avez et on voit si ça correspond.', aside_b='Parler à Juan sur WhatsApp',
  toc_e='Sur cette page', rel_e='À lire aussi',
  rel=[('/fr/barcos/', 'Bateaux à vendre'), ('/fr/guias/que-hace-un-broker-nautico', 'Le rôle d’un courtier nautique'), ('/fr/vender/broker-nautico-barcelona-maresme', 'Vendre à Barcelone et dans le Maresme'), ('/fr/servicios/', 'Services nautiques')],
 ),
}


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def url(lang):
    return f'{BASE}{PRE[lang]}/{SLUG}/'


def main_html(L, t):
    f = t['f']
    wa = WA + urllib.parse.quote(t['wa_msg'])
    li = lambda xs: ''.join(f'<li><b>{a}.</b> {b}</li>' for a, b in xs)
    quien = ''.join(f'<li>{x}</li>' for x in t['quien'])
    ko = ''.join(f'<option>{o}</option>' for o in f['ko'])
    form = (f'<div class="pm-amf" id="colaborar"><p>{t["esc_p"]}</p><form id="pmBroker" novalidate>'
            f'<div><label for="br_n">{f["n"]} <i>*</i></label><input id="br_n" name="nombre" type="text" required autocomplete="name" maxlength="60"></div>'
            f'<div><label for="br_c">{f["co"]} <i>*</i></label><input id="br_c" name="empresa" type="text" required autocomplete="organization" maxlength="100"></div>'
            f'<div><label for="br_e">{f["e"]} <i>*</i></label><input id="br_e" name="email" type="email" required autocomplete="email" maxlength="100"></div>'
            f'<div><label for="br_t">{f["t"]} <small>{f["opt"]}</small></label><input id="br_t" name="telefono" type="tel" placeholder="+34 600 000 000" autocomplete="tel" maxlength="40"></div>'
            f'<div><label for="br_w">{f["w"]} <small>{f["opt"]}</small></label><input id="br_w" name="web" type="text" inputmode="url" placeholder="{esc(f["wp"])}" autocomplete="url" maxlength="120"></div>'
            f'<div><label for="br_z">{f["z"]} <small>{f["opt"]}</small></label><input id="br_z" name="zona" type="text" placeholder="{esc(f["zp"])}" maxlength="100"></div>'
            f'<div class="s2"><label for="br_k">{f["k"]} <i>*</i></label><select id="br_k" name="tipo" required><option value=""></option>{ko}</select></div>'
            f'<div class="s2"><label for="br_x">{f["m"]} <small>{f["opt"]}</small></label><textarea id="br_x" name="mensaje" maxlength="1500" placeholder="{esc(f["mp"])}"></textarea></div>'
            f'<p class="help s2">{f["legal"]}</p>'
            f'<div class="s2"><label class="ck" for="br_ok"><input id="br_ok" name="privacidad" type="checkbox" required><span>{f["ck"]}&nbsp;<i>*</i></span></label></div>'
            f'<div class="s2"><button type="submit">{f["send"]}</button></div><p class="help s2">{f["req"]}</p>'
            f'<p class="pm-amst s2" role="status" aria-live="polite" hidden></p></form></div>')
    toc = ''.join(f'<li><a href="#{i}">{n}</a></li>' for i, n in t['toc'])
    rel = ''.join(f'<a href="{u}">{n}</a>' for u, n in t['rel'])
    h = dict(t['toc'])
    return f'''<main class="art">
  <div class="wrap">
    <article>
      <header>
        <p class="eyebrow">{t["eyebrow"]}</p>
        <h1>{t["h1"]}</h1>
        <div class="meta">{t["meta"]}</div>
        <p class="lead">{t["lead"]}</p>
      </header>
      <div class="prose">
        <h2 id="quien">{h["quien"]}</h2>
        <ul>{quien}</ul>
        <h2 id="propuesta">{h["propuesta"]}</h2>
        <ul>{li(t["prop"])}</ul>
        <h2 id="como">{h["como"]}</h2>
        <ul>{li(t["como"])}</ul>
        <p>{t["como_note"]}</p>
        <h2 id="aporto">{h["aporto"]}</h2>
        <p>{t["aporto_intro"]}</p>
        <ul>{li(t["aporto"])}</ul>
        <h2 id="escribeme">{h["escribeme"]}</h2>
        {form}
        <p class="help">{t["wa_txt"]} <a href="{wa}" target="_blank" rel="noopener">{t["wa_btn"]}</a></p>
        <p class="muted" style="font-size:.88rem;margin-top:26px">{t["small"]}</p>
      </div>
    </article>

    <aside class="aside" aria-label="{esc(t["aside_e"])}">
      <div class="card">
        <p class="eyebrow">{t["aside_e"]}</p>
        <h3>{t["aside_h"]}</h3>
        <p>{t["aside_p"]}</p>
        <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{t["aside_b"]}</a>
      </div>
      <nav class="toc" aria-label="{t["toc_e"]}">
        <p class="eyebrow">{t["toc_e"]}</p>
        <ol>{toc}</ol>
      </nav>
      <div class="rel">
        <p class="eyebrow">{t["rel_e"]}</p>{rel}
      </div>
    </aside>

  </div>
</main>'''


def build(L):
    t = T[L]
    root = ROOT / (PRE[L].lstrip('/') + '/' if PRE[L] else '')
    h = (root / 'servicios' / f'{SRC}.html').read_text(encoding='utf-8')
    full_title = f'{t["title"]} | Plata Marine' if len(t['title']) <= 46 else t['title']
    assert len(full_title) <= 60 and len(t['desc']) <= 155, (L, len(full_title), len(t['desc']))
    h = re.sub(r'<title>.*?</title>', f'<title>{full_title}</title>', h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(t["desc"])}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(full_title)}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(t["desc"])}">', h, count=1)
    # canonical, hreflang, og:url y selector de idioma
    for l2 in PRE:
        h = h.replace(f'{BASE}{PRE[l2]}/servicios/{SRC}"', f'{url(l2)}"')
    # estilos que solo usaba el directorio
    h = re.sub(r'<style>(?:\.dir[^\n]*\n)+', '<style>', h, count=1)
    # datos estructurados: WebPage + BreadcrumbList (sin FAQ ni reseñas)
    wp = {"@context": "https://schema.org", "@type": "WebPage", "@id": url(L) + '#webpage', "url": url(L),
          "name": full_title, "description": t['desc'], "inLanguage": L,
          "isPartOf": {"@type": "WebSite", "name": "Plata Marine", "url": f'{BASE}/'},
          "publisher": {"@type": "Organization", "name": "Plata Marine", "url": f'{BASE}/', "logo": f'{BASE}/logo-plata-marine-1200.png', "email": "juan@platamarine.com"},
          "breadcrumb": {"@id": url(L) + '#breadcrumb'}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "@id": url(L) + '#breadcrumb', "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f'{BASE}{PRE[L]}/'},
        {"@type": "ListItem", "position": 2, "name": t['crumb'], "item": url(L)}]}
    ld = ('<script type="application/ld+json">' + json.dumps(wp, ensure_ascii=False) + '</script>\n'
          '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + '</script>')
    h, n = re.subn(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>\s*<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>',
                   lambda m: ld, h, count=1, flags=re.S)
    assert n == 1
    # cuerpo
    h = re.sub(r'<main class="art">.*?</main>', lambda m: main_html(L, t), h, count=1, flags=re.S)
    # script del formulario
    h = re.sub(r'<script src="/servicios/tramites-forms\.js[^"]*" defer></script>', f'<script src="{JS}" defer></script>', h, count=1)
    # botón de cabecera y menú: esta página no cuelga de Recursos
    h = re.sub(r'(<a class="btn btn-wa" href=")https://wa\.me/[^"]*(" target="_blank" rel="noopener">)', lambda m: m.group(1) + WA + urllib.parse.quote(t['wa_msg']) + m.group(2), h, count=1)
    h = h.replace('class="pmx-dd pmx-res cur"', 'class="pmx-dd pmx-res"')
    assert SRC not in h and 'tramites-forms' not in h and 'FAQPage' not in h and JS in h
    out = root / SLUG / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(h, encoding='utf-8')
    return out


if __name__ == '__main__':
    for L in T:
        print(build(L))
