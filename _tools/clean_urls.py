#!/usr/bin/env python3
"""Quita el .html de los enlaces internos de www.platamarine.com.

Uso: python3 _tools/clean_urls.py [--dry]
Idempotente. Toca .html, sitemap*.xml, search/*.json, *.txt y los .js del sitio
(no _tools). Las URL antiguas con .html siguen abriendo (GitHub Pages).
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {'.git', '_tools', 'node_modules'}
KEEP = ('googledd8c57b3752e5141',)

TOK = re.compile(
    r'(?P<pre>["\'(=>])'
    r'(?P<url>(?:https://www\.platamarine\.com)?(?!//)[A-Za-z0-9_\-./]+?)'
    r'\.html'
    r'(?P<post>[#?"\')<\s,\]])'
)


def clean(url):
    if any(k in url for k in KEEP):
        return None
    if url.endswith('/'):
        return None
    if url == 'index':
        return './'
    if url.endswith('/index'):
        return url[:-5]
    return url


def sub_tokens(text):
    def rep(m):
        new = clean(m.group('url'))
        if new is None:
            return m.group(0)
        return m.group('pre') + new + m.group('post')
    prev = None
    while prev != text:  # tokens contiguos (p. ej. "a.html,b.html")
        prev = text
        text = TOK.sub(rep, text)
    return text


JS_FIX = [
    # concatenaciones slug + '.html'
    ("b.slug + '.html'", "b.slug"),
    ("m.s+'.html\">'", "m.s+'\">'"),
    ("fixed.slug + '.html\">", "fixed.slug + '\">"),
    ("x.slug + '.html\">", "x.slug + '\">"),
    # analytics: detectar barco en enlaces con o sin .html
    ("a[href*=\"barcos/\"][href$=\".html\"]", "a[href*=\"barcos/\"]"),
    ("match(/([a-z0-9-]+)\\.html$/)", "match(/([a-z0-9-]+)(?:\\.html)?$/)"),
]

NAV_HEAD = ("/* URL limpia: si se entra por una dirección con .html, se muestra sin él (nov 2026) */\n"
            "(function(){try{var p=location.pathname;if(/\\.html$/.test(p)&&p.indexOf('googledd')<0){"
            "history.replaceState(null,'',p.replace(/index\\.html$/,'').replace(/\\.html$/,'')+location.search+location.hash);}}catch(e){}})();\n")


def files():
    for p in ROOT.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS:
            continue
        if p.suffix in ('.html', '.js', '.txt') or (p.suffix == '.xml' and p.name.startswith('sitemap')) \
                or (p.suffix == '.json' and rel.parts[0] == 'search'):
            if any(k in p.name for k in KEEP):
                continue
            yield p, rel


def main():
    dry = '--dry' in sys.argv
    changed = []
    for p, rel in files():
        t = p.read_text(encoding='utf-8')
        n = t
        if p.suffix == '.js':
            for a, b in JS_FIX:
                n = n.replace(a, b)
        n = sub_tokens(n)
        if str(rel) == 'nav.js' and 'URL limpia' not in n:
            n = NAV_HEAD + n
        if n != t:
            changed.append(str(rel))
            if not dry:
                p.write_text(n, encoding='utf-8')
    print(len(changed), 'archivos cambiados')
    for c in changed:
        if not c.endswith('.html'):
            print('  ', c)


if __name__ == '__main__':
    main()
