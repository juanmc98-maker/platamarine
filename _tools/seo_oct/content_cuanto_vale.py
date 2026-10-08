# -*- coding: utf-8 -*-
"""Contenido de /cuanto-vale-mi-barco/ en 4 idiomas (la lógica está en /cuanto-vale-mi-barco/calc.js)."""
import json

CSS = '''<style>
.cv{margin-top:20px!important;background:#fff;border:1px solid var(--plata);border-radius:8px;padding:20px 22px;margin:0 0 22px}
.cv label.f{display:block;font-family:var(--display);font-weight:600;font-size:14px;margin:14px 0 6px}
.cv select,.cv input[type=text],.cv input[type=number]{width:100%;font:16px var(--serif);padding:10px 12px;border:1px solid var(--plata-2);border-radius:6px;box-sizing:border-box;background:#fff}
.cv .row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.cv .opt{display:flex;gap:10px;align-items:flex-start;padding:7px 8px;border-radius:6px;cursor:pointer;font-size:15.5px;line-height:1.35}
.cv .opt input{margin-top:4px;flex:none}
.cv .btn{margin-top:16px;cursor:pointer}
.cv .err{font-family:var(--display);font-size:14px;color:#c0392b;margin:10px 0 0;min-height:1em}
.cv-res{background:var(--sea-deep);color:#D5DDE2;padding:22px 24px;border-radius:6px;margin:0 0 22px}
.cv-res h2{color:#fff;font-size:1.35rem;margin:0 0 8px}
.cv-res a{color:#fff}
.cv-res .cv-big{font-family:var(--display);font-size:2rem;font-weight:700;color:#fff;margin:4px 0 12px;line-height:1.15}
.cv-res .cv-nota{font-size:13px;color:#B7C3CB}
@media(max-width:560px){.cv .row{grid-template-columns:1fr}.cv-res .cv-big{font-size:1.6rem}}
</style>'''

def form(t):
    return '''<div class="cv" id="pmCalc" data-lang="%(lang)s"><form id="cvForm" onsubmit="return false" novalidate>
<label class="f" for="cvModelo">%(lModelo)s</label>
<select id="cvModelo"><option value="">%(elige)s</option></select>
<div id="cvOtro" hidden>
<div class="row"><div><label class="f" for="cvTipo">%(lTipo)s</label><select id="cvTipo">%(tipos)s</select></div>
<div><label class="f" for="cvEslora">%(lEslora)s</label><input type="text" id="cvEslora" inputmode="decimal" placeholder="7,5"></div></div>
<label class="f" for="cvMarca">%(lMarca)s</label><input type="text" id="cvMarca" maxlength="60" placeholder="%(phMarca)s">
</div>
<div class="row"><div><label class="f" for="cvAnio">%(lAnio)s</label><input type="number" id="cvAnio" min="1960" max="2026" inputmode="numeric" placeholder="2018"></div>
<div><label class="f" for="cvHoras">%(lHoras)s</label><select id="cvHoras"><option value="normales">%(hN)s</option><option value="altas">%(hA)s</option><option value="nose">%(hX)s</option></select></div></div>
<p class="f" style="font-family:var(--display);font-weight:600;font-size:14px;margin:14px 0 6px">%(lEstado)s</p>
<label class="opt"><input type="radio" name="cvEst" value="top"> <span>%(eTop)s</span></label>
<label class="opt"><input type="radio" name="cvEst" value="normal"> <span>%(eNormal)s</span></label>
<label class="opt"><input type="radio" name="cvEst" value="obra"> <span>%(eObra)s</span></label>
<button type="button" class="btn btn-wa" id="cvBtn">%(boton)s</button>
<p class="err" id="cvErr" role="alert"></p>
</form></div>
<div class="cv-res" id="cvRes" hidden aria-live="polite"></div>
<script type="application/json" id="pmCalcI18n">%(i18n)s</script>''' % dict(t, tipos=''.join('<option value="%s">%s</option>' % x for x in t['tiposL']),
                                                                    i18n=json.dumps(t['js'], ensure_ascii=False))

