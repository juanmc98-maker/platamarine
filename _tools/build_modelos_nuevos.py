# Plata Marine · fichas de modelo nuevas (octubre 2026): Jeanneau Merry Fisher 895 y Beneteau Flyer 8 SUNdeck
# Parte de la plantilla de una ficha existente del mismo tipo (ES/CA/EN) y sustituye contenido.
# Uso: python3 _tools/build_modelos_nuevos.py  (desde la raíz del repo); después node para el bloque "En venta ahora".
import re, json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda l: '' if l == 'es' else '/' + l
FECHA = '2026-10-01'
MES = {'es': 'octubre de 2026', 'ca': "l'octubre de 2026", 'en': 'October 2026'}

def table(rows, l):
    th = {'es': ('Años', 'Rango habitual'), 'ca': ('Anys', 'Rang habitual'), 'en': ('Years', 'Typical range')}[l]
    return '<table class="pr"><tr><th>%s</th><th>%s</th></tr>%s</table>' % (th + (''.join('<tr><td>%s</td><td>%s</td></tr>' % r for r in rows),))

def spec(rows):
    return '<table class="spec">%s</table>' % ''.join('<tr><td>%s</td><td>%s</td></tr>' % r for r in rows)

M = {}
# ---------------------------------------------------------------- MERRY FISHER 895
M['jeanneau-merry-fisher-895'] = dict(
  tpl='jeanneau-merry-fisher-795', names=[('Merry Fisher 795', 'Merry Fisher 895'), ('Merry%20Fisher%20795', 'Merry%20Fisher%20895')],
  brand='Jeanneau', product='Jeanneau Merry Fisher 895', len=8.9, types=['pilothouse', 'cabinado'],
  idx={'es': ('Pilothouse', 'Serie 1 de 2017 a 2024; Serie 2 desde 2024'), 'ca': ('Pilothouse', 'Sèrie 1 de 2017 a 2024; Sèrie 2 des de 2024'), 'en': ('Pilothouse', 'Series 1 2017 to 2024; Series 2 since 2024')},
  pr={'es': [('2017 a 2018', '95.000 a 135.000 €'), ('2019 a 2020', '115.000 a 150.000 €'), ('2021 a 2024', '125.000 a 180.000 € (pocas unidades; las casi nuevas, cerca del precio de catálogo)')],
      'ca': [('2017 a 2018', '95.000 a 135.000 €'), ('2019 a 2020', '115.000 a 150.000 €'), ('2021 a 2024', '125.000 a 180.000 € (poques unitats; les gairebé noves, a prop del preu de catàleg)')],
      'en': [('2017 to 2018', '€95,000 to 135,000'), ('2019 to 2020', '€115,000 to 150,000'), ('2021 to 2024', '€125,000 to 180,000 (few boats; nearly new ones close to list price)')]},
  es=dict(
    title='Merry Fisher 895 de segunda mano: guía y precios',
    desc='Filtraciones, dos motores, viento en maniobra, titulación y precios por años de un Jeanneau Merry Fisher 895 usado.',
    eyebrow='Modelos de ocasión · Pilothouse',
    h1='Jeanneau Merry Fisher 895 de segunda mano: qué mirar, precios y para quién es',
    lead='Es el hermano mayor del 795: casi 9 metros con dos camarotes, aseo, salón cerrado y puerta lateral para amarrar sin ayuda. Lo buscan familias que quieren pasar fines de semana largos a bordo, también en Baleares, sin irse a un barco intraborda de 10 metros. Va con uno o dos fuerabordas, así que el mantenimiento es más sencillo que el de un cabinado clásico. A cambio, es más caro de comprar y de mover, y en puerto el viento lo empuja bastante.',
    note='Años de producción: Serie 1 de 2017 a 2024; Serie 2 desde 2024 (casco nuevo y pasillo de estribor más ancho). Versiones Offshore (más combustible), Marlin (pesca) y Sport. Datos del fabricante y de pruebas publicadas; pueden variar según serie y año.',
    spec=[('Eslora total', '≈ 8,90 m (Serie 1)'), ('Eslora de casco', '7,98 m'), ('Manga', '2,99 m'), ('Peso', '≈ 3.060 kg'), ('Motor habitual', '2 x 150 a 2 x 200 CV fueraborda (también con un solo motor de 300 CV)'), ('Plazas / categoría', 'Hasta 10 personas · C'), ('Combustible / agua', '400 l / 100 l'), ('Cabina', 'Dos camarotes, aseo separado y salón convertible en cama')],
    mirar_h='Qué mirar en un Merry Fisher 895 usado',
    mirar_p='Además de lo general de la guía de <a href="../guias/que-mirar-comprar-barco-segunda-mano.html">qué mirar al comprar de segunda mano</a>, en este modelo me fijo en esto:',
    mirar=['Entradas de agua: los propietarios hablan sobre todo de la luz del techo, el techo corredizo y las plataformas de baño. Mira si hay manchas, juntas cuarteadas o agua en las sentinas.',
           'Dos motores, dos historiales: pide las facturas de mantenimiento de cada uno por separado y comprueba que las horas cuadran. Es normal ver de 150 a 600 horas según el año.',
           'Maniobra con viento: tiene mucha obra muerta y en puerto se mueve. Comprueba que la hélice de proa y los flaps funcionan, porque se usan mucho.',
           'Instalación eléctrica: en barcos con muchos añadidos (electrónica, inversor, placas) revisa el cuadro y el cableado; no todo lo instalado después está bien hecho.',
           'En mar corta a mucha velocidad puede dar golpes de proa si se lleva con prisa; en la prueba de mar fíjate en cómo entra en la ola y en el estado del casco en la zona de proa.'],
    note_pr='Rangos sacados de anuncios en portales europeos (España y, sobre todo, Francia) en octubre de 2026, con motores incluidos. Muchas unidades están en Francia: suelen estar algo más baratas, pero hay que sumar transporte, cambio de bandera y los impuestos que correspondan. Lo explico en la <a href="../guias/comprar-barco-francia-italia-matricular-espana.html">guía de importación</a>.',
    gastos='Para la titulación cuenta la eslora de casco, no la total. El fabricante da 7,98 metros de casco, así que en principio basta el <a href="../titulaciones/">PNB</a> (de día y hasta 5 millas); para navegar de noche, ir más lejos o cruzar a Baleares necesitas el PER. Comprueba siempre la eslora que figura en los papeles del barco concreto. Si ya está matriculado en España no se vuelve a pagar el impuesto de matriculación; si viene de fuera, con casi 9 metros de eslora total consulta con la gestoría si le toca el 12 % (guía del <a href="../guias/impuesto-matriculacion-barcos.html">IEDMT</a>). Al comprar pagarás el ITP (en Cataluña, el 5 % del precio) y la tasa de Capitanía; lo detallo en la guía de <a href="../guias/papeles-vender-barco-cambio-titularidad.html">papeles y cambio de nombre</a>. El amarre de 9 metros en la costa catalana ronda los 3.000 a 5.000 euros al año según el puerto; tarifas en la <a href="../guias/amarres-cataluna-tipos-precios-alquiler-compra.html">guía de amarres</a>.',
    alt='<a href="jeanneau-merry-fisher-795.html">Jeanneau Merry Fisher 795</a> (la misma idea, más pequeño y bastante más barato); <a href="beneteau-antares-8.html">Beneteau Antares 8</a> y el Antares 9, su rival directo de la misma eslora. Y si no tienes claro el tipo de barco, el <a href="../que-barco-necesito.html">test de dos minutos</a> te lo aclara.',
    faq=[('¿Cuánto cuesta un Jeanneau Merry Fisher 895 de segunda mano?', None),
         ('¿Qué título necesito para llevar un Jeanneau Merry Fisher 895?', 'Cuenta la eslora de casco, que según el fabricante es de 7,98 metros: en principio basta el PNB, que permite navegar de día y hasta 5 millas. Para ir más lejos, de noche o a Baleares, el PER. Confírmalo con la eslora que figura en los papeles del barco.'),
         ('¿Se paga impuesto de matriculación al comprar un Jeanneau Merry Fisher 895 usado?', 'No, si ya está matriculado en España: se paga una sola vez. Si lo traes de fuera, consulta con la gestoría, porque su eslora total pasa de 8 metros. Al comprar un usado español pagas el ITP (5 % en Cataluña) y la tasa de Capitanía.')],
    faq_price='Depende sobre todo del año, los motores y el equipamiento. {r}. Son rangos orientativos sacados de anuncios de portales europeos en octubre de 2026; es el precio que se pide, no el de cierre, y el real se cierra mirando el barco.',
    aviso='Esta ficha es orientativa y la escribo desde mi experiencia como broker; no sustituye a una inspección del barco concreto. Los precios cambian con la temporada y el estado de cada unidad. Fuentes: datos técnicos del fabricante (Jeanneau) y pruebas publicadas en prensa náutica; precios a partir de anuncios de portales europeos en octubre de 2026.'),
  ca=dict(
    title='Merry Fisher 895 de segona mà: guia i preus',
    desc="Filtracions, dos motors, vent en maniobra, titulació i preus per anys d'un Jeanneau Merry Fisher 895 usat.",
    eyebrow="Models d'ocasió · Pilothouse",
    h1='Jeanneau Merry Fisher 895 de segona mà: què mirar, preus i per a qui és',
    lead="És el germà gran del 795: gairebé 9 metres amb dos camarots, lavabo, saló tancat i porta lateral per amarrar sense ajuda. El busquen famílies que volen passar caps de setmana llargs a bord, també a Balears, sense anar a un vaixell intrabord de 10 metres. Va amb un o dos foraborda, així que el manteniment és més senzill que el d'un cabinat clàssic. A canvi, és més car de comprar i de moure, i a port el vent l'empeny força.",
    note="Anys de producció: Sèrie 1 de 2017 a 2024; Sèrie 2 des de 2024 (buc nou i passadís d'estribord més ample). Versions Offshore (més combustible), Marlin (pesca) i Sport. Dades del fabricant i de proves publicades; poden variar segons sèrie i any.",
    spec=[('Eslora total', '≈ 8,90 m (Sèrie 1)'), ('Eslora de buc', '7,98 m'), ('Mànega', '2,99 m'), ('Pes', '≈ 3.060 kg'), ('Motor habitual', '2 x 150 a 2 x 200 CV foraborda (també amb un sol motor de 300 CV)'), ('Places / categoria', 'Fins a 10 persones · C'), ('Combustible / aigua', '400 l / 100 l'), ('Cabina', 'Dos camarots, lavabo separat i saló convertible en llit')],
    mirar_h='Què mirar en un Merry Fisher 895 usat',
    mirar_p='A més del general de la guia de <a href="/ca/guias/que-mirar-comprar-barco-segunda-mano.html">què mirar en comprar de segona mà</a>, en aquest model em fixo en això:',
    mirar=["Entrades d'aigua: els propietaris parlen sobretot del llum del sostre, el sostre corredís i les plataformes de bany. Mira si hi ha taques, juntes clivellades o aigua a les sentines.",
           "Dos motors, dos historials: demana les factures de manteniment de cadascun per separat i comprova que les hores quadren. És normal veure de 150 a 600 hores segons l'any.",
           "Maniobra amb vent: té molta obra morta i a port es mou. Comprova que l'hèlix de proa i els flaps funcionen, perquè es fan servir molt.",
           "Instal·lació elèctrica: en vaixells amb molts afegits (electrònica, inversor, plaques) revisa el quadre i el cablejat; no tot el que s'ha instal·lat després està ben fet.",
           "Amb mar curta i molta velocitat pot donar cops de proa si es porta amb pressa; a la prova de mar fixa't en com entra a l'onada i en l'estat del buc a la zona de proa."],
    note_pr="Rangs extrets d'anuncis en portals europeus (Espanya i, sobretot, França) l'octubre de 2026, amb motors inclosos. Moltes unitats són a França: solen estar una mica més barates, però cal sumar-hi transport, canvi de bandera i els impostos que corresponguin. Ho explico a la <a href=\"/ca/guias/comprar-barco-francia-italia-matricular-espana.html\">guia d'importació</a>.",
    gastos="Per a la titulació compta l'eslora de buc, no la total. El fabricant dona 7,98 metres de buc, així que en principi n'hi ha prou amb el <a href=\"/ca/titulaciones/\">PNB</a> (de dia i fins a 5 milles); per navegar de nit, anar més lluny o creuar a Balears necessites el PER. Comprova sempre l'eslora que figura als papers del vaixell concret. Si ja està matriculat a Espanya no es torna a pagar l'impost de matriculació; si ve de fora, amb gairebé 9 metres d'eslora total consulta amb la gestoria si li toca el 12 % (guia de l'<a href=\"/ca/guias/impuesto-matriculacion-barcos.html\">IEDMT</a>). En comprar pagaràs l'ITP (a Catalunya, el 5 % del preu) i la taxa de Capitania; ho detallo a la guia de <a href=\"/ca/guias/papeles-vender-barco-cambio-titularidad.html\">papers i canvi de nom</a>. L'amarratge de 9 metres a la costa catalana va dels 3.000 als 5.000 euros l'any segons el port; tarifes a la <a href=\"/ca/guias/amarres-cataluna-tipos-precios-alquiler-compra.html\">guia d'amarratges</a>.",
    alt='<a href="jeanneau-merry-fisher-795.html">Jeanneau Merry Fisher 795</a> (la mateixa idea, més petit i força més barat); <a href="beneteau-antares-8.html">Beneteau Antares 8</a> i l\'Antares 9, el seu rival directe de la mateixa eslora. I si no tens clar el tipus de vaixell, el <a href="/ca/que-barco-necesito.html">test de dos minuts</a> t\'ho aclareix.',
    faq=[('Quant costa un Jeanneau Merry Fisher 895 de segona mà?', None),
         ('Quin títol necessito per portar un Jeanneau Merry Fisher 895?', "Compta l'eslora de buc, que segons el fabricant és de 7,98 metres: en principi n'hi ha prou amb el PNB, que permet navegar de dia i fins a 5 milles. Per anar més lluny, de nit o a Balears, el PER. Confirma-ho amb l'eslora que figura als papers del vaixell."),
         ('Es paga impost de matriculació en comprar un Jeanneau Merry Fisher 895 usat?', "No, si ja està matriculat a Espanya: es paga una sola vegada. Si el portes de fora, consulta-ho amb la gestoria, perquè la seva eslora total passa de 8 metres. En comprar un usat espanyol pagues l'ITP (5 % a Catalunya) i la taxa de Capitania.")],
    faq_price="Depèn sobretot de l'any, els motors i l'equipament. {r}. Són rangs orientatius extrets d'anuncis de portals europeus l'octubre de 2026; és el preu que es demana, no el de tancament, i el real es tanca mirant el vaixell.",
    aviso="Aquesta fitxa és orientativa i l'escric des de la meva experiència com a broker; no substitueix una inspecció del vaixell concret. Els preus canvien amb la temporada i l'estat de cada unitat. Fonts: dades tècniques del fabricant (Jeanneau) i proves publicades en premsa nàutica; preus a partir d'anuncis de portals europeus l'octubre de 2026."),
  en=dict(
    title='Used Jeanneau Merry Fisher 895: guide and prices',
    desc='Leaks, twin engines, handling in wind, licence and prices by year for a used Jeanneau Merry Fisher 895.',
    eyebrow='Used models · Pilothouse',
    h1='Used Jeanneau Merry Fisher 895: what to check, prices and who it suits',
    lead="The 795's big brother: almost 9 metres with two cabins, heads, an enclosed saloon and a side door for mooring single-handed. It's what families look for when they want long weekends aboard, including trips to the Balearics, without moving up to a 10-metre inboard boat. It runs on one or two outboards, so maintenance is simpler than on a classic cruiser. On the other hand it costs more to buy and to run, and in the marina the wind pushes it around.",
    note='Production years: Series 1 from 2017 to 2024; Series 2 since 2024 (new hull and a wider starboard side deck). Offshore (more fuel), Marlin (fishing) and Sport versions. Manufacturer data and published tests; may vary by series and year.',
    spec=[('Length overall', '≈ 8.90 m (Series 1)'), ('Hull length', '7.98 m'), ('Beam', '2.99 m'), ('Weight', '≈ 3,060 kg'), ('Typical engines', '2 x 150 to 2 x 200 hp outboards (also a single 300 hp)'), ('People / category', 'Up to 10 people · C'), ('Fuel / water', '400 l / 100 l'), ('Cabin', 'Two cabins, separate heads and a saloon that converts into a berth')],
    mirar_h='What to check on a used Merry Fisher 895',
    mirar_p='Besides the general points in the guide to <a href="/en/guias/que-mirar-comprar-barco-segunda-mano.html">what to check when buying a used boat</a>, on this model I focus on this:',
    mirar=['Water ingress: owners mainly mention the roof light, the sliding roof and the bathing platforms. Look for stains, cracked seals or water in the bilges.',
           'Two engines, two histories: ask for the service invoices for each engine separately and check the hours add up. Anything from 150 to 600 hours is normal depending on the year.',
           'Handling in wind: there is a lot of topside and it moves around in the marina. Check the bow thruster and the trim tabs work, because they get used a lot.',
           'Electrics: on boats with many add-ons (electronics, inverter, solar panels) check the switch panel and wiring; not everything fitted later is done well.',
           'In a short sea at speed it can slam if driven hard; on the sea trial watch how it takes the waves and check the forward part of the hull.'],
    note_pr='Ranges from listings on European portals (Spain and, above all, France) in October 2026, engines included. Many boats are in France: they are often a little cheaper, but add transport, re-flagging and any taxes due. I cover this in the <a href="/en/guias/comprar-barco-francia-italia-matricular-espana.html">import guide</a>.',
    gastos='For licensing it is the hull length that counts, not the overall length. The manufacturer gives a hull length of 7.98 metres, so in principle the <a href="/en/titulaciones/">PNB</a> is enough (daytime, up to 5 nm); to sail at night, further out or across to the Balearics you need the PER. Always check the length shown on the papers of the specific boat. If it is already registered in Spain the registration tax is not paid again; if it comes from abroad, with almost 9 metres overall ask your gestoría whether the 12% applies (see the <a href="/en/guias/impuesto-matriculacion-barcos.html">IEDMT guide</a>). When buying you pay transfer tax (ITP, 5% of the price in Catalonia) and the Harbour Master\'s fee; I cover this in the guide to <a href="/en/guias/papeles-vender-barco-cambio-titularidad.html">paperwork and change of ownership</a>. A 9-metre berth on the Catalan coast costs around €3,000 to 5,000 a year depending on the marina; rates are in the <a href="/en/guias/amarres-cataluna-tipos-precios-alquiler-compra.html">mooring guide</a>.',
    alt='The <a href="jeanneau-merry-fisher-795.html">Jeanneau Merry Fisher 795</a> (the same idea, smaller and quite a bit cheaper); the <a href="beneteau-antares-8.html">Beneteau Antares 8</a> and the Antares 9, its direct rival at the same length. And if you\'re not sure which type of boat suits you, the <a href="/en/que-barco-necesito.html">two-minute test</a> will clarify it.',
    faq=[('How much does a used Jeanneau Merry Fisher 895 cost?', None),
         ('What licence do I need to skipper a Jeanneau Merry Fisher 895?', 'It is the hull length that counts, which the manufacturer gives as 7.98 metres: in principle the PNB is enough, allowing daytime sailing up to 5 nm. To go further, at night or to the Balearics, you need the PER. Check it against the length on the boat\'s papers.'),
         ('Is registration tax due when buying a used Jeanneau Merry Fisher 895?', 'Not if it is already registered in Spain: it is only paid once. If you bring one from abroad, check with a gestoría, because its overall length is over 8 metres. When buying a Spanish-registered boat you pay transfer tax (ITP, 5% in Catalonia) and the Harbour Master\'s fee.')],
    faq_price='It mainly depends on the year, the engines and the equipment. {r}. These are indicative ranges from European listings in October 2026; they are asking prices, not sale prices, and the real price is settled by viewing the boat.',
    aviso='This guide is indicative and written from my experience as a broker; it doesn\'t replace a survey of the specific boat. Prices change with the season and each unit\'s condition. Sources: manufacturer technical data (Jeanneau) and tests published in the nautical press; prices from European listings in October 2026.'),
)
# ---------------------------------------------------------------- FLYER 8 SUNDECK
M['beneteau-flyer-8-sundeck'] = dict(
  tpl='beneteau-flyer-7-7-sundeck', names=[('Flyer 7.7 SUNdeck', 'Flyer 8 SUNdeck'), ('Flyer%207.7%20SUNdeck', 'Flyer%208%20SUNdeck')],
  brand='Beneteau', product='Beneteau Flyer 8 SUNdeck', len=8.17, types=['sundeck', 'open'],
  idx={'es': ('Sundeck', 'Desde 2018'), 'ca': ('Sundeck', 'Des de 2018'), 'en': ('Sundeck', 'Since 2018')},
  pr={'es': [('2019 a 2020', '60.000 a 80.000 €'), ('2021 a 2024', '72.500 a 92.500 € (según motor y horas)')],
      'ca': [('2019 a 2020', '60.000 a 80.000 €'), ('2021 a 2024', '72.500 a 92.500 € (segons motor i hores)')],
      'en': [('2019 to 2020', '€60,000 to 80,000'), ('2021 to 2024', '€72,500 to 92,500 (depending on engine and hours)')]},
  es=dict(
    title='Flyer 8 SUNdeck de segunda mano: guía y precios',
    desc='Motor, horas de alquiler, cabina, titulación y precios por años de un Beneteau Flyer 8 SUNdeck usado.',
    eyebrow='Modelos de ocasión · Sundeck',
    h1='Beneteau Flyer 8 SUNdeck de segunda mano: qué mirar, precios y para quién es',
    lead='Es el sustituto del Flyer 7.7 SUNdeck: algo más largo, con casco Air Step y un solo fueraborda, que simplifica mucho el mantenimiento. Es un barco de día para seis u ocho personas, con solárium a proa y a popa, y una cabina pensada para una siesta o alguna noche suelta, no para pasar la semana. Se ve mucho en Cataluña y en flotas de alquiler de Baleares, y eso obliga a mirar bien de dónde viene cada unidad.',
    note='Años de producción: desde 2018 (presentado en el salón de Cannes); hoy se vende la versión V2. Datos del fabricante y de pruebas publicadas; pueden variar según serie y año.',
    spec=[('Eslora total', '8,17 m'), ('Manga', '2,53 m'), ('Peso en rosca', '≈ 2.250 a 2.300 kg según versión'), ('Potencia máxima', '350 CV'), ('Motor habitual', 'Un fueraborda de 250 a 350 CV (Suzuki, Mercury o Yamaha)'), ('Plazas / categoría', '10 personas · C'), ('Combustible', '340 l'), ('Cabina', 'Dinette convertible en cama doble y aseo separado')],
    mirar_h='Qué mirar en un Flyer 8 SUNdeck usado',
    mirar_p='Además de lo general de la guía de <a href="../guias/que-mirar-comprar-barco-segunda-mano.html">qué mirar al comprar de segunda mano</a>, en este modelo me fijo en esto:',
    mirar=['Si ha sido de alquiler: hay bastantes unidades de chárter, sobre todo en Baleares, con muchas horas en pocos años. No es malo por sí mismo, pero pide el historial de uso y de mantenimiento del motor.',
           'Motor y reglaje: con 350 CV va muy rápido pero hay que saber trimarlo; con 250 CV el barco queda más equilibrado. Revisa el espejo de popa y la fijación del motor.',
           'Cabina: la altura interior es justa (alrededor de 1,50 m en el aseo). Si quieres dormir a bordo a menudo, visítalo antes de decidir.',
           'Tomas de aire del casco Air Step: comprueba que estén limpias y sin grietas cuando el barco esté en seco.',
           'Año de modelo y año de matriculación no siempre coinciden; pide la documentación y compara con lo que dice el anuncio, igual que el equipamiento (nevera, cocina exterior, electrónica).'],
    note_pr='Rangos sacados de anuncios en portales europeos (España y Francia) en octubre de 2026, con motor incluido. Hay pocas unidades de 2023 y 2024 a la venta, así que el último tramo es más orientativo. Un barco en Francia suele estar más barato pero hay que sumar transporte, cambio de bandera y los impuestos que correspondan. Lo explico en la <a href="../guias/comprar-barco-francia-italia-matricular-espana.html">guía de importación</a>.',
    gastos='Para la titulación cuenta la eslora de casco que figura en los papeles, no la total de 8,17 metros, que incluye la plataforma. Si la de casco queda por debajo de 8 metros, basta el <a href="../titulaciones/">PNB</a> (de día y hasta 5 millas); si no, necesitas el PER. Pídela antes de comprar. Si ya está matriculado en España no se vuelve a pagar el impuesto de matriculación; si viene de fuera, consulta con la gestoría si le toca el 12 % (guía del <a href="../guias/impuesto-matriculacion-barcos.html">IEDMT</a>). Al comprar pagarás el ITP (en Cataluña, el 5 % del precio) y la tasa de Capitanía; lo detallo en la guía de <a href="../guias/papeles-vender-barco-cambio-titularidad.html">papeles y cambio de nombre</a>. En amarre, un barco de esta eslora cuesta entre 2.500 y 4.000 euros al año en la costa catalana según el puerto, y bastante menos en marina seca; tienes las tarifas en la <a href="../guias/amarres-cataluna-tipos-precios-alquiler-compra.html">guía de amarres</a>.',
    alt='<a href="beneteau-flyer-7-7-sundeck.html">Beneteau Flyer 7.7 SUNdeck</a> (su antecesor, la misma idea por bastante menos dinero); <a href="jeanneau-cap-camarat-7-5-wa.html">Jeanneau Cap Camarat 7.5 WA</a> (más marinero, menos solárium); el Quicksilver Activ 755 Sundeck, si buscas algo parecido algo más barato. Y si no tienes claro el tipo de barco, el <a href="../que-barco-necesito.html">test de dos minutos</a> te lo aclara.',
    faq=[('¿Cuánto cuesta un Beneteau Flyer 8 SUNdeck de segunda mano?', None),
         ('¿Qué título necesito para llevar un Beneteau Flyer 8 SUNdeck?', 'Depende de la eslora de casco que figure en sus papeles, no de la total de 8,17 metros: si queda por debajo de 8 metros, basta el PNB (de día y hasta 5 millas); si no, el PER. Con la Licencia de navegación no llega: el límite son 6 metros.'),
         ('¿Se paga impuesto de matriculación al comprar un Beneteau Flyer 8 SUNdeck usado?', 'No, si ya está matriculado en España: el impuesto se paga una sola vez. Si lo traes de fuera, consulta con la gestoría. Al comprar sí pagas el ITP (impuesto de transmisiones, en Cataluña el 5 %) y la tasa de cambio de titularidad en Capitanía.')],
    faq_price='Depende sobre todo del año, el motor y las horas. {r}. Son rangos orientativos sacados de anuncios de portales europeos en octubre de 2026; es el precio que se pide, no el de cierre, y el real se cierra mirando el barco.',
    aviso='Esta ficha es orientativa y la escribo desde mi experiencia como broker; no sustituye a una inspección del barco concreto. Los precios cambian con la temporada y el estado de cada unidad. Fuentes: datos técnicos del fabricante (Beneteau) y pruebas publicadas en prensa náutica; precios a partir de anuncios de portales europeos en octubre de 2026.'),
  ca=dict(
    title='Flyer 8 SUNdeck de segona mà: guia i preus',
    desc="Motor, hores de lloguer, cabina, titulació i preus per anys d'un Beneteau Flyer 8 SUNdeck usat.",
    eyebrow="Models d'ocasió · Sundeck",
    h1='Beneteau Flyer 8 SUNdeck de segona mà: què mirar, preus i per a qui és',
    lead="És el substitut del Flyer 7.7 SUNdeck: una mica més llarg, amb buc Air Step i un sol foraborda, que simplifica molt el manteniment. És un vaixell de dia per a sis o vuit persones, amb solàrium a proa i a popa, i una cabina pensada per a una migdiada o alguna nit solta, no per passar-hi la setmana. Se'n veuen molts a Catalunya i en flotes de lloguer de Balears, i això obliga a mirar bé d'on ve cada unitat.",
    note="Anys de producció: des de 2018 (presentat al saló de Canes); avui es ven la versió V2. Dades del fabricant i de proves publicades; poden variar segons sèrie i any.",
    spec=[('Eslora total', '8,17 m'), ('Mànega', '2,53 m'), ('Pes en rosca', '≈ 2.250 a 2.300 kg segons versió'), ('Potència màxima', '350 CV'), ('Motor habitual', 'Un foraborda de 250 a 350 CV (Suzuki, Mercury o Yamaha)'), ('Places / categoria', '10 persones · C'), ('Combustible', '340 l'), ('Cabina', 'Dinette convertible en llit doble i lavabo separat')],
    mirar_h='Què mirar en un Flyer 8 SUNdeck usat',
    mirar_p='A més del general de la guia de <a href="/ca/guias/que-mirar-comprar-barco-segunda-mano.html">què mirar en comprar de segona mà</a>, en aquest model em fixo en això:',
    mirar=["Si ha estat de lloguer: hi ha força unitats de xàrter, sobretot a Balears, amb moltes hores en pocs anys. No és dolent per si mateix, però demana l'historial d'ús i de manteniment del motor.",
           "Motor i reglatge: amb 350 CV va molt ràpid però cal saber trimar-lo; amb 250 CV el vaixell queda més equilibrat. Revisa el mirall de popa i la fixació del motor.",
           "Cabina: l'alçada interior és justa (al voltant d'1,50 m al lavabo). Si vols dormir a bord sovint, visita'l abans de decidir.",
           "Preses d'aire del buc Air Step: comprova que estiguin netes i sense esquerdes quan el vaixell estigui en sec.",
           "L'any de model i l'any de matriculació no sempre coincideixen; demana la documentació i compara-la amb el que diu l'anunci, igual que l'equipament (nevera, cuina exterior, electrònica)."],
    note_pr="Rangs extrets d'anuncis en portals europeus (Espanya i França) l'octubre de 2026, amb motor inclòs. Hi ha poques unitats de 2023 i 2024 a la venda, així que l'últim tram és més orientatiu. Un vaixell a França sol estar més barat però cal sumar-hi transport, canvi de bandera i els impostos que corresponguin. Ho explico a la <a href=\"/ca/guias/comprar-barco-francia-italia-matricular-espana.html\">guia d'importació</a>.",
    gastos="Per a la titulació compta l'eslora de buc que figura als papers, no la total de 8,17 metres, que inclou la plataforma. Si la de buc queda per sota de 8 metres, n'hi ha prou amb el <a href=\"/ca/titulaciones/\">PNB</a> (de dia i fins a 5 milles); si no, necessites el PER. Demana-la abans de comprar. Si ja està matriculat a Espanya no es torna a pagar l'impost de matriculació; si ve de fora, consulta amb la gestoria si li toca el 12 % (guia de l'<a href=\"/ca/guias/impuesto-matriculacion-barcos.html\">IEDMT</a>). En comprar pagaràs l'ITP (a Catalunya, el 5 % del preu) i la taxa de Capitania; ho detallo a la guia de <a href=\"/ca/guias/papeles-vender-barco-cambio-titularidad.html\">papers i canvi de nom</a>. En amarratge, un vaixell d'aquesta eslora costa entre 2.500 i 4.000 euros l'any a la costa catalana segons el port, i força menys en marina seca; tens les tarifes a la <a href=\"/ca/guias/amarres-cataluna-tipos-precios-alquiler-compra.html\">guia d'amarratges</a>.",
    alt='<a href="beneteau-flyer-7-7-sundeck.html">Beneteau Flyer 7.7 SUNdeck</a> (el seu antecessor, la mateixa idea per força menys diners); <a href="jeanneau-cap-camarat-7-5-wa.html">Jeanneau Cap Camarat 7.5 WA</a> (més mariner, menys solàrium); el Quicksilver Activ 755 Sundeck, si busques una cosa semblant una mica més barata. I si no tens clar el tipus de vaixell, el <a href="/ca/que-barco-necesito.html">test de dos minuts</a> t\'ho aclareix.',
    faq=[('Quant costa un Beneteau Flyer 8 SUNdeck de segona mà?', None),
         ('Quin títol necessito per portar un Beneteau Flyer 8 SUNdeck?', "Depèn de l'eslora de buc que figuri als seus papers, no de la total de 8,17 metres: si queda per sota de 8 metres, n'hi ha prou amb el PNB (de dia i fins a 5 milles); si no, el PER. Amb la Llicència de navegació no arriba: el límit són 6 metres."),
         ('Es paga impost de matriculació en comprar un Beneteau Flyer 8 SUNdeck usat?', "No, si ja està matriculat a Espanya: l'impost es paga una sola vegada. Si el portes de fora, consulta-ho amb la gestoria. En comprar sí que pagues l'ITP (impost de transmissions, a Catalunya el 5 %) i la taxa de canvi de titularitat a Capitania.")],
    faq_price="Depèn sobretot de l'any, el motor i les hores. {r}. Són rangs orientatius extrets d'anuncis de portals europeus l'octubre de 2026; és el preu que es demana, no el de tancament, i el real es tanca mirant el vaixell.",
    aviso="Aquesta fitxa és orientativa i l'escric des de la meva experiència com a broker; no substitueix una inspecció del vaixell concret. Els preus canvien amb la temporada i l'estat de cada unitat. Fonts: dades tècniques del fabricant (Beneteau) i proves publicades en premsa nàutica; preus a partir d'anuncis de portals europeus l'octubre de 2026."),
  en=dict(
    title='Used Beneteau Flyer 8 SUNdeck: guide and prices',
    desc='Engine, charter hours, cabin, licence and prices by year for a used Beneteau Flyer 8 SUNdeck.',
    eyebrow='Used models · Sundeck',
    h1='Used Beneteau Flyer 8 SUNdeck: what to check, prices and who it suits',
    lead='The replacement for the Flyer 7.7 SUNdeck: a little longer, with an Air Step hull and a single outboard, which keeps maintenance simple. It is a day boat for six to eight people, with sunpads forward and aft, and a cabin meant for a nap or the odd night, not for spending the week aboard. You see a lot of them in Catalonia and in Balearic charter fleets, which means you need to check where each boat has come from.',
    note='Production years: since 2018 (launched at the Cannes boat show); the current version is the V2. Manufacturer data and published tests; may vary by series and year.',
    spec=[('Length overall', '8.17 m'), ('Beam', '2.53 m'), ('Light weight', '≈ 2,250 to 2,300 kg depending on version'), ('Max power', '350 hp'), ('Typical engine', 'A single 250 to 350 hp outboard (Suzuki, Mercury or Yamaha)'), ('People / category', '10 people · C'), ('Fuel', '340 l'), ('Cabin', 'Dinette that converts into a double berth, separate heads')],
    mirar_h='What to check on a used Flyer 8 SUNdeck',
    mirar_p='Besides the general points in the guide to <a href="/en/guias/que-mirar-comprar-barco-segunda-mano.html">what to check when buying a used boat</a>, on this model I focus on this:',
    mirar=['Ex-charter boats: there are quite a few, especially in the Balearics, with a lot of hours in a few years. That is not bad in itself, but ask for the usage and engine service history.',
           'Engine and trim: with 350 hp it is very fast but you need to know how to trim it; with 250 hp the boat is better balanced. Check the transom and the engine mounting.',
           'Cabin: headroom is limited (around 1.50 m in the heads). If you want to sleep aboard often, see it in person before deciding.',
           'Air Step hull vents: check they are clean and crack-free when the boat is out of the water.',
           'Model year and registration year do not always match; ask for the papers and compare them with the listing, and do the same with the equipment (fridge, outdoor galley, electronics).'],
    note_pr='Ranges from listings on European portals (Spain and France) in October 2026, engine included. There are few 2023 and 2024 boats for sale, so the last band is more of a guide. A boat in France is often cheaper, but add transport, re-flagging and any taxes due. I cover this in the <a href="/en/guias/comprar-barco-francia-italia-matricular-espana.html">import guide</a>.',
    gastos='For licensing it is the hull length on the papers that counts, not the 8.17 metres overall, which includes the platform. If the hull length is under 8 metres, the <a href="/en/titulaciones/">PNB</a> is enough (daytime, up to 5 nm); if not, you need the PER. Ask for it before buying. If it is already registered in Spain the registration tax is not paid again; if it comes from abroad, ask your gestoría whether the 12% applies (see the <a href="/en/guias/impuesto-matriculacion-barcos.html">IEDMT guide</a>). When buying you pay transfer tax (ITP, 5% of the price in Catalonia) and the Harbour Master\'s fee; I cover this in the guide to <a href="/en/guias/papeles-vender-barco-cambio-titularidad.html">paperwork and change of ownership</a>. Mooring for a boat this length runs €2,500 to 4,000 a year on the Catalan coast depending on the marina, and considerably less on dry storage; rates are in the <a href="/en/guias/amarres-cataluna-tipos-precios-alquiler-compra.html">mooring guide</a>.',
    alt='The <a href="beneteau-flyer-7-7-sundeck.html">Beneteau Flyer 7.7 SUNdeck</a> (its predecessor, the same idea for quite a bit less); the <a href="jeanneau-cap-camarat-7-5-wa.html">Jeanneau Cap Camarat 7.5 WA</a> (more seaworthy, less sunbathing space); the Quicksilver Activ 755 Sundeck if you want something similar for a bit less. And if you\'re not sure which type of boat suits you, the <a href="/en/que-barco-necesito.html">two-minute test</a> will clarify it.',
    faq=[('How much does a used Beneteau Flyer 8 SUNdeck cost?', None),
         ('What licence do I need to skipper a Beneteau Flyer 8 SUNdeck?', 'It depends on the hull length on its papers, not the 8.17 metres overall: if it is under 8 metres, the PNB is enough (daytime, up to 5 nm); if not, the PER. The Licencia de navegación is not enough: its limit is 6 metres.'),
         ('Is registration tax due when buying a used Beneteau Flyer 8 SUNdeck?', 'Not if it is already registered in Spain: the tax is only paid once. If you bring one from abroad, check with a gestoría. When buying you do pay transfer tax (ITP, 5% in Catalonia) and the Harbour Master\'s change-of-ownership fee.')],
    faq_price='It mainly depends on the year, the engine and the hours. {r}. These are indicative ranges from European listings in October 2026; they are asking prices, not sale prices, and the real price is settled by viewing the boat.',
    aviso='This guide is indicative and written from my experience as a broker; it doesn\'t replace a survey of the specific boat. Prices change with the season and each unit\'s condition. Sources: manufacturer technical data (Beneteau) and tests published in the nautical press; prices from European listings in October 2026.'),
)

