# -*- coding: utf-8 -*-
"""Servicios (ES/CA/EN/FR): el selector "¿Qué necesitas?" pasa a un recorrido en tres etapas
(antes de comprar, mientras navegas, cuando vendes). No quita ninguna sección. Idempotente.
Uso: python3 _tools/servicios_etapas.py (desde la raíz)."""
import re
CSS = ('<style>.svc-steps{display:grid;grid-template-columns:minmax(0,1fr);gap:12px;margin:0 0 30px}'
 '.svc-step{background:#fff;border:1px solid var(--line,#DDE3E7);border-radius:12px;padding:18px 18px 16px;min-width:0}'
 '.svc-step .n{font-family:var(--display);font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2);margin:0 0 4px}'
 '.svc-step h2.st{font-size:20px;margin:0 0 4px;line-height:1.25}.svc-step p.d{font-size:15px;margin:0 0 12px;color:var(--ink-2)}'
 '.svc-step ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}.svc-step li{margin:0;padding:0}.svc-step li::before{content:none}'
 '.svc-step a{display:inline-flex;align-items:center;gap:8px;min-height:44px;font-family:var(--display);font-size:15px;font-weight:600;color:var(--sea);text-decoration:none;border:1px solid var(--plata,#B7C3CB);background:#fff;border-radius:10px;padding:8px 12px}'
 '.svc-step a::after{content:"\\203A";font-size:20px;line-height:1;opacity:.6}'
 '.svc-step a:hover,.svc-step a:focus-visible{border-color:var(--sea);background:var(--sea);color:#fff}'
 '.svc-step a.go{background:var(--wa,#0B766B);border-color:var(--wa,#0B766B);color:#fff}.svc-step a.go:hover,.svc-step a.go:focus-visible{background:#085C53;border-color:#085C53}'
 '@media (max-width:560px){.svc-step ul{flex-direction:column}.svc-step a{display:flex;justify-content:space-between}}</style>')
