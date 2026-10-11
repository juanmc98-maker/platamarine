# -*- coding: utf-8 -*-
"""Genera (ES/CA/EN/FR):
  - /astilleros/                      página para astilleros sin representación en Cataluña (formulario → hoja de leads, source 'astillero')
  - /guias/alquilar-mi-barco-charter.html   guía: ¿puedo alquilar mi barco para pagar los gastos?
Toma cabecera, menú y pie de cada idioma de guias/lista-6-y-lista-7.html.
Uso: python3 _tools/build_astilleros_charter.py  (desde la raíz del repo)"""
import os, re, json
from urllib.parse import quote
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE = 'https://www.platamarine.com'
LANGS = ['es', 'ca', 'en', 'fr']
PRE = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr', 'it': '/it'}
YARD_LANGS = LANGS + ['it']  # la página de astilleros también en italiano (excepción aprobada por Juan, 11 oct 2026)
TODAY = '2026-10-11'

def shell(lang):
    src = 'en' if lang == 'it' else lang
    p = os.path.join(ROOT, ('' if src == 'es' else src + '/') + 'guias/lista-6-y-lista-7.html')
    t = open(p, encoding='utf-8').read()
    b0 = t.index('<body>'); m0 = t.index('<main'); f0 = t.index('</main>') + len('</main>')
    header = t[b0:m0]
    footer = t[f0:]
    # rutas relativas → absolutas
    header = header.replace('href="../"', 'href="%s/"' % PRE['en' if lang == 'it' else lang]).replace('src="../logo', 'src="/logo')
    footer = re.sub(r'href="\.\./(aviso-legal|privacidad|cookies)\.html"', lambda m: 'href="%s/%s.html"' % (PRE['en' if lang == 'it' else lang], m.group(1)), footer)
    return header, footer

def head(lang, path, title, desc, schema, crumbs, extra='', langs=None):
    url = BASE + PRE[lang] + path
    alts = ''.join('<link rel="alternate" hreflang="%s" href="%s%s%s">\n' % (l, BASE, PRE[l], path) for l in (langs or LANGS))
    alts += '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (BASE, path)
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}
    return ('<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<link rel="canonical" href="%s">\n%s'
            '<link rel="icon" type="image/png" href="/logo-plata-marine.png">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:type" content="article">\n'
            '<meta property="og:url" content="%s">\n<meta property="og:image" content="https://www.platamarine.com/og-image.jpg">\n'
            '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            '<link rel="stylesheet" href="/guias/guias.css">\n<script type="application/ld+json">\n%s\n</script>\n'
            '<link rel="stylesheet" href="/nav.css?v=20261006m">\n<script type="application/ld+json">%s</script>\n%s</head>\n'
            % (lang, title, desc, url, alts, title, desc, url, json.dumps(schema, ensure_ascii=False), json.dumps(bc, ensure_ascii=False), extra))

def fix_header(h, lang, path, wa_text, wa_label=None, langs=None):
    # enlace de WhatsApp de la cabecera y selector de idioma apuntando a esta página
    h = re.sub(r'(<a class="btn btn-wa" href="https://wa\.me/34633742973\?text=)[^"]*', lambda m: m.group(1) + quote(wa_text), h, count=1)
    def lsw(m):
        out = []
        for l in (langs or LANGS):
            cur = ' aria-current="page"' if l == lang else ''
            flag = '<span class="flag flag-%s" aria-hidden="true"></span>' % l if l != 'it' else '<span aria-hidden="true" style="font:600 12px/1 sans-serif">IT</span>'
            out.append('<a href="%s%s%s"%s>%s<span class="sr-only">%s</span></a>' % (BASE, PRE[l], path, cur, flag, l.upper()))
        return '<div class="langsw" aria-label="%s">%s</div>' % (m.group(1), ''.join(out))
    h = re.sub(r'<div class="langsw" aria-label="([^"]*)">.*?</div>', lsw, h, count=1, flags=re.S)
    return h

def wa(text):
    return 'https://wa.me/34633742973?text=' + quote(text)

NEXT_STYLE = 'background:rgba(181,138,44,.08);border-left:3px solid #B58A2C;padding:16px 18px;border-radius:0 6px 6px 0;margin:26px 0'
BTN_STYLE = 'display:inline-block;background:#0E3042;color:#fff;padding:10px 18px;border-radius:6px;text-decoration:none;font-family:var(--display,inherit);font-weight:600;font-size:15px'

