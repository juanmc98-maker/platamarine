"""Ficha v2 (hero, índice lateral, puntos sobre la foto, bloques, ficha oscura, cierre).
Primera aplicación: prestige-32 en ES/CA/EN/FR. Transforma la ficha generada sin tocar
cabecera, datos estructurados, PDF, similares ni scripts existentes.
Uso: python3 _tools/ficha_v2.py   (idempotente: si la ficha ya es v2 no hace nada)"""
import re, pathlib, html as H
ROOT = pathlib.Path(__file__).resolve().parent.parent
SLUG = 'prestige-32'
PHOTO = lambda n, s='': f'/{SLUG}-{n}{s}.jpg'  # usa el SLUG vigente (cambia con load())

T = {
 'es': dict(
  nav=['El barco', 'Cubierta', 'Puestos de mando', 'Interior', 'Ficha técnica', 'Fotos', 'Visita'], navlabel='Secciones de la ficha',
  hero_alt='Jeanneau Prestige 32 fondeada en una cala de Menorca, vista de costado con el auxiliar en el pescante', specs_btn='Ver los datos',
  cub_k='Cubierta', cub_h='Un vistazo por fuera', cub_p='Toca los números para ver qué hay en cada zona. Fotos del propietario.',
  spots=[('Flybridge', 'Segundo puesto de gobierno arriba, con bimini (en la foto, plegado).'),
         ('Salón y puesto interior', 'El salón con cocina y el primer puesto de gobierno, con vista a proa.'),
         ('Solárium de proa', 'Zona para tumbarse en proa, con barandilla alrededor.'),
         ('Bañera', 'Zona de popa, con acceso al salón.'),
         ('Plataforma y auxiliar', 'Plataforma de baño con pescante, auxiliar y fueraborda: lo que se agradece al fondear en una cala.')],
  man_k='Puestos de mando', man_h='Se gobierna desde dentro o desde arriba',
  m1_h='Dos puestos de gobierno', m1_p=['El interior, junto al salón, y el del flybridge, con bimini. Los dos llevan la instrumentación del motor.', 'Electrónica: plotter/sonda y VHF.'],
  m1_alt=['Puesto de gobierno interior', 'Puesto de gobierno del flybridge'],
  m2_h='Dos motores diésel', m2_p=['Dos Volvo Penta D4 de 260 cv, con unas 1.500 horas en total según el propietario. Con dos motores se maniobra en puerto con más soltura; a cambio, son dos líneas de propulsión que mantener.', 'Prestaciones y consumo, en la prueba de mar.'],
  m2_alt='Flybridge con asientos y puesto de gobierno',
  mid='¿Quieres pedir el historial de mantenimiento?', ask='Preguntar por WhatsApp',
  int_k='Interior', int_h='Para dormir a bordo',
  i1_h='Salón y cocina', i1_p='Salón con mesa y sofá, televisión y cocina. Tapicería y madera cuidadas, según se ve en las fotos.', i1_alt='Salón con mesa y sofá',
  i2_h='Dos camarotes', i2_p='El de proa y un segundo camarote con televisión.', i2_alt='Camarote de proa',
  i3_h='Un baño completo', i3_p='Y la cocina en el salón, junto al puesto de gobierno interior.', i3_alt=['Cocina', 'Baño'],
  fic_k='Ficha técnica', fic_h='Los datos',
  big=[('10,65 m', 'Eslora (fabricante)'), ('3,52 m', 'Manga (fabricante)'), ('2 x 260 cv', 'Volvo Penta D4'), ('≈ 1.500 h', 'Horas de motor (total)')],
  gal_h='Todas las fotos', gal_p='Toca una foto para verla en grande.',
  end_h='¿Quieres verlo en persona?', end_p='Está en Menorca y se ve con cita previa. Te cuento el historial y organizamos la visita.', visit='Solicitar visita'),
 'ca': dict(
  nav=['El vaixell', 'Coberta', 'Llocs de comandament', 'Interior', 'Fitxa tècnica', 'Fotos', 'Visita'], navlabel='Seccions de la fitxa',
  hero_alt="Jeanneau Prestige 32 fondejada en una cala de Menorca, vista de costat amb l'auxiliar al pescant", specs_btn='Veure les dades',
  cub_k='Coberta', cub_h="Una ullada per fora", cub_p='Toca els números per veure què hi ha a cada zona. Fotos del propietari.',
  spots=[('Flybridge', 'Segon lloc de govern a dalt, amb bimini (a la foto, plegat).'),
         ('Saló i lloc interior', 'El saló amb cuina i el primer lloc de govern, amb vista a proa.'),
         ('Solàrium de proa', 'Zona per estirar-se a proa, amb barana al voltant.'),
         ('Banyera', 'Zona de popa, amb accés al saló.'),
         ('Plataforma i auxiliar', "Plataforma de bany amb pescant, auxiliar i fora borda: el que s'agraeix quan fondeges en una cala.")],
  man_k='Llocs de comandament', man_h="Es governa des de dins o des de dalt",
  m1_h='Dos llocs de govern', m1_p=["L'interior, al costat del saló, i el del flybridge, amb bimini. Tots dos porten la instrumentació del motor.", 'Electrònica: plotter/sonda i VHF.'],
  m1_alt=['Lloc de govern interior', 'Lloc de govern del flybridge'],
  m2_h='Dos motors dièsel', m2_p=['Dos Volvo Penta D4 de 260 cv, amb unes 1.500 hores en total segons el propietari. Amb dos motors es maniobra a port amb més facilitat; a canvi, són dues línies de propulsió per mantenir.', 'Prestacions i consum, a la prova de mar.'],
  m2_alt='Flybridge amb seients i lloc de govern',
  mid="Vols demanar l'historial de manteniment?", ask='Preguntar per WhatsApp',
  int_k='Interior', int_h='Per dormir a bord',
  i1_h='Saló i cuina', i1_p='Saló amb taula i sofà, televisió i cuina. Tapisseria i fusta cuidades, segons es veu a les fotos.', i1_alt='Saló amb taula i sofà',
  i2_h='Dues cabines', i2_p='La de proa i una segona cabina amb televisió.', i2_alt='Cabina de proa',
  i3_h='Un bany complet', i3_p='I la cuina al saló, al costat del lloc de govern interior.', i3_alt=['Cuina', 'Bany'],
  fic_k='Fitxa tècnica', fic_h='Les dades',
  big=[('10,65 m', 'Eslora (fabricant)'), ('3,52 m', 'Mànega (fabricant)'), ('2 x 260 cv', 'Volvo Penta D4'), ('≈ 1.500 h', 'Hores de motor (total)')],
  gal_h='Totes les fotos', gal_p='Toca una foto per veure-la en gran.',
  end_h="El vols veure en persona?", end_p="És a Menorca i es pot veure amb cita prèvia. T'explico l'historial i organitzem la visita.", visit='Sol·licitar visita'),
 'en': dict(
  nav=['The boat', 'Deck', 'Helm stations', 'Interior', 'Specifications', 'Photos', 'Viewing'], navlabel='Listing sections',
  hero_alt='Jeanneau Prestige 32 anchored in a cove in Menorca, side view with the tender on the davits', specs_btn='See the specs',
  cub_k='Deck', cub_h='A look around the outside', cub_p="Tap the numbers to see what's in each area. Owner's photos.",
  spots=[('Flybridge', 'Second helm station up top, with bimini (folded in the photo).'),
         ('Saloon and lower helm', 'The saloon with galley and the main helm station, looking forward.'),
         ('Foredeck sunpad', 'Sunbathing area on the bow, with guardrails all round.'),
         ('Cockpit', 'Aft area, with access to the saloon.'),
         ('Platform and tender', "Bathing platform with davits, tender and outboard: what you'll appreciate when anchoring in a cove.")],
  man_k='Helm stations', man_h='Helm it from inside or from up top',
  m1_h='Two helm stations', m1_p=['The lower helm, next to the saloon, and the flybridge helm, with bimini. Both have engine instruments.', 'Electronics: chartplotter/sounder and VHF.'],
  m1_alt=['Lower helm station', 'Flybridge helm station'],
  m2_h='Twin diesel engines', m2_p=['Twin Volvo Penta D4 260 hp, with about 1,500 hours in total according to the owner. Twin engines give you more control when manoeuvring in port; on the other hand, there are two drive lines to maintain.', 'Performance and fuel use: on the sea trial.'],
  m2_alt='Flybridge with seating and helm station',
  mid='Would you like to ask for the maintenance history?', ask='Ask on WhatsApp',
  int_k='Interior', int_h='Made for sleeping on board',
  i1_h='Saloon and galley', i1_p='Saloon with table and sofa, TV and galley. Upholstery and woodwork look well kept in the photos.', i1_alt='Saloon with table and sofa',
  i2_h='Two cabins', i2_p='The forward cabin and a second cabin with TV.', i2_alt='Forward cabin',
  i3_h='One full bathroom', i3_p='And the galley in the saloon, next to the lower helm.', i3_alt=['Galley', 'Bathroom'],
  fic_k='Specifications', fic_h='The details',
  big=[('10.65 m', 'Length (builder)'), ('3.52 m', 'Beam (builder)'), ('2 x 260 hp', 'Volvo Penta D4'), ('≈ 1,500 h', 'Engine hours (total)')],
  gal_h='All photos', gal_p='Tap a photo to see it larger.',
  end_h='Would you like to see it in person?', end_p="It's in Menorca and can be viewed by appointment. I'll tell you its history and we'll arrange the viewing.", visit='Request a viewing'),
 'fr': dict(
  nav=['Le bateau', 'Pont', 'Postes de pilotage', 'Intérieur', 'Fiche technique', 'Photos', 'Visite'], navlabel='Sections de la fiche',
  hero_alt="Jeanneau Prestige 32 au mouillage dans une crique de Minorque, vue de profil avec l'annexe sur les bossoirs", specs_btn='Voir les données',
  cub_k='Pont', cub_h="Un coup d'œil à l'extérieur", cub_p='Touchez les numéros pour voir chaque zone. Photos du propriétaire.',
  spots=[('Flybridge', 'Second poste de pilotage en haut, avec bimini (replié sur la photo).'),
         ('Carré et poste intérieur', 'Le carré avec cuisine et le premier poste de pilotage, vue vers l’avant.'),
         ('Bain de soleil avant', "Zone pour s'allonger à l'avant, avec filières tout autour."),
         ('Cockpit', "Zone arrière, avec accès au carré."),
         ('Plateforme et annexe', 'Plateforme de bain avec bossoirs, annexe et hors-bord : appréciable au mouillage dans une crique.')],
  man_k='Postes de pilotage', man_h="On le pilote de l'intérieur ou d'en haut",
  m1_h='Deux postes de pilotage', m1_p=["Le poste intérieur, à côté du carré, et celui du flybridge, avec bimini. Les deux ont l'instrumentation moteur.", 'Électronique : traceur/sondeur et VHF.'],
  m1_alt=['Poste de pilotage intérieur', 'Poste de pilotage du flybridge'],
  m2_h='Deux moteurs diesel', m2_p=['Deux Volvo Penta D4 de 260 ch, environ 1 500 heures au total selon le propriétaire. Avec deux moteurs, on manœuvre au port plus facilement ; en contrepartie, il y a deux lignes de propulsion à entretenir.', "Performances et consommation : lors de l'essai en mer."],
  m2_alt='Flybridge avec sièges et poste de pilotage',
  mid="Vous voulez demander l'historique d'entretien ?", ask='Demander sur WhatsApp',
  int_k='Intérieur', int_h='Pour dormir à bord',
  i1_h='Carré et cuisine', i1_p='Carré avec table et canapé, télévision et cuisine. Sellerie et boiseries soignées, d’après les photos.', i1_alt='Carré avec table et canapé',
  i2_h='Deux cabines', i2_p="La cabine avant et une seconde cabine avec télévision.", i2_alt='Cabine avant',
  i3_h='Une salle de bain complète', i3_p='Et la cuisine dans le carré, à côté du poste intérieur.', i3_alt=['Cuisine', 'Salle de bain'],
  fic_k='Fiche technique', fic_h='Les données',
  big=[('10,65 m', 'Longueur (chantier)'), ('3,52 m', 'Largeur (chantier)'), ('2 x 260 ch', 'Volvo Penta D4'), ('≈ 1 500 h', 'Heures moteur (total)')],
  gal_h='Toutes les photos', gal_p='Touchez une photo pour l’agrandir.',
  end_h='Vous voulez le voir sur place ?', end_p="Il est à Minorque et se visite sur rendez-vous. Je vous raconte son historique et on organise la visite.", visit='Demander une visite'),
}
SPOTS_XY = [(50, 24), (39, 37), (24, 41), (74, 50), (89, 58)]
# Fotos de cada bloque (número de foto del barco)
PH = dict(hero=1, spots=1, m1=(16, 17), m2=5, i1=7, i2=9, i3=(12, 14), end=2)
IDS = ['barco', 'cubierta', 'mando', 'interior', 'ficha', 'fotos', 'visita']

