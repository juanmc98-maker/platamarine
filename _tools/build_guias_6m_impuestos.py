# -*- coding: utf-8 -*-
"""Guías: barcos de 6 metros con camarote, e impuestos y gastos al comprar un barco (ES/CA/EN/FR).
Toma cabecera y pie de la guía de semirrígidas deportivas de cada idioma (igual que
build_guia_semirrigida_usada.py) y escribe /<lang>/guias/<slug>/index.html.
Uso: python3 _tools/build_guias_6m_impuestos.py  (desde la raíz del repo)"""
import re, json, os
from urllib.parse import quote

SRC = 'semirrigidas-deportivas-lujo'
BASE = 'https://www.platamarine.com'
DATE = '2026-10-29'
WA = 'https://wa.me/34633742973?text='
OG = {'es': '/og-image.jpg', 'ca': '/og-image-ca.jpg', 'en': '/og-image-en.jpg', 'fr': '/og-image-fr.jpg'}
QB = '/que-barco-necesito'

G = {}

# ====================================================================================
# 1) Barcos de 6 metros con camarote
# ====================================================================================
G['barcos-6-metros-con-camarote'] = {}
A = G['barcos-6-metros-con-camarote']

A['es'] = dict(
title='Barcos de 6 metros con camarote: qué mirar antes de comprar',
desc='Qué da de sí un barco de 6 metros con camarote, qué titulación necesitas, por qué la eslora exacta importa y qué revisar antes de comprar uno.',
h1='Barcos de 6 metros con camarote: qué esperar y qué mirar antes de comprar',
crumb='Barcos de 6 metros con camarote',
wa_head='Hola Juan, estoy buscando un barco de unos 6 metros con camarote.',
wa_card='Hola Juan, he visto un barco de unos 6 metros con camarote y quiero que lo miremos juntos antes de hacer una oferta.',
eyebrow='Guías · Compra',
meta='<span>Por Juan Morante</span><span>Actualizado octubre 2026</span><span>5 min de lectura</span>',
lead='Un barco de unos 6 metros con camarote es la puerta de entrada más habitual a la náutica: cabe en un amarre pequeño, se puede llevar en remolque y tiene un sitio donde resguardarse o echar una siesta. Pero no es un crucero. Esto es lo que da de sí, y lo que hay que mirar antes de comprarlo.',
body='''
        <h2 id="camarote">Qué da de sí un camarote en 6 metros</h2>
        <ul>
          <li><strong>Un refugio, no un dormitorio.</strong> Lo normal es una cama en proa para dos personas, justa de altura. Sirve para guardar cosas secas, cambiarse, resguardarse del sol o pasar alguna noche fondeado en verano.</li>
          <li><strong>El baño, si lo hay, es básico.</strong> En muchos es un WC portátil o químico bajo la cama o en un hueco. Si para ti el baño es importante, pregúntalo antes de ir a verlo.</li>
          <li><strong>Lo que se gana en cabina se pierde en bañera.</strong> Un barco con camarote de 6 m tiene menos sitio fuera que una open de la misma eslora. Piensa cuántos soléis salir y dónde vais a estar la mayor parte del día.</li>
        </ul>

        <h2 id="tipos">Tres formas de llevar el camarote</h2>
        <div class="tbl">
        <table>
          <thead><tr><th>Tipo</th><th>Cómo es</th><th>Para quién</th></tr></thead>
          <tbody>
            <tr><td>Cabinado o walkaround</td><td>Camarote en proa y paso lateral para ir a la punta</td><td>Pesca, fondear y salidas de día</td></tr>
            <tr><td>Timonera (pilothouse)</td><td>El puesto de gobierno va cerrado, con el camarote debajo o delante</td><td>Quien navega también fuera del verano o con viento</td></tr>
            <tr><td>Day cruiser o sundeck</td><td>Solárium en proa y un camarote pequeño debajo</td><td>Baño, calas y vida al sol</td></tr>
          </tbody>
        </table>
        </div>

        <h2 id="eslora">La eslora exacta importa más de lo que parece</h2>
        <p>En la documentación cuenta la eslora de casco, no el nombre del modelo. Y en torno a los 6 metros hay dos límites:</p>
        <ul>
          <li><strong>Titulación.</strong> Con la Licencia de Navegación puedes gobernar barcos de hasta 6 metros con la potencia que admita el fabricante, solo de día y sin alejarte más de 2 millas de un puerto o lugar de abrigo. Si pasa de 6 m, necesitas el PNB (hasta 8 m y 5 millas) o un título superior. Lo tienes en <a href="{p}/titulaciones/">titulaciones</a>.</li>
          <li><strong>ITB.</strong> En lista 7ª (uso privado), por debajo de 6 metros no hay reconocimientos periódicos; de 6 metros en adelante, como máximo cada 5 años. Lo explico en la <a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">guía de la ITB</a>.</li>
        </ul>
        <p>Por debajo de 8 metros no hay impuesto de matriculación, así que a esta eslora no es un factor. Si te interesa por qué, está en la guía del <a href="{p}/guias/impuesto-matriculacion-barcos">impuesto de matriculación</a>.</p>

        <h2 id="revisar">Qué revisar antes de comprar uno usado</h2>
        <ul>
          <li><strong>Humedad en el camarote:</strong> olor a cerrado, manchas en el techo o en los cojines, y de dónde entra el agua (escotilla, portillos, herrajes de cubierta).</li>
          <li><strong>Motor:</strong> año, horas y facturas, y arranque en frío. Casi todos llevan fueraborda; si es intraborda o de cola, la revisión de un mecánico es todavía más importante.</li>
          <li><strong>Casco y espejo de popa:</strong> sin grietas ni humedad alrededor del motor.</li>
          <li><strong>Papeles:</strong> hoja de asiento sin cargas y eslora de casco clara.</li>
          <li><strong>Remolque, si va con él:</strong> papeles, ITV si pasa de 750 kg y que tu coche y tu carné lo puedan llevar.</li>
        </ul>

        <h2 id="costes">Lo que cuesta después</h2>
        <p>Amarre según eslora (o nave y remolque), seguro de responsabilidad civil obligatorio, mantenimiento del motor cada año y antifouling si está en el agua. Lo cuento con números en la guía de <a href="{p}/guias/cuanto-cuesta-mantener-un-barco-cataluna">cuánto cuesta mantener un barco en Cataluña</a>. Y si compras a un particular, el ITP: en Cataluña, el 5 % (el de cada comunidad, en la <a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">guía del ITP</a>).</p>

        <h2 id="buscas">¿Buscas uno?</h2>
        <p>Ahora mismo no tengo ninguno de 6 metros con camarote en venta. Si buscas uno, <a href="{p}/alertas/">crea una alerta</a> y te aviso cuando entre; o haz el test de <a href="{p}{qb}">qué barco necesito</a> y te digo qué tipo te encaja. Si ya has visto uno, mándame las fotos y los datos y lo miramos juntos antes de que hagas una oferta.</p>
''',
cta_e='¿Ya has visto uno?', cta_t='Mándame las fotos y los datos.', cta_p='Lo miramos juntos antes de que hagas una oferta.', cta_b='Escribir a Juan por WhatsApp',
aviso='Guía orientativa. Lo que digo de titulaciones, ITB e impuestos se confirma con la documentación del barco antes de comprar.',
card_e='¿Buscas uno de 6 metros?', card_h='Te aviso cuando entre uno que encaje.', card_p='O mándame el que has visto y lo miramos juntos antes de hacer una oferta. Sin compromiso.', card_b='Hablar con Juan por WhatsApp',
toc_t='En esta guía', toc=[('camarote', 'Qué da de sí el camarote'), ('tipos', 'Tres formas de camarote'), ('eslora', 'La eslora exacta'), ('revisar', 'Qué revisar'), ('costes', 'Lo que cuesta después'), ('buscas', '¿Buscas uno?')],
rel_t='Otras guías', rel=[('/guias/que-mirar-comprar-barco-segunda-mano', 'Qué mirar al comprar un barco de segunda mano'), ('/guias/cuanto-cuesta-mantener-un-barco-cataluna', 'Cuánto cuesta mantener un barco'), ('/guias/impuestos-gastos-comprar-barco/', 'Impuestos y gastos al comprar un barco'), ('/guias/', 'Todas las guías de Plata Marine')],
)

