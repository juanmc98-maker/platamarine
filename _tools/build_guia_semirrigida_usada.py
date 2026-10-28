# -*- coding: utf-8 -*-
"""Guía: comprar una semirrígida de segunda mano (ES/CA/EN/FR).
Toma cabecera y pie de la guía de semirrígidas deportivas de cada idioma, la lista de barcos
(pm-list, se repinta sola desde inventario.js con portal.js) y su CSS de la página de compra de
semirrígidas, y escribe /<lang>/guias/comprar-semirrigida-segunda-mano/index.html.
Uso: python3 _tools/build_guia_semirrigida_usada.py  (desde la raíz del repo)"""
import re, json, os
from urllib.parse import quote

SLUG = 'comprar-semirrigida-segunda-mano'
SRC = 'semirrigidas-deportivas-lujo'
LIST = 'comprar/semirrigidas-neumaticas-segunda-mano.html'
BASE = 'https://www.platamarine.com'
OG = BASE + '/tiger-marine-650-1.jpg'
DATE = '2026-10-28'
WA = 'https://wa.me/34633742973?text='

T = {}

# ---------------------------------------------------------------- ES
T['es'] = dict(
title='Semirrígida de segunda mano: qué revisar antes de comprar',
desc='Qué revisar en una semirrígida de segunda mano: flotadores, motor y horas, casco, papeles y remolque. Y las semirrígidas que tengo ahora en venta.',
h1='Comprar una semirrígida de segunda mano: qué revisar antes de pagar',
crumb='Comprar una semirrígida de segunda mano',
wa_head='Hola Juan, estoy mirando semirrígidas de segunda mano.',
wa_card='Hola Juan, he visto una semirrígida de segunda mano y quiero que la revises conmigo.',
wa_cta='Hola Juan, me interesa una de tus semirrígidas de segunda mano y quiero preguntarte por una visita.',
eyebrow='Guías · Compra',
meta='<span>Por Juan Morante</span><span>Actualizado octubre 2026</span><span>8 min de lectura</span>',
lead='En una semirrígida usada, el año del casco dice poco. Lo que de verdad marca el precio, y los disgustos, son los flotadores, el motor y los papeles. Esto es lo que reviso antes de recomendar una, con los datos de las que tengo ahora en venta.',
body='''
        <h2 id="precio">Qué influye en el precio de una semirrígida usada</h2>
        <p>Más que el año del casco, pesan el motor (su año, sus horas y cómo se ha mantenido), el estado de los flotadores, el equipo y si se vende con remolque. Un ejemplo de mi cartera: la <a href="{p}/barcos/sacs-535">Sacs 535</a> es de 2002, pero su propietario le ha puesto flotadores y tapicería nuevos, ha pintado el casco y ha cambiado la instalación eléctrica y las baterías. Por eso su precio no se parece al de otra semirrígida del mismo año con todo original.</p>
        <p>Estas son las semirrígidas que tengo ahora en venta. Los precios son los anunciados, no una media de mercado:</p>
        {list}
        <p>Si buscas otra eslora u otro motor, puedes <a href="{p}/alertas/">crear una alerta</a> y te aviso cuando entre una que encaje.</p>

        <h2 id="flotadores">Los flotadores: lo primero que miro</h2>
        <p>Son la parte que más sufre (el sol, los roces con el pantalán, el remolque) y, después del motor, la más cara de reparar o cambiar.</p>
        <ul>
          <li><strong>Material.</strong> Suelen ser de tejido con PVC o con CSM (lo que todo el mundo llama Hypalon). El Hypalon suele aguantar mejor el sol, pero también cuentan la calidad del tejido, cómo está hecho y cómo se ha cuidado. Pregunta cuál lleva y de qué año son: los de la Sacs, por ejemplo, son de PVC y nuevos.</li>
          <li><strong>Presión.</strong> Pide que estén hinchados desde el día anterior y compruébalo, mejor con manómetro, compartimento a compartimento. Ojo: con frío la presión baja sola, así que un flotador algo más blando no quiere decir por sí solo que pierda. Si pierde de verdad, hay que encontrar dónde: válvulas, costuras o tejido.</li>
          <li><strong>Costuras y pegados.</strong> Mira la unión del flotador con el casco, los conos de popa y las zonas de roce. Parches hay muchos y no siempre son un problema; un pegado que se abre, sí.</li>
          <li><strong>Aspecto.</strong> Descolorido, pegajoso al tacto o con grietas finas: son señales de envejecimiento que piden mirarlo con más calma.</li>
          <li><strong>Válvulas.</strong> Que estén todas y cierren bien; cada compartimento lleva la suya.</li>
        </ul>
        <p>Si son los originales y tienen muchos años, revisa con especial cuidado costuras, pegados y tejido. Si están muy tocados, pide presupuesto a un taller para repararlos o cambiarlos antes de hacer la oferta: es un gasto importante.</p>

        <h2 id="motor">El motor y las horas</h2>
        <p>Casi todas las semirrígidas de segunda mano llevan fueraborda. Lo que miro:</p>
        <ul>
          <li><strong>El año del motor no es el del casco.</strong> En la Sacs, casco de 2002 y motor de 2007; en la <a href="{p}/barcos/tiger-marine-650">Tiger Marine 650</a>, casco de 2015 y motor de 2012. Las horas se leen con el año del motor.</li>
          <li><strong>Que las horas cuadren con la historia del barco.</strong> El propietario de la Tiger Marine indica unas 110 horas y que solo la tiene en el agua en agosto; el resto del año está hibernada en nave. Es un uso que cuadra con pocas horas, y aun así conviene comprobarlas, cuando se pueda, con el diagnóstico del motor y con las facturas. Pocas horas es bueno si el motor se ha cuidado; un motor que ha pasado años parado y sin mantenimiento también da problemas.</li>
          <li><strong>Facturas.</strong> Aceite, filtros, impulsor de la bomba de agua, ánodos y aceite de la cola. Si no hay papeles, pregunta quién hacía el mantenimiento.</li>
          <li><strong>Arranque en frío.</strong> Pide verlo arrancar sin haberlo encendido antes ese día. Mira que salga agua por el testigo de refrigeración, que no salte ninguna alarma y que la temperatura se mantenga normal: el chorro del testigo solo no garantiza que todo el circuito refrigere bien.</li>
          <li><strong>Cola, hélice y mandos.</strong> Que el aceite de la cola no salga con agua, que la hélice no tenga golpes y que el trim y la dirección vayan finos.</li>
          <li><strong>Un mecánico, si hay dudas.</strong> Que lo revise uno de tu confianza antes de pagar. Una prueba de compresión ayuda a ver problemas internos (sobre todo si un cilindro da muy distinto a los demás), pero no sustituye una revisión completa.</li>
        </ul>

        <h2 id="casco">Casco, consola y espejo de popa</h2>
        <ul>
          <li><strong>Quilla y fondo:</strong> golpes por varadas en la playa o por el remolque.</li>
          <li><strong>Espejo de popa:</strong> que esté firme alrededor de los tornillos del motor y sin grietas, humedad ni señales de movimiento. Un espejo puede estar tocado por dentro sin que se mueva a simple vista, y repararlo es serio.</li>
          <li><strong>Reparaciones:</strong> si el casco se ha pintado o reparado, pregunta qué se hizo y quién lo hizo.</li>
          <li><strong>Consola y bancos:</strong> bien anclados y sin grietas en la fibra.</li>
          <li><strong>Electricidad y equipos:</strong> luces de navegación, bomba de achique, VHF y lo que lleve. Que todo funcione con el motor en marcha.</li>
        </ul>

        <h2 id="papeles">Papeles, titulación e impuestos</h2>
        <ul>
          <li><strong>Titular y cargas.</strong> Si el barco tiene bandera española, pide la hoja de asiento actualizada: ahí constan los datos del registro y las anotaciones que tenga. Si tiene bandera extranjera, como la Tiger Marine (registro polaco), hay que revisar la documentación equivalente de ese país y de quién ha sido. Qué implica una bandera polaca lo cuento en <a href="{p}/guias/bandera-polaca-abanderar-barco-otro-pais">esta guía</a>.</li>
          <li><strong>Titulación.</strong> Cuenta la eslora de casco que figura en la documentación, no el nombre del modelo. Con la Licencia de Navegación puedes gobernar barcos de hasta 6 metros con la potencia de motor adecuada según el fabricante, solo de día y sin alejarte más de 2 millas de un puerto, marina o lugar de abrigo. El PNB permite barcos de motor de hasta 8 metros, a no más de 5 millas. Por encima, una titulación superior. Por eso la Sacs (5,35 m) va con Licencia de Navegación y la Tiger Marine (unos 6,50 m) con el PNB. Lo tienes en <a href="{p}/titulaciones/">titulaciones</a>.</li>
          <li><strong>ITB.</strong> En un barco español de lista 7ª (uso privado), por debajo de 6 metros no hay reconocimientos periódicos; de 6 a 24 metros, como máximo cada 5 años. En lista 6ª (alquiler), siempre. Pide el certificado de navegabilidad y los reconocimientos que le toquen; en un barco con bandera extranjera, lo que exija su país. Lo explico en la <a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">guía de la ITB</a>.</li>
          <li><strong>Impuestos.</strong> Si compras a un particular, normalmente pagas el ITP, y el porcentaje depende de la comunidad. Si vende una empresa o un profesional dentro de su actividad, normalmente la operación lleva IVA. Comprar a través de un bróker no convierte una venta entre particulares en una venta de empresa. Cada caso se confirma con la documentación antes de reservar; los porcentajes, en la guía del <a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">ITP al comprar un barco usado</a>.</li>
          <li><strong>Seguro.</strong> El de responsabilidad civil es obligatorio. Comprueba que la póliza esté en vigor y cubra el barco y el uso que le vas a dar.</li>
        </ul>

        <h2 id="remolque">Si se vende con remolque</h2>
        <p>Muchas semirrígidas se venden con remolque (las dos que tengo, por ejemplo). Lo que hay que mirar:</p>
        <ul>
          <li><strong>Papeles.</strong> Si el remolque pasa de 750 kg de MMA, lleva matrícula propia, ITV y su propio seguro, y también hay que cambiarlo de titular.</li>
          <li><strong>Tu carné.</strong> Con el B puedes llevar un remolque de hasta 750 kg de MMA. Si pasa de 750 kg, con el B la suma de la MMA del coche y la del remolque no puede superar los 3.500 kg; hasta 4.250 kg necesitas el B96, y por encima, el BE.</li>
          <li><strong>Tu coche.</strong> Mira en su ficha técnica cuánto puede remolcar.</li>
          <li><strong>Estado.</strong> Luces, rodillos, ruedas, cabrestante y chasis sin óxido serio.</li>
        </ul>
        <p>Si necesitas uno nuevo, tienes los <a href="{p}/remolques/">remolques</a> que pido a fábrica.</p>

        <h2 id="prueba">La prueba de mar</h2>
        <p>Siempre que se pueda, hay que probarla con una carga normal: cómo sale al planeo, si el motor llega a plena aceleración al régimen de vueltas que marca el fabricante, si vibra o hace ruidos raros, si salta alguna alarma o sube la temperatura y cómo vira. Al volver a puerto, mira otra vez los flotadores y si ha entrado agua.</p>

        <div class="tbl">
        <table>
          <thead><tr><th>Qué reviso</th><th>Buena señal</th><th>Señal de alarma</th></tr></thead>
          <tbody>
            <tr><td>Flotadores</td><td>Mantienen la presión, pegados firmes</td><td>Pierden aire, pegajosos, costuras abiertas</td></tr>
            <tr><td>Motor</td><td>Horas que cuadran, facturas, arranque limpio</td><td>Sin historial, alarmas o temperatura alta</td></tr>
            <tr><td>Casco</td><td>Espejo de popa firme y seco, fondo sin golpes</td><td>Grietas o humedad en el espejo, fibra agrietada</td></tr>
            <tr><td>Papeles</td><td>Titular claro, sin cargas, eslora clara</td><td>Cargas, o el vendedor no enseña los papeles</td></tr>
            <tr><td>Remolque</td><td>Matrícula, ITV y seguro en regla, luces bien</td><td>Sin papeles o con el chasis oxidado</td></tr>
          </tbody>
        </table>
        </div>
''',
cta_e='¿Te encaja alguna?', cta_t='Si alguna de las semirrígidas que tengo te encaja, hablamos de su estado, sus papeles y de cuándo verla.', cta_p='Prefiero aclarar las dudas antes de que te desplaces.', cta_b='Preguntar por una visita',
new='''
        <h2 id="nueva">¿Y si prefieres una nueva?</h2>
        <p>También trabajo semirrígidas nuevas bajo pedido: las <a href="{p}/skipper/">SKIPPER</a>, de 10,85 a 13,40 m, desde 329.000 € + impuestos con motores, y las <a href="{p}/marco/">Mar.Co</a>, de 7,40 a 13,50 m, desde 66.000 € + impuestos sin motores. Las tienes en <a href="{p}/barcos-nuevos/">barcos nuevos</a>, y si dudas entre una semirrígida grande y una lancha, en la guía de <a href="{p}/guias/semirrigidas-deportivas-lujo/">semirrígidas deportivas de lujo</a>.</p>
''',
aviso='Esta guía es orientativa y se basa en lo que reviso cuando miro una semirrígida; no sustituye la revisión de un mecánico o un perito. Los precios son los anunciados de los barcos que tengo en venta, no una tabla de mercado, y las horas y el equipo los indica el propietario y se comprueban con la documentación antes de reservar. Lo que digo sobre titulaciones, ITB, impuestos y remolques (RD 875/2014, RD 1434/1999, RD 607/1999 y normas de la DGT) puede cambiar: confírmalo con tu gestoría, con Capitanía o con la DGT. Podemos equivocarnos y nada de lo que pone aquí es vinculante.',
card_e='¿Has visto una semirrígida?', card_h='La miro contigo antes de que hagas una oferta.', card_p='Mándame las fotos y los datos y te digo qué preguntar al vendedor. Sin compromiso.', card_b='Hablar con Juan por WhatsApp',
toc_t='En esta guía', toc=[('precio','Qué influye en el precio'),('flotadores','Los flotadores'),('motor','El motor y las horas'),('casco','Casco y espejo de popa'),('papeles','Papeles e impuestos'),('remolque','El remolque'),('prueba','Prueba de mar'),('nueva','¿Una nueva?')],
rel_t='Otras guías', rel=[('/comprar/semirrigidas-neumaticas-segunda-mano','Semirrígidas de ocasión en venta'),('/guias/que-mirar-comprar-barco-segunda-mano','Qué mirar al comprar un barco de segunda mano'),('/guias/','Todas las guías de Plata Marine')],
)

