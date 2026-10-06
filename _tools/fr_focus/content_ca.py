# -*- coding: utf-8 -*-
# Contingut (CA) de les pàgines per a compradors francesos. Mateixa estructura que content_es.py.
FECHA = "octubre 2026"

PAGES = {}

PAGES["g1"] = dict(
    kind="guia",
    slug="guias/comprar-barco-espana-matricular-francia.html",
    crumb=("Guies", "/ca/guias/"),
    title="Comprar un vaixell a Espanya i matricular-lo a França: guia pas a pas",
    desc="Si vius a França i has trobat un vaixell a Espanya: quins impostos es paguen aquí, com es dona de baixa del registre espanyol, com portar-lo i quins papers demana França per matricular-lo.",
    eyebrow="Guies · Comprar des de França",
    h1="Comprar un vaixell a Espanya i matricular-lo a França",
    meta=["Per Juan Morante", "Actualitzat octubre 2026", "8 min de lectura"],
    lead="Cada vegada més gent que viu a França busca vaixell a Catalunya. La compra es pot fer sense problemes, però hi ha dos països i dues administracions pel mig, i convé fer les coses en ordre. Aquí t'explico el camí complet: el que es comprova abans de pagar, el que es paga a Espanya, com es dona de baixa el vaixell aquí i què demana França per matricular-lo.",
    toc=[("antes", "Abans de pagar: què comprovar"), ("impuestos", "Impostos a Espanya"), ("baja", "La baixa del registre espanyol"), ("llevarlo", "Com portar el vaixell a França"), ("francia", "Matricular-lo a França"), ("despues", "Després: taxa anual i permís"), ("riesgos", "Els riscos més habituals"), ("faq", "Preguntes freqüents")],
    body="""
<h2 id="antes">Abans de pagar: què comprovar</h2>
<p>El que dona més problemes en una compra entre dos països no és la paperassa, sinó descobrir tard que alguna cosa no quadra. Abans de deixar cap senyal, demana i revisa això:</p>
<ul>
<li><strong>Qui n'és el titular.</strong> Que qui et ven sigui el propietari que consta a la documentació del vaixell, o tingui poders per vendre'l.</li>
<li><strong>Càrregues.</strong> Que el vaixell no tingui hipoteques ni embargaments. Es comprova al Registre de Béns Mobles. Si tingués algun creditor, per donar de baixa el vaixell caldrà la seva autorització.</li>
<li><strong>L'IVA.</strong> Que el vaixell tingui l'IVA pagat a la Unió Europea. El normal és demanar la factura de la primera venda. Per matricular-lo a França te'l demanaran justificar, sobretot si fa més de 7,5 metres.</li>
<li><strong>La bandera actual.</strong> Si el vaixell té bandera espanyola, la baixa es demana a Espanya. Si té una altra bandera (per exemple, polonesa), la baixa es demana al registre d'aquell país, i és un tràmit diferent.</li>
<li><strong>Motors.</strong> Que els números de sèrie dels motors coincideixin amb els papers. França també demana la factura o el document de compra dels motors.</li>
<li><strong>Declaració de conformitat CE.</strong> França la demana per matricular. Els vaixells posats al mercat europeu abans del 16 de juny de 1998 no en tenen i es tramiten amb un altre document.</li>
</ul>
<p>El meu consell és fer la <strong>prova de mar i el peritatge abans de deixar la senyal</strong>, o deixar la senyal amb la condició que el peritatge surti bé. Ho tens explicat a la <a href="/ca/guias/arras-compraventa-barco.html">guia de les arres</a>.</p>

<h2 id="impuestos">Impostos a Espanya</h2>
<p>Depèn de qui et vengui el vaixell:</p>
<ul>
<li><strong>Si ven un particular</strong>, es paga l'impost de transmissions (ITP). Si no ets resident a Espanya, no es paga a Catalunya sinó a l'Agència Tributària de l'Estat: el tipus és el <strong>4 %</strong>, es declara amb el <strong>model 620</strong> per a no residents i hi ha <strong>30 dies hàbils</strong> des de la signatura del contracte. Es calcula sobre el preu o sobre el valor de taules d'Hisenda, si és més alt.</li>
<li><strong>Si ven una empresa</strong>, l'operació porta IVA en lloc d'ITP: en un vaixell usat, normalment l'IVA espanyol. Si el venedor aplica el règim especial de béns usats, l'IVA va inclòs al preu i no apareix desglossat; demana que la factura ho indiqui, perquè és la teva prova de l'IVA davant de França.</li>
<li><strong>Vaixell «nou»:</strong> si fa més de 7,5 metres i es lliura en els 3 mesos següents a la seva primera posada en servei o amb menys de 100 hores de navegació, per a la llei és un mitjà de transport nou i l'IVA es paga a França, no a Espanya.</li>
</ul>
<p>Per declarar i fer els tràmits a Espanya, normalment et demanaran un <strong>NIE</strong> (número d'identificació d'estranger). Convé demanar-lo amb temps.</p>
<p>Si compres sent resident a Espanya, l'ITP és el de la teva comunitat autònoma: el tens a la <a href="/ca/guias/itp-comprar-barco-usado-por-comunidad.html">guia de l'ITP per comunitats</a>.</p>

<h2 id="baja">La baixa del registre espanyol</h2>
<p>Per matricular el vaixell a França, primer ha de sortir del registre espanyol. Es demana a la <strong>Capitania Marítima</strong> com a <strong>baixa per exportació</strong> (definitiva o provisional), amb la sol·licitud d'esbarjo i la taxa corresponent (model 790-025). S'hi aporta el full d'assentament, el document de la compravenda, l'autorització dels creditors si n'hi ha i, si el vaixell té MMSI (el número de la ràdio), la declaració que s'ha desprogramat.</p>
<p>La llei diu que la baixa la demana el titular o algú autoritzat per ell. Per això és important deixar-ho pactat al contracte: que el venedor signi la sol·licitud o t'autoritzi a demanar-la. El certificat de baixa és un dels papers que et demanarà França.</p>

<h2 id="llevarlo">Com portar el vaixell a França</h2>
<p>Hi ha dues maneres:</p>
<ul>
<li><strong>Per carretera.</strong> Per a vaixells que caben en un remolc o en un camió. Per sobre de certes mides (a França, més de 2,55 m d'amplada) és un transport especial amb el seu permís. Ho resol l'empresa de transport.</li>
<li><strong>Navegant.</strong> Un vaixell donat de baixa es queda sense bandera, i sense bandera no es pot navegar. L'habitual és fer primer el canvi de titular a Espanya, anar navegant amb la bandera espanyola i demanar la baixa després. Per navegar per aigües espanyoles cal una assegurança de responsabilitat civil vàlida a Espanya. Confirma aquest ordre amb la gestoria abans de signar, perquè depèn de cada cas.</li>
</ul>

<h2 id="francia">Matricular-lo a França</h2>
<p>Des del 2022, a França l'antiga francisation i la matrícula s'han unit en un únic tràmit: el <strong>certificat d'enregistrement</strong>. El porta l'administració marítima (les DDTM i DML, segons el port base). El portal <em>demarches-plaisance.gouv.fr</em> serveix per a vaixells nous i per a vendes entre particulars de vaixells que ja són francesos; un vaixell que ve d'un registre estranger es tramita amb la DDTM.</p>
<p>Els papers que solen demanar:</p>
<ul>
<li>Factura o contracte de compravenda del vaixell i dels motors.</li>
<li>Declaració de conformitat CE (o el document equivalent per a vaixells anteriors a juny de 1998).</li>
<li>Justificant de la situació de l'IVA, si el vaixell es va comprar en un altre país de la UE.</li>
<li>Certificat de baixa del registre anterior.</li>
<li>Document d'identitat i justificant de domicili a França.</li>
<li>La fitxa de sol·licitud (<em>fiche plaisance</em>).</li>
</ul>
<p>Per matricular a França, almenys el 50 % del vaixell ha de ser d'un ciutadà de la UE i et demanaran un domicili a França.</p>

<h2 id="despues">Després: taxa anual i permís</h2>
<p>A França, els vaixells de <strong>7 metres o més</strong>, i els de menys de 7 metres amb un motor de 22 CV fiscals o més, paguen una taxa anual (l'antiga DAFN). La part del buc va d'uns <strong>77 € per a 7-8 metres</strong> a 886 € a partir de 15 metres, més una part per la potència del motor, amb rebaixes per a vaixells antics. Es paga en línia. França ha aprovat canviar el càlcul a partir del 2027.</p>
<p>Per governar un vaixell francès amb motor de més de 4,5 kW (6 CV) necessites el <strong>permis plaisance</strong>: l'opció costanera permet allunyar-te fins a 6 milles d'un refugi.</p>

<h2 id="riesgos">Els riscos més habituals</h2>
<div class="tbl"><table><thead><tr><th>Risc</th><th>Com evitar-lo</th></tr></thead><tbody>
<tr><td>Vaixell amb hipoteca o embargament</td><td>Demanar la nota del Registre de Béns Mobles abans de pagar</td></tr>
<tr><td>IVA sense justificar</td><td>Factura de primera venda o factura del venedor professional que ho indiqui</td></tr>
<tr><td>Bandera d'un altre país (polonesa o una altra)</td><td>Saber on es demana la baixa abans de comprar</td></tr>
<tr><td>Motors que no quadren amb els papers</td><td>Comprovar els números de sèrie i demanar-ne les factures</td></tr>
<tr><td>Vaixell «gairebé nou» facturat amb IVA espanyol</td><td>Si és mitjà de transport nou, l'IVA va a França</td></tr>
<tr><td>ITP sense pagar</td><td>Model 620 en 30 dies hàbils; sense ell es complica el canvi de titular</td></tr>
</tbody></table></div>

<h2 id="ayuda">Com et puc ajudar</h2>
<p>Soc broker nàutic a Catalunya: poso en contacte qui ven el seu vaixell amb qui el compra. T'ajudo a trobar el vaixell, reviso amb el venedor la documentació (titular, càrregues, IVA, motors, bandera) i t'acompanyo a la prova de mar i al peritatge si el vols fer. Els tràmits de la baixa a Espanya i de la matrícula a França els fa una gestoria nàutica; al <a href="/ca/servicios/directorio.html">directori d'empreses</a> tens gestories per zona.</p>

<h2 id="faq">Preguntes freqüents</h2>
<h3>Pago impostos a Espanya i un altre cop a França?</h3><p>Si compres un vaixell usat amb l'IVA europeu pagat, no es torna a pagar IVA a França. A Espanya pagues l'ITP del 4 % si compres a un particular, o l'IVA si compres a una empresa. Després, a França, la taxa anual si el vaixell hi està obligat.</p>
<h3>Puc tornar navegant amb el vaixell?</h3><p>Sí, però no amb el vaixell ja donat de baixa, perquè es queda sense bandera. L'habitual és fer primer el canvi de titular a Espanya, navegar amb bandera espanyola i demanar la baixa després. Confirma-ho amb la gestoria.</p>
<h3>Necessito NIE?</h3><p>Normalment sí, per declarar l'impost i fer el canvi de titular. Convé demanar-lo amb temps.</p>
<h3>Quant costa la taxa anual a França?</h3><p>Els vaixells de menys de 7 metres amb poca potència no la paguen. Per a un vaixell de 7 a 8 metres, la part del buc són uns 77 € l'any, més una part segons la potència del motor.</p>
""",
    faq=[("Pago impostos a Espanya i un altre cop a França?", "Si compres un vaixell usat amb l'IVA europeu pagat, no es torna a pagar IVA a França. A Espanya pagues l'ITP del 4 % si compres a un particular, o l'IVA si compres a una empresa. Després, a França, la taxa anual si el vaixell hi està obligat."),
         ("Puc tornar navegant amb el vaixell?", "Sí, però no amb el vaixell ja donat de baixa, perquè es queda sense bandera. L'habitual és fer primer el canvi de titular a Espanya, navegar amb bandera espanyola i demanar la baixa després. Confirma-ho amb la gestoria."),
         ("Necessito NIE?", "Normalment sí, per declarar l'impost i fer el canvi de titular. Convé demanar-lo amb temps."),
         ("Quant costa la taxa anual a França?", "Els vaixells de menys de 7 metres amb poca potència no la paguen. Per a un vaixell de 7 a 8 metres, la part del buc són uns 77 € l'any, més una part segons la potència del motor.")],
    note="Informació orientativa, revisada l'octubre de 2026 segons la normativa espanyola (Texto refundido del ITP, arts. 6, 8 i 11; RD 1027/1989; RD 1435/2010; RD 607/1999) i la informació oficial francesa (mer.gouv.fr, service-public.fr, douane.gouv.fr, BOFiP). No és assessorament fiscal ni legal i la normativa pot canviar. Cada cas depèn del vaixell i de la teva situació: confirma-ho amb una gestoria nàutica o amb l'administració abans de comprar.",
    card=dict(eyebrow="Vius a França?", h3="T'ajudo a trobar el vaixell a Catalunya.", p="Explica'm què busques i on el faràs servir, i et dic quins vaixells encaixen i quins papers cal revisar.", wa="Hola Juan, visc a França i busco un vaixell a Espanya.", btn="Parlar amb Juan per WhatsApp"),
    rel=[("/ca/comprar/barcos-ocasion-espana-compradores-franceses.html", "Vaixells d'ocasió a Espanya per a compradors francesos"), ("/ca/guias/barco-frances-en-cataluna.html", "Tenir el teu vaixell a Catalunya si vius a França"), ("/ca/guias/itp-comprar-barco-usado-por-comunidad.html", "ITP en comprar un vaixell usat")],
    header_wa="Hola Juan, visc a França i tinc un dubte sobre comprar un vaixell a Espanya.",
)

