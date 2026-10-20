"""Genera el "Informe de precios de barcos de ocasión" en PDF (ES/CA/EN/FR) a partir de lo ya publicado:
- /precios/ de cada idioma: tabla por modelo, tabla por tipo, notas, factores, método y aviso (textos tal cual).
- /cuanto-vale-mi-barco/calc.js: horquillas por modelo y tramo de años (array M).
No añade cifras propias: si cambian /precios/ o calc.js (revisión mensual), relanzar y cambiar MES abajo.
Uso: PM_ROOT=<repo> python3 _tools/build_informe_precios.py
Salida: precios/informe-precios-barcos-ocasion.pdf (ES) y -ca/-en/-fr.pdf (mismo nombre todos los meses, enlaces fijos)."""
import re, os, json, html, asyncio
from playwright.async_api import async_playwright

ROOT = os.environ.get('PM_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = 'precios/informe-precios-barcos-ocasion%s.pdf'

L = {
 'es': dict(pre='', title='Informe de precios de barcos de ocasión', month='Octubre 2026',
            sub='Precios que se piden en anuncios, por modelo y por año', years='Por modelo y año', ycol=['Modelo', 'Años', 'Horquilla'],
            types='Por tipo de barco', calc_h='¿Y tu barco?',
            calc_p='Con la calculadora ves la horquilla de tu modelo y año en un minuto. Si tu modelo no está, o quieres una orientación con tus datos (motor, horas, puerto), escríbeme y lo miramos.',
            calc_l='Calculadora', wa_l='WhatsApp',
            small='Informe orientativo, elaborado con anuncios públicos: son precios pedidos, no precios de cierre ni tasaciones. Podemos equivocarnos y nada de lo que aparece aquí es vinculante ni constituye una oferta.',
            page='Página'),
 'ca': dict(pre='ca/', title="Informe de preus de vaixells d'ocasió", month='Octubre 2026',
            sub="Preus que es demanen en anuncis, per model i per any", years='Per model i any', ycol=['Model', 'Anys', 'Forquilla'],
            types='Per tipus de vaixell', calc_h='I el teu vaixell?',
            calc_p="Amb la calculadora veus la forquilla del teu model i any en un minut. Si el teu model no hi és, o vols una orientació amb les teves dades (motor, hores, port), escriu-me i ho mirem.",
            calc_l='Calculadora', wa_l='WhatsApp',
            small="Informe orientatiu, elaborat amb anuncis públics: són preus demanats, no preus de tancament ni taxacions. Ens podem equivocar i res del que apareix aquí és vinculant ni constitueix una oferta.",
            page='Pàgina'),
 'en': dict(pre='en/', title='Used boat price report', month='October 2026',
            sub='Asking prices in listings, by model and by year', years='By model and year', ycol=['Model', 'Years', 'Range'],
            types='By boat type', calc_h='What about your boat?',
            calc_p='The calculator shows the range for your model and year in a minute. If your model is not there, or you would like a view based on your details (engine, hours, marina), message me and we will look at it.',
            calc_l='Calculator', wa_l='WhatsApp',
            small='Indicative report based on public listings: these are asking prices, not sale prices or surveys. We may be wrong, and nothing here is binding or an offer.',
            page='Page'),
 'fr': dict(pre='fr/', title='Rapport sur les prix des bateaux d’occasion', month='Octobre 2026',
            sub='Prix demandés dans les annonces, par modèle et par année', years='Par modèle et par année', ycol=['Modèle', 'Années', 'Fourchette'],
            types='Par type de bateau', calc_h='Et votre bateau ?',
            calc_p='Avec le calculateur, vous voyez la fourchette de votre modèle et de votre année en une minute. Si votre modèle n’y est pas, ou si vous voulez une estimation avec vos données (moteur, heures, port), écrivez-moi et nous regardons ensemble.',
            calc_l='Calculateur', wa_l='WhatsApp',
            small='Rapport indicatif établi à partir d’annonces publiques : ce sont des prix demandés, pas des prix de vente ni des expertises. Nous pouvons nous tromper et rien de ce qui figure ici n’est contractuel ni ne constitue une offre.',
            page='Page'),
}


def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def inner(s):
    """Conserva <strong>/<em>, quita enlaces y demás etiquetas."""
    s = re.sub(r'<(?!/?(strong|em)\b)[^>]+>', '', s)
    return s.strip()


def rows(tb):
    return [[c for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr, re.S)] for tr in re.findall(r'<tr.*?</tr>', tb, re.S)]


def money(n, lang):
    s = '{:,}'.format(n)
    if lang == 'en':
        return '€' + s
    s = s.replace(',', '.' if lang in ('es', 'ca') else ' ')
    return s + ' €'


def bands():
    t = open(os.path.join(ROOT, 'cuanto-vale-mi-barco/calc.js'), encoding='utf-8').read()
    out = {}
    for s, n, b in re.findall(r"\{s:'([^']+)',n:'([^']+)',b:(\[\[.*?\]\])\}", t):
        out[s] = (n, json.loads(b))
    return out


