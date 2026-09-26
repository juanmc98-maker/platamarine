"""Genera las fichas PDF de Plata Marine (ES/CA/EN) a partir de la ficha HTML de cada idioma.
Uso: python3 build_pdfs.py [slug ...]   (sin argumentos: todos)
Salida: barcos/<slug>.pdf (ES), barcos/<slug>-ca.pdf, barcos/<slug>-en.pdf
"""
import re, sys, os, io, base64, html, asyncio
import qrcode
from PIL import Image
from playwright.async_api import async_playwright

ROOT = '/home/claude/platamarine'
SLUGS = ['starfisher-840', 'oceanis-50', 'sealine-365', 'monte-carlo-27', 'van-de-stadt-36', 'monterey-278-ss',
         'faeton-730-moraga', 'sacs-535', 'ranieri-azzurra-5m']
L = {
 'es': dict(pre='', sale='EN VENTA', sold='VENDIDO', langtag='Ficha en español', tech='Resumen técnico', gal='Galería',
            interest='¿Te interesa este barco?', interest2='Escríbeme y lo vemos juntos, sin compromiso.',
            soldt='Este barco ya está vendido', soldt2='Si buscas uno parecido, mira los barcos disponibles o crea una alerta en la web.',
            scan='Ficha completa y todas las fotos', broker='Broker náutico',
            legal='Plata Marine gestiona el contacto y la operación como intermediario. La información de esta ficha procede del propietario y se comprueba con la documentación antes de la venta; tiene carácter informativo y los datos definitivos serán los que figuren en el contrato de compraventa. Precio sin gastos de cambio de titularidad. Se recomienda prueba de mar y, si el comprador lo desea, peritaje independiente.',
            date='Ficha actualizada el 26/09/2026'),
 'ca': dict(pre='ca/', sale='EN VENDA', sold='VENUT', langtag='Fitxa en català', tech='Resum tècnic', gal='Galeria',
            interest="T'interessa aquest vaixell?", interest2="Escriu-me i el veiem junts, sense compromís.",
            soldt='Aquest vaixell ja està venut', soldt2='Si en busques un de semblant, mira els vaixells disponibles o crea una alerta al web.',
            scan='Fitxa completa i totes les fotos', broker='Broker nàutic',
            legal="Plata Marine gestiona el contacte i l'operació com a intermediari. La informació d'aquesta fitxa prové del propietari i es comprova amb la documentació abans de la venda; té caràcter informatiu i les dades definitives seran les que figurin al contracte de compravenda. Preu sense despeses de canvi de titularitat. Es recomana prova de mar i, si el comprador ho vol, peritatge independent.",
            date='Fitxa actualitzada el 26/09/2026'),
 'en': dict(pre='en/', sale='FOR SALE', sold='SOLD', langtag='Listing in English', tech='Technical summary', gal='Gallery',
            interest='Interested in this boat?', interest2="Message me and we'll look at it together, no obligation.",
            soldt='This boat has been sold', soldt2='If you are after something similar, see the boats available or set up an alert on the website.',
            scan='Full listing and all photos', broker='Nautical broker',
            legal='Plata Marine handles the contact and the transaction as an intermediary. The information in this listing comes from the owner and is checked against the documentation before the sale; it is for information only and the final details will be those stated in the sale contract. Price excludes ownership-transfer costs. A sea trial is recommended and, if the buyer wishes, an independent survey.',
            date='Listing updated 26/09/2026'),
}

def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def img_data(path, maxw=1200, q=72):
    im = Image.open(path).convert('RGB')
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def qr_data(url):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(url); q.make(fit=True)
    im = q.make_image(fill_color='#0D1C27', back_color='white')
    b = io.BytesIO(); im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

