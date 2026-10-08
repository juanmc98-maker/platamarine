# -*- coding: utf-8 -*-
"""Generador genérico de páginas de contenido (4 idiomas) a partir de la guía de arras como plantilla.
Usado por build_valor.py. Idempotente."""
import os, re, json, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BASE = 'https://www.platamarine.com'
LANGS = ['es', 'ca', 'en', 'fr']
TPL = 'guias/arras-compraventa-barco.html'
HOME = {'es': 'Plata Marine', 'ca': 'Plata Marine', 'en': 'Plata Marine', 'fr': 'Plata Marine'}

def pre(l):
    return '' if l == 'es' else '/' + l

def url(l, rel):
    return BASE + pre(l) + '/' + rel

def build(rel, pages, crumbs, ld_type='Article', extra_head='', extra_foot=''):
    """rel: ruta relativa sin idioma (p. ej. 'guias/x.html' o 'cuanto-vale-mi-barco/').
    pages[l] = dict(title, h1, desc, eyebrow, meta, lead, body, aside, aviso)
    crumbs[l] = [(nombre, rel)] niveles intermedios entre inicio y la página."""
    for l in LANGS:
        p = pages[l]
        P = pre(l)
        tpath = os.path.join(ROOT, (l + '/' if l != 'es' else '') + TPL)
        s = open(tpath, encoding='utf-8').read()
        # rutas del idioma: sustituir la URL de la plantilla por la nueva
        s = s.replace(TPL, rel)
        s = re.sub(r'<title>.*?</title>', '<title>%s · Plata Marine</title>' % html.escape(p['title'], quote=False), s, 1, re.S)
        s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % html.escape(p['desc']), s, 1)
        s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % html.escape(p['title']), s, 1)
        s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % html.escape(p['desc']), s, 1)
        s = s.replace('href="guias.css"', 'href="/guias/guias.css"').replace('href="../guias/guias.css"', 'href="/guias/guias.css"')
        s = s.replace('href="../logo-plata-marine.png"', 'href="/logo-plata-marine.png"')
        u = url(l, rel)
        if ld_type == 'Article':
            ld = {"@context": "https://schema.org", "@graph": [{"@type": "Article", "headline": p['h1'], "inLanguage": l, "url": u,
                  "description": p['desc'], "dateModified": "2026-10-07", "datePublished": "2026-10-07",
                  "author": {"@type": "Person", "name": "Juan Morante"}, "publisher": {"@type": "Organization", "name": "Plata Marine", "url": BASE + "/"}}]}
        else:
            ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": p['h1'], "applicationCategory": "UtilityApplication",
                  "operatingSystem": "Web", "inLanguage": l, "url": u, "description": p['desc'], "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
                  "provider": {"@type": "Organization", "name": "Plata Marine", "url": BASE + "/"}}
        if p.get('faq'):
            fq = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in p['faq']]}
            if '@graph' in ld: ld['@graph'].append(fq)
            else: ld = {"@context": "https://schema.org", "@graph": [dict({k: v for k, v in ld.items() if k != '@context'}), fq]}
        s = re.sub(r'<script type="application/ld\+json">\s*\{"@context": "https://schema.org", "@graph".*?</script>',
                   lambda m: '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False) + '\n</script>', s, 1, re.S)
        items = [{"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": BASE + P + "/"}]
        for i, (n, r) in enumerate(crumbs[l]):
            items.append({"@type": "ListItem", "position": i + 2, "name": n, "item": url(l, r)})
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": p['h1'], "item": u})
        s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>',
                   lambda m: '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}, ensure_ascii=False) + '</script>', s, 1, re.S)
        if extra_head:
            s = s.replace('</head>', extra_head + '\n</head>', 1)
        # migas visibles: quitar las de la plantilla si las hay (se generan dentro del header del artículo)
        crumbs_html = '<nav class="crumbs" aria-label="Migas"><a href="%s/">Plata Marine</a>' % P + ''.join(
            ' › <a href="%s/%s">%s</a>' % (P, r, html.escape(n)) for n, r in crumbs[l]) + '</nav>'
        main = ('<main class="art">\n  <div class="wrap">\n    <article>\n      <header>\n        <p class="eyebrow">%s</p>\n        <h1>%s</h1>\n'
                '        <div class="meta">%s</div>\n        <p class="lead">%s</p>\n      </header>\n\n      <div class="prose">\n%s\n      </div>\n'
                '    <p class="aviso aviso-fiscal" style="font-size:.82em;opacity:.85">%s</p>\n    </article>\n\n%s\n  </div>\n</main>') % (
            p['eyebrow'], p['h1'], p['meta'], p['lead'], p['body'].replace('{P}', P), p['aviso'].replace('{P}', P), p['aside'].replace('{P}', P))
        s = re.sub(r'<main class="art">.*?</main>', lambda m: main, s, 1, re.S)
        s = re.sub(r'<nav class="crumbs".*?</nav>\s*', '', s, flags=re.S)
        if extra_foot:
            s = s.replace('</body>', extra_foot + '\n</body>', 1)
        out = os.path.join(ROOT, (l + '/' if l != 'es' else '') + (rel + 'index.html' if rel.endswith('/') else rel))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'w', encoding='utf-8').write(s)
        print('ok', os.path.relpath(out, ROOT))

def sitemap(rels):
    sm = os.path.join(ROOT, 'sitemap.xml')
    s = open(sm, encoding='utf-8').read()
    add = ''
    for rel in rels:
        for l in LANGS:
            u = url(l, rel)
            if '<loc>%s</loc>' % u in s: continue
            add += '    <url><loc>%s</loc><lastmod>2026-10-07</lastmod><priority>0.8</priority></url>\n' % u
    if add:
        s = s.replace('</urlset>', add + '</urlset>')
        open(sm, 'w', encoding='utf-8').write(s)
    print('sitemap', s.count('<url>'))
