# -*- coding: utf-8 -*-
"""Guía (ES/CA/EN/FR): /guias/listas-matricula-barcos-espana.html — las 9 listas del Registro de Matrícula (RD 1027/1989, art. 4).
Reutiliza cabecera/pie y utilidades de build_astilleros_charter.py. Añade la tarjeta en guias/index.html de cada idioma.
Uso: python3 _tools/build_guia_listas.py"""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(__file__))
import build_astilleros_charter as B

FN = 'listas-matricula-barcos-espana.html'
IMG = 'https://images.unsplash.com/photo-1760446005737-fb250add7d17?auto=format&fit=crop&w=800&q=70'
IDS = ['que', 'leer', 'nueve', 'recreo', 'pesca', 'novena', 'comprar']

def table(head, rows):
    h = ''.join('<th>%s</th>' % c for c in head)
    r = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in row) for row in rows)
    return '<div class="tbl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (h, r)

C = {
'es': dict(
  title='Listas de matrícula de barcos en España: las 9 listas explicadas',
  desc='Qué significa la lista de la matrícula de un barco: de la 1ª a la 9ª, qué se inscribe en cada una, cómo se lee la matrícula y qué mirar si compras un barco que viene de pesca o de alquiler.',
  h1='Las 9 listas de matrícula de barcos en España, explicadas', eyebrow='Guías · Listas',
  meta=['Por Juan Morante', 'Actualizado octubre 2026', '6 min de lectura'], crumb='Las 9 listas de matrícula',
  lead='Todo barco matriculado en España está inscrito en una “lista”, y ese número es lo primero que aparece en su matrícula. Si compras o vendes un barco de recreo, casi siempre verás la 6ª o la 7ª, pero en el mercado de ocasión también aparecen barcos que vienen de la pesca o de un organismo público. Aquí tienes las nueve, qué significa cada una y qué te afecta.',
  s=dict(
   que=('Qué es una lista', '<p>El Registro de Matrícula de Buques lo lleva cada Capitanía Marítima, y se organiza en libros llamados “listas”. Cada barco se inscribe en la que corresponde a su procedencia y a su actividad. Lo regula el artículo 4 del Real Decreto 1027/1989, de abanderamiento y matriculación de buques. Para las embarcaciones de recreo de 2,5 a 24 metros se aplica además el Real Decreto 1435/2010.</p>'),
   leer=('Cómo se lee una matrícula', '<p>La matrícula (el “indicativo de matrícula”) combina, en este orden, la <strong>lista</strong>, la <strong>provincia marítima</strong>, el <strong>distrito marítimo</strong> y el <strong>folio</strong> con el año de inscripción. Por ejemplo, una matrícula del tipo <em>7ª-BA-2-123-18</em> se leería como lista 7ª, provincia marítima de Barcelona, distrito 2, folio 123, inscrita en 2018 (es un ejemplo inventado para explicar el formato).</p><p>En las embarcaciones de recreo tiene que ir en las dos amuras, lo más alta posible sobre la línea de flotación, de un tamaño legible y en un color que contraste con el casco. Las auxiliares llevan la matrícula del barco principal con “Aux” entre paréntesis.</p>'),
   nueve=('Las 9 listas, una por una', None),
   recreo=('6ª y 7ª: las que importan en recreo', '<p>La diferencia entre las dos es el ánimo de lucro. En la <strong>6ª</strong> van los barcos de recreo que se explotan comercialmente (alquiler, chárter); en la <strong>7ª</strong>, los de uso privado, para navegar, hacer deporte o pescar sin ser profesional. Cambia el impuesto de matriculación, las inspecciones y los seguros; lo tienes desarrollado en la guía de <a href="lista-6-y-lista-7.html">lista 6ª y lista 7ª</a>, y si te planteas alquilar tu barco, en <a href="alquilar-mi-barco-charter.html">¿Puedo alquilar mi barco para pagar los gastos?</a>.</p><p>Las embarcaciones de recreo con marcado CE de hasta 12 metros tienen además un régimen de inscripción simplificado (artículo 8 del RD 1435/2010). Si tu caso es ese, pide que te lo confirmen en Capitanía.</p>'),
   pesca=('3ª y 4ª: barcos que vienen de la pesca', '<p>De vez en cuando salen a la venta barcos inscritos en la 3ª (pesca profesional) o en la 4ª (auxiliares de pesca y de acuicultura). Muchos llaüts y barcas de madera tienen ese origen. Para usarlos como barco de recreo hay que tramitar el cambio a la 7ª en Capitanía Marítima, y eso puede pedir inspección, documentación y adaptar el equipo de seguridad.</p><p>Antes de comprar uno, pregunta en qué lista está hoy, si el cambio ya está hecho y qué falta. No des por hecho que lo puedes usar como un barco de recreo cualquiera mientras siga en una lista de pesca.</p>'),
   novena=('9ª y lista complementaria', '<p>La <strong>9ª</strong> es un registro provisional: ahí se anotan los barcos en construcción desde que se autoriza la obra, salvo las embarcaciones deportivas fabricadas en serie. Cuando el barco se termina, se cancela esa inscripción y se abre la definitiva en la lista que le corresponda.</p><p>Aparte, los barcos importados con abanderamiento provisional se inscriben en una <strong>lista especial complementaria</strong> de la lista que les toque (artículo 4.2 del RD 1027/1989).</p>'),
   comprar=('Qué mirar si compras', '<ol><li>La lista que figura hoy en la documentación, y que coincida con la matrícula del casco.</li><li>Si viene de la 6ª, la fecha en que pasó a uso comercial y si hay impuesto de matriculación pendiente.</li><li>Si viene de la 3ª o la 4ª, si el cambio a la 7ª ya está hecho.</li><li>Si es una lista 8ª (organismo público), cómo se ha dado de baja y con qué documentos se transmite.</li></ol><p>Si tienes dudas con un barco concreto, mándame la matrícula y la documentación y te digo qué comprobar.</p>')),
  thead=['Lista', 'Qué se inscribe', '¿Te afecta si compras un barco de recreo?'],
  rows=[['1ª', 'Plataformas de extracción del subsuelo marino, remolcadores de altura y buques de apoyo o suministro a esas plataformas.', 'No.'],
        ['2ª', 'Buques de transporte marítimo de pasajeros, de mercancías o de ambos.', 'No.'],
        ['3ª', 'Buques de pesca profesional: captura y extracción de pescado y otros recursos marinos con fines comerciales.', 'A veces: barcos de pesca que se venden para recreo.'],
        ['4ª', 'Embarcaciones auxiliares de pesca y de acuicultura, y artefactos para el cultivo de especies marinas.', 'A veces, como la 3ª.'],
        ['5ª', 'Remolcadores, embarcaciones y artefactos de servicios de puertos, radas y bahías.', 'Muy raramente.'],
        ['6ª', 'Barcos y embarcaciones de recreo que se explotan con ánimo de lucro (alquiler, chárter).', 'Sí: barcos que vienen del alquiler.'],
        ['7ª', 'Barcos y embarcaciones de recreo de uso privado: deporte sin ánimo de lucro o pesca no profesional.', 'Sí: es la lista normal de un particular.'],
        ['8ª', 'Buques y embarcaciones de organismos públicos (Estado, comunidades autónomas, entidades locales).', 'Rara vez: subastas de barcos públicos.'],
        ['9ª', 'Registro provisional de barcos en construcción, salvo embarcaciones deportivas fabricadas en serie.', 'Solo si encargas un barco a medida.']],
  fine='Información orientativa basada en el Real Decreto 1027/1989 (art. 4, texto consolidado del BOE) y el Real Decreto 1435/2010, revisada en octubre de 2026. No es asesoramiento legal y la normativa puede cambiar. Confirma cualquier trámite con la Capitanía Marítima o con una gestoría náutica.',
  next_eyebrow='Siguiente paso', next_p='<strong>¿Miras un barco y no tienes clara su lista?</strong> Te digo qué comprobar antes de hacer una oferta.', next_btn='Ver barcos en venta', next_href='/barcos/',
  aside_eyebrow='¿Dudas con una matrícula?', aside_h='Mándamela y te digo qué significa.', aside_p='Con la matrícula y la documentación te digo en qué lista está y qué mirar. Sin compromiso.', aside_btn='Hablar con Juan por WhatsApp',
  wa='Hola Juan, tengo una duda sobre la lista de matrícula de un barco.',
  toc=['Qué es una lista', 'Cómo se lee una matrícula', 'Las 9 listas', '6ª y 7ª', '3ª y 4ª: pesca', '9ª y complementaria', 'Qué mirar si compras'],
  rel=[('lista-6-y-lista-7.html', 'Lista 6ª y lista 7ª'), ('papeles-vender-barco-cambio-titularidad.html', 'Papeles para vender un barco'), ('./', 'Todas las guías de Plata Marine')],
  card=('Listas', 'Las 9 listas de matrícula de barcos en España', 'De la 1ª a la 9ª: qué se inscribe en cada lista, cómo se lee una matrícula y qué mirar si el barco viene de la pesca o del alquiler.')),
'ca': dict(
  title='Llistes de matrícula de vaixells a Espanya: les 9 llistes explicades',
  desc='Què vol dir la llista de la matrícula d’un vaixell: de la 1a a la 9a, què s’inscriu a cadascuna, com es llegeix la matrícula i què mirar si compres un vaixell que ve de la pesca o del lloguer.',
  h1='Les 9 llistes de matrícula de vaixells a Espanya, explicades', eyebrow='Guies · Llistes',
  meta=['Per Juan Morante', 'Actualitzat octubre 2026', '6 min de lectura'], crumb='Les 9 llistes de matrícula',
  lead='Tot vaixell matriculat a Espanya està inscrit en una “llista”, i aquest número és el primer que apareix a la matrícula. Si compres o vens un vaixell d’esbarjo, gairebé sempre veuràs la 6a o la 7a, però al mercat d’ocasió també apareixen vaixells que vénen de la pesca o d’un organisme públic. Aquí tens les nou, què vol dir cadascuna i què t’afecta.',
  s=dict(
   que=('Què és una llista', '<p>El Registre de Matrícula de Vaixells el porta cada Capitania Marítima, i s’organitza en llibres anomenats “llistes”. Cada vaixell s’inscriu a la que correspon a la seva procedència i a la seva activitat. Ho regula l’article 4 del Reial decret 1027/1989, d’abanderament i matriculació de vaixells. Per a les embarcacions d’esbarjo de 2,5 a 24 metres s’aplica a més el Reial decret 1435/2010.</p>'),
   leer=('Com es llegeix una matrícula', '<p>La matrícula (l’“indicatiu de matrícula”) combina, en aquest ordre, la <strong>llista</strong>, la <strong>província marítima</strong>, el <strong>districte marítim</strong> i el <strong>foli</strong> amb l’any d’inscripció. Per exemple, una matrícula del tipus <em>7ª-BA-2-123-18</em> es llegiria com a llista 7a, província marítima de Barcelona, districte 2, foli 123, inscrita el 2018 (és un exemple inventat per explicar el format).</p><p>A les embarcacions d’esbarjo ha d’anar a totes dues amures, tan alta com sigui possible sobre la línia de flotació, d’una mida llegible i d’un color que contrasti amb el buc. Les auxiliars porten la matrícula del vaixell principal amb “Aux” entre parèntesis.</p>'),
   nueve=('Les 9 llistes, una per una', None),
   recreo=('6a i 7a: les que importen en esbarjo', '<p>La diferència entre les dues és l’ànim de lucre. A la <strong>6a</strong> hi van els vaixells d’esbarjo que s’exploten comercialment (lloguer, xàrter); a la <strong>7a</strong>, els d’ús privat, per navegar, fer esport o pescar sense ser professional. Canvia l’impost de matriculació, les inspeccions i les assegurances; ho tens desenvolupat a la guia de la <a href="lista-6-y-lista-7.html">llista 6a i la llista 7a</a>, i si et planteges llogar el teu vaixell, a <a href="alquilar-mi-barco-charter.html">Puc llogar el meu vaixell per pagar les despeses?</a>.</p><p>Les embarcacions d’esbarjo amb marcatge CE de fins a 12 metres tenen a més un règim d’inscripció simplificat (article 8 del RD 1435/2010). Si és el teu cas, demana que t’ho confirmin a Capitania.</p>'),
   pesca=('3a i 4a: vaixells que vénen de la pesca', '<p>De tant en tant surten a la venda vaixells inscrits a la 3a (pesca professional) o a la 4a (auxiliars de pesca i d’aqüicultura). Molts llaüts i barques de fusta tenen aquest origen. Per fer-los servir com a vaixell d’esbarjo cal tramitar el canvi a la 7a a Capitania Marítima, i això pot demanar inspecció, documentació i adaptar l’equip de seguretat.</p><p>Abans de comprar-ne un, pregunta en quina llista és avui, si el canvi ja està fet i què hi falta. No donis per fet que el pots fer servir com un vaixell d’esbarjo qualsevol mentre continuï en una llista de pesca.</p>'),
   novena=('9a i llista complementària', '<p>La <strong>9a</strong> és un registre provisional: s’hi anoten els vaixells en construcció des que s’autoritza l’obra, excepte les embarcacions esportives fabricades en sèrie. Quan el vaixell s’acaba, es cancel·la aquesta inscripció i s’obre la definitiva a la llista que li correspongui.</p><p>A part, els vaixells importats amb abanderament provisional s’inscriuen en una <strong>llista especial complementària</strong> de la llista que els toqui (article 4.2 del RD 1027/1989).</p>'),
   comprar=('Què mirar si compres', '<ol><li>La llista que figura avui a la documentació, i que coincideixi amb la matrícula del buc.</li><li>Si ve de la 6a, la data en què va passar a ús comercial i si hi ha impost de matriculació pendent.</li><li>Si ve de la 3a o la 4a, si el canvi a la 7a ja està fet.</li><li>Si és una llista 8a (organisme públic), com s’ha donat de baixa i amb quins documents es transmet.</li></ol><p>Si tens dubtes amb un vaixell concret, envia’m la matrícula i la documentació i et dic què cal comprovar.</p>')),
  thead=['Llista', 'Què s’hi inscriu', 'T’afecta si compres un vaixell d’esbarjo?'],
  rows=[['1a', 'Plataformes d’extracció del subsòl marí, remolcadors d’altura i vaixells de suport o subministrament a aquestes plataformes.', 'No.'],
        ['2a', 'Vaixells de transport marítim de passatgers, de mercaderies o de tots dos.', 'No.'],
        ['3a', 'Vaixells de pesca professional: captura i extracció de peix i altres recursos marins amb finalitats comercials.', 'De vegades: vaixells de pesca que es venen per a esbarjo.'],
        ['4a', 'Embarcacions auxiliars de pesca i d’aqüicultura, i artefactes per al cultiu d’espècies marines.', 'De vegades, com la 3a.'],
        ['5a', 'Remolcadors, embarcacions i artefactes de serveis de ports, rades i badies.', 'Molt rarament.'],
        ['6a', 'Vaixells i embarcacions d’esbarjo que s’exploten amb ànim de lucre (lloguer, xàrter).', 'Sí: vaixells que vénen del lloguer.'],
        ['7a', 'Vaixells i embarcacions d’esbarjo d’ús privat: esport sense ànim de lucre o pesca no professional.', 'Sí: és la llista normal d’un particular.'],
        ['8a', 'Vaixells i embarcacions d’organismes públics (Estat, comunitats autònomes, ens locals).', 'Rarament: subhastes de vaixells públics.'],
        ['9a', 'Registre provisional de vaixells en construcció, excepte embarcacions esportives fabricades en sèrie.', 'Només si encarregues un vaixell a mida.']],
  fine='Informació orientativa basada en el Reial decret 1027/1989 (art. 4, text consolidat del BOE) i el Reial decret 1435/2010, revisada l’octubre de 2026. No és assessorament legal i la normativa pot canviar. Confirma qualsevol tràmit amb la Capitania Marítima o amb una gestoria nàutica.',
  next_eyebrow='Següent pas', next_p='<strong>Mires un vaixell i no tens clara la seva llista?</strong> Et dic què comprovar abans de fer una oferta.', next_btn='Veure vaixells en venda', next_href='/ca/barcos/',
  aside_eyebrow='Dubtes amb una matrícula?', aside_h='Envia-me-la i et dic què vol dir.', aside_p='Amb la matrícula i la documentació et dic en quina llista és i què mirar. Sense compromís.', aside_btn='Parla amb en Juan per WhatsApp',
  wa='Hola Juan, tinc un dubte sobre la llista de matrícula d’un vaixell.',
  toc=['Què és una llista', 'Com es llegeix una matrícula', 'Les 9 llistes', '6a i 7a', '3a i 4a: pesca', '9a i complementària', 'Què mirar si compres'],
  rel=[('lista-6-y-lista-7.html', 'Llista 6a i llista 7a'), ('papeles-vender-barco-cambio-titularidad.html', 'Papers per vendre un vaixell'), ('./', 'Totes les guies de Plata Marine')],
  card=('Llistes', 'Les 9 llistes de matrícula de vaixells a Espanya', 'De la 1a a la 9a: què s’inscriu a cada llista, com es llegeix una matrícula i què mirar si el vaixell ve de la pesca o del lloguer.')),
'en': dict(
  title='Spanish boat registration lists: all 9 lists explained',
  desc='What the list in a Spanish boat registration means: from list 1 to list 9, what is registered in each, how to read the registration number and what to check if the boat comes from fishing or charter.',
  h1='The 9 Spanish boat registration lists, explained', eyebrow='Guides · Registration lists',
  meta=['By Juan Morante', 'Updated October 2026', '6 min read'], crumb='The 9 registration lists',
  lead='Every boat registered in Spain is entered on a “list”, and that number is the first thing in its registration. If you buy or sell a recreational boat you will nearly always see list 6 or 7, but the second-hand market also has boats that come from fishing or from a public body. Here are all nine, what each one means and which affect you.',
  s=dict(
   que=('What a list is', '<p>The Ship Registry (Registro de Matrícula de Buques) is kept by each Harbour Master’s Office (Capitanía Marítima) and is organised in books called “lists”. Each boat is entered on the one that matches its origin and activity. This is set out in article 4 of Royal Decree 1027/1989 on ship flagging and registration. For recreational boats from 2.5 to 24 metres, Royal Decree 1435/2010 also applies.</p>'),
   leer=('How to read a registration number', '<p>The registration (“indicativo de matrícula”) combines, in this order, the <strong>list</strong>, the <strong>maritime province</strong>, the <strong>maritime district</strong> and the <strong>folio</strong> with the year of registration. For example, a registration like <em>7ª-BA-2-123-18</em> would read as list 7, maritime province of Barcelona, district 2, folio 123, registered in 2018 (an invented example to show the format).</p><p>On recreational boats it must appear on both bows, as high as possible above the waterline, large enough to read and in a colour that contrasts with the hull. Tenders carry the main boat’s registration with “Aux” in brackets.</p>'),
   nueve=('The 9 lists, one by one', None),
   recreo=('Lists 6 and 7: the ones that matter for leisure boats', '<p>The difference between them is profit. <strong>List 6</strong> is for recreational boats run commercially (rental, charter); <strong>list 7</strong> is for private use: cruising, sport or non-professional fishing. Registration tax, inspections and insurance all change; it’s covered in detail in the guide to <a href="lista-6-y-lista-7.html">list 6 and list 7</a>, and if you’re thinking of renting out your boat, in <a href="alquilar-mi-barco-charter.html">Can I charter out my boat to cover the costs?</a>.</p><p>CE-marked recreational boats up to 12 metres also have a simplified registration regime (article 8 of RD 1435/2010). If that’s your case, ask the Harbour Master’s Office to confirm it.</p>'),
   pesca=('Lists 3 and 4: boats that come from fishing', '<p>Every now and then boats registered on list 3 (professional fishing) or list 4 (fishing and aquaculture auxiliaries) come up for sale. Many traditional llaüts and wooden boats have that origin. To use one as a leisure boat, the change to list 7 has to be processed at the Harbour Master’s Office, which may involve an inspection, paperwork and upgrading the safety equipment.</p><p>Before buying one, ask which list it is on today, whether the change has already been made and what is missing. Don’t assume you can use it like any other leisure boat while it is still on a fishing list.</p>'),
   novena=('List 9 and the complementary list', '<p><strong>List 9</strong> is a provisional register: boats under construction are entered there from the moment the build is authorised, except series-built sports boats. When the boat is finished, that entry is cancelled and the permanent one is opened on the appropriate list.</p><p>Separately, boats imported under provisional flag are entered on a <strong>special complementary list</strong> of the list that applies to them (article 4.2 of RD 1027/1989).</p>'),
   comprar=('What to check when buying', '<ol><li>The list shown today in the documents, and that it matches the registration on the hull.</li><li>If it comes from list 6, the date it switched to commercial use and whether any registration tax is outstanding.</li><li>If it comes from list 3 or 4, whether the change to list 7 has been completed.</li><li>If it is a list 8 boat (public body), how it was deregistered and which documents transfer it.</li></ol><p>If you have doubts about a specific boat, send me the registration and the documents and I’ll tell you what to check.</p>')),
  thead=['List', 'What is registered', 'Does it affect you when buying a leisure boat?'],
  rows=[['1', 'Offshore extraction platforms, ocean-going tugs and support or supply vessels for those platforms.', 'No.'],
        ['2', 'Ships carrying passengers, cargo or both.', 'No.'],
        ['3', 'Professional fishing vessels: catching and harvesting fish and other marine resources commercially.', 'Sometimes: fishing boats sold for leisure use.'],
        ['4', 'Fishing and aquaculture auxiliary boats, and structures for farming marine species.', 'Sometimes, like list 3.'],
        ['5', 'Tugs, boats and craft providing services in ports, roadsteads and bays.', 'Very rarely.'],
        ['6', 'Recreational boats run for profit (rental, charter).', 'Yes: boats coming out of charter.'],
        ['7', 'Recreational boats for private use: non-profit sport or non-professional fishing.', 'Yes: the normal list for a private owner.'],
        ['8', 'Ships and boats belonging to public bodies (central, regional or local government).', 'Rarely: auctions of public boats.'],
        ['9', 'Provisional register of boats under construction, except series-built sports boats.', 'Only if you order a custom build.']],
  fine='General information based on Royal Decree 1027/1989 (art. 4, BOE consolidated text) and Royal Decree 1435/2010, reviewed in October 2026. This is not legal advice and regulations may change. Confirm any procedure with the Harbour Master’s Office or a nautical gestoría.',
  next_eyebrow='Next step', next_p='<strong>Looking at a boat and unsure about its list?</strong> I’ll tell you what to check before you make an offer.', next_btn='See boats for sale', next_href='/en/barcos/',
  aside_eyebrow='Questions about a registration?', aside_h='Send it to me and I’ll tell you what it means.', aside_p='With the registration and the documents I’ll tell you which list it’s on and what to check. No obligation.', aside_btn='Talk to Juan on WhatsApp',
  wa='Hi Juan, I have a question about a boat’s registration list.',
  toc=['What a list is', 'How to read a registration', 'The 9 lists', 'Lists 6 and 7', 'Lists 3 and 4: fishing', 'List 9 and complementary', 'What to check when buying'],
  rel=[('lista-6-y-lista-7.html', 'List 6 and list 7'), ('papeles-vender-barco-cambio-titularidad.html', 'Paperwork to sell a boat'), ('./', 'All Plata Marine guides')],
  card=('Registration lists', 'The 9 Spanish boat registration lists', 'From list 1 to list 9: what each list covers, how to read a registration number and what to check if the boat comes from fishing or charter.')),
'fr': dict(
  title='Listes d’immatriculation des bateaux en Espagne : les 9 listes expliquées',
  desc='Ce que signifie la liste dans l’immatriculation d’un bateau espagnol : de la liste 1 à la 9, ce qui est inscrit dans chacune, comment lire l’immatriculation et quoi vérifier si le bateau vient de la pêche ou de la location.',
  h1='Les 9 listes d’immatriculation des bateaux en Espagne, expliquées', eyebrow='Guides · Listes d’immatriculation',
  meta=['Par Juan Morante', 'Mis à jour en octobre 2026', '6 min de lecture'], crumb='Les 9 listes d’immatriculation',
  lead='Tout bateau immatriculé en Espagne est inscrit sur une « liste », et ce numéro est le premier élément de son immatriculation. Si vous achetez ou vendez un bateau de plaisance, vous verrez presque toujours la liste 6 ou 7, mais le marché de l’occasion compte aussi des bateaux qui viennent de la pêche ou d’un organisme public. Voici les neuf, ce que signifie chacune et lesquelles vous concernent.',
  s=dict(
   que=('Qu’est-ce qu’une liste', '<p>Le registre d’immatriculation des navires est tenu par chaque Capitanía Marítima et organisé en livres appelés « listes ». Chaque bateau est inscrit sur celle qui correspond à son origine et à son activité. C’est l’article 4 du décret royal 1027/1989 sur le pavillon et l’immatriculation des navires qui le prévoit. Pour les bateaux de plaisance de 2,5 à 24 mètres, le décret royal 1435/2010 s’applique également.</p>'),
   leer=('Comment lire une immatriculation', '<p>L’immatriculation (« indicativo de matrícula ») combine, dans cet ordre, la <strong>liste</strong>, la <strong>province maritime</strong>, le <strong>district maritime</strong> et le <strong>folio</strong> avec l’année d’inscription. Par exemple, une immatriculation du type <em>7ª-BA-2-123-18</em> se lirait : liste 7, province maritime de Barcelone, district 2, folio 123, inscrite en 2018 (exemple inventé pour expliquer le format).</p><p>Sur les bateaux de plaisance, elle doit figurer sur les deux joues, le plus haut possible au-dessus de la ligne de flottaison, en taille lisible et dans une couleur qui contraste avec la coque. Les annexes portent l’immatriculation du bateau principal avec « Aux » entre parenthèses.</p>'),
   nueve=('Les 9 listes, une par une', None),
   recreo=('Listes 6 et 7 : celles qui comptent en plaisance', '<p>La différence entre les deux, c’est le but lucratif. La <strong>liste 6</strong> regroupe les bateaux de plaisance exploités commercialement (location, charter) ; la <strong>liste 7</strong>, ceux à usage privé : navigation, sport ou pêche non professionnelle. La taxe d’immatriculation, les inspections et les assurances changent ; tout est détaillé dans le guide <a href="lista-6-y-lista-7.html">liste 6 et liste 7</a>, et si vous pensez louer votre bateau, dans <a href="alquilar-mi-barco-charter.html">Puis-je louer mon bateau pour couvrir les frais ?</a>.</p><p>Les bateaux de plaisance marqués CE jusqu’à 12 mètres disposent en outre d’un régime d’inscription simplifié (article 8 du RD 1435/2010). Si c’est votre cas, faites-le confirmer par la Capitanía.</p>'),
   pesca=('Listes 3 et 4 : bateaux issus de la pêche', '<p>De temps en temps, des bateaux inscrits en liste 3 (pêche professionnelle) ou en liste 4 (auxiliaires de pêche et d’aquaculture) sont mis en vente. Beaucoup de llaüts et de barques en bois ont cette origine. Pour les utiliser en plaisance, il faut demander le passage en liste 7 à la Capitanía Marítima, ce qui peut impliquer une inspection, des documents et une mise à niveau de l’équipement de sécurité.</p><p>Avant d’en acheter un, demandez sur quelle liste il est aujourd’hui, si le changement est déjà fait et ce qui manque. Ne partez pas du principe que vous pouvez l’utiliser comme n’importe quel bateau de plaisance tant qu’il reste sur une liste de pêche.</p>'),
   novena=('Liste 9 et liste complémentaire', '<p>La <strong>liste 9</strong> est un registre provisoire : on y inscrit les bateaux en construction dès que les travaux sont autorisés, sauf les bateaux de sport construits en série. Une fois le bateau terminé, cette inscription est annulée et l’inscription définitive est ouverte sur la liste appropriée.</p><p>Par ailleurs, les bateaux importés sous pavillon provisoire sont inscrits sur une <strong>liste spéciale complémentaire</strong> de la liste qui les concerne (article 4.2 du RD 1027/1989).</p>'),
   comprar=('Quoi vérifier si vous achetez', '<ol><li>La liste qui figure aujourd’hui dans les documents, et qu’elle corresponde à l’immatriculation sur la coque.</li><li>S’il vient de la liste 6, la date de son passage à l’usage commercial et s’il reste une taxe d’immatriculation à payer.</li><li>S’il vient de la liste 3 ou 4, si le passage en liste 7 est terminé.</li><li>S’il s’agit d’un bateau en liste 8 (organisme public), comment il a été radié et avec quels documents il est cédé.</li></ol><p>Si vous avez un doute sur un bateau précis, envoyez-moi l’immatriculation et les documents et je vous dis quoi vérifier.</p>')),
  thead=['Liste', 'Ce qui est inscrit', 'Cela vous concerne-t-il pour un bateau de plaisance ?'],
  rows=[['1', 'Plateformes d’extraction en mer, remorqueurs de haute mer et navires d’appui ou de ravitaillement de ces plateformes.', 'Non.'],
        ['2', 'Navires de transport de passagers, de marchandises ou des deux.', 'Non.'],
        ['3', 'Navires de pêche professionnelle : capture et extraction de poissons et d’autres ressources marines à des fins commerciales.', 'Parfois : bateaux de pêche vendus pour la plaisance.'],
        ['4', 'Embarcations auxiliaires de pêche et d’aquaculture, et installations d’élevage d’espèces marines.', 'Parfois, comme la liste 3.'],
        ['5', 'Remorqueurs, embarcations et engins de services portuaires, de rades et de baies.', 'Très rarement.'],
        ['6', 'Bateaux de plaisance exploités dans un but lucratif (location, charter).', 'Oui : bateaux issus de la location.'],
        ['7', 'Bateaux de plaisance à usage privé : sport sans but lucratif ou pêche non professionnelle.', 'Oui : la liste normale d’un particulier.'],
        ['8', 'Navires et embarcations appartenant à des organismes publics (État, régions, collectivités locales).', 'Rarement : ventes aux enchères de bateaux publics.'],
        ['9', 'Registre provisoire des bateaux en construction, sauf bateaux de sport construits en série.', 'Seulement si vous commandez une construction sur mesure.']],
  fine='Information indicative fondée sur le décret royal 1027/1989 (art. 4, texte consolidé du BOE) et le décret royal 1435/2010, revue en octobre 2026. Ce n’est pas un conseil juridique et la réglementation peut changer. Confirmez toute démarche auprès de la Capitanía Marítima ou d’une gestoría nautique.',
  next_eyebrow='Étape suivante', next_p='<strong>Vous regardez un bateau et sa liste n’est pas claire ?</strong> Je vous dis quoi vérifier avant de faire une offre.', next_btn='Voir les bateaux en vente', next_href='/fr/barcos/',
  aside_eyebrow='Un doute sur une immatriculation ?', aside_h='Envoyez-la-moi et je vous dis ce qu’elle signifie.', aside_p='Avec l’immatriculation et les documents, je vous dis sur quelle liste il est et quoi vérifier. Sans engagement.', aside_btn='Parler avec Juan sur WhatsApp',
  wa='Bonjour Juan, j’ai une question sur la liste d’immatriculation d’un bateau.',
  toc=['Qu’est-ce qu’une liste', 'Lire une immatriculation', 'Les 9 listes', 'Listes 6 et 7', 'Listes 3 et 4 : pêche', 'Liste 9 et complémentaire', 'Quoi vérifier si vous achetez'],
  rel=[('lista-6-y-lista-7.html', 'Liste 6 et liste 7'), ('papeles-vender-barco-cambio-titularidad.html', 'Papiers pour vendre un bateau'), ('./', 'Tous les guides Plata Marine')],
  card=('Listes d’immatriculation', 'Les 9 listes d’immatriculation des bateaux en Espagne', 'De la liste 1 à la 9 : ce que couvre chaque liste, comment lire une immatriculation et quoi vérifier si le bateau vient de la pêche ou de la location.')),
}

