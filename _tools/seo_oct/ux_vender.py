# -*- coding: utf-8 -*-
"""Revisión UX de /vender-barco/ (6 oct 2026), ES/CA/EN/FR. Idempotente.
Orden nuevo: presentación → condiciones → cómo funciona (una sola explicación en 4 fases) → formulario →
preguntas frecuentes → contenido complementario (qué tener listo, precio, errores) → quién soy.
No se borra contenido salvo los "3 pasos", que repetían las 4 fases (su ancla #pasos se conserva)."""
import re, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HOW = {
 'es': ('Cómo funciona', 'Puedes anunciarlo tú, claro. La diferencia está en todo lo que pasa entre publicar el anuncio y cobrar: el precio, la ficha, las consultas, las visitas, la negociación y los papeles. Empiezas con el formulario de abajo o por WhatsApp, y esto es lo que hago yo en cada fase.'),
 'ca': ('Com funciona', 'Pots anunciar-lo tu, és clar. La diferència és tot el que passa entre publicar l\'anunci i cobrar: el preu, la fitxa, les consultes, les visites, la negociació i els papers. Comences amb el formulari de sota o per WhatsApp, i això és el que faig jo a cada fase.'),
 'en': ('How it works', 'You can list it yourself, of course. The difference lies in everything that happens between publishing the listing and getting paid: the price, the listing itself, enquiries, viewings, negotiation and paperwork. You start with the form below or on WhatsApp, and this is what I do at each stage.'),
 'fr': ('Comment ça marche', 'Vous pouvez bien sûr publier l’annonce vous-même. La différence tient à tout ce qui se passe entre la publication et l’encaissement : le prix, l’annonce, les demandes, les visites, la négociation et les démarches. Vous commencez avec le formulaire ci-dessous ou par WhatsApp, et voici ce que je fais à chaque étape.'),
}
HELP2 = {
 'es': 'Te confirmo aquí mismo cuando me llegue. Si lo prefieres, escríbeme por WhatsApp o email con los botones de arriba. Los campos con * son obligatorios.',
 'ca': 'Et confirmo aquí mateix quan m\'arribi. Si ho prefereixes, escriu-me per WhatsApp o correu amb els botons de dalt. Els camps amb * són obligatoris.',
 'en': 'I will confirm right here when it reaches me. If you prefer, message me on WhatsApp or by email with the buttons above. Fields marked * are required.',
 'fr': 'Je vous le confirme ici même dès réception. Si vous préférez, écrivez-moi par WhatsApp ou par e-mail avec les boutons ci-dessus. Les champs marqués * sont obligatoires.',
}
ORDER = [('inicio', 'sec alt'), ('condiciones', 'sec'), ('vender', 'sec alt'), ('valora', 'sec final'), ('preguntas', 'sec'), ('preparar', 'sec alt'), ('precio', 'sec'), ('errores', 'sec alt'), ('juan', 'sec')]

def run(l):
    f = os.path.join(ROOT, (l + '/' if l != 'es' else '') + 'vender-barco/index.html')
    s = open(f, encoding='utf-8').read(); o = s
    if 'data-ux="oct"' in s:
        return f, 'ya aplicado'
    secs = {}
    spans = []
    for m in re.finditer(r'<section class="([^"]*)" id="([a-z]+)">.*?</section>', s, flags=re.S):
        secs[m.group(2)] = m.group(0); spans.append((m.start(), m.end(), m.group(2)))
    need = [k for k, _ in ORDER] + ['pasos']
    missing = [k for k in need if k not in secs]
    assert not missing, (f, missing, list(secs))
    extra = [k for k in secs if k not in need]
    assert not extra, (f, extra)
    start, end = spans[0][0], spans[-1][1]
    between = s[start:end]
    # todo lo que no es <section> entre la primera y la última debe ser espacio en blanco
    rest = re.sub(r'<section class="[^"]*" id="[a-z]+">.*?</section>', '', between, flags=re.S)
    assert rest.strip() == '', (f, rest.strip()[:200])
    v = secs['vender']
    h2, lead = HOW[l]
    v = re.sub(r'<h2>.*?</h2>', '<h2>%s</h2>' % h2, v, count=1, flags=re.S)
    v = re.sub(r'<p class="sec-lead">.*?</p>', '<p class="sec-lead">%s</p>' % lead, v, count=1, flags=re.S)
    v = v.replace('<span id="como"></span>', '<span id="como"></span><span id="pasos"></span>', 1)
    secs['vender'] = v
    out = []
    for k, cls in ORDER:
        sec = re.sub(r'^<section class="[^"]*"', '<section class="%s"' % cls, secs[k], count=1)
        if k == 'inicio':
            sec = sec.replace('<section ', '<section data-ux="oct" ', 1)
        out.append(sec)
    s = s[:start] + '\n\n  '.join(out) + s[end:]
    s = re.sub(r'(<p class="form-help">)(Al pulsar «Enviar consulta»|En prémer «Enviar consulta»|Pressing "Send inquiry"|En appuyant sur « Envoyer la demande »)[^<]*(</p>)', lambda m: m.group(1) + HELP2[l] + m.group(3), s, count=1)
    open(f, 'w', encoding='utf-8').write(s)
    return f, len(o), len(s)

if __name__ == '__main__':
    for l in ['es', 'ca', 'en', 'fr']:
        print(run(l))
