# -*- coding: utf-8 -*-
# OBSOLETO tras los ajustes del 3 nov 2026 (44 px, 16 px, <375 px, buscador de texto bajo el hero en móvil): los cambios ya están en las portadas; no relanzar.
"""Portada (ES/CA/EN/FR): buscador rápido en móvil (tipo + precio) dentro del primer bloque.
En móvil sustituye al botón "Ver barcos en venta" y oculta el bloque de filtros de debajo (duplicado).
Escritorio sin cambios. Idempotente. Uso: python3 _tools/hero_quick_movil.py (desde la raíz)."""
L = {
 'index.html':    dict(t='Tipo de barco', p='Precio máximo', ta='Motor o vela', pa='Cualquier precio', b='Ver barcos',
                       tipos=[('all','Tipo'),('motor','Motor'),('vela','Vela')],
                       prec=[('all','Precio'),('0-30000','Hasta 30.000 €'),('30000-60000','30.000 – 60.000 €'),('60000-100000','60.000 – 100.000 €'),('100000-','Más de 100.000 €')]),
 'ca/index.html': dict(t='Tipus de vaixell', p='Preu màxim', b='Veure vaixells',
                       tipos=[('all','Tipo'),('motor','Motor'),('vela','Vela')],
                       prec=[('all','Preu'),('0-30000','Fins a 30.000 €'),('30000-60000','30.000 – 60.000 €'),('60000-100000','60.000 – 100.000 €'),('100000-','Més de 100.000 €')]),
 'en/index.html': dict(t='Boat type', p='Price', b='See boats',
                       tipos=[('all','Type'),('motor','Motor'),('vela','Sail')],
                       prec=[('all','Price'),('0-30000','Up to €30,000'),('30000-60000','€30,000 – €60,000'),('60000-100000','€60,000 – €100,000'),('100000-','Over €100,000')]),
 'fr/index.html': dict(t='Type de bateau', p='Prix', b='Voir',
                       tipos=[('all','Type'),('motor','Moteur'),('vela','Voile')],
                       prec=[('all','Prix'),('0-30000','Jusqu’à 30 000 €'),('30000-60000','30 000 € – 60 000 €'),('60000-100000','60 000 € – 100 000 €'),('100000-','Plus de 100 000 €')]),
}
CSS = ('<style>.hero-quick{display:none}@media (max-width:640px){'
       '.hero-quick{pointer-events:auto;display:flex;align-items:stretch;gap:6px;width:100%;max-width:360px;margin:14px auto 0;padding:5px;background:#fff;border-radius:14px;box-shadow:0 6px 24px rgba(0,0,0,.25)}'
       '.hero-quick select{flex:1 1 0;min-width:0;min-height:44px;font:inherit;font-family:var(--display);font-size:15px;color:#0D1C27;padding:11px 6px;border:1px solid rgba(127,146,158,.45);border-radius:10px;background:#fff}'
       '.hero-quick button{flex:none;min-height:44px;font-family:var(--display);font-weight:600;font-size:15px;padding:0 14px;border:0;border-radius:10px;background:var(--wa,#0B766B);color:#fff;cursor:pointer}'
       '.hero-quick select:focus-visible,.hero-quick button:focus-visible{outline:2px solid #0E3042;outline-offset:2px}'
       '.hero-btns .btn.ghost{display:none}.pmfind{display:none}}</style>')
JS = ('<script>/* Buscador rápido de portada en móvil: tipo + precio, al catálogo */(function(){var f=document.getElementById("pmQuick");if(!f)return;'
      'f.addEventListener("submit",function(e){e.preventDefault();var p=new URLSearchParams();["tipo","precio"].forEach(function(k){var v=f.elements[k].value;if(v&&v!=="all")p.set(k,v);});'
      'var q=p.toString();try{if(window.pmCount)window.pmCount({t:"buscador_portada_movil",m:q||"todo"});}catch(x){}location.href=f.getAttribute("action")+(q?"?"+q:"");});})();</script>')
MARK = '<form class="hero-quick"'
for path, d in L.items():
    h = open(path, encoding='utf-8').read()
    if MARK in h:
        print('ya estaba', path); continue
    anchor = '<form class="hero-search"'
    assert h.count(anchor) == 1, path
    opts = lambda xs: ''.join('<option value="%s">%s</option>' % x for x in xs)
    form = (CSS + MARK + ' id="pmQuick" action="barcos/" role="search">'
            '<select name="tipo" aria-label="%s">%s</select>'
            '<select name="precio" aria-label="%s">%s</select>'
            '<button type="submit">%s</button></form>' % (d['t'], opts(d['tipos']), d['p'], opts(d['prec']), d['b']) + JS)
    # justo después de los botones del hero, antes del buscador de texto
    i = h.index(anchor)
    j = h.rfind('<style>.hero-search', 0, i)
    pos = j if j != -1 and i - j < 3000 else i
    h = h[:pos] + form + h[pos:]
    open(path, 'w', encoding='utf-8').write(h)
    print('ok', path)
