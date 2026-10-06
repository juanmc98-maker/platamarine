# -*- coding: utf-8 -*-
# Contenido maestro (ES) de las páginas para compradores franceses. Las versiones CA/EN/FR
# viven en content_ca.py, content_en.py y content_fr.py con la misma estructura.
FECHA = "octubre 2026"

PAGES = {}

PAGES["g1"] = dict(
    kind="guia",
    slug="guias/comprar-barco-espana-matricular-francia.html",
    crumb=("Guías", "/guias/"),
    title="Comprar un barco en España y matricularlo en Francia: guía paso a paso",
    desc="Si vives en Francia y has encontrado un barco en España: qué impuestos se pagan aquí, cómo se da de baja en el registro español, cómo llevarlo y qué papeles pide Francia para matricularlo.",
    eyebrow="Guías · Comprar desde Francia",
    h1="Comprar un barco en España y matricularlo en Francia",
    meta=["Por Juan Morante", "Actualizado octubre 2026", "8 min de lectura"],
    lead="Cada vez más gente que vive en Francia busca barco en Cataluña. La compra se puede hacer sin problema, pero hay dos países y dos administraciones de por medio, y conviene hacer las cosas en orden. Aquí te explico el camino completo: lo que se comprueba antes de pagar, lo que se paga en España, cómo se da de baja el barco aquí y qué pide Francia para matricularlo.",
    toc=[("antes", "Antes de pagar: qué comprobar"), ("impuestos", "Impuestos en España"), ("baja", "La baja en el registro español"), ("llevarlo", "Cómo llevar el barco a Francia"), ("francia", "Matricularlo en Francia"), ("despues", "Después: tasa anual y permiso"), ("riesgos", "Los riesgos más habituales"), ("faq", "Preguntas frecuentes")],
    body="""
<h2 id="antes">Antes de pagar: qué comprobar</h2>
<p>Lo que más problemas da en una compra entre dos países no es el papeleo, sino descubrir tarde que algo no cuadra. Antes de dejar ninguna señal, pide y revisa esto:</p>
<ul>
<li><strong>Quién es el titular.</strong> Que quien te vende sea el propietario que figura en la documentación del barco, o tenga poder para vender.</li>
<li><strong>Cargas.</strong> Que el barco no tenga hipotecas ni embargos. Se comprueba en el Registro de Bienes Muebles. Si tuviera algún acreedor, para dar de baja el barco hará falta su autorización.</li>
<li><strong>El IVA.</strong> Que el barco tenga el IVA pagado en la Unión Europea. Lo normal es pedir la factura de la primera venta. Para matricularlo en Francia te pedirán justificarlo, sobre todo si mide más de 7,5 metros.</li>
<li><strong>La bandera actual.</strong> Si el barco tiene bandera española, la baja se pide en España. Si tiene otra bandera (por ejemplo, polaca), la baja se pide en el registro de ese país, y es un trámite distinto.</li>
<li><strong>Motores.</strong> Que los números de serie de los motores coincidan con los papeles. Francia pide también la factura o el documento de compra de los motores.</li>
<li><strong>Declaración de conformidad CE.</strong> Francia la pide para matricular. Los barcos puestos en el mercado europeo antes del 16 de junio de 1998 no la tienen y se tramitan con otro documento.</li>
</ul>
<p>Mi consejo es hacer la <strong>prueba de mar y el peritaje antes de dejar la señal</strong>, o dejar la señal con la condición de que el peritaje salga bien. Lo tienes explicado en la <a href="/guias/arras-compraventa-barco.html">guía de las arras</a>.</p>

<h2 id="impuestos">Impuestos en España</h2>
<p>Depende de quién te venda el barco:</p>
<ul>
<li><strong>Si vende un particular</strong>, se paga el impuesto de transmisiones (ITP). Si no eres residente en España, no se paga a Cataluña sino a la Agencia Tributaria del Estado: el tipo es el <strong>4 %</strong>, se declara con el <strong>modelo 620</strong> para no residentes y hay <strong>30 días hábiles</strong> desde la firma del contrato. Se calcula sobre el precio o sobre el valor de tablas de Hacienda, si es mayor.</li>
<li><strong>Si vende una empresa</strong>, la operación lleva IVA en lugar de ITP: en un barco usado, normalmente el IVA español. Si el vendedor aplica el régimen especial de bienes usados, el IVA va incluido en el precio y no aparece desglosado; pide que la factura lo indique, porque es tu prueba del IVA ante Francia.</li>
<li><strong>Barco «nuevo»:</strong> si mide más de 7,5 metros y se entrega en los 3 meses siguientes a su primera puesta en servicio o con menos de 100 horas de navegación, para la ley es un medio de transporte nuevo y el IVA se paga en Francia, no en España.</li>
</ul>
<p>Para declarar y hacer los trámites en España, normalmente te pedirán un <strong>NIE</strong> (número de identificación de extranjero). Conviene pedirlo con tiempo.</p>
<p>Si compras siendo residente en España, el ITP es el de tu comunidad autónoma: lo tienes en la <a href="/guias/itp-comprar-barco-usado-por-comunidad.html">guía del ITP por comunidades</a>.</p>

<h2 id="baja">La baja en el registro español</h2>
<p>Para matricular el barco en Francia, primero tiene que salir del registro español. Se pide en la <strong>Capitanía Marítima</strong> como <strong>baja por exportación</strong> (definitiva o provisional), con la solicitud de recreo y la tasa correspondiente (modelo 790-025). Se aporta la hoja de asiento, el documento de la compraventa, la autorización de los acreedores si los hay y, si el barco tiene MMSI (el número de la radio), la declaración de que se ha desprogramado.</p>
<p>La ley dice que la baja la pide el titular o alguien autorizado por él. Por eso es importante dejarlo pactado en el contrato: que el vendedor firme la solicitud o te autorice a pedirla. El certificado de baja es uno de los papeles que te pedirá Francia.</p>

<h2 id="llevarlo">Cómo llevar el barco a Francia</h2>
<p>Hay dos formas:</p>
<ul>
<li><strong>Por carretera.</strong> Para barcos que caben en un remolque o en un camión. Por encima de ciertas medidas (en Francia, más de 2,55 m de ancho) es un transporte especial con su permiso. Lo resuelve la empresa de transporte.</li>
<li><strong>Navegando.</strong> Un barco dado de baja se queda sin bandera, y sin bandera no se puede navegar. Lo habitual es hacer primero el cambio de titular en España, ir navegando con la bandera española y pedir la baja después. Para navegar por aguas españolas hace falta un seguro de responsabilidad civil válido en España. Confirma este orden con la gestoría antes de firmar, porque depende de cada caso.</li>
</ul>

<h2 id="francia">Matricularlo en Francia</h2>
<p>Desde 2022, en Francia la antigua francisation y la matrícula se han unido en un único trámite: el <strong>certificat d'enregistrement</strong>. Lo lleva la administración marítima (las DDTM y DML, según el puerto base). El portal <em>demarches-plaisance.gouv.fr</em> sirve para barcos nuevos y para ventas entre particulares de barcos que ya son franceses; un barco que viene de un registro extranjero se tramita con la DDTM.</p>
<p>Los papeles que suelen pedir:</p>
<ul>
<li>Factura o contrato de compraventa del barco y de los motores.</li>
<li>Declaración de conformidad CE (o el documento equivalente para barcos anteriores a junio de 1998).</li>
<li>Justificante de la situación del IVA, si el barco se compró en otro país de la UE.</li>
<li>Certificado de baja del registro anterior.</li>
<li>Documento de identidad y justificante de domicilio en Francia.</li>
<li>La ficha de solicitud (<em>fiche plaisance</em>).</li>
</ul>
<p>Para matricular en Francia, al menos el 50 % del barco tiene que ser de un ciudadano de la UE y te pedirán un domicilio en Francia.</p>

<h2 id="despues">Después: tasa anual y permiso</h2>
<p>En Francia, los barcos de <strong>7 metros o más</strong>, y los de menos de 7 metros con un motor de 22 CV fiscales o más, pagan una tasa anual (la antigua DAFN). La parte del casco va de unos <strong>77 € para 7-8 metros</strong> a 886 € a partir de 15 metros, más una parte por la potencia del motor, con rebajas para barcos antiguos. Se paga en línea. Francia ha aprobado cambiar el cálculo a partir de 2027.</p>
<p>Para gobernar un barco francés con motor de más de 4,5 kW (6 CV) necesitas el <strong>permis plaisance</strong>: la opción costera permite alejarte hasta 6 millas de un refugio.</p>

<h2 id="riesgos">Los riesgos más habituales</h2>
<div class="tbl"><table><thead><tr><th>Riesgo</th><th>Cómo evitarlo</th></tr></thead><tbody>
<tr><td>Barco con hipoteca o embargo</td><td>Pedir la nota del Registro de Bienes Muebles antes de pagar</td></tr>
<tr><td>IVA sin justificar</td><td>Factura de primera venta o factura del vendedor profesional que lo indique</td></tr>
<tr><td>Bandera de otro país (polaca u otra)</td><td>Saber dónde se pide la baja antes de comprar</td></tr>
<tr><td>Motores que no cuadran con los papeles</td><td>Comprobar números de serie y pedir sus facturas</td></tr>
<tr><td>Barco «casi nuevo» facturado con IVA español</td><td>Si es medio de transporte nuevo, el IVA va en Francia</td></tr>
<tr><td>ITP sin pagar</td><td>Modelo 620 en 30 días hábiles; sin él se complica el cambio de titular</td></tr>
</tbody></table></div>

<h2 id="ayuda">Cómo te puedo ayudar</h2>
<p>Soy broker náutico en Cataluña: pongo en contacto a quien vende su barco con quien lo compra. Te ayudo a encontrar el barco, reviso con el vendedor la documentación (titular, cargas, IVA, motores, bandera) y te acompaño en la prueba de mar y en el peritaje si quieres hacerlo. Los trámites de la baja en España y de la matrícula en Francia los hace una gestoría náutica; en el <a href="/servicios/directorio.html">directorio de empresas</a> tienes gestorías por zona.</p>

<h2 id="faq">Preguntas frecuentes</h2>
<h3>¿Pago impuestos en España y otra vez en Francia?</h3><p>Si compras un barco usado con el IVA europeo pagado, no se vuelve a pagar IVA en Francia. En España pagas el ITP del 4 % si compras a un particular, o el IVA si compras a una empresa. Después, en Francia, la tasa anual si el barco está obligado.</p>
<h3>¿Puedo volver navegando con el barco?</h3><p>Sí, pero no con el barco ya dado de baja, porque se queda sin bandera. Lo habitual es hacer primero el cambio de titular en España, navegar con bandera española y pedir la baja después. Confírmalo con la gestoría.</p>
<h3>¿Necesito NIE?</h3><p>Normalmente sí, para declarar el impuesto y hacer el cambio de titular. Conviene pedirlo con tiempo.</p>
<h3>¿Cuánto cuesta la tasa anual en Francia?</h3><p>Los barcos de menos de 7 metros con poca potencia no la pagan. Para un barco de 7 a 8 metros, la parte del casco son unos 77 € al año, más una parte según la potencia del motor.</p>
""",
    faq=[("¿Pago impuestos en España y otra vez en Francia?", "Si compras un barco usado con el IVA europeo pagado, no se vuelve a pagar IVA en Francia. En España pagas el ITP del 4 % si compras a un particular, o el IVA si compras a una empresa. Después, en Francia, la tasa anual si el barco está obligado."),
         ("¿Puedo volver navegando con el barco?", "Sí, pero no con el barco ya dado de baja, porque se queda sin bandera. Lo habitual es hacer primero el cambio de titular en España, navegar con bandera española y pedir la baja después. Confírmalo con la gestoría."),
         ("¿Necesito NIE?", "Normalmente sí, para declarar el impuesto y hacer el cambio de titular. Conviene pedirlo con tiempo."),
         ("¿Cuánto cuesta la tasa anual en Francia?", "Los barcos de menos de 7 metros con poca potencia no la pagan. Para un barco de 7 a 8 metros, la parte del casco son unos 77 € al año, más una parte según la potencia del motor.")],
    note="Información orientativa, revisada en octubre de 2026 según la normativa española (Texto refundido del ITP, arts. 6, 8 y 11; RD 1027/1989; RD 1435/2010; RD 607/1999) y la información oficial francesa (mer.gouv.fr, service-public.fr, douane.gouv.fr, BOFiP). No es asesoramiento fiscal ni legal y la normativa puede cambiar. Cada caso depende del barco y de tu situación: confírmalo con una gestoría náutica o con la administración antes de comprar.",
    card=dict(eyebrow="¿Vives en Francia?", h3="Te ayudo a encontrar el barco en Cataluña.", p="Cuéntame qué buscas y dónde lo vas a usar, y te digo qué barcos encajan y qué papeles revisar.", wa="Hola Juan, vivo en Francia y busco un barco en España.", btn="Hablar con Juan por WhatsApp"),
    rel=[("/comprar/barcos-ocasion-espana-compradores-franceses.html", "Barcos de ocasión en España para compradores franceses"), ("/guias/barco-frances-en-cataluna.html", "Tener tu barco en Cataluña si vives en Francia"), ("/guias/itp-comprar-barco-usado-por-comunidad.html", "ITP al comprar un barco usado")],
    header_wa="Hola Juan, vivo en Francia y tengo una duda sobre comprar un barco en España.",
)