T = {}
T['es'] = dict(lang='es', lModelo='Modelo de tu barco', elige='Elige tu modelo…', lTipo='Tipo de barco', lEslora='Eslora (m)', lMarca='Marca y modelo',
  phMarca='Ej. Sessa Key Largo 24', lAnio='Año', lHoras='Horas de motor', hN='Normales para su edad', hA='Más altas de lo normal', hX='No lo sé',
  lEstado='¿Cómo está?', eTop='Muy cuidado y con el mantenimiento al día (con facturas)', eNormal='Normal para su edad', eObra='Necesita trabajos (motor, tapicería, gelcoat…)',
  boton='Ver precio orientativo',
  tiposL=[('open', 'Open / consola central'), ('sundeck', 'Sundeck o bowrider'), ('wa', 'Walkaround'), ('pilot', 'Pilothouse (tipo pesca-paseo)'), ('cruiser', 'Cabinado / cruiser'), ('otro', 'Otro (velero, semirrígida, fly…)')],
  js=dict(otro='Mi modelo no está en la lista', errModelo='Elige tu modelo (o «Mi modelo no está en la lista»).', errAnio='Pon el año del barco.', errEstado='Marca cómo está el barco.',
    miBarco='tu barco', sinDatosT='{n}: lo valoro a mano',
    sinDatos='De tu modelo todavía no tengo suficientes anuncios comparables para darte un rango fiable, y prefiero no inventármelo. Mándame los datos y te digo lo que veo en el mercado, gratis.',
    refTipo='Como referencia muy general, los modelos de este tipo que sigo cada mes se anuncian entre {a} y {b}, según modelo, año y motor.',
    sinAnioT='{n} de {y}: lo valoro a mano', sinAnio='Para ese año no tengo anuncios comparables suficientes de este modelo. Mándame los datos y te digo qué veo en el mercado.',
    desde='Desde', pocos='De estos años hay pocas unidades a la venta y los precios varían mucho según motor y equipo: conviene verlo caso a caso.',
    contexto='Los {y0}-{y1} de este modelo se anuncian entre {a} y {b}. Tu rango sale de colocar tu barco dentro de esa horquilla según el estado y las horas.',
    obra='Si los trabajos son importantes (motor, estructura), el precio puede quedar por debajo de este rango.',
    horas='Con muchas horas, un historial de mantenimiento con facturas y una revisión reciente del motor ayudan a defender el precio.',
    verModelo='Ver precios por años y qué mirar en el {n}',
    nota='Precio orientativo de anuncio a partir de anuncios públicos revisados cada mes. No es una tasación ni una oferta de compra; el precio final de venta suele quedar algo por debajo tras la negociación.',
    cta='Pedir a Juan una valoración personal', waModelo='Hola Juan, he usado la calculadora de la web. Tengo un {n} de {y} y me gustaría una valoración.',
    waOtro='Hola Juan, he usado la calculadora de la web. Tengo un {n} de {y}, eslora {e} m, y me gustaría una valoración.'))
T['ca'] = dict(lang='ca', lModelo='Model del teu vaixell', elige='Tria el teu model…', lTipo='Tipus de vaixell', lEslora='Eslora (m)', lMarca='Marca i model',
  phMarca='Ex. Sessa Key Largo 24', lAnio='Any', lHoras='Hores de motor', hN='Normals per a la seva edat', hA='Més altes del normal', hX='No ho sé',
  lEstado='Com està?', eTop='Molt cuidat i amb el manteniment al dia (amb factures)', eNormal='Normal per a la seva edat', eObra='Necessita feines (motor, tapisseria, gelcoat…)',
  boton='Veure preu orientatiu',
  tiposL=[('open', 'Open / consola central'), ('sundeck', 'Sundeck o bowrider'), ('wa', 'Walkaround'), ('pilot', 'Pilothouse (tipus pesca-passeig)'), ('cruiser', 'Cabinat / cruiser'), ('otro', 'Un altre (veler, semirígida, fly…)')],
  js=dict(otro='El meu model no és a la llista', errModelo='Tria el teu model (o «El meu model no és a la llista»).', errAnio="Posa l'any del vaixell.", errEstado='Marca com està el vaixell.',
    miBarco='el teu vaixell', sinDatosT="{n}: el valoro a mà",
    sinDatos="Del teu model encara no tinc prou anuncis comparables per donar-te un rang fiable, i prefereixo no inventar-me'l. Envia'm les dades i et dic què veig al mercat, gratis.",
    refTipo="Com a referència molt general, els models d'aquest tipus que segueixo cada mes s'anuncien entre {a} i {b}, segons model, any i motor.",
    sinAnioT='{n} de {y}: el valoro a mà', sinAnio="Per a aquest any no tinc prou anuncis comparables d'aquest model. Envia'm les dades i et dic què veig al mercat.",
    desde='Des de', pocos="D'aquests anys hi ha poques unitats a la venda i els preus varien molt segons motor i equip: convé mirar-ho cas per cas.",
    contexto="Els {y0}-{y1} d'aquest model s'anuncien entre {a} i {b}. El teu rang surt de situar el teu vaixell dins d'aquesta forquilla segons l'estat i les hores.",
    obra='Si les feines són importants (motor, estructura), el preu pot quedar per sota d’aquest rang.',
    horas='Amb moltes hores, un historial de manteniment amb factures i una revisió recent del motor ajuden a defensar el preu.',
    verModelo='Veure preus per anys i què mirar en el {n}',
    nota="Preu orientatiu d'anunci a partir d'anuncis públics revisats cada mes. No és una taxació ni una oferta de compra; el preu final de venda sol quedar una mica per sota després de la negociació.",
    cta='Demanar a Juan una valoració personal', waModelo='Hola Juan, he fet servir la calculadora del web. Tinc un {n} de {y} i m’agradaria una valoració.',
    waOtro='Hola Juan, he fet servir la calculadora del web. Tinc un {n} de {y}, eslora {e} m, i m’agradaria una valoració.'))