A['ca'] = dict(
title='Vaixells de 6 metres amb cabina: què mirar abans de comprar',
desc='Què dona de si un vaixell de 6 metres amb cabina, quina titulació necessites, per què l’eslora exacta importa i què revisar abans de comprar-ne un.',
h1='Vaixells de 6 metres amb cabina: què esperar i què mirar abans de comprar',
crumb='Vaixells de 6 metres amb cabina',
wa_head='Hola Juan, busco un vaixell d’uns 6 metres amb cabina.',
wa_card='Hola Juan, he vist un vaixell d’uns 6 metres amb cabina i vull que el mirem junts abans de fer una oferta.',
eyebrow='Guies · Compra',
meta='<span>Per Juan Morante</span><span>Actualitzat octubre 2026</span><span>5 min de lectura</span>',
lead='Un vaixell d’uns 6 metres amb cabina és la porta d’entrada més habitual a la nàutica: cap en un amarratge petit, es pot portar amb remolc i té un lloc on resguardar-se o fer la migdiada. Però no és un creuer. Això és el que dona de si, i el que cal mirar abans de comprar-lo.',
body='''
        <h2 id="camarote">Què dona de si una cabina en 6 metres</h2>
        <ul>
          <li><strong>Un refugi, no un dormitori.</strong> El més normal és un llit a proa per a dues persones, just d’alçada. Serveix per guardar coses seques, canviar-se, resguardar-se del sol o passar alguna nit fondejat a l’estiu.</li>
          <li><strong>El bany, si n’hi ha, és bàsic.</strong> En molts és un WC portàtil o químic sota el llit o en un forat. Si per a tu el bany és important, pregunta-ho abans d’anar a veure’l.</li>
          <li><strong>El que es guanya a la cabina es perd a la banyera.</strong> Un vaixell amb cabina de 6 m té menys espai a fora que una open de la mateixa eslora. Pensa quants soleu sortir i on passareu la major part del dia.</li>
        </ul>

        <h2 id="tipos">Tres maneres de portar la cabina</h2>
        <div class="tbl">
        <table>
          <thead><tr><th>Tipus</th><th>Com és</th><th>Per a qui</th></tr></thead>
          <tbody>
            <tr><td>Cabinat o walkaround</td><td>Cabina a proa i pas lateral per anar a la punta</td><td>Pesca, fondejar i sortides de dia</td></tr>
            <tr><td>Timonera (pilothouse)</td><td>El lloc de govern va tancat, amb la cabina a sota o al davant</td><td>Qui navega també fora de l’estiu o amb vent</td></tr>
            <tr><td>Day cruiser o sundeck</td><td>Solàrium a proa i una cabina petita a sota</td><td>Bany, cales i vida al sol</td></tr>
          </tbody>
        </table>
        </div>

        <h2 id="eslora">L’eslora exacta importa més del que sembla</h2>
        <p>A la documentació compta l’eslora de casc, no el nom del model. I al voltant dels 6 metres hi ha dos límits:</p>
        <ul>
          <li><strong>Titulació.</strong> Amb la Llicència de Navegació pots governar vaixells de fins a 6 metres amb la potència que admeti el fabricant, només de dia i sense allunyar-te més de 2 milles d’un port o lloc d’abric. Si passa de 6 m, necessites el PNB (fins a 8 m i 5 milles) o un títol superior. Ho tens a <a href="{p}/titulaciones/">titulacions</a>.</li>
          <li><strong>ITB.</strong> A la llista 7a (ús privat), per sota de 6 metres no hi ha reconeixements periòdics; de 6 metres en amunt, com a màxim cada 5 anys. Ho explico a la <a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">guia de l’ITB</a>.</li>
        </ul>
        <p>Per sota de 8 metres no hi ha impost de matriculació, així que a aquesta eslora no és un factor. Si t’interessa per què, és a la guia de l’<a href="{p}/guias/impuesto-matriculacion-barcos">impost de matriculació</a>.</p>

        <h2 id="revisar">Què revisar abans de comprar-ne un de segona mà</h2>
        <ul>
          <li><strong>Humitat a la cabina:</strong> olor de tancat, taques al sostre o als coixins, i per on entra l’aigua (escotilla, portells, ferratges de coberta).</li>
          <li><strong>Motor:</strong> any, hores i factures, i arrencada en fred. Gairebé tots porten fora borda; si és intrabord o de cua, la revisió d’un mecànic és encara més important.</li>
          <li><strong>Casc i mirall de popa:</strong> sense esquerdes ni humitat al voltant del motor.</li>
          <li><strong>Papers:</strong> full d’assentament sense càrregues i eslora de casc clara.</li>
          <li><strong>Remolc, si hi va:</strong> papers, ITV si passa de 750 kg i que el teu cotxe i el teu carnet el puguin portar.</li>
        </ul>

        <h2 id="costes">El que costa després</h2>
        <p>Amarratge segons l’eslora (o nau i remolc), assegurança de responsabilitat civil obligatòria, manteniment del motor cada any i antifouling si és a l’aigua. Ho explico amb números a la guia de <a href="{p}/guias/cuanto-cuesta-mantener-un-barco-cataluna">quant costa mantenir un vaixell a Catalunya</a>. I si compres a un particular, l’ITP: a Catalunya, el 5 % (el de cada comunitat, a la <a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">guia de l’ITP</a>).</p>

        <h2 id="buscas">En busques un?</h2>
        <p>Ara mateix no en tinc cap de 6 metres amb cabina en venda. Si en busques un, <a href="{p}/alertas/">crea una alerta</a> i t’aviso quan n’entri un; o fes el test de <a href="{p}{qb}">quin vaixell necessito</a> i et dic quin tipus t’encaixa. Si ja n’has vist un, envia’m les fotos i les dades i el mirem junts abans que facis una oferta.</p>
''',
cta_e='Ja n’has vist un?', cta_t='Envia’m les fotos i les dades.', cta_p='El mirem junts abans que facis una oferta.', cta_b='Escriure a Juan per WhatsApp',
aviso='Guia orientativa. El que dic de titulacions, ITB i impostos es confirma amb la documentació del vaixell abans de comprar.',
card_e='En busques un de 6 metres?', card_h='T’aviso quan n’entri un que encaixi.', card_p='O envia’m el que has vist i el mirem junts abans de fer una oferta. Sense compromís.', card_b='Parlar amb Juan per WhatsApp',
toc_t='En aquesta guia', toc=[('camarote', 'Què dona de si la cabina'), ('tipos', 'Tres maneres de cabina'), ('eslora', 'L’eslora exacta'), ('revisar', 'Què revisar'), ('costes', 'El que costa després'), ('buscas', 'En busques un?')],
rel_t='Altres guies', rel=[('/guias/que-mirar-comprar-barco-segunda-mano', 'Què mirar en comprar un vaixell de segona mà'), ('/guias/cuanto-cuesta-mantener-un-barco-cataluna', 'Quant costa mantenir un vaixell'), ('/guias/impuestos-gastos-comprar-barco/', 'Impostos i despeses en comprar un vaixell'), ('/guias/', 'Totes les guies de Plata Marine')],
)

