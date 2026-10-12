"""Oceanis 50 (12 oct 2026, Juan): horas del motor "sin datos" (sin hablar del propietario), palo/botavara/jarcia en una
sola línea del equipamiento y amarre de alquiler (dicho por el propietario). ES/CA/EN/FR. Idempotente.
Uso: python3 _tools/fix_oceanis_datos.py"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
R = {
 'es': [('<dd>Sin contador de horas</dd>', '<dd>Sin datos</dd>'), (' El motor no tiene contador de horas.', ''),
        ('<li>Palo</li><li>Botavara y jarcia fija de 2019</li>', '<li>Palo, botavara y jarcia fija de 2019</li>'),
        ('<dt>Amarre</dt><dd>Se confirma con el vendedor</dd>', '<dt>Amarre</dt><dd>De alquiler</dd>')],
 'ca': [("<dd>Sense comptador d'hores</dd>", '<dd>Sense dades</dd>'), (" El motor no té comptador d'hores.", ''),
        ('<li>Pal</li><li>Botavara i eixàrcia fixa del 2019</li>', '<li>Pal, botavara i eixàrcia fixa del 2019</li>'),
        ('<dt>Amarratge</dt><dd>Es confirma amb el venedor</dd>', '<dt>Amarratge</dt><dd>De lloguer</dd>')],
 'en': [('<dd>No hour meter</dd>', '<dd>No data</dd>'), (' The engine has no hour meter.', ''),
        ('<li>Mast</li><li>Boom and standing rigging from 2019</li>', '<li>Mast, boom and standing rigging from 2019</li>'),
        ('<dt>Berth</dt><dd>Confirmed with the seller</dd>', '<dt>Berth</dt><dd>Rented</dd>')],
 'fr': [('<dd>Pas de compteur d’heures</dd>', '<dd>Pas de données</dd>'), (' Le moteur n’a pas de compteur d’heures.', ''),
        ('<li>Mât</li><li>Bôme et gréement dormant de 2019</li>', '<li>Mât, bôme et gréement dormant de 2019</li>'),
        ('<dt>Place de port</dt><dd>À confirmer avec le vendeur</dd>', '<dt>Place de port</dt><dd>Louée</dd>')],
}
for lang, reps in R.items():
    p = ROOT / ('' if lang == 'es' else lang) / 'barcos' / 'oceanis-50.html'
    s0 = s = p.read_text()
    for a, b in reps:
        s = s.replace(a, b)
    if s != s0: p.write_text(s); print('ok', lang)
    for a, _ in reps:
        if a in s: print('QUEDA', lang, a)
