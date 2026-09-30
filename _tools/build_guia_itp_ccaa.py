# -*- coding: utf-8 -*-
"""Guía: ITP al comprar un barco usado por comunidad autónoma (ES/CA/EN)."""
import re, json, html, urllib.parse as u, os
ROOT='/home/claude/platamarine/'
PRE={'es':'','ca':'ca/','en':'en/'}
SLUG='guias/itp-comprar-barco-usado-por-comunidad.html'
IMG='https://images.unsplash.com/photo-1778977772022-e3ab5550bc2a?auto=format&fit=crop&w=800&q=70'
def esc(t): return html.escape(t, quote=True)
def q(t): return u.quote(t, safe='')

ROWS=[  # comunidad, tipo, nota  (ES); CA/EN traducen la nota
 ('Andalucía','4 %/8 %','8 % si la eslora supera los 8 m'),
 ('Aragón','4 %',''),
 ('Asturias','4 %/8 %','8 % si la eslora supera los 8 m'),
 ('Baleares','4 %',''),
 ('Canarias','5,5 %',''),
 ('Cantabria','4 % / 8 %','8 % si la eslora supera los 8 m'),
 ('Castilla-La Mancha','6 %',''),
 ('Castilla y León','5 %',''),
 ('Cataluña','5 %','Plazo de un mes'),
 ('Comunidad Valenciana','6 %/8 %','8 % si supera 8 m de eslora o 20.000 € de valor'),
 ('Extremadura','6 %',''),
 ('Galicia','1 %','Tipo específico para embarcaciones de recreo'),
 ('La Rioja','4 %',''),
 ('Madrid','4 %',''),
 ('Murcia','4 %',''),
 ('Navarra','4 %','Régimen foral'),
 ('País Vasco','4 %','Régimen foral (Álava, Bizkaia, Gipuzkoa)'),
 ('Ceuta y Melilla','2 %','Residentes'),
 ('No residentes en España','4 %','Tipo estatal, se presenta en la Agencia Tributaria'),
]
NOTE_T={'ca':{'8 % si la eslora supera los 8 m':'8 % si l\'eslora supera els 8 m','Plazo de un mes':'Termini d\'un mes','8 % si supera 8 m de eslora o 20.000 € de valor':'8 % si supera 8 m d\'eslora o 20.000 € de valor','Tipo específico para embarcaciones de recreo':'Tipus específic per a embarcacions d\'esbarjo','Régimen foral':'Règim foral','Régimen foral (Álava, Bizkaia, Gipuzkoa)':'Règim foral (Àlaba, Biscaia, Guipúscoa)','Residentes':'Residents','Tipo estatal, se presenta en la Agencia Tributaria':'Tipus estatal, es presenta a l\'Agència Tributària'},
        'en':{'8 % si la eslora supera los 8 m':'8 % if the boat is over 8 m long','Plazo de un mes':'One-month deadline','8 % si supera 8 m de eslora o 20.000 € de valor':'8 % if over 8 m long or worth more than €20,000','Tipo específico para embarcaciones de recreo':'Specific rate for pleasure boats','Régimen foral':'Regional (foral) tax regime','Régimen foral (Álava, Bizkaia, Gipuzkoa)':'Regional (foral) regime (Álava, Bizkaia, Gipuzkoa)','Residentes':'Residents','Tipo estatal, se presenta en la Agencia Tributaria':'State rate, filed with the national tax agency'}}
REG_T={'ca':{'Cataluña':'Catalunya','Comunidad Valenciana':'Comunitat Valenciana','Baleares':'Illes Balears','Castilla y León':'Castella i Lleó','Castilla-La Mancha':'Castella-la Manxa','Aragón':'Aragó','Galicia':'Galícia','No residentes en España':'No residents a Espanya','Ceuta y Melilla':'Ceuta i Melilla','Canarias':'Canàries','País Vasco':'País Basc','Asturias':'Astúries','Andalucía':'Andalusia','Cantabria':'Cantàbria'},
       'en':{'Cataluña':'Catalonia','Comunidad Valenciana':'Valencia region','Baleares':'Balearic Islands','Castilla y León':'Castile and León','Castilla-La Mancha':'Castilla-La Mancha','Aragón':'Aragon','No residentes en España':'Non-residents in Spain','Ceuta y Melilla':'Ceuta and Melilla','Canarias':'Canary Islands','País Vasco':'Basque Country','Andalucía':'Andalusia','Navarra':'Navarre'}}

