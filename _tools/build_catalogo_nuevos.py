#!/usr/bin/env python3
"""Barcos nuevos en el catálogo /barcos/ (ES/CA/EN/FR): mete las tarjetas de los modelos nuevos de SeaStorm, Sunrise
y Catharsis (las de SKIPPER ya están escritas a mano en la página) entre los marcadores
<!-- nuevos-marcas --> … <!-- /nuevos-marcas -->, con data-new="1" para que salgan con el filtro Estado = Nuevos.
También deja la tarjeta "Barcos nuevos" de arriba y los enlaces de barcos nuevos con las cuatro marcas, y que el filtro
"Sin título" encuentre los barcos que se pueden llevar sin titulación.
Datos: build_sunrise.py, build_seastorm.py y build_catharsis.py. Se puede lanzar varias veces (sustituye el bloque).
Uso (desde la raíz del repo): python3 _tools/build_catalogo_nuevos.py"""
import re, os, sys, html, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_sunrise as SR      # noqa: E402
import build_seastorm as SS     # noqa: E402
import build_catharsis as CT    # noqa: E402

ROOT = '.'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
LI = ['es', 'ca', 'en', 'fr']
WA = '34633742973'
VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': 'HT'}
M0, M1 = '<!-- nuevos-marcas -->', '<!-- /nuevos-marcas -->'
BRANDS_TXT = ('SeaStorm, Sunrise, Catharsis y SKIPPER', 'SeaStorm, Sunrise, Catharsis i SKIPPER', 'SeaStorm, Sunrise, Catharsis and SKIPPER', 'SeaStorm, Sunrise, Catharsis et SKIPPER')

C = {
 'es': dict(new='Nuevo', from_='Desde', lic='Titulación', wa='Preguntar por WhatsApp', see='Ver el barco', wa_txt='Hola Juan, me interesa el {} nuevo. ¿Podemos hablar?',
            pax='personas', out='fueraborda hasta {} cv, motor aparte', eco='motor eléctrico incluido', cath='dos fueraborda (hasta 600 cv en total), motores aparte',
            sin='Sin título con motor de hasta 15 CV; con más, Licencia de Navegación o superior',
            bsel='{b}, desde {p}&nbsp;€ <span class="vat">+IVA</span>', more='Barcos nuevos: <a href="{h}">{b}&nbsp;→</a>',
            morel='<p><strong>Barcos nuevos:</strong> <a href="{h}">{b}, desde {p} € +IVA</a></p>'),
 'ca': dict(new='Nou', from_='Des de', lic='Titulació', wa='Preguntar per WhatsApp', see='Veure el vaixell', wa_txt='Hola Juan, m\'interessa el {} nou. Podem parlar?',
            pax='persones', out='fora borda fins a {} cv, motor a part', eco='motor elèctric inclòs', cath='dos fora borda (fins a 600 cv en total), motors a part',
            sin='Sense títol amb motor de fins a 15 CV; amb més, Llicència de Navegació o superior',
            bsel='{b}, des de {p}&nbsp;€ <span class="vat">+IVA</span>', more='Vaixells nous: <a href="{h}">{b}&nbsp;→</a>',
            morel='<p><strong>Vaixells nous:</strong> <a href="{h}">{b}, des de {p} € +IVA</a></p>'),
 'en': dict(new='New', from_='From', lic='Licence', wa='Ask on WhatsApp', see='See the boat', wa_txt='Hi Juan, I\'m interested in the new {}. Can we talk?',
            pax='people', out='outboard up to {} hp, engine extra', eco='electric engine included', cath='twin outboards (up to 600 hp in total), engines extra',
            sin='No licence with an engine up to 15 hp; above that, Licencia de Navegación or higher',
            bsel='{b}, from €{p} <span class="vat">+VAT</span>', more='New boats: <a href="{h}">{b}&nbsp;→</a>',
            morel='<p><strong>New boats:</strong> <a href="{h}">{b}, from €{p} +VAT</a></p>'),
 'fr': dict(new='Neuf', from_='À partir de', lic='Permis', wa='Demander sur WhatsApp', see='Voir le bateau', wa_txt='Bonjour Juan, le {} neuf m’intéresse. Pouvons-nous en parler ?',
            pax='personnes', out='hors-bord jusqu’à {} ch, moteur en sus', eco='moteur électrique inclus', cath='deux hors-bord (jusqu’à 600 ch au total), moteurs en sus',
            sin='Sans permis avec un moteur jusqu’à 15 ch ; au-delà, Licencia de Navegación ou supérieur',
            bsel='{b}, à partir de {p}&nbsp;€ <span class="vat">HT</span>', more='Bateaux neufs : <a href="{h}">{b}&nbsp;→</a>',
            morel='<p><strong>Bateaux neufs :</strong> <a href="{h}">{b}, à partir de {p} € HT</a></p>'),
}
# Textos que decían solo "SKIPPER" (descripción, schema e intro del catálogo)
FIX = {
 'es': [('y barcos nuevos SKIPPER. Habla con Juan Morante.', 'y barcos nuevos de SeaStorm, Sunrise, Catharsis y SKIPPER. Habla con Juan Morante.'),
        ('y barcos nuevos SKIPPER por encargo.', 'y barcos nuevos por encargo de SeaStorm, Sunrise, Catharsis y SKIPPER.')],
 'ca': [('i vaixells nous SKIPPER. Parla amb Juan Morante.', 'i vaixells nous de SeaStorm, Sunrise, Catharsis i SKIPPER. Parla amb Juan Morante.'),
        ('i vaixells nous SKIPPER per encàrrec.', 'i vaixells nous per encàrrec de SeaStorm, Sunrise, Catharsis i SKIPPER.')],
 'en': [('plus new SKIPPER boats. Prices, photos', 'plus new SeaStorm, Sunrise, Catharsis and SKIPPER boats. Prices, photos'),
        ('plus new SKIPPER boats built to order.', 'plus new boats built to order by SeaStorm, Sunrise, Catharsis and SKIPPER.')],
 'fr': [('et bateaux neufs SKIPPER. Prix, photos', 'et bateaux neufs SeaStorm, Sunrise, Catharsis et SKIPPER. Prix, photos'),
        ('et des SKIPPER neufs construits sur commande.', 'et des bateaux neufs SeaStorm, Sunrise, Catharsis et SKIPPER construits sur commande.')],
}
CSS = ('<style id="nuevos-marcas-css">.bimg.bimg-logo{display:flex;align-items:center;justify-content:center;aspect-ratio:16/10;background:#0E3042}'
       '.bimg.bimg-logo img{width:62%;height:auto;aspect-ratio:auto;object-fit:contain;background:none}.bimg img.ct{object-fit:contain;background:#fff}</style>')