def parse(slug, lang):
    p = os.path.join(ROOT, L[lang]['pre'] + 'barcos/' + slug + '.html')
    t = open(p, encoding='utf-8').read()
    name = strip(re.search(r'<h1>(.*?)</h1>', t, re.S).group(1))
    sub = [strip(x) for x in re.findall(r'<span>(.*?)</span>', re.search(r'<div class="sub">(.*?)</div>', t, re.S).group(1))]
    price = strip(re.search(r'<p class="price">(.*?)</p>', t, re.S).group(1))
    sold = 'schema.org/SoldOut' in t
    specs = [(strip(a), strip(b)) for a, b in re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', re.search(r'<dl class="specs">(.*?)</dl>', t, re.S).group(1))]
    prose = re.search(r'<div class="prose">(.*?)</div>', t, re.S).group(1)
    h2 = strip(re.search(r'<h2>(.*?)</h2>', prose, re.S).group(1))
    paras = [p for p in re.findall(r'<p>(.*?)</p>', prose, re.S)]
    thumbs = re.findall(r'<img src="/([a-z0-9-]+-\d+\.jpg)"', re.search(r'<div class="gal">(.*?)</div>\s*</div>', t, re.S).group(1))
    seen = []
    for x in thumbs:
        if x not in seen: seen.append(x)
    url = 'https://www.platamarine.com/' + L[lang]['pre'] + 'barcos/' + slug + '.html'
    return dict(name=name, sub=sub, price=price, sold=sold, specs=specs, h2=h2, paras=paras, photos=seen, url=url)

CSS = '''
@font-face{font-family:"Archivo";src:url(file://%(root)s/archivo.woff2) format("woff2-variations");font-weight:100 900;font-stretch:62%% 125%%}
@font-face{font-family:"Source Serif 4";src:url(file://%(root)s/source-serif-4.woff2) format("woff2-variations");font-weight:200 900}
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:"Source Serif 4",Georgia,serif;color:#0D1C27;font-size:10.5pt;line-height:1.5}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}
.page:last-child{page-break-after:auto}
.pad{padding:16mm 16mm 22mm}
h1,h2,h3,.disp{font-family:"Archivo",Arial,sans-serif}
.foot{position:absolute;left:16mm;right:16mm;bottom:9mm;display:flex;justify-content:space-between;font:8pt "Archivo",Arial,sans-serif;color:#7F929E;border-top:0.4pt solid #B7C3CB;padding-top:3mm}
.cover-img{height:168mm;background-size:cover;background-position:center}
.band{background:#0E3042;color:#fff;padding:9mm 16mm;display:flex;justify-content:space-between;align-items:center}
.band .k{font:700 9pt "Archivo",Arial;letter-spacing:.22em;color:#D9C28A}
.band .n{font:700 25pt/1.05 "Archivo",Arial;font-stretch:90%%;margin-top:2mm}
.band img{height:15mm}
.band.sold .k{color:#fff;background:#B23A2E;display:inline-block;padding:1.2mm 3mm;border-radius:1mm}
.cov{padding:9mm 16mm 0}
.cov .meta{font:600 10.5pt "Archivo",Arial;color:#44545F}
.cov .price{font:750 24pt "Archivo",Arial;color:#17465F;margin-top:3mm}
.cov .price.sold{color:#B23A2E}
.cov .lang{display:inline-block;margin-top:5mm;font:600 8pt "Archivo",Arial;letter-spacing:.08em;text-transform:uppercase;color:#44545F;border:0.6pt solid #B7C3CB;border-radius:1mm;padding:1mm 2.5mm}
.cov .broker{font:600 9pt "Archivo",Arial;color:#7F929E;margin-top:2mm}
h2.sec{font:700 14pt "Archivo",Arial;margin:0 0 4mm;color:#0E3042;border-bottom:1.2pt solid #B58A2C;padding-bottom:2mm}
table.specs{width:100%%;border-collapse:collapse;font:9.5pt "Archivo",Arial;margin-bottom:7mm}
table.specs th{text-align:left;width:34%%;font-weight:650;color:#44545F;padding:2mm 3mm;vertical-align:top}
table.specs td{padding:2mm 3mm;vertical-align:top}
table.specs tr:nth-child(odd){background:#F3F5F6}
.prose p{margin:0 0 3mm;text-align:left}
.gal{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.gal div{height:76mm;background-size:cover;background-position:center;border-radius:1mm}
.contact{background:#0E3042;color:#fff;height:297mm;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 24mm}
.contact h2{font:700 22pt "Archivo",Arial;margin:0}
.contact .s{color:#C9D3D9;margin:3mm 0 10mm}
.contact .qr{background:#fff;padding:3mm;border-radius:2mm}
.contact .qr img{width:42mm;height:42mm;display:block}
.contact .u{font:600 9pt "Archivo",Arial;margin-top:3mm;color:#D9C28A;word-break:break-all}
.contact .who{font:600 11pt "Archivo",Arial;margin-top:12mm;line-height:1.7}
.contact .legal{position:absolute;bottom:14mm;left:24mm;right:24mm;font:7.8pt/1.45 "Archivo",Arial;color:#AFC0CA}
.contact .logo{height:14mm;margin-bottom:12mm}
'''

def page_foot(d, n):
    return '<div class="foot"><span>%s</span><span>Plata Marine · %s</span><span>%d</span></div>' % (
        html.escape(d['url'].replace('https://', '')), html.escape(d['name']), n)

def build_html(slug, lang, logo_white):
    c = L[lang]; d = parse(slug, lang)
    ph = [img_data(os.path.join(ROOT, x)) for x in d['photos']]
    pages = []
    status = c['sold'] if d['sold'] else c['sale']
    meta = ' · '.join(d['sub'][:1] + d['sub'][-1:]) if d['sub'] else ''
    pages.append('''<section class="page"><div class="cover-img" style="background-image:url(%s)"></div>
<div class="band%s"><div><div class="k">%s</div><div class="n">%s</div></div><img src="%s" alt="Plata Marine"></div>
<div class="cov"><div class="meta">%s</div><div class="price%s">%s</div>
<div class="broker">Plata Marine · %s · Juan Morante · 633 742 973 · juan@platamarine.com</div>
<div class="lang">%s</div></div>%s</section>''' % (
        ph[0], ' sold' if d['sold'] else '', status, html.escape(d['name']), logo_white,
        html.escape(' · '.join(d['sub'])), ' sold' if d['sold'] else '', html.escape(d['price']),
        c['broker'], c['langtag'], page_foot(d, 1)))
    rows = ''.join('<tr><th>%s</th><td>%s</td></tr>' % (html.escape(a), html.escape(b)) for a, b in d['specs'])
    paras = ''.join('<p>%s</p>' % re.sub(r'<(?!/?strong)[^>]+>', '', p) for p in d['paras'])
    pages.append('<section class="page"><div class="pad"><h2 class="sec">%s</h2><table class="specs">%s</table><h2 class="sec">%s</h2><div class="prose">%s</div></div>%s</section>' % (
        c['tech'], rows, html.escape(d['h2']), paras, page_foot(d, 2)))
    n = 3
    rest = ph[1:]
    for i in range(0, len(rest), 6):
        cells = ''.join('<div style="background-image:url(%s)"></div>' % x for x in rest[i:i + 6])
        pages.append('<section class="page"><div class="pad"><h2 class="sec">%s · %s</h2><div class="gal">%s</div></div>%s</section>' % (
            html.escape(d['name']), c['gal'], cells, page_foot(d, n)))
        n += 1
    h, s = (c['soldt'], c['soldt2']) if d['sold'] else (c['interest'], c['interest2'])
    pages.append('''<section class="page"><div class="contact"><img class="logo" src="%s" alt="Plata Marine"><h2>%s</h2><p class="s">%s</p>
<div class="qr"><img src="%s" alt=""></div><div class="u">%s<br>%s</div>
<div class="who">Juan Morante · Plata Marine<br>WhatsApp 633 742 973 · juan@platamarine.com</div>
<p class="legal">%s<br>%s</p></div></section>''' % (
        logo_white, h, s, qr_data(d['url']), c['scan'], html.escape(d['url'].replace('https://', '')), c['legal'], c['date']))
    return '<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s</body></html>' % (
        lang, html.escape(d['name']), CSS % {'root': ROOT}, ''.join(pages)), d

def logo_white():
    im = Image.open(os.path.join(ROOT, 'logo-plata-marine.png')).convert('RGBA')
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a: px[x, y] = (255, 255, 255, a)
    im.thumbnail((900, 300))
    b = io.BytesIO(); im.save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

async def main(slugs):
    lw = logo_white()
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page()
        for slug in slugs:
            for lang in ['es', 'ca', 'en']:
                doc, d = build_html(slug, lang, lw)
                tmp = '/tmp/claude-0/pdf_%s_%s.html' % (slug, lang)
                open(tmp, 'w', encoding='utf-8').write(doc)
                await pg.goto('file://' + tmp); await pg.wait_for_timeout(150)
                out = os.path.join(ROOT, 'barcos', slug + ('' if lang == 'es' else '-' + lang) + '.pdf')
                await pg.pdf(path=out, format='A4', print_background=True, prefer_css_page_size=True)
                print(out, os.path.getsize(out) // 1024, 'KB', 'SOLD' if d['sold'] else '')
        await br.close()

if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:] or SLUGS))
