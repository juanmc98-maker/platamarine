"""Rellena el texto alternativo de las miniaturas de galería de las fichas de barcos (ES/CA/EN/FR).
Formato: "{Modelo} – foto N" (ES/CA) / "{Modelo} – photo N" (EN/FR), N = posición en la galería.
Solo toca miniaturas con alt vacío; las que ya tienen descripción propia se respetan.
El modelo sale de inventario.js (campo name), nunca el nombre de la embarcación.
Uso: python3 _tools/alt_galeria.py   (idempotente; relanzar tras crear o regenerar una ficha)"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = dict(re.findall(r"slug: '([^']+)', name: '([^']+)'", open(os.path.join(ROOT, 'inventario.js'), encoding='utf-8').read()))
WORD = {'': 'foto', 'ca': 'foto', 'en': 'photo', 'fr': 'photo'}


def fix(path, lang):
    slug = os.path.basename(path)[:-5]
    name = NAMES.get(slug)
    t = open(path, encoding='utf-8').read()
    if not name or 'class="thumbs"' not in t:
        return 0
    n = [0]

    def rep(m):
        tag = m.group(0)
        if 'data-full=' not in tag or re.search(r'\balt="[^"]', tag):
            return tag
        i = int(re.search(r'data-i="(\d+)"', tag).group(1)) + 1
        alt = html.escape('%s – %s %d' % (name, WORD[lang], i), quote=True)
        n[0] += 1
        if re.search(r'\balt=""', tag):
            return tag.replace('alt=""', 'alt="%s"' % alt, 1)
        return tag.replace('<img ', '<img alt="%s" ' % alt, 1)

    t2 = re.sub(r'<img [^>]*>', rep, t)
    if t2 != t:
        open(path, 'w', encoding='utf-8').write(t2)
    return n[0]


if __name__ == '__main__':
    for lang in ('', 'ca', 'en', 'fr'):
        d = os.path.join(ROOT, lang, 'barcos')
        for f in sorted(os.listdir(d)):
            if f.endswith('.html') and f != 'index.html':
                c = fix(os.path.join(d, f), lang)
                if c:
                    print('%s/%s: %d' % (lang or 'es', f, c))
