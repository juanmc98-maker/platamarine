# -*- coding: utf-8 -*-
"""Enlaza las guías /guias/barcos-6-metros-con-camarote/ e /guias/impuestos-gastos-comprar-barco/
desde el índice de guías (tarjetas) y el sitemap, en ES/CA/EN/FR. Idempotente."""
import re
IMG = {'barcos-6-metros-con-camarote': '/rio-550-cruiser-1-m.jpg', 'impuestos-gastos-comprar-barco': '/hero-poster.jpg'}
L = {
 'es': dict(p='', more='Leer la guía →', cards={
   'barcos-6-metros-con-camarote': ('Compra', 'Barcos de 6 metros con camarote: qué esperar y qué mirar', 'Qué da de sí el camarote, qué titulación necesitas, por qué la eslora exacta importa y qué revisar antes de comprar.'),
   'impuestos-gastos-comprar-barco': ('Fiscalidad', 'Impuestos y gastos al comprar un barco: qué se paga en cada caso', 'IVA, ITP, impuesto de matriculación y papeles, según a quién compres el barco, si es nuevo o usado y cuánto mide.')}),
 'ca': dict(p='/ca', more='Llegir la guia →', cards={
   'barcos-6-metros-con-camarote': ('Compra', 'Vaixells de 6 metres amb cabina: què esperar i què mirar', 'Què dona de si la cabina, quina titulació necessites, per què l’eslora exacta importa i què revisar abans de comprar.'),
   'impuestos-gastos-comprar-barco': ('Fiscalitat', 'Impostos i despeses en comprar un vaixell: què es paga en cada cas', 'IVA, ITP, impost de matriculació i papers, segons a qui compris el vaixell, si és nou o de segona mà i quant fa.')}),
 'en': dict(p='/en', more='Read the guide →', cards={
   'barcos-6-metros-con-camarote': ('Buying', '6-metre boats with a cabin: what to expect and what to check', 'What the cabin gives you, which licence you need, why the exact length matters and what to check before you buy.'),
   'impuestos-gastos-comprar-barco': ('Tax', 'Taxes and costs when buying a boat in Spain', 'VAT, ITP, registration tax and paperwork, depending on who you buy from, whether the boat is new or used and its length.')}),
 'fr': dict(p='/fr', more='Lire le guide →', cards={
   'barcos-6-metros-con-camarote': ('Achat', 'Bateaux de 6 mètres avec cabine : à quoi s’attendre', 'Ce que permet la cabine, le permis qu’il faut, pourquoi la longueur exacte compte et que vérifier avant d’acheter.'),
   'impuestos-gastos-comprar-barco': ('Fiscalité', 'Acheter un bateau d’occasion en Espagne : taxes et frais à prévoir', 'ITP, TVA, taxe d’immatriculation et papiers, selon le vendeur, l’âge du bateau et sa longueur.')}),
}
for lang, d in L.items():
    pre = d['p'].lstrip('/') + '/' if d['p'] else ''
    f = pre + 'guias/index.html'; s = open(f, encoding='utf-8').read()
    for S, (t, h, p) in d['cards'].items():
        if f'href="{S}/"' in s: continue
        card = f'<li><a href="{S}/"><img src="{IMG[S]}" alt="" loading="lazy"><span class="g-body"><span class="tag">{t}</span><h2>{h}</h2><p>{p}</p><span class="g-more">{d["more"]}</span></span></a></li>'
        s, n = re.subn(r'(<li><a href="semirrigidas-deportivas-lujo/">)', lambda m: card + m.group(1), s, count=1)
        assert n == 1, f
    open(f, 'w', encoding='utf-8').write(s)
f = 'sitemap.xml'; s = open(f, encoding='utf-8').read()
for lang, d in L.items():
    for S in reversed(list(d['cards'])):
        url = f"https://www.platamarine.com{d['p']}/guias/{S}/"
        if url in s: continue
        old = f"https://www.platamarine.com{d['p']}/guias/comprar-semirrigida-segunda-mano/"
        i = s.index(old); j = s.index('</url>', i) + len('</url>')
        pr = '0.7' if lang == 'es' else '0.6'
        s = s[:j] + f"\n    <url><loc>{url}</loc><lastmod>2026-10-29</lastmod><priority>{pr}</priority></url>" + s[j:]
open(f, 'w', encoding='utf-8').write(s)
print('ok')