T['en'] = dict(lang='en', lModelo='Your boat model', elige='Choose your model…', lTipo='Boat type', lEslora='Length (m)', lMarca='Make and model',
  phMarca='E.g. Sessa Key Largo 24', lAnio='Year', lHoras='Engine hours', hN='Normal for its age', hA='Higher than usual', hX="I don't know",
  lEstado='What condition is it in?', eTop='Very well kept, maintenance up to date (with invoices)', eNormal='Normal for its age', eObra='Needs work (engine, upholstery, gelcoat…)',
  boton='See guide price',
  tiposL=[('open', 'Open / centre console'), ('sundeck', 'Sundeck or bowrider'), ('wa', 'Walkaround'), ('pilot', 'Pilothouse (fishing/cruising)'), ('cruiser', 'Cabin cruiser'), ('otro', 'Other (sailboat, RIB, flybridge…)')],
  js=dict(otro="My model isn't on the list", errModelo="Choose your model (or “My model isn't on the list”).", errAnio="Enter the boat's year.", errEstado="Tell me what condition it's in.",
    miBarco='your boat', sinDatosT='{n}: I value it by hand',
    sinDatos="I don't yet have enough comparable listings for your model to give you a reliable range, and I'd rather not make one up. Send me the details and I'll tell you what I see on the market, free of charge.",
    refTipo='As a very general reference, the models of this type that I track each month are listed between {a} and {b}, depending on model, year and engine.',
    sinAnioT='{n} from {y}: I value it by hand', sinAnio="For that year I don't have enough comparable listings of this model. Send me the details and I'll tell you what I see on the market.",
    desde='From', pocos='Few boats from these years are for sale and prices vary a lot with engine and equipment: it is best looked at case by case.',
    contexto='{y0}-{y1} boats of this model are listed between {a} and {b}. Your range places your boat inside that bracket according to condition and hours.',
    obra='If the work needed is major (engine, structure), the price may fall below this range.',
    horas='With high hours, a maintenance record with invoices and a recent engine service help to defend the price.',
    verModelo='See prices by year and what to check on the {n}',
    nota='Guide asking price based on public listings reviewed every month. This is not a valuation report or an offer to buy; the final sale price is usually somewhat lower after negotiation.',
    cta='Ask Juan for a personal valuation', waModelo="Hi Juan, I've used the calculator on your website. I have a {n} from {y} and would like a valuation.",
    waOtro="Hi Juan, I've used the calculator on your website. I have a {n} from {y}, {e} m long, and would like a valuation."))
T['fr'] = dict(lang='fr', lModelo='Modèle de votre bateau', elige='Choisissez votre modèle…', lTipo='Type de bateau', lEslora='Longueur (m)', lMarca='Marque et modèle',
  phMarca='Ex. Sessa Key Largo 24', lAnio='Année', lHoras='Heures moteur', hN='Normales pour son âge', hA='Plus élevées que la normale', hX='Je ne sais pas',
  lEstado='Dans quel état est-il ?', eTop='Très soigné, entretien à jour (avec factures)', eNormal='Normal pour son âge', eObra='Travaux à prévoir (moteur, sellerie, gelcoat…)',
  boton='Voir le prix indicatif',
  tiposL=[('open', 'Open / console centrale'), ('sundeck', 'Sundeck ou bowrider'), ('wa', 'Walkaround'), ('pilot', 'Pilothouse (pêche-promenade)'), ('cruiser', 'Cabine / cruiser'), ('otro', 'Autre (voilier, semi-rigide, fly…)')],
  js=dict(otro="Mon modèle n'est pas dans la liste", errModelo="Choisissez votre modèle (ou « Mon modèle n'est pas dans la liste »).", errAnio="Indiquez l'année du bateau.", errEstado="Indiquez l'état du bateau.",
    miBarco='votre bateau', sinDatosT='{n} : je l’estime au cas par cas',
    sinDatos="Je n'ai pas encore assez d'annonces comparables pour votre modèle pour vous donner une fourchette fiable, et je préfère ne pas l'inventer. Envoyez-moi les données et je vous dis ce que je vois sur le marché, gratuitement.",
    refTipo='À titre très général, les modèles de ce type que je suis chaque mois sont annoncés entre {a} et {b}, selon le modèle, l’année et le moteur.',
    sinAnioT='{n} de {y} : je l’estime au cas par cas', sinAnio="Pour cette année, je n'ai pas assez d'annonces comparables de ce modèle. Envoyez-moi les données et je vous dis ce que je vois sur le marché.",
    desde='À partir de', pocos='Peu d’unités de ces années sont à vendre et les prix varient beaucoup selon le moteur et l’équipement : mieux vaut voir au cas par cas.',
    contexto='Les {y0}-{y1} de ce modèle sont annoncés entre {a} et {b}. Votre fourchette place votre bateau dans cet intervalle selon son état et ses heures.',
    obra='Si les travaux sont importants (moteur, structure), le prix peut être inférieur à cette fourchette.',
    horas='Avec beaucoup d’heures, un historique d’entretien avec factures et une révision récente du moteur aident à défendre le prix.',
    verModelo='Voir les prix par année et les points à vérifier sur le {n}',
    nota="Prix d'annonce indicatif à partir d'annonces publiques revues chaque mois. Ce n'est ni une expertise ni une offre d'achat ; le prix de vente final est en général un peu inférieur après négociation.",
    cta='Demander à Juan une estimation personnalisée', waModelo="Bonjour Juan, j'ai utilisé le calculateur du site. J'ai un {n} de {y} et je souhaiterais une estimation.",
    waOtro="Bonjour Juan, j'ai utilisé le calculateur du site. J'ai un {n} de {y}, {e} m de long, et je souhaiterais une estimation."))