def img(n, alt, cls='', eager=False):
    lz = '' if eager else ' loading="lazy" decoding="async"'
    return (f'<img{" class=%s" % chr(34)+cls+chr(34) if cls else ""} src="{PHOTO(n,"-m")}" srcset="{PHOTO(n,"-m")} 1000w, {PHOTO(n)} 1600w" '
            f'sizes="(max-width: 820px) 100vw, 560px" alt="{H.escape(alt)}"{lz}>')

def build(lang):
    p = ROOT / ('' if lang == 'es' else lang) / 'barcos' / f'{SLUG}.html'
    s = p.read_text()
    if 'class="boat v2"' in s:
        print(lang, 'ya es v2'); return
    t = T[lang]
    i0 = s.index('<div class="head" data-pm-boat='); i0 = s.rindex('\n', 0, i0) + 1
    g0 = s.index('<div class="gal">'); g0 = s.rindex('\n', 0, g0) + 1
    n0 = s.index('<p class="muted head-note">')
    head = s[i0:g0]
    status = re.search(r'<span class="status[^"]*">[^<]*</span>', head).group(0)
    h1 = re.search(r'<h1>.*?</h1>', head).group(0)
    sub = re.search(r'<div class="sub">.*?</div>', head).group(0)
    price = re.search(r'<p class="price">.*?</p>', head).group(0)
    ask_a = re.search(r'<a class="btn btn-wa btn-ask"[^>]*>', head).group(0)
    ask_href = re.search(r'href="([^"]+)"', ask_a).group(1)
    pdf_a = re.search(r'<a class="pdf-link"[^>]*>.*?</a>', head).group(0)
    gal = gal_src = s[g0:n0]
    note = re.search(r'<p class="muted head-note">.*?</p>\n', s).group(0)
    specs = re.search(r'<dl class="specs">.*?</dl>', s, re.S).group(0)
    visit_a = re.search(r'<a class="btn btn-wa"[^>]*data-wa-context="ficha_visita">[^<]*</a>', s).group(0)
    visit_href = re.search(r'href="([^"]+)"', visit_a).group(1)
    wa = lambda txt, ctx, cls='btn btn-wa': f'<a class="{cls}" href="{ask_href}" target="_blank" rel="noopener" data-wa-context="{ctx}">{txt}</a>'
    vis = lambda cls='btn btn-wa': f'<a class="{cls}" href="{visit_href}" target="_blank" rel="noopener" data-wa-context="ficha_visita">{t["visit"]}</a>'

    side = '<nav class="v2-side" aria-label="%s">' % t['navlabel'] + ''.join(
        f'<a href="#{i}"><span>{n}</span><i></i></a>' for i, n in zip(IDS, t['nav'])) + '</nav>'
    hero = f'''<section class="v2-hero" id="barco">
<img class="v2-hero-img" src="{PHOTO(PH['hero'])}" srcset="{PHOTO(PH['hero'],'-m')} 1000w, {PHOTO(PH['hero'])} 1600w" sizes="100vw" alt="{H.escape(t['hero_alt'])}" fetchpriority="high">
<div class="v2-hero-in wrap head" data-pm-boat="{SLUG}">
<div>{status}
{h1}
{sub}</div>
<div class="price-box">{price}
<div class="v2-ctas">{ask_a}{re.search(r'>([^<]*)</a>', head[head.find('btn-ask'):]).group(1)}</a><a class="btn v2-ghost" href="#ficha">{t['specs_btn']}</a></div>
{pdf_a.replace('class="pdf-link"', 'class="pdf-link v2-pdf"')}</div>
</div>
</section>
'''
    dots = ''.join(f'<button type="button" class="v2-dot" style="left:{x}%;top:{y}%" data-t="{k}" aria-expanded="false" aria-label="{H.escape(t["spots"][k][0])}">{k+1}</button>'
                   for k, (x, y) in enumerate(SPOTS_XY))
    legend = ''.join(f'<li><b>{k+1} · {H.escape(a)}.</b> {H.escape(b)}</li>' for k, (a, b) in enumerate(t['spots']))
    data = H.escape('[' + ','.join('["%s","%s"]' % (a.replace('"', '\\"'), b.replace('"', '\\"')) for a, b in t['spots']) + ']')
    duo = lambda a, b, alts: f'<div class="v2-ph v2-duo">{img(a, alts[0])}{img(b, alts[1])}</div>'
    one = lambda n, alt: f'<div class="v2-ph">{img(n, alt)}</div>'
    _blk = lambda ph, h, ps, rev=False: f'<div class="v2-alt{" rev" if rev else ""}">{ph}<div><h3>{h}</h3>' + ''.join(f'<p>{x}</p>' for x in ([ps] if isinstance(ps, str) else ps)) + '</div></div>'
    # Barcos con pocas fotos: un bloque con PH=None no sale; m1/i3 con un solo número llevan una foto en vez de dos
    def blk(k, rev=False):
        n = PH.get(k)
        if n is None: return ''
        alt = t[k + '_alt']
        ph = duo(*n, alt) if isinstance(n, tuple) else one(n, alt[0] if isinstance(alt, list) else alt)
        return _blk(ph, t[k + '_h'], t[k + '_p'], rev)
    # miniaturas de la galería sin texto alternativo: nombre del barco y número de foto
    bname = re.sub(r'<[^>]+>', '', h1).strip()
    fw = {'es': 'foto', 'ca': 'foto', 'en': 'photo', 'fr': 'photo'}[lang]
    gal = re.sub(r'alt="" loading="lazy" data-i="(\d+)"', lambda m: f'alt="{bname} – {fw} {int(m.group(1)) + 1}" loading="lazy" data-i="{m.group(1)}"', gal)
    sections = f'''<div class="wrap v2-note">{note.strip()}</div>
<section class="v2-sec" id="cubierta"><div class="wrap">
<p class="v2-k">{t['cub_k']}</p><h2>{t['cub_h']}</h2><p class="v2-lead">{t['cub_p']}</p>
<div class="v2-spots" data-spots="{data}">{img(PH['spots'], t.get('spots_alt', t['hero_alt']))}{dots}</div>
<ol class="v2-legend">{legend}</ol>
</div></section>
<section class="v2-sec v2-band" id="mando"><div class="wrap">
<p class="v2-k">{t['man_k']}</p><h2>{t['man_h']}</h2>
{blk('m1')}
{blk('m2', True)}
<div class="v2-mid"><p>{t['mid']}</p>{wa(t['ask'], 'ficha_historial')}</div>
</div></section>
<section class="v2-sec" id="interior"><div class="wrap">
<p class="v2-k">{t['int_k']}</p><h2>{t['int_h']}</h2>
{blk('i1')}
{blk('i2', True)}
{blk('i3')}
</div></section>
<section class="v2-sec v2-dark" id="ficha"><div class="wrap">
<p class="v2-k">{t['fic_k']}</p><h2>{t['fic_h']}</h2>
<div class="v2-big">{''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in t['big'])}</div>
{specs}
<div class="v2-ctas">{vis()}{pdf_a.replace('class="pdf-link"', 'class="btn v2-ghost"')}</div>
</div></section>
<section class="v2-sec" id="fotos"><div class="wrap">
<h2>{t['gal_h']}</h2><p class="v2-lead">{t['gal_p']}</p>{gal}</div></section>
'''
    end = f'''<section class="v2-end" id="visita" style="--bg:url('{PHOTO(PH['end'],"-m")}')"><div class="wrap">
<h2>{t['end_h']}</h2><p>{t['end_p']}</p>
<div class="v2-ctas">{vis()}{wa(t['ask'], 'ficha_cierre', 'btn v2-ghost')}</div>
</div></section>
'''
    # quitar cabecera, galería, nota y specs de su sitio original
    s2 = s.replace(head, '').replace(gal_src, '\n').replace(note, '').replace(specs, '')
    s2, nn = re.subn(r'<main class="boat">\s*<div class="wrap">', lambda m: '<main class="boat v2">\n' + side + '\n' + hero + sections + '<div class="wrap">', s2, count=1)
    assert nn == 1
    # quitar la miga de pan dentro del wrap y ponerla arriba del todo (sigue visible y accesible)
    crumb = re.search(r'[ \t]*<p class="crumb">.*?</p>\n', s2).group(0)
    s2 = s2.replace(crumb, '', 1).replace('<main class="boat v2">\n', '<main class="boat v2">\n<div class="wrap v2-crumb">' + crumb.strip() + '</div>\n', 1)
    assert '<div class="wrap"><!--pm-sim-->' in s2
    s2 = s2.replace('<div class="wrap"><!--pm-sim-->', end + '<div class="wrap"><!--pm-sim-->', 1)
    s2 = re.sub(r'(<div class="wrap"></div>\s*)+', '', s2)
    s2 = re.sub(r'(<link rel="stylesheet" href="(?:/barcos/)?barcos\.css">)', r'\1\n<link rel="stylesheet" href="/barcos/ficha-v2.css?v=20261011">', s2, count=1)
    s2 = s2.replace('<script src="/barcos/ficha-acciones.js', '<script src="/barcos/ficha-v2.js?v=20261011" defer></script>\n<script src="/barcos/ficha-acciones.js', 1)
    assert s2.count('<h1>') == 1 and 'ficha-v2.css' in s2 and 'ficha-v2.js' in s2 and 'class="specs"' in s2 and 'class="gal"' in s2
    p.write_text(s2)
    print(lang, 'ok', len(s), '->', len(s2))

def load(slug):
    """Carga la configuración de otro barco desde _tools/ficha_v2_boats/<slug>.py (SLUG, T, SPOTS_XY, PH)."""
    import importlib.util
    global SLUG, T, SPOTS_XY, PH
    pth = pathlib.Path(__file__).resolve().parent / 'ficha_v2_boats' / (slug.replace('-', '_') + '.py')
    spec = importlib.util.spec_from_file_location('cfg', pth); cfg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cfg)
    SLUG, T, SPOTS_XY, PH = cfg.SLUG, cfg.T, cfg.SPOTS_XY, cfg.PH

if __name__ == '__main__':
    import sys
    for slug in (sys.argv[1:] or ['prestige-32']):
        if slug != 'prestige-32': load(slug)
        for l in T: build(l)