C={
'es':dict(
 title='ITP al comprar un barco usado: cuánto se paga en cada comunidad autónoma',
 desc='Tabla con el tipo de ITP que paga el comprador de un barco de segunda mano en cada comunidad autónoma (Cataluña 5 %, Baleares 4 %, Valencia 6-8 %, Galicia 1 %…), sobre qué valor se calcula, en qué plazo y cómo se presenta el modelo 620.',
 eyebrow='Guías · Fiscalidad', by='Por Juan Morante', upd='Actualizado septiembre 2026', read='6 min de lectura',
 lead='Cuando compras un barco usado a un particular en España pagas el Impuesto de Transmisiones Patrimoniales (ITP). Lo fija cada comunidad autónoma, y va del 1 % de Galicia al 8 % de algunas comunidades para esloras grandes. Aquí tienes la tabla completa y lo que necesitas saber para no llevarte sorpresas.',
 tag='Fiscalidad', card_desc='Tabla por comunidades, sobre qué valor se calcula, plazos y modelo 620. Con ejemplos.',
 toc=[('que-es','Qué es y cuándo se paga'),('tabla','La tabla por comunidades'),('base','Sobre qué valor se calcula'),('ejemplos','Tres ejemplos'),('como','Cómo se paga, paso a paso'),('errores','Errores que veo a menudo'),('faq','Preguntas frecuentes')],
 secs=[
  ('que-es','Qué es y cuándo se paga','<p>El ITP (Impuesto sobre Transmisiones Patrimoniales Onerosas) grava la compra de bienes usados entre particulares. En náutica se aplica cuando compras a un <strong>particular</strong> un barco que ya está matriculado en España. Lo paga siempre el <strong>comprador</strong>.</p><p>Hay dos casos en los que no se paga ITP: si el vendedor es una <strong>empresa o un profesional</strong> (la operación lleva IVA en lugar de ITP), y si el barco es nuevo o viene de fuera de España sin matricular, que es cuando entra en juego el <a href="/guias/impuesto-matriculacion-barcos.html">impuesto de matriculación</a>.</p><p>Un detalle que sorprende a muchos: el impuesto se paga en la comunidad autónoma donde <strong>reside el comprador</strong>, no donde está el barco ni donde vive el vendedor. Si vives en Madrid y compras un barco en Palma, liquidas en Madrid al 4 %.</p>'),
  ('tabla','La tabla por comunidades','__TABLE__<p class="aviso">Tipos aplicables a embarcaciones de recreo usadas según la normativa autonómica revisada en septiembre de 2026. Algunas comunidades aplican un tipo superior a partir de 8 metros de eslora o de cierto valor: compruébalo antes de cerrar el precio. Si tu comunidad no figura o tienes dudas, consulta la agencia tributaria autonómica.</p>'),
  ('base','Sobre qué valor se calcula','<p>La base del impuesto es el <strong>mayor</strong> de dos valores: el precio que figura en el contrato de compraventa o el <strong>valor de tablas</strong> que publica cada año el Ministerio de Hacienda en su orden de precios medios de venta de embarcaciones. Esa orden asigna un valor por marca, modelo y año, con un porcentaje de depreciación según la antigüedad.</p><p>Por eso no sirve de nada poner en el contrato un precio por debajo del real: si Hacienda ve que el valor de tablas es mayor, liquida sobre ese valor y puede reclamar la diferencia con intereses. Si el barco está por debajo de tablas por su estado, se puede justificar con un peritaje, pero es un camino más largo.</p>'),
  ('ejemplos','Tres ejemplos','<ul><li><strong>Comprador en Cataluña, barco de 7,5 m por 60.000 €:</strong> 5 % de 60.000 = <strong>3.000 €</strong>, a la Agència Tributària de Catalunya en el plazo de un mes.</li><li><strong>Comprador en la Comunidad Valenciana, barco de 8,5 m por 60.000 €:</strong> al superar los 8 m se aplica el 8 %: <strong>4.800 €</strong>. El mismo barco con 7,99 m pagaría el 6 %: 3.600 €.</li><li><strong>Comprador en Galicia, barco de 10 m por 90.000 €:</strong> 1 % = <strong>900 €</strong>, uno de los tipos más bajos de España.</li></ul><p>Si el valor de tablas de ese modelo y año fuera superior al precio pactado, el cálculo se haría sobre el valor de tablas.</p>'),
  ('como','Cómo se paga, paso a paso','<ol><li><strong>Contrato de compraventa</strong> firmado por ambas partes, con precio, fecha, datos del barco (matrícula, NIB, marca, modelo, eslora) y de las dos personas.</li><li><strong>Modelo 620</strong> (en algunas comunidades 600 o 621), que se rellena y paga por internet en la sede de la agencia tributaria de tu comunidad. Necesitas certificado digital o Cl@ve, o hacerlo a través de una gestoría.</li><li><strong>Plazo:</strong> con carácter general 30 días hábiles desde la firma; en Cataluña es un mes y en Andalucía dos meses. Fuera de plazo hay recargos.</li><li><strong>Justificante de pago:</strong> es uno de los documentos que Capitanía Marítima pide para el <a href="/guias/papeles-vender-barco-cambio-titularidad.html">cambio de titularidad</a>. Sin ITP pagado, el barco no pasa a tu nombre.</li></ol>'),
  ('errores','Errores que veo a menudo','<ul><li><strong>Pagar en la comunidad equivocada.</strong> El impuesto va a la comunidad donde reside el comprador. Si se paga en otra, hay que pedir la devolución y volver a liquidar.</li><li><strong>Declarar un precio bajo.</strong> Hacienda cruza el precio con las tablas y liquida la diferencia, con intereses y a veces sanción.</li><li><strong>Pensar que la bandera extranjera te libra.</strong> Si el comprador reside en España, paga ITP aunque el barco lleve bandera belga o polaca.</li><li><strong>Olvidar los 8 metros.</strong> En Andalucía, Asturias, Cantabria y la Comunidad Valenciana el tipo sube al 8 % a partir de esa eslora, y en Valencia también por valor.</li><li><strong>Dejarlo para el final.</strong> El plazo corre desde la firma del contrato, no desde la entrega del barco.</li></ul>'),
 ],
 faq=[
  ('¿Quién paga el ITP al comprar un barco usado?','El comprador. El vendedor no paga ITP; en su caso tributa la ganancia en su IRPF si vende por más de lo que le costó, algo poco habitual en barcos.'),
  ('¿Se paga ITP si compro el barco a una empresa?','No. Si el vendedor es una empresa o un profesional que actúa como tal, la venta lleva IVA (21 %) y no ITP. Conviene pedir factura.'),
  ('¿Dónde se paga el ITP de un barco?','En la comunidad autónoma donde reside el comprador, con el modelo 620 (o el que use esa comunidad), normalmente por internet en la sede de su agencia tributaria.'),
  ('¿Qué pasa si pago el ITP fuera de plazo?','Se aplican recargos que crecen con el retraso (del 1 % mensual hasta el 15 %, más intereses a partir de un año). Si te requiere Hacienda antes de que presentes, puede haber sanción.'),
 ],
 fiscal='Información fiscal orientativa, revisada en septiembre de 2026 según el Real Decreto Legislativo 1/1993, el Real Decreto 828/1995 y la normativa autonómica vigente. No es asesoramiento fiscal. El importe final depende del valor que fije Hacienda, de la situación del barco y de posibles exenciones, y la normativa puede cambiar. Confírmalo con tu gestoría o con la Administración antes de comprar.',
 aside=('¿Vas a comprar?','Te digo qué ITP te toca antes de que hagas la oferta.','Cuéntame el barco que miras, dónde vives y el precio, y te contesto con el cálculo y lo que hay que revisar. Sin compromiso.','Hablar con Juan por WhatsApp'),
 wa='Hola Juan, tengo una duda sobre el ITP de un barco que quiero comprar.',
 toc_t='En esta guía', other='Otras guías', allg='Todas las guías de Plata Marine',
 th=('Comunidad autónoma','Tipo de ITP','Observaciones'),
),
'ca':dict(
 title='ITP en comprar un vaixell usat: quant es paga a cada comunitat autònoma',
 desc='Taula amb el tipus d\'ITP que paga el comprador d\'un vaixell de segona mà a cada comunitat autònoma (Catalunya 5 %, Balears 4 %, València 6-8 %, Galícia 1 %…), sobre quin valor es calcula, en quin termini i com es presenta el model 620.',
 eyebrow='Guies · Fiscalitat', by='Per Juan Morante', upd='Actualitzat setembre 2026', read='6 min de lectura',
 lead='Quan compres un vaixell usat a un particular a Espanya pagues l\'Impost de Transmissions Patrimonials (ITP). El fixa cada comunitat autònoma, i va de l\'1 % de Galícia al 8 % d\'algunes comunitats per a eslores grans. Aquí tens la taula completa i el que necessites saber per no endur-te sorpreses.',
 tag='Fiscalitat', card_desc='Taula per comunitats, sobre quin valor es calcula, terminis i model 620. Amb exemples.',
 toc=[('que-es','Què és i quan es paga'),('tabla','La taula per comunitats'),('base','Sobre quin valor es calcula'),('ejemplos','Tres exemples'),('como','Com es paga, pas a pas'),('errores','Errors que veig sovint'),('faq','Preguntes freqüents')],
 secs=[
  ('que-es','Què és i quan es paga','<p>L\'ITP (Impost sobre Transmissions Patrimonials Oneroses) grava la compra de béns usats entre particulars. En nàutica s\'aplica quan compres a un <strong>particular</strong> un vaixell que ja està matriculat a Espanya. El paga sempre el <strong>comprador</strong>.</p><p>Hi ha dos casos en què no es paga ITP: si el venedor és una <strong>empresa o un professional</strong> (l\'operació porta IVA en lloc d\'ITP), i si el vaixell és nou o ve de fora d\'Espanya sense matricular, que és quan entra en joc l\'<a href="/ca/guias/impuesto-matriculacion-barcos.html">impost de matriculació</a>.</p><p>Un detall que sorprèn molta gent: l\'impost es paga a la comunitat autònoma on <strong>resideix el comprador</strong>, no on és el vaixell ni on viu el venedor. Si vius a Madrid i compres un vaixell a Palma, liquides a Madrid al 4 %.</p>'),
  ('tabla','La taula per comunitats','__TABLE__<p class="aviso">Tipus aplicables a embarcacions d\'esbarjo usades segons la normativa autonòmica revisada el setembre de 2026. Algunes comunitats apliquen un tipus superior a partir de 8 metres d\'eslora o d\'un cert valor: comprova-ho abans de tancar el preu. Si la teva comunitat no hi figura o tens dubtes, consulta l\'agència tributària autonòmica.</p>'),
  ('base','Sobre quin valor es calcula','<p>La base de l\'impost és el <strong>més gran</strong> de dos valors: el preu que figura al contracte de compravenda o el <strong>valor de taules</strong> que publica cada any el Ministeri d\'Hisenda a la seva ordre de preus mitjans de venda d\'embarcacions. Aquesta ordre assigna un valor per marca, model i any, amb un percentatge de depreciació segons l\'antiguitat.</p><p>Per això no serveix de res posar al contracte un preu per sota del real: si Hisenda veu que el valor de taules és més alt, liquida sobre aquest valor i pot reclamar la diferència amb interessos. Si el vaixell està per sota de taules pel seu estat, es pot justificar amb un peritatge, però és un camí més llarg.</p>'),
  ('ejemplos','Tres exemples','<ul><li><strong>Comprador a Catalunya, vaixell de 7,5 m per 60.000 €:</strong> 5 % de 60.000 = <strong>3.000 €</strong>, a l\'Agència Tributària de Catalunya en el termini d\'un mes.</li><li><strong>Comprador a la Comunitat Valenciana, vaixell de 8,5 m per 60.000 €:</strong> en superar els 8 m s\'aplica el 8 %: <strong>4.800 €</strong>. El mateix vaixell amb 7,99 m pagaria el 6 %: 3.600 €.</li><li><strong>Comprador a Galícia, vaixell de 10 m per 90.000 €:</strong> 1 % = <strong>900 €</strong>, un dels tipus més baixos d\'Espanya.</li></ul><p>Si el valor de taules d\'aquell model i any fos superior al preu pactat, el càlcul es faria sobre el valor de taules.</p>'),
  ('como','Com es paga, pas a pas','<ol><li><strong>Contracte de compravenda</strong> signat per totes dues parts, amb preu, data, dades del vaixell (matrícula, NIB, marca, model, eslora) i de les dues persones.</li><li><strong>Model 620</strong> (en algunes comunitats 600 o 621), que s\'omple i es paga per internet a la seu de l\'agència tributària de la teva comunitat. Necessites certificat digital o Cl@ve, o fer-ho a través d\'una gestoria.</li><li><strong>Termini:</strong> amb caràcter general 30 dies hàbils des de la signatura; a Catalunya és un mes i a Andalusia dos mesos. Fora de termini hi ha recàrrecs.</li><li><strong>Justificant de pagament:</strong> és un dels documents que Capitania Marítima demana per al <a href="/ca/guias/papeles-vender-barco-cambio-titularidad.html">canvi de titularitat</a>. Sense l\'ITP pagat, el vaixell no passa al teu nom.</li></ol>'),
  ('errores','Errors que veig sovint','<ul><li><strong>Pagar a la comunitat equivocada.</strong> L\'impost va a la comunitat on resideix el comprador. Si es paga en una altra, cal demanar la devolució i tornar a liquidar.</li><li><strong>Declarar un preu baix.</strong> Hisenda creua el preu amb les taules i liquida la diferència, amb interessos i de vegades sanció.</li><li><strong>Pensar que la bandera estrangera te\'n lliura.</strong> Si el comprador resideix a Espanya, paga ITP encara que el vaixell porti bandera belga o polonesa.</li><li><strong>Oblidar els 8 metres.</strong> A Andalusia, Astúries, Cantàbria i la Comunitat Valenciana el tipus puja al 8 % a partir d\'aquesta eslora, i a València també per valor.</li><li><strong>Deixar-ho per al final.</strong> El termini corre des de la signatura del contracte, no des del lliurament del vaixell.</li></ul>'),
 ],
 faq=[
  ('Qui paga l\'ITP en comprar un vaixell usat?','El comprador. El venedor no paga ITP; si de cas tributa el guany a l\'IRPF si ven per més del que li va costar, cosa poc habitual en vaixells.'),
  ('Es paga ITP si compro el vaixell a una empresa?','No. Si el venedor és una empresa o un professional que actua com a tal, la venda porta IVA (21 %) i no ITP. Convé demanar factura.'),
  ('On es paga l\'ITP d\'un vaixell?','A la comunitat autònoma on resideix el comprador, amb el model 620 (o el que faci servir aquella comunitat), normalment per internet a la seu de la seva agència tributària.'),
  ('Què passa si pago l\'ITP fora de termini?','S\'apliquen recàrrecs que creixen amb el retard (de l\'1 % mensual fins al 15 %, més interessos a partir d\'un any). Si Hisenda et requereix abans que presentis, hi pot haver sanció.'),
 ],
 fiscal='Informació fiscal orientativa, revisada el setembre de 2026 segons el Reial decret legislatiu 1/1993, el Reial decret 828/1995 i la normativa autonòmica vigent. No és assessorament fiscal. L\'import final depèn del valor que fixi Hisenda, de la situació del vaixell i de possibles exempcions, i la normativa pot canviar. Confirma-ho amb la teva gestoria o amb l\'Administració abans de comprar.',
 aside=('Vols comprar?','Et dic quin ITP et toca abans que facis l\'oferta.','Explica\'m el vaixell que mires, on vius i el preu, i et contesto amb el càlcul i el que cal revisar. Sense compromís.','Parlar amb Juan per WhatsApp'),
 wa='Hola Juan, tinc un dubte sobre l\'ITP d\'un vaixell que vull comprar.',
 toc_t='En aquesta guia', other='Altres guies', allg='Totes les guies de Plata Marine',
 th=('Comunitat autònoma','Tipus d\'ITP','Observacions'),
),
'en':dict(
 title='Transfer tax (ITP) when buying a used boat: what you pay in each Spanish region',
 desc='Table of the ITP transfer tax a buyer pays on a second-hand boat in each Spanish region (Catalonia 5 %, Balearics 4 %, Valencia 6-8 %, Galicia 1 %…), what value it is calculated on, the deadline and how to file form 620.',
 eyebrow='Guides · Tax', by='By Juan Morante', upd='Updated September 2026', read='6 min read',
 lead='When you buy a used boat from a private individual in Spain you pay the Transfer Tax (ITP). Each autonomous region sets its own rate, from 1 % in Galicia to 8 % in some regions for larger boats. Here is the full table and what you need to know to avoid surprises.',
 tag='Tax', card_desc='Table by region, what value it is calculated on, deadlines and form 620. With examples.',
 toc=[('que-es','What it is and when you pay it'),('tabla','The table by region'),('base','What value it is calculated on'),('ejemplos','Three examples'),('como','How to pay it, step by step'),('errores','Mistakes I see often'),('faq','Frequently asked questions')],
 secs=[
  ('que-es','What it is and when you pay it','<p>ITP (Impuesto sobre Transmisiones Patrimoniales Onerosas) is the tax on the purchase of used goods between private individuals. In boating it applies when you buy from a <strong>private seller</strong> a boat that is already registered in Spain. The <strong>buyer</strong> always pays it.</p><p>There are two cases where no ITP is due: when the seller is a <strong>company or a professional</strong> (the sale carries VAT instead), and when the boat is new or comes from outside Spain unregistered, which is when the <a href="/en/guias/impuesto-matriculacion-barcos.html">registration tax</a> comes into play.</p><p>A detail that surprises many people: the tax is paid in the region where the <strong>buyer lives</strong>, not where the boat is or where the seller lives. If you live in Madrid and buy a boat in Palma, you pay in Madrid at 4 %.</p>'),
  ('tabla','The table by region','__TABLE__<p class="aviso">Rates for used pleasure boats under the regional rules reviewed in September 2026. Some regions apply a higher rate above 8 metres in length or above a certain value: check before you settle the price. If your region is not listed or you are unsure, ask the regional tax agency.</p>'),
  ('base','What value it is calculated on','<p>The tax base is the <strong>higher</strong> of two values: the price in the sale contract or the <strong>table value</strong> that the Ministry of Finance publishes each year in its order of average sale prices for boats. That order assigns a value by make, model and year, with a depreciation percentage according to age.</p><p>That is why it is pointless to put a price below the real one in the contract: if the tax office sees that the table value is higher, it assesses on that value and can claim the difference with interest. If the boat is worth less than the table because of its condition, you can justify it with a survey, but it is a longer road.</p>'),
  ('ejemplos','Three examples','<ul><li><strong>Buyer in Catalonia, 7.5 m boat for €60,000:</strong> 5 % of 60,000 = <strong>€3,000</strong>, paid to the Catalan tax agency within one month.</li><li><strong>Buyer in the Valencia region, 8.5 m boat for €60,000:</strong> over 8 m the rate is 8 %: <strong>€4,800</strong>. The same boat at 7.99 m would pay 6 %: €3,600.</li><li><strong>Buyer in Galicia, 10 m boat for €90,000:</strong> 1 % = <strong>€900</strong>, one of the lowest rates in Spain.</li></ul><p>If the table value for that model and year were higher than the agreed price, the tax would be calculated on the table value.</p>'),
  ('como','How to pay it, step by step','<ol><li><strong>Sale contract</strong> signed by both parties, with price, date, boat details (registration, NIB, make, model, length) and both people\'s details.</li><li><strong>Form 620</strong> (600 or 621 in some regions), filled in and paid online at your regional tax agency\'s website. You need a Spanish digital certificate or Cl@ve, or you can do it through an agency (gestoría).</li><li><strong>Deadline:</strong> generally 30 working days from signing; in Catalonia it is one month and in Andalusia two months. Late filing carries surcharges.</li><li><strong>Proof of payment:</strong> it is one of the documents the Capitanía Marítima requires for the <a href="/en/guias/papeles-vender-barco-cambio-titularidad.html">change of ownership</a>. Without ITP paid, the boat is not transferred to your name.</li></ol>'),
  ('errores','Mistakes I see often','<ul><li><strong>Paying in the wrong region.</strong> The tax goes to the region where the buyer lives. If it is paid elsewhere, you have to request a refund and file again.</li><li><strong>Declaring a low price.</strong> The tax office cross-checks the price with the tables and assesses the difference, with interest and sometimes a penalty.</li><li><strong>Thinking a foreign flag exempts you.</strong> If the buyer lives in Spain, ITP is due even if the boat flies a Belgian or Polish flag.</li><li><strong>Forgetting the 8 metres.</strong> In Andalusia, Asturias, Cantabria and the Valencia region the rate rises to 8 % above that length, and in Valencia also by value.</li><li><strong>Leaving it to the end.</strong> The deadline runs from the signing of the contract, not from the handover of the boat.</li></ul>'),
 ],
 faq=[
  ('Who pays ITP when buying a used boat?','The buyer. The seller does not pay ITP; at most they pay income tax on the gain if they sell for more than they paid, which is unusual with boats.'),
  ('Is ITP due if I buy the boat from a company?','No. If the seller is a company or a professional acting as such, the sale carries 21 % VAT and no ITP. Ask for an invoice.'),
  ('Where is the ITP on a boat paid?','In the autonomous region where the buyer lives, with form 620 (or the one that region uses), usually online at its tax agency\'s website.'),
  ('What happens if I pay ITP late?','Surcharges apply and grow with the delay (from 1 % per month up to 15 %, plus interest after a year). If the tax office requests it before you file, there may be a penalty.'),
 ],
 fiscal='Indicative tax information, reviewed in September 2026 under Royal Legislative Decree 1/1993, Royal Decree 828/1995 and the regional rules in force. This is not tax advice. The final amount depends on the value set by the tax office, the boat\'s situation and possible exemptions, and the rules may change. Confirm with your tax adviser or the tax office before buying.',
 aside=('Buying a boat?','I will tell you the ITP due before you make an offer.','Tell me the boat you are looking at, where you live and the price, and I will reply with the calculation and what to check. No obligation.','Talk to Juan on WhatsApp'),
 wa='Hi Juan, I have a question about the ITP on a boat I want to buy.',
 toc_t='In this guide', other='Other guides', allg='All Plata Marine guides',
 th=('Autonomous region','ITP rate','Notes'),
),
}

