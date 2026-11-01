#!/usr/bin/env python3
"""Página de servicio: cambio de titularidad y de bandera (ES/CA/EN/FR).

Uso: python3 _tools/build_tramites.py
Toma como molde /servicios/amarres.html de cada idioma (cabecera, menú, pie)
y genera /servicios/cambio-titularidad-barco.html. Sin precios y sin nombrar
gestorías (decisión de Juan, 1 nov 2026).
"""
import json, re, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SLUG = 'cambio-titularidad-barco'
BASE = 'https://www.platamarine.com'
PRE = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
WA = 'https://wa.me/34633742973?text='

T = {
 'es': dict(
  title='Cambio de titularidad de barco en Cataluña y Baleares',
  desc='¿Has comprado un barco o lo tienes apalabrado? Te gestionamos el cambio de titularidad (transferencia) y de bandera con una gestoría náutica colaboradora.',
  crumb='Servicios', eyebrow='Servicios · Papeles del barco',
  h1='Cambio de titularidad y de bandera de tu barco',
  meta='<span>Por Juan Morante</span><span>Actualizado en noviembre de 2026</span>',
  lead='Si vas a comprar un barco, o ya lo tienes apalabrado con el vendedor, te gestiono el papeleo para que quede a tu nombre: el cambio de titularidad (también llamado transferencia o cambio de nombre) y, si hace falta, el cambio de bandera. Lo tramita una gestoría náutica con la que colaboro y tú hablas solo conmigo. Trabajo sobre todo en Cataluña y Baleares, y si tu barco está en otra zona, pregúntame.',
  toc=[('que', 'Qué te gestiono'), ('como', 'Cómo funciona'), ('docs', 'Qué documentos suelen pedir'), ('antes', 'Si aún no lo has comprado'), ('pedir', 'Pedir la gestión'), ('faq', 'Preguntas frecuentes')],
  que=[('Cambio de titularidad', 'La transferencia del barco del vendedor al comprador, entre particulares o comprando a una empresa.'),
       ('Cambio de bandera', 'Pasar a bandera española un barco que viene de otro país, o abanderarlo fuera si es lo que te conviene.'),
       ('Cambio de lista', 'Si vas a pasar el barco de uso privado (7ª lista) a chárter (6ª lista), o al revés.'),
       ('Revisión previa', 'Antes de pagar, comprobamos que el barco está a nombre de quien te lo vende y que la documentación está en regla.')],
  como=[('Me cuentas tu caso', 'Qué barco es, dónde está, qué bandera tiene y si ya está comprado o apalabrado.'),
        ('Te digo qué hace falta', 'La lista de documentos para tu caso y un presupuesto cerrado por escrito antes de empezar.'),
        ('Lo tramitamos', 'La gestoría hace el trámite y yo te mantengo al día hasta que tienes los papeles a tu nombre.')],
  docs_intro='Cada caso es distinto, pero esto es lo que se suele pedir en un cambio de titularidad entre particulares:',
  docs=['DNI o NIE del comprador y del vendedor.', 'Contrato de compraventa firmado por los dos.', 'La documentación del barco: certificado de registro o de navegabilidad y, si la tiene, la hoja de asiento.',
        'El justificante de haber pagado el impuesto de la compra (en una compra entre particulares, normalmente el ITP de tu comunidad autónoma).', 'Si cambia la bandera, los papeles del registro de origen y su baja.'],
  docs_note='La lista exacta te la confirmo según tu caso antes de empezar.',
  antes_h='Si aún no lo has comprado',
  antes='Mejor todavía: es el momento de evitar sorpresas. Antes de pagar conviene comprobar que quien vende es el titular, que el barco no tiene cargas y que los papeles cuadran con el barco (eslora, motor, número de casco). Si quieres dejarlo reservado, te recomiendo hacerlo con un contrato de arras.',
  pedir_h='Pedir la gestión', pedir_p='Cuéntame lo básico y te digo qué hace falta en tu caso. Sin compromiso.',
  f=dict(n='Nombre', t='Teléfono', e='Email', opt='(opcional)', tr='Qué necesitas', tro=['Cambio de titularidad', 'Cambio de bandera', 'Las dos cosas', 'No lo tengo claro'],
         b='Barco (marca, modelo y eslora)', bp='Beneteau Antares 8, 7,9 m', s='Situación', so=['Ya lo he comprado', 'Lo tengo apalabrado', 'Todavía lo estoy buscando'],
         fl='Bandera actual', flp='Española, francesa…', m='Algo más', mp='Dónde está el barco, plazos…', send='Enviar',
         legal='Responsable: Juan Morante (Plata Marine). Uso tus datos solo para contestarte y, si me lo pides, preparar la gestión con la gestoría colaboradora. No los cedo a nadie más. Puedes ejercer tus derechos en juan@platamarine.com. <a href="/privacidad">Política de privacidad</a>.',
         ck='He leído la información de privacidad y acepto que uses estos datos para contestarme.', req='Los campos con * son obligatorios.'),
  wa_txt='Prefieres WhatsApp?', wa_btn='Escríbeme por WhatsApp', wa_msg='Hola Juan, necesito hacer el cambio de titularidad de un barco.',
  faq=[('¿Cuánto cuesta?', 'Depende del barco y del trámite. Antes de empezar te paso un presupuesto cerrado por escrito, con las tasas y el impuesto aparte para que veas qué es cada cosa.'),
       ('¿Tengo que ir a algún sitio?', 'Normalmente se resuelve con la documentación. Si en tu caso hace falta firmar algo en persona, te lo digo desde el principio.'),
       ('¿Lo puedo hacer aunque no haya comprado el barco con vosotros?', 'Sí. Da igual dónde lo hayas encontrado: si lo tienes apalabrado o ya es tuyo, te ayudo con los papeles.'),
       ('¿Quién paga el impuesto de la compra?', 'En una compraventa entre particulares lo paga normalmente el comprador. Tienes los detalles por comunidad en la guía del ITP.')],
  small='Información orientativa: los requisitos y los impuestos pueden cambiar y dependen de cada caso. Te lo confirmamos por escrito antes de empezar.',
  aside_e='¿Lo tienes apalabrado?', aside_h='Te ayudo a cerrarlo bien.', aside_p='Cuéntame qué barco es y en qué punto estás.', aside_b='Hablar con Juan por WhatsApp',
  toc_e='En esta página', rel_e='También te puede interesar',
  rel=[('/guias/papeles-vender-barco-cambio-titularidad', 'Papeles para vender un barco'), ('/guias/itp-comprar-barco-usado-por-comunidad', 'ITP al comprar un barco usado'), ('/guias/arras-compraventa-barco', 'Contrato de arras'), ('/guias/bandera-polaca-abanderar-barco-otro-pais', 'Bandera polaca'), ('/guias/listas-matricula-barcos-espana', 'Listas de matrícula')],
  wabtn='Hablar con Juan', svc_card=('Cambio de titularidad y de bandera', 'Si compras un barco o lo tienes apalabrado, te gestiono el papeleo para que quede a tu nombre.', 'Ver el servicio'),
  link_guide='¿Prefieres que te lo gestionemos? <a href="{u}">Te hacemos el cambio de titularidad y de bandera</a>.',
 ),
 'ca': dict(
  title='Canvi de titularitat de vaixell a Catalunya i Balears',
  desc='Has comprat un vaixell o el tens apalabrat? Gestionem el canvi de titularitat i el canvi de bandera amb una gestoria nàutica col·laboradora, amb un sol interlocutor.',
  crumb='Serveis', eyebrow='Serveis · Papers del vaixell',
  h1='Canvi de titularitat i de bandera del teu vaixell',
  meta='<span>Per Juan Morante</span><span>Actualitzat el novembre de 2026</span>',
  lead='Si vas a comprar un vaixell, o ja el tens apalabrat amb el venedor, et gestiono els papers perquè quedi a nom teu: el canvi de titularitat i, si cal, el canvi de bandera. Ho tramita una gestoria nàutica amb qui col·laboro i tu parles només amb mi. Treballo sobretot a Catalunya i Balears, i si el teu vaixell és en una altra zona, pregunta-m’ho.',
  toc=[('que', 'Què et gestiono'), ('como', 'Com funciona'), ('docs', 'Quins documents solen demanar'), ('antes', 'Si encara no l’has comprat'), ('pedir', 'Demanar la gestió'), ('faq', 'Preguntes freqüents')],
  que=[('Canvi de titularitat', 'La transferència del vaixell del venedor al comprador, entre particulars o comprant a una empresa.'),
       ('Canvi de bandera', 'Passar a bandera espanyola un vaixell que ve d’un altre país, o abanderar-lo fora si és el que et convé.'),
       ('Canvi de llista', 'Si passaràs el vaixell d’ús privat (7a llista) a xàrter (6a llista), o a l’inrevés.'),
       ('Revisió prèvia', 'Abans de pagar, comprovem que el vaixell està a nom de qui te’l ven i que la documentació està en regla.')],
  como=[('M’expliques el teu cas', 'Quin vaixell és, on és, quina bandera té i si ja està comprat o apalabrat.'),
        ('Et dic què cal', 'La llista de documents per al teu cas i un pressupost tancat per escrit abans de començar.'),
        ('Ho tramitem', 'La gestoria fa el tràmit i jo et mantinc al dia fins que tens els papers a nom teu.')],
  docs_intro='Cada cas és diferent, però això és el que se sol demanar en un canvi de titularitat entre particulars:',
  docs=['DNI o NIE del comprador i del venedor.', 'Contracte de compravenda signat pels dos.', 'La documentació del vaixell: certificat de registre o de navegabilitat i, si en té, el full d’assentament.',
        'El justificant d’haver pagat l’impost de la compra (en una compra entre particulars, normalment l’ITP de la teva comunitat autònoma).', 'Si canvia la bandera, els papers del registre d’origen i la seva baixa.'],
  docs_note='La llista exacta te la confirmo segons el teu cas abans de començar.',
  antes_h='Si encara no l’has comprat',
  antes='Encara millor: és el moment d’evitar sorpreses. Abans de pagar convé comprovar que qui ven n’és el titular, que el vaixell no té càrregues i que els papers quadren amb el vaixell (eslora, motor, número de casc). Si el vols deixar reservat, et recomano fer-ho amb un contracte d’arres.',
  pedir_h='Demanar la gestió', pedir_p='Explica’m el bàsic i et dic què cal en el teu cas. Sense compromís.',
  f=dict(n='Nom', t='Telèfon', e='Correu', opt='(opcional)', tr='Què necessites', tro=['Canvi de titularitat', 'Canvi de bandera', 'Les dues coses', 'No ho tinc clar'],
         b='Vaixell (marca, model i eslora)', bp='Beneteau Antares 8, 7,9 m', s='Situació', so=['Ja l’he comprat', 'El tinc apalabrat', 'Encara l’estic buscant'],
         fl='Bandera actual', flp='Espanyola, francesa…', m='Alguna cosa més', mp='On és el vaixell, terminis…', send='Enviar',
         legal='Responsable: Juan Morante (Plata Marine). Faig servir les teves dades només per contestar-te i, si m’ho demanes, preparar la gestió amb la gestoria col·laboradora. No les cedeixo a ningú més. Pots exercir els teus drets a juan@platamarine.com. <a href="/ca/privacidad">Política de privacitat</a>.',
         ck='He llegit la informació de privacitat i accepto que facis servir aquestes dades per contestar-me.', req='Els camps amb * són obligatoris.'),
  wa_txt='Prefereixes WhatsApp?', wa_btn='Escriu-me per WhatsApp', wa_msg='Hola Juan, necessito fer el canvi de titularitat d’un vaixell.',
  faq=[('Quant costa?', 'Depèn del vaixell i del tràmit. Abans de començar et passo un pressupost tancat per escrit, amb les taxes i l’impost a part perquè vegis què és cada cosa.'),
       ('He d’anar a algun lloc?', 'Normalment es resol amb la documentació. Si en el teu cas cal signar alguna cosa en persona, t’ho dic des del principi.'),
       ('Ho puc fer encara que no hagi comprat el vaixell amb vosaltres?', 'Sí. Tant és on l’hagis trobat: si el tens apalabrat o ja és teu, t’ajudo amb els papers.'),
       ('Qui paga l’impost de la compra?', 'En una compravenda entre particulars normalment el paga el comprador. Tens els detalls per comunitat a la guia de l’ITP.')],
  small='Informació orientativa: els requisits i els impostos poden canviar i depenen de cada cas. T’ho confirmem per escrit abans de començar.',
  aside_e='El tens apalabrat?', aside_h='T’ajudo a tancar-ho bé.', aside_p='Explica’m quin vaixell és i en quin punt estàs.', aside_b='Parlar amb Juan per WhatsApp',
  toc_e='En aquesta pàgina', rel_e='També et pot interessar',
  rel=[('/ca/guias/papeles-vender-barco-cambio-titularidad', 'Papers per vendre un vaixell'), ('/ca/guias/itp-comprar-barco-usado-por-comunidad', 'ITP en comprar un vaixell usat'), ('/ca/guias/arras-compraventa-barco', 'Contracte d’arres'), ('/ca/guias/bandera-polaca-abanderar-barco-otro-pais', 'Bandera polonesa'), ('/ca/guias/listas-matricula-barcos-espana', 'Llistes de matrícula')],
  wabtn='Parlar amb Juan', svc_card=('Canvi de titularitat i de bandera', 'Si compres un vaixell o el tens apalabrat, et gestiono els papers perquè quedi a nom teu.', 'Veure el servei'),
  link_guide='Prefereixes que t’ho gestionem? <a href="{u}">Et fem el canvi de titularitat i de bandera</a>.',
 ),
 'en': dict(
  title='Boat ownership transfer in Spain: we handle it',
  desc='Bought a boat in Spain or agreed the deal? We handle the change of ownership and change of flag with a partner nautical agency, with a single point of contact.',
  crumb='Services', eyebrow='Services · Boat paperwork',
  h1='Change of ownership and flag for your boat',
  meta='<span>By Juan Morante</span><span>Updated November 2026</span>',
  lead='If you are buying a boat in Spain, or you have already agreed the deal with the seller, I handle the paperwork so it ends up in your name: the change of ownership and, if needed, the change of flag. A nautical agency I work with processes it, and you only deal with me.',
  toc=[('que', 'What I handle'), ('como', 'How it works'), ('docs', 'Documents usually required'), ('antes', 'If you have not bought it yet'), ('pedir', 'Request the service'), ('faq', 'FAQ')],
  que=[('Change of ownership', 'Transferring the boat from seller to buyer, between private individuals or when buying from a company.'),
       ('Change of flag', 'Bringing a boat from another country under the Spanish flag, or flagging it abroad if that suits you better.'),
       ('Change of list', 'If you are moving the boat from private use (7th list) to charter (6th list), or the other way round.'),
       ('Check before you pay', 'Before paying, we check the boat is registered to the person selling it and that the paperwork is in order.')],
  como=[('You tell me about your case', 'Which boat, where it is, which flag it has and whether it is already bought or agreed.'),
        ('I tell you what is needed', 'The list of documents for your case and a fixed written quote before we start.'),
        ('We process it', 'The agency handles the procedure and I keep you updated until the papers are in your name.')],
  docs_intro='Every case is different, but this is what is usually required for a change of ownership between private individuals:',
  docs=['ID card, NIE or passport of buyer and seller.', 'Purchase contract signed by both.', 'The boat’s documents: registration or seaworthiness certificate and, if it has one, the registry entry sheet.',
        'Proof that the purchase tax has been paid (between private individuals, usually the regional transfer tax, ITP).', 'If the flag changes, the papers from the original registry and its deletion.'],
  docs_note='I will confirm the exact list for your case before we start.',
  antes_h='If you have not bought it yet',
  antes='Even better: this is the time to avoid surprises. Before paying, it is worth checking that the seller is the registered owner, that the boat has no charges against it and that the papers match the boat (length, engine, hull number). If you want to reserve it, I recommend doing so with a deposit agreement (arras).',
  pedir_h='Request the service', pedir_p='Tell me the basics and I will tell you what your case needs. No obligation.',
  f=dict(n='Name', t='Phone', e='Email', opt='(optional)', tr='What you need', tro=['Change of ownership', 'Change of flag', 'Both', 'Not sure'],
         b='Boat (make, model and length)', bp='Beneteau Antares 8, 7.9 m', s='Situation', so=['I have already bought it', 'The deal is agreed', 'I am still looking'],
         fl='Current flag', flp='Spanish, French…', m='Anything else', mp='Where the boat is, timing…', send='Send',
         legal='Controller: Juan Morante (Plata Marine). I use your details only to reply to you and, if you ask me to, to prepare the procedure with the partner agency. I do not share them with anyone else. You can exercise your rights at juan@platamarine.com. <a href="/en/privacidad">Privacy policy</a>.',
         ck='I have read the privacy information and agree to you using these details to reply to me.', req='Fields marked * are required.'),
  wa_txt='Prefer WhatsApp?', wa_btn='Message me on WhatsApp', wa_msg='Hi Juan, I need to transfer the ownership of a boat.',
  faq=[('How much does it cost?', 'It depends on the boat and the procedure. Before we start I send you a fixed written quote, with fees and tax shown separately so you can see what each item is.'),
       ('Do I need to go anywhere in person?', 'It is usually done with the paperwork. If your case needs a signature in person, I will tell you from the start.'),
       ('Can I use this if I did not buy the boat through you?', 'Yes. It does not matter where you found it: if the deal is agreed or the boat is already yours, I will help you with the papers.'),
       ('Who pays the purchase tax?', 'In a sale between private individuals it is usually the buyer. You can see the details by region in the ITP guide.')],
  small='For guidance only: requirements and taxes can change and depend on each case. We confirm everything in writing before we start.',
  aside_e='Deal agreed?', aside_h='Let’s close it properly.', aside_p='Tell me which boat it is and where you are in the process.', aside_b='Talk to Juan on WhatsApp',
  toc_e='On this page', rel_e='You may also be interested in',
  rel=[('/en/guias/papeles-vender-barco-cambio-titularidad', 'Paperwork to sell a boat'), ('/en/guias/itp-comprar-barco-usado-por-comunidad', 'Transfer tax on a used boat'), ('/en/guias/arras-compraventa-barco', 'Deposit agreement (arras)'), ('/en/guias/bandera-polaca-abanderar-barco-otro-pais', 'Polish flag'), ('/en/guias/listas-matricula-barcos-espana', 'Spanish registration lists')],
  wabtn='Talk to Juan', svc_card=('Change of ownership and flag', 'If you are buying a boat or the deal is agreed, I handle the paperwork so it ends up in your name.', 'See the service'),
  link_guide='Would you rather we handled it? <a href="{u}">We take care of the change of ownership and flag</a>.',
 ),
 'fr': dict(
  title='Changement de propriétaire d’un bateau en Espagne',
  desc='Vous achetez un bateau en Espagne ? Nous gérons le changement de propriétaire et de pavillon avec une agence nautique partenaire et un seul interlocuteur.',
  crumb='Services', eyebrow='Services · Papiers du bateau',
  h1='Changement de propriétaire et de pavillon de votre bateau',
  meta='<span>Par Juan Morante</span><span>Mis à jour en novembre 2026</span>',
  lead='Si vous achetez un bateau en Espagne, ou si l’affaire est déjà conclue avec le vendeur, je m’occupe des papiers pour qu’il soit à votre nom : le changement de propriétaire et, si besoin, le changement de pavillon. Une agence nautique avec laquelle je travaille s’occupe de la démarche et vous ne traitez qu’avec moi.',
  toc=[('que', 'Ce que je gère'), ('como', 'Comment ça marche'), ('docs', 'Documents habituellement demandés'), ('antes', 'Si vous ne l’avez pas encore acheté'), ('pedir', 'Demander la gestion'), ('faq', 'Questions fréquentes')],
  que=[('Changement de propriétaire', 'Le transfert du bateau du vendeur à l’acheteur, entre particuliers ou en achetant à une société.'),
       ('Changement de pavillon', 'Passer sous pavillon espagnol un bateau venant d’un autre pays, ou le faire immatriculer ailleurs si cela vous convient mieux.'),
       ('Changement de liste', 'Si le bateau passe d’un usage privé (7e liste) à la location (6e liste), ou l’inverse.'),
       ('Vérification préalable', 'Avant de payer, nous vérifions que le bateau est au nom de la personne qui le vend et que les papiers sont en règle.')],
  como=[('Vous m’expliquez votre cas', 'Quel bateau, où il se trouve, quel pavillon et s’il est déjà acheté ou si l’affaire est conclue.'),
        ('Je vous dis ce qu’il faut', 'La liste des documents pour votre cas et un devis ferme par écrit avant de commencer.'),
        ('Nous nous en occupons', 'L’agence fait la démarche et je vous tiens informé jusqu’à ce que les papiers soient à votre nom.')],
  docs_intro='Chaque cas est différent, mais voici ce qui est habituellement demandé pour un changement de propriétaire entre particuliers :',
  docs=['Pièce d’identité, NIE ou passeport de l’acheteur et du vendeur.', 'Contrat de vente signé par les deux.', 'Les papiers du bateau : certificat d’immatriculation ou de navigabilité et, s’il existe, la feuille d’inscription au registre.',
        'Le justificatif de paiement de l’impôt de l’achat (entre particuliers, en général l’ITP de la communauté autonome).', 'Si le pavillon change, les papiers du registre d’origine et sa radiation.'],
  docs_note='Je vous confirme la liste exacte pour votre cas avant de commencer.',
  antes_h='Si vous ne l’avez pas encore acheté',
  antes='C’est encore mieux : c’est le moment d’éviter les mauvaises surprises. Avant de payer, il faut vérifier que le vendeur est bien le propriétaire, que le bateau n’a pas de charges et que les papiers correspondent au bateau (longueur, moteur, numéro de coque). Pour le réserver, je vous conseille un contrat d’arrhes (arras).',
  pedir_h='Demander la gestion', pedir_p='Dites-moi l’essentiel et je vous dirai ce qu’il faut dans votre cas. Sans engagement.',
  f=dict(n='Nom', t='Téléphone', e='E-mail', opt='(facultatif)', tr='Ce dont vous avez besoin', tro=['Changement de propriétaire', 'Changement de pavillon', 'Les deux', 'Je ne sais pas encore'],
         b='Bateau (marque, modèle et longueur)', bp='Beneteau Antares 8, 7,9 m', s='Situation', so=['Je l’ai déjà acheté', 'L’affaire est conclue', 'Je cherche encore'],
         fl='Pavillon actuel', flp='Espagnol, français…', m='Autre chose', mp='Où se trouve le bateau, délais…', send='Envoyer',
         legal='Responsable : Juan Morante (Plata Marine). J’utilise vos données uniquement pour vous répondre et, si vous me le demandez, préparer la démarche avec l’agence partenaire. Je ne les cède à personne d’autre. Vous pouvez exercer vos droits à juan@platamarine.com. <a href="/fr/privacidad">Politique de confidentialité</a>.',
         ck='J’ai lu les informations sur la confidentialité et j’accepte que vous utilisiez ces données pour me répondre.', req='Les champs marqués * sont obligatoires.'),
  wa_txt='Vous préférez WhatsApp ?', wa_btn='M’écrire sur WhatsApp', wa_msg='Bonjour Juan, je dois faire le changement de propriétaire d’un bateau.',
  faq=[('Combien ça coûte ?', 'Cela dépend du bateau et de la démarche. Avant de commencer, je vous envoie un devis ferme par écrit, avec les taxes et l’impôt à part pour que vous voyiez chaque poste.'),
       ('Dois-je me déplacer ?', 'En général, tout se fait avec les documents. Si votre cas demande une signature en personne, je vous le dis dès le départ.'),
       ('Puis-je le faire si je n’ai pas acheté le bateau chez vous ?', 'Oui. Peu importe où vous l’avez trouvé : si l’affaire est conclue ou si le bateau est déjà à vous, je vous aide avec les papiers.'),
       ('Qui paie l’impôt de l’achat ?', 'Dans une vente entre particuliers, c’est en général l’acheteur. Les détails par région sont dans le guide de l’ITP.')],
  small='Information indicative : les exigences et les impôts peuvent changer et dépendent de chaque cas. Nous vous confirmons tout par écrit avant de commencer. Je ne parle pas français : j’utilise un traducteur.',
  aside_e='Affaire conclue ?', aside_h='Je vous aide à bien la finaliser.', aside_p='Dites-moi quel bateau et où vous en êtes.', aside_b='Parler à Juan sur WhatsApp',
  toc_e='Sur cette page', rel_e='Cela peut aussi vous intéresser',
  rel=[('/fr/guias/papeles-vender-barco-cambio-titularidad', 'Papiers pour vendre un bateau'), ('/fr/guias/itp-comprar-barco-usado-por-comunidad', 'ITP à l’achat d’un bateau d’occasion'), ('/fr/guias/arras-compraventa-barco', 'Contrat d’arrhes'), ('/fr/guias/bandera-polaca-abanderar-barco-otro-pais', 'Pavillon polonais'), ('/fr/guias/listas-matricula-barcos-espana', 'Listes d’immatriculation')],
  wabtn='Parler à Juan', svc_card=('Changement de propriétaire et de pavillon', 'Si vous achetez un bateau ou si l’affaire est conclue, je gère les papiers pour qu’il soit à votre nom.', 'Voir le service'),
  link_guide='Vous préférez que nous nous en occupions ? <a href="{u}">Nous gérons le changement de propriétaire et de pavillon</a>.',
 ),
}


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def url(lang):
    return f'{BASE}{PRE[lang]}/servicios/{SLUG}'