A['en'] = dict(
title='6-metre boats with a cabin: what to check before buying',
desc='What a boat of around 6 metres with a cabin can do, which licence you need, why the exact length matters and what to check before you buy one.',
h1='6-metre boats with a cabin: what to expect and what to check before you buy',
crumb='6-metre boats with a cabin',
wa_head='Hi Juan, I’m looking for a boat of around 6 metres with a cabin.',
wa_card='Hi Juan, I’ve seen a boat of around 6 metres with a cabin and I’d like us to look at it together before I make an offer.',
eyebrow='Guides · Buying',
meta='<span>By Juan Morante</span><span>Updated October 2026</span><span>5 min read</span>',
lead='A boat of around 6 metres with a cabin is the most common way into boating: it fits a small berth, it can go on a trailer and it has somewhere to shelter or have a nap. But it isn’t a cruiser. Here’s what it can do, and what to check before you buy one.',
body='''
        <h2 id="camarote">What a cabin gives you in 6 metres</h2>
        <ul>
          <li><strong>A shelter, not a bedroom.</strong> Usually there’s a berth in the bow for two people, with little headroom. It’s for keeping things dry, getting changed, getting out of the sun or spending the odd summer night at anchor.</li>
          <li><strong>The toilet, if there is one, is basic.</strong> On many boats it’s a portable or chemical toilet under the berth or tucked into a space. If a toilet matters to you, ask before you go and see the boat.</li>
          <li><strong>What you gain in the cabin you lose in the cockpit.</strong> A 6 m boat with a cabin has less room outside than an open boat of the same length. Think about how many of you usually go out and where you’ll spend most of the day.</li>
        </ul>

        <h2 id="tipos">Three ways to fit a cabin</h2>
        <div class="tbl">
        <table>
          <thead><tr><th>Type</th><th>What it’s like</th><th>Who it suits</th></tr></thead>
          <tbody>
            <tr><td>Cuddy cabin or walkaround</td><td>Cabin in the bow and side decks to walk to the front</td><td>Fishing, anchoring and day trips</td></tr>
            <tr><td>Pilothouse</td><td>The helm is enclosed, with the cabin below or in front</td><td>People who also go out outside summer or when it’s windy</td></tr>
            <tr><td>Day cruiser or sundeck</td><td>Sunpad on the bow and a small cabin underneath</td><td>Swimming, coves and time in the sun</td></tr>
          </tbody>
        </table>
        </div>

        <h2 id="eslora">The exact length matters more than it seems</h2>
        <p>What counts is the hull length in the boat’s papers, not the model name. And around 6 metres there are two thresholds in Spain:</p>
        <ul>
          <li><strong>Licence.</strong> With the Licencia de Navegación you can skipper boats up to 6 metres with the engine power the builder allows, in daylight only and no more than 2 miles from a port or sheltered spot. Over 6 m, you need the PNB (up to 8 m and 5 miles) or a higher licence. See <a href="{p}/titulaciones/">licences</a>.</li>
          <li><strong>ITB (technical inspection).</strong> On list 7 (private use), boats under 6 metres have no periodic inspections; from 6 metres up, at most every 5 years. I explain it in the <a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">ITB guide</a>.</li>
        </ul>
        <p>Under 8 metres there’s no registration tax, so at this length it isn’t a factor. If you want to know why, it’s in the guide to the <a href="{p}/guias/impuesto-matriculacion-barcos">registration tax (IEDMT)</a>.</p>

        <h2 id="revisar">What to check before buying a used one</h2>
        <ul>
          <li><strong>Damp in the cabin:</strong> a musty smell, stains on the headlining or the cushions, and where the water gets in (hatch, portholes, deck fittings).</li>
          <li><strong>Engine:</strong> year, hours and invoices, and a cold start. Almost all have an outboard; if it’s an inboard or a sterndrive, having a mechanic check it matters even more.</li>
          <li><strong>Hull and transom:</strong> no cracks or damp around the engine.</li>
          <li><strong>Paperwork:</strong> registry sheet (hoja de asiento) with no charges and a clear hull length.</li>
          <li><strong>Trailer, if it comes with one:</strong> papers, ITV (roadworthiness test) if it’s over 750 kg, and check that your car and your driving licence can tow it.</li>
        </ul>

        <h2 id="costes">What it costs afterwards</h2>
        <p>A berth based on length (or storage and a trailer), compulsory third-party insurance, yearly engine servicing and antifouling if it stays in the water. I put numbers on it in the guide to <a href="{p}/guias/cuanto-cuesta-mantener-un-barco-cataluna">what it costs to keep a boat in Catalonia</a>. And if you buy from a private seller, there’s ITP (transfer tax): 5% in Catalonia (each region’s rate is in the <a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">ITP guide</a>).</p>

        <h2 id="buscas">Looking for one?</h2>
        <p>Right now I don’t have any 6-metre boats with a cabin for sale. If you’re looking for one, <a href="{p}/alertas/">set up an alert</a> and I’ll let you know when one comes in; or take the <a href="{p}{qb}">which boat do I need</a> quiz and I’ll tell you which type suits you. If you’ve already seen one, send me the photos and details and we’ll look at it together before you make an offer.</p>
''',
cta_e='Already seen one?', cta_t='Send me the photos and details.', cta_p='We’ll look at it together before you make an offer.', cta_b='Message Juan on WhatsApp',
aviso='This guide is for guidance only. What I say about licences, ITB and taxes is confirmed against the boat’s paperwork before you buy.',
card_e='Looking for a 6-metre boat?', card_h='I’ll let you know when one that fits comes in.', card_p='Or send me the one you’ve seen and we’ll look at it together before you make an offer. No obligation.', card_b='Talk to Juan on WhatsApp',
toc_t='In this guide', toc=[('camarote', 'What the cabin gives you'), ('tipos', 'Three cabin layouts'), ('eslora', 'The exact length'), ('revisar', 'What to check'), ('costes', 'What it costs afterwards'), ('buscas', 'Looking for one?')],
rel_t='Other guides', rel=[('/guias/que-mirar-comprar-barco-segunda-mano', 'What to check when buying a used boat'), ('/guias/cuanto-cuesta-mantener-un-barco-cataluna', 'What it costs to keep a boat'), ('/guias/impuestos-gastos-comprar-barco/', 'Taxes and costs when buying a boat'), ('/guias/', 'All Plata Marine guides')],
)

