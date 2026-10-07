# -*- coding: utf-8 -*-
"""SEO de octubre (6 oct 2026), ES/CA/EN/FR. Idempotente.
#1 título/descripcion de /barcos/; landing de Cataluña: FAQ que se habían quedado en el lateral vuelven a su sitio + enlaces por tipo.
#7 /titulaciones/: título y descripción orientados a "titulación náutica / patrón de barco" + 4 preguntas frecuentes (con FAQPage).
Enlaces a las landings nuevas desde /comprar/ y /guias/, y sitemap."""
import re, os, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
LANGS = ['es', 'ca', 'en', 'fr']
PRE = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
def path(l, p): return os.path.join(ROOT, (l + '/' if l != 'es' else '') + p)
def rd(f): return open(f, encoding='utf-8').read()
def wr(f, s): open(f, 'w', encoding='utf-8').write(s)
def set_meta(s, title, desc):
    s = re.sub(r'<title>.*?</title>', lambda m: '<title>%s</title>' % title, s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc.replace('"', '&quot;'), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title.replace('"', '&quot;'), s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + desc.replace('"', '&quot;'), s, count=1)
    return s

BARCOS = {
 'es': ('Barcos de segunda mano en venta · Plata Marine', 'Barcos a motor y veleros de segunda mano en venta. Consulta precios, fotos y fichas en Cataluña, Baleares y otras zonas. Habla con Juan Morante.'),
 'ca': ('Vaixells de segona mà en venda · Plata Marine', 'Vaixells a motor i velers de segona mà en venda. Consulta preus, fotos i fitxes a Catalunya, les Balears i altres zones. Parla amb Juan Morante.'),
 'en': ('Used boats for sale in Spain · Plata Marine', 'Browse used motorboats and sailboats for sale in Catalonia, the Balearics and beyond. Prices, photos and full boat details. Contact Juan Morante.'),
 'fr': ('Bateaux d’occasion à vendre en Espagne · Plata Marine', 'Bateaux à moteur et voiliers d’occasion en Catalogne, aux Baléares et ailleurs en Espagne. Prix, photos et fiches détaillées. Contactez Juan Morante.'),
}
TIT = {
 'es': ('Titulación náutica: qué título necesitas para llevar un barco', 'Qué titulación necesitas para llevar un barco según su eslora: Licencia de Navegación, PNB, PER (patrón de barco) y Patrón de Yate. Atribuciones, exámenes en Cataluña y precio.', 'Preguntas frecuentes', [
   ('¿Qué titulación necesito para llevar un barco?', 'Depende de la eslora que figura en los papeles y de lo lejos que quieras ir: hasta 6 metros, la Licencia de Navegación; hasta 8 metros, el PNB; hasta 15 metros (24 con las prácticas de ampliación), el PER; y para alejarte más, Patrón y Capitán de Yate. Para veleros, además, las prácticas de vela.'),
   ('¿Qué es el título de patrón de barco?', 'En la calle se llama así al PER, Patrón de Embarcaciones de Recreo: es el título más habitual para barcos de 8 a 15 metros. En Cataluña el mismo título se llama PEE (Patró d\'Embarcacions d\'Esbarjo).'),
   ('¿Puedo llevar un barco de 6 metros con la Licencia de Navegación?', 'Sí, si la eslora de los papeles no pasa de 6 metros y el motor es el adecuado según el fabricante, de día y sin alejarte más de 2 millas de un puerto o abrigo. Muchos barcos que se anuncian de 6 metros miden algo más en los papeles: compruébalo antes de comprar.'),
   ('¿Qué título necesito para un barco de 8 metros?', 'Con 8 metros o menos en los papeles, el PNB. Si mide más de 8 metros, el PER.'),
 ]),
 'ca': ('Titulació nàutica: quin títol necessites per portar un vaixell', 'Quina titulació necessites per portar un vaixell segons l\'eslora: Llicència de Navegació, PNB, PER o PEE (patró) i Patró de Iot. Atribucions, exàmens a Catalunya i preu.', 'Preguntes freqüents', [
   ('Quina titulació necessito per portar un vaixell?', 'Depèn de l\'eslora que consta als papers i de com de lluny vulguis anar: fins a 6 metres, la Llicència de Navegació; fins a 8 metres, el PNB; fins a 15 metres (24 amb les pràctiques d\'ampliació), el PER; i per allunyar-te més, Patró i Capità de Iot. Per a velers, a més, les pràctiques de vela.'),
   ('Què és el PEE i què el diferencia del PER?', 'Són el mateix títol. A Catalunya, el Patró d\'Embarcacions d\'Esbarjo (PEE) és el nom que rep el PER (Patrón de Embarcaciones de Recreo), i té les mateixes atribucions.'),
   ('Puc portar un vaixell de 6 metres amb la Llicència de Navegació?', 'Sí, si l\'eslora dels papers no passa de 6 metres i el motor és l\'adequat segons el fabricant, de dia i sense allunyar-te més de 2 milles d\'un port o abric. Molts vaixells que s\'anuncien de 6 metres fan una mica més als papers: comprova-ho abans de comprar.'),
   ('Quin títol necessito per a un vaixell de 8 metres?', 'Amb 8 metres o menys als papers, el PNB. Si fa més de 8 metres, el PER (PEE).'),
 ]),
 'en': ('Spanish boating licences: which licence you need to skipper a boat', 'Which Spanish boating licence you need by boat length: Licencia de Navegación, PNB, PER and Yacht Skipper. What each allows, exams in Catalonia and cost. Boat licence Spain, explained.', 'Frequently asked questions', [
   ('Which licence do I need to skipper a boat in Spain?', 'It depends on the length on the boat\'s papers and how far you want to go: up to 6 metres, the Licencia de Navegación; up to 8 metres, the PNB; up to 15 metres (24 with the extension), the PER; and further offshore, Yacht Skipper and Yacht Master. For sailboats you also need the sailing practicals.'),
   ('What is the PER?', 'The Patrón de Embarcaciones de Recreo is the most common licence for boats from 8 to 15 metres. In Catalonia the same licence is called PEE (Patró d\'Embarcacions d\'Esbarjo).'),
   ('Can I skipper a 6-metre boat with the Licencia de Navegación?', 'Yes, if the length on the papers is no more than 6 metres and the engine is suitable according to the builder, in daylight and within 2 miles of a port or shelter. Many boats advertised as 6 metres are slightly longer on paper: check before buying.'),
   ('Which licence do I need for an 8-metre boat?', 'With 8 metres or less on the papers, the PNB. Over 8 metres, the PER.'),
 ]),
 'fr': ('Permis bateau en Espagne : quel permis pour piloter un bateau', 'Quel permis bateau espagnol selon la longueur : Licencia de Navegación, PNB, PER et Patrón de Yate. Ce que chacun permet, examens en Catalogne et coût.', 'Questions fréquentes', [
   ('Quel permis faut-il pour piloter un bateau en Espagne ?', 'Cela dépend de la longueur inscrite sur les papiers et de la distance : jusqu’à 6 mètres, la Licencia de Navegación ; jusqu’à 8 mètres, le PNB ; jusqu’à 15 mètres (24 avec l’extension), le PER ; et au-delà, Patrón et Capitán de Yate. Pour les voiliers, il faut aussi les pratiques de voile.'),
   ('Qu’est-ce que le PER ?', 'Le Patrón de Embarcaciones de Recreo est le permis le plus courant pour les bateaux de 8 à 15 mètres. En Catalogne, le même permis s’appelle PEE (Patró d’Embarcacions d’Esbarjo).'),
   ('Peut-on piloter un bateau de 6 mètres avec la Licencia de Navegación ?', 'Oui, si la longueur inscrite sur les papiers ne dépasse pas 6 mètres et que le moteur est adapté selon le constructeur, de jour et à 2 milles maximum d’un port ou d’un abri. Beaucoup de bateaux annoncés à 6 mètres mesurent un peu plus sur les papiers : vérifiez avant d’acheter.'),
   ('Quel permis pour un bateau de 8 mètres ?', 'Avec 8 mètres ou moins sur les papiers, le PNB. Au-delà de 8 mètres, le PER.'),
 ]),
}
NEWLINKS = {  # /comprar/ índice
 'es': [('Tipo', 'semirrigidas-neumaticas-segunda-mano', 'Semirrígidas y neumáticas'), ('Tipo', 'barcos-6-metros-con-camarote-segunda-mano', 'Barcos de 6 metros con camarote'), ('Tipo', 'llauts-segunda-mano', 'Llaüts de segunda mano'), ('Precio', 'cuanto-cuesta-un-barco', '¿Cuánto cuesta un barco?')],
 'ca': [('Tipus', 'semirrigidas-neumaticas-segunda-mano', 'Semirígides i neumàtiques'), ('Tipus', 'barcos-6-metros-con-camarote-segunda-mano', 'Vaixells de 6 metres amb cabina'), ('Tipus', 'llauts-segunda-mano', 'Llaüts de segona mà'), ('Preu', 'cuanto-cuesta-un-barco', 'Quant costa un vaixell?')],
 'en': [('Type', 'semirrigidas-neumaticas-segunda-mano', 'RIBs and inflatables'), ('Type', 'barcos-6-metros-con-camarote-segunda-mano', '6-metre boats with a cabin'), ('Type', 'llauts-segunda-mano', 'Used llaüts'), ('Price', 'cuanto-cuesta-un-barco', 'How much does a boat cost?')],
 'fr': [('Type', 'semirrigidas-neumaticas-segunda-mano', 'Semi-rigides et pneumatiques'), ('Type', 'barcos-6-metros-con-camarote-segunda-mano', 'Bateaux de 6 mètres avec cabine'), ('Type', 'llauts-segunda-mano', 'Llaüts d’occasion'), ('Prix', 'cuanto-cuesta-un-barco', 'Combien coûte un bateau ?')],
}
CATTYPE = {
 'es': 'Por tipo: <a href="/comprar/lanchas-motor-segunda-mano.html">lanchas</a> · <a href="/comprar/veleros-segunda-mano.html">veleros</a> · <a href="/comprar/semirrigidas-neumaticas-segunda-mano.html">semirrígidas</a> · <a href="/comprar/barcos-6-metros-con-camarote-segunda-mano.html">barcos de 6 metros con camarote</a> · <a href="/comprar/llauts-segunda-mano.html">llaüts</a>.',
 'ca': 'Per tipus: <a href="/ca/comprar/lanchas-motor-segunda-mano.html">llanxes</a> · <a href="/ca/comprar/veleros-segunda-mano.html">velers</a> · <a href="/ca/comprar/semirrigidas-neumaticas-segunda-mano.html">semirígides</a> · <a href="/ca/comprar/barcos-6-metros-con-camarote-segunda-mano.html">vaixells de 6 metres amb cabina</a> · <a href="/ca/comprar/llauts-segunda-mano.html">llaüts</a>.',
 'en': 'By type: <a href="/en/comprar/lanchas-motor-segunda-mano.html">motorboats</a> · <a href="/en/comprar/veleros-segunda-mano.html">sailboats</a> · <a href="/en/comprar/semirrigidas-neumaticas-segunda-mano.html">RIBs</a> · <a href="/en/comprar/barcos-6-metros-con-camarote-segunda-mano.html">6-metre boats with a cabin</a> · <a href="/en/comprar/llauts-segunda-mano.html">llaüts</a>.',
 'fr': 'Par type : <a href="/fr/comprar/lanchas-motor-segunda-mano.html">bateaux à moteur</a> · <a href="/fr/comprar/veleros-segunda-mano.html">voiliers</a> · <a href="/fr/comprar/semirrigidas-neumaticas-segunda-mano.html">semi-rigides</a> · <a href="/fr/comprar/barcos-6-metros-con-camarote-segunda-mano.html">bateaux de 6 mètres avec cabine</a> · <a href="/fr/comprar/llauts-segunda-mano.html">llaüts</a>.',
}

