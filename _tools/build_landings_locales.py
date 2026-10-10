# -*- coding: utf-8 -*-
"""Genera las landings locales (Costa Brava para compradores; Barcelona y Maresme para vendedores)
en ES/CA/EN a partir de la plantilla de /comprar/barcos-segunda-mano-cataluna.html."""
import re, json, html, urllib.parse as u

ROOT = '/home/claude/platamarine/'
PRE = {'es': '', 'ca': 'ca/', 'en': 'en/'}

def esc(t): return html.escape(t, quote=True)

def q(t): return u.quote(t, safe='')

# ---------- contenido ----------
CB = {
 'es': dict(
  title='Barcos de segunda mano en venta en la Costa Brava',
  desc='Barcos de ocasión en la Costa Brava, de Blanes a Portbou, con el encargo de venta firmado por el propietario. Qué barco encaja en las calas, amarres, ITP al 5 % y títulos.',
  eyebrow='Comprar barco · Costa Brava', by='Por Juan Morante', upd='Actualizado en septiembre de 2026',
  lead='La Costa Brava es donde más barcos gestiono. Estos son los que gestiono ahora entre Blanes y Portbou, y debajo, lo que conviene saber si vas a comprar para navegar aquí.',
  h2list='Barcos en venta en la Costa Brava',
  empty='Ahora mismo no tengo ningún barco disponible en la Costa Brava. <a href="/alertas/">Crea una alerta</a> y te aviso en cuanto entre uno.',
  note='Todos los barcos que publico tienen el encargo de venta firmado por su propietario. <a href="/barcos/">Ver el catálogo completo con filtros</a>.',
  secs=[
   ('Qué barco encaja en la Costa Brava', '<p>Aquí el barco se usa sobre todo para ir de cala en cala y fondear: de Blanes a Palamós, las islas Medes, el cabo de Creus. Por eso los que más se buscan son los <strong>open, sundeck y walkaround de 6 a 9 metros</strong>, con plataforma de baño y sombra, y las <strong>semirrígidas</strong>, que se sacan del agua en invierno y se llevan en remolque. Si quieres pasar alguna noche a bordo, un <strong>cabinado de 8 a 11 metros</strong> con un camarote decente y aseo cambia mucho la experiencia.</p><p>Ten en cuenta el norte: en el golfo de Roses y hacia Cadaqués la tramontana obliga a mirar el parte con más cuidado, y un casco con algo más de eslora y peso se agradece. En el sur, entre Blanes y Palamós, el día de calas es más tranquilo y casi cualquier eslora funciona.</p>'),
   ('Puertos y amarres', '<p>Los puertos principales son Blanes, Sant Feliu de Guíxols, Palamós, l\'Estartit, l\'Escala, Roses, Empuriabrava (con sus canales) y Llançà. En verano el amarre de alquiler escasea y en los puertos pequeños hay lista de espera, así que antes de comprar conviene tener claro dónde va a dormir el barco. Muchos propietarios lo resuelven con <strong>varadero en seco</strong> (marina seca) y botadura cada vez que salen: para barcos de hasta 7-8 metros suele salir más barato que un amarre en el agua.</p><p>Si el barco se vende con amarre en propiedad y se puede subrogar, lo indico en la ficha. Tienes las tarifas de los puertos catalanes en la <a href="/guias/amarres-cataluna-tipos-precios-alquiler-compra.html">guía de amarres</a>.</p>'),
   ('Comprar a un particular en Girona', '<p>Al comprar un barco usado a un particular en Cataluña se paga el <strong>ITP del 5 %</strong> a la Agència Tributària de Catalunya en el plazo de un mes, sobre el precio de compra o el valor de tablas de Hacienda si es mayor. Después se hace el cambio de titularidad en la Capitanía Marítima que corresponda (Palamós o Roses para la mayoría de la Costa Brava). Si el vendedor es una empresa, la operación lleva IVA en lugar de ITP. Lo tienes paso a paso en <a href="/papeles-fiscalidad/">papeles e impuestos</a> y en la <a href="/herramientas/impuestos-comprar-barco.html">calculadora de impuestos</a>.</p><p>En los barcos de mi cartera compruebo la documentación con el propietario antes de que te comprometas: titularidad, cargas, certificado de navegabilidad y estado fiscal. Y si el barco te convence, te acompaño en la prueba de mar y en el peritaje si quieres hacerlo.</p>'),
  ],
  cta=('¿No está el que buscas?', 'Dime qué buscas y te aviso cuando entre un barco en la Costa Brava que encaje, antes de que salga en ningún portal.', 'Crear alerta', 'Ver todos los barcos'),
  faqh='Preguntas frecuentes',
  faq=[
   ('¿Cuánto cuesta un barco de segunda mano en la Costa Brava?', 'Depende del tipo y la eslora: una lancha open de 6 a 7 metros se mueve entre unos 20.000 y 60.000 €, y un sundeck o walkaround de 7 a 8,5 metros entre 25.000 y más de 100.000 € según el año. Tienes los rangos por modelo en la página de precios.'),
   ('¿Qué impuesto se paga al comprar un barco usado en Girona?', 'El ITP del 5 % si compras a un particular, sobre el precio o el valor de tablas de Hacienda si es mayor, con un mes de plazo. Si compras a una empresa, la operación lleva IVA en lugar de ITP.'),
   ('¿Es difícil encontrar amarre en la Costa Brava?', 'En verano, sí, sobre todo en los puertos pequeños. Muchos propietarios optan por varadero en seco. Si el barco se vende con amarre traspasable, vale la pena tenerlo en cuenta en el precio.'),
  ],
  fiscal='Información fiscal orientativa, revisada en septiembre de 2026 según la Ley 38/1992 y la normativa autonómica vigente. No es asesoramiento fiscal. El importe final depende del valor que fije Hacienda, de la situación del barco y de posibles exenciones, y la normativa puede cambiar. Confírmalo con tu gestoría o con la Administración antes de comprar.',
  aside=('¿Lo miramos juntos?', 'Te ayudo a encontrar el barco.', 'Cuéntame qué uso le vas a dar, dónde lo tendrías y tu presupuesto, y te digo qué encaja.', 'Hablar con Juan por WhatsApp'),
  wa='Hola Juan, busco un barco de segunda mano en la Costa Brava.',
  rel=('También te puede interesar', [('/guias/amarres-cataluna-tipos-precios-alquiler-compra.html','Amarres en Cataluña: tipos y precios'),('/comprar/barcos-segunda-mano-cataluna.html','Barcos de segunda mano en Cataluña'),('/precios/','Precios por modelo'),('/comprar/','Comprar un barco de segunda mano')]),
 ),
 'ca': dict(
  title='Vaixells de segona mà en venda a la Costa Brava',
  desc='Vaixells d\'ocasió a la Costa Brava, de Blanes a Portbou, amb l\'encàrrec de venda signat pel propietari. Quin vaixell encaixa a les cales, amarratges, ITP al 5 % i títols.',
  eyebrow='Comprar vaixell · Costa Brava', by='Per Juan Morante', upd='Actualitzat el setembre de 2026',
  lead='La Costa Brava és on gestiono més vaixells. Aquests són els que gestiono ara entre Blanes i Portbou, i a sota, el que convé saber si vols comprar per navegar aquí.',
  h2list='Vaixells en venda a la Costa Brava',
  empty='Ara mateix no tinc cap vaixell disponible a la Costa Brava. <a href="/ca/alertas/">Crea una alerta</a> i t\'aviso quan n\'entri un.',
  note='Tots els vaixells que publico tenen l\'encàrrec de venda signat pel seu propietari. <a href="/ca/barcos/">Veure el catàleg complet amb filtres</a>.',
  secs=[
   ('Quin vaixell encaixa a la Costa Brava', '<p>Aquí el vaixell es fa servir sobretot per anar de cala en cala i fondejar: de Blanes a Palamós, les illes Medes, el cap de Creus. Per això els més buscats són els <strong>open, sundeck i walkaround de 6 a 9 metres</strong>, amb plataforma de bany i ombra, i les <strong>semirígides</strong>, que es treuen de l\'aigua a l\'hivern i es porten amb remolc. Si vols passar alguna nit a bord, un <strong>cabinat de 8 a 11 metres</strong> amb una cabina decent i lavabo canvia molt l\'experiència.</p><p>Tingues en compte el nord: al golf de Roses i cap a Cadaqués la tramuntana obliga a mirar el temps amb més cura, i un casc amb una mica més d\'eslora i pes s\'agraeix. Al sud, entre Blanes i Palamós, el dia de cales és més tranquil i gairebé qualsevol eslora funciona.</p>'),
   ('Ports i amarratges', '<p>Els ports principals són Blanes, Sant Feliu de Guíxols, Palamós, l\'Estartit, l\'Escala, Roses, Empuriabrava (amb els seus canals) i Llançà. A l\'estiu l\'amarratge de lloguer escasseja i als ports petits hi ha llista d\'espera, així que abans de comprar convé tenir clar on dormirà el vaixell. Molts propietaris ho resolen amb <strong>varador en sec</strong> (marina seca) i avarada cada cop que surten: per a vaixells de fins a 7-8 metres sol sortir més barat que un amarratge a l\'aigua.</p><p>Si el vaixell es ven amb amarratge en propietat i es pot subrogar, ho indico a la fitxa. Tens les tarifes dels ports catalans a la <a href="/ca/guias/amarres-cataluna-tipos-precios-alquiler-compra.html">guia d\'amarratges</a>.</p>'),
   ('Comprar a un particular a Girona', '<p>En comprar un vaixell usat a un particular a Catalunya es paga l\'<strong>ITP del 5 %</strong> a l\'Agència Tributària de Catalunya en el termini d\'un mes, sobre el preu de compra o el valor de taules d\'Hisenda si és superior. Després es fa el canvi de titularitat a la Capitania Marítima que correspongui (Palamós o Roses per a la majoria de la Costa Brava). Si el venedor és una empresa, l\'operació porta IVA en lloc d\'ITP. Ho tens pas a pas a <a href="/ca/papeles-fiscalidad/">papers i impostos</a> i a la <a href="/ca/herramientas/impuestos-comprar-barco.html">calculadora d\'impostos</a>.</p><p>Als vaixells de la meva cartera comprovo la documentació amb el propietari abans que et comprometis: titularitat, càrregues, certificat de navegabilitat i estat fiscal. I si el vaixell et convenç, t\'acompanyo a la prova de mar i al peritatge si el vols fer.</p>'),
  ],
  cta=('No hi és el que busques?', 'Digue\'m què busques i t\'aviso quan entri un vaixell a la Costa Brava que encaixi, abans que surti a cap portal.', 'Crear alerta', 'Veure tots els vaixells'),
  faqh='Preguntes freqüents',
  faq=[
   ('Quant costa un vaixell de segona mà a la Costa Brava?', 'Depèn del tipus i l\'eslora: una llanxa open de 6 a 7 metres es mou entre uns 20.000 i 60.000 €, i un sundeck o walkaround de 7 a 8,5 metres entre 25.000 i més de 100.000 € segons l\'any. Tens els rangs per model a la pàgina de preus.'),
   ('Quin impost es paga en comprar un vaixell usat a Girona?', 'L\'ITP del 5 % si compres a un particular, sobre el preu o el valor de taules d\'Hisenda si és superior, amb un mes de termini. Si compres a una empresa, l\'operació porta IVA en lloc d\'ITP.'),
   ('És difícil trobar amarratge a la Costa Brava?', 'A l\'estiu, sí, sobretot als ports petits. Molts propietaris opten per varador en sec. Si el vaixell es ven amb amarratge traspassable, val la pena tenir-ho en compte en el preu.'),
  ],
  fiscal='Informació fiscal orientativa, revisada el setembre de 2026 segons la Llei 38/1992 i la normativa autonòmica vigent. No és assessorament fiscal. L\'import final depèn del valor que fixi Hisenda, de la situació del vaixell i de possibles exempcions, i la normativa pot canviar. Confirma-ho amb la teva gestoria o amb l\'Administració abans de comprar.',
  aside=('Ho mirem junts?', 'T\'ajudo a trobar el vaixell.', 'Explica\'m quin ús li donaràs, on el tindries i el teu pressupost, i et dic què encaixa.', 'Parlar amb Juan per WhatsApp'),
  wa='Hola Juan, busco un vaixell de segona mà a la Costa Brava.',
  rel=('També et pot interessar', [('/ca/guias/amarres-cataluna-tipos-precios-alquiler-compra.html','Amarratges a Catalunya: tipus i preus'),('/ca/comprar/barcos-segunda-mano-cataluna.html','Vaixells de segona mà a Catalunya'),('/ca/precios/','Preus per model'),('/ca/comprar/','Comprar un vaixell de segona mà')]),
 ),
 'en': dict(
  title='Used boats for sale on the Costa Brava',
  desc='Pre-owned boats on the Costa Brava, from Blanes to Portbou, each with a sales mandate signed by the owner. Which boat suits the coves, berths, 5 % transfer tax and licences.',
  eyebrow='Buy a boat · Costa Brava', by='By Juan Morante', upd='Updated September 2026',
  lead='The Costa Brava is where I handle most of my boats. These are the ones I am currently handling between Blanes and Portbou, and below, what is worth knowing if you are buying to sail here.',
  h2list='Boats for sale on the Costa Brava',
  empty='Right now I have no boat available on the Costa Brava. <a href="/en/alertas/">Create an alert</a> and I will let you know as soon as one comes in.',
  note='Every boat I publish has a sales mandate signed by its owner. <a href="/en/barcos/">See the full catalogue with filters</a>.',
  secs=[
   ('Which boat suits the Costa Brava', '<p>Here boats are used above all to hop from cove to cove and anchor: from Blanes to Palamós, the Medes islands, Cap de Creus. That is why the most sought-after are <strong>open, sundeck and walkaround boats of 6 to 9 metres</strong>, with a bathing platform and shade, and <strong>RIBs</strong>, which come out of the water in winter and travel on a trailer. If you want to spend the odd night aboard, a <strong>cabin cruiser of 8 to 11 metres</strong> with a decent cabin and heads changes the experience.</p><p>Bear the north in mind: in the Gulf of Roses and towards Cadaqués the tramontana wind means watching the forecast more carefully, and a hull with a bit more length and weight is welcome. In the south, between Blanes and Palamós, a day in the coves is calmer and almost any size works.</p>'),
   ('Harbours and berths', '<p>The main harbours are Blanes, Sant Feliu de Guíxols, Palamós, l\'Estartit, l\'Escala, Roses, Empuriabrava (with its canals) and Llançà. In summer rental berths are scarce and the small harbours have waiting lists, so before buying it pays to know where the boat will live. Many owners solve it with <strong>dry stack storage</strong> and a launch each time they go out: for boats up to 7-8 metres it is usually cheaper than a wet berth.</p><p>If a boat is sold with an owned berth that can be transferred, I say so on its page. Rates for the Catalan harbours are in the <a href="/en/guias/amarres-cataluna-tipos-precios-alquiler-compra.html">berths guide</a>.</p>'),
   ('Buying from a private seller in Girona', '<p>When you buy a used boat from a private individual in Catalonia you pay <strong>5 % transfer tax (ITP)</strong> to the Catalan tax agency within one month, on the purchase price or the tax office\'s table value if higher. The change of ownership is then done at the relevant Capitanía Marítima (Palamós or Roses for most of the Costa Brava). If the seller is a company, the sale carries VAT instead of ITP. Step by step in <a href="/en/papeles-fiscalidad/">paperwork and taxes</a> and the <a href="/en/herramientas/impuestos-comprar-barco.html">tax calculator</a>.</p><p>On the boats in my portfolio I check the documentation with the owner before you commit: ownership, liens, seaworthiness certificate and tax status. And if the boat convinces you, I go with you on the sea trial and the survey if you want one.</p>'),
  ],
  cta=('Not the one you are looking for?', 'Tell me what you want and I will let you know when a matching boat comes in on the Costa Brava, before it appears on any portal.', 'Create an alert', 'See all boats'),
  faqh='Frequently asked questions',
  faq=[
   ('How much does a used boat cost on the Costa Brava?', 'It depends on the type and length: an open boat of 6 to 7 metres ranges from about €20,000 to €60,000, and a sundeck or walkaround of 7 to 8.5 metres from €25,000 to over €100,000 depending on the year. Ranges by model are on the prices page.'),
   ('What tax do you pay when buying a used boat in Girona?', '5 % ITP if you buy from a private individual, on the price or the tax office\'s table value if higher, within one month. If you buy from a company, the sale carries VAT instead of ITP.'),
   ('Is it hard to find a berth on the Costa Brava?', 'In summer, yes, especially in the small harbours. Many owners choose dry storage. If a boat is sold with a transferable berth, it is worth factoring into the price.'),
  ],
  fiscal='Indicative tax information, reviewed in September 2026 under Law 38/1992 and the regional rules in force. This is not tax advice. The final amount depends on the value set by the tax office, the boat\'s situation and possible exemptions, and the rules may change. Confirm with your tax adviser or the tax office before buying.',
  aside=('Shall we look together?', 'I help you find the boat.', 'Tell me how you will use it, where you would keep it and your budget, and I will tell you what fits.', 'Talk to Juan on WhatsApp'),
  wa='Hi Juan, I am looking for a used boat on the Costa Brava.',
  rel=('You may also like', [('/en/guias/amarres-cataluna-tipos-precios-alquiler-compra.html','Berths in Catalonia: types and prices'),('/en/comprar/barcos-segunda-mano-cataluna.html','Used boats in Catalonia'),('/en/precios/','Prices by model'),('/en/comprar/','Buying a used boat')]),
 ),
}