def parse(lang):
    t = open(os.path.join(ROOT, L[lang]['pre'] + 'precios/index.html'), encoding='utf-8').read()
    tables = re.findall(r'<table.*?</table>', t, re.S)
    mrows = rows(tables[0])
    trows = rows(tables[1])
    models = []
    for r in mrows[1:]:
        slug = re.search(r'/modelos/([a-z0-9-]+)\.html', r[5]).group(1)
        models.append(dict(slug=slug, cells=[strip(c) for c in r[:5]]))
    fac = re.search(r'id="factores"[^>]*>.*?</h2>\s*<ul>(.*?)</ul>', t, re.S).group(1)
    return dict(
        mhead=[strip(c) for c in mrows[0][:5]], models=models,
        thead=[strip(c) for c in trows[0]], types=[[strip(c) for c in r] for r in trows[1:]],
        lead=inner(re.search(r'<p class="lead">(.*?)</p>', t, re.S).group(1)),
        notes=[inner(x) for x in re.findall(r'<p class="note">(.*?)</p>', t, re.S)],
        fac_h=strip(re.search(r'<h2 id="factores">(.*?)</h2>', t, re.S).group(1)),
        fac=[inner(x) for x in re.findall(r'<li>(.*?)</li>', fac, re.S)],
        met_h=strip(re.search(r'<h2 id="metodo">(.*?)</h2>', t, re.S).group(1)),
        met=inner(re.search(r'<h2 id="metodo">.*?</h2>\s*<p>(.*?)</p>', t, re.S).group(1)),
        mod_h=strip(re.search(r'<h2 id="modelos">(.*?)</h2>', t, re.S).group(1)),
        aviso=inner(re.search(r'<p class="aviso">(.*?)</p>', t, re.S).group(1)),
    )


CSS = '''
@font-face{font-family:"Hanken Grotesk";src:url(file://%(root)s/hanken-grotesk.woff2) format("woff2");font-weight:100 900}
@page{size:A4;margin:14mm 15mm 16mm}
*{box-sizing:border-box}
body{margin:0;font-family:"Hanken Grotesk",Helvetica,Arial,sans-serif;color:#0D1C27;font-size:9.6pt;line-height:1.45}
.top{display:flex;justify-content:space-between;align-items:center;border-bottom:1.4pt solid #0E3042;padding-bottom:4mm;margin-bottom:6mm}
.top img{height:15mm}
.top .m{text-align:right;font-size:8.5pt;color:#44545F;line-height:1.35}
.top .m b{display:block;color:#0E3042;font-size:10pt;letter-spacing:.06em;text-transform:uppercase}
h1{font-size:21pt;line-height:1.1;margin:0 0 2mm;color:#0E3042;letter-spacing:-.01em}
.sub{font-size:11pt;color:#17465F;margin:0 0 5mm;font-weight:600}
.lead{font-size:10.2pt;margin:0 0 6mm}
h2{font-size:12.5pt;color:#0E3042;margin:6mm 0 3mm;padding-bottom:1.5mm;border-bottom:.8pt solid #B7C3CB;break-after:avoid}
table{width:100%%;border-collapse:collapse;font-size:9pt;break-inside:auto}
th{text-align:left;font-weight:700;color:#fff;background:#0E3042;padding:2mm 2.4mm}
td{padding:1.7mm 2.4mm;border-bottom:.5pt solid #DDE3E8;vertical-align:top}
tr{break-inside:avoid}
td.n,th.n{text-align:right;white-space:nowrap}
tr.g td{border-top:.9pt solid #9FB0BC}
table.y td{padding:1.15mm 2.4mm;font-size:8.7pt}
td.mn{font-weight:650;color:#0E3042}
.note{font-size:8.4pt;color:#44545F;margin:2.5mm 0 0}
ul{margin:0;padding-left:5mm}
li{margin:0 0 1.6mm}
.cta{margin-top:7mm;background:#0E3042;color:#fff;border-radius:2mm;padding:5mm 6mm;break-inside:avoid}
.cta h3{margin:0 0 1.5mm;font-size:12pt}
.cta p{margin:0 0 3mm;color:#DCE4EA}
.cta .l{display:flex;gap:8mm;flex-wrap:wrap;font-weight:700;font-size:9.5pt}
.cta .l span{color:#D9C28A;font-weight:600}
.small{margin-top:6mm;font-size:7.8pt;color:#5E707C;border-top:.5pt solid #B7C3CB;padding-top:3mm;break-inside:avoid}
.small p{margin:0 0 1.5mm}
.pb{break-before:page}
'''