def barcos(l):
    f = path(l, 'barcos/index.html'); s = rd(f); t, d = BARCOS[l]; wr(f, set_meta(s, t, d))

def titulaciones(l):
    f = path(l, 'titulaciones/index.html'); s = rd(f)
    t, d, fh, faq = TIT[l]
    s = set_meta(s, t, d)
    if 'id="faq-tit"' not in s:
        block = '<h2 id="faq-tit">%s</h2>\n        %s\n        ' % (fh, ''.join('<h3>%s</h3><p>%s</p>' % qa for qa in faq))
        s = s.replace('<h2 id="test">', block + '<h2 id="test">', 1)
        ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
        s = s.replace('</head>', '<script type="application/ld+json">%s</script>\n</head>' % json.dumps(ld, ensure_ascii=False), 1)
    wr(f, s)

def cataluna(l):
    f = path(l, 'comprar/barcos-segunda-mano-cataluna.html'); s = rd(f)
    # FAQ que estaban dentro de la tarjeta lateral -> al final de la sección de preguntas
    m = re.search(r'(<aside class="aside">\s*<div class="card">.*?<p>[^<]*</p>)((?:<h3>.*?</h3><p>.*?</p>)+)', s, flags=re.S)
    if m:
        moved = m.group(2)
        s = s[:m.start(2)] + s[m.end(2):]
        i = s.index('<h2 id="faq">'); j = s.index('</div>', i)
        s = s[:j] + moved + '\n      ' + s[j:]
    if 'semirrigidas-neumaticas-segunda-mano.html' not in s:
        s = re.sub(r'(<p class="note"[^>]*>.*?)(</p>)', lambda m: m.group(1) + ' ' + CATTYPE[l] + m.group(2), s, count=1, flags=re.S)
    wr(f, s)