def eur(n, lang, nb=True):
    s = f'{n:,}'
    if lang == 'en':
        return s
    if lang == 'fr':
        return s.replace(',', '&nbsp;' if nb else ' ')
    return s.replace(',', '.')


def num(s, lang):
    return s.replace(',', '.') if lang == 'en' else s


def size(path):
    try:
        from PIL import Image
        return Image.open(ROOT + path).size
    except Exception:
        return (800, 600)


def models(lang):
    """Modelos nuevos (sin SKIPPER) con los datos de su generador."""
    li = LI.index(lang)
    c = C[lang]
    out = []
    for m in SS.M:
        slug, name, L, hp, price = m[0], m[1], m[2], m[9], m[12]
        over5 = m[13]
        out.append(dict(name=name, href=f'/seastorm/#seastorm-{slug}', brand='seastorm', price=price,
                        img=f'/seastorm/fotos/{slug}-1-m.jpg', full=f'/seastorm/fotos/{slug}-1.jpg',
                        sub=f'{num(L, lang)} m · {c["out"].format(hp)}',
                        tit=1 if over5 else 0, lic=SS.T[lang]['lic_short'] if over5 else c['sin'], d=SS.T[lang]['d'][slug],
                        comb='gasolina', motor='fuera'))
    for slug, name, L, B, pax, hp, price, nph, lic, inc in SR.M:
        out.append(dict(name=f'Sunrise {name}', href=f'/sunrise/#sunrise-{slug}', brand='sunrise', price=price, contain=True,
                        img=f'/sunrise/fotos/{slug}-1-m.jpg', full=f'/sunrise/fotos/{slug}-1.jpg',
                        sub=f'{num(L, lang)} m · {pax} {c["pax"]} · {c["eco"] if hp is None else c["out"].format(hp)}',
                        tit={'sin': 0, 'ln': 1, 'pnb': 2}[lic], lic=c['sin'] if lic == 'sin' else SR.T[lang]['lic'][lic], d=SR.T[lang]['d'][slug],
                        comb='' if hp is None else 'gasolina', motor='fuera'))
    out.append(dict(name='Catharsis 930', href='/catharsis/', brand='catharsis', price=CT.PRICE,
                    img='/catharsis/fotos/catharsis-930-1-m.jpg', full='/catharsis/fotos/catharsis-930-1.jpg',
                    sub=f'{num("9,30", lang)} m · {c["cath"]}', tit=3, lic=CT.T[lang]['lic'], d=CT.T[lang]['d'].split('. ')[0] + '.',
                    comb='gasolina', motor='fuera'))
    out.sort(key=lambda m: -m['price'])
    return out