def build_html(lang, b, logo_url):
    c, d = L[lang], parse(lang)
    pre = '' if lang == 'es' else '/' + lang
    h = d['mhead']
    m_rows = ''.join('<tr><td class="mn">%s</td><td>%s</td><td class="n">%s</td><td class="n">%s</td><td class="n">%s</td></tr>' % tuple(html.escape(x) for x in m['cells']) for m in d['models'])
    y_rows = ''
    for m in d['models']:
        name, bb = b[m['slug']]
        for i, (y1, y2, lo, hi) in enumerate(bb):
            rng = '%s – %s' % (money(lo, lang), money(hi, lang)) if hi else money(lo, lang) + ' +'
            y_rows += '<tr%s><td class="mn">%s</td><td>%d–%d</td><td class="n">%s</td></tr>' % (
                ' class="g"' if i == 0 else '', html.escape(name) if i == 0 else '', y1, y2, rng)
    t_rows = ''.join('<tr>' + ''.join('<td%s>%s</td>' % (' class="n"' if j == 2 else '', html.escape(x)) for j, x in enumerate(r)) + '</tr>' for r in d['types'])
    body = '''
<div class="top"><img src="%(logo)s" alt="Plata Marine"><div class="m"><b>%(month)s</b>www.platamarine.com</div></div>
<h1>%(title)s</h1>
<p class="sub">%(sub)s</p>
<p class="lead">%(lead)s</p>
<h2>%(mod_h)s</h2>
<table><thead><tr><th>%(h0)s</th><th>%(h1)s</th><th class="n">%(h2)s</th><th class="n">%(h3)s</th><th class="n">%(h4)s</th></tr></thead><tbody>%(m_rows)s</tbody></table>
%(notes)s
<h2 class="pb">%(years)s</h2>
<table class="y"><thead><tr><th>%(y0)s</th><th>%(y1)s</th><th class="n">%(y2)s</th></tr></thead><tbody>%(y_rows)s</tbody></table>
<h2>%(types)s</h2>
<table><thead><tr><th>%(t0)s</th><th>%(t1)s</th><th class="n">%(t2)s</th></tr></thead><tbody>%(t_rows)s</tbody></table>
<h2>%(fac_h)s</h2>
<ul>%(fac)s</ul>
<h2>%(met_h)s</h2>
<p>%(met)s</p>
<div class="cta"><h3>%(calc_h)s</h3><p>%(calc_p)s</p><div class="l"><div>%(calc_l)s: <span>www.platamarine.com%(pre)s/cuanto-vale-mi-barco/</span></div><div>%(wa_l)s: <span>+34 633 742 973</span></div></div></div>
<div class="small"><p>%(small)s</p><p>%(aviso)s</p></div>
''' % dict(logo=logo_url, month=c['month'], title=html.escape(c['title']), sub=html.escape(c['sub']), lead=d['lead'], mod_h=html.escape(d['mod_h']),
           h0=h[0], h1=h[1], h2=h[2], h3=h[3], h4=h[4], m_rows=m_rows, notes=''.join('<p class="note">%s</p>' % n for n in d['notes']),
           years=html.escape(c['years']), y0=c['ycol'][0], y1=c['ycol'][1], y2=c['ycol'][2], y_rows=y_rows,
           types=html.escape(c['types']), t0=d['thead'][0], t1=d['thead'][1], t2=d['thead'][2], t_rows=t_rows,
           fac_h=html.escape(d['fac_h']), fac=''.join('<li>%s</li>' % x for x in d['fac']), met_h=html.escape(d['met_h']), met=d['met'],
           calc_h=html.escape(c['calc_h']), calc_p=html.escape(c['calc_p']), calc_l=c['calc_l'], wa_l=c['wa_l'], pre=pre,
           small=html.escape(c['small']), aviso=d['aviso'])
    return '<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>%s · %s · Plata Marine</title><style>%s</style></head><body>%s</body></html>' % (
        lang, html.escape(c['title']), c['month'], CSS % {'root': ROOT}, body)


FOOT = '<div style="width:100%%;font:7.5pt Helvetica,Arial,sans-serif;color:#7F929E;padding:0 15mm;display:flex;justify-content:space-between"><span>Plata Marine · %s · %s</span><span>%s <span class="pageNumber"></span>/<span class="totalPages"></span></span></div>'


async def main():
    b = bands()
    logo = 'file://' + os.path.join(ROOT, 'logo-plata-marine.png')
    tmpdir = os.environ.get('TMPDIR', '/tmp')
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page()
        for lang in ('es', 'ca', 'en', 'fr'):
            c = L[lang]
            tmp = os.path.join(tmpdir, 'informe_precios_%s.html' % lang)
            open(tmp, 'w', encoding='utf-8').write(build_html(lang, b, logo))
            await pg.goto('file://' + tmp)
            await pg.wait_for_timeout(200)
            out = os.path.join(ROOT, OUT % ('' if lang == 'es' else '-' + lang))
            await pg.pdf(path=out, format='A4', print_background=True, display_header_footer=True,
                         header_template='<div></div>', footer_template=FOOT % (html.escape(c['title']), c['month'], c['page']),
                         margin={'top': '14mm', 'bottom': '16mm', 'left': '15mm', 'right': '15mm'})
            os.remove(tmp)
            print(out, os.path.getsize(out) // 1024, 'KB')
        await br.close()

if __name__ == '__main__':
    asyncio.run(main())