A['fr'] = dict(
title='Bateau 6 mètres avec cabine : que vérifier avant d’acheter',
desc='Ce que permet un bateau de 6 mètres avec cabine, le permis qu’il faut en Espagne, pourquoi la longueur exacte compte et que vérifier avant d’acheter.',
h1='Bateaux de 6 mètres avec cabine : à quoi s’attendre et que vérifier avant d’acheter',
crumb='Bateaux de 6 mètres avec cabine',
wa_head='Bonjour Juan, je cherche un bateau d’environ 6 mètres avec cabine.',
wa_card='Bonjour Juan, j’ai vu un bateau d’environ 6 mètres avec cabine et j’aimerais qu’on le regarde ensemble avant de faire une offre.',
eyebrow='Guides · Acheter',
meta='<span>Par Juan Morante</span><span>Mis à jour en octobre 2026</span><span>5 min de lecture</span>',
lead='Un bateau d’environ 6 mètres avec cabine, c’est la porte d’entrée la plus courante dans la plaisance : il tient sur une petite place de port, il se transporte sur remorque et il a un endroit pour s’abriter ou faire la sieste. Mais ce n’est pas un bateau de croisière. Voici ce qu’il permet, et ce qu’il faut vérifier avant de l’acheter.',
body='''
        <h2 id="camarote">Ce que permet une cabine sur 6 mètres</h2>
        <ul>
          <li><strong>Un abri, pas une chambre.</strong> En général, une couchette à l’avant pour deux personnes, avec une hauteur juste. Elle sert à garder des affaires au sec, à se changer, à se mettre à l’ombre ou à passer une nuit au mouillage en été.</li>
          <li><strong>Les toilettes, s’il y en a, sont sommaires.</strong> Sur beaucoup de bateaux, ce sont des WC portables ou chimiques sous la couchette ou dans un coin. Si c’est important pour vous, demandez-le avant d’aller voir le bateau.</li>
          <li><strong>Ce qu’on gagne en cabine, on le perd dans le cockpit.</strong> Un bateau de 6 m avec cabine a moins de place à l’extérieur qu’un open de la même longueur. Pensez au nombre de personnes qui sortent d’habitude et à l’endroit où vous passerez la plus grande partie de la journée.</li>
        </ul>

        <h2 id="tipos">Trois façons d’aménager la cabine</h2>
        <div class="tbl">
        <table>
          <thead><tr><th>Type</th><th>Comment c’est</th><th>Pour qui</th></tr></thead>
          <tbody>
            <tr><td>Cabine ou walkaround</td><td>Cabine à l’avant et passavants pour aller à la proue</td><td>Pêche, mouillage et sorties à la journée</td></tr>
            <tr><td>Timonerie (pilothouse)</td><td>Le poste de pilotage est fermé, avec la cabine dessous ou devant</td><td>Ceux qui naviguent aussi hors saison ou avec du vent</td></tr>
            <tr><td>Day cruiser ou sundeck</td><td>Bain de soleil à l’avant et une petite cabine dessous</td><td>Baignade, criques et vie au soleil</td></tr>
          </tbody>
        </table>
        </div>

        <h2 id="eslora">La longueur exacte compte plus qu’on ne le croit</h2>
        <p>Ce qui compte, c’est la longueur de coque indiquée dans les papiers, pas le nom du modèle. Et autour de 6 mètres, il y a deux seuils en Espagne :</p>
        <ul>
          <li><strong>Permis.</strong> Avec la Licencia de Navegación espagnole, vous pouvez piloter des bateaux jusqu’à 6 mètres avec la puissance admise par le constructeur, de jour uniquement et à 2 milles maximum d’un port ou d’un abri. Au-delà de 6 m, il faut le PNB (jusqu’à 8 m et 5 milles) ou un permis supérieur. Voir <a href="{p}/titulaciones/">permis</a>.</li>
          <li><strong>ITB (inspection technique).</strong> En liste 7 (usage privé), pas d’inspections périodiques sous 6 mètres ; à partir de 6 mètres, tous les 5 ans au maximum. Je l’explique dans le <a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">guide de l’ITB</a>.</li>
        </ul>
        <p>Sous 8 mètres, il n’y a pas de taxe d’immatriculation espagnole : à cette longueur, ce n’est pas un sujet. Si vous voulez savoir pourquoi, c’est dans le guide de la <a href="{p}/guias/impuesto-matriculacion-barcos">taxe d’immatriculation (IEDMT)</a>.</p>

        <h2 id="revisar">Que vérifier avant d’en acheter un d’occasion</h2>
        <ul>
          <li><strong>Humidité dans la cabine :</strong> odeur de renfermé, taches au plafond ou sur les coussins, et par où entre l’eau (écoutille, hublots, accastillage de pont).</li>
          <li><strong>Moteur :</strong> année, heures et factures, et démarrage à froid. Presque tous ont un hors-bord ; si c’est un inbord ou un moteur avec embase, l’avis d’un mécanicien est encore plus important.</li>
          <li><strong>Coque et tableau arrière :</strong> sans fissures ni humidité autour du moteur.</li>
          <li><strong>Papiers :</strong> extrait du registre (hoja de asiento) sans charges et longueur de coque claire.</li>
          <li><strong>Remorque, si elle est vendue avec :</strong> papiers, contrôle technique (ITV) au-delà de 750 kg, et vérifiez que votre voiture et votre permis de conduire permettent de la tracter.</li>
        </ul>

        <h2 id="costes">Ce que ça coûte ensuite</h2>
        <p>Une place de port selon la longueur (ou un hangar et une remorque), l’assurance responsabilité civile obligatoire, l’entretien annuel du moteur et l’antifouling s’il reste à l’eau. Je donne les chiffres dans le guide <a href="{p}/guias/cuanto-cuesta-mantener-un-barco-cataluna">combien coûte l’entretien d’un bateau en Catalogne</a>. Et si vous achetez à un particulier, l’ITP (droits de mutation) : 5 % en Catalogne pour un résident (les taux, et le cas des non-résidents, dans le <a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">guide de l’ITP</a>).</p>

        <h2 id="buscas">Vous en cherchez un ?</h2>
        <p>En ce moment, je n’ai aucun bateau de 6 mètres avec cabine en vente. Si vous en cherchez un, <a href="{p}/alertas/">créez une alerte</a> et je vous préviens dès qu’il en arrive un ; ou faites le test <a href="{p}{qb}">quel bateau me faut-il</a> et je vous dis quel type vous convient. Si vous en avez déjà vu un, envoyez-moi les photos et les informations et on le regarde ensemble avant que vous fassiez une offre.</p>
''',
cta_e='Vous en avez déjà vu un ?', cta_t='Envoyez-moi les photos et les informations.', cta_p='On le regarde ensemble avant que vous fassiez une offre.', cta_b='Écrire à Juan sur WhatsApp',
aviso='Guide indicatif. Ce que je dis sur les permis, l’ITB et les impôts se confirme avec les papiers du bateau avant d’acheter.',
card_e='Vous cherchez un 6 mètres ?', card_h='Je vous préviens dès qu’il en arrive un qui vous convient.', card_p='Ou envoyez-moi celui que vous avez vu et on le regarde ensemble avant de faire une offre. Sans engagement.', card_b='Écrire à Juan sur WhatsApp',
toc_t='Dans ce guide', toc=[('camarote', 'Ce que permet la cabine'), ('tipos', 'Trois types de cabine'), ('eslora', 'La longueur exacte'), ('revisar', 'Que vérifier'), ('costes', 'Ce que ça coûte ensuite'), ('buscas', 'Vous en cherchez un ?')],
rel_t='Autres guides', rel=[('/guias/que-mirar-comprar-barco-segunda-mano', 'Que vérifier en achetant un bateau d’occasion'), ('/guias/cuanto-cuesta-mantener-un-barco-cataluna', 'Combien coûte l’entretien d’un bateau'), ('/guias/comprar-barco-espana-matricular-francia', 'Acheter en Espagne et immatriculer en France'), ('/guias/', 'Tous les guides de Plata Marine')],
)

# ====================================================================================
# 2) Impuestos y gastos al comprar un barco
# ====================================================================================
G['impuestos-gastos-comprar-barco'] = {}
B = G['impuestos-gastos-comprar-barco']

