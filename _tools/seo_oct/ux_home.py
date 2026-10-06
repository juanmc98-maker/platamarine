# -*- coding: utf-8 -*-
"""Revisión UX de la portada (6 oct 2026), ES/CA/EN/FR. Idempotente: se puede volver a lanzar tras un git pull.
- Hero: solo dos caminos (se quita el enlace a la herramienta de precio, que sigue en el menú y en /vender-barco/).
- Fuera el buscador rápido (inventario pequeño; el catálogo tiene filtros y acepta los mismos parámetros por URL).
- Fuera el bloque doble "vender / comprar" que repetía el hero; sus enlaces por zona pasan al bloque de compradores.
- "¿Para qué un broker?" se integra en el bloque del formulario de vendedor (se conservan las anclas #vender y #condiciones).
- Tarjetas destacadas compactas (sin párrafo ni miniaturas) y guías sin fotos de archivo (mismos enlaces).
- Compradores: un botón principal (WhatsApp) y la alerta como enlace; el test sigue en el menú.
"""
import re, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
P = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
ZONES = {
 'es': 'También por zona: <a href="/comprar/barcos-segunda-mano-cataluna.html">Cataluña</a>, <a href="/comprar/barcos-segunda-mano-costa-brava.html">Costa Brava</a> y <a href="/comprar/barcos-segunda-mano-baleares.html">Baleares</a>.',
 'ca': 'També per zona: <a href="/ca/comprar/barcos-segunda-mano-cataluna.html">Catalunya</a>, <a href="/ca/comprar/barcos-segunda-mano-costa-brava.html">Costa Brava</a> i <a href="/ca/comprar/barcos-segunda-mano-baleares.html">Balears</a>.',
 'en': 'Also by area: <a href="/en/comprar/barcos-segunda-mano-cataluna.html">Catalonia</a>, <a href="/en/comprar/barcos-segunda-mano-costa-brava.html">Costa Brava</a> and <a href="/en/comprar/barcos-segunda-mano-baleares.html">Balearic Islands</a>.',
 'fr': 'Aussi par zone : <a href="/fr/comprar/barcos-segunda-mano-cataluna.html">Catalogne</a>, <a href="/fr/comprar/barcos-segunda-mano-costa-brava.html">Costa Brava</a> et <a href="/fr/comprar/barcos-segunda-mano-baleares.html">Baléares</a>.',
}
SELL = {  # entrada del bloque de vendedor (sustituye al bloque "¿Para qué un broker?")
 'es': ('¿Piensas vender tu barco? Cuéntame cuál es y lo estudiamos.', 'La diferencia de trabajar con un broker está en todo lo que pasa entre publicar el anuncio y cobrar: el precio, la ficha, las consultas, las visitas, la negociación y los papeles. Sin exclusiva, sin adelantos y con las condiciones por escrito antes de empezar. Esta consulta no es un encargo de venta. <a href="/vender-barco/">Cómo trabajo, paso a paso</a>.'),
 'ca': ('Penses vendre el teu vaixell? Explica\'m quin és i l\'estudiem.', 'La diferència de treballar amb un broker és tot el que passa entre publicar l\'anunci i cobrar: el preu, la fitxa, les consultes, les visites, la negociació i els papers. Sense exclusiva, sense avançaments i amb les condicions per escrit abans de començar. Aquesta consulta no és un encàrrec de venda. <a href="/ca/vender-barco/">Com treballo, pas a pas</a>.'),
 'en': ('Thinking of selling your boat? Tell me about it and I will take a look.', 'The difference a broker makes lies in everything that happens between publishing the listing and getting paid: the price, the listing itself, enquiries, viewings, negotiation and paperwork. No exclusivity, no upfront fees and the terms in writing before we start. This enquiry is not a sale mandate. <a href="/en/vender-barco/">How I work, step by step</a>.'),
 'fr': ('Vous pensez vendre votre bateau ? Parlez-m’en et je l’étudie.', 'Passer par un courtier change tout ce qui se passe entre la publication de l’annonce et l’encaissement : le prix, l’annonce elle-même, les demandes, les visites, la négociation et les démarches. Sans exclusivité, sans frais anticipés et avec les conditions par écrit avant de commencer. Cette demande n’est pas un mandat de vente. <a href="/fr/vender-barco/">Ma façon de travailler, étape par étape</a>.'),
}
HELP2 = {
 'es': 'Te confirmo aquí mismo cuando me llegue. Si lo prefieres, escríbeme por WhatsApp o email con los botones de arriba. Los campos con * son obligatorios.',
 'ca': 'Et confirmo aquí mateix quan m\'arribi. Si ho prefereixes, escriu-me per WhatsApp o correu amb els botons de dalt. Els camps amb * són obligatoris.',
 'en': 'I will confirm right here when it reaches me. If you prefer, message me on WhatsApp or by email with the buttons above. Fields marked * are required.',
 'fr': 'Je vous le confirme ici même dès réception. Si vous préférez, écrivez-moi par WhatsApp ou par e-mail avec les boutons ci-dessus. Les champs marqués * sont obligatoires.',
}
CSS = '<style id="ux-oct">/* Revisión UX 6 oct 2026 */#venta .boat .desc,#venta .boat .thumbs{display:none}#guias .guias-cards img{display:none}#guias .guias-cards .gc-body{padding-top:18px}#comprar .buy-alt{margin-top:14px;font-family:var(--display);font-size:15px}#valora .sell-lead{max-width:62ch;color:var(--ink-2);margin-top:12px}@media(min-width:900px){#guias .guias-cards{grid-template-columns:repeat(4,1fr)}}</style>'

