# Plata Marine · motorizaciones Mercury en el configurador Mar.Co (tarifa de Mar.Co, oct 2026).
# Precio mostrado = precio de tarifa Mercury + instalación (incluye instalación, baterías, desconectadores y filtros).
# Idempotente: reescribe el bloque "mer" de window.MC_CFG y los textos de motores en las 36 páginas.
import json, os, re, sys

ROOT = os.environ.get('PM_ROOT', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V = '20261027m'

# (n, cv): (nombre, tarifa, blanco, jpo [-1 no disponible, 0 incluido], instalación)
ENG = {
    (1, 250): ('Verado V8 250', 26600, 900, -1, 2750),
    (1, 300): ('Verado V8 300', 30150, 900, -1, 2750),
    (1, 350): ('Verado V10 350', 35800, 1200, -1, 2750),
    (1, 400): ('Verado V10 400', 40100, 1200, -1, 2750),
    (1, 425): ('Verado V10 425', 40900, 1200, -1, 2750),
    (1, 500): ('Racing V8 500R', 64800, 800, -1, 2750),
    (2, 200): ('FourStroke V6 200', 43850, 1800, -1, 4750),
    (2, 225): ('FourStroke V6 225', 46500, 1500, -1, 4750),
    (2, 250): ('Verado V8 250', 50850, 1800, 17500, 4750),
    (2, 300): ('Verado V8 300', 58000, 1800, 17500, 4750),
    (2, 350): ('Verado V10 350', 69850, 2400, 16000, 4750),
    (2, 400): ('Verado V10 400', 78350, 2400, 16100, 4750),
    (2, 425): ('Verado V10 425', 80000, 2400, 16100, 4750),
    (2, 500): ('Racing V8 500R', 127100, 1500, 26750, 4750),
    (2, 600): ('Verado V12 600', 181900, 3500, 0, 6500),
    (3, 300): ('Verado V8 300', 89450, 2700, 21000, 6200),
    (3, 350): ('Verado V10 350', 106000, 3500, 19500, 6200),
    (3, 400): ('Verado V10 400', 117450, 3500, 19500, 6200),
    (3, 425): ('Verado V10 425', 120300, 3500, 19500, 6200),
    (3, 500): ('Racing V8 500R', 192850, 2250, 32000, 6200),
}
OPT = {
    'twentythree': ['1*250', '1*300'],
    'r-evolution-26': ['1*350', '1*400', '1*425', '1*500'],
    'r-evolution-x27': ['2*200', '2*225', '2*250', '2*300'],
    'twentysix': ['2*225', '2*250', '2*300'],
    'e-motion-29': ['2*250', '2*300'],
    'e-motion-32': ['2*300', '2*350'],
    'e-motion-36': ['2*400', '2*425', '2*500', '2*600', '3*300', '3*350', '3*400', '3*425', '3*500'],
    'r-evolution-35': ['2*300', '2*350', '2*400', '2*425', '2*500'],
    'r-evolution-x36': ['2*400', '2*425', '2*500', '2*600', '3*300', '3*350', '3*400', '3*425', '3*500'],
}
T = {
    'es': dict(pre='', h='Elige la motorización Mercury', w='Motores en color blanco', j='Joystick JPO', inc='incluido',
               n='Precio de tarifa Mercury con instalación, baterías, desconectadores y filtros.',
               note_old='Los motores no están en la tarifa del astillero: te los presupuesto aparte.',
               note_new='Con Mercury tienes aquí el precio de cada motorización; con otra marca, te la presupuesto aparte.',
               tot_old='motores y transporte desde fábrica, aparte', tot_new='transporte desde fábrica y motores de otra marca, aparte'),
    'ca': dict(pre='ca/', h='Tria la motorització Mercury', w='Motors de color blanc', j='Joystick JPO', inc='inclòs',
               n='Preu de tarifa Mercury amb instal·lació, bateries, desconnectadors i filtres.',
               note_old='Els motors no són a la tarifa de la drassana: te’ls pressuposto a part.',
               note_new='Amb Mercury tens aquí el preu de cada motorització; amb una altra marca, te la pressuposto a part.',
               tot_old='motors i transport des de fàbrica, a part', tot_new='transport des de fàbrica i motors d’una altra marca, a part'),
    'en': dict(pre='en/', h='Choose your Mercury engines', w='White engines', j='JPO joystick', inc='included',
               n='Mercury list price including installation, batteries, battery switches and filters.',
               note_old='Engines are not in the shipyard price list: I quote them separately.',
               note_new='With Mercury you see the price of each engine package here; other brands I quote separately.',
               tot_old='engines and transport from the factory are extra', tot_new='transport from the factory and other-brand engines are extra'),
    'fr': dict(pre='fr/', h='Choisissez la motorisation Mercury', w='Moteurs de couleur blanche', j='Joystick JPO', inc='inclus',
               n='Prix tarif Mercury avec installation, batteries, coupe-batteries et filtres.',
               note_old='Les moteurs ne figurent pas au tarif du chantier : je vous les chiffre à part.',
               note_new='Avec Mercury, vous voyez ici le prix de chaque motorisation ; une autre marque, je vous la chiffre à part.',
               tot_old='moteurs et transport depuis l’usine en sus', tot_new='transport depuis l’usine et moteurs d’une autre marque en sus'),
}

def mer(slug):
    out = []
    for k in OPT[slug]:
        n, cv = map(int, k.split('*'))
        name, lp, wh, jpo, ins = ENG[(n, cv)]
        out.append([f'{n} × Mercury {name}', lp + ins, wh, jpo])
    return out

changed = 0
for lg, t in T.items():
    for slug in OPT:
        f = os.path.join(ROOT, t['pre'] + 'marco', slug, 'index.html')
        s = open(f, encoding='utf-8').read(); o = s
        m = re.search(r'window\.MC_CFG=(\{.*?\});</script>', s, re.S)
        if not m: sys.exit('sin MC_CFG: ' + f)
        d = json.loads(m.group(1))
        d['mer'] = mer(slug)
        d['L'].update({'m_h': t['h'], 'm_w': t['w'], 'm_j': t['j'], 'm_inc': t['inc'], 'm_n': t['n']})
        s = s[:m.start(1)] + json.dumps(d, ensure_ascii=False) + s[m.end(1):]
        s = s.replace(t['note_old'], t['note_new']).replace(t['tot_old'], t['tot_new'])
        s = re.sub(r'marco-config\.js\?v=[0-9a-z]+', 'marco-config.js?v=' + V, s)
        if t['note_new'] not in s or t['tot_new'] not in s: sys.exit('texto no encontrado: ' + f)
        if s != o:
            open(f, 'w', encoding='utf-8').write(s); changed += 1
print('ok', changed, 'páginas')