def main_html(L, t):
    f = t['f']
    wa = WA + urllib.parse.quote(t['wa_msg'])
    que = ''.join(f'<li><b>{a}.</b> {b}</li>' for a, b in t['que'])
    como = ''.join(f'<li><b>{a}.</b> {b}</li>' for a, b in t['como'])
    docs = ''.join(f'<li>{d}</li>' for d in t['docs'])
    faq = ''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in t['faq'])
    tro = ''.join(f'<option>{o}</option>' for o in f['tro'])
    so = ''.join(f'<option>{o}</option>' for o in f['so'])
    form = (f'<div class="pm-amf" id="pedir-gestion"><p>{t["pedir_p"]}</p><form id="pmTram" novalidate>'
            f'<div><label for="tr_n">{f["n"]} <i>*</i></label><input id="tr_n" name="nombre" type="text" required autocomplete="name" maxlength="80"></div>'
            f'<div><label for="tr_t">{f["t"]} <i>*</i></label><input id="tr_t" name="telefono" type="tel" placeholder="600 000 000" required autocomplete="tel" maxlength="80"></div>'
            f'<div class="s2"><label for="tr_e">{f["e"]} <small>{f["opt"]}</small></label><input id="tr_e" name="email" type="email" placeholder="nombre@gmail.com" autocomplete="email" maxlength="100"></div>'
            f'<div><label for="tr_q">{f["tr"]} <i>*</i></label><select id="tr_q" name="tramite" required><option value=""></option>{tro}</select></div>'
            f'<div><label for="tr_s">{f["s"]} <i>*</i></label><select id="tr_s" name="situacion" required><option value=""></option>{so}</select></div>'
            f'<div><label for="tr_b">{f["b"]} <i>*</i></label><input id="tr_b" name="barco" type="text" placeholder="{esc(f["bp"])}" required maxlength="100"></div>'
            f'<div><label for="tr_f">{f["fl"]} <small>{f["opt"]}</small></label><input id="tr_f" name="bandera" type="text" placeholder="{esc(f["flp"])}" maxlength="60"></div>'
            f'<div class="s2"><label for="tr_x">{f["m"]} <small>{f["opt"]}</small></label><textarea id="tr_x" name="mensaje" maxlength="1000" placeholder="{esc(f["mp"])}"></textarea></div>'
            f'<p class="help s2">{f["legal"]}</p>'
            f'<div class="s2"><label class="ck" for="tr_ok"><input id="tr_ok" name="privacidad" type="checkbox" required><span>{f["ck"]}&nbsp;<i>*</i></span></label></div>'
            f'<div class="s2"><button type="submit">{f["send"]}</button></div><p class="help s2">{f["req"]}</p>'
            f'<p class="pm-amst s2" role="status" aria-live="polite" hidden></p></form></div>')
    toc = ''.join(f'<li><a href="#{i}">{n}</a></li>' for i, n in t['toc'])
    rel = ''.join(f'<a href="{u}">{n}</a>' for u, n in t['rel'])
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
        <h2 id="que">{t["toc"][0][1]}</h2>
        <ul>{que}</ul>
        <h2 id="como">{t["toc"][1][1]}</h2>
        <ol>{como}</ol>
        <h2 id="docs">{t["toc"][2][1]}</h2>
        <p>{t["docs_intro"]}</p>
        <ul>{docs}</ul>
        <p>{t["docs_note"]}</p>
        <h2 id="antes">{t["antes_h"]}</h2>
        <p>{t["antes"]}</p>
        <h2 id="pedir">{t["pedir_h"]}</h2>
        {form}
        <p class="help">{t["wa_txt"]} <a href="{wa}" target="_blank" rel="noopener">{t["wa_btn"]}</a></p>
        <h2 id="faq">{t["toc"][5][1]}</h2>
        {faq}
        <p class="muted" style="font-size:.82rem;margin-top:26px">{t["small"]}</p>
      </div>
    </article>

    <aside class="aside" aria-label="Contacto">
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
    src = ROOT / (PRE[L].lstrip('/') + '/' if PRE[L] else '') / 'servicios' / 'amarres.html'
    h = src.read_text(encoding='utf-8')
    old_url = f'{BASE}{PRE[L]}/servicios/amarres'
    # cabecera
    full_title = f'{t["title"]} | Plata Marine' if len(t['title']) <= 46 else t['title']
    h = re.sub(r'<title>.*?</title>', f'<title>{full_title}</title>', h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(t["desc"])}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(full_title)}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(t["desc"])}">', h, count=1)
    for l2 in PRE:
        h = h.replace(f'{BASE}{PRE[l2]}/servicios/amarres"', f'{BASE}{PRE[l2]}/servicios/{SLUG}"')
    # breadcrumb + FAQ
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f'{BASE}{PRE[L]}/'},
        {"@type": "ListItem", "position": 2, "name": t['crumb'], "item": f'{BASE}{PRE[L]}/servicios/'},
        {"@type": "ListItem", "position": 3, "name": t['h1'], "item": url(L)}]}
    fq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t['faq']]}
    h = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>',
               lambda m: '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + '</script>\n<script type="application/ld+json">' + json.dumps(fq, ensure_ascii=False) + '</script>', h, count=1, flags=re.S)
    # cuerpo
    h = re.sub(r'<main class="art">.*?</main>', lambda m: main_html(L, t), h, count=1, flags=re.S)
    # script del formulario
    h = h.replace('<script src="/guias/amarres-forms.js?v=20261018" defer></script>', '<script src="/servicios/tramites-forms.js?v=20261101" defer></script>')
    # botón de cabecera
    h = re.sub(r'(<a class="btn btn-wa" href=")https://wa\.me/[^"]*(" target="_blank" rel="noopener">)', lambda m: m.group(1) + WA + urllib.parse.quote(t['wa_msg']) + m.group(2), h, count=1)
    h = re.sub(r'(/servicios/amarres")\s*aria-current="page"', r'\1', h)
    assert 'amarres-forms' not in h and SLUG in h
    out = src.parent / f'{SLUG}.html'
    out.write_text(h, encoding='utf-8')
    return out