B['es'] = dict(
title='Impuestos al comprar un barco en España: qué se paga',
desc='IVA, ITP, impuesto de matriculación y gastos de papeles al comprar un barco nuevo o usado en España, según a quién se lo compres y cuánto mida.',
h1='Impuestos y gastos al comprar un barco en España: qué se paga en cada caso',
crumb='Impuestos y gastos al comprar un barco',
wa_head='Hola Juan, quiero saber qué impuestos le tocan a un barco.',
wa_card='Hola Juan, te mando el anuncio de un barco para saber qué impuestos le tocan y qué papeles pedir.',
eyebrow='Guías · Fiscalidad',
meta='<span>Por Juan Morante</span><span>Actualizado octubre 2026</span><span>5 min de lectura</span>',
lead='El precio del anuncio casi nunca es lo que acabas pagando. Según a quién le compres el barco, si es nuevo o usado y cuánto mide, se suman unos impuestos u otros. Aquí tienes los casos uno por uno, para que hagas las cuentas antes de cerrar el precio.',
body='''
        <h2 id="resumen">Resumen: qué pagas en cada caso</h2>
        <div class="tbl">
        <table>
          <thead><tr><th>Compras…</th><th>Impuesto</th><th>Matriculación (IEDMT)</th></tr></thead>
          <tbody>
            <tr><td>Usado, a un particular</td><td>ITP, según tu comunidad (en Cataluña, 5 %)</td><td>No, ya está matriculado</td></tr>
            <tr><td>Usado, a una empresa o profesional</td><td>IVA (21 %)</td><td>No, ya está matriculado</td></tr>
            <tr><td>Nuevo, de hasta 8 m</td><td>IVA (21 %)</td><td>Exento (modelo 06)</td></tr>
            <tr><td>Nuevo, de más de 8 m</td><td>IVA (21 %)</td><td>12 % en la primera matriculación</td></tr>
            <tr><td>Nuevo, para chárter (lista 6ª)</td><td>IVA, deducible si hay actividad real</td><td>Puede ir exento (modelo 05)</td></tr>
          </tbody>
        </table>
        </div>
{extra}
        <h2 id="itp">Barco usado a un particular: el ITP</h2>
        <p>Lo paga el comprador y lo fija la comunidad donde vive él, no donde está el barco. Va del 1 % de Galicia al 8 % de algunas comunidades para esloras grandes; en Cataluña es el 5 %, con el modelo 620 y un mes de plazo. Se calcula sobre el precio del contrato o sobre las tablas de Hacienda, lo que sea mayor. La tabla completa está en la <a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">guía del ITP por comunidades</a>.</p>

        <h2 id="iva">Barco usado a una empresa o profesional: IVA</h2>
        <p>Si el vendedor es una empresa o un profesional que vende dentro de su actividad, la operación lleva IVA en lugar de ITP. Comprar a través de un bróker no cambia esto: si el dueño es un particular, sigue siendo ITP.</p>

        <h2 id="nuevo">Barco nuevo: IVA y, si pasa de 8 metros, el 12 %</h2>
        <p>Un barco nuevo paga el 21 % de IVA. Si mide más de 8 metros, además paga el impuesto de matriculación (IEDMT), el 12 % en la primera matriculación en España, sobre el barco entero tal como se matricula: casco, motores y equipos montados. Por eso hay tantos barcos de 7,99 m. Hasta 8 metros está exento, con una declaración (modelo 06). Las motos de agua lo pagan siempre. Lo explico con ejemplos en la guía del <a href="{p}/guias/impuesto-matriculacion-barcos">impuesto de matriculación</a>.</p>

        <h2 id="charter">Si es para chárter: lista 6ª</h2>
        <p>Un barco dedicado de verdad al alquiler puede matricularse sin IEDMT (con el reconocimiento previo de Hacienda, modelo 05), y el IVA puede ser deducible si hay actividad real. A cambio tiene que cumplir los requisitos de barco comercial, y si en los primeros años deja el chárter, el impuesto puede volver. Lo cuento en la guía de <a href="{p}/guias/lista-6-y-lista-7">lista 6ª y lista 7ª</a>. Esto lo tiene que ver tu gestor según cómo vayas a darlo de alta.</p>

        <h2 id="papeles">Los papeles</h2>
        <p>Aparte de los impuestos, el cambio de titularidad en Capitanía Marítima (o la matriculación, si es nuevo), que normalmente se hace con una gestoría. Antes de pagar, pide siempre la hoja de asiento actualizada para comprobar que el barco no tiene cargas. La lista completa de documentos está en la <a href="{p}/guias/papeles-vender-barco-cambio-titularidad">guía de papeles</a>.</p>

        <h2 id="despues">Y lo que llega después</h2>
        <ul>
          <li>Seguro de responsabilidad civil, obligatorio desde el primer día.</li>
          <li>Amarre o, si es pequeño, nave y remolque.</li>
          <li><a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">ITB</a> cuando le toque.</li>
          <li>Mantenimiento: motor, antifouling, equipo de seguridad.</li>
        </ul>
        <p>Todo esto, con números, en la guía de <a href="{p}/guias/cuanto-cuesta-mantener-un-barco-cataluna">cuánto cuesta mantener un barco en Cataluña</a>.</p>

        <h2 id="cuentas">¿Quieres hacer las cuentas de un barco concreto?</h2>
        <p>Mándame el anuncio y te digo qué impuestos le tocan y qué papeles pedir antes de reservar. Si es uno de los <a href="{p}/barcos/">barcos que tengo en venta</a>, te lo detallo por escrito.</p>
''',
extra='',
cta_e='¿Tienes un barco a la vista?', cta_t='Mándame el anuncio.', cta_p='Te digo qué impuestos le tocan y qué papeles pedir antes de reservar.', cta_b='Mandar el anuncio por WhatsApp',
aviso='Guía orientativa con la normativa revisada en octubre de 2026. Cada caso se confirma con la documentación del barco y con tu gestoría antes de comprar.',
card_e='¿Haces las cuentas de un barco?', card_h='Mándame el anuncio y te digo qué impuestos le tocan.', card_p='Y qué papeles pedir antes de reservar. Sin compromiso.', card_b='Hablar con Juan por WhatsApp',
toc_t='En esta guía', toc=[('resumen', 'Resumen por casos'), ('itp', 'Usado a un particular: ITP'), ('iva', 'Usado a una empresa: IVA'), ('nuevo', 'Barco nuevo'), ('charter', 'Para chárter: lista 6ª'), ('papeles', 'Los papeles'), ('despues', 'Lo que llega después'), ('cuentas', 'Tu caso concreto')],
rel_t='Otras guías', rel=[('/guias/itp-comprar-barco-usado-por-comunidad', 'El ITP por comunidades'), ('/guias/impuesto-matriculacion-barcos', 'Impuesto de matriculación'), ('/guias/comprar-barco-espana-no-residente', 'Comprar un barco si no eres residente'), ('/guias/barcos-6-metros-con-camarote/', 'Barcos de 6 metros con camarote'), ('/guias/', 'Todas las guías de Plata Marine')],
)