# ---------------------------------------------------------------- CA
T['ca'] = dict(
title='Semirígida de segona mà: què revisar abans de comprar',
desc='Què revisar en una semirígida de segona mà: flotadors, motor i hores, casc, papers i remolc. I les semirígides que tinc ara en venda.',
h1='Comprar una semirígida de segona mà: què revisar abans de pagar',
crumb='Comprar una semirígida de segona mà',
wa_head='Hola Juan, estic mirant semirígides de segona mà.',
wa_card='Hola Juan, he vist una semirígida de segona mà i vull que la revisis amb mi.',
wa_cta="Hola Juan, m'interessa una de les teves semirígides de segona mà i et vull preguntar per una visita.",
eyebrow='Guies · Comprar',
meta='<span>Per Juan Morante</span><span>Actualitzat octubre 2026</span><span>8 min de lectura</span>',
lead="En una semirígida usada, l'any del casc diu poca cosa. El que de debò marca el preu, i els disgustos, són els flotadors, el motor i els papers. Això és el que reviso abans de recomanar-ne una, amb les dades de les que tinc ara en venda.",
body='''
        <h2 id="precio">Què influeix en el preu d'una semirígida usada</h2>
        <p>Més que l'any del casc, pesen el motor (l'any, les hores i com s'ha mantingut), l'estat dels flotadors, l'equip i si es ven amb remolc. Un exemple de la meva cartera: la <a href="{p}/barcos/sacs-535">Sacs 535</a> és del 2002, però el propietari li ha posat flotadors i tapisseria nous, ha pintat el casc i ha canviat la instal·lació elèctrica i les bateries. Per això el seu preu no s'assembla al d'una altra semirígida del mateix any amb tot original.</p>
        <p>Aquestes són les semirígides que tinc ara en venda. Els preus són els anunciats, no una mitjana de mercat:</p>
        {list}
        <p>Si busques una altra eslora o un altre motor, pots <a href="{p}/alertas/">crear una alerta</a> i t'aviso quan n'entri una que encaixi.</p>

        <h2 id="flotadores">Els flotadors: el primer que miro</h2>
        <p>Són la part que més pateix (el sol, els fregaments amb el pantalà, el remolc) i, després del motor, la més cara de reparar o canviar.</p>
        <ul>
          <li><strong>Material.</strong> Solen ser de teixit amb PVC o amb CSM (el que tothom en diu Hypalon). L'Hypalon sol aguantar millor el sol, però també compten la qualitat del teixit, com està fet i com s'ha cuidat. Pregunta quin porta i de quin any són: els de la Sacs, per exemple, són de PVC i nous.</li>
          <li><strong>Pressió.</strong> Demana que estiguin inflats des del dia abans i comprova-ho, millor amb manòmetre, compartiment per compartiment. Compte: amb fred la pressió baixa sola, així que un flotador una mica més tou no vol dir per si sol que perdi. Si perd de debò, cal trobar on: vàlvules, costures o teixit.</li>
          <li><strong>Costures i enganxats.</strong> Mira la unió del flotador amb el casc, els cons de popa i les zones de fregament. Pedaços n'hi ha molts i no sempre són un problema; un enganxat que s'obre, sí.</li>
          <li><strong>Aspecte.</strong> Descolorit, enganxós al tacte o amb esquerdes fines: són senyals d'envelliment que demanen mirar-ho amb més calma.</li>
          <li><strong>Vàlvules.</strong> Que hi siguin totes i tanquin bé; cada compartiment porta la seva.</li>
        </ul>
        <p>Si són els originals i tenen molts anys, revisa amb especial cura costures, enganxats i teixit. Si estan molt tocats, demana pressupost a un taller per reparar-los o canviar-los abans de fer l'oferta: és una despesa important.</p>

        <h2 id="motor">El motor i les hores</h2>
        <p>Gairebé totes les semirígides de segona mà porten forabord. El que miro:</p>
        <ul>
          <li><strong>L'any del motor no és el del casc.</strong> A la Sacs, casc del 2002 i motor del 2007; a la <a href="{p}/barcos/tiger-marine-650">Tiger Marine 650</a>, casc del 2015 i motor del 2012. Les hores es llegeixen amb l'any del motor.</li>
          <li><strong>Que les hores quadrin amb la història del vaixell.</strong> El propietari de la Tiger Marine indica unes 110 hores i que només la té a l'aigua a l'agost; la resta de l'any és hivernada en una nau. És un ús que quadra amb poques hores, i tot i així convé comprovar-les, quan es pugui, amb el diagnòstic del motor i amb les factures. Poques hores és bo si el motor s'ha cuidat; un motor que ha passat anys aturat i sense manteniment també dona problemes.</li>
          <li><strong>Factures.</strong> Oli, filtres, impulsor de la bomba d'aigua, ànodes i oli de la cua. Si no hi ha papers, pregunta qui en feia el manteniment.</li>
          <li><strong>Arrencada en fred.</strong> Demana veure'l arrencar sense haver-lo engegat abans aquell dia. Mira que surti aigua pel testimoni de refrigeració, que no salti cap alarma i que la temperatura es mantingui normal: el raig del testimoni sol no garanteix que tot el circuit refrigeri bé.</li>
          <li><strong>Cua, hèlix i comandaments.</strong> Que l'oli de la cua no surti amb aigua, que l'hèlix no tingui cops i que el trim i la direcció vagin fins.</li>
          <li><strong>Un mecànic, si hi ha dubtes.</strong> Que el revisi un de confiança abans de pagar. Una prova de compressió ajuda a veure problemes interns (sobretot si un cilindre dona molt diferent dels altres), però no substitueix una revisió completa.</li>
        </ul>

        <h2 id="casco">Casc, consola i mirall de popa</h2>
        <ul>
          <li><strong>Quilla i fons:</strong> cops per varades a la platja o pel remolc.</li>
          <li><strong>Mirall de popa:</strong> que estigui ferm al voltant dels cargols del motor i sense esquerdes, humitat ni senyals de moviment. Un mirall pot estar tocat per dins sense que es mogui a simple vista, i reparar-lo és seriós.</li>
          <li><strong>Reparacions:</strong> si el casc s'ha pintat o reparat, pregunta què s'hi va fer i qui ho va fer.</li>
          <li><strong>Consola i bancs:</strong> ben ancorats i sense esquerdes a la fibra.</li>
          <li><strong>Electricitat i equips:</strong> llums de navegació, bomba d'esgotament, VHF i el que porti. Que tot funcioni amb el motor en marxa.</li>
        </ul>

        <h2 id="papeles">Papers, titulació i impostos</h2>
        <ul>
          <li><strong>Titular i càrregues.</strong> Si el vaixell té bandera espanyola, demana el full d'assentament actualitzat: hi consten les dades del registre i les anotacions que tingui. Si té bandera estrangera, com la Tiger Marine (registre polonès), cal revisar la documentació equivalent d'aquell país i de qui ha estat. Què implica una bandera polonesa ho explico en <a href="{p}/guias/bandera-polaca-abanderar-barco-otro-pais">aquesta guia</a>.</li>
          <li><strong>Titulació.</strong> Compta l'eslora de casc que figura a la documentació, no el nom del model. Amb la Llicència de Navegació pots governar vaixells de fins a 6 metres amb la potència de motor adequada segons el fabricant, només de dia i sense allunyar-te més de 2 milles d'un port, marina o lloc d'abric. El PNB permet vaixells de motor de fins a 8 metres, a no més de 5 milles. Per sobre, una titulació superior. Per això la Sacs (5,35 m) va amb Llicència de Navegació i la Tiger Marine (uns 6,50 m) amb el PNB. Ho tens a <a href="{p}/titulaciones/">titulacions</a>.</li>
          <li><strong>ITB.</strong> En un vaixell espanyol de llista 7a (ús privat), per sota de 6 metres no hi ha reconeixements periòdics; de 6 a 24 metres, com a màxim cada 5 anys. A la llista 6a (lloguer), sempre. Demana el certificat de navegabilitat i els reconeixements que li toquin; en un vaixell amb bandera estrangera, el que exigeixi el seu país. Ho explico a la <a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">guia de la ITB</a>.</li>
          <li><strong>Impostos.</strong> Si compres a un particular, normalment pagues l'ITP, i el percentatge depèn de la comunitat. Si ven una empresa o un professional dins de la seva activitat, normalment l'operació porta IVA. Comprar a través d'un bròquer no converteix una venda entre particulars en una venda d'empresa. Cada cas es confirma amb la documentació abans de reservar; els percentatges, a la guia de l'<a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">ITP en comprar un vaixell usat</a>.</li>
          <li><strong>Assegurança.</strong> La de responsabilitat civil és obligatòria. Comprova que la pòlissa estigui en vigor i cobreixi el vaixell i l'ús que li donaràs.</li>
        </ul>

        <h2 id="remolque">Si es ven amb remolc</h2>
        <p>Moltes semirígides es venen amb remolc (les dues que tinc, per exemple). El que cal mirar:</p>
        <ul>
          <li><strong>Papers.</strong> Si el remolc passa de 750 kg de MMA, porta matrícula pròpia, ITV i la seva pròpia assegurança, i també cal canviar-lo de titular.</li>
          <li><strong>El teu carnet.</strong> Amb el B pots portar un remolc de fins a 750 kg de MMA. Si passa de 750 kg, amb el B la suma de la MMA del cotxe i la del remolc no pot superar els 3.500 kg; fins a 4.250 kg necessites el B96, i per sobre, el BE.</li>
          <li><strong>El teu cotxe.</strong> Mira a la fitxa tècnica quant pot remolcar.</li>
          <li><strong>Estat.</strong> Llums, corrons, rodes, cabrestant i xassís sense rovell seriós.</li>
        </ul>
        <p>Si en necessites un de nou, tens els <a href="{p}/remolques/">remolcs</a> que demano a fàbrica.</p>

        <h2 id="prueba">La prova de mar</h2>
        <p>Sempre que es pugui, cal provar-la amb una càrrega normal: com surt al planatge, si el motor arriba a plena acceleració al règim de voltes que marca el fabricant, si vibra o fa sorolls estranys, si salta alguna alarma o puja la temperatura i com vira. Quan tornis a port, mira un altre cop els flotadors i si ha entrat aigua.</p>

        <div class="tbl">
        <table>
          <thead><tr><th>Què reviso</th><th>Bon senyal</th><th>Senyal d'alarma</th></tr></thead>
          <tbody>
            <tr><td>Flotadors</td><td>Mantenen la pressió, enganxats ferms</td><td>Perden aire, enganxosos, costures obertes</td></tr>
            <tr><td>Motor</td><td>Hores que quadren, factures, arrencada neta</td><td>Sense historial, alarmes o temperatura alta</td></tr>
            <tr><td>Casc</td><td>Mirall de popa ferm i sec, fons sense cops</td><td>Esquerdes o humitat al mirall, fibra esquerdada</td></tr>
            <tr><td>Papers</td><td>Titular clar, sense càrregues, eslora clara</td><td>Càrregues, o el venedor no ensenya els papers</td></tr>
            <tr><td>Remolc</td><td>Matrícula, ITV i assegurança en regla, llums bé</td><td>Sense papers o amb el xassís rovellat</td></tr>
          </tbody>
        </table>
        </div>
''',
cta_e="T'encaixa alguna?", cta_t="Si alguna de les semirígides que tinc t'encaixa, parlem del seu estat, dels papers i de quan veure-la.", cta_p="Prefereixo aclarir els dubtes abans que et desplacis.", cta_b='Preguntar per una visita',
new='''
        <h2 id="nueva">I si en prefereixes una de nova?</h2>
        <p>També treballo semirígides noves per encàrrec: les <a href="{p}/skipper/">SKIPPER</a>, de 10,85 a 13,40 m, des de 329.000 € + impostos amb motors, i les <a href="{p}/marco/">Mar.Co</a>, de 7,40 a 13,50 m, des de 66.000 € + impostos sense motors. Les tens a <a href="{p}/barcos-nuevos/">vaixells nous</a>, i si dubtes entre una semirígida gran i una llanxa, a la guia de <a href="{p}/guias/semirrigidas-deportivas-lujo/">semirígides esportives de luxe</a>.</p>
''',
aviso="Aquesta guia és orientativa i es basa en el que reviso quan miro una semirígida; no substitueix la revisió d'un mecànic o un perit. Els preus són els anunciats dels vaixells que tinc en venda, no una taula de mercat, i les hores i l'equip els indica el propietari i es comproven amb la documentació abans de reservar. El que dic sobre titulacions, ITB, impostos i remolcs (RD 875/2014, RD 1434/1999, RD 607/1999 i normes de la DGT) pot canviar: confirma-ho amb la teva gestoria, amb Capitania o amb la DGT. Ens podem equivocar i res del que hi ha aquí és vinculant.",
card_e='Has vist una semirígida?', card_h="La miro amb tu abans que facis una oferta.", card_p="Envia'm les fotos i les dades i et dic què preguntar al venedor. Sense compromís.", card_b='Parlar amb Juan per WhatsApp',
toc_t='En aquesta guia', toc=[('precio','Què influeix en el preu'),('flotadores','Els flotadors'),('motor','El motor i les hores'),('casco','Casc i mirall de popa'),('papeles','Papers i impostos'),('remolque','El remolc'),('prueba','Prova de mar'),('nueva','Una de nova?')],
rel_t='Altres guies', rel=[('/comprar/semirrigidas-neumaticas-segunda-mano',"Semirígides d'ocasió en venda"),('/guias/que-mirar-comprar-barco-segunda-mano','Què mirar en comprar un vaixell de segona mà'),('/guias/','Totes les guies de Plata Marine')],
)

