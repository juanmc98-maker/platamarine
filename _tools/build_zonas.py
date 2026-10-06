# -*- coding: utf-8 -*-
"""Landings de vendedor por zona (Costa Brava, Tarragona, Baleares) en ES/CA/EN/FR, a partir de la página
de Barcelona-Maresme de cada idioma (cabecera, menú y pie). Añade enlaces entre zonas, bloque en /vender-barco/
y sitemap. Uso: python3 build_zonas.py <raiz_repo>"""
import sys, re, json, html, urllib.parse as up, importlib.util, os
ROOT = sys.argv[1]
spec = importlib.util.spec_from_file_location('zd', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zonas_data.py'))
zd = importlib.util.module_from_spec(spec); spec.loader.exec_module(zd)
UI, ZONES, ORDER = zd.UI, zd.ZONES, zd.ORDER
PRE = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
DOM = 'https://www.platamarine.com'
BCN = 'vender/broker-nautico-barcelona-maresme.html'
e = lambda s: html.escape(s, quote=False)
ea = lambda s: html.escape(s, quote=True)

def url(lang, slug): return f"{DOM}{PRE[lang]}/vender/{slug}"

def zone_links(lang, current):
    out = []
    for k in ORDER:
        if k == current: continue
        z = ZONES[k]; out.append(f'<a href="{PRE[lang]}/vender/{z["slug"]}">{e(z["T"][lang]["name"])}</a>')
    return out

def build(zkey, lang):
    z = ZONES[zkey]; d = z['T'][lang]; u = UI[lang]; slug = z['slug']
    src = os.path.join(ROOT, (lang + '/' if lang != 'es' else '') + BCN)
    t = open(src, encoding='utf-8').read()
    me = url(lang, slug)
    # cabecera
    t = re.sub(r'<title>.*?</title>', f'<title>{e(d["title"])}</title>', t, 1, re.S)
    t = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{ea(d["desc"])}">', t, 1)
    t = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{ea(d["title"])}">', t, 1)
    t = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{ea(d["desc"])}">', t, 1)
    t = t.replace('broker-nautico-barcelona-maresme.html', slug)   # canonical, hreflang, og:url, breadcrumb, menú (aria-current)
    # el menú debe seguir apuntando a la página de Barcelona: lo restauramos dentro de <nav>
    def fixnav(m): return m.group(0).replace('/vender/' + slug, '/vender/broker-nautico-barcelona-maresme.html').replace(' aria-current="page"', '')
    t = re.sub(r'<nav class="(?:nav pmx-nav|pmx-panel)".*?</nav>', fixnav, t, flags=re.S)
    # JSON-LD principal
    faq = list(d['faq']) + [u['faq_fee'], u['faq_exc']]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": d['title'], "inLanguage": lang, "url": me, "description": d['desc'], "publisher": {"@type": "Organization", "name": "Plata Marine"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    t = re.sub(r'<script type="application/ld\+json">\s*\{"@context": "https://schema.org", "@graph".*?</script>',
               '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False) + '\n</script>', t, 1, re.S)
    t = re.sub(r'("position": 3, "name": ")[^"]*(")', lambda m: m.group(1) + d['title'].replace('"', '\\"') + m.group(2), t, 1)
    # cuerpo
    wa = 'https://wa.me/34633742973?text=' + up.quote(d['wa'], safe='')
    zl = ' · '.join(zone_links(lang, zkey))
    main = f'''<main class="art">
  <div class="wrap">
    <article>
      <header>
        <p class="eyebrow">{e(u["eye"])} · {e(d["name"])}</p>
        <h1>{e(d["title"])}</h1>
        <div class="meta"><span>{e(u["by"])}</span><span>{e(u["upd"])}</span></div>
        <p class="lead">{e(d["lead"])}</p>
      </header>
      <div class="prose">
        <h2 id="s0">{e(d["h2"])}</h2>{''.join('<p>' + e(p) + '</p>' for p in d["p"])}
        <h2 id="s1">{e(u["how"])}</h2><ul>{''.join('<li>' + li + '</li>' for li in u["how_list"])}</ul>
        <h2 id="s2">{e(u["need"])}</h2><p>{e(u["need_p"])}</p><p>{u["need_p2"]}</p>
        <div class="cta2"><h3>{e(u["cta_h"])}</h3><p>{e(u["cta_p"])}</p><a class="btn btn-wa" href="{PRE[lang]}/vender-barco/">{e(u["cta_b1"])}</a><a class="btn btn-ghost" href="{PRE[lang]}/herramientas/valora-tu-barco.html">{e(u["cta_b2"])}</a></div>
        <h2 id="faq">{e(u["faqh"])}</h2>
        {''.join('<h3>' + e(q) + '</h3><p>' + e(a) + '</p>' for q, a in faq)}
        <p class="zonas"><strong>{e(u["zones"])}:</strong> {zl}</p>
      </div>
    <p class="aviso aviso-fiscal" style="font-size:.82em;opacity:.85">{e(u["aviso"])}</p>
    </article>
    <aside class="aside">
      <div class="card">
        <p class="eyebrow">{e(u["a_eye"])}</p>
        <h3>{e(u["a_h"])}</h3>
        <p>{e(u["a_p"])}</p>
        <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{e(u["a_b"])}</a>
      </div>
      <div class="rel"><p class="eyebrow">{e(u["rel"])}</p>{''.join(f'<a href="{h}">{e(x)}</a>' for h, x in u["rel_links"])}</div>
    </aside>
  </div>
</main>'''
    t = t[:t.find('<main')] + main + t[t.find('</main>') + 7:]
    out = os.path.join(ROOT, (lang + '/' if lang != 'es' else '') + 'vender/' + slug)
    open(out, 'w', encoding='utf-8').write(t)
    return out

made = []
for z in ['costa-brava', 'tarragona', 'baleares']:
    for l in ['es', 'ca', 'en', 'fr']: made.append(build(z, l))

# Barcelona-Maresme: añadir la línea de otras zonas al final de la prosa (idempotente)
for l in ['es', 'ca', 'en', 'fr']:
    p = os.path.join(ROOT, (l + '/' if l != 'es' else '') + BCN); t = open(p, encoding='utf-8').read()
    if 'class="zonas"' not in t:
        zl = ' · '.join(zone_links(l, 'barcelona'))
        t = t.replace('\n      </div>\n    <p class="aviso aviso-fiscal"', f'\n        <p class="zonas"><strong>{e(UI[l]["zones"])}:</strong> {zl}</p>\n      </div>\n    <p class="aviso aviso-fiscal"', 1)
        open(p, 'w', encoding='utf-8').write(t); made.append(p)

# /vender-barco/: bloque "Dónde trabajo" antes de las preguntas frecuentes (idempotente)
VB = {'es': ('Dónde trabajo', 'Tengo la base en Cataluña y trabajo barcos en toda la costa catalana y, cuando el barco lo justifica, en Baleares:', 'Preguntas frecuentes'),
      'ca': ('On treballo', 'Tinc la base a Catalunya i treballo vaixells a tota la costa catalana i, quan el vaixell ho justifica, a les Balears:', 'Preguntes freqüents'),
      'en': ('Where I work', 'I am based in Catalonia and work with boats all along the Catalan coast and, when the boat justifies it, in the Balearic Islands:', 'Frequently asked questions'),
      'fr': ('Où je travaille', 'Je suis basé en Catalogne et je travaille sur toute la côte catalane et, quand le bateau le justifie, aux Baléares :', 'Questions fréquentes')}
for l, (h, txt, faqh) in VB.items():
    p = os.path.join(ROOT, (l + '/' if l != 'es' else '') + 'vender-barco/index.html'); t = open(p, encoding='utf-8').read()
    if 'id="zonas"' in t: continue
    links = ' · '.join(f'<a href="{PRE[l]}/vender/{ZONES[k]["slug"]}">{e(ZONES[k]["T"][l]["name"])}</a>' for k in ORDER)
    m = re.search(r'<h2[^>]*>\s*' + re.escape(faqh), t)
    if not m: print('SIN FAQ en', p); continue
    block = f'<h2 id="zonas">{e(h)}</h2>\n<p>{e(txt)} {links}.</p>\n'
    t = t[:m.start()] + block + t[m.start():]
    open(p, 'w', encoding='utf-8').write(t); made.append(p)

# sitemap
sp = os.path.join(ROOT, 'sitemap.xml'); s = open(sp, encoding='utf-8').read()
add = ''
for z in ['costa-brava', 'tarragona', 'baleares']:
    for l in ['es', 'ca', 'en', 'fr']:
        u_ = url(l, ZONES[z]['slug'])
        if u_ not in s: add += f'    <url><loc>{u_}</loc><lastmod>2026-10-07</lastmod><priority>0.8</priority></url>\n'
if add:
    s = s.replace('</urlset>', add + '</urlset>'); open(sp, 'w', encoding='utf-8').write(s); made.append(sp)
print('\n'.join(sorted(set(made))))