B['ca'] = dict(
title='Impostos en comprar un vaixell a Espanya: què es paga',
desc='IVA, ITP, impost de matriculació i despeses de papers en comprar un vaixell nou o de segona mà a Espanya, segons a qui el compris i quant faci.',
h1='Impostos i despeses en comprar un vaixell a Espanya: què es paga en cada cas',
crumb='Impostos i despeses en comprar un vaixell',
wa_head='Hola Juan, vull saber quins impostos li toquen a un vaixell.',
wa_card='Hola Juan, t’envio l’anunci d’un vaixell per saber quins impostos li toquen i quins papers demanar.',
eyebrow='Guies · Fiscalitat',
meta='<span>Per Juan Morante</span><span>Actualitzat octubre 2026</span><span>5 min de lectura</span>',
lead='El preu de l’anunci gairebé mai és el que acabes pagant. Segons a qui li compris el vaixell, si és nou o de segona mà i quant fa, se sumen uns impostos o uns altres. Aquí tens els casos un per un, perquè facis els números abans de tancar el preu.',
body='''
        <h2 id="resumen">Resum: què pagues en cada cas</h2>
        <div class="tbl">
        <table>
          <thead><tr><th>Compres…</th><th>Impost</th><th>Matriculació (IEDMT)</th></tr></thead>
          <tbody>
            <tr><td>De segona mà, a un particular</td><td>ITP, segons la teva comunitat (a Catalunya, 5 %)</td><td>No, ja està matriculat</td></tr>
            <tr><td>De segona mà, a una empresa o professional</td><td>IVA (21 %)</td><td>No, ja està matriculat</td></tr>
            <tr><td>Nou, de fins a 8 m</td><td>IVA (21 %)</td><td>Exempt (model 06)</td></tr>
            <tr><td>Nou, de més de 8 m</td><td>IVA (21 %)</td><td>12 % en la primera matriculació</td></tr>
            <tr><td>Nou, per a xàrter (llista 6a)</td><td>IVA, deduïble si hi ha activitat real</td><td>Pot anar exempt (model 05)</td></tr>
          </tbody>
        </table>
        </div>
{extra}
        <h2 id="itp">Vaixell de segona mà a un particular: l’ITP</h2>
        <p>El paga el comprador i el fixa la comunitat on viu ell, no on és el vaixell. Va de l’1 % de Galícia al 8 % d’algunes comunitats per a esloras grans; a Catalunya és el 5 %, amb el model 620 i un mes de termini. Es calcula sobre el preu del contracte o sobre les taules d’Hisenda, el que sigui més alt. La taula completa és a la <a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">guia de l’ITP per comunitats</a>.</p>

        <h2 id="iva">Vaixell de segona mà a una empresa o professional: IVA</h2>
        <p>Si el venedor és una empresa o un professional que ven dins de la seva activitat, l’operació porta IVA en lloc d’ITP. Comprar a través d’un bròquer no ho canvia: si el propietari és un particular, continua sent ITP.</p>

        <h2 id="nuevo">Vaixell nou: IVA i, si passa de 8 metres, el 12 %</h2>
        <p>Un vaixell nou paga el 21 % d’IVA. Si fa més de 8 metres, a més paga l’impost de matriculació (IEDMT), el 12 % en la primera matriculació a Espanya, sobre el vaixell sencer tal com es matricula: casc, motors i equips muntats. Per això hi ha tants vaixells de 7,99 m. Fins a 8 metres està exempt, amb una declaració (model 06). Les motos d’aigua el paguen sempre. Ho explico amb exemples a la guia de l’<a href="{p}/guias/impuesto-matriculacion-barcos">impost de matriculació</a>.</p>

        <h2 id="charter">Si és per a xàrter: llista 6a</h2>
        <p>Un vaixell dedicat de debò al lloguer es pot matricular sense IEDMT (amb el reconeixement previ d’Hisenda, model 05), i l’IVA pot ser deduïble si hi ha activitat real. A canvi ha de complir els requisits de vaixell comercial, i si en els primers anys deixa el xàrter, l’impost pot tornar. Ho explico a la guia de la <a href="{p}/guias/lista-6-y-lista-7">llista 6a i la llista 7a</a>. Això ho ha de mirar el teu gestor segons com el vulguis donar d’alta.</p>

        <h2 id="papeles">Els papers</h2>
        <p>A banda dels impostos, el canvi de titularitat a Capitania Marítima (o la matriculació, si és nou), que normalment es fa amb una gestoria. Abans de pagar, demana sempre el full d’assentament actualitzat per comprovar que el vaixell no té càrregues. La llista completa de documents és a la <a href="{p}/guias/papeles-vender-barco-cambio-titularidad">guia de papers</a>.</p>

        <h2 id="despues">I el que arriba després</h2>
        <ul>
          <li>Assegurança de responsabilitat civil, obligatòria des del primer dia.</li>
          <li>Amarratge o, si és petit, nau i remolc.</li>
          <li><a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">ITB</a> quan li toqui.</li>
          <li>Manteniment: motor, antifouling, equip de seguretat.</li>
        </ul>
        <p>Tot això, amb números, a la guia de <a href="{p}/guias/cuanto-cuesta-mantener-un-barco-cataluna">quant costa mantenir un vaixell a Catalunya</a>.</p>

        <h2 id="cuentas">Vols fer els números d’un vaixell concret?</h2>
        <p>Envia’m l’anunci i et dic quins impostos li toquen i quins papers demanar abans de reservar. Si és un dels <a href="{p}/barcos/">vaixells que tinc en venda</a>, t’ho detallo per escrit.</p>
''',
extra='',
cta_e='Tens un vaixell a la vista?', cta_t='Envia’m l’anunci.', cta_p='Et dic quins impostos li toquen i quins papers demanar abans de reservar.', cta_b='Enviar l’anunci per WhatsApp',
aviso='Guia orientativa amb la normativa revisada l’octubre de 2026. Cada cas es confirma amb la documentació del vaixell i amb la teva gestoria abans de comprar.',
card_e='Fas els números d’un vaixell?', card_h='Envia’m l’anunci i et dic quins impostos li toquen.', card_p='I quins papers demanar abans de reservar. Sense compromís.', card_b='Parlar amb Juan per WhatsApp',
toc_t='En aquesta guia', toc=[('resumen', 'Resum per casos'), ('itp', 'Segona mà a un particular: ITP'), ('iva', 'Segona mà a una empresa: IVA'), ('nuevo', 'Vaixell nou'), ('charter', 'Per a xàrter: llista 6a'), ('papeles', 'Els papers'), ('despues', 'El que arriba després'), ('cuentas', 'El teu cas concret')],
rel_t='Altres guies', rel=[('/guias/itp-comprar-barco-usado-por-comunidad', 'L’ITP per comunitats'), ('/guias/impuesto-matriculacion-barcos', 'Impost de matriculació'), ('/guias/comprar-barco-espana-no-residente', 'Comprar un vaixell si no ets resident'), ('/guias/barcos-6-metros-con-camarote/', 'Vaixells de 6 metres amb cabina'), ('/guias/', 'Totes les guies de Plata Marine')],
)

B['en'] = dict(
title='Taxes when buying a boat in Spain: what you pay',
desc='VAT, ITP, registration tax and paperwork costs when you buy a new or used boat in Spain, depending on who you buy it from and how long it is.',
h1='Taxes and costs when buying a boat in Spain: what you pay in each case',
crumb='Taxes and costs when buying a boat',
wa_head='Hi Juan, I’d like to know which taxes apply to a boat.',
wa_card='Hi Juan, here’s the listing for a boat. I’d like to know which taxes apply and which papers to ask for.',
eyebrow='Guides · Tax',
meta='<span>By Juan Morante</span><span>Updated October 2026</span><span>5 min read</span>',
lead='The listed price is hardly ever what you end up paying. Depending on who you buy the boat from, whether it’s new or used and how long it is, different taxes are added. Here are the cases one by one, so you can do the sums before you agree a price.',
body='''
        <h2 id="resumen">Summary: what you pay in each case</h2>
        <div class="tbl">
        <table>
          <thead><tr><th>You buy…</th><th>Tax</th><th>Registration tax (IEDMT)</th></tr></thead>
          <tbody>
            <tr><td>Used, from a private seller</td><td>ITP, depending on your region (5% in Catalonia)</td><td>No, it’s already registered</td></tr>
            <tr><td>Used, from a company or professional</td><td>VAT (21%)</td><td>No, it’s already registered</td></tr>
            <tr><td>New, up to 8 m</td><td>VAT (21%)</td><td>Exempt (form 06)</td></tr>
            <tr><td>New, over 8 m</td><td>VAT (21%)</td><td>12% on first registration</td></tr>
            <tr><td>New, for charter (list 6)</td><td>VAT, deductible if there’s genuine business activity</td><td>Can be exempt (form 05)</td></tr>
          </tbody>
        </table>
        </div>
{extra}
        <h2 id="itp">Used boat from a private seller: ITP</h2>
        <p>ITP (transfer tax) is paid by the buyer, and the rate is set by the region where the buyer lives, not where the boat is. It ranges from 1% in Galicia to 8% in some regions for larger boats; in Catalonia it’s 5%, filed on form 620 within one month. It’s calculated on the contract price or on the tax authority’s valuation tables, whichever is higher. The full table is in the <a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">ITP guide by region</a>. If you don’t live in Spain, the <a href="{p}/guias/comprar-barco-espana-no-residente">guide for non-residents</a> covers your case.</p>

        <h2 id="iva">Used boat from a company or professional: VAT</h2>
        <p>If the seller is a company or a professional selling as part of their business, the sale carries VAT instead of ITP. Buying through a broker doesn’t change this: if the owner is a private individual, it’s still ITP.</p>

        <h2 id="nuevo">New boat: VAT and, over 8 metres, the 12%</h2>
        <p>A new boat pays 21% VAT. If it’s over 8 metres, it also pays the registration tax (IEDMT): 12% on its first registration in Spain, on the whole boat as registered, meaning hull, engines and fitted equipment. That’s why there are so many 7.99 m boats. Up to 8 metres it’s exempt, with a declaration (form 06). Jet skis always pay it. I explain it with examples in the guide to the <a href="{p}/guias/impuesto-matriculacion-barcos">registration tax</a>.</p>

        <h2 id="charter">If it’s for charter: list 6</h2>
        <p>A boat genuinely used for charter can be registered without IEDMT (with prior recognition from the tax authority, form 05), and the VAT can be deductible if there’s genuine business activity. In return it has to meet the requirements for a commercial boat, and if it stops chartering in the first few years, the tax can come back. I explain it in the guide to <a href="{p}/guias/lista-6-y-lista-7">list 6 and list 7</a>. Your gestor (tax adviser) needs to look at this based on how you plan to register the activity.</p>

        <h2 id="papeles">The paperwork</h2>
        <p>On top of the taxes, there’s the change of ownership at the Harbour Master’s office (Capitanía Marítima), or the registration if the boat is new, which is usually done through a gestoría. Before you pay, always ask for the up-to-date registry sheet (hoja de asiento) to check the boat has no charges against it. The full list of documents is in the <a href="{p}/guias/papeles-vender-barco-cambio-titularidad">paperwork guide</a>.</p>

        <h2 id="despues">And what comes afterwards</h2>
        <ul>
          <li>Third-party insurance, compulsory from day one.</li>
          <li>A berth or, for a small boat, storage and a trailer.</li>
          <li>The <a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">ITB</a> inspection when it’s due.</li>
          <li>Maintenance: engine, antifouling, safety equipment.</li>
        </ul>
        <p>All of this, with numbers, in the guide to <a href="{p}/guias/cuanto-cuesta-mantener-un-barco-cataluna">what it costs to keep a boat in Catalonia</a>.</p>

        <h2 id="cuentas">Want to do the sums on a specific boat?</h2>
        <p>Send me the listing and I’ll tell you which taxes apply and which papers to ask for before you reserve it. If it’s one of the <a href="{p}/barcos/">boats I have for sale</a>, I’ll set it out in writing.</p>
''',
extra='',
cta_e='Got a boat in mind?', cta_t='Send me the listing.', cta_p='I’ll tell you which taxes apply and which papers to ask for before you reserve.', cta_b='Send the listing on WhatsApp',
aviso='This guide is for guidance only and reflects the rules as reviewed in October 2026. Each case is confirmed against the boat’s paperwork and with your gestoría before you buy.',
card_e='Doing the sums on a boat?', card_h='Send me the listing and I’ll tell you which taxes apply.', card_p='And which papers to ask for before you reserve. No obligation.', card_b='Talk to Juan on WhatsApp',
toc_t='In this guide', toc=[('resumen', 'Summary by case'), ('itp', 'Used, private seller: ITP'), ('iva', 'Used, company seller: VAT'), ('nuevo', 'New boat'), ('charter', 'For charter: list 6'), ('papeles', 'The paperwork'), ('despues', 'What comes afterwards'), ('cuentas', 'Your specific boat')],
rel_t='Other guides', rel=[('/guias/itp-comprar-barco-usado-por-comunidad', 'ITP by region'), ('/guias/impuesto-matriculacion-barcos', 'Registration tax (IEDMT)'), ('/guias/comprar-barco-espana-no-residente', 'Buying a boat in Spain as a non-resident'), ('/guias/barcos-6-metros-con-camarote/', '6-metre boats with a cabin'), ('/guias/', 'All Plata Marine guides')],
)

