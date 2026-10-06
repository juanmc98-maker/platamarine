# -*- coding: utf-8 -*-
"""Revisión UX del catálogo /barcos/ (6 oct 2026), ES/CA/EN/FR. Idempotente.
- Introducción de una frase; los enlaces por zona/tipo/modelo y el aviso para vendedores pasan debajo del listado.
- Combustible y motor bajo "Más filtros" (tipo, titulación, precio, zona y orden siguen visibles).
- Descripción de las tarjetas limitada a 3 líneas (el texto completo sigue en el HTML y en la ficha)."""
import re, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
INTRO = {
 'es': 'Los barcos que gestiono ahora, con el precio a la vista y el encargo firmado por su propietario. ¿No está el tuyo? <a href="../alertas/">Crea una alerta</a>.',
 'ca': 'Els vaixells que gestiono ara, amb el preu a la vista i l\'encàrrec signat pel propietari. No hi és el teu? <a href="../alertas/">Crea una alerta</a>.',
 'en': 'The boats I am handling now, with the price shown and a sale mandate signed by the owner. Not seeing yours? <a href="../alertas/">Create an alert</a>.',
 'fr': 'Les bateaux que je vends actuellement, avec le prix affiché et un mandat signé par le propriétaire. Vous ne trouvez pas le vôtre ? <a href="../alertas/">Créez une alerte</a>.',
}
MORE = {'es': 'Más filtros', 'ca': 'Més filtres', 'en': 'More filters', 'fr': 'Plus de filtres'}
def links(l):
    p = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}[l]
    T = {
     'es': ('Por zona', ['Cataluña', 'Costa Brava', 'Baleares'], 'Por tipo', ['Lanchas a motor', 'Veleros', 'Semirrígidas', 'Barcos de 6 metros con camarote', 'Llaüts', 'Con Licencia o PNB'], 'Por modelo', ['Merry Fisher 795', 'Cap Camarat 7.5 WA', 'Cap Camarat 8.5 WA', 'todos los modelos'], '¿Cuánto cuesta un barco?', '¿Vendes un barco?', 'Mira qué influye en su precio (2 min)'),
     'ca': ('Per zona', ['Catalunya', 'Costa Brava', 'Balears'], 'Per tipus', ['Llanxes a motor', 'Velers', 'Semirígides', 'Vaixells de 6 metres amb cabina', 'Llaüts', 'Amb Llicència o PNB'], 'Per model', ['Merry Fisher 795', 'Cap Camarat 7.5 WA', 'Cap Camarat 8.5 WA', 'tots els models'], 'Quant costa un vaixell?', 'Vens un vaixell?', 'Mira què influeix en el preu (2 min)'),
     'en': ('By area', ['Catalonia', 'Costa Brava', 'Balearic Islands'], 'By type', ['Motorboats', 'Sailboats', 'RIBs', '6-metre boats with a cabin', 'Llaüts', 'With Licencia or PNB'], 'By model', ['Merry Fisher 795', 'Cap Camarat 7.5 WA', 'Cap Camarat 8.5 WA', 'all models'], 'How much does a boat cost?', 'Selling a boat?', 'See what affects its price (2 min)'),
     'fr': ('Par zone', ['Catalogne', 'Costa Brava', 'Baléares'], 'Par type', ['Bateaux à moteur', 'Voiliers', 'Semi-rigides', 'Bateaux de 6 mètres avec cabine', 'Llaüts', 'Avec Licencia ou PNB'], 'Par modèle', ['Merry Fisher 795', 'Cap Camarat 7.5 WA', 'Cap Camarat 8.5 WA', 'tous les modèles'], 'Combien coûte un bateau ?', 'Vous vendez un bateau ?', 'Voyez ce qui influe sur son prix (2 min)'),
    }[l]
    z = ['barcos-segunda-mano-cataluna', 'barcos-segunda-mano-costa-brava', 'barcos-segunda-mano-baleares']
    t = ['lanchas-motor-segunda-mano', 'veleros-segunda-mano', 'semirrigidas-neumaticas-segunda-mano', 'barcos-6-metros-con-camarote-segunda-mano', 'llauts-segunda-mano', 'barcos-licencia-navegacion-pnb']
    m = ['/modelos/jeanneau-merry-fisher-795.html', '/modelos/jeanneau-cap-camarat-7-5-wa.html', '/modelos/jeanneau-cap-camarat-8-5-wa.html', '/modelos/']
    a = lambda h, x: '<a href="%s">%s</a>' % (h, x)
    return ('<div class="bmorel"><p><strong>%s:</strong> %s</p><p><strong>%s:</strong> %s</p><p><strong>%s:</strong> %s · %s</p><p>%s %s</p></div>' % (
        T[0], ' · '.join(a('%s/comprar/%s.html' % (p, s), n) for s, n in zip(z, T[1])),
        T[2], ' · '.join(a('%s/comprar/%s.html' % (p, s), n) for s, n in zip(t, T[3])),
        T[4], ' · '.join(a(p + h, n) for h, n in zip(m, T[5])), a('%s/comprar/cuanto-cuesta-un-barco.html' % p, T[6]),
        T[7], a('%s/herramientas/valora-tu-barco.html' % p, T[8])))
CSS = '<style id="ux-oct">.bmore{display:flex;flex-wrap:wrap;gap:14px 22px;align-items:flex-end}.bmore>summary{align-self:flex-end;cursor:pointer;font-size:.9rem;font-weight:600;color:var(--sea);padding:8px 2px;list-style:none;text-decoration:underline;text-underline-offset:3px}.bmore>summary::-webkit-details-marker{display:none}.bmore[open]>summary{display:none}.bdesc{display:-webkit-box;-webkit-line-clamp:3;line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}.bmorel{margin-top:40px;max-width:80ch;color:var(--ink-2);font-size:.95em;line-height:1.6}.bmorel p{margin:0 0 6px}</style>'
JS = '<script id="ux-oct-js">(function(){var d=document.querySelector(".bmore");if(!d)return;function chk(){var c=document.getElementById("f-comb"),m=document.getElementById("f-mot");if((c&&c.value!=="all")||(m&&m.value!=="all"))d.open=true;}chk();window.addEventListener("pageshow",chk);})();</script>'

def run(l):
    f = os.path.join(ROOT, (l + '/' if l != 'es' else '') + 'barcos/index.html')
    s = open(f, encoding='utf-8').read(); o = s
    if 'id="ux-oct"' in s:
        return f, 'ya aplicado'
    s = re.sub(r'<p style="max-width:62ch;color:var\(--ink-2\)">.*?</p>', lambda m: '<p style="max-width:62ch;color:var(--ink-2)">%s</p>' % INTRO[l], s, count=1, flags=re.S)
    s = re.sub(r'\s*<p style="max-width:62ch;color:var\(--ink-2\);margin-top:8px;font-size:\.95em">.*?</p>', '', s, count=1, flags=re.S)
    s = re.sub(r'(<fieldset><label for="f-comb">.*?</fieldset>\s*<fieldset><label for="f-mot">.*?</fieldset>)',
               lambda m: '<details class="bmore"><summary>%s</summary>%s</details>' % (MORE[l], m.group(1)), s, count=1, flags=re.S)
    s = s.replace('    <div class="sell">', '    ' + links(l) + '\n    <div class="sell">', 1)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = s.replace('</body>', JS + '\n</body>', 1)
    open(f, 'w', encoding='utf-8').write(s)
    return f, len(o), len(s), s.count('class="bmore"'), s.count('class="bmorel"')

if __name__ == '__main__':
    for l in ['es', 'ca', 'en', 'fr']:
        print(run(l))
