# -*- coding: utf-8 -*-
"""Guía ITP (FR): mismas correcciones que la versión ES del 3 nov 2026 + fecha y fuentes."""
import re
f='fr/guias/itp-comprar-barco-usado-por-comunidad.html'
h=open(f,encoding='utf-8').read()
R=[
 ('et quand le bateau est neuf ou arrive de l’étranger sans être immatriculé, ce qui fait alors intervenir la <a href="/fr/guias/impuesto-matriculacion-barcos">taxe d’immatriculation</a>.',
  'et quand le bateau est neuf : l’achat est alors soumis à la TVA et, si le bateau mesure plus de 8 m, à la <a href="/fr/guias/impuesto-matriculacion-barcos">taxe d’immatriculation</a>.',1),
 ('<td>Cantabrie</td><td style="white-space:nowrap">4 % / 8 %</td><td>8 % si le bateau mesure plus de 8 m</td>',
  '<td>Cantabrie</td><td style="white-space:nowrap">8 %</td><td>Taux général pour les biens meubles, sans distinction de longueur</td>',1),
 ('<td>Castille-La Manche</td><td>6 %</td><td></td>','<td>Castille-La Manche</td><td>6 %</td><td>À confirmer auprès de son administration fiscale</td>',1),
 ('<td>Communauté valencienne</td><td>6 %/8 %</td><td>8 % au-delà de 8 m de long ou d’une valeur supérieure à 20 000 €</td>',
  '<td>Communauté valencienne</td><td>6 %/8 %</td><td>8 % au-delà de 8 m de long ou à partir de 20 000 € de valeur</td>',1),
 ('<td>Estrémadure</td><td>6 %</td><td></td>','<td>Estrémadure</td><td>6 %</td><td>À confirmer auprès de son administration fiscale</td>',1),
 ('<td>Navarre</td><td>4 %</td><td>Régime fiscal propre (foral)</td>','<td>Navarre</td><td>4 %</td><td>Régime fiscal propre (foral) ; à confirmer auprès de la Hacienda Foral</td>',1),
 ('<td>Pays basque</td><td>4 %</td><td>Régime propre (foral) (Álava, Bizkaia, Gipuzkoa)</td>','<td>Pays basque</td><td>4 %</td><td>Régime propre (foral) (Álava, Bizkaia, Gipuzkoa) ; à confirmer auprès de votre diputación</td>',1),
 ('<td>Ceuta et Melilla</td><td>2 %</td><td>Résidents</td>','<td>Ceuta et Melilla</td><td>2 %</td><td>Résidents ; à confirmer auprès de l’Agencia Tributaria</td>',1),
 ('Le même bateau à 7,99 m paierait 6 % : 3 600 €.','Le même bateau à 7,99 m paierait aussi 8 %, car il vaut plus de 20 000 € : il suffit de remplir l’une des deux conditions.',1),
 ('en général 30 jours ouvrables à compter de la signature ; en Catalogne, c’est un mois, et en Andalousie, deux mois.',
  'en général 30 jours ouvrables à compter de la signature ; en Catalogne et aux Baléares, c’est un mois, et en Andalousie, deux mois.',1),
 ('En Andalousie, dans les Asturies, en Cantabrie et dans la Communauté valencienne, le taux monte à 8 % au-delà de cette longueur, et à Valence également selon la valeur.',
  'En Andalousie, dans les Asturies et dans la Communauté valencienne, le taux monte à 8 % au-delà de 8 m de long, et à Valence également si le bateau vaut 20 000 € ou plus.',1),
 ('la vente est soumise à 21 % de TVA et non à l’ITP. Demandez une facture.',
  'la vente est soumise à la TVA et non à l’ITP. Si le vendeur applique le régime des biens d’occasion (REBU), la TVA est comprise dans le prix et n’apparaît pas séparément. Demandez une facture.',None),
 ('(de 1 % par mois jusqu’à 15 %, plus des intérêts au-delà d’un an)',
  '(1 %, plus 1 % par mois complet de retard pendant la première année ; au-delà de 12 mois, 15 % plus des intérêts de retard)',None),
 ('<span>Mis à jour en septembre 2026</span>','<span>Vérifié le 3 novembre 2026</span>',1),
 ('Information fiscale indicative, révisée en septembre 2026 au regard du','Information fiscale indicative, vérifiée le 3 novembre 2026 au regard du',1),
]
for a,b,n in R:
    c=h.count(a)
    assert c>=1 and (n is None or c==n),(a[:50],c)
    h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Sources officielles</strong> (vérifiées le 3 novembre 2026) :</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/no-residentes/impuesto-sobre-transmisiones-patrimoniales-actos-documentados/vehiculos-embarcaciones-recreo-aeronaves-usados620.html" target="_blank" rel="noopener">Agencia Tributaria : formulaire 620, bateaux d’occasion</a></li>'
 '<li><a href="https://tramits.gencat.cat/ca/tramits/tramits-temes/ITPAJD-Transmissions-patrimonials-oneroses" target="_blank" rel="noopener">Generalitat de Catalunya : ITP, délai et déclaration</a></li>'
 '<li><a href="https://atc.gencat.cat/web/.content/documents/02_doc_tributs/01_itpajd/guia_itp.pdf" target="_blank" rel="noopener">Agència Tributària de Catalunya : guide de l’ITP</a></li>'
 '<li><a href="https://www.atib.es/ta/contenido.aspx?Id=5347&amp;lang=es" target="_blank" rel="noopener">ATIB (Baléares) : délai et formulaires</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-1998-8202" target="_blank" rel="noopener">BOE : loi 13/1997 de la Communauté valencienne (taux de 8 %)</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE : Orden HAC/1501/2025, prix moyens des bateaux 2026</a></li>'
 '</ul></div>')
a='Vérifiez auprès de votre conseiller fiscal ou de l’administration fiscale avant d’acheter.</p>'
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