T = {
'': dict(aria='Servicios según en qué punto estás', s=[
  ('Paso 1','Al comprar tu barco','Revisa el barco, comprueba la documentación y organiza los trámites de compra.',
   [('../guias/que-mirar-comprar-barco-segunda-mano','Qué mirar antes de comprar'),('cambio-titularidad-barco','Cambio de titularidad'),('#transporte','Transporte del barco'),('#seguro','Seguro')]),
  ('Paso 2','Mientras navegas','Mantén tu barco al día: revisiones, mantenimiento y trámites.',
   [('#itb','ITB'),('#varadero','Varadero y taller'),('#limpieza','Limpieza y mantenimiento'),('#gestoria','Gestoría náutica')]),
  ('Paso 3','Cuando decides vender','Descubre cuánto vale, prepáralo para enseñarlo y ten la documentación lista.',
   [('../cuanto-vale-mi-barco/','¿Cuánto vale mi barco?'),('../navegante/preparar-barco-fin-de-temporada','Prepararlo para enseñarlo'),('../vender/guia-fotos-barco','Cómo hacer las fotos'),('../guias/papeles-vender-barco-cambio-titularidad','Documentación para vender'),('../vender-barco/#valora','Quiero vender mi barco','go')])]),
'ca/': dict(aria='Serveis segons en quin punt ets', s=[
  ('Pas 1','En comprar el teu vaixell','Revisa el vaixell, comprova la documentació i organitza els tràmits de compra.',
   [('../guias/que-mirar-comprar-barco-segunda-mano','Què mirar abans de comprar'),('cambio-titularidad-barco','Canvi de titularitat'),('#transporte','Transport del vaixell'),('#seguro','Assegurança')]),
  ('Pas 2','Mentre navegues','Tingues el vaixell al dia: revisions, manteniment i tràmits.',
   [('#itb','ITB'),('#varadero','Varador i taller'),('#limpieza','Neteja i manteniment'),('#gestoria','Gestoria nàutica')]),
  ('Pas 3','Quan decideixes vendre','Descobreix quant val, prepara’l per ensenyar-lo i tingues la documentació a punt.',
   [('../cuanto-vale-mi-barco/','Quant val el meu vaixell?'),('../navegante/preparar-barco-fin-de-temporada','Preparar-lo per ensenyar-lo'),('../vender/guia-fotos-barco','Com fer les fotos'),('../guias/papeles-vender-barco-cambio-titularidad','Documentació per vendre'),('../vender-barco/#valora','Vull vendre el meu vaixell','go')])]),
'en/': dict(aria='Services by stage', s=[
  ('Step 1','When you buy your boat','Check the boat, verify the paperwork and arrange the purchase formalities.',
   [('../guias/que-mirar-comprar-barco-segunda-mano','What to check before buying'),('cambio-titularidad-barco','Change of ownership'),('#transporte','Boat transport'),('#seguro','Insurance')]),
  ('Step 2','While you own it','Keep your boat up to date: inspections, maintenance and paperwork.',
   [('#itb','Inspection (ITB)'),('#varadero','Boatyard and workshop'),('#limpieza','Cleaning and maintenance'),('#gestoria','Paperwork')]),
  ('Step 3','When you decide to sell','Find out what it is worth, get it ready for viewings and have the paperwork ready.',
   [('../cuanto-vale-mi-barco/','What is my boat worth?'),('../navegante/preparar-barco-fin-de-temporada','Get it ready for viewings'),('../vender/guia-fotos-barco','How to take the photos'),('../guias/papeles-vender-barco-cambio-titularidad','Paperwork to sell'),('../vender-barco/#valora','I want to sell my boat','go')])]),
'fr/': dict(aria='Services selon votre étape', s=[
  ('Étape 1','À l’achat de votre bateau','Inspectez le bateau, vérifiez les papiers et organisez les formalités d’achat.',
   [('../guias/que-mirar-comprar-barco-segunda-mano','Ce qu’il faut vérifier avant d’acheter'),('cambio-titularidad-barco','Changement de propriétaire'),('#transporte','Transport du bateau'),('#seguro','Assurance')]),
  ('Étape 2','Pendant que vous naviguez','Gardez votre bateau à jour : contrôles, entretien et formalités.',
   [('#itb','Inspection (ITB)'),('#varadero','Chantier et atelier'),('#limpieza','Nettoyage et entretien'),('#gestoria','Formalités')]),
  ('Étape 3','Quand vous décidez de vendre','Découvrez ce qu’il vaut, préparez-le pour les visites et ayez les papiers prêts.',
   [('../cuanto-vale-mi-barco/','Combien vaut mon bateau ?'),('../navegante/preparar-barco-fin-de-temporada','Le préparer pour les visites'),('../vender/guia-fotos-barco','Comment faire les photos'),('../guias/papeles-vender-barco-cambio-titularidad','Papiers pour vendre'),('../vender-barco/#valora','Je veux vendre mon bateau','go')])]),
}
for l, d in T.items():
    path = l + 'servicios/index.html'
    h = open(path, encoding='utf-8').read()
    if 'class="svc-steps"' in h:
        print('ya estaba', path); continue
    cards = ''
    for n, t, desc, links in d['s']:
        lis = ''.join('<li><a href="%s"%s>%s</a></li>' % (x[0], ' class="go"' if len(x) > 2 else '', x[1]) for x in links)
        cards += '<section class="svc-step"><p class="n">%s</p><h2 class="st">%s</h2><p class="d">%s</p><ul>%s</ul></section>' % (n, t, desc, lis)
    new = CSS + '<nav class="svc-steps" aria-label="%s">%s</nav>' % (d['aria'], cards)
    h2, k = re.subn(r'<nav class="svc-pick".*?</nav>', lambda m: new, h, count=1, flags=re.S)
    assert k == 1, path
    open(path, 'w', encoding='utf-8').write(h2)
    print('ok', path)