# ---------------------------------------------------------------- ASTILLEROS
A = {
'es': dict(
  title='¿Eres astillero? Representación comercial en Cataluña · Plata Marine',
  desc='Astilleros sin distribuidor en Cataluña: te represento como agente comercial a comisión, sin que tengas que mandar stock. Cómo trabajo y formulario de contacto.',
  crumbs=['Plata Marine', 'Para astilleros'],
  eyebrow='Para astilleros', h1='¿Fabricas barcos y aún no tienes quien te represente en Cataluña?',
  meta=['Juan Morante', 'Plata Marine · Cataluña'],
  lead='Soy Juan Morante, bróker náutico en Cataluña. Busco astilleros que todavía no tengan distribuidor aquí para representarlos como agente comercial a comisión: presento tus barcos a compradores de la zona y acompaño cada venta hasta la firma.',
  body='''<h2 id="como">Cómo trabajo</h2>
<ul>
<li><strong>Agente comercial a comisión.</strong> Trabajo con un contrato de agencia (Ley 12/1992). Cobro solo por ventas cerradas.</li>
<li><strong>Sin stock ni barco de demostración por mi parte.</strong> Las pruebas de mar se organizan con el astillero o con el barco de algún cliente que quiera enseñarlo.</li>
<li><strong>El pedido y la factura son del astillero.</strong> Yo presento la marca, atiendo las consultas, acompaño las visitas y llevo cada operación hasta la firma.</li>
<li><strong>Mismo precio de tarifa.</strong> El cliente paga lo mismo que si comprara directamente en fábrica.</li>
</ul>
<h2 id="aporto">Qué te puedo aportar</h2>
<ul>
<li>Llevo 12 años de cara al público, primero en la venta de vehículos y ahora como bróker náutico, escuchando lo que necesita cada cliente.</li>
<li>Una web, <a href="/">www.platamarine.com</a>, en cuatro idiomas, con guías, calculadoras y barcos en venta que leen compradores de Cataluña y Baleares.</li>
<li>Atención en castellano, catalán e inglés (en francés, con traductor).</li>
<li>Conocimiento del cliente local: qué esloras y qué tipo de barco se mueven en la Costa Brava, el Maresme, Barcelona y la Costa Daurada.</li>
</ul>
<h2 id="encaje">Con qué astilleros encajo</h2>
<ul>
<li>Sin distribuidor oficial en Cataluña (si ya lo tienes, no quiero pisar a nadie).</li>
<li>Con marcado CE y organismo notificado verificable.</li>
<li>Cualquier eslora y tipo de barco a motor; veleros, según el caso.</li>
<li>Dispuestos a facilitar fichas técnicas, fotos, lista de precios y plazos de entrega reales.</li>
</ul>
<p>Lo normal es empezar con una llamada o un correo para conocernos, ver tu gama y comprobar si encaja con lo que buscan los compradores de aquí. Si encaja, lo ponemos por escrito: zona, comisión, forma de cobro y cómo se registran los clientes que presento.</p>''',
  form_title='Escríbeme', form_intro='Cuéntame quién sois y qué barcos fabricáis. Te contesto en 24 horas laborables.',
  f=dict(yard='Astillero o marca', web='Web', country='País', name='Tu nombre', role='Cargo', email='Email', tel='Teléfono', msg='Mensaje', opt='opcional',
         ph_yard='Astilleros del Mar', ph_web='https://…', ph_country='Italia', ph_name='Marco', ph_role='Export manager', ph_email='nombre@astillero.com', ph_tel='+39 3xx xxx xxxx', ph_msg='Gama, esloras, dónde vendéis hoy…',
         send='Enviar', legal='Responsable: Juan Morante (Plata Marine). Usaré estos datos solo para contestar a tu mensaje y valorar una posible colaboración comercial. Puedes ejercer tus derechos en juan@platamarine.com. <a href="/privacidad.html">Política de privacidad</a>.', req='Los campos con * son obligatorios.'),
  aside_eyebrow='¿Prefieres WhatsApp?', aside_h='Escríbeme directamente.', aside_p='Dime qué astillero sois y te contesto por ahí.', aside_btn='Hablar con Juan por WhatsApp',
  wa='Hola Juan, te escribo de un astillero y me interesa hablar de representación en Cataluña.',
  toc=['Cómo trabajo', 'Qué te puedo aportar', 'Con qué astilleros encajo', 'Escríbeme'],
  fine='Esta página explica cómo trabajo; no es una oferta vinculante. Las condiciones de cada colaboración se acuerdan por escrito con cada astillero.'),
'ca': dict(
  title='Ets drassana? Representació comercial a Catalunya · Plata Marine',
  desc='Drassanes sense distribuïdor a Catalunya: et represento com a agent comercial a comissió, sense que hagis d’enviar estoc. Com treballo i formulari de contacte.',
  crumbs=['Plata Marine', 'Per a drassanes'],
  eyebrow='Per a drassanes', h1='Fabriques vaixells i encara no tens qui et representi a Catalunya?',
  meta=['Juan Morante', 'Plata Marine · Catalunya'],
  lead='Sóc en Juan Morante, bròker nàutic a Catalunya. Busco drassanes que encara no tinguin distribuïdor aquí per representar-les com a agent comercial a comissió: presento els teus vaixells a compradors de la zona i acompanyo cada venda fins a la signatura.',
  body='''<h2 id="como">Com treballo</h2>
<ul>
<li><strong>Agent comercial a comissió.</strong> Treballo amb un contracte d’agència (Llei 12/1992). Cobro només per vendes tancades.</li>
<li><strong>Sense estoc ni vaixell de demostració per part meva.</strong> Les proves de mar s’organitzen amb la drassana o amb el vaixell d’algun client que el vulgui ensenyar.</li>
<li><strong>La comanda i la factura són de la drassana.</strong> Jo presento la marca, atenc les consultes, acompanyo les visites i porto cada operació fins a la signatura.</li>
<li><strong>Mateix preu de tarifa.</strong> El client paga el mateix que si comprés directament a fàbrica.</li>
</ul>
<h2 id="aporto">Què et puc aportar</h2>
<ul>
<li>Fa 12 anys que treballo de cara al públic, primer en la venda de vehicles i ara com a bròker nàutic, escoltant què necessita cada client.</li>
<li>Un web, <a href="/ca/">www.platamarine.com</a>, en quatre idiomes, amb guies, calculadores i vaixells en venda que llegeixen compradors de Catalunya i Balears.</li>
<li>Atenció en català, castellà i anglès (en francès, amb traductor).</li>
<li>Coneixement del client local: quines eslores i quin tipus de vaixell es mouen a la Costa Brava, el Maresme, Barcelona i la Costa Daurada.</li>
</ul>
<h2 id="encaje">Amb quines drassanes encaixo</h2>
<ul>
<li>Sense distribuïdor oficial a Catalunya (si ja en tens, no vull trepitjar ningú).</li>
<li>Amb marcatge CE i organisme notificat verificable.</li>
<li>Qualsevol eslora i tipus de vaixell a motor; velers, segons el cas.</li>
<li>Disposades a facilitar fitxes tècniques, fotos, llista de preus i terminis d’entrega reals.</li>
</ul>
<p>El més normal és començar amb una trucada o un correu per conèixer-nos, veure la teva gamma i comprovar si encaixa amb el que busquen els compradors d’aquí. Si encaixa, ho posem per escrit: zona, comissió, forma de cobrament i com es registren els clients que presento.</p>''',
  form_title='Escriu-me', form_intro='Explica’m qui sou i quins vaixells fabriqueu. Et contesto en 24 hores laborables.',
  f=dict(yard='Drassana o marca', web='Web', country='País', name='El teu nom', role='Càrrec', email='Correu', tel='Telèfon', msg='Missatge', opt='opcional',
         ph_yard='Drassanes del Mar', ph_web='https://…', ph_country='Itàlia', ph_name='Marco', ph_role='Export manager', ph_email='nom@drassana.com', ph_tel='+39 3xx xxx xxxx', ph_msg='Gamma, eslores, on veneu avui…',
         send='Enviar', legal='Responsable: Juan Morante (Plata Marine). Faré servir aquestes dades només per respondre el teu missatge i valorar una possible col·laboració comercial. Pots exercir els teus drets a juan@platamarine.com. <a href="/ca/privacidad.html">Política de privacitat</a>.', req='Els camps amb * són obligatoris.'),
  aside_eyebrow='Prefereixes WhatsApp?', aside_h='Escriu-me directament.', aside_p='Digues-me quina drassana sou i et contesto per allà.', aside_btn='Parla amb en Juan per WhatsApp',
  wa='Hola Juan, t’escric d’una drassana i m’interessa parlar de representació a Catalunya.',
  toc=['Com treballo', 'Què et puc aportar', 'Amb quines drassanes encaixo', 'Escriu-me'],
  fine='Aquesta pàgina explica com treballo; no és una oferta vinculant. Les condicions de cada col·laboració s’acorden per escrit amb cada drassana.'),
'en': dict(
  title='Boat builders: dealer and sales agent in Catalonia, Spain · Plata Marine',
  desc='Looking for a boat dealer or sales agent in Spain? I represent boat builders in Catalonia (Barcelona, Costa Brava) as a commission-based agent, with no stock required.',
  crumbs=['Plata Marine', 'For boat builders'],
  eyebrow='For boat builders', h1='Do you build boats and have no one representing you in Catalonia yet?',
  meta=['Juan Morante', 'Plata Marine · Catalonia'],
  lead='I’m Juan Morante, a yacht broker in Catalonia. I’m looking for boat builders with no dealer here yet, to represent them as a commission-based sales agent: I introduce your boats to local buyers and see each sale through to signing.',
  body='''<h2 id="como">How I work</h2>
<ul>
<li><strong>Commission-based sales agent.</strong> I work under an agency agreement (Spanish Law 12/1992) and am only paid on closed sales.</li>
<li><strong>No stock or demo boat on my side.</strong> Sea trials are arranged with the yard or with a client’s boat whose owner is happy to show it.</li>
<li><strong>Orders and invoices are issued by the yard.</strong> I present the brand, handle enquiries, accompany viewings and take each deal through to signing.</li>
<li><strong>Same list price.</strong> The client pays the same as buying direct from the factory.</li>
</ul>
<h2 id="aporto">What I can offer</h2>
<ul>
<li>12 years in customer-facing sales, first in vehicle sales and now as a yacht broker, listening to what each client needs.</li>
<li>A website, <a href="/en/">www.platamarine.com</a>, in four languages, with guides, calculators and boats for sale read by buyers in Catalonia and the Balearic Islands.</li>
<li>Service in Spanish, Catalan and English (French with a translator).</li>
<li>Knowledge of local buyers: which lengths and types of boat sell on the Costa Brava, the Maresme, Barcelona and the Costa Daurada.</li>
</ul>
<h2 id="encaje">Which yards I’m a good fit for</h2>
<ul>
<li>No official dealer in Catalonia (if you already have one, I don’t want to step on anyone’s toes).</li>
<li>CE marking with a verifiable notified body.</li>
<li>Motor boats of any length and type; sailboats, case by case.</li>
<li>Willing to share technical sheets, photos, price lists and real delivery times.</li>
</ul>
<p>We usually start with a call or an email to get to know each other, look at your range and check whether it fits what buyers here are looking for. If it does, we put it in writing: territory, commission, payment terms and how the clients I introduce are registered.</p>''',
  form_title='Get in touch', form_intro='Tell me who you are and what boats you build. I reply within 24 working hours.',
  f=dict(yard='Yard or brand', web='Website', country='Country', name='Your name', role='Position', email='Email', tel='Phone', msg='Message', opt='optional',
         ph_yard='Sea Yachts', ph_web='https://…', ph_country='Italy', ph_name='Marco', ph_role='Export manager', ph_email='name@yard.com', ph_tel='+39 3xx xxx xxxx', ph_msg='Range, lengths, where you sell today…',
         send='Send', legal='Data controller: Juan Morante (Plata Marine). I will use this data only to reply to your message and assess a possible sales partnership. You can exercise your rights at juan@platamarine.com. <a href="/en/privacidad.html">Privacy policy</a>.', req='Fields marked * are required.'),
  aside_eyebrow='Prefer WhatsApp?', aside_h='Message me directly.', aside_p='Tell me which yard you’re from and I’ll reply there.', aside_btn='Talk to Juan on WhatsApp',
  wa='Hi Juan, I’m writing from a boat builder and would like to talk about representation in Catalonia.',
  toc=['How I work', 'What I can offer', 'Which yards I’m a good fit for', 'Get in touch'],
  fine='This page explains how I work; it is not a binding offer. The terms of each partnership are agreed in writing with each yard.'),
'fr': dict(
  title='Chantiers navals : représentation commerciale en Catalogne · Plata Marine',
  desc='Chantiers sans distributeur en Catalogne : je vous représente comme agent commercial à la commission, sans stock à envoyer. Comment je travaille et formulaire de contact.',
  crumbs=['Plata Marine', 'Pour les chantiers navals'],
  eyebrow='Pour les chantiers navals', h1='Vous construisez des bateaux et personne ne vous représente encore en Catalogne ?',
  meta=['Juan Morante', 'Plata Marine · Catalogne'],
  lead='Je suis Juan Morante, courtier nautique en Catalogne. Je recherche des chantiers qui n’ont pas encore de distributeur ici, pour les représenter comme agent commercial à la commission : je présente vos bateaux aux acheteurs de la région et j’accompagne chaque vente jusqu’à la signature.',
  body='''<h2 id="como">Comment je travaille</h2>
<ul>
<li><strong>Agent commercial à la commission.</strong> Je travaille avec un contrat d’agence (loi espagnole 12/1992) et je ne suis rémunéré que sur les ventes conclues.</li>
<li><strong>Pas de stock ni de bateau de démonstration de mon côté.</strong> Les essais en mer s’organisent avec le chantier ou avec le bateau d’un client prêt à le montrer.</li>
<li><strong>La commande et la facture sont émises par le chantier.</strong> Je présente la marque, je réponds aux demandes, j’accompagne les visites et je suis chaque opération jusqu’à la signature.</li>
<li><strong>Même prix catalogue.</strong> Le client paie le même prix qu’en achetant directement à l’usine.</li>
</ul>
<h2 id="aporto">Ce que je peux vous apporter</h2>
<ul>
<li>12 ans au contact des clients, d’abord dans la vente de véhicules et aujourd’hui comme courtier nautique, à l’écoute de ce dont chacun a besoin.</li>
<li>Un site, <a href="/fr/">www.platamarine.com</a>, en quatre langues, avec des guides, des calculateurs et des bateaux en vente, lu par des acheteurs de Catalogne et des Baléares.</li>
<li>Accueil en espagnol, catalan et anglais (en français, avec un traducteur).</li>
<li>Connaissance de la clientèle locale : quelles longueurs et quels types de bateaux se vendent sur la Costa Brava, le Maresme, Barcelone et la Costa Daurada.</li>
</ul>
<h2 id="encaje">Avec quels chantiers je travaille</h2>
<ul>
<li>Sans distributeur officiel en Catalogne (si vous en avez déjà un, je ne veux marcher sur les plates-bandes de personne).</li>
<li>Avec marquage CE et organisme notifié vérifiable.</li>
<li>Bateaux à moteur de toute longueur et de tout type ; voiliers, au cas par cas.</li>
<li>Prêts à fournir fiches techniques, photos, liste de prix et délais de livraison réels.</li>
</ul>
<p>En général, on commence par un appel ou un e-mail pour faire connaissance, voir votre gamme et vérifier si elle correspond à ce que recherchent les acheteurs d’ici. Si c’est le cas, on le met par écrit : territoire, commission, modalités de paiement et enregistrement des clients que je présente.</p>''',
  form_title='Écrivez-moi', form_intro='Dites-moi qui vous êtes et quels bateaux vous construisez. Je réponds sous 24 heures ouvrées.',
  f=dict(yard='Chantier ou marque', web='Site web', country='Pays', name='Votre nom', role='Fonction', email='E-mail', tel='Téléphone', msg='Message', opt='facultatif',
         ph_yard='Chantier de la Mer', ph_web='https://…', ph_country='France', ph_name='Pierre', ph_role='Export manager', ph_email='nom@chantier.com', ph_tel='+33 6 xx xx xx xx', ph_msg='Gamme, longueurs, où vous vendez aujourd’hui…',
         send='Envoyer', legal='Responsable : Juan Morante (Plata Marine). J’utiliserai ces données uniquement pour répondre à votre message et étudier une éventuelle collaboration commerciale. Vous pouvez exercer vos droits à juan@platamarine.com. <a href="/fr/privacidad.html">Politique de confidentialité</a>.', req='Les champs marqués * sont obligatoires.'),
  aside_eyebrow='Vous préférez WhatsApp ?', aside_h='Écrivez-moi directement.', aside_p='Dites-moi de quel chantier vous êtes et je vous réponds là-bas.', aside_btn='Parler avec Juan sur WhatsApp',
  wa='Bonjour Juan, je vous écris de la part d’un chantier naval et j’aimerais parler de représentation en Catalogne.',
  toc=['Comment je travaille', 'Ce que je peux vous apporter', 'Avec quels chantiers je travaille', 'Écrivez-moi'],
  fine='Cette page explique comment je travaille ; ce n’est pas une offre contractuelle. Les conditions de chaque collaboration sont convenues par écrit avec chaque chantier.'),
}