def table(lang, d):
    rows=''
    for reg,rate,note in ROWS:
        r=REG_T.get(lang,{}).get(reg,reg); n=NOTE_T.get(lang,{}).get(note,note) if note else ''
        if lang=='en': rate=rate.replace(',','.')
        rows+='<tr><td>%s</td><td>%s</td><td>%s</td></tr>'%(esc(r),esc(rate),esc(n))
    th=d['th']
    return '<div class="tbl"><table><thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table></div>'%(esc(th[0]),esc(th[1]),esc(th[2]),rows)

def build(lang):
    d=C[lang]; pre=PRE[lang]
    tpl=open(ROOT+pre+'guias/impuesto-matriculacion-barcos.html',encoding='utf-8').read()
    s=tpl
    s=re.sub(r'<title>.*?</title>','<title>'+esc(d['title'])+' · Plata Marine</title>',s,1)
    s=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+esc(d['desc'])+'">',s,1)
    s=s.replace('guias/impuesto-matriculacion-barcos.html',SLUG)
    s=re.sub(r'<meta property="og:title" content="[^"]*">','<meta property="og:title" content="'+esc(d['title'])+'">',s,1)
    s=re.sub(r'<meta property="og:description" content="[^"]*">','<meta property="og:description" content="'+esc(d['desc'])+'">',s,1)
    url='https://www.platamarine.com/'+pre+SLUG
    ld={"@context":"https://schema.org","@graph":[{"@type":"Article","headline":d['title'],"inLanguage":lang,"url":url,"description":d['desc'],"datePublished":"2026-09-30","dateModified":"2026-09-30","author":{"@type":"Person","name":"Juan Morante"},"publisher":{"@type":"Organization","name":"Plata Marine"}},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":qn,"acceptedAnswer":{"@type":"Answer","text":an}} for qn,an in d['faq']]}]}
    if '<script type="application/ld+json">' in s:
        s=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:'<script type="application/ld+json">\n'+json.dumps(ld,ensure_ascii=False)+'\n</script>',s,1,flags=re.S)
    else:
        s=s.replace('</head>','<script type="application/ld+json">\n'+json.dumps(ld,ensure_ascii=False)+'\n</script>\n</head>',1)
    # article
    secs=''.join('<h2 id="%s">%s</h2>%s\n'%(i,esc(h),b.replace('__TABLE__',table(lang,d))) for i,h,b in d['secs'])
    faq='<h2 id="faq">%s</h2>'%esc(d['toc'][-1][1])+''.join('<h3>%s</h3><p>%s</p>'%(esc(qn),esc(an)) for qn,an in d['faq'])
    article=('<header>\n        <p class="eyebrow">%s</p>\n        <h1>%s</h1>\n        <div class="meta"><span>%s</span><span>%s</span><span>%s</span></div>\n        <p class="lead">%s</p>\n      </header>\n\n      <div class="prose">\n        %s%s\n      </div>\n    <p class="aviso aviso-fiscal" style="font-size:.82em;opacity:.85">%s</p>\n    </article>'
             %(esc(d['eyebrow']),esc(d['title']),esc(d['by']),esc(d['upd']),esc(d['read']),esc(d['lead']),secs,faq,esc(d['fiscal'])))
    s=re.sub(r'<header>\s*<p class="eyebrow">.*?</article>',lambda m:article,s,1,flags=re.S)
    a=d['aside']
    aside=('<aside class="aside" aria-label="Contacto y navegación">\n      <div class="card">\n        <p class="eyebrow">%s</p>\n        <h3>%s</h3>\n        <p>%s</p>\n        <a class="btn btn-wa" href="https://wa.me/34633742973?text=%s" target="_blank" rel="noopener">%s</a>\n      </div>\n      <nav class="toc" aria-label="%s">\n        <p class="eyebrow">%s</p>\n        <ol>%s</ol>\n      </nav>\n      <div class="rel">\n        <p class="eyebrow">%s</p>\n        <a href="./">%s</a>\n      </div>\n    </aside>'
           %(esc(a[0]),esc(a[1]),esc(a[2]),q(d['wa']),esc(a[3]),esc(d['toc_t']),esc(d['toc_t']),''.join('<li><a href="#%s">%s</a></li>'%(i,esc(t)) for i,t in d['toc']),esc(d['other']),esc(d['allg'])))
    s=re.sub(r'<aside class="aside"[^>]*>.*?</aside>',lambda m:aside,s,1,flags=re.S)
    out=ROOT+pre+SLUG; open(out,'w',encoding='utf-8').write(s)
    # index card (guías) after the IEDMT card
    idx=ROOT+pre+'guias/index.html'; g=open(idx,encoding='utf-8').read()
    if 'itp-comprar-barco-usado-por-comunidad.html' not in g:
        m=re.search(r'<li><a href="impuesto-matriculacion-barcos.html">.*?</li>',g,re.S)
        card='<li><a href="itp-comprar-barco-usado-por-comunidad.html"><img src="%s" alt="" loading="lazy"><span class="g-body"><span class="tag">%s</span><h2>%s</h2><p>%s</p><span class="g-more">%s</span></span></a></li>'%(IMG,esc(d['tag']),esc(d['title']),esc(d['card_desc']),re.search(r'<span class="g-more">([^<]*)</span>',m.group(0)).group(1))
        g=g[:m.end()]+card+g[m.end():]; open(idx,'w',encoding='utf-8').write(g)
    # papeles-fiscalidad card
    pf=ROOT+pre+'papeles-fiscalidad/index.html'; p=open(pf,encoding='utf-8').read()
    if 'itp-comprar-barco-usado-por-comunidad.html' not in p:
        m=re.search(r'<li><a href="../guias/impuesto-matriculacion-barcos.html">.*?</li>',p,re.S)
        if m:
            card=m.group(0).replace('impuesto-matriculacion-barcos.html','itp-comprar-barco-usado-por-comunidad.html')
            card=re.sub(r'<h2>.*?</h2>','<h2>'+esc(d['title'])+'</h2>',card,1,flags=re.S)
            card=re.sub(r'<p>.*?</p>','<p>'+esc(d['card_desc'])+'</p>',card,1,flags=re.S)
            card=re.sub(r'src="[^"]*"','src="'+IMG+'"',card,1)
            p=p[:m.end()]+card+p[m.end():]; open(pf,'w',encoding='utf-8').write(p)
    return out

if __name__=='__main__':
    for l in PRE: print(build(l))
    sm=ROOT+'sitemap.xml'; s=open(sm,encoding='utf-8').read(); add=''
    for pre in ['','ca/','en/']:
        u_='https://www.platamarine.com/'+pre+SLUG
        if u_ not in s: add+='    <url><loc>%s</loc><lastmod>2026-09-30</lastmod><priority>0.7</priority></url>\n'%u_
    open(sm,'w',encoding='utf-8').write(s.replace('</urlset>',add+'</urlset>')); print('sitemap +',add.count('<url>'))
