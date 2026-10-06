#!/usr/bin/env python3
"""Menú simplificado Plata Marine (oct 2026): Barcos en venta · Vender mi barco · Te busco barco · Recursos▾ · Sobre mí · Contacto.
Reescribe <nav class="nav pmx-nav"> y <nav class="pmx-panel"> en todas las páginas (ES/CA/EN/FR). Idempotente.
Uso: python3 bake_menu_simple.py <raiz_repo>"""
import os, re, sys, html
ROOT = sys.argv[1]
T = {
 '': dict(aria='Secciones', top=[('/barcos/','Barcos en venta'),('/vender-barco/','Vender mi barco'),('/#comprar','Te busco barco')], res='Recursos',
   cols=[('Vender',[('/herramientas/valora-tu-barco.html','¿Qué influye en el precio de mi barco?'),('/papeles-fiscalidad/','Papeles e impuestos'),('/guias/que-hace-un-broker-nautico.html','Qué hace un bróker náutico'),('ZONAS','Vender por zona'),('/vender/guia-fotos-barco.html','Cómo hacer las fotos de tu barco')]),
         ('Comprar',[('/alertas/','Avísame de barcos nuevos'),('/que-barco-necesito.html','¿Qué barco necesito?'),('/modelos/','Modelos: qué mirar y precios'),('/comprar/','Comprar barco: por zona y tipo'),('/precios/','Precios de barcos de ocasión'),('/herramientas/','Calculadoras: impuestos, costes, financiación')]),
         ('Aprende',[('/guias/','Guías'),('/actualidad/','Actualidad'),('/navegante/','Guía del navegante'),('/titulaciones/','Titulaciones')]),
         ('Servicios',[('/servicios/','ITB, gestoría, varadero y más'),('/servicios/directorio.html','Directorio de empresas'),('/servicios/escuelas.html','Escuelas náuticas'),('/servicios/amarres.html','Amarres')])],
   end=[('/#juan','Sobre mí'),('/#contacto','Contacto')]),
 '/ca': dict(aria='Seccions', top=[('/barcos/','Vaixells en venda'),('/vender-barco/','Vendre el meu vaixell'),('/#comprar','Et busco vaixell')], res='Recursos',
   cols=[('Vendre',[('/herramientas/valora-tu-barco.html','Què influeix en el preu del meu vaixell?'),('/papeles-fiscalidad/','Papers i impostos'),('/guias/que-hace-un-broker-nautico.html','Què fa un bròker nàutic'),('ZONAS','Vendre per zona'),('/vender/guia-fotos-barco.html','Com fer les fotos del teu vaixell')]),
         ('Comprar',[('/alertas/',"Avisa'm de vaixells nous"),('/que-barco-necesito.html','Quin vaixell necessito?'),('/modelos/','Models: què mirar i preus'),('/comprar/','Comprar vaixell: per zona i tipus'),('/precios/','Preus de vaixells d’ocasió'),('/herramientas/','Calculadores: impostos, costos, finançament')]),
         ('Aprèn',[('/guias/','Guies'),('/actualidad/','Actualitat'),('/navegante/','Guia del navegant'),('/titulaciones/','Titulacions')]),
         ('Serveis',[('/servicios/','ITB, gestoria, varador i més'),('/servicios/directorio.html',"Directori d'empreses"),('/servicios/escuelas.html','Escoles nàutiques'),('/servicios/amarres.html','Amarradors')])],
   end=[('/#juan','Sobre mi'),('/#contacto','Contacte')]),
 '/en': dict(aria='Sections', top=[('/barcos/','Boats for sale'),('/vender-barco/','Sell my boat'),('/#comprar','I’ll find you a boat')], res='Resources',
   cols=[('Selling',[('/herramientas/valora-tu-barco.html','What affects my boat’s price?'),('/papeles-fiscalidad/','Paperwork and taxes'),('/guias/que-hace-un-broker-nautico.html','What a boat broker does'),('ZONAS','Selling by area'),('/vender/guia-fotos-barco.html','How to photograph your boat')]),
         ('Buying',[('/alertas/','Tell me about new boats'),('/que-barco-necesito.html','Which boat do I need?'),('/modelos/','Models: what to check and prices'),('/comprar/','Buy a boat: by area and type'),('/precios/','Used boat prices'),('/herramientas/','Calculators: taxes, costs, finance')]),
         ('Learn',[('/guias/','Guides'),('/actualidad/','News'),('/navegante/',"Skipper's guide"),('/titulaciones/','Boating licences')]),
         ('Services',[('/servicios/','Inspection, paperwork, boatyard and more'),('/servicios/directorio.html','Company directory'),('/servicios/escuelas.html','Boating schools'),('/servicios/amarres.html','Moorings')])],
   end=[('/#juan','About me'),('/#contacto','Contact')]),
 '/fr': dict(aria='Rubriques', top=[('/barcos/','Bateaux à vendre'),('/vender-barco/','Vendre mon bateau'),('/#comprar','Je cherche votre bateau')], res='Ressources',
   cols=[('Vendre',[('/herramientas/valora-tu-barco.html','Qu’est-ce qui influe sur le prix de mon bateau ?'),('/papeles-fiscalidad/','Papiers et fiscalité'),('/guias/que-hace-un-broker-nautico.html','Ce que fait un courtier nautique'),('ZONAS','Vendre par zone'),('/vender/guia-fotos-barco.html','Comment photographier votre bateau')]),
         ('Acheter',[('/alertas/','Prévenez-moi des nouveaux bateaux'),('/que-barco-necesito.html','De quel bateau ai-je besoin ?'),('/modelos/','Modèles : points à vérifier et prix'),('/comprar/','Acheter un bateau : par zone et par type'),('/precios/','Prix des bateaux d’occasion'),('/herramientas/','Calculatrices : taxes, coûts, financement')]),
         ('Apprendre',[('/guias/','Guides'),('/actualidad/','Actualités'),('/navegante/','Guide du plaisancier'),('/titulaciones/','Permis bateau')]),
         ('Services',[('/servicios/','Expertise, papiers, chantier naval et plus'),('/servicios/directorio.html','Annuaire des entreprises'),('/servicios/escuelas.html','Écoles nautiques'),('/servicios/amarres.html','Places de port')])],
   end=[('/#juan','Qui suis-je'),('/#contacto','Contact')]),
}
def e(s): return html.escape(s, quote=True)
def cur(href, path): return ' aria-current="page"' if '#' not in href and (path == href or path == href + 'index.html') else ''
ZN = {'': ['Costa Brava','Barcelona y Maresme','Tarragona','Baleares'], '/ca': ['Costa Brava','Barcelona i Maresme','Tarragona','Balears'],
      '/en': ['Costa Brava','Barcelona & Maresme','Tarragona','Balearics'], '/fr': ['Costa Brava','Barcelone et Maresme','Tarragone','Baléares']}