def build():
    for lang in B.LANGS:
        d = C[lang]; path = '/guias/' + FN; url = B.BASE + B.PRE[lang] + path
        schema = {"@context": "https://schema.org", "@type": "Article", "headline": d['h1'], "author": {"@type": "Person", "name": "Juan Morante"},
                  "publisher": {"@type": "Organization", "name": "Plata Marine"}, "datePublished": B.TODAY, "dateModified": B.TODAY, "inLanguage": lang, "mainEntityOfPage": url}
        crumbs = [('Plata Marine', B.BASE + B.PRE[lang] + '/'), (B.GUIDES_NAME[lang], B.BASE + B.PRE[lang] + '/guias/'), (d['crumb'], url)]
        H, Fo = B.shell(lang)
        H = B.fix_header(H, lang, path, d['wa'])
        body = ''
        for i in IDS:
            t, html_ = d['s'][i]
            if html_ is None:
                html_ = table(d['thead'], d['rows'])
            body += '        <h2 id="%s">%s</h2>\n        %s\n' % (i, t, html_)
        toc = ''.join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in zip(IDS, d['toc']))
        rel = ''.join('<a href="%s">%s</a>' % (h, t) for h, t in d['rel'])
        main = '''<main class="art">
  <div class="wrap">
    <article>
      <header>
        <p class="eyebrow">%s</p>
        <h1>%s</h1>
        <div class="meta"><span>%s</span><span>%s</span><span>%s</span></div>
        <p class="lead">%s</p>
      </header>

      <div class="prose">
%s      </div>
      <p style="font-size:13px;opacity:.75;margin-top:22px">%s</p>
    <div class="next-step" data-next="barcos" style="%s"><p class="eyebrow" style="margin:0 0 8px">%s</p><p style="margin:0 0 12px">%s</p><a class="next-btn" style="%s" href="%s">%s</a></div>
    </article>

    <aside class="aside" aria-label="Contacto y navegación">
      <div class="card">
        <p class="eyebrow">%s</p>
        <h3>%s</h3>
        <p>%s</p>
        <a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s</a>
      </div>
      <nav class="toc" aria-label="Contenido de la guía"><ol>%s</ol></nav>
      <div class="rel">%s</div>
    </aside>
  </div>
</main>''' % (d['eyebrow'], d['h1'], d['meta'][0], d['meta'][1], d['meta'][2], d['lead'], body, d['fine'], B.NEXT_STYLE, d['next_eyebrow'], d['next_p'], B.BTN_STYLE, d['next_href'], d['next_btn'],
              d['aside_eyebrow'], d['aside_h'], d['aside_p'], B.wa(d['wa']), d['aside_btn'], toc, rel)
        out = B.head(lang, path, d['title'], d['desc'], schema, crumbs) + H + main + Fo
        pre = '' if lang == 'es' else lang + '/'
        open(os.path.join(B.ROOT, pre + 'guias/' + FN), 'w', encoding='utf-8').write(out)
        # tarjeta en el índice de guías, justo antes de la de lista 6ª/7ª
        p = os.path.join(B.ROOT, pre + 'guias/index.html'); g = open(p, encoding='utf-8').read()
        if FN not in g:
            i = g.find('<li><a href="lista-6-y-lista-7.html">'); j = g.find('</li>', i) + 5
            more = re.search(r'<span class="g-more">([^<]*)</span>', g[i:j]).group(1)
            tag, h, ptxt = d['card']
            card = '<li><a href="%s"><img src="%s" alt="" loading="lazy"><span class="g-body"><span class="tag">%s</span><h2>%s</h2><p>%s</p><span class="g-more">%s</span></span></a></li>\n' % (FN, IMG, tag, h, ptxt, more)
            g = g[:i] + card + g[i:]
            open(p, 'w', encoding='utf-8').write(g)
        print('ok', lang)

if __name__ == '__main__':
    build()
