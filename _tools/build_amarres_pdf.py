"""PDF descargable "Precios de amarres en Cataluña 2026" (ES/CA/EN/FR) a partir de la tabla de la guía de cada idioma.
Uso: PM_ROOT=<repo> python3 _tools/build_amarres_pdf.py
Salida: guias/precios-amarres-cataluna-2026.pdf (ES) y -ca / -en / -fr.
Si cambian las tarifas de la guía (tarea de 1 marzo y 1 septiembre), relanzar.
"""
import os, re, io, html, base64, asyncio
import qrcode
from PIL import Image
from playwright.async_api import async_playwright

ROOT = os.environ.get('PM_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = 'amarres-cataluna-tipos-precios-alquiler-compra'
L = {
 'es': dict(pre='', out='precios-amarres-cataluna-2026.pdf',
   k='Tabla de precios', t='Amarres en Cataluña 2026', s='Tarifas oficiales de 19 puertos, para un barco de unos 8 × 3 m y otro de unos 12 × 4 m, en amarre de base anual y en tránsito.',
   notes=['Las cifras salen de las tarifas publicadas por cada puerto o club para 2026 (2025 en Port Ginesta). Revisadas en septiembre de 2026.',
          'Las marcadas con ≈ son cálculos a partir de una tarifa por metro cuadrado.',
          'Cada puerto incluye cosas distintas (IVA, tasa, agua y luz): mira la última columna antes de comparar.'],
   h2='¿Y ahora qué?', c1='¿Tienes un amarre que alquilar o traspasar?', c1s='Puedo publicarlo en mi web sin coste por adelantado. Cuéntame el puerto y las medidas.',
   c2='¿Buscas barco y sitio donde tenerlo?', c2s='Te digo qué puertos encajan con el barco que tienes en mente y qué preguntar antes de firmar.',
   scan='Guía completa, con lo que hay que saber antes de alquilar o comprar un amarre',
   legal='Información orientativa, elaborada con las tarifas publicadas por cada puerto. Puede contener errores y cambiar en cualquier momento, y no es vinculante: confirma siempre la tarifa y lo que incluye con el puerto o club.'),
 'ca': dict(pre='ca/', out='precios-amarres-cataluna-2026-ca.pdf',
   k='Taula de preus', t='Amarratges a Catalunya 2026', s="Tarifes oficials de 19 ports, per a un vaixell d'uns 8 × 3 m i un altre d'uns 12 × 4 m, en amarratge de base anual i en trànsit.",
   notes=["Les xifres surten de les tarifes publicades per cada port o club per al 2026 (2025 a Port Ginesta). Revisades el setembre de 2026.",
          'Les marcades amb ≈ són càlculs a partir d’una tarifa per metre quadrat.',
          'Cada port inclou coses diferents (IVA, taxa, aigua i llum): mira l’última columna abans de comparar.'],
   h2='I ara què?', c1='Tens un amarratge per llogar o traspassar?', c1s='El puc publicar al meu web sense cap cost per avançat. Explica’m el port i les mides.',
   c2='Busques vaixell i lloc on tenir-lo?', c2s='Et dic quins ports encaixen amb el vaixell que tens al cap i què cal preguntar abans de signar.',
   scan='Guia completa, amb el que cal saber abans de llogar o comprar un amarratge',
   legal='Informació orientativa, feta amb les tarifes publicades per cada port. Pot contenir errors i canviar en qualsevol moment, i no és vinculant: confirma sempre la tarifa i què inclou amb el port o club.'),
 'en': dict(pre='en/', out='precios-amarres-cataluna-2026-en.pdf',
   k='Price table', t='Moorings in Catalonia 2026', s='Official rates at 19 marinas, for a boat of about 8 × 3 m and one of about 12 × 4 m, on an annual base berth and in transit.',
   notes=['Figures come from the rates published by each marina or club for 2026 (2025 at Port Ginesta). Reviewed in September 2026.',
          'Figures marked ≈ are my own calculations from a per-square-metre rate.',
          'Each marina includes different things (VAT, harbour fee, water and power): check the last column before comparing.'],
   h2='What next?', c1='Do you have a berth to rent out or transfer?', c1s='I can list it on my website with no upfront cost. Tell me the marina and the size.',
   c2='Looking for a boat and somewhere to keep it?', c2s='I can tell you which marinas suit the boat you have in mind and what to ask before you sign.',
   scan='Full guide, with what you need to know before renting or buying a berth',
   legal='For guidance only, based on the rates published by each marina. It may contain errors and change at any time, and it is not binding: always confirm the rate and what it includes with the marina or club.'),
 'fr': dict(pre='fr/', out='precios-amarres-cataluna-2026-fr.pdf',
   k='Tableau des prix', t='Places de port en Catalogne 2026', s="Tarifs officiels de 19 ports, pour un bateau d'environ 8 × 3 m et un autre d'environ 12 × 4 m, en place annuelle et en escale.",
   notes=['Les chiffres proviennent des tarifs publiés par chaque port ou club pour 2026 (2025 à Port Ginesta). Revus en septembre 2026.',
          'Les chiffres précédés de ≈ sont des calculs à partir d’un tarif au mètre carré.',
          'Chaque port inclut des choses différentes (TVA, taxe, eau et électricité) : regardez la dernière colonne avant de comparer.'],
   h2='Et maintenant ?', c1='Vous avez une place de port à louer ou à céder ?', c1s='Je peux la publier sur mon site sans frais à l’avance. Indiquez-moi le port et les dimensions.',
   c2='Vous cherchez un bateau et une place où le garder ?', c2s='Je vous dis quels ports conviennent au bateau que vous envisagez et quoi demander avant de signer.',
   scan='Guide complet, avec ce qu’il faut savoir avant de louer ou d’acheter une place de port',
   legal="Information indicative, établie à partir des tarifs publiés par chaque port. Elle peut contenir des erreurs et changer à tout moment, et n'est pas contractuelle : confirmez toujours le tarif et ce qu'il comprend auprès du port ou du club. Nous ne parlons pas français : ce texte a été traduit avec un outil de traduction."),
}

def table(lang):
    s = open(os.path.join(ROOT, L[lang]['pre'] + 'guias', SLUG + '.html'), encoding='utf-8').read()
    t = s[s.find('<table'):s.find('</table>')]
    rows = []
    for r in re.findall(r'<tr.*?</tr>', t, flags=re.S):
        cells = []
        for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, flags=re.S):
            m = re.search(r'<(small|span)[^>]*>(.*?)</\1>', c, flags=re.S)
            sub = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip() if m else ''
            if m: c = c.replace(m.group(0), '')
            main = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', c))).strip()
            cells.append((main, sub))
        rows.append(cells)
    return rows

