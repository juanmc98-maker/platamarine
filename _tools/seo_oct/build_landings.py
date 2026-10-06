# -*- coding: utf-8 -*-
"""Genera las landings SEO de octubre de 2026 en ES/CA/EN/FR a partir de la plantilla
/comprar/veleros-segunda-mano.html de cada idioma (cabecera, menú, pie y scripts se heredan).
Uso: python3 _tools/seo_oct/build_landings.py   (desde la raíz del repo)"""
import json, re, os, subprocess, sys, html
sys.path.insert(0, os.path.dirname(__file__))
from pages_content import PAGES as P1
from pages_content2 import PAGES as P2
PAGES = dict(P1); PAGES.update(P2)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
LANGS = ['es', 'ca', 'en', 'fr']
PRE = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
UPD = {'es': 'Actualizado en octubre de 2026', 'ca': "Actualitzat l'octubre de 2026", 'en': 'Updated October 2026', 'fr': 'Mis à jour en octobre 2026'}
FAQH = {'es': 'Preguntas frecuentes', 'ca': 'Preguntes freqüents', 'en': 'Frequently asked questions', 'fr': 'Questions fréquentes'}
SEE = {'es': 'Ver ficha', 'ca': 'Veure fitxa', 'en': 'See details', 'fr': 'Voir la fiche'}
VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': '+TVA'}
FISCAL = {
 'es': 'Información fiscal orientativa, revisada en octubre de 2026 según la Ley 38/1992 y la normativa autonómica vigente. No es asesoramiento fiscal. El importe final depende del valor que fije Hacienda, de la situación del barco y de posibles exenciones, y la normativa puede cambiar. Confírmalo con tu gestoría o con la Administración antes de comprar.',
 'ca': "Informació fiscal orientativa, revisada l'octubre de 2026 segons la Llei 38/1992 i la normativa autonòmica vigent. No és assessorament fiscal. L'import final depèn del valor que fixi Hisenda, de la situació del vaixell i de possibles exempcions, i la normativa pot canviar. Confirma-ho amb la teva gestoria o amb l'Administració abans de comprar.",
 'en': 'Guide tax information, reviewed in October 2026 under Law 38/1992 and current regional rules. It is not tax advice. The final amount depends on the value set by the tax authority, the boat\'s situation and possible exemptions, and the rules may change. Check with your agency or the authorities before buying.',
 'fr': 'Information fiscale indicative, revue en octobre 2026 selon la loi espagnole 38/1992 et la réglementation régionale en vigueur. Ce n’est pas un conseil fiscal. Le montant final dépend de la valeur fixée par l’administration, de la situation du bateau et d’éventuelles exonérations, et les règles peuvent changer. Vérifiez auprès d’un gestionnaire ou de l’administration avant d’acheter.',
}
CRUMB2 = {'es': 'Comprar', 'ca': 'Comprar', 'en': 'Buy', 'fr': 'Acheter'}

INV = json.loads(subprocess.check_output(['node', os.path.join(ROOT, '_tools/seo_oct/inv_dump.js')], cwd=ROOT))

def price(n, l):
    s = '{:,}'.format(n)
    if l == 'en': return '€' + s
    return s.replace(',', ' ' if l == 'fr' else '.') + ' €'

def match(b, f):
    if b['status'] != 'available': return False
    if f.get('zone') and b.get('zone') != f['zone']: return False
    if f.get('kind') and b['kind'] != f['kind']: return False
    if f.get('types') and not any(t in b.get('types', []) for t in f['types']): return False
    if f.get('minLen') and not b['length'] >= f['minLen']: return False
    if f.get('maxLen') and not b['length'] <= f['maxLen']: return False
    return True

def cards(f, l):
    out = []
    for b in sorted([b for b in INV if match(b, f)], key=lambda b: -(b.get('price') or 0)):
        u = PRE[l] + '/barcos/' + b['slug'] + '.html'
        img = '/' + b['slug'] + '-1'
        e = html.escape
        out.append('<a class="pcard" href="%s"><img src="%s-m.jpg" srcset="%s-m.jpg 1000w, %s.jpg 1600w" sizes="(max-width: 640px) 100vw, 360px" alt="%s" loading="lazy" width="1600" height="900"><span class="pc-b"><strong>%s</strong><span class="pc-p">%s%s</span><span class="pc-d">%s · %s</span><span class="pc-t">%s</span><span class="pc-l">%s →</span></span></a>' % (
            u, img, img, img, e(b['name']), e(b['name']), price(b['price'], l), (' <span class="vat">' + VAT[l] + '</span>') if b.get('vat') else '', b['year'], e(b['d'][l]), e(b['tl'][l]), SEE[l]))
    return ''.join(out)

def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()

