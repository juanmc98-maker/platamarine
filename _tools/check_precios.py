"""Comprueba que los rangos de la calculadora (cuanto-vale-mi-barco/calc.js) coinciden con las fichas de /modelos/ en ES/CA/EN/FR.
Lanzar tras la revisión mensual de precios:  python3 _tools/check_precios.py
Registro de observaciones: _tools/precios_observaciones.csv (una fila por anuncio revisado; solo datos públicos del anuncio, nunca datos del vendedor)."""
import re, html, sys
js = open('cuanto-vale-mi-barco/calc.js', encoding='utf-8').read()
M = re.findall(r"\{s:'([^']+)',n:'[^']+',b:(\[\[.*?\]\])\}", js)
def forms(n): return {f"{n:,}".replace(',', '.'), f"{n:,}", f"{n:,}".replace(',', ' '), f"{n:,}".replace(',', ' ')}
bad = 0
for slug, b in M:
    for l in ['', 'ca/', 'en/', 'fr/']:
        t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', open(f'{l}modelos/{slug}.html', encoding='utf-8').read())))
        for y0, y1, lo, hi in eval(b):
            for v in [lo] + ([hi] if hi else []):
                if not any(x in t for x in forms(v)): bad += 1; print('NO COINCIDE', l or 'es/', slug, y0, y1, v)
print(f'{len(M)} modelos revisados, {bad} diferencias'); sys.exit(1 if bad else 0)