def b64(path, maxw=None):
    im = Image.open(path).convert('RGBA')
    if maxw: im.thumbnail((maxw, maxw))
    b = io.BytesIO(); im.save(b, 'PNG'); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

def qr(url):
    q = qrcode.QRCode(border=1, box_size=10); q.add_data(url); q.make(fit=True)
    b = io.BytesIO(); q.make_image(fill_color='#0E3042', back_color='white').save(b, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

CSS = '''@font-face{font-family:A;src:url(%(fa)s) format('woff2');font-weight:100 900}@font-face{font-family:S;src:url(%(fs)s) format('woff2');font-weight:200 900}
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body{margin:0;font-family:S,Georgia,serif;color:#0D1C27}
.page{width:297mm;height:210mm;position:relative;overflow:hidden;page-break-after:always;padding:10mm 14mm 14mm}
.top{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:1.5px solid #B58A2C;padding-bottom:3mm;margin-bottom:3mm}
.k{font-family:A;font-weight:600;font-size:8.5pt;letter-spacing:.14em;text-transform:uppercase;color:#17465F}
h1{font-family:A;font-weight:700;font-size:18pt;margin:.5mm 0 1mm}.s{font-size:9pt;color:#44545F;max-width:190mm;margin:0}
.top img{height:13mm}
table{width:100%%;border-collapse:collapse;font-size:7.3pt;line-height:1.2}
th{font-family:A;font-weight:600;text-align:left;font-size:7.6pt;color:#fff;background:#0E3042;padding:1.6mm 2mm}
td{padding:1mm 2mm;border-bottom:.5px solid #D5DCE0;vertical-align:top}
tr:nth-child(even) td{background:#F3F5F6}td:first-child{font-family:A;font-weight:600;width:22%%}td:last-child{color:#44545F;width:30%%}
td small{display:inline;margin-left:1.5mm;font-family:S;font-weight:400;color:#7F929E;font-size:6.8pt}
.foot{position:absolute;left:15mm;right:15mm;bottom:7mm;display:flex;justify-content:space-between;font-family:A;font-size:7.5pt;color:#7F929E}
.notes{margin:2mm 0 0;padding:0 0 0 4mm;font-size:9pt;line-height:1.5;color:#44545F}
h2{font-family:A;font-size:18pt;margin:7mm 0 6mm}.cards{display:flex;gap:9mm}
.card{flex:1;border-top:3px solid #B58A2C;background:#F3F5F6;padding:7mm 8mm}.card h3{font-family:A;font-size:13pt;margin:0 0 3mm}.card p{margin:0;font-size:10.5pt;line-height:1.45}
.wa{margin-top:10mm;font-family:A;font-size:12pt;font-weight:600;color:#0B766B}
.qr{display:flex;gap:7mm;align-items:center;margin-top:8mm}.qr img{width:31mm}.qr p{margin:0;font-size:10pt;max-width:150mm}.qr b{font-family:A;font-size:11pt;display:block;margin-top:1.5mm;color:#17465F}
.legal{position:absolute;left:15mm;right:15mm;bottom:15mm;font-size:7.4pt;color:#7F929E;line-height:1.4}'''

def font(n):
    return 'data:font/woff2;base64,' + base64.b64encode(open(os.path.join(ROOT, n), 'rb').read()).decode()
FA = font('archivo.woff2'); FS = font('source-serif-4.woff2')

def build(lang, logo):
    c = L[lang]; rows = table(lang)
    url = 'www.platamarine.com/' + c['pre'] + 'guias/' + SLUG
    head = ''.join('<th>%s</th>' % html.escape(m) for m, _ in rows[0])
    body = ''.join('<tr>%s</tr>' % ''.join('<td>%s%s</td>' % (html.escape(m), '<small>%s</small>' % html.escape(s) if s else '') for m, s in r) for r in rows[1:])
    foot = '<div class="foot"><span>Plata Marine · Juan Morante</span><span>%s</span></div>' % url
    p1 = '<section class="page"><div class="top"><div><div class="k">%s</div><h1>%s</h1><p class="s">%s</p></div><img src="%s" alt="Plata Marine"></div><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>%s</section>' % (
        c['k'], c['t'], c['s'], logo, head, body, foot)
    p2 = '<section class="page"><div class="top"><div><div class="k">%s</div><h1>%s</h1></div><img src="%s" alt="Plata Marine"></div><ul class="notes">%s</ul><h2>%s</h2><div class="cards"><div class="card"><h3>%s</h3><p>%s</p></div><div class="card"><h3>%s</h3><p>%s</p></div></div><p class="wa">WhatsApp +34 633 742 973 · juan@platamarine.com</p><div class="qr"><img src="%s" alt=""><p>%s<b>%s</b></p></div><p class="legal">%s</p>%s</section>' % (
        c['k'], c['t'], logo, ''.join('<li>%s</li>' % n for n in c['notes']), c['h2'], c['c1'], c['c1s'], c['c2'], c['c2s'], qr('https://' + url), c['scan'], url, c['legal'], foot)
    return '<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>%s · Plata Marine</title><style>%s</style></head><body>%s%s</body></html>' % (lang, c['t'], CSS % {'fa': FA, 'fs': FS}, p1, p2)

async def main():
    logo = b64(os.path.join(ROOT, 'logo-plata-marine.png'), 700)
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page()
        for lang in L:
            await pg.set_content(build(lang, logo), wait_until='load')
            await pg.wait_for_timeout(300)
            out = os.path.join(ROOT, 'guias', L[lang]['out'])
            await pg.pdf(path=out, print_background=True, prefer_css_page_size=True)
            try:
                import pikepdf
                with pikepdf.open(out, allow_overwriting_input=True) as pdf:
                    with pdf.open_metadata(set_pikepdf_as_editor=False) as m:
                        for key in list(m.keys()): del m[key]
                    [pdf.docinfo.__delitem__(k) for k in list(pdf.docinfo.keys())]
                    pdf.docinfo['/Title'] = L[lang]['t']; pdf.docinfo['/Author'] = 'Plata Marine'
                    pdf.save(out)
            except ImportError:
                pass
            print(out, os.path.getsize(out))
        await br.close()

asyncio.run(main())