WA = 'https://wa.me/34633742973?text='

def aside(eb, h3, p, wa_txt, wa_btn, toc_t, toc, rel_t, rels):
    import urllib.parse
    return ('''    <aside class="aside" aria-label="Contacto">
      <div class="card">
        <p class="eyebrow">%s</p>
        <h3>%s</h3>
        <p>%s</p>
        <a class="btn btn-wa" href="%s%s" target="_blank" rel="noopener">%s</a>
      </div>
      <nav class="toc" aria-label="%s"><p class="eyebrow">%s</p><ol>%s</ol></nav>
      <div class="rel"><p class="eyebrow">%s</p>%s</div>
    </aside>''' % (eb, h3, p, WA, urllib.parse.quote(wa_txt), wa_btn, toc_t, toc_t,
                   ''.join('<li><a href="#%s">%s</a></li>' % x for x in toc), rel_t, ''.join('<a href="%s">%s</a>' % x for x in rels)))

PAGES = {}
FAQ = {}
FAQ['es'] = [
 ('¿Esto es una tasación?', 'No. Es un precio orientativo de anuncio a partir de anuncios públicos de barcos como el tuyo. Una tasación formal la firma un perito después de ver el barco. Te lo explico en la <a href="{P}/guias/tasacion-barco.html">guía de tasación</a>.'),
 ('¿Por qué no sale mi modelo?', 'Solo pongo modelos de los que tengo suficientes anuncios comparables para dar un rango fiable. Cada mes reviso los precios y voy añadiendo modelos. Si el tuyo no está, te lo valoro a mano y gratis.'),
 ('¿Por qué el precio de venta suele ser más bajo?', 'Porque los rangos salen de lo que se pide en los anuncios, y casi siempre hay negociación. Por eso conviene salir con un precio defendible, no con el más alto que veas publicado.'),
 ('¿Cuánto tardaré en venderlo?', 'Depende del tipo de barco, del precio y de la época: fuera de temporada suele alargarse. No te voy a prometer un plazo, pero sí ayudarte a que el precio y el anuncio no sean lo que lo frene.'),
 ('¿Tiene algún coste la valoración personal?', 'No. La valoración y la primera conversación son gratis. Solo cobro si gestiono la venta y se cierra, y eso queda por escrito antes de empezar.')]
FAQ['ca'] = [
 ('Això és una taxació?', "No. És un preu orientatiu d'anunci a partir d'anuncis públics de vaixells com el teu. Una taxació formal la signa un perit després de veure el vaixell. T'ho explico a la <a href=\"{P}/guias/tasacion-barco.html\">guia de taxació</a>."),
 ('Per què no surt el meu model?', "Només poso models dels quals tinc prou anuncis comparables per donar un rang fiable. Cada mes reviso els preus i vaig afegint models. Si el teu no hi és, te'l valoro a mà i gratis."),
 ('Per què el preu de venda sol ser més baix?', "Perquè els rangs surten del que es demana als anuncis, i gairebé sempre hi ha negociació. Per això convé sortir amb un preu defensable, no amb el més alt que vegis publicat."),
 ('Quant trigaré a vendre’l?', "Depèn del tipus de vaixell, del preu i de l'època: fora de temporada sol allargar-se. No et prometré un termini, però sí ajudar-te perquè el preu i l'anunci no siguin el que el frena."),
 ('La valoració personal té cap cost?', "No. La valoració i la primera conversa són gratis. Només cobro si gestiono la venda i es tanca, i això queda per escrit abans de començar.")]