A['it'] = dict(
  title='Cantieri nautici: agente e rappresentanza in Catalogna (Spagna) · Plata Marine',
  desc='Cantiere senza rivenditore in Catalogna? Vi rappresento come agente commerciale a provvigione a Barcellona e in Costa Brava, senza bisogno di stock. Come lavoro e modulo di contatto.',
  crumbs=['Plata Marine', 'Per i cantieri nautici'],
  eyebrow='Per i cantieri nautici', h1='Costruite barche e non avete ancora nessuno che vi rappresenti in Catalogna?',
  meta=['Juan Morante', 'Plata Marine · Catalogna'],
  lead='Sono Juan Morante, broker nautico in Catalogna. Cerco cantieri che non abbiano ancora un rivenditore qui, per rappresentarli come agente commerciale a provvigione: presento le vostre barche agli acquirenti della zona e seguo ogni vendita fino alla firma.',
  body='''<h2 id="como">Come lavoro</h2>
<ul>
<li><strong>Agente commerciale a provvigione.</strong> Lavoro con un contratto di agenzia (legge spagnola 12/1992) e vengo pagato solo sulle vendite concluse.</li>
<li><strong>Nessuno stock né barca dimostrativa da parte mia.</strong> Le prove in mare si organizzano con il cantiere o con la barca di un cliente disposto a mostrarla.</li>
<li><strong>Ordine e fattura sono del cantiere.</strong> Io presento il marchio, rispondo alle richieste, accompagno le visite e seguo ogni trattativa fino alla firma.</li>
<li><strong>Stesso prezzo di listino.</strong> Il cliente paga lo stesso prezzo che pagherebbe acquistando direttamente in fabbrica.</li>
</ul>
<h2 id="aporto">Cosa posso offrirvi</h2>
<ul>
<li>12 anni a contatto con il pubblico, prima nella vendita di veicoli e oggi come broker nautico, ascoltando ciò di cui ha bisogno ogni cliente.</li>
<li>Un sito, <a href="/en/">www.platamarine.com</a>, in quattro lingue, con guide, calcolatori e barche in vendita, letto da acquirenti della Catalogna e delle Baleari.</li>
<li>Assistenza in spagnolo, catalano e inglese (in italiano e francese, con l’aiuto di un traduttore).</li>
<li>Conoscenza del cliente locale: quali lunghezze e quali tipi di barca si vendono in Costa Brava, nel Maresme, a Barcellona e in Costa Daurada.</li>
</ul>
<h2 id="encaje">Con quali cantieri lavoro</h2>
<ul>
<li>Senza rivenditore ufficiale in Catalogna (se lo avete già, non voglio pestare i piedi a nessuno).</li>
<li>Con marcatura CE e organismo notificato verificabile.</li>
<li>Barche a motore di qualsiasi lunghezza e tipo; barche a vela, da valutare caso per caso.</li>
<li>Disposti a fornire schede tecniche, foto, listino prezzi e tempi di consegna reali.</li>
</ul>
<p>Di solito si comincia con una telefonata o una e-mail per conoscerci, vedere la vostra gamma e capire se corrisponde a ciò che cercano gli acquirenti di qui. Se è così, mettiamo tutto per iscritto: zona, provvigione, modalità di pagamento e registrazione dei clienti che presento.</p>''',
  form_title='Scrivetemi', form_intro='Raccontatemi chi siete e quali barche costruite. Rispondo entro 24 ore lavorative.',
  f=dict(yard='Cantiere o marchio', web='Sito web', country='Paese', name='Il vostro nome', role='Ruolo', email='E-mail', tel='Telefono', msg='Messaggio', opt='facoltativo',
         ph_yard='Cantiere del Mare', ph_web='https://…', ph_country='Italia', ph_name='Marco', ph_role='Export manager', ph_email='nome@cantiere.it', ph_tel='+39 3xx xxx xxxx', ph_msg='Gamma, lunghezze, dove vendete oggi…',
         send='Invia', legal='Titolare: Juan Morante (Plata Marine). Userò questi dati solo per rispondere al vostro messaggio e valutare una possibile collaborazione commerciale. Potete esercitare i vostri diritti scrivendo a juan@platamarine.com. <a href="/en/privacidad.html">Informativa sulla privacy</a> (in inglese).', req='I campi con * sono obbligatori.'),
  aside_eyebrow='Preferite WhatsApp?', aside_h='Scrivetemi direttamente.', aside_p='Ditemi di quale cantiere siete e vi rispondo lì.', aside_btn='Scrivi a Juan su WhatsApp',
  wa='Buongiorno Juan, vi scrivo da un cantiere nautico e vorrei parlare di rappresentanza in Catalogna.',
  toc=['Come lavoro', 'Cosa posso offrirvi', 'Con quali cantieri lavoro', 'Scrivetemi'],
  fine='Questa pagina spiega come lavoro; non è un’offerta vincolante. Le condizioni di ogni collaborazione si concordano per iscritto con ciascun cantiere. Testo scritto con l’aiuto di un traduttore.')

