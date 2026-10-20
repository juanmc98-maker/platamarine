#!/usr/bin/env python3
"""Quita el país / la ciudad de fábrica de las páginas de SKIPPER (/skipper/ y subpáginas, 4 idiomas) y de sus
tarjetas en /barcos/ y del bloque SKIPPER de la portada. Decisión de Juan (20 oct 2026): no poner el país de los astilleros de barcos nuevos.
Las páginas de SKIPPER no tienen generador vigente: este script se puede lanzar tantas veces como haga falta.
Uso (desde la raíz del repo): python3 _tools/sin_pais_skipper.py"""
import glob

R = [  # de lo más largo a lo más corto
 ('Semirrígidas griegas ', 'Semirrígidas '), ('Semirígides gregues ', 'Semirígides '), ('Greek RIBs ', 'RIBs '), ('Semi-rigides grecs ', 'Semi-rigides '),
 # ES
 ('En Koropi, a las afueras de Atenas (Grecia), en el astillero BSK Marine, fundado en 2015', 'En el astillero BSK Marine, fundado en 2015'),
 ('astillero fundado en 2015 en Koropi, a las afueras de Atenas', 'astillero fundado en 2015'),
 ('en el astillero de SKIPPER en Koropi, cerca de Atenas', 'en el astillero de SKIPPER'),
 ('la fábrica de SKIPPER en Koropi (Atenas)', 'la fábrica de SKIPPER'),
 ('la fábrica de Koropi (Atenas)', 'la fábrica'),
 ('la fábrica de Koropi', 'la fábrica'),
 (' en Koropi, a las afueras de Atenas', ' en el astillero'),
 (' en Koropi, cerca de Atenas', ' en el astillero'),
 (' en Koropi (Atenas)', ' en el astillero'),
 ('prueba de mar en Atenas, con visita', 'prueba de mar, con visita'),
 ('prueba de mar en Atenas', 'prueba de mar en el astillero'),
 ('Prueba de mar en Grecia', 'Prueba de mar en el astillero'),
 ('a la fábrica de Atenas', 'a la fábrica'),
 ('Fabricado en Grecia, entrega en España', 'Entrega en España'),
 ('Semirrígidas griegas fabricadas por encargo en Koropi (Atenas), del molde', 'Semirrígidas fabricadas por encargo, del molde'),
 # CA
 ('A Koropi, als afores d’Atenes (Grècia), a la drassana BSK Marine, fundada el 2015', 'A la drassana BSK Marine, fundada el 2015'),
 ('drassana fundada el 2015 a Koropi, als afores d’Atenes', 'drassana fundada el 2015'),
 ('a la drassana de SKIPPER a Koropi, a prop d’Atenes', 'a la drassana de SKIPPER'),
 ('la fàbrica de SKIPPER a Koropi (Atenes)', 'la fàbrica de SKIPPER'),
 ('la fàbrica de Koropi (Atenes)', 'la fàbrica'),
 ('la fàbrica de Koropi', 'la fàbrica'),
 (' a Koropi, als afores d’Atenes', ' a la drassana'),
 (' a Koropi, a prop d’Atenes', ' a la drassana'),
 (' a Koropi (Atenes)', ' a la drassana'),
 ('prova de mar a Atenes, amb visita', 'prova de mar, amb visita'),
 ('prova de mar a Atenes', 'prova de mar a la drassana'),
 ('Prova de mar a Grècia', 'Prova de mar a la drassana'),
 ('a la fàbrica d’Atenes', 'a la fàbrica'),
 ('Fabricat a Grècia, entrega a Espanya', 'Entrega a Espanya'),
 ("Semirígides gregues fabricades per encàrrec a Koropi (Atenes), del motlle", "Semirígides fabricades per encàrrec, del motlle"),
 # EN
 ('In Koropi, on the outskirts of Athens (Greece), at the BSK Marine yard, founded in 2015', 'At the BSK Marine yard, founded in 2015'),
 ('a yard founded in 2015 in Koropi, near Athens', 'a yard founded in 2015'),
 ('at the SKIPPER yard in Koropi, near Athens', 'at the SKIPPER yard'),
 ('the SKIPPER factory in Koropi (Athens)', 'the SKIPPER factory'),
 ('the factory in Koropi (Athens)', 'the factory'),
 ('the factory in Koropi', 'the factory'),
 (' in Koropi, on the outskirts of Athens', ' at the yard'),
 (' in Koropi, near Athens', ' at the yard'),
 (' in Koropi (Athens)', ' at the yard'),
 ('sea trial in Athens with the yard, including', 'sea trial with the yard, including'),
 ('sea trial in Athens, including', 'sea trial, including'),
 ('sea trial in Athens', 'sea trial at the yard'),
 ('Sea trial in Greece', 'Sea trial at the yard'),
 ('from the factory in Athens', 'from the factory'),
 ('Built in Greece, delivered in Spain', 'Delivered in Spain'),
 ('Greek RIBs built to order in Koropi (Athens), from the mould', 'RIBs built to order, from the mould'),
 # FR
 ('À Koropi, près d’Athènes (Grèce), au chantier BSK Marine, fondé en 2015', 'Au chantier BSK Marine, fondé en 2015'),
 ('chantier fondé en 2015 à Koropi, près d’Athènes', 'chantier fondé en 2015'),
 ('au chantier SKIPPER de Koropi, près d’Athènes', 'au chantier SKIPPER'),
 ('l’usine SKIPPER à Koropi (Athènes)', 'l’usine SKIPPER'),
 ('l’usine de Koropi (Athènes)', 'l’usine'),
 ('l’usine de Koropi', 'l’usine'),
 (' à Koropi, près d’Athènes', ' au chantier'),
 (' à Koropi (Athènes)', ' au chantier'),
 ('essai en mer à Athènes, avec visite', 'essai en mer, avec visite'),
 ('essai en mer à Athènes', 'essai en mer au chantier'),
 ('Essai en mer en Grèce', 'Essai en mer au chantier'),
 ('à l’usine d’Athènes', 'à l’usine'),
 ('Construit en Grèce, livré en Espagne', 'Livré en Espagne'),
 ('Semi-rigides grecs construits sur commande à Koropi (Athènes), du moule', 'Semi-rigides construits sur commande, du moule'),
]

files = []
for pre in ('', 'ca/', 'en/', 'fr/'):
    files += glob.glob(pre + 'skipper/index.html') + glob.glob(pre + 'skipper/*/index.html') + [pre + 'barcos/index.html', pre + 'index.html']
for f in files:
    s = open(f, encoding='utf-8').read()
    o = s
    for a, b in R:
        s = s.replace(a, b)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s)
        print('ok', f)