FAQ['en'] = [
 ('Is this a valuation report?', 'No. It is a guide asking price based on public listings of boats like yours. A formal valuation is signed by a surveyor after seeing the boat. I explain it in the <a href="{P}/guias/tasacion-barco.html">valuation guide</a>.'),
 ("Why isn't my model listed?", "I only include models for which I have enough comparable listings to give a reliable range. I review prices every month and keep adding models. If yours isn't there, I'll value it by hand, free of charge."),
 ('Why is the selling price usually lower?', 'Because the ranges come from asking prices, and there is almost always some negotiation. That is why it pays to start with a price you can justify, not the highest one you see online.'),
 ('How long will it take to sell?', "It depends on the type of boat, the price and the time of year: out of season it usually takes longer. I won't promise you a timeframe, but I can help make sure the price and the listing aren't what is holding it back."),
 ('Does the personal valuation cost anything?', 'No. The valuation and the first conversation are free. I only charge if I handle the sale and it goes through, and that is agreed in writing before we start.')]
FAQ['fr'] = [
 ("Est-ce une expertise ?", "Non. C'est un prix d'annonce indicatif à partir d'annonces publiques de bateaux comme le vôtre. Une expertise en bonne et due forme est signée par un expert après avoir vu le bateau. Je l'explique dans le <a href=\"{P}/guias/tasacion-barco.html\">guide de l'expertise</a>."),
 ("Pourquoi mon modèle n'apparaît-il pas ?", "Je n'inclus que les modèles pour lesquels j'ai assez d'annonces comparables pour donner une fourchette fiable. Je revois les prix chaque mois et j'ajoute des modèles. Si le vôtre n'y est pas, je l'estime au cas par cas, gratuitement."),
 ("Pourquoi le prix de vente est-il souvent plus bas ?", "Parce que les fourchettes reflètent les prix demandés dans les annonces, et il y a presque toujours une négociation. Mieux vaut partir d'un prix que l'on peut justifier, pas du plus élevé que l'on voit en ligne."),
 ("Combien de temps pour le vendre ?", "Cela dépend du type de bateau, du prix et de la saison : hors saison, c'est en général plus long. Je ne vous promettrai pas de délai, mais je peux vous aider pour que le prix et l'annonce ne soient pas ce qui freine la vente."),
 ("L'estimation personnalisée est-elle payante ?", "Non. L'estimation et le premier échange sont gratuits. Je ne facture que si je gère la vente et qu'elle se conclut, et c'est convenu par écrit avant de commencer.")]

def faq_html(l, title):
    return '<h2 id="faq">%s</h2>' % title + ''.join('<h3>%s</h3><p>%s</p>' % (q, a) for q, a in FAQ[l])

B = {}
B['es'] = dict(
 title='¿Cuánto vale mi barco? Calculadora de precio orientativo (2026)', h1='¿Cuánto vale mi barco?',
 desc='Calcula gratis el precio orientativo de tu barco de segunda mano según modelo, año, estado y horas, con precios de anuncios revisados cada mes. Sin registrarte.',
 eyebrow='Herramientas · Vender', meta='<span>Por Juan Morante</span><span>Precios revisados en octubre de 2026</span>',
 lead='Elige tu modelo, el año y cómo está, y te digo en qué rango se están anunciando barcos como el tuyo. Si tu modelo no está en la lista, te lo digo claro y lo valoro a mano. Sin registrarte y sin dejar el correo.',
 h_origen='De dónde salen estos precios', origen='<p>Los rangos salen de anuncios públicos de portales españoles y europeos que reviso cada mes, separados por modelo y por años. Los tienes todos en la <a href="{P}/precios/">tabla de precios de barcos de segunda mano</a>, y cada modelo tiene su ficha con lo que conviene mirar antes de comprar o vender.</p><p>Son precios de anuncio, no de cierre. Entre lo que se pide y lo que se acaba firmando casi siempre hay negociación; te lo explico en <a href="{P}/guias/precio-barco-ocasion.html">cómo poner precio a un barco de ocasión</a>.</p>',
 h_sube='Qué sube y qué baja el precio', sube='<ul><li><strong>Motor y horas.</strong> Es lo primero que mira un comprador. Las horas por sí solas dicen poco; con facturas de mantenimiento dicen mucho.</li><li><strong>Mantenimiento demostrable.</strong> Facturas, varadas, antifouling, revisiones. Lo que no se puede demostrar, el comprador lo descuenta.</li><li><strong>Papeles al día.</strong> ITB en vigor, titularidad clara y sin cargas. Un papel pendiente frena la venta más que un defecto visible.</li><li><strong>Equipo.</strong> Electrónica, toldos, hélice de proa o remolque suman, pero rara vez lo que costaron.</li><li><strong>Época y zona.</strong> En primavera hay más compradores; en otoño e invierno las ventas se alargan.</li></ul><p>Si quieres repasarlo punto por punto con tu barco, usa <a href="{P}/herramientas/valora-tu-barco.html">qué influye en el precio de mi barco</a>.</p>',
 h_fiscal='Valor de mercado y valor fiscal no son lo mismo', fiscal='<p>Hacienda publica cada año unos precios medios de embarcaciones que sirven para calcular impuestos como el ITP. Ese valor no mira el estado de tu barco, el motor ni el equipo, así que puede quedar por encima o por debajo de lo que vale en el mercado. Te lo explico en <a href="{P}/guias/valor-fiscal-barco-tablas-hacienda.html">el valor fiscal de un barco y las tablas de Hacienda</a>.</p>',
 faq_t='Preguntas frecuentes',
 aviso='Precios orientativos a octubre de 2026 a partir de anuncios públicos. No son una tasación, ni una oferta de compra, ni un compromiso de venta a ese precio. Podemos equivocarnos y nada de esta página es vinculante.',
 a=('¿Vendes tu barco?', 'Te preparo un precio de salida con datos.', 'Mándame modelo, año, motor y unas fotos, y te digo qué veo en el mercado. Gratis y sin compromiso.', 'Hola Juan, quiero saber cuánto vale mi barco.', 'Hablar con Juan por WhatsApp',
    'En esta página', [('pmCalc', 'Calculadora'), ('origen', 'De dónde salen los precios'), ('sube', 'Qué sube y qué baja el precio'), ('fiscal', 'Valor de mercado y valor fiscal'), ('faq', 'Preguntas frecuentes')],
    'También te puede interesar', [('{P}/vender-barco/', 'Vender mi barco con Plata Marine'), ('{P}/guias/tasacion-barco.html', 'Tasación de un barco: qué es y cuándo la necesitas'), ('{P}/precios/', 'Precios de barcos de segunda mano')]),
 crumbs=[('Herramientas', 'herramientas/')])