if __name__ == '__main__':
    for L in T:
        print(build(L))


def link_everywhere():
    """Enlaces desde servicios, papeles e impuestos y la guía de papeles; sitemap."""
    import datetime
    for L, t in T.items():
        p = PRE[L]
        u = f'{p}/servicios/{SLUG}'
        par = '<p class="pm-tram-link">' + t['link_guide'].format(u=u) + '</p>'
        root = ROOT / (p.lstrip('/') + '/' if p else '')
        # servicios/index: tras el primer párrafo de #gestoria
        f = root / 'servicios' / 'index.html'; h = f.read_text(encoding='utf-8')
        if 'pm-tram-link' not in h:
            i = h.index('id="gestoria"'); j = h.index('</p>', i) + 4
            h = h[:j] + '\n        ' + par + h[j:]; f.write_text(h, encoding='utf-8')
        # guía de papeles: tras el lead
        f = root / 'guias' / 'papeles-vender-barco-cambio-titularidad.html'; h = f.read_text(encoding='utf-8')
        if 'pm-tram-link' not in h:
            i = h.index('class="lead"'); j = h.index('</p>', i) + 4
            h = h[:j] + '\n        ' + par + h[j:]; f.write_text(h, encoding='utf-8')
        # papeles e impuestos: dentro del bloque final
        f = root / 'papeles-fiscalidad' / 'index.html'; h = f.read_text(encoding='utf-8')
        if 'pm-tram-link' not in h:
            k = h.rfind('<a class="btn btn-wa"')
            i = h.rfind('</p>', 0, k) + 4
            h = h[:i] + '\n        ' + par.replace('<p class="pm-tram-link">', '<p class="pm-tram-link" style="margin:8px 0 0">') + h[i:]; f.write_text(h, encoding='utf-8')
    f = ROOT / 'sitemap.xml'; h = f.read_text(encoding='utf-8')
    if SLUG not in h:
        today = datetime.date.today().isoformat()
        add = ''.join(f'    <url><loc>{BASE}{PRE[L]}/servicios/{SLUG}</loc><lastmod>{today}</lastmod><priority>{"0.7" if L == "es" else "0.6"}</priority></url>\n' for L in T)
        h = h.replace('</urlset>', add + '</urlset>'); f.write_text(h, encoding='utf-8')


if __name__ == '__main__':
    link_everywhere()