FORM_CSS = '''<style>
.yard-form{display:grid;grid-template-columns:1fr 1fr;gap:14px 16px;margin:18px 0 8px}
.yard-form .span2{grid-column:1/-1}
.yard-form label{display:block;font-weight:600;font-size:14px;margin-bottom:6px}
.yard-form label small{font-weight:400;opacity:.75}
.yard-form input,.yard-form textarea{width:100%;box-sizing:border-box;font:inherit;font-size:16px;padding:11px 12px;border:1px solid rgba(14,48,66,.25);border-radius:6px;background:#fff;color:#0E3042}
.yard-form textarea{min-height:120px;resize:vertical}
.yard-form input:focus-visible,.yard-form textarea:focus-visible{outline:2px solid #0B766B;outline-offset:1px}
.yard-form .help{font-size:13.5px;line-height:1.5;opacity:.85;margin:0}
.yard-form button{font:inherit;font-weight:600;background:#0B766B;color:#fff;border:0;border-radius:6px;padding:12px 22px;cursor:pointer}
.yard-form button:disabled{opacity:.6;cursor:default}
@media (max-width:640px){.yard-form{grid-template-columns:1fr}}
</style>
'''

def build_astilleros():
    for lang in YARD_LANGS:
        d = A[lang]; F = d['f']; path = '/astilleros/'
        url = BASE + PRE[lang] + path
        schema = {"@context": "https://schema.org", "@type": "WebPage", "name": d['h1'], "description": d['desc'], "inLanguage": lang, "url": url,
                  "author": {"@type": "Person", "name": "Juan Morante"}, "publisher": {"@type": "Organization", "name": "Plata Marine"}, "dateModified": TODAY}
        crumbs = [(d['crumbs'][0], BASE + PRE[lang] + '/'), (d['crumbs'][1], url)]
        H, Fo = shell(lang)
        H = fix_header(H, lang, path, d['wa'], langs=YARD_LANGS)
        if lang == 'it':
            H = H.replace('<html lang="en">', '<html lang="it">')
        def fld(id_, lab, ph, req=True, typ='text', span=False, extra=''):
            star = ' <i>*</i>' if req else ' <small>(%s)</small>' % F['opt']
            return '<div class="%s"><label for="%s">%s%s</label><input id="%s" name="%s" type="%s" placeholder="%s"%s%s></div>' % (
                'span2' if span else '', id_, lab, star, id_, id_, typ, ph, ' required' if req else '', extra)
        form = ('<form id="astilleroForm" class="yard-form" novalidate data-contact-intent="yard">'
                + fld('ya_yard', F['yard'], F['ph_yard'], extra=' autocomplete="organization" maxlength="80"')
                + fld('ya_web', F['web'], F['ph_web'], req=False, typ='url', extra=' inputmode="url" maxlength="120"')
                + fld('ya_name', F['name'], F['ph_name'], extra=' autocomplete="name" maxlength="60"')
                + fld('ya_role', F['role'], F['ph_role'], req=False, extra=' autocomplete="organization-title" maxlength="60"')
                + fld('ya_email', F['email'], F['ph_email'], typ='email', extra=' autocomplete="email" maxlength="100"')
                + fld('ya_tel', F['tel'], F['ph_tel'], typ='tel', extra=' autocomplete="tel" inputmode="tel" maxlength="20"')
                + fld('ya_country', F['country'], F['ph_country'], req=False, extra=' autocomplete="country-name" maxlength="40"')
                + '<div></div>'
                + '<div class="span2"><label for="ya_msg">%s <small>(%s)</small></label><textarea id="ya_msg" name="ya_msg" maxlength="1500" placeholder="%s"></textarea></div>' % (F['msg'], F['opt'], F['ph_msg'])
                + '<p class="help span2">%s</p>' % F['legal']
                + '<div class="span2"><button type="submit" id="ya_send">%s</button></div>' % F['send']
                + '<p class="help span2">%s</p>' % F['req']
                + '<p id="ya_status" class="help span2" role="status" aria-live="polite" hidden></p>'
                + '</form>')
        toc_ids = ['como', 'aporto', 'encaje', 'escribeme']
        toc = ''.join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in zip(toc_ids, d['toc']))
        main = '''<main class="art">
  <div class="wrap">
    <article>
      <header>
        <p class="eyebrow">%s</p>
        <h1>%s</h1>
        <div class="meta"><span>%s</span><span>%s</span></div>
        <p class="lead">%s</p>
      </header>
      <div class="prose">
%s
        <h2 id="escribeme">%s</h2>
        <p>%s</p>
        %s
        <p style="font-size:13px;opacity:.75;margin-top:22px">%s</p>
      </div>
    </article>
    <aside class="aside" aria-label="Contacto">
      <div class="card">
        <p class="eyebrow">%s</p>
        <h3>%s</h3>
        <p>%s</p>
        <a class="btn btn-wa" href="%s" target="_blank" rel="noopener">%s</a>
      </div>
      <nav class="toc" aria-label="Contenido"><ol>%s</ol></nav>
    </aside>
  </div>
</main>''' % (d['eyebrow'], d['h1'], d['meta'][0], d['meta'][1], d['lead'], d['body'], d['form_title'], d['form_intro'], form, d['fine'],
              d['aside_eyebrow'], d['aside_h'], d['aside_p'], wa(d['wa']), d['aside_btn'], toc)
        Fo = Fo.replace('<script src="/analytics.js', '<script src="/astilleros/astilleros.js?v=20261011" defer></script>\n<script src="/analytics.js')
        out = head(lang, path, d['title'], d['desc'], schema, crumbs, FORM_CSS, langs=YARD_LANGS) + H + main + Fo
        dest = os.path.join(ROOT, ('' if lang == 'es' else lang + '/') + 'astilleros/index.html')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'w', encoding='utf-8').write(out)
        print('ok', dest)