B['ca'] = dict(
 title='Quant val el meu vaixell? Calculadora de preu orientatiu (2026)', h1='Quant val el meu vaixell?',
 desc="Calcula gratis el preu orientatiu del teu vaixell de segona mà segons model, any, estat i hores, amb preus d'anuncis revisats cada mes. Sense registrar-te.",
 eyebrow='Eines · Vendre', meta="<span>Per Juan Morante</span><span>Preus revisats l'octubre de 2026</span>",
 lead="Tria el teu model, l'any i com està, i et dic en quin rang s'anuncien vaixells com el teu. Si el teu model no és a la llista, t'ho dic clar i el valoro a mà. Sense registrar-te i sense deixar el correu.",
 h_origen="D'on surten aquests preus", origen="<p>Els rangs surten d'anuncis públics de portals espanyols i europeus que reviso cada mes, separats per model i per anys. Els tens tots a la <a href=\"{P}/precios/\">taula de preus de vaixells de segona mà</a>, i cada model té la seva fitxa amb el que convé mirar abans de comprar o vendre.</p><p>Són preus d'anunci, no de tancament. Entre el que es demana i el que s'acaba signant gairebé sempre hi ha negociació; t'ho explico a <a href=\"{P}/guias/precio-barco-ocasion.html\">com posar preu a un vaixell d'ocasió</a>.</p>",
 h_sube='Què puja i què baixa el preu', sube="<ul><li><strong>Motor i hores.</strong> És el primer que mira un comprador. Les hores soles diuen poc; amb factures de manteniment diuen molt.</li><li><strong>Manteniment demostrable.</strong> Factures, varades, antifouling, revisions. El que no es pot demostrar, el comprador ho descompta.</li><li><strong>Papers al dia.</strong> ITB vigent, titularitat clara i sense càrregues. Un paper pendent frena la venda més que un defecte visible.</li><li><strong>Equip.</strong> Electrònica, tendals, hèlice de proa o remolc sumen, però rarament el que van costar.</li><li><strong>Època i zona.</strong> A la primavera hi ha més compradors; a la tardor i l'hivern les vendes s'allarguen.</li></ul><p>Si ho vols repassar punt per punt amb el teu vaixell, fes servir <a href=\"{P}/herramientas/valora-tu-barco.html\">què influeix en el preu del meu vaixell</a>.</p>",
 h_fiscal='Valor de mercat i valor fiscal no són el mateix', fiscal="<p>Hisenda publica cada any uns preus mitjans d'embarcacions que serveixen per calcular impostos com l'ITP. Aquest valor no mira l'estat del teu vaixell, el motor ni l'equip, així que pot quedar per sobre o per sota del que val al mercat. T'ho explico a <a href=\"{P}/guias/valor-fiscal-barco-tablas-hacienda.html\">el valor fiscal d'un vaixell i les taules d'Hisenda</a>.</p>",
 faq_t='Preguntes freqüents',
 aviso="Preus orientatius a octubre de 2026 a partir d'anuncis públics. No són una taxació, ni una oferta de compra, ni un compromís de venda a aquest preu. Ens podem equivocar i res d'aquesta pàgina és vinculant.",
 a=('Vens el teu vaixell?', 'Et preparo un preu de sortida amb dades.', "Envia'm model, any, motor i unes fotos, i et dic què veig al mercat. Gratis i sense compromís.", 'Hola Juan, vull saber quant val el meu vaixell.', 'Parlar amb Juan per WhatsApp',
    'En aquesta pàgina', [('pmCalc', 'Calculadora'), ('origen', "D'on surten els preus"), ('sube', 'Què puja i què baixa el preu'), ('fiscal', 'Valor de mercat i valor fiscal'), ('faq', 'Preguntes freqüents')],
    'També et pot interessar', [('{P}/vender-barco/', 'Vendre el meu vaixell amb Plata Marine'), ('{P}/guias/tasacion-barco.html', "Taxació d'un vaixell: què és i quan la necessites"), ('{P}/precios/', 'Preus de vaixells de segona mà')]),
 crumbs=[('Eines', 'herramientas/')])