ZS = ['broker-nautico-costa-brava.html','broker-nautico-barcelona-maresme.html','broker-nautico-tarragona-costa-daurada.html','broker-nautico-baleares.html']
def zonas(pre, label, path):
    ls = ''.join(f'<a href="{pre}/vender/{s}"{cur(pre + "/vender/" + s, path)}>{e(n)}</a>' for s, n in zip(ZS, ZN[pre]))
    return f'<div class="pmx-zonas"><span>{e(label)}</span>{ls}</div>'
def build(pre, path):
    c = T[pre]; P = lambda h: pre + h
    a = lambda h, t: zonas(pre, t, path) if h == 'ZONAS' else f'<a href="{P(h)}"{cur(P(h), path)}>{e(t)}</a>'
    res_cur = any(cur(P(h), path) for _, its in c['cols'] for h, _ in its if h != 'ZONAS') or '/vender/broker-nautico-' in path
    cols = ''.join(f'<div class="pmx-col" id="pmxM{i+1}"><p>{e(n)}</p>' + ''.join(a(h, t) for h, t in its) + '</div>' for i, (n, its) in enumerate(c['cols']))
    nav = (f'<nav class="nav pmx-nav" aria-label="{c["aria"]}">\n      ' + '\n      '.join(a(h, t) for h, t in c['top']) +
           f'\n      <div class="pmx-dd pmx-res{" cur" if res_cur else ""}"><button type="button" aria-expanded="false" aria-controls="pmxRes">{e(c["res"])}</button><div class="pmx-menu pmx-mega" id="pmxRes">{cols}</div></div>\n      ' +
           '\n      '.join(a(h, t) for h, t in c['end']) + '\n    </nav>')
    grp = ''.join(f'<div class="pmx-grp pmx-sub"><p>{e(n)}</p>' + ''.join(a(h, t) for h, t in its) + '</div>' for n, its in c['cols'])
    panel_in = ('<div class="pmx-grp pmx-main">' + ''.join(a(h, t) for h, t in c['top']) + '</div>\n      '
                f'<div class="pmx-reshead"><p>{e(c["res"])}</p></div>\n      ' + grp + '\n      '
                '<div class="pmx-grp pmx-main">' + ''.join(a(h, t) for h, t in c['end']) + '</div>')
    return nav, panel_in
NAV = re.compile(r'<nav class="nav pmx-nav"[^>]*>.*?</nav>', re.S)
PIN = re.compile(r'(<nav class="pmx-panel" id="pmxPanel"[^>]*>\s*<div class="pmx-in">\s*)(.*?)(\s*<div class="pmx-wide">)', re.S)
n = 0; skipped = []
for d, _, fs in os.walk(ROOT):
    if '/.git' in d or '/_tools' in d: continue
    for f in fs:
        if not f.endswith('.html'): continue
        fp = os.path.join(d, f); rel = '/' + os.path.relpath(fp, ROOT).replace(os.sep, '/')
        t = open(fp, encoding='utf-8').read()
        if not NAV.search(t): skipped.append(rel); continue
        pre = next((p for p in ('/ca', '/en', '/fr') if rel.startswith(p + '/')), '')
        nav, pin = build(pre, rel)
        t2 = NAV.sub(lambda m: nav, t, count=1)
        t2 = PIN.sub(lambda m: m.group(1) + pin + m.group(3), t2, count=1)
        if t2 != t: open(fp, 'w', encoding='utf-8').write(t2); n += 1
print('páginas cambiadas:', n); print('sin menú:', len(skipped), skipped[:20])