# ---------------------------------------------------------------- GUÍA CHÁRTER
G = {
'es': dict(
  title='¿Puedo alquilar mi barco para pagar los gastos? Lo que dice la ley en 2026',
  desc='Alquilar tu barco particular en España: lista 6ª o cambio temporal de la 7ª (máx. 3 meses), empresa gestora, seguros, IAE, IVA e IEDMT, y la prohibición de Baleares.',
  h1='¿Puedo alquilar mi barco para pagar los gastos?', eyebrow='Guías · Alquiler',
  meta=['Por Juan Morante', 'Actualizado octubre 2026', '8 min de lectura'],
  lead='Es una de las preguntas que más me hacen los propietarios: “¿y si lo alquilo unas semanas en verano y así cubro el amarre?”. Se puede, pero no como mucha gente se imagina. Aquí tienes lo que dice la normativa a octubre de 2026, con sus fuentes, para que decidas con los números delante.',
  crumb='Alquilar mi barco: lo que dice la ley',
  body='''<h2 id="corta">La respuesta corta</h2>
<p>Un particular no puede alquilar su barco “de vez en cuando” y cobrar sin más. Alquilar una embarcación de recreo es una actividad económica: hay que estar dado de alta, cumplir requisitos de seguridad y seguros más exigentes y declarar los ingresos. Hay dos caminos, y ninguno permite seguir usando el barco como siempre mientras está alquilado.</p>
<h2 id="caminos">Los dos caminos legales</h2>
<p><strong>1. Pasar el barco a lista 6ª (uso comercial).</strong> Es la vía de las empresas de chárter: el barco se dedica al alquiler, pasa las inspecciones de embarcación comercial y lleva los seguros correspondientes. Te explico las diferencias entre listas en la guía de <a href="lista-6-y-lista-7.html">lista 6ª y lista 7ª</a>.</p>
<p><strong>2. El cambio temporal a uso comercial, sin salir de la lista 7ª.</strong> Desde el 31 de diciembre de 2025 lo regula el Real Decreto 1188/2025, que modificó el artículo 9 del Reglamento de Ordenación de la Navegación Marítima (RD 186/2023). Sus condiciones:</p>
<ul>
<li>Como máximo <strong>3 meses consecutivos por año natural</strong>.</li>
<li>El barco lo tiene que gestionar una <strong>empresa de arrendamiento náutico</strong> con contrato de gestión, y es ella quien pide la autorización.</li>
<li>Durante ese periodo, <strong>ni el propietario ni personas vinculadas pueden usarlo ni trabajar a bordo</strong> (salvo tripulación profesional enrolada de forma permanente).</li>
<li>Pasa por el régimen de reconocimientos de la lista 6ª, lleva “CT” delante de la matrícula en ambas amuras y necesita seguro de accidentes para todas las personas a bordo.</li>
</ul>
<h2 id="requisitos">Requisitos que se aplican siempre</h2>
<ul>
<li><strong>Máximo 12 pasajeros</strong> además de la tripulación. Por encima, ya es normativa de buques de pasaje.</li>
<li><strong>Sin patrón:</strong> quien alquila responde de que el que gobierna tenga la titulación necesaria.</li>
<li><strong>Con patrón:</strong> el patrón y la tripulación necesitan titulación profesional, no basta con un título de recreo.</li>
<li><strong>Despacho:</strong> declaración responsable, lista de tripulantes, pólizas en vigor y estar al corriente de impuestos.</li>
<li><strong>Seguro de responsabilidad civil</strong> con los mínimos del RD 607/1999 (120.202,42 € por víctima y 240.404,84 € por siniestro en daños personales; 96.161,94 € en daños materiales) y <strong>seguro de accidentes</strong> de los pasajeros (RD 1575/1989).</li>
<li><strong>Alta en el epígrafe 855.2 del IAE</strong> (“Alquiler de embarcaciones”), aunque sea un solo barco, según la consulta vinculante de Hacienda V0249-05. Para un particular, eso significa hacerlo como autónomo.</li>
</ul>
<h2 id="baleares">Baleares: el alquiler con la lista 7ª está prohibido</h2>
<p>El Decreto 44/2025 del Govern balear (BOIB de 2 de agosto de 2025) exige la lista 6ª para alquilar y <strong>prohíbe el cambio temporal a uso comercial</strong>, así como el alquiler por plazas. Además pide declaración responsable, inscripción en el registro balear, tasa, acreditar el amarre o la autorización portuaria, seguros, contrato con el número de declaración, registro de pasajeros y una bandera numérica a bordo.</p>
<p>El decreto está recurrido, pero el Tribunal Superior de Justicia de Baleares rechazó suspenderlo el 8 de enero de 2026, así que sigue en vigor. Y se vigila: en 2025 el Govern abrió 162 expedientes por alquiler irregular, con 471.600 € en multas propuestas. Recuerda también que fondear sobre posidonia está prohibido (Decreto 25/2018).</p>
<h2 id="cataluna">Cataluña</h2>
<p>No he encontrado una norma catalana propia como la balear. Mientras no se publique, se aplica la estatal: lista 6ª o cambio temporal de la 7ª con empresa gestora y un máximo de 3 meses. Antes de dar ningún paso, confírmalo con la Capitanía Marítima de tu zona y con el puerto, porque no todos los amarres admiten actividad comercial.</p>
<h2 id="fiscal">Impuestos: lo que más se pasa por alto</h2>
<ul>
<li><strong>IVA:</strong> el alquiler lleva el 21 %.</li>
<li><strong>Impuesto de matriculación (IEDMT):</strong> los barcos dedicados <em>efectiva y exclusivamente</em> al alquiler pueden estar exentos, con reconocimiento previo de Hacienda (art. 66 de la Ley 38/1992). Si el propietario o alguien vinculado lo usa para sí, deja de haber alquiler y se pierde la exención (consulta V1307-2025). Lo explico en la guía del <a href="impuesto-matriculacion-barcos.html">impuesto de matriculación</a>.</li>
<li><strong>IVA de la compra:</strong> solo se puede deducir si la actividad empresarial es real desde el principio y se puede demostrar. Con un uso mixto (unas semanas alquilado y el resto para ti) no hay un criterio claro: consúltalo con tu asesor antes de comprar.</li>
<li><strong>IRPF:</strong> lo que ingreses es rendimiento de actividad económica y se declara como tal.</li>
</ul>
<h2 id="numeros">Lo que nadie te cuenta</h2>
<p>Los ingresos que se anuncian suelen ser brutos. Antes de echar cuentas, pregunta por todo lo que se come el margen: la parte de la empresa gestora, un seguro más caro, las inspecciones adicionales, el desgaste de motor e interiores, la limpieza entre clientes y una temporada que, en la práctica, se concentra en pocas semanas. No pongo cifras porque cambian mucho según barco, zona y gestora: pídelas por escrito.</p>
<h2 id="compensa">Entonces, ¿me compensa?</h2>
<p>Depende de qué quieras. Si compras un barco pensando en explotarlo, con números hechos y una gestora seria, puede tener sentido. Si lo que quieres es navegar tú y que el alquiler “pague el amarre”, choca con la ley: en los meses de alquiler no puedes usarlo, y en Baleares no puedes hacerlo con la lista 7ª. A veces lo sensato es elegir un barco cuyos gastos puedas asumir solo; para eso tienes la <a href="/herramientas/coste-mantener-barco.html">calculadora de lo que cuesta mantener un barco</a>.</p>''',
  fine='Información orientativa basada en el RD 186/2023 (modificado por el RD 1188/2025), el RD 607/1999, el RD 1575/1989, la Ley 38/1992, el Decreto balear 44/2025 y consultas de la Dirección General de Tributos, revisada en octubre de 2026. No es asesoramiento legal ni fiscal, y la normativa puede cambiar. Confírmalo con Capitanía Marítima, tu gestoría o un abogado antes de alquilar.',
  next_eyebrow='Siguiente paso', next_p='<strong>¿Te planteas cambiar de barco?</strong> Te digo con calma qué vale el tuyo y qué opciones tienes.', next_btn='Vender mi barco', next_href='/vender-barco/',
  aside_eyebrow='¿Dudas con tu caso?', aside_h='Cuéntame tu barco y te digo qué mirar.', aside_p='Eslora, lista, dónde está amarrado y qué te planteas. Sin compromiso.', aside_btn='Hablar con Juan por WhatsApp',
  wa='Hola Juan, tengo una duda sobre alquilar mi barco.',
  toc=['La respuesta corta', 'Los dos caminos legales', 'Requisitos de siempre', 'Baleares', 'Cataluña', 'Impuestos', 'Lo que nadie te cuenta', '¿Me compensa?'],
  rel=[('lista-6-y-lista-7.html', 'Lista 6ª y lista 7ª'), ('impuesto-matriculacion-barcos.html', 'Impuesto de matriculación (IEDMT)'), ('./', 'Todas las guías de Plata Marine')],
  card=('Alquiler', '¿Puedo alquilar mi barco para pagar los gastos?', 'Lista 6ª o cambio temporal de la 7ª, empresa gestora, seguros, impuestos y la prohibición de Baleares, con las normas de 2026.')),
'ca': dict(
  title='Puc llogar el meu vaixell per pagar les despeses? El que diu la llei el 2026',
  desc='Llogar el teu vaixell particular a Espanya: llista 6a o canvi temporal de la 7a (màx. 3 mesos), empresa gestora, assegurances, IAE, IVA i IEDMT, i la prohibició de Balears.',
  h1='Puc llogar el meu vaixell per pagar les despeses?', eyebrow='Guies · Lloguer',
  meta=['Per Juan Morante', 'Actualitzat octubre 2026', '8 min de lectura'],
  lead='És una de les preguntes que més em fan els propietaris: “i si el llogo unes setmanes a l’estiu i així cobreixo l’amarratge?”. Es pot, però no com molta gent s’imagina. Aquí tens el que diu la normativa a octubre de 2026, amb les fonts, perquè decideixis amb els números al davant.',
  crumb='Llogar el meu vaixell: el que diu la llei',
  body='''<h2 id="corta">La resposta curta</h2>
<p>Un particular no pot llogar el seu vaixell “de tant en tant” i cobrar sense més. Llogar una embarcació d’esbarjo és una activitat econòmica: cal estar donat d’alta, complir requisits de seguretat i assegurances més exigents i declarar els ingressos. Hi ha dos camins, i cap no permet continuar fent servir el vaixell com sempre mentre està llogat.</p>
<h2 id="caminos">Els dos camins legals</h2>
<p><strong>1. Passar el vaixell a la llista 6a (ús comercial).</strong> És la via de les empreses de xàrter: el vaixell es dedica al lloguer, passa les inspeccions d’embarcació comercial i porta les assegurances corresponents. T’explico les diferències entre llistes a la guia de la <a href="lista-6-y-lista-7.html">llista 6a i la llista 7a</a>.</p>
<p><strong>2. El canvi temporal a ús comercial, sense sortir de la llista 7a.</strong> Des del 31 de desembre de 2025 el regula el Reial decret 1188/2025, que va modificar l’article 9 del Reglament d’ordenació de la navegació marítima (RD 186/2023). Les condicions:</p>
<ul>
<li>Com a màxim <strong>3 mesos consecutius per any natural</strong>.</li>
<li>El vaixell l’ha de gestionar una <strong>empresa d’arrendament nàutic</strong> amb contracte de gestió, i és ella qui demana l’autorització.</li>
<li>Durant aquest període, <strong>ni el propietari ni persones vinculades el poden fer servir ni treballar-hi a bord</strong> (excepte tripulació professional enrolada de manera permanent).</li>
<li>Passa pel règim de reconeixements de la llista 6a, porta “CT” davant de la matrícula a totes dues amures i necessita assegurança d’accidents per a totes les persones a bord.</li>
</ul>
<h2 id="requisitos">Requisits que s’apliquen sempre</h2>
<ul>
<li><strong>Màxim 12 passatgers</strong> a més de la tripulació. Per sobre, ja és normativa de vaixells de passatge.</li>
<li><strong>Sense patró:</strong> qui lloga respon que qui governa tingui la titulació necessària.</li>
<li><strong>Amb patró:</strong> el patró i la tripulació necessiten titulació professional; no n’hi ha prou amb un títol d’esbarjo.</li>
<li><strong>Despatx:</strong> declaració responsable, llista de tripulants, pòlisses en vigor i estar al corrent d’impostos.</li>
<li><strong>Assegurança de responsabilitat civil</strong> amb els mínims del RD 607/1999 (120.202,42 € per víctima i 240.404,84 € per sinistre en danys personals; 96.161,94 € en danys materials) i <strong>assegurança d’accidents</strong> dels passatgers (RD 1575/1989).</li>
<li><strong>Alta a l’epígraf 855.2 de l’IAE</strong> (“Lloguer d’embarcacions”), encara que sigui un sol vaixell, segons la consulta vinculant d’Hisenda V0249-05. Per a un particular, això vol dir fer-ho com a autònom.</li>
</ul>
<h2 id="baleares">Balears: el lloguer amb la llista 7a està prohibit</h2>
<p>El Decret 44/2025 del Govern balear (BOIB del 2 d’agost de 2025) exigeix la llista 6a per llogar i <strong>prohibeix el canvi temporal a ús comercial</strong>, així com el lloguer per places. A més demana declaració responsable, inscripció al registre balear, taxa, acreditar l’amarratge o l’autorització portuària, assegurances, contracte amb el número de declaració, registre de passatgers i una bandera numèrica a bord.</p>
<p>El decret està recorregut, però el Tribunal Superior de Justícia de les Illes Balears va rebutjar suspendre’l el 8 de gener de 2026, de manera que continua vigent. I es vigila: el 2025 el Govern va obrir 162 expedients per lloguer irregular, amb 471.600 € en multes proposades. Recorda també que fondejar sobre posidònia està prohibit (Decret 25/2018).</p>
<h2 id="cataluna">Catalunya</h2>
<p>No he trobat una norma catalana pròpia com la balear. Mentre no se’n publiqui cap, s’aplica l’estatal: llista 6a o canvi temporal de la 7a amb empresa gestora i un màxim de 3 mesos. Abans de fer cap pas, confirma-ho amb la Capitania Marítima de la teva zona i amb el port, perquè no tots els amarratges admeten activitat comercial.</p>
<h2 id="fiscal">Impostos: el que més es passa per alt</h2>
<ul>
<li><strong>IVA:</strong> el lloguer porta el 21 %.</li>
<li><strong>Impost de matriculació (IEDMT):</strong> els vaixells dedicats <em>efectivament i exclusivament</em> al lloguer poden estar-ne exempts, amb reconeixement previ d’Hisenda (art. 66 de la Llei 38/1992). Si el propietari o algú vinculat el fa servir per a si mateix, deixa d’haver-hi lloguer i es perd l’exempció (consulta V1307-2025). Ho explico a la guia de l’<a href="impuesto-matriculacion-barcos.html">impost de matriculació</a>.</li>
<li><strong>IVA de la compra:</strong> només es pot deduir si l’activitat empresarial és real des del principi i es pot demostrar. Amb un ús mixt (unes setmanes llogat i la resta per a tu) no hi ha un criteri clar: consulta-ho amb el teu assessor abans de comprar.</li>
<li><strong>IRPF:</strong> el que ingressis és rendiment d’activitat econòmica i es declara com a tal.</li>
</ul>
<h2 id="numeros">El que ningú no t’explica</h2>
<p>Els ingressos que s’anuncien solen ser bruts. Abans de fer comptes, pregunta per tot el que es menja el marge: la part de l’empresa gestora, una assegurança més cara, les inspeccions addicionals, el desgast de motor i interiors, la neteja entre clients i una temporada que, a la pràctica, es concentra en poques setmanes. No poso xifres perquè canvien molt segons el vaixell, la zona i la gestora: demana-les per escrit.</p>
<h2 id="compensa">Aleshores, em compensa?</h2>
<p>Depèn del que vulguis. Si compres un vaixell pensant a explotar-lo, amb els números fets i una gestora seriosa, pot tenir sentit. Si el que vols és navegar tu i que el lloguer “pagui l’amarratge”, xoca amb la llei: els mesos de lloguer no el pots fer servir, i a Balears no ho pots fer amb la llista 7a. De vegades el més assenyat és triar un vaixell les despeses del qual puguis assumir tu sol; per a això tens la <a href="/ca/herramientas/coste-mantener-barco.html">calculadora del que costa mantenir un vaixell</a>.</p>''',
  fine='Informació orientativa basada en el RD 186/2023 (modificat pel RD 1188/2025), el RD 607/1999, el RD 1575/1989, la Llei 38/1992, el Decret balear 44/2025 i consultes de la Direcció General de Tributs, revisada l’octubre de 2026. No és assessorament legal ni fiscal, i la normativa pot canviar. Confirma-ho amb Capitania Marítima, la teva gestoria o un advocat abans de llogar.',
  next_eyebrow='Següent pas', next_p='<strong>Et plantejes canviar de vaixell?</strong> Et dic amb calma què val el teu i quines opcions tens.', next_btn='Vendre el meu vaixell', next_href='/ca/vender-barco/',
  aside_eyebrow='Dubtes amb el teu cas?', aside_h='Explica’m el teu vaixell i et dic què mirar.', aside_p='Eslora, llista, on és amarrat i què et planteges. Sense compromís.', aside_btn='Parla amb en Juan per WhatsApp',
  wa='Hola Juan, tinc un dubte sobre llogar el meu vaixell.',
  toc=['La resposta curta', 'Els dos camins legals', 'Requisits de sempre', 'Balears', 'Catalunya', 'Impostos', 'El que ningú no t’explica', 'Em compensa?'],
  rel=[('lista-6-y-lista-7.html', 'Llista 6a i llista 7a'), ('impuesto-matriculacion-barcos.html', 'Impost de matriculació (IEDMT)'), ('./', 'Totes les guies de Plata Marine')],
  card=('Lloguer', 'Puc llogar el meu vaixell per pagar les despeses?', 'Llista 6a o canvi temporal de la 7a, empresa gestora, assegurances, impostos i la prohibició de Balears, amb les normes del 2026.')),
'en': dict(
  title='Can I charter out my boat to cover the costs? Spanish rules in 2026',
  desc='Renting out your private boat in Spain: list 6 or the temporary switch from list 7 (max. 3 months), management company, insurance, tax registration, VAT, IEDMT and the Balearic ban.',
  h1='Can I charter out my boat to cover the costs?', eyebrow='Guides · Charter',
  meta=['By Juan Morante', 'Updated October 2026', '8 min read'],
  lead='It’s one of the questions owners ask me most: “what if I rent it out for a few weeks in summer to cover the berth?”. It can be done, but not the way many people imagine. Here is what Spanish regulations say as of October 2026, with sources, so you can decide with the numbers in front of you.',
  crumb='Chartering out my boat: what the law says',
  body='''<h2 id="corta">The short answer</h2>
<p>A private owner can’t simply rent out their boat “now and then” and get paid. Renting out a recreational boat is a business activity: you have to be registered, meet stricter safety and insurance requirements and declare the income. There are two routes, and neither lets you keep using the boat as usual while it’s being rented.</p>
<h2 id="caminos">The two legal routes</h2>
<p><strong>1. Move the boat to list 6 (commercial use).</strong> This is the route charter companies take: the boat is dedicated to rental, passes commercial vessel inspections and carries the corresponding insurance. I explain the differences between lists in the guide to <a href="lista-6-y-lista-7.html">list 6 and list 7</a>.</p>
<p><strong>2. The temporary switch to commercial use, staying on list 7.</strong> Since 31 December 2025 it has been governed by Royal Decree 1188/2025, which amended article 9 of the Maritime Navigation Regulation (RD 186/2023). The conditions:</p>
<ul>
<li>A maximum of <strong>3 consecutive months per calendar year</strong>.</li>
<li>The boat must be managed by a <strong>charter company</strong> under a management contract, and it is that company that applies for authorisation.</li>
<li>During that period, <strong>neither the owner nor related persons may use it or work on board</strong> (except professional crew permanently signed on).</li>
<li>It follows the list 6 inspection regime, carries “CT” before the registration number on both bows and needs accident insurance for everyone on board.</li>
</ul>
<h2 id="requisitos">Requirements that always apply</h2>
<ul>
<li><strong>Maximum 12 passengers</strong> plus crew. Above that, passenger ship rules apply.</li>
<li><strong>Bareboat:</strong> the charterer is responsible for whoever skippers holding the required licence.</li>
<li><strong>Skippered:</strong> the skipper and crew need professional qualifications; a recreational licence is not enough.</li>
<li><strong>Clearance:</strong> responsible declaration, crew list, valid policies and being up to date with taxes.</li>
<li><strong>Third-party liability insurance</strong> with the minimums of RD 607/1999 (€120,202.42 per victim and €240,404.84 per incident for personal injury; €96,161.94 for property damage) and <strong>passenger accident insurance</strong> (RD 1575/1989).</li>
<li><strong>Registration under IAE heading 855.2</strong> (“Boat rental”), even for a single boat, according to binding tax ruling V0249-05. For a private individual, that means doing it as self-employed (autónomo).</li>
</ul>
<h2 id="baleares">Balearic Islands: chartering on list 7 is banned</h2>
<p>Balearic Decree 44/2025 (BOIB, 2 August 2025) requires list 6 for charter and <strong>bans the temporary switch to commercial use</strong>, as well as selling individual seats. It also requires a responsible declaration, entry in the Balearic register, a fee, proof of berth or port authorisation, insurance, a contract showing the declaration number, a passenger log and a numbered flag on board.</p>
<p>The decree has been challenged, but the Balearic High Court refused to suspend it on 8 January 2026, so it remains in force. And it is enforced: in 2025 the regional government opened 162 cases for illegal charter, with €471,600 in proposed fines. Remember too that anchoring on posidonia seagrass is prohibited (Decree 25/2018).</p>
<h2 id="cataluna">Catalonia</h2>
<p>I haven’t found a specific Catalan regulation like the Balearic one. Until one is published, national rules apply: list 6 or the temporary switch from list 7 with a management company and a maximum of 3 months. Before taking any step, check with the Harbour Master’s Office (Capitanía Marítima) in your area and with your port, because not every berth allows commercial activity.</p>
<h2 id="fiscal">Tax: what most people overlook</h2>
<ul>
<li><strong>VAT:</strong> charter is subject to 21%.</li>
<li><strong>Registration tax (IEDMT):</strong> boats used <em>effectively and exclusively</em> for charter can be exempt, with prior recognition by the tax office (art. 66 of Law 38/1992). If the owner or a related person uses it privately, it no longer counts as rental and the exemption is lost (ruling V1307-2025). I explain it in the guide to the <a href="impuesto-matriculacion-barcos.html">registration tax</a>.</li>
<li><strong>VAT on the purchase:</strong> only deductible if the business activity is genuine from the start and can be proven. For mixed use (a few weeks chartered, the rest for you) there is no clear criterion: check with your adviser before buying.</li>
<li><strong>Income tax:</strong> what you earn is business income and must be declared as such.</li>
</ul>
<h2 id="numeros">What nobody tells you</h2>
<p>Advertised earnings are usually gross. Before doing the maths, ask about everything that eats into the margin: the management company’s share, pricier insurance, extra inspections, wear on engines and interiors, cleaning between clients and a season that in practice is concentrated into a few weeks. I don’t give figures because they vary a lot by boat, area and company: ask for them in writing.</p>
<h2 id="compensa">So, is it worth it?</h2>
<p>It depends on what you want. If you buy a boat to run it as a business, with the numbers done and a serious management company, it can make sense. If what you want is to sail yourself and have charter “pay for the berth”, it clashes with the law: during the charter months you can’t use it, and in the Balearics you can’t do it on list 7. Sometimes the sensible thing is to choose a boat whose costs you can cover on your own; for that you have the <a href="/en/herramientas/coste-mantener-barco.html">boat running cost calculator</a>.</p>''',
  fine='General information based on RD 186/2023 (amended by RD 1188/2025), RD 607/1999, RD 1575/1989, Law 38/1992, Balearic Decree 44/2025 and rulings of the Spanish Directorate General of Taxes, reviewed in October 2026. This is not legal or tax advice and regulations may change. Check with the Harbour Master’s Office, your gestoría or a lawyer before chartering.',
  next_eyebrow='Next step', next_p='<strong>Thinking about changing boats?</strong> I’ll calmly tell you what yours is worth and what your options are.', next_btn='Sell my boat', next_href='/en/vender-barco/',
  aside_eyebrow='Questions about your case?', aside_h='Tell me about your boat and I’ll tell you what to check.', aside_p='Length, list, where it’s berthed and what you have in mind. No obligation.', aside_btn='Talk to Juan on WhatsApp',
  wa='Hi Juan, I have a question about chartering out my boat.',
  toc=['The short answer', 'The two legal routes', 'Requirements that always apply', 'Balearic Islands', 'Catalonia', 'Tax', 'What nobody tells you', 'Is it worth it?'],
  rel=[('lista-6-y-lista-7.html', 'List 6 and list 7'), ('impuesto-matriculacion-barcos.html', 'Registration tax (IEDMT)'), ('./', 'All Plata Marine guides')],
  card=('Charter', 'Can I charter out my boat to cover the costs?', 'List 6 or the temporary switch from list 7, management company, insurance, tax and the Balearic ban, under the 2026 rules.')),
'fr': dict(
  title='Puis-je louer mon bateau pour couvrir les frais ? Règles en Espagne en 2026',
  desc='Louer votre bateau privé en Espagne : liste 6 ou passage temporaire de la liste 7 (3 mois max.), société de gestion, assurances, IAE, TVA, IEDMT et interdiction aux Baléares.',
  h1='Puis-je louer mon bateau pour couvrir les frais ?', eyebrow='Guides · Location',
  meta=['Par Juan Morante', 'Mis à jour en octobre 2026', '8 min de lecture'],
  lead='C’est l’une des questions que les propriétaires me posent le plus : « et si je le louais quelques semaines l’été pour payer la place de port ? ». C’est possible, mais pas comme beaucoup l’imaginent. Voici ce que dit la réglementation espagnole en octobre 2026, avec les sources, pour décider en ayant les chiffres sous les yeux.',
  crumb='Louer mon bateau : ce que dit la loi',
  body='''<h2 id="corta">La réponse courte</h2>
<p>Un particulier ne peut pas louer son bateau « de temps en temps » et encaisser sans plus. Louer un bateau de plaisance est une activité économique : il faut être déclaré, respecter des exigences de sécurité et d’assurance plus strictes et déclarer les revenus. Il existe deux voies, et aucune ne permet de continuer à utiliser le bateau comme d’habitude pendant qu’il est loué.</p>
<h2 id="caminos">Les deux voies légales</h2>
<p><strong>1. Passer le bateau en liste 6 (usage commercial).</strong> C’est la voie des sociétés de location : le bateau est consacré à la location, passe les inspections de navire commercial et dispose des assurances correspondantes. J’explique les différences entre les listes dans le guide <a href="lista-6-y-lista-7.html">liste 6 et liste 7</a>.</p>
<p><strong>2. Le passage temporaire à l’usage commercial, en restant en liste 7.</strong> Depuis le 31 décembre 2025, il est encadré par le décret royal 1188/2025, qui a modifié l’article 9 du règlement espagnol sur la navigation maritime (RD 186/2023). Les conditions :</p>
<ul>
<li><strong>3 mois consécutifs maximum par année civile</strong>.</li>
<li>Le bateau doit être géré par une <strong>société de location nautique</strong> sous contrat de gestion, et c’est elle qui demande l’autorisation.</li>
<li>Pendant cette période, <strong>ni le propriétaire ni les personnes liées ne peuvent l’utiliser ni travailler à bord</strong> (sauf équipage professionnel enrôlé en permanence).</li>
<li>Il suit le régime d’inspections de la liste 6, porte « CT » devant l’immatriculation sur les deux joues et doit avoir une assurance accidents pour toutes les personnes à bord.</li>
</ul>
<h2 id="requisitos">Les exigences qui s’appliquent toujours</h2>
<ul>
<li><strong>12 passagers maximum</strong> en plus de l’équipage. Au-delà, ce sont les règles des navires à passagers.</li>
<li><strong>Sans skipper :</strong> le locataire répond du fait que la personne qui barre ait le permis requis.</li>
<li><strong>Avec skipper :</strong> le skipper et l’équipage doivent avoir un titre professionnel ; un permis de plaisance ne suffit pas.</li>
<li><strong>Formalités de départ :</strong> déclaration responsable, liste d’équipage, polices en vigueur et être à jour de ses impôts.</li>
<li><strong>Assurance responsabilité civile</strong> avec les minimums du RD 607/1999 (120 202,42 € par victime et 240 404,84 € par sinistre pour les dommages corporels ; 96 161,94 € pour les dommages matériels) et <strong>assurance accidents</strong> des passagers (RD 1575/1989).</li>
<li><strong>Inscription à la rubrique 855.2 de l’IAE</strong> (« Location de bateaux »), même pour un seul bateau, selon la réponse fiscale contraignante V0249-05. Pour un particulier, cela veut dire le faire en tant qu’indépendant (autónomo).</li>
</ul>
<h2 id="baleares">Baléares : la location en liste 7 est interdite</h2>
<p>Le décret baléare 44/2025 (BOIB du 2 août 2025) impose la liste 6 pour louer et <strong>interdit le passage temporaire à l’usage commercial</strong>, ainsi que la vente de places à l’unité. Il exige aussi une déclaration responsable, l’inscription au registre baléare, une taxe, la preuve de la place de port ou d’une autorisation portuaire, les assurances, un contrat mentionnant le numéro de déclaration, un registre des passagers et un pavillon numéroté à bord.</p>
<p>Le décret fait l’objet de recours, mais le Tribunal supérieur de justice des Baléares a refusé de le suspendre le 8 janvier 2026 : il reste donc en vigueur. Et il est appliqué : en 2025, le gouvernement régional a ouvert 162 dossiers pour location irrégulière, avec 471 600 € d’amendes proposées. Rappelez-vous aussi qu’il est interdit de mouiller sur la posidonie (décret 25/2018).</p>
<h2 id="cataluna">Catalogne</h2>
<p>Je n’ai pas trouvé de réglementation catalane spécifique comme celle des Baléares. Tant qu’il n’y en a pas, ce sont les règles nationales qui s’appliquent : liste 6 ou passage temporaire de la liste 7 avec une société de gestion et 3 mois maximum. Avant toute démarche, vérifiez auprès de la Capitanía Marítima de votre zone et de votre port, car toutes les places n’admettent pas d’activité commerciale.</p>
<h2 id="fiscal">Fiscalité : ce qu’on oublie le plus souvent</h2>
<ul>
<li><strong>TVA :</strong> la location est soumise à 21 %.</li>
<li><strong>Taxe d’immatriculation (IEDMT) :</strong> les bateaux consacrés <em>effectivement et exclusivement</em> à la location peuvent en être exonérés, avec reconnaissance préalable par l’administration fiscale (art. 66 de la loi 38/1992). Si le propriétaire ou une personne liée l’utilise pour lui-même, il n’y a plus location et l’exonération est perdue (réponse V1307-2025). Je l’explique dans le guide de la <a href="impuesto-matriculacion-barcos.html">taxe d’immatriculation</a>.</li>
<li><strong>TVA de l’achat :</strong> déductible uniquement si l’activité professionnelle est réelle dès le départ et peut être prouvée. En usage mixte (quelques semaines en location, le reste pour vous), il n’y a pas de critère clair : consultez votre conseiller avant d’acheter.</li>
<li><strong>Impôt sur le revenu :</strong> ce que vous encaissez est un revenu d’activité et se déclare comme tel.</li>
</ul>
<h2 id="numeros">Ce que personne ne vous dit</h2>
<p>Les revenus annoncés sont généralement bruts. Avant de faire vos calculs, renseignez-vous sur tout ce qui réduit la marge : la part de la société de gestion, une assurance plus chère, les inspections supplémentaires, l’usure du moteur et des intérieurs, le nettoyage entre deux clients et une saison qui, en pratique, se concentre sur quelques semaines. Je ne donne pas de chiffres car ils varient beaucoup selon le bateau, la zone et la société : demandez-les par écrit.</p>
<h2 id="compensa">Alors, est-ce que ça vaut le coup ?</h2>
<p>Tout dépend de ce que vous voulez. Si vous achetez un bateau pour l’exploiter, avec des chiffres sérieux et une société de gestion fiable, cela peut avoir du sens. Si vous voulez naviguer vous-même et que la location « paie la place de port », cela se heurte à la loi : pendant les mois de location vous ne pouvez pas l’utiliser, et aux Baléares c’est impossible en liste 7. Parfois, le plus raisonnable est de choisir un bateau dont vous pouvez assumer seul les frais ; pour cela, vous avez le <a href="/fr/herramientas/coste-mantener-barco.html">calculateur du coût d’un bateau</a>.</p>''',
  fine='Information indicative fondée sur le RD 186/2023 (modifié par le RD 1188/2025), le RD 607/1999, le RD 1575/1989, la loi 38/1992, le décret baléare 44/2025 et des réponses de la Direction générale des impôts espagnole, revue en octobre 2026. Ce n’est pas un conseil juridique ni fiscal, et la réglementation peut changer. Vérifiez auprès de la Capitanía Marítima, de votre gestoría ou d’un avocat avant de louer.',
  next_eyebrow='Étape suivante', next_p='<strong>Vous pensez changer de bateau ?</strong> Je vous dis tranquillement ce que vaut le vôtre et quelles sont vos options.', next_btn='Vendre mon bateau', next_href='/fr/vender-barco/',
  aside_eyebrow='Des questions sur votre cas ?', aside_h='Parlez-moi de votre bateau et je vous dis quoi vérifier.', aside_p='Longueur, liste, port d’attache et ce que vous envisagez. Sans engagement.', aside_btn='Parler avec Juan sur WhatsApp',
  wa='Bonjour Juan, j’ai une question sur la location de mon bateau.',
  toc=['La réponse courte', 'Les deux voies légales', 'Les exigences de toujours', 'Baléares', 'Catalogne', 'Fiscalité', 'Ce que personne ne vous dit', 'Est-ce que ça vaut le coup ?'],
  rel=[('lista-6-y-lista-7.html', 'Liste 6 et liste 7'), ('impuesto-matriculacion-barcos.html', 'Taxe d’immatriculation (IEDMT)'), ('./', 'Tous les guides Plata Marine')],
  card=('Location', 'Puis-je louer mon bateau pour couvrir les frais ?', 'Liste 6 ou passage temporaire de la liste 7, société de gestion, assurances, fiscalité et interdiction aux Baléares, selon les règles de 2026.')),
}
GUIDES_NAME = {'es': 'Guías', 'ca': 'Guies', 'en': 'Guides', 'fr': 'Guides'}