# ---------------------------------------------------------------- EN
T['en'] = dict(
title='Buying a used RIB in Spain: what to check first',
desc='What to check on a used RIB: tubes, engine and hours, hull, paperwork and trailer. Plus the RIBs I have for sale right now.',
h1='Buying a used RIB: what to check before you pay',
crumb='Buying a used RIB',
wa_head="Hi Juan, I'm looking at used RIBs.",
wa_card="Hi Juan, I've seen a used RIB and I'd like you to look at it with me.",
wa_cta="Hi Juan, I'm interested in one of your used RIBs and I'd like to ask about a viewing.",
eyebrow='Guides · Buying',
meta='<span>By Juan Morante</span><span>Updated October 2026</span><span>8 min read</span>',
lead="On a used RIB, the year of the hull tells you little. What really sets the price, and causes the headaches, is the tubes, the engine and the paperwork. This is what I check before recommending one, with the details of the RIBs I have for sale right now.",
body='''
        <h2 id="precio">What drives the price of a used RIB</h2>
        <p>More than the hull year, what counts is the engine (its year, its hours and how it's been serviced), the condition of the tubes, the equipment and whether it comes with a trailer. An example from my listings: the <a href="{p}/barcos/sacs-535">Sacs 535</a> is from 2002, but the owner has fitted new tubes and upholstery, painted the hull and replaced the wiring and batteries. That's why its price looks nothing like that of another RIB from the same year with everything original.</p>
        <p>These are the RIBs I have for sale right now. The prices are the asking prices, not a market average:</p>
        {list}
        <p>If you're after a different length or engine, you can <a href="{p}/alertas/">set up an alert</a> and I'll let you know when one comes in that fits.</p>

        <h2 id="flotadores">The tubes: the first thing I look at</h2>
        <p>They take the most punishment (sun, rubbing against the pontoon, the trailer) and, after the engine, they're the most expensive part to repair or replace.</p>
        <ul>
          <li><strong>Material.</strong> They're usually PVC-coated or CSM-coated fabric (what everyone calls Hypalon). Hypalon usually stands up to the sun better, but the quality of the fabric, how the tubes were made and how they've been looked after matter too. Ask which one it has and how old the tubes are: the ones on the Sacs, for example, are new PVC.</li>
          <li><strong>Pressure.</strong> Ask for them to be inflated the day before and check them, ideally with a gauge, compartment by compartment. Bear in mind that pressure drops by itself when it's cold, so a slightly softer tube doesn't on its own mean it's leaking. If it really is losing air, the leak needs finding: valves, seams or fabric.</li>
          <li><strong>Seams and bonding.</strong> Check where the tube joins the hull, the stern cones and the rub areas. Plenty of RIBs have patches and that isn't always a problem; bonding that's coming apart is.</li>
          <li><strong>Appearance.</strong> Faded, sticky to the touch or with fine cracks: signs of ageing that call for a closer look.</li>
          <li><strong>Valves.</strong> All present and sealing properly; each compartment has its own.</li>
        </ul>
        <p>If the tubes are original and old, look especially carefully at the seams, bonding and fabric. If they're in poor shape, get a workshop quote to repair or replace them before you make an offer: it's a significant cost.</p>

        <h2 id="motor">The engine and the hours</h2>
        <p>Almost all used RIBs have outboards. What I check:</p>
        <ul>
          <li><strong>The engine year isn't the hull year.</strong> On the Sacs, 2002 hull and 2007 engine; on the <a href="{p}/barcos/tiger-marine-650">Tiger Marine 650</a>, 2015 hull and 2012 engine. Read the hours against the engine's year.</li>
          <li><strong>Hours that match the boat's story.</strong> The Tiger Marine's owner reports around 110 hours and says it's only in the water in August, spending the rest of the year stored indoors. That kind of use fits low hours, but it's still worth checking them, where possible, with the engine diagnostics and the invoices. Low hours are good if the engine has been looked after; an engine that has sat for years without servicing has its own problems.</li>
          <li><strong>Invoices.</strong> Oil, filters, water pump impeller, anodes and gearcase oil. If there's no paperwork, ask who did the servicing.</li>
          <li><strong>Cold start.</strong> Ask to see it start without having been run earlier that day. Check water comes out of the tell-tale, no alarm goes off and the temperature stays normal: the tell-tale stream alone doesn't prove the whole cooling circuit is working.</li>
          <li><strong>Gearcase, propeller and controls.</strong> No water in the gearcase oil, no damage to the propeller, and smooth trim and steering.</li>
          <li><strong>A mechanic, if in doubt.</strong> Have one you trust check it before you pay. A compression test helps spot internal problems (especially if one cylinder reads very differently from the rest), but it doesn't replace a full inspection.</li>
        </ul>

        <h2 id="casco">Hull, console and transom</h2>
        <ul>
          <li><strong>Keel and bottom:</strong> knocks from beaching or from the trailer.</li>
          <li><strong>Transom:</strong> solid around the engine bolts, with no cracks, damp or signs of movement. A transom can be damaged inside without visibly flexing, and repairing it is serious work.</li>
          <li><strong>Repairs:</strong> if the hull has been painted or repaired, ask what was done and who did it.</li>
          <li><strong>Console and seats:</strong> firmly fixed, no cracks in the fibreglass.</li>
          <li><strong>Electrics and equipment:</strong> navigation lights, bilge pump, VHF and anything else fitted. Everything should work with the engine running.</li>
        </ul>

        <h2 id="papeles">Paperwork, licences and taxes</h2>
        <ul>
          <li><strong>Owner and charges.</strong> If the boat is Spanish-flagged, ask for an up-to-date registry extract (hoja de asiento): it shows the registry details and any entries against the boat. If it's foreign-flagged, like the Tiger Marine (Polish register), you need to check the equivalent documents from that country and its ownership history. What a Polish flag means is explained in <a href="{p}/guias/bandera-polaca-abanderar-barco-otro-pais">this guide</a>.</li>
          <li><strong>Licence.</strong> What counts is the hull length in the documents, not the model name. In Spain, the Licencia de Navegación lets you skipper boats up to 6 metres with the engine power the manufacturer specifies as suitable, in daylight only and no more than 2 miles from a port, marina or shelter. The PNB covers motorboats up to 8 metres, no more than 5 miles out. Above that, a higher licence. That's why the Sacs (5.35 m) needs the Licencia de Navegación and the Tiger Marine (about 6.50 m) the PNB. See <a href="{p}/titulaciones/">licences</a>.</li>
          <li><strong>ITB (inspection).</strong> For a Spanish boat on List 7 (private use), there are no periodic inspections under 6 metres; from 6 to 24 metres, at most every 5 years. On List 6 (charter), always. Ask for the certificate of seaworthiness and any inspections due; for a foreign-flagged boat, whatever its country requires. It's explained in the <a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">ITB guide</a>.</li>
          <li><strong>Taxes.</strong> If you buy from a private seller, you normally pay transfer tax (ITP), and the rate depends on the region. If a company or professional sells as part of their business, the sale normally carries VAT. Buying through a broker doesn't turn a private sale into a business sale. Each case is confirmed with the paperwork before you reserve; the rates are in the guide to <a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">ITP on a used boat</a>.</li>
          <li><strong>Insurance.</strong> Third-party liability insurance is compulsory. Check the policy is in force and covers the boat and the use you'll give it.</li>
        </ul>

        <h2 id="remolque">If it comes with a trailer</h2>
        <p>Many RIBs are sold with a trailer (both of mine, for example). What to check:</p>
        <ul>
          <li><strong>Papers.</strong> Above 750 kg gross weight, the trailer has its own registration, ITV and insurance, and ownership has to be transferred too.</li>
          <li><strong>Your licence.</strong> In Spain, a B licence lets you tow a trailer up to 750 kg gross weight. Above 750 kg, with a B licence the gross weights of car and trailer together can't exceed 3,500 kg; up to 4,250 kg you need B96, and above that, BE.</li>
          <li><strong>Your car.</strong> Check its registration documents for how much it can tow.</li>
          <li><strong>Condition.</strong> Lights, rollers, tyres, winch and a chassis without serious rust.</li>
        </ul>
        <p>If you need a new one, there are the <a href="{p}/remolques/">trailers</a> I order from the factory.</p>

        <h2 id="prueba">The sea trial</h2>
        <p>Whenever possible, take it out with a normal load: how it gets onto the plane, whether the engine reaches the manufacturer's full-throttle rev range, any vibration or odd noises, any alarm or rising temperature, and how it turns. Back in port, check the tubes again and whether any water has come in.</p>

        <div class="tbl">
        <table>
          <thead><tr><th>What I check</th><th>Good sign</th><th>Warning sign</th></tr></thead>
          <tbody>
            <tr><td>Tubes</td><td>Hold pressure, bonding solid</td><td>Losing air, sticky, seams opening</td></tr>
            <tr><td>Engine</td><td>Hours that fit, invoices, clean start</td><td>No history, alarms or high temperature</td></tr>
            <tr><td>Hull</td><td>Solid, dry transom, no knocks underneath</td><td>Cracks or damp in the transom, cracked fibreglass</td></tr>
            <tr><td>Paperwork</td><td>Clear owner, no charges, clear length</td><td>Charges, or the seller won't show the papers</td></tr>
            <tr><td>Trailer</td><td>Registration, ITV and insurance in order, lights working</td><td>No papers or a rusty chassis</td></tr>
          </tbody>
        </table>
        </div>
''',
cta_e='Does one fit?', cta_t="If one of my RIBs suits you, let's talk about its condition, its paperwork and when you could see it.", cta_p="I'd rather clear up any questions before you travel.", cta_b='Ask about a viewing',
new='''
        <h2 id="nueva">What if you'd rather have a new one?</h2>
        <p>I also handle new RIBs built to order: <a href="{p}/skipper/">SKIPPER</a>, from 10.85 to 13.40 m, from €329,000 + taxes with engines, and <a href="{p}/marco/">Mar.Co</a>, from 7.40 to 13.50 m, from €66,000 + taxes without engines. They're in <a href="{p}/barcos-nuevos/">new boats</a>, and if you're torn between a large RIB and a speedboat, see the guide to <a href="{p}/guias/semirrigidas-deportivas-lujo/">luxury performance RIBs</a>.</p>
''',
aviso="This guide is for guidance only and is based on what I check when I look at a RIB; it doesn't replace an inspection by a mechanic or a surveyor. The prices are the asking prices of the boats I have for sale, not a market table, and hours and equipment are reported by the owner and checked against the paperwork before you reserve. What I say about licences, ITB, taxes and trailers (RD 875/2014, RD 1434/1999, RD 607/1999 and DGT rules) may change: confirm it with your gestoría, the Harbour Master's office or the DGT. We may get things wrong and nothing on this page is binding.",
card_e='Seen a RIB you like?', card_h="I'll look at it with you before you make an offer.", card_p="Send me the photos and details and I'll tell you what to ask the seller. No obligation.", card_b='Talk to Juan on WhatsApp',
toc_t='In this guide', toc=[('precio','What drives the price'),('flotadores','The tubes'),('motor','Engine and hours'),('casco','Hull and transom'),('papeles','Paperwork and taxes'),('remolque','The trailer'),('prueba','Sea trial'),('nueva','A new one?')],
rel_t='Other guides', rel=[('/comprar/semirrigidas-neumaticas-segunda-mano','Used RIBs for sale'),('/guias/que-mirar-comprar-barco-segunda-mano','What to check when buying a used boat'),('/guias/','All Plata Marine guides')],
)

