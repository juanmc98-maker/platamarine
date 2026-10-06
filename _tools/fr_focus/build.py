# -*- coding: utf-8 -*-
"""Genera las 3 páginas para compradores franceses (2 guías + 1 landing) en ES/CA/EN/FR
a partir de plantillas existentes. Uso: python3 _tools/fr_focus/build.py (desde la raíz del repo)."""
import re, json, sys, os, html, urllib.parse, importlib
sys.path.insert(0, os.path.dirname(__file__))
B = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': 'ca/', 'en': 'en/', 'fr': 'fr/'}
TPL = {'guia': 'guias/arras-compraventa-barco.html', 'landing': 'comprar/barcos-segunda-mano-costa-brava.html'}
OG = {'es': 'og-image.jpg', 'ca': 'og-image-ca.jpg', 'en': 'og-image-en.jpg', 'fr': 'og-image-fr.jpg'}
SITE = {'es': 'Plata Marine', 'ca': 'Plata Marine', 'en': 'Plata Marine', 'fr': 'Plata Marine'}
TOCL = {'es': 'En esta guía', 'ca': 'En aquesta guia', 'en': 'In this guide', 'fr': 'Dans ce guide'}
RELL = {'es': 'También te puede interesar', 'ca': 'També et pot interessar', 'en': 'You may also like', 'fr': 'À lire aussi'}

def esc(s): return html.escape(s, quote=True)
def wa(t): return 'https://wa.me/34633742973?text=' + urllib.parse.quote(t, safe='')

def build(key, lang, P):
    pre = LANGS[lang]
    tpl_path = pre + TPL[P['kind']]
    s = open(tpl_path, encoding='utf-8').read()
    old = TPL[P['kind']]
    s = s.replace(old, P['slug'])
    url = B + '/' + pre + P['slug']
    s = re.sub(r'<title>.*?</title>', '<title>' + esc(P['title']) + ' · Plata Marine</title>', s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + esc(P['desc']) + '">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="' + esc(P['title']) + '">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="' + esc(P['desc']) + '">', s, count=1)
    s = re.sub(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="' + B + '/' + OG[lang] + '">', s, count=1)
    # JSON-LD: artículo + FAQ y migas
    art = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": P['title'], "inLanguage": lang, "url": url, "description": P['desc'],
         "datePublished": "2026-10-06", "dateModified": "2026-10-06",
         "author": {"@type": "Person", "name": "Juan Morante"}, "publisher": {"@type": "Organization", "name": "Plata Marine"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in P['faq']]}]}
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": B + '/' + pre},
        {"@type": "ListItem", "position": 2, "name": P['crumb'][0], "item": B + P['crumb'][1]},
        {"@type": "ListItem", "position": 3, "name": P['title'], "item": url}]}
    blocks = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, flags=re.S))
    assert len(blocks) >= 2, (tpl_path, len(blocks))
    new_art = '<script type="application/ld+json">\n' + json.dumps(art, ensure_ascii=False) + '\n</script>'
    new_crumb = '<script type="application/ld+json">' + json.dumps(crumb, ensure_ascii=False) + '</script>'
    out = []; last = 0; done_art = False
    for m in blocks:
        out.append(s[last:m.start()])
        txt = m.group(0)
        if 'BreadcrumbList' in txt: out.append(new_crumb)
        elif not done_art: out.append(new_art); done_art = True
        else: out.append('')
        last = m.end()
    out.append(s[last:]); s = ''.join(out)
    # WhatsApp de la cabecera
    s = re.sub(r'(<header class="top">.*?<a class="btn btn-wa" href=")[^"]*(")', lambda m: m.group(1) + esc(wa(P['header_wa'])) + m.group(2), s, count=1, flags=re.S)
    # artículo
    meta = ''.join('<span>' + esc(x) + '</span>' for x in P['meta'])
    article = ('<article>\n      <header>\n        <p class="eyebrow">' + esc(P['eyebrow']) + '</p>\n        <h1>' + esc(P['h1']) +
               '</h1>\n        <div class="meta">' + meta + '</div>\n        <p class="lead">' + esc(P['lead']) +
               '</p>\n      </header>\n\n      <div class="prose">\n' + P['body'].strip() + '\n      </div>\n      <p class="aviso aviso-fiscal" style="font-size:.82em;opacity:.85">' +
               esc(P['note']) + '</p>\n    </article>')
    s = re.sub(r'<article>.*?</article>', lambda m: article, s, count=1, flags=re.S)
    c = P['card']
    toc = ''
    if P['kind'] == 'guia':
        toc = ('\n      <nav class="toc" aria-label="' + TOCL[lang] + '">\n        <p class="eyebrow">' + TOCL[lang] + '</p>\n        <ol>' +
               ''.join('<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in P['toc']) + '</ol>\n      </nav>')
    rel = '<div class="rel"><p class="eyebrow">' + RELL[lang] + '</p>' + ''.join('<a href="%s">%s</a>' % (h, esc(t)) for h, t in P['rel']) + '</div>'
    aside_open = re.search(r'<aside[^>]*>', s).group(0)
    aside = (aside_open + '\n      <div class="card">\n        <p class="eyebrow">' + esc(c['eyebrow']) + '</p>\n        <h3>' + esc(c['h3']) + '</h3>\n        <p>' + esc(c['p']) +
             '</p>\n        <a class="btn btn-wa" href="' + esc(wa(c['wa'])) + '" target="_blank" rel="noopener">' + esc(c['btn']) + '</a>\n      </div>' + toc + '\n      ' + rel + '\n    </aside>')
    s = re.sub(r'<aside[^>]*>.*?</aside>', lambda m: aside, s, count=1, flags=re.S)
    os.makedirs(os.path.dirname(pre + P['slug']) or '.', exist_ok=True)
    open(pre + P['slug'], 'w', encoding='utf-8').write(s)
    return pre + P['slug']

if __name__ == '__main__':
    for lang in LANGS:
        mod = importlib.import_module('content_' + lang)
        for key, P in mod.PAGES.items():
            print(build(key, lang, P))