def comprar_index(l):
    f = path(l, 'comprar/index.html'); s = rd(f)
    if 'llauts-segunda-mano.html' in s: return
    items = ''.join('<li><a href="%s/comprar/%s.html"><span class="g-body"><span class="g-tag">%s</span><strong>%s</strong></span></a></li>' % (PRE[l], sl, tag, name) for tag, sl, name in NEWLINKS[l])
    anchor = '<li><a href="%s/comprar/barcos-licencia-navegacion-pnb.html">' % PRE[l]
    i = s.find(anchor); assert i > 0, f
    j = s.index('</li>', i) + 5
    s = s[:j] + items + s[j:]
    wr(f, s)

def guias_index(l):
    f = path(l, 'guias/index.html'); s = rd(f)
    if 'cuanto-cuesta-un-barco.html' in s: return
    T = {'es': 'También te puede servir: <a href="/comprar/cuanto-cuesta-un-barco.html">¿cuánto cuesta un barco? Precios por tipo y eslora</a>.',
         'ca': 'També et pot servir: <a href="/ca/comprar/cuanto-cuesta-un-barco.html">quant costa un vaixell? Preus per tipus i eslora</a>.',
         'en': 'You may also find useful: <a href="/en/comprar/cuanto-cuesta-un-barco.html">how much does a boat cost? Prices by type and length</a>.',
         'fr': 'Peut aussi vous servir : <a href="/fr/comprar/cuanto-cuesta-un-barco.html">combien coûte un bateau ? Prix par type et longueur</a>.'}[l]
    i = s.find('</ul>', s.find('precio-barco-ocasion.html'))
    assert i > 0, f
    s = s[:i + 5] + '\n<p style="margin-top:14px">%s</p>' % T + s[i + 5:]
    wr(f, s)

def sitemap():
    f = os.path.join(ROOT, 'sitemap.xml'); s = rd(f)
    add = ''
    for sl in ['barcos-6-metros-con-camarote-segunda-mano', 'semirrigidas-neumaticas-segunda-mano', 'llauts-segunda-mano', 'cuanto-cuesta-un-barco']:
        for l in LANGS:
            u = 'https://www.platamarine.com%s/comprar/%s.html' % (PRE[l], sl)
            if u not in s:
                add += '    <url><loc>%s</loc><lastmod>2026-10-07</lastmod><priority>0.8</priority></url>\n' % u
    for p in ['barcos/', 'titulaciones/', 'comprar/', 'comprar/barcos-segunda-mano-cataluna.html', '', 'vender-barco/']:
        for l in LANGS:
            u = 'https://www.platamarine.com%s/%s' % (PRE[l], p)
            s = re.sub(r'(<loc>%s</loc><lastmod>)[^<]*' % re.escape(u), r'\g<1>2026-10-07', s)
    s = s.replace('</urlset>', add + '</urlset>')
    wr(f, s)

if __name__ == '__main__':
    for l in LANGS:
        barcos(l); titulaciones(l); cataluna(l); comprar_index(l); guias_index(l)
    sitemap()
    print('ok')