PAGES["g2"] = dict(
    kind="guia",
    slug="guias/barco-frances-en-cataluna.html",
    crumb=("Guías", "/guias/"),
    title="Tener tu barco en Cataluña si vives en Francia: amarre, impuestos y permiso",
    desc="Si veraneas en Cataluña y quieres tener el barco aquí: traer tu barco francés o comprar uno en España, qué impuestos y seguros aplican, qué permiso necesitas y cómo funcionan los amarres en la Costa Brava.",
    eyebrow="Guías · Si vives en Francia",
    h1="Tener tu barco en Cataluña si vives en Francia",
    meta=["Por Juan Morante", "Actualizado octubre 2026", "7 min de lectura"],
    lead="Si pasas los veranos en la Costa Brava o en otro punto de Cataluña, tener el barco aquí te ahorra el viaje de cada año. Hay dos caminos: traer tu barco con bandera francesa o comprar uno aquí. Los dos funcionan, pero cada uno tiene sus reglas. Te las resumo.",
    toc=[("dos", "Dos caminos"), ("frances", "Traer tu barco con bandera francesa"), ("espanol", "Comprar aquí y dejarlo con bandera española"), ("permiso", "Qué permiso necesitas"), ("amarre", "Amarre e invernaje"), ("faq", "Preguntas frecuentes")],
    body="""
<h2 id="dos">Dos caminos</h2>
<ul>
<li><strong>Traer tu barco francés</strong> y dejarlo amarrado aquí con su bandera.</li>
<li><strong>Comprar un barco en España</strong> y, o bien llevarlo a Francia (lo tienes en la <a href="/guias/comprar-barco-espana-matricular-francia.html">guía para matricularlo en Francia</a>), o bien dejarlo aquí con bandera española.</li>
</ul>

<h2 id="frances">Traer tu barco con bandera francesa</h2>
<p>Francia y España son de la Unión Europea, así que un barco francés con el IVA europeo pagado puede estar en un puerto catalán <strong>sin trámites de entrada</strong> ni aduana. Te conviene llevar a bordo los papeles del barco y el justificante del IVA.</p>
<p>No hay un plazo máximo de estancia mientras el barco lo uses tú y personas que tampoco viven en España. El punto delicado es <strong>quién lo usa</strong>: la ley española obliga a matricular en España los barcos que usan aquí personas residentes en España, y a pagar el impuesto de matriculación (el 12 % en barcos de más de 8 metros). Hacienda ha dicho en consultas recientes que las entradas repetidas de un barco extranjero usado por un residente se consideran uso habitual. En la práctica: si lo dejas a familiares, amigos o a un patrón que vive en España, puede aparecer esa obligación. Lo explicamos en la <a href="/guias/impuesto-matriculacion-barcos.html">guía del impuesto de matriculación</a>.</p>
<p>Dos cosas más:</p>
<ul>
<li><strong>Seguro.</strong> En aguas españolas es obligatorio un seguro de responsabilidad civil, también para barcos extranjeros. Comprueba que tu póliza francesa cubre España.</li>
<li><strong>La tasa anual francesa</strong> se sigue pagando en Francia aunque el barco esté aquí. En España pagarás el amarre y los servicios del puerto.</li>
</ul>

<h2 id="espanol">Comprar aquí y dejarlo con bandera española</h2>
<p>Un no residente puede tener un barco con bandera española a su nombre. Lo que te vas a encontrar:</p>
<ul>
<li><strong>Impuesto de la compra.</strong> Si compras a un particular siendo no residente, el ITP es el <strong>4 %</strong>, con el modelo 620 de la Agencia Tributaria del Estado y 30 días hábiles de plazo. Si compras a una empresa, IVA.</li>
<li><strong>NIE.</strong> Normalmente te lo pedirán para declarar y hacer el cambio de titular.</li>
<li><strong>ITB.</strong> La inspección técnica: en los barcos de recreo de 6 a 24 metros, como máximo cada 5 años. Los de menos de 6 metros no tienen inspecciones periódicas.</li>
<li><strong>Seguro de responsabilidad civil</strong> obligatorio.</li>
<li><strong>Ojo en Francia:</strong> si vives en Francia y navegas por aguas francesas con un barco de bandera extranjera, Francia puede cobrarte un impuesto equivalente a su tasa anual (el <em>droit de passeport</em>). Si el barco se queda en España, no te afecta.</li>
</ul>

<h2 id="permiso">Qué permiso necesitas</h2>
<ul>
<li><strong>Barco con bandera francesa:</strong> se aplica la normativa francesa también en España. Con tu <em>permis plaisance</em> puedes gobernarlo dentro de sus límites (la opción costera, hasta 6 millas de un refugio).</li>
<li><strong>Barco con bandera española:</strong> como ciudadano europeo con un título de tu país, la Capitanía Marítima te puede autorizar a gobernarlo. Es un trámite que conviene hacer antes de la temporada. Tienes las titulaciones españolas en <a href="/titulaciones/">titulaciones</a>.</li>
</ul>

<h2 id="amarre">Amarre e invernaje</h2>
<p>En la Costa Brava, la mayoría de puertos los gestionan clubs náuticos o empresas concesionarias. Cerca de la frontera tienes Portbou, Colera, Llançà, El Port de la Selva, Roses, Empuriabrava, L'Escala, L'Estartit y, más al sur, Palamós.</p>
<ul>
<li><strong>Anual o por temporada.</strong> El amarre anual sale más barato por mes, pero en verano el de alquiler escasea y en los puertos pequeños hay lista de espera. Como referencia, las tarifas oficiales 2026 del puerto de Portbou para un barco de 7,5 a 8,5 metros son unos 3.445 € al año, o unos 1.045 € por un mes de julio o agosto.</li>
<li><strong>Invernaje en seco.</strong> Para barcos de hasta 7-8 metros, la marina seca o el varadero suelen salir más baratos que el agua, y el barco pasa el invierno protegido.</li>
<li><strong>Mantenimiento cuando no estás.</strong> Es lo que más preocupa a quien vive lejos: alguien que revise amarras, baterías y sentinas. En <a href="/servicios/">servicios</a> tienes empresas de mantenimiento y varaderos.</li>
</ul>
<p>Tienes más precios y tipos de amarre en la <a href="/guias/amarres-cataluna-tipos-precios-alquiler-compra.html">guía de amarres en Cataluña</a>.</p>

<h2 id="ayuda">Cómo te puedo ayudar</h2>
<p>Si buscas barco para tenerlo aquí, te ayudo a encontrarlo y reviso con el vendedor la documentación. Y si el barco se vende con amarre que se puede traspasar, lo indico en la ficha.</p>

<h2 id="faq">Preguntas frecuentes</h2>
<h3>¿Puedo dejar mi barco francés todo el año en Cataluña?</h3><p>Sí. Al ser un barco de la Unión Europea con el IVA pagado, no hay plazo máximo mientras lo uses tú y otras personas que no vivan en España.</p>
<h3>¿Puedo prestarle el barco a un amigo que vive en España?</h3><p>Con cuidado: si lo usan residentes en España, la ley puede obligar a matricularlo aquí y a pagar el impuesto de matriculación. Consúltalo antes con una gestoría.</p>
<h3>¿Me sirve mi permis plaisance en España?</h3><p>Para un barco con bandera francesa, sí, dentro de sus límites. Para un barco con bandera española necesitas una autorización de la Capitanía Marítima.</p>
<h3>¿Es obligatorio el seguro?</h3><p>En aguas españolas, sí: un seguro de responsabilidad civil, también para barcos con bandera extranjera.</p>
""",
    faq=[("¿Puedo dejar mi barco francés todo el año en Cataluña?", "Sí. Al ser un barco de la Unión Europea con el IVA pagado, no hay plazo máximo mientras lo uses tú y otras personas que no vivan en España."),
         ("¿Puedo prestarle el barco a un amigo que vive en España?", "Con cuidado: si lo usan residentes en España, la ley puede obligar a matricularlo aquí y a pagar el impuesto de matriculación. Consúltalo antes con una gestoría."),
         ("¿Me sirve mi permis plaisance en España?", "Para un barco con bandera francesa, sí, dentro de sus límites. Para un barco con bandera española necesitas una autorización de la Capitanía Marítima."),
         ("¿Es obligatorio el seguro?", "En aguas españolas, sí: un seguro de responsabilidad civil, también para barcos con bandera extranjera.")],
    note="Información orientativa, revisada en octubre de 2026 según la normativa española (Ley 38/1992, disposición adicional 1.ª y art. 65; consulta DGT V0820-25; RD 875/2014; RD 1434/1999; RD 607/1999; Texto refundido del ITP) y la información oficial francesa (mer.gouv.fr, douane.gouv.fr). Los precios de amarre son las tarifas publicadas por el puerto de Portbou para 2026 y pueden cambiar. No es asesoramiento fiscal ni legal: confírmalo con una gestoría náutica o con la administración.",
    card=dict(eyebrow="¿Veraneas en Cataluña?", h3="Te ayudo a tener tu barco aquí.", p="Cuéntame dónde pasas el verano y qué barco buscas, y te digo qué encaja.", wa="Hola Juan, veraneo en Cataluña y quiero tener un barco aquí.", btn="Hablar con Juan por WhatsApp"),
    rel=[("/comprar/barcos-ocasion-espana-compradores-franceses.html", "Barcos de ocasión en España para compradores franceses"), ("/guias/comprar-barco-espana-matricular-francia.html", "Comprar en España y matricular en Francia"), ("/guias/amarres-cataluna-tipos-precios-alquiler-compra.html", "Amarres en Cataluña: tipos y precios")],
    header_wa="Hola Juan, veraneo en Cataluña y tengo una duda sobre tener el barco aquí.",
)