def build_guide():
    fn = 'alquilar-mi-barco-charter.html'
    for lang in LANGS:
        d = G[lang]; path = '/guias/' + fn; url = BASE + PRE[lang] + path
        schema = {"@context": "https://schema.org", "@type": "Article", "headline": d['h1'], "author": {"@type": "Person", "name": "Juan Morante"},
                  "publisher": {"@type": "Organization", "name": "Plata Marine"}, "datePublished": TODAY, "dateModified": TODAY, "inLanguage": lang, "mainEntityOfPage": url}
        crumbs = [('Plata Marine', BASE + PRE[lang] + '/'), (GUIDES_NAME[lang], BASE + PRE[lang] + '/guias/'), (d['crumb'], url)]
        H, Fo = shell(lang)
        H = fix_header(H, lang, path, d['wa'])
        ids = ['corta', 'caminos', 'requisitos', 'baleares', 'cataluna', 'fiscal', 'numeros', 'compensa']
        toc = ''.join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in zip(ids, d['toc']))
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
%s
      </div>
      <p style="font-size:13px;opacity:.75;margin-top:22px">%s</p>
    <div class="next-step" data-next="vender" style="%s"><p class="eyebrow" style="margin:0 0 8px">%s</p><p style="margin:0 0 12px">%s</p><a class="next-btn" style="%s" href="%s">%s</a></div>
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
</main>''' % (d['eyebrow'], d['h1'], d['meta'][0], d['meta'][1], d['meta'][2], d['lead'], d['body'], d['fine'], NEXT_STYLE, d['next_eyebrow'], d['next_p'], BTN_STYLE, d['next_href'], d['next_btn'],
              d['aside_eyebrow'], d['aside_h'], d['aside_p'], wa(d['wa']), d['aside_btn'], toc, rel)
        out = head(lang, path, d['title'], d['desc'], schema, crumbs) + H + main + Fo
        dest = os.path.join(ROOT, ('' if lang == 'es' else lang + '/') + 'guias/' + fn)
        open(dest, 'w', encoding='utf-8').write(out)
        print('ok', dest)

if __name__ == '__main__':
    build_astilleros()
    build_guide()