# ---------------------------------------------------------------- FR
T['fr'] = dict(
title='Semi-rigide d’occasion en Espagne : que vérifier',
desc='Que vérifier sur un semi-rigide d’occasion : flotteurs, moteur et heures, coque, papiers et remorque. Et les semi-rigides que j’ai en vente en ce moment.',
h1='Acheter un semi-rigide d’occasion : que vérifier avant de payer',
crumb='Acheter un semi-rigide d’occasion',
wa_head='Bonjour Juan, je regarde des semi-rigides d’occasion.',
wa_card='Bonjour Juan, j’ai vu un semi-rigide d’occasion et j’aimerais que vous le regardiez avec moi.',
wa_cta='Bonjour Juan, un de vos semi-rigides d’occasion m’intéresse et j’aimerais organiser une visite.',
eyebrow='Guides · Acheter',
meta='<span>Par Juan Morante</span><span>Mis à jour en octobre 2026</span><span>8 min de lecture</span>',
lead='Sur un semi-rigide d’occasion, l’année de la coque dit peu de chose. Ce qui fait vraiment le prix, et les mauvaises surprises, ce sont les flotteurs, le moteur et les papiers. Voici ce que je vérifie avant d’en recommander un, avec les données de ceux que j’ai en vente en ce moment.',
body='''
        <h2 id="precio">Ce qui fait le prix d’un semi-rigide d’occasion</h2>
        <p>Plus que l’année de la coque, ce qui compte, c’est le moteur (son année, ses heures et son entretien), l’état des flotteurs, l’équipement et la présence d’une remorque. Un exemple parmi mes bateaux : le <a href="{p}/barcos/sacs-535">Sacs 535</a> date de 2002, mais son propriétaire a posé des flotteurs et une sellerie neufs, repeint la coque et refait l’installation électrique et les batteries. C’est pour cela que son prix ne ressemble pas à celui d’un autre semi-rigide de la même année resté d’origine.</p>
        <p>Voici les semi-rigides que j’ai en vente en ce moment. Les prix sont les prix affichés, pas une moyenne du marché :</p>
        {list}
        <p>Si vous cherchez une autre longueur ou un autre moteur, vous pouvez <a href="{p}/alertas/">créer une alerte</a> et je vous préviens dès qu’il en arrive un qui vous convient.</p>

        <h2 id="flotadores">Les flotteurs : la première chose que je regarde</h2>
        <p>C’est la partie qui souffre le plus (le soleil, les frottements contre le ponton, la remorque) et, après le moteur, la plus chère à réparer ou à remplacer.</p>
        <ul>
          <li><strong>Matériau.</strong> Ce sont en général des tissus enduits de PVC ou de CSM (ce que tout le monde appelle Hypalon). L’Hypalon résiste en général mieux au soleil, mais la qualité du tissu, la fabrication et l’entretien comptent aussi. Demandez lequel et de quelle année : ceux du Sacs, par exemple, sont en PVC et neufs.</li>
          <li><strong>Pression.</strong> Demandez qu’ils soient gonflés depuis la veille et vérifiez-la, de préférence au manomètre, compartiment par compartiment. Attention : par temps froid la pression baisse toute seule, donc un flotteur un peu plus mou ne signifie pas à lui seul qu’il fuit. S’il perd vraiment de l’air, il faut trouver où : valves, coutures ou tissu.</li>
          <li><strong>Coutures et collages.</strong> Regardez la jonction flotteur-coque, les cônes arrière et les zones de frottement. Les rustines sont fréquentes et pas toujours un problème ; un collage qui s’ouvre, si.</li>
          <li><strong>Aspect.</strong> Décoloré, collant au toucher ou avec de fines craquelures : des signes de vieillissement qui demandent un examen plus attentif.</li>
          <li><strong>Valves.</strong> Toutes présentes et étanches ; chaque compartiment a la sienne.</li>
        </ul>
        <p>S’ils sont d’origine et anciens, examinez avec soin coutures, collages et tissu. S’ils sont très abîmés, demandez un devis de réparation ou de remplacement à un atelier avant de faire une offre : c’est une dépense importante.</p>

        <h2 id="motor">Le moteur et les heures</h2>
        <p>Presque tous les semi-rigides d’occasion ont un hors-bord. Ce que je regarde :</p>
        <ul>
          <li><strong>L’année du moteur n’est pas celle de la coque.</strong> Sur le Sacs, coque de 2002 et moteur de 2007 ; sur le <a href="{p}/barcos/tiger-marine-650">Tiger Marine 650</a>, coque de 2015 et moteur de 2012. Les heures se lisent avec l’année du moteur.</li>
          <li><strong>Des heures cohérentes avec l’histoire du bateau.</strong> Le propriétaire du Tiger Marine indique environ 110 heures et précise qu’il n’est à l’eau qu’en août et passe le reste de l’année à l’abri dans un hangar. C’est un usage cohérent avec peu d’heures, mais il vaut mieux les vérifier, quand c’est possible, avec le diagnostic du moteur et les factures. Peu d’heures, c’est bien si le moteur a été entretenu ; un moteur resté des années à l’arrêt sans entretien pose aussi des problèmes.</li>
          <li><strong>Factures.</strong> Huile, filtres, turbine de pompe à eau, anodes et huile d’embase. Sans papiers, demandez qui faisait l’entretien.</li>
          <li><strong>Démarrage à froid.</strong> Demandez à le voir démarrer sans avoir tourné plus tôt dans la journée. Vérifiez que l’eau sort par le témoin de refroidissement, qu’aucune alarme ne se déclenche et que la température reste normale : le jet du témoin seul ne prouve pas que tout le circuit refroidit bien.</li>
          <li><strong>Embase, hélice et commandes.</strong> Pas d’eau dans l’huile d’embase, pas de chocs sur l’hélice, trim et direction souples.</li>
          <li><strong>Un mécanicien en cas de doute.</strong> Faites-le vérifier par un mécanicien de confiance avant de payer. Un test de compression aide à repérer des problèmes internes (surtout si un cylindre donne une valeur très différente des autres), mais ne remplace pas une révision complète.</li>
        </ul>

        <h2 id="casco">Coque, console et tableau arrière</h2>
        <ul>
          <li><strong>Quille et carène :</strong> chocs dus aux échouages sur la plage ou à la remorque.</li>
          <li><strong>Tableau arrière :</strong> ferme autour des boulons du moteur, sans fissures, humidité ni signe de mouvement. Un tableau peut être abîmé à l’intérieur sans bouger à l’œil nu, et le réparer est un travail sérieux.</li>
          <li><strong>Réparations :</strong> si la coque a été repeinte ou réparée, demandez ce qui a été fait et par qui.</li>
          <li><strong>Console et banquettes :</strong> bien fixées, sans fissures dans la fibre.</li>
          <li><strong>Électricité et équipements :</strong> feux de navigation, pompe de cale, VHF et le reste. Tout doit fonctionner moteur en marche.</li>
        </ul>

        <h2 id="papeles">Papiers, permis et impôts</h2>
        <ul>
          <li><strong>Propriétaire et charges.</strong> Si le bateau est sous pavillon espagnol, demandez l’extrait du registre à jour (hoja de asiento) : il indique les données du registre et les inscriptions éventuelles. S’il est sous pavillon étranger, comme le Tiger Marine (registre polonais), il faut vérifier les documents équivalents de ce pays et l’historique des propriétaires. Ce qu’implique un pavillon polonais, je l’explique dans <a href="{p}/guias/bandera-polaca-abanderar-barco-otro-pais">ce guide</a>.</li>
          <li><strong>Permis.</strong> C’est la longueur de coque indiquée dans les documents qui compte, pas le nom du modèle. En Espagne, la Licencia de Navegación permet de piloter des bateaux jusqu’à 6 mètres avec la puissance moteur adaptée selon le constructeur, de jour uniquement et à 2 milles maximum d’un port, d’une marina ou d’un abri. Le PNB couvre les bateaux à moteur jusqu’à 8 mètres, à 5 milles maximum. Au-delà, un permis supérieur. C’est pour cela que le Sacs (5,35 m) se pilote avec la Licencia de Navegación et le Tiger Marine (environ 6,50 m) avec le PNB. Voir <a href="{p}/titulaciones/">permis</a>.</li>
          <li><strong>ITB (inspection).</strong> Pour un bateau espagnol en liste 7 (usage privé), pas d’inspections périodiques sous 6 mètres ; de 6 à 24 mètres, tous les 5 ans au maximum. En liste 6 (location), toujours. Demandez le certificat de navigabilité et les inspections dues ; pour un bateau sous pavillon étranger, ce qu’exige son pays. Je l’explique dans le <a href="{p}/guias/itb-inspeccion-tecnica-barcos-recreo">guide de l’ITB</a>.</li>
          <li><strong>Impôts.</strong> Si vous achetez à un particulier, vous payez normalement l’ITP (droits de mutation), dont le taux dépend de la région. Si une entreprise ou un professionnel vend dans le cadre de son activité, la vente est normalement soumise à la TVA. Passer par un courtier ne transforme pas une vente entre particuliers en vente professionnelle. Chaque cas se confirme avec les papiers avant de réserver ; les taux sont dans le guide de l’<a href="{p}/guias/itp-comprar-barco-usado-por-comunidad">ITP sur un bateau d’occasion</a>.</li>
          <li><strong>Assurance.</strong> La responsabilité civile est obligatoire. Vérifiez que la police est en vigueur et couvre le bateau et l’usage prévu.</li>
        </ul>

        <h2 id="remolque">S’il est vendu avec remorque</h2>
        <p>Beaucoup de semi-rigides sont vendus avec remorque (mes deux, par exemple). Ce qu’il faut vérifier :</p>
        <ul>
          <li><strong>Papiers.</strong> Au-delà de 750 kg de PTAC, la remorque a sa propre immatriculation, son contrôle technique (ITV) et sa propre assurance, et il faut aussi en changer le titulaire.</li>
          <li><strong>Votre permis.</strong> En Espagne, le permis B permet de tracter une remorque jusqu’à 750 kg de PTAC. Au-delà de 750 kg, avec le B, le PTAC de la voiture et celui de la remorque ensemble ne peuvent pas dépasser 3 500 kg ; jusqu’à 4 250 kg il faut le B96, et au-delà, le BE.</li>
          <li><strong>Votre voiture.</strong> Vérifiez sur sa carte grise ce qu’elle peut tracter.</li>
          <li><strong>État.</strong> Feux, rouleaux, pneus, treuil et châssis sans rouille importante.</li>
        </ul>
        <p>Si vous en avez besoin d’une neuve, il y a les <a href="{p}/remolques/">remorques</a> que je commande à l’usine.</p>

        <h2 id="prueba">L’essai en mer</h2>
        <p>Dès que possible, il faut l’essayer avec une charge normale : comment il déjauge, si le moteur atteint à pleins gaz la plage de régime indiquée par le constructeur, s’il vibre ou fait des bruits bizarres, si une alarme se déclenche ou si la température monte, et comment il vire. De retour au port, regardez à nouveau les flotteurs et s’il a pris l’eau.</p>

        <div class="tbl">
        <table>
          <thead><tr><th>Ce que je vérifie</th><th>Bon signe</th><th>Signal d’alerte</th></tr></thead>
          <tbody>
            <tr><td>Flotteurs</td><td>Tiennent la pression, collages solides</td><td>Perdent de l’air, collants, coutures ouvertes</td></tr>
            <tr><td>Moteur</td><td>Heures cohérentes, factures, démarrage net</td><td>Sans historique, alarmes ou température élevée</td></tr>
            <tr><td>Coque</td><td>Tableau arrière ferme et sec, carène sans chocs</td><td>Fissures ou humidité dans le tableau, fibre fissurée</td></tr>
            <tr><td>Papiers</td><td>Propriétaire clair, sans charges, longueur claire</td><td>Charges, ou le vendeur ne montre pas les papiers</td></tr>
            <tr><td>Remorque</td><td>Immatriculation, ITV et assurance en règle, feux en ordre</td><td>Sans papiers ou châssis rouillé</td></tr>
          </tbody>
        </table>
        </div>
''',
cta_e='L’un d’eux vous convient ?', cta_t='Si l’un de mes semi-rigides vous convient, parlons de son état, de ses papiers et du moment pour le voir.', cta_p='Je préfère répondre à vos questions avant que vous vous déplaciez.', cta_b='Demander une visite',
new='''
        <h2 id="nueva">Et si vous préférez un neuf ?</h2>
        <p>Je m’occupe aussi de semi-rigides neufs sur commande : les <a href="{p}/skipper/">SKIPPER</a>, de 10,85 à 13,40 m, à partir de 329 000 € + taxes avec moteurs, et les <a href="{p}/marco/">Mar.Co</a>, de 7,40 à 13,50 m, à partir de 66 000 € + taxes sans moteurs. Vous les trouverez dans <a href="{p}/barcos-nuevos/">bateaux neufs</a> et, si vous hésitez entre un grand semi-rigide et une vedette, dans le guide des <a href="{p}/guias/semirrigidas-deportivas-lujo/">semi-rigides sportifs de luxe</a>.</p>
''',
aviso='Ce guide est indicatif et repose sur ce que je vérifie quand je regarde un semi-rigide ; il ne remplace pas l’inspection d’un mécanicien ou d’un expert. Les prix sont les prix affichés des bateaux que j’ai en vente, pas un tableau de marché, et les heures et l’équipement sont indiqués par le propriétaire et vérifiés avec les papiers avant la réservation. Ce que je dis sur les permis, l’ITB, les impôts et les remorques (RD 875/2014, RD 1434/1999, RD 607/1999 et règles de la DGT) peut changer : confirmez-le auprès de votre gestoría, de la Capitanía Marítima ou de la DGT. Nous ne parlons pas français et utilisons un traducteur. Nous pouvons nous tromper et rien sur cette page n’est contractuel.',
card_e='Vous avez vu un semi-rigide ?', card_h='Je le regarde avec vous avant que vous fassiez une offre.', card_p='Envoyez-moi les photos et les données et je vous dis quoi demander au vendeur. Sans engagement.', card_b='Écrire à Juan sur WhatsApp',
toc_t='Dans ce guide', toc=[('precio','Ce qui fait le prix'),('flotadores','Les flotteurs'),('motor','Moteur et heures'),('casco','Coque et tableau arrière'),('papeles','Papiers et impôts'),('remolque','La remorque'),('prueba','Essai en mer'),('nueva','Un neuf ?')],
rel_t='Autres guides', rel=[('/comprar/semirrigidas-neumaticas-segunda-mano','Semi-rigides d’occasion en vente'),('/guias/que-mirar-comprar-barco-segunda-mano','Que vérifier en achetant un bateau d’occasion'),('/guias/','Tous les guides de Plata Marine')],
)