B['en'] = dict(
 title='How much is my boat worth? Guide price calculator (2026)', h1='How much is my boat worth?',
 desc='Work out a free guide price for your used boat by model, year, condition and engine hours, using listing prices reviewed every month. No sign-up needed.',
 eyebrow='Tools · Selling', meta='<span>By Juan Morante</span><span>Prices reviewed in October 2026</span>',
 lead="Choose your model, the year and its condition, and I'll show you the range boats like yours are being listed at. If your model isn't on the list, I'll say so plainly and value it by hand. No sign-up and no email required.",
 h_origen='Where these prices come from', origen='<p>The ranges come from public listings on Spanish and European portals that I review every month, split by model and by year. You can see them all in the <a href="{P}/precios/">used boat price table</a>, and each model has its own page with what to check before buying or selling.</p><p>These are asking prices, not closing prices. There is almost always negotiation between what is asked and what is finally signed; I explain it in <a href="{P}/guias/precio-barco-ocasion.html">how to price a used boat</a>.</p>',
 h_sube='What pushes the price up or down', sube='<ul><li><strong>Engine and hours.</strong> The first thing a buyer looks at. Hours alone say little; with maintenance invoices they say a lot.</li><li><strong>Provable maintenance.</strong> Invoices, haul-outs, antifouling, services. Whatever cannot be proven, the buyer discounts.</li><li><strong>Paperwork in order.</strong> Valid ITB (Spanish boat inspection), clear ownership and no charges on the boat. A pending document slows a sale more than a visible defect.</li><li><strong>Equipment.</strong> Electronics, canopies, bow thruster or trailer add value, but rarely what they cost.</li><li><strong>Season and area.</strong> There are more buyers in spring; in autumn and winter sales take longer.</li></ul><p>To go through it point by point for your boat, use <a href="{P}/herramientas/valora-tu-barco.html">what affects the price of my boat</a>.</p>',
 h_fiscal='Market value and tax value are not the same', fiscal='<p>The Spanish tax authorities publish average boat prices every year, used to calculate taxes such as transfer tax (ITP). That value ignores your boat\'s condition, engine and equipment, so it can be above or below its market value. I explain it in <a href="{P}/guias/valor-fiscal-barco-tablas-hacienda.html">the tax value of a boat and the official tables</a>.</p>',
 faq_t='Frequently asked questions',
 aviso='Guide prices as of October 2026 based on public listings. They are not a valuation report, an offer to buy or a commitment to sell at that price. We may be wrong and nothing on this page is binding.',
 a=('Selling your boat?', "I'll prepare an asking price backed by data.", "Send me the model, year, engine and a few photos, and I'll tell you what I see on the market. Free and with no obligation.", "Hi Juan, I'd like to know how much my boat is worth.", 'Talk to Juan on WhatsApp',
    'On this page', [('pmCalc', 'Calculator'), ('origen', 'Where the prices come from'), ('sube', 'What pushes the price up or down'), ('fiscal', 'Market value and tax value'), ('faq', 'FAQ')],
    'You may also like', [('{P}/vender-barco/', 'Sell my boat with Plata Marine'), ('{P}/guias/tasacion-barco.html', 'Boat valuation: what it is and when you need one'), ('{P}/precios/', 'Used boat prices')]),
 crumbs=[('Tools', 'herramientas/')])