PAGES["g2"] = dict(
    kind="guia",
    slug="guias/barco-frances-en-cataluna.html",
    crumb=("Guies", "/ca/guias/"),
    title="Tenir el teu vaixell a Catalunya si vius a França: amarrador, impostos i permís",
    desc="Si estiueges a Catalunya i vols tenir el vaixell aquí: portar el teu vaixell francès o comprar-ne un a Espanya, quins impostos i assegurances s'apliquen, quin permís necessites i com funcionen els amarradors a la Costa Brava.",
    eyebrow="Guies · Si vius a França",
    h1="Tenir el teu vaixell a Catalunya si vius a França",
    meta=["Per Juan Morante", "Actualitzat octubre 2026", "7 min de lectura"],
    lead="Si passes els estius a la Costa Brava o en un altre punt de Catalunya, tenir el vaixell aquí t'estalvia el viatge de cada any. Hi ha dos camins: portar el teu vaixell amb bandera francesa o comprar-ne un aquí. Tots dos funcionen, però cadascun té les seves regles. Te les resumeixo.",
    toc=[("dos", "Dos camins"), ("frances", "Portar el teu vaixell amb bandera francesa"), ("espanol", "Comprar aquí i deixar-lo amb bandera espanyola"), ("permiso", "Quin permís necessites"), ("amarre", "Amarrador i hivernada"), ("faq", "Preguntes freqüents")],
    body="""
<h2 id="dos">Dos camins</h2>
<ul>
<li><strong>Portar el teu vaixell francès</strong> i deixar-lo amarrat aquí amb la seva bandera.</li>
<li><strong>Comprar un vaixell a Espanya</strong> i, o bé portar-lo a França (ho tens a la <a href="/ca/guias/comprar-barco-espana-matricular-francia.html">guia per matricular-lo a França</a>), o bé deixar-lo aquí amb bandera espanyola.</li>
</ul>

<h2 id="frances">Portar el teu vaixell amb bandera francesa</h2>
<p>França i Espanya són de la Unió Europea, així que un vaixell francès amb l'IVA europeu pagat pot estar en un port català <strong>sense tràmits d'entrada</strong> ni duana. Et convé portar a bord els papers del vaixell i el justificant de l'IVA.</p>
<p>No hi ha un termini màxim d'estada mentre el vaixell el facis servir tu i persones que tampoc viuen a Espanya. El punt delicat és <strong>qui el fa servir</strong>: la llei espanyola obliga a matricular a Espanya els vaixells que fan servir aquí persones residents a Espanya, i a pagar l'impost de matriculació (el 12 % en vaixells de més de 8 metres). Hisenda ha dit en consultes recents que les entrades repetides d'un vaixell estranger usat per un resident es consideren ús habitual. A la pràctica: si el deixes a familiars, amics o a un patró que viu a Espanya, pot aparèixer aquesta obligació. Ho expliquem a la <a href="/ca/guias/impuesto-matriculacion-barcos.html">guia de l'impost de matriculació</a>.</p>
<p>Dues coses més:</p>
<ul>
<li><strong>Assegurança.</strong> En aigües espanyoles és obligatòria una assegurança de responsabilitat civil, també per a vaixells estrangers. Comprova que la teva pòlissa francesa cobreix Espanya.</li>
<li><strong>La taxa anual francesa</strong> es continua pagant a França encara que el vaixell sigui aquí. A Espanya pagaràs l'amarrador i els serveis del port.</li>
</ul>

<h2 id="espanol">Comprar aquí i deixar-lo amb bandera espanyola</h2>
<p>Un no resident pot tenir un vaixell amb bandera espanyola a nom seu. El que et trobaràs:</p>
<ul>
<li><strong>Impost de la compra.</strong> Si compres a un particular sent no resident, l'ITP és el <strong>4 %</strong>, amb el model 620 de l'Agència Tributària de l'Estat i 30 dies hàbils de termini. Si compres a una empresa, IVA.</li>
<li><strong>NIE.</strong> Normalment te'l demanaran per declarar i fer el canvi de titular.</li>
<li><strong>ITB.</strong> La inspecció tècnica: en els vaixells d'esbarjo de 6 a 24 metres, com a màxim cada 5 anys. Els de menys de 6 metres no tenen inspeccions periòdiques.</li>
<li><strong>Assegurança de responsabilitat civil</strong> obligatòria.</li>
<li><strong>Compte a França:</strong> si vius a França i navegues per aigües franceses amb un vaixell de bandera estrangera, França et pot cobrar un impost equivalent a la seva taxa anual (el <em>droit de passeport</em>). Si el vaixell es queda a Espanya, no t'afecta.</li>
</ul>

<h2 id="permiso">Quin permís necessites</h2>
<ul>
<li><strong>Vaixell amb bandera francesa:</strong> s'aplica la normativa francesa també a Espanya. Amb el teu <em>permis plaisance</em> el pots governar dins dels seus límits (l'opció costanera, fins a 6 milles d'un refugi).</li>
<li><strong>Vaixell amb bandera espanyola:</strong> com a ciutadà europeu amb un títol del teu país, la Capitania Marítima et pot autoritzar a governar-lo. És un tràmit que convé fer abans de la temporada. Tens les titulacions espanyoles a <a href="/ca/titulaciones/">titulacions</a>.</li>
</ul>

<h2 id="amarre">Amarrador i hivernada</h2>
<p>A la Costa Brava, la majoria de ports els gestionen clubs nàutics o empreses concessionàries. A prop de la frontera tens Portbou, Colera, Llançà, El Port de la Selva, Roses, Empuriabrava, L'Escala, L'Estartit i, més al sud, Palamós.</p>
<ul>
<li><strong>Anual o per temporada.</strong> L'amarrador anual surt més barat per mes, però a l'estiu el de lloguer escasseja i als ports petits hi ha llista d'espera. Com a referència, les tarifes oficials 2026 del port de Portbou per a un vaixell de 7,5 a 8,5 metres són uns 3.445 € l'any, o uns 1.045 € per un mes de juliol o agost.</li>
<li><strong>Hivernada en sec.</strong> Per a vaixells de fins a 7-8 metres, la marina seca o l'escar solen sortir més barats que l'aigua, i el vaixell passa l'hivern protegit.</li>
<li><strong>Manteniment quan no hi ets.</strong> És el que més preocupa a qui viu lluny: algú que revisi amarres, bateries i sentines. A <a href="/ca/servicios/">serveis</a> tens empreses de manteniment i escars.</li>
</ul>
<p>Tens més preus i tipus d'amarrador a la <a href="/ca/guias/amarres-cataluna-tipos-precios-alquiler-compra.html">guia d'amarradors a Catalunya</a>.</p>

<h2 id="ayuda">Com et puc ajudar</h2>
<p>Si busques vaixell per tenir-lo aquí, t'ajudo a trobar-lo i reviso amb el venedor la documentació. I si el vaixell es ven amb amarrador que es pot traspassar, ho indico a la fitxa.</p>

<h2 id="faq">Preguntes freqüents</h2>
<h3>Puc deixar el meu vaixell francès tot l'any a Catalunya?</h3><p>Sí. Com que és un vaixell de la Unió Europea amb l'IVA pagat, no hi ha termini màxim mentre el facis servir tu i altres persones que no visquin a Espanya.</p>
<h3>Puc deixar el vaixell a un amic que viu a Espanya?</h3><p>Amb compte: si el fan servir residents a Espanya, la llei pot obligar a matricular-lo aquí i a pagar l'impost de matriculació. Consulta-ho abans amb una gestoria.</p>
<h3>Em serveix el meu permis plaisance a Espanya?</h3><p>Per a un vaixell amb bandera francesa, sí, dins dels seus límits. Per a un vaixell amb bandera espanyola necessites una autorització de la Capitania Marítima.</p>
<h3>És obligatòria l'assegurança?</h3><p>En aigües espanyoles, sí: una assegurança de responsabilitat civil, també per a vaixells amb bandera estrangera.</p>
""",
    faq=[("Puc deixar el meu vaixell francès tot l'any a Catalunya?", "Sí. Com que és un vaixell de la Unió Europea amb l'IVA pagat, no hi ha termini màxim mentre el facis servir tu i altres persones que no visquin a Espanya."),
         ("Puc deixar el vaixell a un amic que viu a Espanya?", "Amb compte: si el fan servir residents a Espanya, la llei pot obligar a matricular-lo aquí i a pagar l'impost de matriculació. Consulta-ho abans amb una gestoria."),
         ("Em serveix el meu permis plaisance a Espanya?", "Per a un vaixell amb bandera francesa, sí, dins dels seus límits. Per a un vaixell amb bandera espanyola necessites una autorització de la Capitania Marítima."),
         ("És obligatòria l'assegurança?", "En aigües espanyoles, sí: una assegurança de responsabilitat civil, també per a vaixells amb bandera estrangera.")],
    note="Informació orientativa, revisada l'octubre de 2026 segons la normativa espanyola (Ley 38/1992, disposició addicional 1a i art. 65; consulta DGT V0820-25; RD 875/2014; RD 1434/1999; RD 607/1999; Texto refundido del ITP) i la informació oficial francesa (mer.gouv.fr, douane.gouv.fr). Els preus d'amarrador són les tarifes publicades pel port de Portbou per al 2026 i poden canviar. No és assessorament fiscal ni legal: confirma-ho amb una gestoria nàutica o amb l'administració.",
    card=dict(eyebrow="Estiueges a Catalunya?", h3="T'ajudo a tenir el teu vaixell aquí.", p="Explica'm on passes l'estiu i quin vaixell busques, i et dic què encaixa.", wa="Hola Juan, estiuejo a Catalunya i vull tenir un vaixell aquí.", btn="Parlar amb Juan per WhatsApp"),
    rel=[("/ca/comprar/barcos-ocasion-espana-compradores-franceses.html", "Vaixells d'ocasió a Espanya per a compradors francesos"), ("/ca/guias/comprar-barco-espana-matricular-francia.html", "Comprar a Espanya i matricular a França"), ("/ca/guias/amarres-cataluna-tipos-precios-alquiler-compra.html", "Amarradors a Catalunya: tipus i preus")],
    header_wa="Hola Juan, estiuejo a Catalunya i tinc un dubte sobre tenir el vaixell aquí.",
)