B['fr'] = dict(
title='Bateau d’occasion en Espagne : taxes et frais à prévoir',
desc='ITP, TVA, taxe d’immatriculation et papiers : ce que vous payez en achetant un bateau en Espagne, selon le vendeur et la longueur du bateau.',
h1='Acheter un bateau d’occasion en Espagne : taxes et frais à prévoir',
crumb='Taxes et frais pour acheter un bateau en Espagne',
wa_head='Bonjour Juan, j’aimerais savoir quelles taxes s’appliquent à un bateau en Espagne.',
wa_card='Bonjour Juan, je vous envoie l’annonce d’un bateau pour savoir quelles taxes s’appliquent et quels papiers demander.',
eyebrow='Guides · Fiscalité',
meta='<span>Par Juan Morante</span><span>Mis à jour en octobre 2026</span><span>5 min de lecture</span>',
lead='Le prix de l’annonce n’est presque jamais ce que vous payez au final. Selon à qui vous achetez le bateau, s’il est neuf ou d’occasion et sa longueur, ce ne sont pas les mêmes impôts qui s’ajoutent. Voici les cas un par un, pour faire vos calculs avant de vous mettre d’accord sur le prix.',
body='''
        <h2 id="resumen">En résumé : ce que vous payez dans chaque cas</h2>
        <div class="tbl">
        <table>
          <thead><tr><th>Vous achetez…</th><th>Impôt</th><th>Taxe d’immatriculation (IEDMT)</th></tr></thead>
          <tbody>
            <tr><td>D’occasion, à un particulier</td><td>ITP, selon votre communauté autonome (en Catalogne, 5 %)</td><td>Non, il est déjà immatriculé</td></tr>
            <tr><td>D’occasion, à une entreprise ou un professionnel</td><td>TVA espagnole (21 %)</td><td>Non, il est déjà immatriculé</td></tr>
            <tr><td>Neuf, jusqu’à 8 m</td><td>TVA espagnole (21 %)</td><td>Exonéré (modelo 06)</td></tr>
            <tr><td>Neuf, plus de 8 m</td><td>TVA espagnole (21 %)</td><td>12 % à la première immatriculation</td></tr>
            <tr><td>Neuf, pour la location (liste 6)</td><td>TVA, déductible s’il y a une vraie activité</td><td>Peut être exonéré (modelo 05)</td></tr>
          </tbody>
        </table>
        </div>
{extra}
        <h2 id="itp">Bateau d’occasion acheté à un particulier : l’ITP</h2>
        <p>L’ITP (droits de mutation) est payé par l’acheteur, et son taux dépend de la communauté autonome où il réside, pas de l’endroit où se trouve le bateau. Il va de 1 % en Galice à 8 % dans certaines communautés pour les grandes longueurs ; en Catalogne, c’est 5 %, avec le modelo 620 et un mois de délai. Il se calcule sur le prix du contrat ou sur les barèmes de l’administration fiscale, selon ce qui est le plus élevé. Le tableau complet est dans le <a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">guide de l’ITP par communauté</a>.</p>

        <h2 id="iva">Bateau d’occasion acheté à une entreprise ou un professionnel : la TVA</h2>
        <p>Si le vendeur est une entreprise ou un professionnel qui vend dans le cadre de son activité, la vente est soumise à la TVA au lieu de l’ITP. Passer par un courtier n’y change rien : si le propriétaire est un particulier, c’est toujours l’ITP.</p>

        <h2 id="nuevo">Bateau neuf : TVA et, au-delà de 8 mètres, les 12 %</h2>
        <p>Un bateau neuf paie 21 % de TVA espagnole. S’il mesure plus de 8 mètres, il paie aussi la taxe d’immatriculation (IEDMT) : 12 % à la première immatriculation en Espagne, sur le bateau complet tel qu’il est immatriculé, c’est-à-dire coque, moteurs et équipements montés. C’est pour cela qu’il y a tant de bateaux de 7,99 m. Jusqu’à 8 mètres, il en est exonéré, avec une déclaration (modelo 06). Les scooters des mers la paient toujours. Je l’explique avec des exemples dans le guide de la <a href="{p}/guias/impuesto-matriculacion-barcos">taxe d’immatriculation</a>.</p>

        <h2 id="charter">Si c’est pour la location : la liste 6</h2>
        <p>Un bateau vraiment consacré à la location peut être immatriculé sans IEDMT (avec la reconnaissance préalable de l’administration fiscale, modelo 05), et la TVA peut être déductible s’il y a une vraie activité. En contrepartie, il doit remplir les conditions d’un bateau commercial, et s’il arrête la location dans les premières années, la taxe peut redevenir due. Je l’explique dans le guide de la <a href="{p}/guias/lista-6-y-lista-7">liste 6 et liste 7</a>. C’est à votre gestor (conseiller) de le voir selon la façon dont vous déclarez l’activité.</p>

        <h2 id="papeles">Les papiers</h2>
        <p>En plus des impôts, il y a le changement de propriétaire à la Capitanía Marítima (la capitainerie espagnole), ou l’immatriculation si le bateau est neuf, qui se fait normalement avec une gestoría. Avant de payer, demandez toujours l’extrait du registre à jour (hoja de asiento) pour vérifier que le bateau n’a pas de charges. La liste complète des documents est dans le <a href="{p}/guias/papeles-vender-barco-cambio-titularidad">guide des papiers</a>.</p>

        <h2 id="despues">Et ce qui vient ensuite</h2>
        <ul>
          <li>L’assurance responsabilité civile, obligatoire dès le premier jour.</li>
          <li>Une place de port ou, pour un petit bateau, un hangar et une remorque.</li>
          <li>L’<a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">ITB</a> quand elle est due.</li>
          <li>L’entretien : moteur, antifouling, équipement de sécurité.</li>
        </ul>
        <p>Tout cela, avec des chiffres, dans le guide <a href="{p}/guias/cuanto-cuesta-mantener-un-barco-cataluna">combien coûte l’entretien d’un bateau en Catalogne</a>.</p>

        <h2 id="cuentas">Vous voulez faire les calculs pour un bateau précis ?</h2>
        <p>Envoyez-moi l’annonce et je vous dis quelles taxes s’appliquent et quels papiers demander avant de réserver. Si c’est l’un des <a href="{p}/barcos/">bateaux que j’ai en vente</a>, je vous le détaille par écrit.</p>
''',
extra='''
        <div class="next-step" style="background:#F3F5F6;border-left:3px solid #0E3042;padding:16px 18px;border-radius:0 6px 6px 0;margin:22px 0">
          <p style="margin:0 0 8px"><strong>Vous vivez en France ?</strong> Ce tableau correspond aux impôts espagnols pour quelqu’un qui réside en Espagne. Si vous n’êtes pas résident, l’ITP ne dépend pas d’une communauté autonome : il se déclare auprès de l’administration fiscale de l’État espagnol. Et si vous comptez ramener le bateau en France et l’y immatriculer, il faut le radier du registre espagnol et ce sont ensuite les règles françaises qui s’appliquent ; pour un bateau neuf ou presque neuf, la TVA peut même se payer en France et non en Espagne.</p>
          <p style="margin:0">Je l’explique pas à pas dans le guide <a href="{p}/guias/comprar-barco-espana-matricular-francia"><strong>acheter un bateau en Espagne et l’immatriculer en France</strong></a>.</p>
        </div>
''',
cta_e='Vous avez un bateau en vue ?', cta_t='Envoyez-moi l’annonce.', cta_p='Je vous dis quelles taxes s’appliquent et quels papiers demander avant de réserver.', cta_b='Envoyer l’annonce sur WhatsApp',
aviso='Guide indicatif, réglementation revue en octobre 2026. Chaque cas se confirme avec les papiers du bateau et avec votre gestoría avant d’acheter.',
card_e='Vous faites vos calculs ?', card_h='Envoyez-moi l’annonce et je vous dis quelles taxes s’appliquent.', card_p='Et quels papiers demander avant de réserver. Sans engagement.', card_b='Écrire à Juan sur WhatsApp',
toc_t='Dans ce guide', toc=[('resumen', 'En résumé'), ('itp', 'Occasion, particulier : ITP'), ('iva', 'Occasion, professionnel : TVA'), ('nuevo', 'Bateau neuf'), ('charter', 'Location : liste 6'), ('papeles', 'Les papiers'), ('despues', 'Ce qui vient ensuite'), ('cuentas', 'Votre bateau')],
rel_t='Autres guides', rel=[('/guias/comprar-barco-espana-matricular-francia', 'Acheter en Espagne et immatriculer en France'), ('/guias/comprar-barco-espana-no-residente', 'Acheter un bateau en Espagne sans y résider'), ('/guias/itp-comprar-barco-usado-por-comunidad', 'L’ITP par communauté'), ('/guias/impuesto-matriculacion-barcos', 'Taxe d’immatriculation (IEDMT)'), ('/guias/', 'Tous les guides de Plata Marine')],
)

