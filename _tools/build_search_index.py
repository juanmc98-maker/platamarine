# -*- coding: utf-8 -*-
"""Índice del buscador de la web (lupa de la cabecera). Genera /search/es.json, ca.json, en.json y fr.json
con título, descripción y URL de cada página indexable de su idioma. Volver a lanzarlo al publicar páginas nuevas.
Uso: python3 _tools/build_search_index.py   (desde la raíz del repo)"""
import os, re, json, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SKIP_DIRS = {'_tools', 'video', '.git', 'search', 'fotos-guia'}
SKIP_FILES = {'404.html', 'hero-video.html'}
out = {'es': [], 'ca': [], 'en': [], 'fr': []}

def clean(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()

for dp, dns, fns in os.walk(ROOT):
    rel = os.path.relpath(dp, ROOT)
    parts = [] if rel == '.' else rel.split(os.sep)
    if any(p in SKIP_DIRS or p.startswith('.') for p in parts):
        dns[:] = []
        continue
    for fn in fns:
        if not fn.endswith('.html') or fn in SKIP_FILES or fn.startswith('google'):
            continue
        p = os.path.join(dp, fn)
        s = open(p, encoding='utf-8', errors='ignore').read()
        if re.search(r'<meta name="robots" content="[^"]*noindex', s) or 'http-equiv="refresh"' in s:
            continue
        lang = parts[0] if parts and parts[0] in ('ca', 'en', 'fr') else 'es'
        t = clean((re.search(r'<title>(.*?)</title>', s, re.S) or [None, ''])[1])
        t = re.sub(r'\s*[·|]\s*Plata Marine\s*$', '', t)
        d = clean((re.search(r'<meta name="description" content="([^"]*)"', s) or [None, ''])[1])
        h = clean((re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S) or [None, ''])[1])
        url = '/' + ('' if rel == '.' else rel.replace(os.sep, '/') + '/') + ('' if fn == 'index.html' else fn)
        if not t:
            continue
        out[lang].append({'u': url, 't': t, 'd': d[:220], 'h': h if h and h != t else ''})

os.makedirs(os.path.join(ROOT, 'search'), exist_ok=True)
for l, items in out.items():
    items.sort(key=lambda x: (x['u'].count('/'), x['u']))
    json.dump(items, open(os.path.join(ROOT, 'search', l + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(l, len(items), os.path.getsize(os.path.join(ROOT, 'search', l + '.json')), 'bytes')
