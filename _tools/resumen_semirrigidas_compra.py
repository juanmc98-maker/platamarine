# -*- coding: utf-8 -*-
"""Página de compra de semirrígidas (ES/CA/EN/FR): sustituye los bloques técnicos «flotadores» y «casco,
consola y motor» por un resumen corto que lleva a la guía, para que la página de listado y la guía no
compitan por las mismas búsquedas. Idempotente."""
import re
G = 'comprar-semirrigida-segunda-mano'
L = {
 '': '<h2 id="s1">Qué revisar antes de comprar una</h2><p>En una semirrígida usada lo primero son los flotadores (material, edad, costuras y si mantienen la presión), después el motor (horas, facturas y arranque en frío), el espejo de popa, los papeles y, si lo lleva, el remolque. Lo tienes punto por punto en la guía para <a href="/guias/%s/">comprar una semirrígida de segunda mano</a>.</p>' % G,
 'ca/': '<h2 id="s1">Què revisar abans de comprar-ne una</h2><p>En una semirígida usada el primer són els flotadors (material, edat, costures i si mantenen la pressió), després el motor (hores, factures i arrencada en fred), el mirall de popa, els papers i, si en porta, el remolc. Ho tens punt per punt a la guia per <a href="/ca/guias/%s/">comprar una semirígida de segona mà</a>.</p>' % G,
 'en/': '<h2 id="s1">What to check before you buy</h2><p>On a used RIB, start with the tubes (material, age, seams and whether they hold pressure), then the engine (hours, invoices and a cold start), the transom, the paperwork and, if it has one, the trailer. It\'s all covered point by point in the guide to <a href="/en/guias/%s/">buying a used RIB</a>.</p>' % G,
 'fr/': '<h2 id="s1">Que vérifier avant d’acheter</h2><p>Sur un semi-rigide d’occasion, commencez par les flotteurs (matériau, âge, coutures et tenue de la pression), puis le moteur (heures, factures et démarrage à froid), le tableau arrière, les papiers et, s’il y en a une, la remorque. Tout est détaillé dans le guide pour <a href="/fr/guias/%s/">acheter un semi-rigide d’occasion</a>.</p>' % G,
}
for pre, new in L.items():
    f = pre + 'comprar/semirrigidas-neumaticas-segunda-mano.html'; s = open(f, encoding='utf-8').read()
    if 'id="s2"' not in s: continue
    s, n = re.subn(r'<h2 id="s1">.*?(?=<h2 id="s3">)', new + '\n', s, count=1, flags=re.S)
    assert n == 1, f
    open(f, 'w', encoding='utf-8').write(s)
print('ok')