def run(l):
    f = os.path.join(ROOT, (l + '/' if l != 'es' else '') + 'index.html')
    s = open(f, encoding='utf-8').read()
    o = s
    # 1. Hero: quitar el enlace a la herramienta de precio
    s = re.sub(r'\s*<p style="margin:14px 0 0"><a class="hero-valora"[^>]*>.*?</a></p>', '', s, count=1, flags=re.S)
    # 2. Buscador rápido
    s = re.sub(r'\s*<section class="qsearch".*?</section>', '', s, count=1, flags=re.S)
    # 3. Bloque doble vender/comprar (el primero; en FR se conserva el bloque para residentes en Francia)
    m = re.search(r'\s*<section class="service-switch" aria-label="(Vender o comprar|Vendre ou acheter|Vendre o comprar|Selling or buying|Sell or buy)[^"]*">.*?</section>', s, flags=re.S)
    if m:
        s = s[:m.start()] + s[m.end():]
    # 4. Bloque "¿Para qué un broker?" -> se integra en #valora
    m = re.search(r'\s*<section class="sec" id="vender">.*?</section>', s, flags=re.S)
    if m:
        s = s[:m.start()] + s[m.end():]
    h2, lead = SELL[l]
    if 'class="sell-lead"' not in s:
        s = re.sub(r'(<section class="sec final" id="valora">\s*)<div class="wrap">\s*<p class="eyebrow">([^<]*)</p>\s*<h2>.*?</h2>\s*<p class="intro">.*?</p>',
                   lambda m: m.group(1).replace('id="valora">', 'id="valora">') + '<span id="vender"></span><span id="condiciones"></span>\n    <div class="wrap">\n      <p class="eyebrow">%s</p>\n      <h2>%s</h2>\n      <p class="intro sell-lead">%s</p>' % (m.group(2), h2, lead),
                   s, count=1, flags=re.S)
    # nota del formulario más corta (se mantiene el texto legal)
    s = re.sub(r'(<p class="form-help">)(Al pulsar «Enviar consulta»|En prémer «Enviar consulta»|Pressing "Send inquiry"|En appuyant sur « Envoyer la demande »)[^<]*(</p>)', lambda m: m.group(1) + HELP2[l] + m.group(3), s, count=1)
    # 5. Compradores: alerta como enlace, test fuera del recorrido principal; enlaces por zona
    m = re.search(r'(<section class="sec" id="comprar">.*?<div class="boat-cta"[^>]*>\s*<a class="btn btn-wa"[^>]*>[^<]*</a>)\s*<a class="btn btn-ghost" href="[^"]*que-barco-necesito\.html">[^<]*</a>\s*<a class="btn btn-ghost" href="([^"]*alertas/)">([^<]*)</a>\s*</div>', s, flags=re.S)
    if m:
        s = s[:m.start()] + m.group(1) + '\n          </div>\n          <p class="buy-alt"><a href="%s">%s</a></p>' % (m.group(2), m.group(3)) + s[m.end():]
    if 'barcos-segunda-mano-costa-brava.html">Costa Brava</a>' not in s[s.find('id="comprar"'):s.find('id="guias"')]:
        s = re.sub(r'(<section class="sec" id="comprar">.*?<p class="intro">.*?)(</p>)', lambda m: m.group(1) + ' ' + ZONES[l] + m.group(2), s, count=1, flags=re.S)
    # 6. CSS
    if 'id="ux-oct"' not in s:
        s = s.replace('</head>', CSS + '\n</head>', 1)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s)
    return f, len(o), len(s)

if __name__ == '__main__':
    for l in ['es', 'ca', 'en', 'fr']:
        print(run(l))