H = {'es': ('Ficha rápida', 'Precio de segunda mano orientativo', 'Título, impuestos y gastos fijos', 'Alternativas que miraría', 'Preguntas frecuentes'),
     'ca': ('Fitxa ràpida', 'Preu de segona mà orientatiu', 'Títol, impostos i despeses fixes', 'Alternatives que miraria', 'Preguntes freqüents'),
     'en': ('Quick specs', 'Indicative used price', 'Licence, taxes and fixed costs', "Alternatives I'd consider", 'Frequently asked questions')}
META = {'es': ('Por Juan Morante', 'Precios revisados en octubre de 2026'), 'ca': ('Per Juan Morante', "Preus revisats l'octubre de 2026"), 'en': ('By Juan Morante', 'Prices reviewed October 2026')}

def build(slug, m, l):
    t = m[l]; tpl = m['tpl']
    h = open(f'{R}{P(l)}/modelos/{tpl}.html', encoding='utf-8').read()
    h = h.replace(tpl, slug)
    for a, b in m['names']: h = h.replace(a, b)
    h = re.sub(r'<title>.*?</title>', f'<title>{t["title"]}</title>', h, 1)
    h = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda x: x.group(1) + t['desc'], h)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda x: x.group(1) + t['title'], h)
    rtxt = '; '.join(f'{a}: {b}' for a, b in m['pr'][l])
    fp = t['faq_price'].format(r=rtxt)
    faqs = [(q, a if a else fp) for q, a in t['faq']]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": t['h1'], "author": {"@type": "Person", "name": "Juan Morante"}, "publisher": {"@type": "Organization", "name": "Plata Marine"},
         "datePublished": FECHA, "dateModified": FECHA, "inLanguage": l, "mainEntityOfPage": f"https://www.platamarine.com{P(l)}/modelos/{slug}.html",
         "about": {"@type": "Product", "name": m['product'], "brand": {"@type": "Brand", "name": m['brand']}}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]}
    h = re.sub(r'(<script type="application/ld\+json">\n).*?(\n</script>)', lambda x: x.group(1) + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + x.group(2), h, 1, flags=re.S)
    hd = H[l]; me = META[l]
    top = (f'<article>\n      <header>\n        <p class="eyebrow">{t["eyebrow"]}</p>\n        <h1>{t["h1"]}</h1>\n'
           f'        <div class="meta"><span>{me[0]}</span><span>{me[1]}</span></div>\n        <p class="lead">{t["lead"]}</p>\n      </header>\n'
           f'      <div class="prose">\n        <h2 id="ficha">{hd[0]}</h2>\n        <p class="note">{t["note"]}</p>\n        {spec(t["spec"])}\n\n'
           f'        <h2 id="mirar">{t["mirar_h"]}</h2>\n        <p>{t["mirar_p"]}</p>\n        <ul>{"".join("<li>%s</li>" % x for x in t["mirar"])}</ul>\n\n'
           f'        <h2 id="precio">{hd[1]}</h2>\n        {table(m["pr"][l], l)}\n        <p class="note">{t["note_pr"]}</p>\n\n        <div class="cta2">')
    h, n = re.subn(r'<article>\s*<header>.*?<div class="cta2">', lambda x: top, h, 1, flags=re.S); assert n == 1
    h = re.sub(r'<!--pm-sim-->[\s\S]*?<!--/pm-sim-->\n?', '', h)
    faqhtml = ''.join(f'<h3>{q}</h3><p>{a}</p>' for q, a in faqs)
    bot = (f'<h2 id="gastos">{hd[2]}</h2>\n        <p>{t["gastos"]}</p>\n\n        <h2 id="alternativas">{hd[3]}</h2>\n        <p>{t["alt"]}</p>\n\n'
           f'        <h2 id="faq">{hd[4]}</h2>\n        {faqhtml}\n        <p class="aviso">{t["aviso"]}</p>')
    h, n = re.subn(r'<h2 id="gastos">.*?<p class="aviso">.*?</p>', lambda x: bot, h, 1, flags=re.S); assert n == 1
    open(f'{R}{P(l)}/modelos/{slug}.html', 'w', encoding='utf-8').write(h)

for slug, m in M.items():
    for l in ('es', 'ca', 'en'): build(slug, m, l)
print('ok')
