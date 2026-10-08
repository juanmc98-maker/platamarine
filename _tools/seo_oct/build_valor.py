# -*- coding: utf-8 -*-
"""#1 /cuanto-vale-mi-barco/ + #3 guías valor fiscal y tasación (ES/CA/EN/FR). Uso: python3 _tools/seo_oct/build_valor.py
Después: python3 _tools/bake_menu_simple.py (si toca) y python3 _tools/build_search_index.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pagebuild as pb, content_cuanto_vale as cv, content_guias_valor as gv
pg, cr = cv.pages()
pb.build('cuanto-vale-mi-barco/', pg, cr, ld_type='WebApplication', extra_head=cv.CSS, extra_foot='<script src="/cuanto-vale-mi-barco/calc.js?v=20261007" defer></script>')
pg, cr = gv.pages(gv.VF); pb.build('guias/valor-fiscal-barco-tablas-hacienda.html', pg, cr)
pg, cr = gv.pages(gv.TS); pb.build('guias/tasacion-barco.html', pg, cr)
pb.sitemap(['cuanto-vale-mi-barco/', 'guias/valor-fiscal-barco-tablas-hacienda.html', 'guias/tasacion-barco.html'])