ASIDE = {'es': 'Contacto y navegación', 'ca': 'Contacte i navegació', 'en': 'Contact and navigation', 'fr': 'Contact et navigation'}


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')


def pre(lang):
    return '' if lang == 'es' else lang + '/'


def build(slug, lang):
    t = G[slug][lang]; p = '' if lang == 'es' else '/' + lang
    src = open(f"{pre(lang)}guias/{SRC}/index.html", encoding='utf-8').read()
    head, rest = src.split('<main class="art">', 1)
    foot = rest.split('</main>', 1)[1]
    url = f"{BASE}{p}/guias/{slug}/"
    og = BASE + OG[lang]
    head = head.replace(SRC, slug)
    head = re.sub(r'<title>.*?</title>', f"<title>{t['title']}</title>", head, count=1)
    for k, v in (('name="description"', t['desc']), ('property="og:title"', t['title']), ('property="og:description"', t['desc']), ('property="og:image"', og)):
        head = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + esc(v), head, count=1)
    art = {"@context": "https://schema.org", "@type": "Article", "headline": t['h1'],
           "author": {"@type": "Person", "name": "Juan Morante"}, "publisher": {"@type": "Organization", "name": "Plata Marine"},
           "datePublished": DATE, "dateModified": DATE, "inLanguage": lang, "mainEntityOfPage": url, "image": og}
    head = re.sub(r'(<script type="application/ld\+json">\s*)\{"@context": "https://schema.org", "@type": "Article".*?\}\s*(</script>)',
                  lambda m: m.group(1) + json.dumps(art, ensure_ascii=False) + "\n" + m.group(2), head, count=1, flags=re.S)
    head = re.sub(r'("position": 3, "name": ")[^"]*', lambda m: m.group(1) + t['crumb'], head, count=1)
    head = re.sub(r'(<a class="btn btn-wa" href="https://wa.me/34633742973\?text=)[^"]*(" target="_blank" rel="noopener">[^<]*</a><div class="langsw")',
                  lambda m: m.group(1) + quote(t['wa_head'], safe='') + m.group(2), head, count=1)
    toc = ''.join(f'\n          <li><a href="#{a}">{b}</a></li>' for a, b in t['toc'])
    rel = ''.join(f'\n        <a href="{p}{h}">{x}</a>' for h, x in t['rel'])
    body = t['body'].replace('{extra}', t.get('extra', '')).replace('{p}', p).replace('{qb}', QB)
    cta = (f'''
        <div class="next-step" data-next="whatsapp" style="background:rgba(181,138,44,.08);border-left:3px solid #B58A2C;padding:16px 18px;border-radius:0 6px 6px 0;margin:26px 0"><p class="eyebrow" style="margin:0 0 8px">{t['cta_e']}</p><p style="margin:0 0 12px"><strong>{t['cta_t']}</strong> {t['cta_p']}</p><a class="next-btn" style="display:inline-block;background:#0E3042;color:#fff;padding:10px 18px;border-radius:6px;text-decoration:none;font-family:var(--display,inherit);font-weight:600;font-size:15px" href="{WA}{quote(t['wa_card'], safe='')}" target="_blank" rel="noopener">{t['cta_b']}</a></div>''')
    main = f'''<main class="art">
  <div class="wrap">
    <article>
      <header>
        <p class="eyebrow">{t['eyebrow']}</p>
        <h1>{t['h1']}</h1>
        <div class="meta">{t['meta']}</div>
        <p class="lead">{t['lead']}</p>
      </header>

      <div class="prose">{body}{cta}

        <p class="aviso" style="font-size:.82em;opacity:.85;font-style:italic">{t['aviso']}</p>
      </div>
    </article>

    <aside class="aside" aria-label="{ASIDE[lang]}">
      <div class="card">
        <p class="eyebrow">{t['card_e']}</p>
        <h3>{t['card_h']}</h3>
        <p>{t['card_p']}</p>
        <a class="btn btn-wa" href="{WA}{quote(t['wa_card'], safe='')}" target="_blank" rel="noopener">{t['card_b']}</a>
      </div>
      <nav class="toc" aria-label="{t['toc_t']}">
        <p class="eyebrow">{t['toc_t']}</p>
        <ol>{toc}
        </ol>
      </nav>
      <div class="rel">
        <p class="eyebrow">{t['rel_t']}</p>{rel}
      </div>
    </aside>
  </div>
</main>'''
    out = f"{pre(lang)}guias/{slug}/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(head + main + foot)
    return out


if __name__ == '__main__':
    for slug in G:
        for l in ('es', 'ca', 'en', 'fr'):
            print(build(slug, l))
