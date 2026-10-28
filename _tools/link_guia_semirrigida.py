# -*- coding: utf-8 -*-
"""Enlaza la guía /guias/comprar-semirrigida-segunda-mano/ desde la página de compra de semirrígidas,
el índice de guías (tarjeta) y el sitemap, en ES/CA/EN/FR. Idempotente."""
import re
S = 'comprar-semirrigida-segunda-mano'
L = {
 'es': dict(p='', more='<p>Lo explico con más detalle, con los precios de las que tengo, en la guía para <a href="/guias/%s/">comprar una semirrígida de segunda mano</a>.</p>' % S,
   rel='<a href="/guias/%s/">Comprar una semirrígida de segunda mano</a>' % S,
   card=('Comprar','Semirrígida de segunda mano: qué revisar antes de comprar','Flotadores, motor y horas, casco, papeles y remolque, con los precios de las semirrígidas que tengo en venta.','Leer la guía →')),
 'ca': dict(p='/ca', more='<p>Ho explico amb més detall, amb els preus de les que tinc, a la guia per <a href="/ca/guias/%s/">comprar una semirígida de segona mà</a>.</p>' % S,
   rel='<a href="/ca/guias/%s/">Comprar una semirígida de segona mà</a>' % S,
   card=('Comprar','Semirígida de segona mà: què revisar abans de comprar','Flotadors, motor i hores, casc, papers i remolc, amb els preus de les semirígides que tinc en venda.','Llegir la guia →')),
 'en': dict(p='/en', more='<p>I go into more detail, with the prices of the ones I have, in the guide to <a href="/en/guias/%s/">buying a used RIB</a>.</p>' % S,
   rel='<a href="/en/guias/%s/">Buying a used RIB</a>' % S,
   card=('Buying','Buying a used RIB: what to check before you pay','Tubes, engine and hours, hull, paperwork and trailer, with the prices of the RIBs I have for sale.','Read the guide →')),
 'fr': dict(p='/fr', more='<p>Je l’explique plus en détail, avec les prix de ceux que j’ai, dans le guide pour <a href="/fr/guias/%s/">acheter un semi-rigide d’occasion</a>.</p>' % S,
   rel='<a href="/fr/guias/%s/">Acheter un semi-rigide d’occasion</a>' % S,
   card=('Achat et vente','Semi-rigide d’occasion : que vérifier avant de payer','Flotteurs, moteur et heures, coque, papiers et remorque, avec les prix des semi-rigides que j’ai en vente.','Lire le guide →')),
}
for lang, d in L.items():
    pre = d['p'].lstrip('/') + '/' if d['p'] else ''
    # 1) página de compra
    f = pre + 'comprar/semirrigidas-neumaticas-segunda-mano.html'; s = open(f, encoding='utf-8').read()
    if S not in s:
        s, n1 = re.subn(r'<p>[^<]*<a href="[^"]*que-mirar-comprar-barco-segunda-mano[^"]*">[^<]*</a>\.?</p>', d['more'], s, count=1)
        s, n2 = re.subn(r'(<div class="rel"><p class="eyebrow">[^<]*</p>)', lambda m: m.group(1) + d['rel'], s, count=1)
        assert n1 == 1 and n2 == 1, (f, n1, n2)
        open(f, 'w', encoding='utf-8').write(s)
    # 2) índice de guías
    f = pre + 'guias/index.html'; s = open(f, encoding='utf-8').read()
    if S not in s:
        t, h, p, m = d['card']
        card = f'<li><a href="{S}/"><img src="/tiger-marine-650-1-m.jpg" alt="" loading="lazy"><span class="g-body"><span class="tag">{t}</span><h2>{h}</h2><p>{p}</p><span class="g-more">{m}</span></span></a></li>'
        s, n = re.subn(r'(<li><a href="semirrigidas-deportivas-lujo/">)', card.replace('\\', '\\\\') + r'\1', s, count=1)
        assert n == 1, f
        open(f, 'w', encoding='utf-8').write(s)
# 3) sitemap
f = 'sitemap.xml'; s = open(f, encoding='utf-8').read()
for lang, d in L.items():
    url = f"https://www.platamarine.com{d['p']}/guias/{S}/"
    if url in s: continue
    old = f"https://www.platamarine.com{d['p']}/guias/semirrigidas-deportivas-lujo/"
    i = s.index(old); j = s.index('</url>', i) + len('</url>')
    pr = '0.7' if lang == 'es' else '0.6'
    s = s[:j] + f"\n    <url><loc>{url}</loc><lastmod>2026-10-28</lastmod><priority>{pr}</priority></url>" + s[j:]
open(f, 'w', encoding='utf-8').write(s)
print('ok')
