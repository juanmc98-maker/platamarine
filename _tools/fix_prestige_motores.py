"""Prestige 32: corrige el motor (son 2 x Volvo Penta D4 260 cv, aprox. 1.500 h en total, dato confirmado por Juan
el 11 oct 2026) en ficha ES/CA/EN/FR, portada, catálogo, páginas de compra, inventario y buscador.
Uso: python3 _tools/fix_prestige_motores.py   (idempotente)"""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent

# Frases largas por idioma (primero) ------------------------------------------------------------
P = {
 'es': [
  (r'<p>Monta un único Volvo Penta D4 de 260 CV diésel.*?</p>',
   '<p>Monta dos Volvo Penta D4 de 260 CV diésel, con unas 1.500 horas en total según el propietario. Es una motorización muy extendida en barcos de esta eslora. Con dos motores se maniobra en puerto con más soltura; a cambio, son dos líneas de propulsión que mantener. Las prestaciones y el consumo reales dependen de la carga, el estado del casco y las hélices: lo suyo es comprobarlos en la prueba de mar.</p>'),
  (r'<h3>Un solo motor diésel</h3><p>.*?</p>',
   '<h3>Dos motores diésel</h3><p>Dos Volvo Penta D4 de 260 cv, con unas 1.500 horas en total según el propietario. Con dos motores se maniobra en puerto con más soltura; a cambio, son dos líneas de propulsión que mantener.</p>'),
  ('mantenimiento del motor y la cola (con unas 1.500 horas,', 'mantenimiento de los motores y las colas (con unas 1.500 horas en total,'),
  ('con un Volvo Penta D4 de 260 CV diésel y unas 1.500 horas', 'con dos Volvo Penta D4 de 260 CV diésel y unas 1.500 horas en total'),
  ('Volvo Penta D4 de 260 cv diésel (aprox. 1.500 h)', 'dos Volvo Penta D4 de 260 cv diésel (aprox. 1.500 h en total)'),
  ('Volvo Penta D4 260 cv diésel (aprox. 1.500 h)', '2 x Volvo Penta D4 260 cv diésel (aprox. 1.500 h en total)'),
  ('<dd>Aprox. 1.500</dd>', '<dd>Aprox. 1.500 en total</dd>'),
  ('<span>Horas de motor</span>', '<span>Horas de motor (total)</span>'),
 ],
 'ca': [
  (r'<p>Munta un únic Volvo Penta D4 de 260 CV dièsel.*?</p>',
   '<p>Munta dos Volvo Penta D4 de 260 CV dièsel, amb unes 1.500 hores en total segons el propietari. És una motorització molt estesa en vaixells d&#x27;aquesta eslora. Amb dos motors es maniobra a port amb més facilitat; a canvi, són dues línies de propulsió per mantenir. Les prestacions i el consum reals depenen de la càrrega, l&#x27;estat del casc i les hèlixs: el millor és comprovar-los a la prova de mar.</p>'),
  (r'<h3>Un sol motor dièsel</h3><p>.*?</p>',
   '<h3>Dos motors dièsel</h3><p>Dos Volvo Penta D4 de 260 cv, amb unes 1.500 hores en total segons el propietari. Amb dos motors es maniobra a port amb més facilitat; a canvi, són dues línies de propulsió per mantenir.</p>'),
  ('manteniment del motor i la cua (amb unes 1.500 hores,', 'manteniment dels motors i les cues (amb unes 1.500 hores en total,'),
  ('amb un Volvo Penta D4 de 260 CV dièsel i unes 1.500 hores', 'amb dos Volvo Penta D4 de 260 CV dièsel i unes 1.500 hores en total'),
  ('Volvo Penta D4 de 260 cv dièsel (aprox. 1.500 h)', 'dos Volvo Penta D4 de 260 cv dièsel (aprox. 1.500 h en total)'),
  ('Volvo Penta D4 260 cv dièsel (aprox. 1.500 h)', '2 x Volvo Penta D4 260 cv dièsel (aprox. 1.500 h en total)'),
  ('<dd>Aprox. 1.500</dd>', '<dd>Aprox. 1.500 en total</dd>'),
  ('<span>Hores de motor</span>', '<span>Hores de motor (total)</span>'),
 ],
 'en': [
  (r'<p>It has a single Volvo Penta D4 260 hp diesel.*?</p>',
   '<p>It has twin Volvo Penta D4 260 hp diesels, with around 1,500 hours in total according to the owner. It is a very common engine on boats of this size. Twin engines give you more control when manoeuvring in port; on the other hand, there are two drive lines to maintain. Real performance and fuel consumption depend on load, hull condition and propellers, so they are best checked on a sea trial.</p>'),
  (r'<h3>A single diesel engine</h3><p>.*?</p>',
   '<h3>Twin diesel engines</h3><p>Twin Volvo Penta D4 260 hp, with about 1,500 hours in total according to the owner. Twin engines give you more control when manoeuvring in port; on the other hand, there are two drive lines to maintain.</p>'),
  ('maintenance invoices for the engine and sterndrive (with around 1,500 hours,', 'maintenance invoices for the engines and sterndrives (with around 1,500 hours in total,'),
  ('with a single 260 hp Volvo Penta D4 diesel and around 1,500 hours', 'with twin 260 hp Volvo Penta D4 diesels and around 1,500 hours in total'),
  ('single Volvo Penta D4 260 hp diesel (approx. 1,500 h)', 'twin Volvo Penta D4 260 hp diesels (approx. 1,500 h in total)'),
  ('Volvo Penta D4 260 hp diesel (approx. 1,500 h)', 'twin Volvo Penta D4 260 hp diesels (approx. 1,500 h in total)'),
  ('<dd>Approx. 1,500</dd>', '<dd>Approx. 1,500 in total</dd>'),
  ('<span>Engine hours</span>', '<span>Engine hours (total)</span>'),
 ],
 'fr': [
  (r'<p>Il est équipé d’un seul moteur diesel Volvo Penta D4 260 ch.*?</p>',
   '<p>Il est équipé de deux moteurs diesel Volvo Penta D4 de 260 ch, avec environ 1 500 heures au total selon le propriétaire. C’est une motorisation très répandue sur les bateaux de cette taille. Avec deux moteurs, on manœuvre au port plus facilement ; en contrepartie, il y a deux lignes de propulsion à entretenir. Les performances et la consommation réelles dépendent de la charge, de l’état de la coque et des hélices : le mieux est de les vérifier lors de l’essai en mer.</p>'),
  (r'<h3>Un seul moteur diesel</h3><p>.*?</p>',
   '<h3>Deux moteurs diesel</h3><p>Deux Volvo Penta D4 de 260 ch, environ 1 500 heures au total selon le propriétaire. Avec deux moteurs, on manœuvre au port plus facilement ; en contrepartie, il y a deux lignes de propulsion à entretenir.</p>'),
  ('factures d’entretien du moteur et de l’embase (avec environ 1 500 heures,', 'factures d’entretien des moteurs et des embases (avec environ 1 500 heures au total,'),
  (r'avec un seul moteur diesel Volvo Penta D4 de 260 ch\s+et environ 1[\s ]500 heures','avec deux moteurs diesel Volvo Penta D4 de 260 ch et environ 1 500 heures au total'),
  ('un seul moteur diesel Volvo Penta D4 260 ch (env. 1 500 h)', 'deux moteurs diesel Volvo Penta D4 260 ch (env. 1 500 h au total)'),
  ('moteur diesel Volvo Penta D4 260 ch (env. 1 500 h)', 'deux moteurs diesel Volvo Penta D4 260 ch (env. 1 500 h au total)'),
  ('<li>Diesel Volvo Penta D4 260 ch</li>', '<li>2 x Volvo Penta D4 260 ch, diesel</li>'),
  ('<dd>Env. 1 500</dd>', '<dd>Env. 1 500 au total</dd>'),
  ('<span>Heures moteur</span>', '<span>Heures moteur (total)</span>'),
 ],
}
# Cortas y comunes: "Volvo Penta D4 260 cv/hp/ch" → "2 x …" (solo donde no lleve ya 2 x / dos / twin)
SHORT = [(r'(?<!2 x )(?<!dos )(?<!twin )(?<!Twin )(?<!deux moteurs diesel )Volvo Penta D4 260 (cv|hp|ch)\b', r'2 x Volvo Penta D4 260 \1'),
         (r'<b>260 (cv|hp|ch)</b>', r'<b>2 x 260 \1</b>')]

def lang_of(p):
    r = p.relative_to(ROOT).parts
    return r[0] if r[0] in ('ca', 'en', 'fr') else 'es'

def fix(p, lang=None):
    s0 = s = p.read_text()
    langs = [lang] if lang else ['es', 'ca', 'en', 'fr']
    for l in langs:
        for a, b in P[l]:
            if a.startswith(('<p>', '<h3>', 'avec un seul')):
                s = re.sub(a, lambda m: b, s, flags=re.S)
            else:
                s = s.replace(a, b)
    for a, b in SHORT:
        s = re.sub(a, b, s)
    if s != s0:
        p.write_text(s); print('ok', p.relative_to(ROOT))

if __name__ == '__main__':
    files = set()
    for pat in ['barcos/*.html', '*/barcos/*.html', 'index.html', '*/index.html', 'comprar/*.html', '*/comprar/*.html']:
        files |= set(ROOT.glob(pat))
    for p in sorted(files):
        if 'D4' in p.read_text():
            fix(p, lang_of(p))
    for p in [ROOT / 'inventario.js'] + sorted(ROOT.glob('search/*.json')):
        fix(p, None if p.name == 'inventario.js' else p.stem)