def build(slug, spec, l):
    c = spec[l]
    p = PRE[l]
    shell = open(os.path.join(ROOT, (l + '/' if l != 'es' else '') + 'comprar/veleros-segunda-mano.html'), encoding='utf-8').read()
    s = shell.replace('comprar/veleros-segunda-mano.html', 'comprar/%s.html' % slug)
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % html.escape(c['title'], quote=False), s, 1)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(c['desc']), s, 1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(c['title']), s, 1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(c['desc']), s, 1)
    url = 'https://www.platamarine.com%s/comprar/%s.html' % (p, slug)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": c['h1'], "inLanguage": l, "url": url, "dateModified": "2026-10-06", "publisher": {"@type": "Organization", "name": "Plata Marine"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c['faq']]}]}
    s = re.sub(r'<script type="application/ld\+json">\s*\{"@context": "https://schema.org", "@graph".*?</script>',
               lambda m: '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False) + '\n</script>', s, 1, flags=re.S)
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": "https://www.platamarine.com%s/" % p},
        {"@type": "ListItem", "position": 2, "name": CRUMB2[l], "item": "https://www.platamarine.com%s/comprar/" % p},
        {"@type": "ListItem", "position": 3, "name": c['h1'], "item": url}]}
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>',
               lambda m: '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + '</script>', s, 1, flags=re.S)
    # WhatsApp del encabezado y del lateral
    from urllib.parse import quote
    s = re.sub(r'(https://wa\.me/34633742973\?text=)[^"]*(" target="_blank" rel="noopener">(?:Hablar|Parlar|Talk|Parler))',
               lambda m: m.group(1) + quote(c['wa'], safe='') + m.group(2), s)
    # Cuerpo del artículo
    a0 = s.index('<p class="eyebrow">', s.index('<article>'))
    a1 = s.index('<h2 id="barcos">')
    head = '<p class="eyebrow">%s</p>\n        <h1>%s</h1>\n        <div class="meta"><span>%s</span><span>%s</span></div>\n        <p class="lead">%s</p>\n      </header>\n      <div class="prose">\n        ' % (
        c['eyebrow'], c['h1'], re.search(r'<div class="meta"><span>(.*?)</span>', s).group(1), UPD[l], c['lead'])
    intro = c.get('intro', '').replace('{P}', p)
    s = s[:a0] + head + intro + s[a1:]
    s = s.replace('<h2 id="barcos">' + re.search(r'<h2 id="barcos">(.*?)</h2>', s).group(1) + '</h2>', '<h2 id="barcos">%s</h2>' % c['h2list'], 1)
    f = spec['filter']
    s = re.sub(r"<div class=\"pm-list\" data-f='[^']*'>.*?</div>", lambda m: "<div class=\"pm-list\" data-f='%s'>%s</div>" % (json.dumps(f, ensure_ascii=False), cards(f, l)), s, 1, flags=re.S)
    if not cards(f, l):
        s = re.sub(r'<p class="pm-empty" hidden>.*?</p>', lambda m: '<p class="pm-empty">%s</p>' % c.get('empty', '').replace('{P}', p), s, 1, flags=re.S)
    n0 = s.index('</p>', s.index('<p class="note"')) + 4
    n1 = s.index('<div class="cta2">')
    body = '\n        ' + c['body'].replace('{P}', p) + '\n        '
    s = s[:n0] + body + s[n1:]
    f0 = s.index('<h2 id="faq">')
    f1 = s.index('</div>', f0)
    faq = '<h2 id="faq">%s</h2>\n        %s\n      ' % (FAQH[l], ''.join('<h3>%s</h3><p>%s</p>' % (q, a) for q, a in c['faq']))
    s = s[:f0] + faq + s[f1:]
    if spec.get('fiscal'):
        s = s.replace('</div>\n    </article>', '</div>\n    <p class="aviso aviso-fiscal" style="font-size:.82em;opacity:.85">%s</p>\n    </article>' % FISCAL[l], 1)
    r0 = s.index('<div class="rel">')
    r1 = s.index('</div>', r0) + 6
    eb = re.search(r'<div class="rel"><p class="eyebrow">(.*?)</p>', s).group(1)
    rel = '<div class="rel"><p class="eyebrow">%s</p>%s</div>' % (eb, ''.join('<a href="%s">%s</a>' % (h.replace('{P}', p), t) for h, t in c['rel']))
    s = s[:r0] + rel + s[r1:]
    s = s.replace('/portal.js?v=20261006', '/portal.js?v=20261007')
    out = os.path.join(ROOT, (l + '/' if l != 'es' else '') + 'comprar/%s.html' % slug)
    open(out, 'w', encoding='utf-8').write(s)
    return out

if __name__ == '__main__':
    for slug, spec in PAGES.items():
        for l in LANGS:
            print(build(slug, spec, l))
