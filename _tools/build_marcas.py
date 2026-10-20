#!/usr/bin/env python3
"""/marcas/ ya no es una página propia: todas las marcas de barcos nuevos (SeaStorm, Sunrise, Catharsis y SKIPPER)
están juntas en /barcos-nuevos/ (generador: build_barcos_nuevos.py). Este script deja /marcas/ (ES/CA/EN/FR)
como redirección a /barcos-nuevos/ de su idioma (meta refresh + canonical + noindex), igual que otras páginas retiradas.
Uso: python3 _tools/build_marcas.py  (desde la raíz del repo)"""
import os

ROOT = '.'
BASE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
TXT = {'es': 'Barcos nuevos: SeaStorm, Sunrise, Catharsis y SKIPPER', 'ca': 'Vaixells nous: SeaStorm, Sunrise, Catharsis i SKIPPER',
       'en': 'New boats: SeaStorm, Sunrise, Catharsis and SKIPPER', 'fr': 'Bateaux neufs : SeaStorm, Sunrise, Catharsis et SKIPPER'}

if __name__ == '__main__':
    for lang, p in LANGS.items():
        to = f'{p}/barcos-nuevos/'
        out = (f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
               f'<meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{BASE}{to}"><title>Plata Marine</title></head>'
               f'<body><p><a href="{to}">{TXT[lang]}</a></p></body></html>\n')
        os.makedirs(f'{ROOT}{p}/marcas', exist_ok=True)
        open(f'{ROOT}{p}/marcas/index.html', 'w', encoding='utf-8').write(out)
        print('ok', lang, len(out))