BM = {
 'es': dict(
  title='Broker náutico en Barcelona y el Maresme · vender tu barco',
  desc='Juan Morante, broker náutico: te ayudo a vender tu barco en Barcelona, Badalona, el Masnou, Premià, Mataró o Arenys. Precio con criterio, anuncio cuidado y compradores filtrados. A éxito y sin exclusiva.',
  eyebrow='Vender barco · Barcelona y Maresme', by='Por Juan Morante', upd='Actualizado en septiembre de 2026',
  lead='Si tienes el barco en Port Vell, Port Olímpic, Port Fòrum, Badalona, el Masnou, Premià, Mataró o Arenys y quieres venderlo sin que te coma el tiempo, te cuento cómo trabajo y qué puedo hacer por ti.',
  secs=[
   ('Vender un barco en Barcelona y el Maresme', '<p>Es la zona con más oferta de Cataluña, y eso tiene dos caras: hay compradores todo el año, pero tu barco compite con muchos anuncios parecidos. La diferencia la marcan el precio de salida, unas fotos y un texto que expliquen bien el barco, y responder rápido y con criterio a quien pregunta. Ahí es donde entro yo.</p><p>Qué hago: estudio el precio con barcos comparables a la venta y el tiempo que llevan anunciados, preparo la ficha con tus fotos y la publico en mi web y en portales, hablo con cada interesado antes de organizar una visita, negocio contigo al lado y coordino la documentación del cambio de titularidad; si hace falta gestoría, acordamos antes su alcance y su coste.</p>'),
   ('Cómo trabajo', '<ul><li><strong>A éxito.</strong> Mis honorarios se pactan en la hoja de encargo y se cobran cuando el barco se vende, no antes.</li><li><strong>Sin exclusiva ni adelantos.</strong> Puedes mantener tu propio anuncio mientras trabajamos.</li><li><strong>Empezamos con tus fotos y la documentación.</strong> A la visita voy cuando hay un comprador serio, y te acompaño en la prueba de mar.</li><li><strong>Trato directo conmigo</strong> durante toda la operación, por WhatsApp o por teléfono.</li></ul><p>Trabajo barcos a motor y veleros, normalmente de 6 a 24 metros, en cualquiera de los puertos entre Barcelona y Arenys de Mar, y también en el Garraf y la Costa Brava.</p>'),
   ('Qué necesito para empezar', '<p>Marca, modelo y año, motorización y horas, dónde está el barco y en qué régimen de amarre, si tiene el certificado de navegabilidad en vigor, y unas fotos actuales. Con eso te doy una primera opinión sobre el precio, sin compromiso. Si te encaja, firmamos la hoja de encargo y me pongo con el anuncio.</p><p>Si antes quieres hacerte una idea tú mismo, tienes la <a href="/herramientas/valora-tu-barco.html">herramienta para valorar tu barco</a> y la guía <a href="/guias/que-hace-un-broker-nautico.html">qué hace un broker náutico</a>.</p>'),
  ],
  cta=('¿Hablamos de tu barco?', 'Cuéntame qué barco tienes y dónde está, y te digo cómo lo vendería.', 'Quiero vender mi barco', '¿Cuánto vale mi barco?'),
  ctalinks=('/#vender','/herramientas/valora-tu-barco.html'),
  faqh='Preguntas frecuentes',
  faq=[
   ('¿Cuánto cobra un broker náutico por vender un barco?', 'Un porcentaje sobre el precio final de venta, que se pacta por escrito en la hoja de encargo antes de empezar y solo se cobra si el barco se vende. Te lo explico con detalle cuando hablemos de tu barco.'),
   ('¿Tengo que dar exclusiva?', 'No. Trabajo sin exclusiva y puedes mantener tu propio anuncio mientras tanto.'),
   ('¿Tienes que venir a ver el barco?', 'No hace falta al principio: empezamos con tus fotos y la documentación. Voy a verlo con el comprador cuando hay un interés serio, y te acompaño en la prueba de mar.'),
   ('¿Qué papeles hacen falta para vender un barco?', 'Hoja de asiento o certificado de registro, certificado de navegabilidad en vigor, último recibo del impuesto y del seguro, y la factura de compra si la tienes. Si falta algo, te digo cómo conseguirlo.'),
  ],
  fiscal='La comisión y las condiciones concretas se fijan en la hoja de encargo. Plata Marine actúa como intermediario: no compra ni vende barcos en nombre propio.',
  aside=('¿Hablamos?', 'Te digo cómo vendería tu barco.', 'Escríbeme con el modelo, el año y dónde está el barco y te contesto en el día.', 'Hablar con Juan por WhatsApp'),
  wa='Hola Juan, quiero vender mi barco en la zona de Barcelona / Maresme.',
  rel=('También te puede interesar', [('/herramientas/valora-tu-barco.html','¿Cuánto vale mi barco?'),('/guias/que-hace-un-broker-nautico.html','Qué hace un broker náutico'),('/papeles-fiscalidad/','Papeles e impuestos'),('/guias/amarres-cataluna-tipos-precios-alquiler-compra.html','Amarres en Cataluña')]),
 ),
 'ca': dict(
  title='Broker nàutic a Barcelona i el Maresme · vendre el teu vaixell',
  desc='Juan Morante, broker nàutic: t\'ajudo a vendre el teu vaixell a Barcelona, Badalona, el Masnou, Premià, Mataró o Arenys. Preu amb criteri, anunci cuidat i compradors filtrats. A èxit i sense exclusiva.',
  eyebrow='Vendre vaixell · Barcelona i Maresme', by='Per Juan Morante', upd='Actualitzat el setembre de 2026',
  lead='Si tens el vaixell al Port Vell, Port Olímpic, Port Fòrum, Badalona, el Masnou, Premià, Mataró o Arenys i el vols vendre sense que et mengi el temps, t\'explico com treballo i què puc fer per tu.',
  secs=[
   ('Vendre un vaixell a Barcelona i el Maresme', '<p>És la zona amb més oferta de Catalunya, i això té dues cares: hi ha compradors tot l\'any, però el teu vaixell competeix amb molts anuncis semblants. La diferència la marquen el preu de sortida, unes fotos i un text que expliquin bé el vaixell, i respondre ràpid i amb criteri a qui pregunta. Aquí és on entro jo.</p><p>Què faig: estudio el preu amb dades de vaixells comparables venuts i en venda, preparo l\'anunci i el posiciono al meu web i als portals que funcionen, filtro els contactes perquè només t\'arribin compradors reals, negocio amb tu al costat i m\'ocupo de la paperassa del canvi de titularitat amb la gestoria.</p>'),
   ('Com treballo', '<ul><li><strong>A èxit.</strong> Els meus honoraris es pacten al full d\'encàrrec i es cobren quan el vaixell es ven, no abans.</li><li><strong>Sense exclusiva ni bestretes.</strong> Pots mantenir el teu propi anunci mentre treballem.</li><li><strong>Comencem amb les teves fotos i la documentació.</strong> A la visita hi vaig quan hi ha un comprador seriós, i t\'acompanyo a la prova de mar.</li><li><strong>Tracte directe amb mi</strong> durant tota l\'operació, per WhatsApp o per telèfon.</li></ul><p>Treballo vaixells a motor i velers, normalment de 6 a 24 metres, a qualsevol dels ports entre Barcelona i Arenys de Mar, i també al Garraf i la Costa Brava.</p>'),
   ('Què necessito per començar', '<p>Marca, model i any, motorització i hores, on és el vaixell i en quin règim d\'amarratge, si té el certificat de navegabilitat en vigor, i unes fotos actuals. Amb això et dono una primera opinió sobre el preu, sense compromís. Si t\'encaixa, signem el full d\'encàrrec i em poso amb l\'anunci.</p><p>Si abans vols fer-te\'n una idea tu mateix, tens l\'<a href="/ca/herramientas/valora-tu-barco.html">eina per valorar el teu vaixell</a> i la guia <a href="/ca/guias/que-hace-un-broker-nautico.html">què fa un broker nàutic</a>.</p>'),
  ],
  cta=('Parlem del teu vaixell?', 'Explica\'m quin vaixell tens i on és, i et dic com el vendria.', 'Vull vendre el meu vaixell', 'Quant val el meu vaixell?'),
  ctalinks=('/ca/#vender','/ca/herramientas/valora-tu-barco.html'),
  faqh='Preguntes freqüents',
  faq=[
   ('Quant cobra un broker nàutic per vendre un vaixell?', 'Un percentatge sobre el preu final de venda, que es pacta per escrit al full d\'encàrrec abans de començar i només es cobra si el vaixell es ven. T\'ho explico amb detall quan parlem del teu vaixell.'),
   ('He de donar exclusiva?', 'No. Treballo sense exclusiva i pots mantenir el teu propi anunci mentrestant.'),
   ('Has de venir a veure el vaixell?', 'No cal al principi: comencem amb les teves fotos i la documentació. Hi vaig amb el comprador quan hi ha un interès seriós, i t\'acompanyo a la prova de mar.'),
   ('Quins papers calen per vendre un vaixell?', 'Full d\'assentament o certificat de registre, certificat de navegabilitat en vigor, últim rebut de l\'impost i de l\'assegurança, i la factura de compra si la tens. Si falta alguna cosa, et dic com aconseguir-la.'),
  ],
  fiscal='La comissió i les condicions concretes es fixen al full d\'encàrrec. Plata Marine actua com a intermediari: no compra ni ven vaixells en nom propi.',
  aside=('Parlem?', 'Et dic com vendria el teu vaixell.', 'Escriu-me amb el model, l\'any i on és el vaixell i et contesto el mateix dia.', 'Parlar amb Juan per WhatsApp'),
  wa='Hola Juan, vull vendre el meu vaixell a la zona de Barcelona / Maresme.',
  rel=('També et pot interessar', [('/ca/herramientas/valora-tu-barco.html','Quant val el meu vaixell?'),('/ca/guias/que-hace-un-broker-nautico.html','Què fa un broker nàutic'),('/ca/papeles-fiscalidad/','Papers i impostos'),('/ca/guias/amarres-cataluna-tipos-precios-alquiler-compra.html','Amarratges a Catalunya')]),
 ),
 'en': dict(
  title='Yacht broker in Barcelona and the Maresme · selling your boat',
  desc='Juan Morante, yacht broker: I help you sell your boat in Barcelona, Badalona, El Masnou, Premià, Mataró or Arenys. A well-reasoned price, a careful listing and screened buyers. Success fee, no exclusivity.',
  eyebrow='Sell a boat · Barcelona and Maresme', by='By Juan Morante', upd='Updated September 2026',
  lead='If your boat is in Port Vell, Port Olímpic, Port Fòrum, Badalona, El Masnou, Premià, Mataró or Arenys and you want to sell it without it eating your time, here is how I work and what I can do for you.',
  secs=[
   ('Selling a boat in Barcelona and the Maresme', '<p>It is the area with the most supply in Catalonia, and that cuts both ways: there are buyers all year round, but your boat competes with many similar listings. What makes the difference is the asking price, photos and a text that explain the boat properly, and answering enquiries quickly and with judgement. That is where I come in.</p><p>What I do: I work out the price from data on comparable boats sold and for sale, prepare the listing and position it on my website and the portals that work, screen the contacts so only real buyers reach you, negotiate with you beside me and handle the ownership-transfer paperwork with the agency.</p>'),
   ('How I work', '<ul><li><strong>Success fee.</strong> My fee is agreed in the mandate and paid when the boat sells, not before.</li><li><strong>No exclusivity, no advances.</strong> You can keep your own listing while we work.</li><li><strong>We start with your photos and the paperwork.</strong> I visit when there is a serious buyer, and I go with you on the sea trial.</li><li><strong>You deal directly with me</strong> throughout, by WhatsApp or phone.</li></ul><p>I handle motorboats and sailing yachts, usually 6 to 24 metres, in any of the harbours between Barcelona and Arenys de Mar, and also in the Garraf and on the Costa Brava.</p>'),
   ('What I need to get started', '<p>Make, model and year, engines and hours, where the boat is and on what kind of berth, whether the seaworthiness certificate is current, and some recent photos. With that I give you a first opinion on price, no obligation. If it suits you, we sign the mandate and I get on with the listing.</p><p>If you would rather get an idea yourself first, there is the <a href="/en/herramientas/valora-tu-barco.html">boat valuation tool</a> and the guide <a href="/en/guias/que-hace-un-broker-nautico.html">what a yacht broker does</a>.</p>'),
  ],
  cta=('Shall we talk about your boat?', 'Tell me what boat you have and where it is, and I will tell you how I would sell it.', 'I want to sell my boat', 'What is my boat worth?'),
  ctalinks=('/en/#vender','/en/herramientas/valora-tu-barco.html'),
  faqh='Frequently asked questions',
  faq=[
   ('How much does a yacht broker charge to sell a boat?', 'A percentage of the final sale price, agreed in writing in the mandate before we start and only charged if the boat sells. I explain it in detail when we talk about your boat.'),
   ('Do I have to give exclusivity?', 'No. I work without exclusivity and you can keep your own listing in the meantime.'),
   ('Do you need to come and see the boat?', 'Not at first: we start with your photos and the paperwork. I go to see it with the buyer when there is serious interest, and I go with you on the sea trial.'),
   ('What paperwork do I need to sell a boat?', 'Registration certificate, current seaworthiness certificate, latest tax and insurance receipts, and the purchase invoice if you have it. If anything is missing, I tell you how to get it.'),
  ],
  fiscal='The fee and specific terms are set in the mandate. Plata Marine acts as an intermediary: it does not buy or sell boats in its own name.',
  aside=('Shall we talk?', 'I will tell you how I would sell your boat.', 'Message me with the model, the year and where the boat is and I will reply the same day.', 'Talk to Juan on WhatsApp'),
  wa='Hi Juan, I want to sell my boat in the Barcelona / Maresme area.',
  rel=('You may also like', [('/en/herramientas/valora-tu-barco.html','What is my boat worth?'),('/en/guias/que-hace-un-broker-nautico.html','What a yacht broker does'),('/en/papeles-fiscalidad/','Paperwork and taxes'),('/en/guias/amarres-cataluna-tipos-precios-alquiler-compra.html','Berths in Catalonia')]),
 ),
}