B['fr'] = dict(
 title='Combien vaut mon bateau ? Calculateur de prix indicatif (2026)', h1='Combien vaut mon bateau ?',
 desc="Calculez gratuitement le prix indicatif de votre bateau d'occasion selon le modèle, l'année, l'état et les heures moteur, avec des prix d'annonces revus chaque mois. Sans inscription.",
 eyebrow='Outils · Vendre', meta='<span>Par Juan Morante</span><span>Prix revus en octobre 2026</span>',
 lead="Choisissez votre modèle, l'année et son état, et je vous indique dans quelle fourchette sont annoncés des bateaux comme le vôtre. Si votre modèle n'est pas dans la liste, je vous le dis franchement et je l'estime au cas par cas. Sans inscription ni adresse e-mail.",
 h_origen="D'où viennent ces prix", origen="<p>Les fourchettes proviennent d'annonces publiques de portails espagnols et européens que je revois chaque mois, par modèle et par année. Vous les trouverez toutes dans le <a href=\"{P}/precios/\">tableau des prix de bateaux d'occasion</a>, et chaque modèle a sa fiche avec les points à vérifier avant d'acheter ou de vendre.</p><p>Ce sont des prix d'annonce, pas des prix de vente conclus. Entre le prix demandé et le prix signé, il y a presque toujours une négociation ; je l'explique dans <a href=\"{P}/guias/precio-barco-ocasion.html\">comment fixer le prix d'un bateau d'occasion</a>.</p>",
 h_sube='Ce qui fait monter ou baisser le prix', sube="<ul><li><strong>Moteur et heures.</strong> C'est la première chose que regarde un acheteur. Les heures seules disent peu ; avec des factures d'entretien, elles disent beaucoup.</li><li><strong>Entretien prouvé.</strong> Factures, carénages, antifouling, révisions. Ce qui ne peut pas être prouvé, l'acheteur le déduit.</li><li><strong>Papiers en règle.</strong> ITB (contrôle technique espagnol) en cours de validité, propriété claire et sans charges. Un papier en attente freine plus la vente qu'un défaut visible.</li><li><strong>Équipement.</strong> Électronique, tauds, propulseur d'étrave ou remorque ajoutent de la valeur, mais rarement ce qu'ils ont coûté.</li><li><strong>Saison et zone.</strong> Il y a plus d'acheteurs au printemps ; en automne et en hiver, les ventes prennent plus de temps.</li></ul><p>Pour le passer en revue point par point avec votre bateau, utilisez <a href=\"{P}/herramientas/valora-tu-barco.html\">ce qui influe sur le prix de mon bateau</a>.</p>",
 h_fiscal='Valeur de marché et valeur fiscale ne sont pas la même chose', fiscal="<p>Le fisc espagnol publie chaque année des prix moyens de bateaux qui servent à calculer des impôts comme l'ITP (droits de mutation). Cette valeur ne tient compte ni de l'état du bateau, ni du moteur, ni de l'équipement : elle peut être supérieure ou inférieure à sa valeur de marché. Je l'explique dans <a href=\"{P}/guias/valor-fiscal-barco-tablas-hacienda.html\">la valeur fiscale d'un bateau en Espagne</a>.</p>",
 faq_t='Questions fréquentes',
 aviso="Prix indicatifs à octobre 2026 à partir d'annonces publiques. Ce n'est ni une expertise, ni une offre d'achat, ni un engagement de vente à ce prix. Nous pouvons nous tromper et rien sur cette page n'est contractuel.",
 a=('Vous vendez votre bateau ?', 'Je vous prépare un prix de départ chiffré.', "Envoyez-moi le modèle, l'année, le moteur et quelques photos, et je vous dis ce que je vois sur le marché. Gratuit et sans engagement.", 'Bonjour Juan, je voudrais savoir combien vaut mon bateau.', 'Parler à Juan sur WhatsApp',
    'Sur cette page', [('pmCalc', 'Calculateur'), ('origen', "D'où viennent les prix"), ('sube', 'Ce qui fait monter ou baisser le prix'), ('fiscal', 'Valeur de marché et valeur fiscale'), ('faq', 'Questions fréquentes')],
    'À lire aussi', [('{P}/vender-barco/', 'Vendre mon bateau avec Plata Marine'), ('{P}/guias/tasacion-barco.html', "L'expertise d'un bateau : ce que c'est et quand en avoir besoin"), ('{P}/precios/', "Prix des bateaux d'occasion")]),
 crumbs=[('Outils', 'herramientas/')])

def pages():
    out, crumbs = {}, {}
    for l, b in B.items():
        body = form(T[l]) + '\n<h2 id="origen">%s</h2>%s\n<h2 id="sube">%s</h2>%s\n<h2 id="fiscal">%s</h2>%s\n%s' % (
            b['h_origen'], b['origen'], b['h_sube'], b['sube'], b['h_fiscal'], b['fiscal'], faq_html(l, b['faq_t']))
        out[l] = dict(title=b['title'], h1=b['h1'], desc=b['desc'], eyebrow=b['eyebrow'], meta=b['meta'], lead=b['lead'], body=body,
                      aviso=b['aviso'], aside=aside(*b['a']), faq=[(q, a.replace('{P}', '')) for q, a in FAQ[l]])
        crumbs[l] = b['crumbs']
    return out, crumbs