PAGES["l4"] = dict(
    kind="landing",
    slug="comprar/barcos-ocasion-espana-compradores-franceses.html",
    crumb=("Comprar barco", "/comprar/"),
    title="Barcos de ocasión en España para compradores que viven en Francia",
    desc="Barcos de segunda mano en venta en Cataluña para quien vive en Francia: para llevártelo a Francia o tenerlo aquí en verano. Impuestos, papeles y cómo comprar con tranquilidad.",
    eyebrow="Comprar barco · Si vives en Francia",
    h1="Barcos de ocasión en España, si vives en Francia",
    meta=["Por Juan Morante", "Actualizado octubre 2026"],
    lead="Estos son los barcos que gestiono ahora. Si vives en Francia, puedes comprar uno para llevártelo y matricularlo allí, o para tenerlo aquí y usarlo en verano. Debajo te explico lo básico de cada caso.",
    toc=[("barcos", "Barcos en venta"), ("llevar", "Para llevártelo a Francia"), ("aqui", "Para tenerlo en Cataluña"), ("como", "Cómo compramos"), ("faq", "Preguntas frecuentes")],
    body="""
<h2 id="barcos">Barcos en venta</h2>
<div class="pm-list" data-f='{}'></div>
<p class="pm-empty" hidden>Ahora mismo no tengo barcos disponibles. <a href="/alertas/">Crea una alerta</a> y te aviso en cuanto entre uno.</p>
<p class="note" style="font-family:var(--display);font-size:12.5px;color:var(--ink-2)">Todos los barcos que publico tienen el encargo de venta firmado por su propietario. <a href="/barcos/">Ver el catálogo completo con filtros</a>.</p>

<h2 id="llevar">Para llevártelo a Francia</h2>
<p>Si compras a un particular siendo no residente, en España se paga el ITP del <strong>4 %</strong> con el modelo 620; si compras a una empresa, IVA. Después se da de baja el barco en el registro español y se matricula en Francia con el <em>certificat d'enregistrement</em>. Un barco usado con el IVA europeo pagado no vuelve a pagar IVA en Francia. Lo tienes paso a paso en la <a href="/guias/comprar-barco-espana-matricular-francia.html">guía para comprar en España y matricular en Francia</a>.</p>

<h2 id="aqui">Para tenerlo en Cataluña</h2>
<p>Puedes dejarlo con bandera española a tu nombre, o traer tu barco francés y amarrarlo aquí sin trámites de entrada. Lo importante es que lo uses tú y personas que no vivan en España, tener un seguro de responsabilidad civil válido en España y el permiso adecuado. Lo explico en la <a href="/guias/barco-frances-en-cataluna.html">guía para tener tu barco en Cataluña</a>.</p>

<h2 id="como">Cómo compramos</h2>
<ol>
<li><strong>Me cuentas qué buscas</strong>: tipo de barco, eslora, presupuesto y si lo quieres llevar a Francia o tenerlo aquí.</li>
<li><strong>Reviso la documentación con el vendedor</strong>: titular, cargas, IVA, motores y bandera.</li>
<li><strong>Prueba de mar y peritaje</strong>, si quieres hacerlo, antes de dejar la señal.</li>
<li><strong>Contrato y papeles</strong>, con una gestoría náutica que haga el cambio de titular o la baja para Francia.</li>
</ol>
<p>Si el barco que buscas no está en la lista, <a href="/alertas/">crea una alerta</a> y te aviso cuando entre uno que encaje.</p>

<h2 id="faq">Preguntas frecuentes</h2>
<h3>¿Puedo comprar un barco en España viviendo en Francia?</h3><p>Sí. Necesitarás normalmente un NIE y, si compras a un particular, pagar el ITP del 4 % como no residente.</p>
<h3>¿Tengo que pagar el IVA otra vez en Francia?</h3><p>No, si es un barco usado con el IVA europeo pagado. Solo se paga en Francia si el barco cuenta como nuevo (más de 7,5 metros y menos de 3 meses o de 100 horas de uso).</p>
<h3>¿Puedo ver el barco antes de comprarlo?</h3><p>Claro. Lo recomendable es verlo, hacer una prueba de mar y, si quieres, un peritaje antes de dejar ninguna señal.</p>
""",
    faq=[("¿Puedo comprar un barco en España viviendo en Francia?", "Sí. Necesitarás normalmente un NIE y, si compras a un particular, pagar el ITP del 4 % como no residente."),
         ("¿Tengo que pagar el IVA otra vez en Francia?", "No, si es un barco usado con el IVA europeo pagado. Solo se paga en Francia si el barco cuenta como nuevo (más de 7,5 metros y menos de 3 meses o de 100 horas de uso)."),
         ("¿Puedo ver el barco antes de comprarlo?", "Claro. Lo recomendable es verlo, hacer una prueba de mar y, si quieres, un peritaje antes de dejar ninguna señal.")],
    note="Información fiscal orientativa, revisada en octubre de 2026. No es asesoramiento fiscal ni legal y la normativa puede cambiar. Confírmalo con una gestoría náutica o con la administración antes de comprar.",
    card=dict(eyebrow="¿Vives en Francia?", h3="Te ayudo a encontrar el barco.", p="Cuéntame qué buscas, tu presupuesto y si lo quieres llevar a Francia o tenerlo aquí.", wa="Hola Juan, vivo en Francia y busco un barco de ocasión en España.", btn="Hablar con Juan por WhatsApp"),
    rel=[("/guias/comprar-barco-espana-matricular-francia.html", "Comprar en España y matricular en Francia"), ("/guias/barco-frances-en-cataluna.html", "Tener tu barco en Cataluña si vives en Francia"), ("/comprar/barcos-segunda-mano-costa-brava.html", "Barcos de segunda mano en la Costa Brava")],
    header_wa="Hola Juan, vivo en Francia y busco un barco en España.",
)

# Textos sueltos: enlace en guías index, portada FR y fichas
INDEX_CARD = {
  "g1": dict(tag="Comprar desde Francia", h2="Comprar un barco en España y matricularlo en Francia", p="Impuestos en España, baja en el registro español, cómo llevarlo y qué papeles pide Francia."),
  "g2": dict(tag="Si vives en Francia", h2="Tener tu barco en Cataluña si vives en Francia", p="Bandera francesa o española, impuestos, seguro, permiso y amarres en la Costa Brava."),
}