ASIDE = {'es': 'Contacto y navegación', 'ca': 'Contacte i navegació', 'en': 'Contact and navigation', 'fr': 'Contact et navigation'}

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')

def pre(lang):
    return '' if lang == 'es' else lang + '/'

def build(lang):
    t = T[lang]; p = '' if lang == 'es' else '/' + lang
    src = open(f"{pre(lang)}guias/{SRC}/index.html", encoding='utf-8').read()
    lst = open(pre(lang) + LIST, encoding='utf-8').read()
    style = re.search(r'<style>\.pm-list\{.*?</style>', lst, re.S).group(0)
    box = re.search(r'<div class="pm-list" data-f=\'[^\']*\'>.*?</a></div>', lst, re.S).group(0)
    empty = re.search(r'<p class="pm-empty" hidden>.*?</p>', lst, re.S).group(0)
    head, rest = src.split('<main class="art">', 1)
    foot = rest.split('</main>', 1)[1]
    url = f"{BASE}{p}/guias/{SLUG}/"
    head = head.replace(SRC, SLUG)
    head = re.sub(r'<title>.*?</title>', f"<title>{t['title']}</title>", head, count=1)
    for k, v in (('name="description"', t['desc']), ('property="og:title"', t['title']), ('property="og:description"', t['desc']), ('property="og:image"', OG)):
        head = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + esc(v), head, count=1)
    head = head.replace('og:image:width" content="1200"', 'og:image:width" content="1600"').replace('og:image:height" content="630"', 'og:image:height" content="1000"')
    art = {"@context": "https://schema.org", "@type": "Article", "headline": t['h1'],
           "author": {"@type": "Person", "name": "Juan Morante"}, "publisher": {"@type": "Organization", "name": "Plata Marine"},
           "datePublished": DATE, "dateModified": DATE, "inLanguage": lang, "mainEntityOfPage": url, "image": OG}
    head = re.sub(r'(<script type="application/ld\+json">\s*)\{"@context": "https://schema.org", "@type": "Article".*?\}\s*(</script>)',
                  lambda m: m.group(1) + json.dumps(art, ensure_ascii=False) + "\n" + m.group(2), head, count=1, flags=re.S)
    head = re.sub(r'("position": 3, "name": ")[^"]*', lambda m: m.group(1) + t['crumb'], head, count=1)
    head = re.sub(r'(<a class="btn btn-wa" href="https://wa.me/34633742973\?text=)[^"]*(" target="_blank" rel="noopener">[^<]*</a><div class="langsw")',
                  lambda m: m.group(1) + quote(t['wa_head'], safe='') + m.group(2), head, count=1)
    head = head.replace('</head>', style + '\n</head>', 1)
    foot = foot.replace('</body>', '<script src="/inventario.js?v=20261006" defer></script>\n<script src="/portal.js?v=20261007" defer></script>\n</body>', 1)
    toc = ''.join(f'\n          <li><a href="#{a}">{b}</a></li>' for a, b in t['toc'])
    rel = ''.join(f'\n        <a href="{p}{h}">{x}</a>' for h, x in t['rel'])
    body = t['body'].replace('{list}', box + '\n        ' + empty).replace('{p}', p)
    new = t['new'].replace('{p}', p)
    cta = (f'''
        <div class="next-step" data-next="visita" style="background:rgba(181,138,44,.08);border-left:3px solid #B58A2C;padding:16px 18px;border-radius:0 6px 6px 0;margin:26px 0"><p class="eyebrow" style="margin:0 0 8px">{t['cta_e']}</p><p style="margin:0 0 12px"><strong>{t['cta_t']}</strong> {t['cta_p']}</p><a class="next-btn" style="display:inline-block;background:#0E3042;color:#fff;padding:10px 18px;border-radius:6px;text-decoration:none;font-family:var(--display,inherit);font-weight:600;font-size:15px" href="{WA}{quote(t['wa_cta'], safe='')}" target="_blank" rel="noopener">{t['cta_b']}</a></div>''')
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
{new}
        <p class="aviso" style="font-size:.82em;opacity:.85">{t['aviso']}</p>
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
    out = f"{pre(lang)}guias/{SLUG}/index.html"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(head + main + foot)
    return out

if __name__ == '__main__':
    for l in ('es', 'ca', 'en', 'fr'):
        print(build(l))