def cards(lang):
    p = LANGS[lang]
    c = C[lang]
    vat = VAT[lang]
    s = ''
    for i, m in enumerate(models(lang)):
        href = p + m['href']
        if os.path.exists(ROOT + m['img']):
            w, h = size(m['img'])
            fw = size(m['full'])[0] if os.path.exists(ROOT + m['full']) else w
            ss = f' srcset="{m["img"]} {w}w, {m["full"]} {fw}w"' if fw > w else ''
            ct = ' class="ct"' if m.get('contain') else ''
            pic = f'<a class="bimg" href="{href}"><img{ct} src="{m["img"]}"{ss} sizes="(max-width: 820px) 100vw, 560px" alt="{html.escape(m["name"])}" loading="lazy" width="{w}" height="{h}"><span class="status new">{c["new"]}</span></a>'
        else:  # sin fotos del modelo: logo de la marca (nunca la foto de otro modelo)
            pic = f'<a class="bimg bimg-logo" href="{href}"><img src="/seastorm/fotos/seastorm-logo.png" alt="{html.escape(m["name"])}" loading="lazy" width="840" height="60"><span class="status new">{c["new"]}</span></a>'
        wa = f'https://wa.me/{WA}?text=' + urllib.parse.quote(c['wa_txt'].format(m['name']), safe='')
        price = f'{c["from_"]} €{eur(m["price"], lang)}' if lang == 'en' else f'{c["from_"]} {eur(m["price"], lang)}{"&nbsp;" if lang == "fr" else " "}€'
        s += f'''
      <article class="bcard bnew" data-new="1" data-sold="0" data-brand="{m['brand']}" data-tipo="motor" data-titulo="{m['tit']}" data-precio="{m['price']}" data-zona="" data-comb="{m['comb']}" data-motor="{m['motor']}" data-anyo="2026" data-i="{-0.95 + i * 0.03:.2f}">
        {pic}
        <div class="bbody">
          <div class="head" style="margin:0 0 6px"><h2><a href="{href}">{html.escape(m['name'])}</a></h2><p class="price">{price} <span class="vat">{vat}</span></p></div>
          <p class="sub" style="margin:0">{html.escape(m['sub'], quote=False)}</p>
          <span class="tbadge">{c['lic']}: {html.escape(m['lic'], quote=False)}</span>
          <p class="bdesc">{html.escape(m['d'], quote=False)}</p>
          <div class="bcta"><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{c['wa']}</a><a class="btn btn-ghost" href="{href}">{c['see']}</a></div>
        </div>
      </article>'''
    return M0 + '\n      ' + CSS + s + '\n      ' + M1


def low(lang):
    return min([m['price'] for m in models(lang)] + [329000])


def build(lang):
    p = LANGS[lang]
    li = LI.index(lang)
    c = C[lang]
    path = f'{ROOT}{p}/barcos/index.html'
    s = open(path, encoding='utf-8').read()
    b = BRANDS_TXT[li]
    hub = f'{p}/barcos-nuevos/'
    # 1) tarjetas de modelos
    blk = cards(lang)
    if M0 in s:
        s = re.sub(re.escape(M0) + r'.*?' + re.escape(M1), lambda m: blk, s, count=1, flags=re.S)
    else:
        m = re.search(r'<article class="bcard bnew"[^>]*data-i="-1">.*?</article>', s, flags=re.S)
        assert m, lang
        s = s[:m.end()] + '\n      ' + blk + s[m.end():]
    # 2) tarjeta "Barcos nuevos" de arriba
    s, n = re.subn(r'(<a href="#nuevos" data-estado="nuevo">.*?<small>).*?(</small>)',
                   lambda m: m.group(1) + c['bsel'].format(b=b, p=eur(low(lang), lang)) + m.group(2), s, count=1, flags=re.S)
    assert n == 1, lang
    # 3) una sola línea con las cuatro marcas (antes: "ver la marca SKIPPER" + "Otras marcas nuevas")
    s, n = re.subn(r'<p class="bsel-more">.*?</nav>', lambda m: '<p class="bsel-more">' + c['more'].format(h=hub, b=b) + '</p></nav>', s, count=1, flags=re.S)
    assert n == 1, lang
    # 4) bloque de enlaces de abajo: "Barcos pequeños nuevos: Sunrise" -> las cuatro marcas
    s, n = re.subn(r'(<div class="bmorel">)<p><strong>[^<]*</strong> <a href="[^"]*(?:/sunrise/|/barcos-nuevos/)">[^<]*</a></p>',
                   lambda m: m.group(1) + c['morel'].format(h=hub, b=b, p=eur(low(lang), lang, nb=False)), s, count=1)
    assert n == 1, lang
    # 5) textos que solo nombraban SKIPPER
    for a, z in FIX[lang]:
        s = s.replace(a, z)
    # 6) filtro "Sin título": que encuentre los barcos con data-titulo="0"
    s = s.replace("ok=ok&&(+tl>=need)&&!(c.dataset.tipo==='vela'&&+tl<3)&&+tl>0;", "ok=ok&&(+tl>=need)&&!(c.dataset.tipo==='vela'&&+tl<3);")
    s = s.replace('/* Estado: nuevo (SKIPPER, data-new="1")', '/* Estado: nuevo (barcos nuevos de todas las marcas, data-new="1")')
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', lang, len(s))


if __name__ == '__main__':
    for l in LANGS:
        build(l)