CB_SLUG = 'comprar/barcos-segunda-mano-costa-brava.html'
BM_SLUG = 'vender/broker-nautico-barcelona-maresme.html'

def build(lang, d, slug, list_area):
    pre = PRE[lang]
    tpl = open(ROOT + pre + 'comprar/barcos-segunda-mano-cataluna.html', encoding='utf-8').read()
    s = tpl
    # head
    s = re.sub(r'<title>.*?</title>', '<title>' + esc(d['title']) + '</title>', s, 1)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + esc(d['desc']) + '">', s, 1)
    s = s.replace('comprar/barcos-segunda-mano-cataluna.html', slug)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="' + esc(d['title']) + '">', s, 1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="' + esc(d['desc']) + '">', s, 1)
    url = 'https://www.platamarine.com/' + pre + slug
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage" if list_area else "WebPage", "name": d['title'], "inLanguage": lang, "url": url, "description": d['desc'], "publisher": {"@type": "Organization", "name": "Plata Marine"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": qn, "acceptedAnswer": {"@type": "Answer", "text": an}} for qn, an in d['faq']]}]}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False) + '\n</script>', s, 1, flags=re.S)
    # header WA buttons (two occurrences of the Cataluña text)
    s = re.sub(r'wa\.me/34633742973\?text=Hola%20Juan%2C%20busco%20un%20barco%20de%20segunda%20mano%20en%20Catalu%C3%B1a\.|wa\.me/34633742973\?text=Hola%20Juan%2C%20busco%20un%20vaixell%20de%20segona%20m%C3%A0%20a%20Catalunya\.|wa\.me/34633742973\?text=Hi%20Juan%2C%20I%20am%20looking%20for%20a%20used%20boat%20in%20Catalonia\.', 'wa.me/34633742973?text=' + q(d['wa']), s)
    # article body
    if list_area:
        # keep the pre-rendered cards of the area only
        lm = re.search(r'<div class="pm-list" data-f=\'[^\']*\'>(.*?)</div>', s, re.S)
        cards = re.findall(r'<a class="pcard".*?</a>', lm.group(1), re.S)
        keep = [c for c in cards if any(k in c for k in AREA_SLUGS[list_area])]
        listhtml = '<div class="pm-list" data-f=\'{"area": "' + list_area + '"}\'>' + ''.join(keep) + '</div>\n        <p class="pm-empty"' + ('' if keep else '') + ' hidden>' + d['empty'] + '</p>\n        <p class="note" style="font-family:var(--display);font-size:12.5px;color:var(--ink-2)">' + d['note'] + '</p>\n'
        listblock = '<h2 id="barcos">' + esc(d['h2list']) + '</h2>\n        ' + listhtml
    else:
        listblock = ''
    secs = ''.join('<h2 id="s%d">%s</h2>%s\n        ' % (i, esc(h), b) for i, (h, b) in enumerate(d['secs']))
    c = d['cta']
    if list_area:
        cta = '<div class="cta2"><h3>%s</h3><p>%s</p><a class="btn btn-wa" href="/%salertas/">%s</a><a class="btn btn-ghost" href="/%sbarcos/">%s</a></div>' % (esc(c[0]), esc(c[1]), pre, esc(c[2]), pre, esc(c[3]))
    else:
        l1, l2 = d['ctalinks']
        cta = '<div class="cta2"><h3>%s</h3><p>%s</p><a class="btn btn-wa" href="%s">%s</a><a class="btn btn-ghost" href="%s">%s</a></div>' % (esc(c[0]), esc(c[1]), l1, esc(c[2]), l2, esc(c[3]))
    faq = '<h2 id="faq">' + esc(d['faqh']) + '</h2>\n        ' + ''.join('<h3>%s</h3><p>%s</p>' % (esc(qn), esc(an)) for qn, an in d['faq'])
    article = ('<header>\n        <p class="eyebrow">%s</p>\n        <h1>%s</h1>\n        <div class="meta"><span>%s</span><span>%s</span></div>\n        <p class="lead">%s</p>\n      </header>\n      <div class="prose">\n        %s%s\n        %s\n        %s\n      </div>\n    <p class="aviso aviso-fiscal" style="font-size:.82em;opacity:.85">%s</p>\n    </article>'
               % (esc(d['eyebrow']), esc(d['title']), esc(d['by']), esc(d['upd']), esc(d['lead']), listblock, secs, cta, faq, esc(d['fiscal'])))
    s = re.sub(r'<header>\s*<p class="eyebrow">.*?</article>', lambda m: article, s, 1, flags=re.S)
    # aside
    a = d['aside']
    aside = ('<div class="card">\n        <p class="eyebrow">%s</p>\n        <h3>%s</h3>\n        <p>%s</p>\n        <a class="btn btn-wa" href="https://wa.me/34633742973?text=%s" target="_blank" rel="noopener">%s</a>\n      </div>\n      <div class="rel"><p class="eyebrow">%s</p>%s</div>'
             % (esc(a[0]), esc(a[1]), esc(a[2]), q(d['wa']), esc(a[3]), esc(d['rel'][0]), ''.join('<a href="%s">%s</a>' % (h, esc(t)) for h, t in d['rel'][1])))
    s = re.sub(r'<div class="card">.*?</div>\s*<div class="rel">.*?</div>', lambda m: aside, s, 1, flags=re.S)
    if slug.startswith('vender/'):
        pass  # relative ../ links (logo, legal) keep working: same depth as comprar/
    out = ROOT + pre + slug
    import os; os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(s)
    return out

AREA_SLUGS = {'costa-brava': ['/gallart-1050.html', '/monte-carlo-27.html', '/monterey-278-ss.html']}

if __name__ == '__main__':
    for lang in PRE:
        print(build(lang, CB[lang], CB_SLUG, 'costa-brava'))
        print(build(lang, BM[lang], BM_SLUG, None))