PAGES["l4"] = dict(
    kind="landing",
    slug="comprar/barcos-ocasion-espana-compradores-franceses.html",
    crumb=("Comprar vaixell", "/ca/comprar/"),
    title="Vaixells d'ocasió a Espanya per a compradors que viuen a França",
    desc="Vaixells de segona mà en venda a Catalunya per a qui viu a França: per endur-te'l a França o tenir-lo aquí a l'estiu. Impostos, papers i com comprar amb tranquil·litat.",
    eyebrow="Comprar vaixell · Si vius a França",
    h1="Vaixells d'ocasió a Espanya, si vius a França",
    meta=["Per Juan Morante", "Actualitzat octubre 2026"],
    lead="Aquests són els vaixells que gestiono ara. Si vius a França, en pots comprar un per endur-te'l i matricular-lo allà, o per tenir-lo aquí i fer-lo servir a l'estiu. A sota t'explico el bàsic de cada cas.",
    toc=[("barcos", "Vaixells en venda"), ("llevar", "Per endur-te'l a França"), ("aqui", "Per tenir-lo a Catalunya"), ("como", "Com comprem"), ("faq", "Preguntes freqüents")],
    body="""
<h2 id="barcos">Vaixells en venda</h2>
<div class="pm-list" data-f='{}'></div>
<p class="pm-empty" hidden>Ara mateix no tinc vaixells disponibles. <a href="/ca/alertas/">Crea una alerta</a> i t'aviso tan bon punt n'entri un.</p>
<p class="note" style="font-family:var(--display);font-size:12.5px;color:var(--ink-2)">Tots els vaixells que publico tenen l'encàrrec de venda signat pel seu propietari. <a href="/ca/barcos/">Veure el catàleg complet amb filtres</a>.</p>

<h2 id="llevar">Per endur-te'l a França</h2>
<p>Si compres a un particular sent no resident, a Espanya es paga l'ITP del <strong>4 %</strong> amb el model 620; si compres a una empresa, IVA. Després es dona de baixa el vaixell del registre espanyol i es matricula a França amb el <em>certificat d'enregistrement</em>. Un vaixell usat amb l'IVA europeu pagat no torna a pagar IVA a França. Ho tens pas a pas a la <a href="/ca/guias/comprar-barco-espana-matricular-francia.html">guia per comprar a Espanya i matricular a França</a>.</p>

<h2 id="aqui">Per tenir-lo a Catalunya</h2>
<p>El pots deixar amb bandera espanyola a nom teu, o portar el teu vaixell francès i amarrar-lo aquí sense tràmits d'entrada. El més important és que el facis servir tu i persones que no visquin a Espanya, tenir una assegurança de responsabilitat civil vàlida a Espanya i el permís adequat. Ho explico a la <a href="/ca/guias/barco-frances-en-cataluna.html">guia per tenir el teu vaixell a Catalunya</a>.</p>

<h2 id="como">Com comprem</h2>
<ol>
<li><strong>M'expliques què busques</strong>: tipus de vaixell, eslora, pressupost i si el vols portar a França o tenir-lo aquí.</li>
<li><strong>Reviso la documentació amb el venedor</strong>: titular, càrregues, IVA, motors i bandera.</li>
<li><strong>Prova de mar i peritatge</strong>, si el vols fer, abans de deixar la senyal.</li>
<li><strong>Contracte i papers</strong>, amb una gestoria nàutica que faci el canvi de titular o la baixa per a França.</li>
</ol>
<p>Si el vaixell que busques no és a la llista, <a href="/ca/alertas/">crea una alerta</a> i t'aviso quan n'entri un que encaixi.</p>

<h2 id="faq">Preguntes freqüents</h2>
<h3>Puc comprar un vaixell a Espanya vivint a França?</h3><p>Sí. Normalment necessitaràs un NIE i, si compres a un particular, pagar l'ITP del 4 % com a no resident.</p>
<h3>He de pagar l'IVA un altre cop a França?</h3><p>No, si és un vaixell usat amb l'IVA europeu pagat. Només es paga a França si el vaixell compta com a nou (més de 7,5 metres i menys de 3 mesos o de 100 hores d'ús).</p>
<h3>Puc veure el vaixell abans de comprar-lo?</h3><p>És clar. El recomanable és veure'l, fer una prova de mar i, si vols, un peritatge abans de deixar cap senyal.</p>
""",
    faq=[("Puc comprar un vaixell a Espanya vivint a França?", "Sí. Normalment necessitaràs un NIE i, si compres a un particular, pagar l'ITP del 4 % com a no resident."),
         ("He de pagar l'IVA un altre cop a França?", "No, si és un vaixell usat amb l'IVA europeu pagat. Només es paga a França si el vaixell compta com a nou (més de 7,5 metres i menys de 3 mesos o de 100 hores d'ús)."),
         ("Puc veure el vaixell abans de comprar-lo?", "És clar. El recomanable és veure'l, fer una prova de mar i, si vols, un peritatge abans de deixar cap senyal.")],
    note="Informació fiscal orientativa, revisada l'octubre de 2026. No és assessorament fiscal ni legal i la normativa pot canviar. Confirma-ho amb una gestoria nàutica o amb l'administració abans de comprar.",
    card=dict(eyebrow="Vius a França?", h3="T'ajudo a trobar el vaixell.", p="Explica'm què busques, el teu pressupost i si el vols portar a França o tenir-lo aquí.", wa="Hola Juan, visc a França i busco un vaixell d'ocasió a Espanya.", btn="Parlar amb Juan per WhatsApp"),
    rel=[("/ca/guias/comprar-barco-espana-matricular-francia.html", "Comprar a Espanya i matricular a França"), ("/ca/guias/barco-frances-en-cataluna.html", "Tenir el teu vaixell a Catalunya si vius a França"), ("/ca/comprar/barcos-segunda-mano-costa-brava.html", "Vaixells de segona mà a la Costa Brava")],
    header_wa="Hola Juan, visc a França i busco un vaixell a Espanya.",
)

# Textos solts: enllaç a l'índex de guies, portada FR i fitxes
INDEX_CARD = {
  "g1": dict(tag="Comprar des de França", h2="Comprar un vaixell a Espanya i matricular-lo a França", p="Impostos a Espanya, baixa del registre espanyol, com portar-lo i quins papers demana França."),
  "g2": dict(tag="Si vius a França", h2="Tenir el teu vaixell a Catalunya si vius a França", p="Bandera francesa o espanyola, impostos, assegurança, permís i amarradors a la Costa Brava."),
}
