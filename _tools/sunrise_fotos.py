#!/usr/bin/env python3
"""Fotos de /sunrise/ (ES/CA/EN/FR), oct 2026: galerías por modelo con número de fotos variable y portada nueva.
Edita las páginas publicadas en su sitio (no las regenera) y es idempotente. Relanzar después de build_sunrise.py.
Fotos: originales de sunriseyacht.pl y de boatcenter.pl (distribuidor polaco del fabricante), en /sunrise/fotos/<slug>-<n>.jpg
(hasta 1400 px) y <slug>-<n>-m.jpg (800 px), sin EXIF. Las fotos recortadas sobre fondo blanco llevan class="cut"
(se ven enteras sobre gris claro); las del agua llenan el marco. Portada: /sunrise/fotos/hero.jpg (680 DC en cala).
Uso (desde la raíz del repo): python3 _tools/sunrise_fotos.py"""
import re, html

LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
NAMES = {'700-eco-tender': '700 ECO Tender', '680-dc': '680 DC', '645': '645', '606-br': '606 BR',
         '530-open': '530 Open', '545': '545', '530-tender': '530 Tender', '400-open': '400 Open'}
# 1 = foto recortada sobre fondo blanco
CUT = {
 '700-eco-tender': [0, 0],
 '680-dc': [0, 0, 0, 0, 0, 0, 0, 1, 1],
 '645': [0] * 9,
 '606-br': [0, 0, 1, 1, 1, 1],
 '530-open': [1] * 7,
 '545': [1],
 '530-tender': [0, 0, 0, 0, 1, 1, 1, 1],
 '400-open': [1] * 4,
}
CSS_OLD = '.sr-gal img{flex:0 0 100%;width:100%;height:auto;aspect-ratio:4/3;object-fit:contain;scroll-snap-align:start;background:#fff}'
CSS_NEW = ('.sr-gal img{flex:0 0 100%;width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;scroll-snap-align:start;background:#F3F6F7}'
           '.sr-gal img.cut{object-fit:contain;background:#fff}')
HERO_ALT = 'Sunrise 680 DC'


def gal(slug, lang):
    name = NAMES[slug]
    w = 'foto' if lang in ('es', 'ca') else 'photo'
    out = []
    for i, c in enumerate(CUT[slug], 1):
        cls = ' class="cut"' if c else ''
        out.append(f'<img{cls} src="/sunrise/fotos/{slug}-{i}-m.jpg" srcset="/sunrise/fotos/{slug}-{i}-m.jpg 800w, /sunrise/fotos/{slug}-{i}.jpg 1400w" '
                   f'sizes="(max-width:820px) 100vw, 560px" alt="Sunrise {name} – {w} {i}" width="800" height="533" loading="lazy" decoding="async">')
    return ''.join(out)


def run():
    for lang, pre in LANGS.items():
        p = f'.{pre}/sunrise/index.html'
        s = open(p, encoding='utf-8').read()
        s = s.replace(CSS_OLD, CSS_NEW)
        if CSS_NEW not in s:
            raise SystemExit('CSS de galería no encontrado en ' + p)
        for slug in CUT:
            s, n = re.subn(r'(<article class="sr-m" id="sunrise-' + re.escape(slug) + r'">\s*<div><div class="sr-gal"[^>]*>).*?(</div></div>)',
                           lambda m: m.group(1) + gal(slug, lang) + m.group(2), s, count=1, flags=re.S)
            if n != 1:
                raise SystemExit(f'galería {slug} no encontrada en {p}')
            # con una sola foto no se dice "desliza"
            if len(CUT[slug]) == 1:
                s = re.sub(r'(<article class="sr-m" id="sunrise-' + re.escape(slug) + r'">(?:(?!</article>).)*?)<p class="sr-hint">[^<]*</p>\s*', r'\1', s, count=1, flags=re.S)
        s = re.sub(r'<img class="ph" src="/sunrise/fotos/[^"]+" alt="[^"]*" width="\d+" height="\d+"',
                   f'<img class="ph" src="/sunrise/fotos/hero.jpg" alt="{HERO_ALT}" width="1021" height="680"', s, count=1)
        s = re.sub(r'(<meta property="og:image" content=")[^"]*', r'\g<1>https://www.platamarine.com/sunrise/fotos/hero.jpg', s)
        s = re.sub(r'<meta property="og:image:width" content="\d+">', '<meta property="og:image:width" content="1021">', s)
        s = re.sub(r'<meta property="og:image:height" content="\d+">', '<meta property="og:image:height" content="680">', s)
        s = s.replace('.sr-hero img.ph{display:block;width:100%;height:auto;aspect-ratio:16/8;max-height:420px;object-fit:cover}',
                      '.sr-hero img.ph{display:block;width:100%;height:auto;aspect-ratio:16/8;max-height:420px;object-fit:cover;object-position:50% 60%}')
        open(p, 'w', encoding='utf-8').write(s)
        print('ok', p)


if __name__ == '__main__':
    run()
