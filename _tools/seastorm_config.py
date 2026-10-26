#!/usr/bin/env python3
"""Añade el configurador "Configura tu SeaStorm" a /seastorm/ en ES/CA/EN/FR (después de "cara a cara").
Idempotente: reemplaza lo que haya entre <!--ss-cfg--> y <!--/ss-cfg-->. Relanzar SIEMPRE después de build_seastorm.py.
Uso (desde la raíz del repo): python3 _tools/seastorm_config.py

Qué hace: modelo -> color de casco -> motor -> extras, con precio al momento y la titulación que pide.
Solo usa datos contrastados de build_seastorm.py (PVP Advantage .990 +IVA, CV recomendados y máximos, eslora).
No inventa precios de motor, remolque, transporte ni matriculación: salen como "te lo presupuesto".
Titulación: RD 875/2014 art. 10.1.a (redacción RD 1188/2025): sin título hasta 5 m y 15 CV, uso privado, de día,
a no más de 2 millas; Licencia de Navegación hasta 6 m. Lógica en /seastorm/config.js."""
import re, json, html

ROOT = '.'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
IVA = 0.21
VAT = {'es': '+IVA', 'ca': '+IVA', 'en': '+VAT', 'fr': 'HT'}
# slug, nombre, eslora (m), CV máx, CV recomendados (texto, valor para "recomendado"), PVP sin IVA, foto o None
M = [
 ('12',   'SeaStorm 12',   3.66, 30, '25–30', 30, 4454, '/seastorm/fotos/12-1-m.jpg'),
 ('13-s', 'SeaStorm 13 S', 4.00, 60, '40',    40, 6683, '/seastorm/fotos/13-s-1-m.jpg'),
 ('14',   'SeaStorm 14',   4.28, 40, '30–40', 40, 7253, '/seastorm/fotos/14-1-m.jpg'),
 ('17',   'SeaStorm 17',   5.17, 80, '60',    60, 10928, '/seastorm/fotos/17-1-m.jpg'),
]
COLORS = [('#F4F5F2', 'white'), ('#B9BEC2', 'lgrey'), ('#4D555B', 'dgrey'), ('#2F6B3A', 'green'), ('#9BD31F', 'lime'), ('#C62828', 'red'), ('#F2C511', 'yellow'), ('#1F4E8C', 'blue'), ('#E8712A', 'orange')]

T = {
 'es': dict(
  nav='Configurar', k='Configurador', h='Configura tu SeaStorm',
  sub='Elige modelo, color, motor y extras. Verás el precio del barco al momento, la titulación que necesitas y lo que te presupuesto aparte.',
  s1='1. Modelo', s2='2. Color del casco', s3='3. Motor', s4='4. Extras',
  colors={'white': 'Blanco', 'lgrey': 'Gris claro', 'dgrey': 'Gris oscuro', 'green': 'Verde', 'lime': 'Verde lima', 'red': 'Rojo', 'yellow': 'Amarillo', 'blue': 'Azul', 'orange': 'Naranja'},
  m_none='Sin motor', m_none_d='Ya tengo uno o lo pongo yo',
  m_15='15 CV', m_15_d='Se puede llevar sin titulación',
  m_rec='{cv} CV', m_rec_d='El recomendado por el fabricante',
  m_max='{cv} CV', m_max_d='La potencia máxima homologada',
  x_trailer='Remolque adecuado a su peso', x_reg='Matriculación y papeles', x_ship='Transporte desde fábrica',
  x_ship_d='siempre aparte',
  sum_h='Tu SeaStorm', sum_boat='Barco (versión Advantage)', sum_vat='con IVA', sum_color='Color', sum_motor='Motor',
  sum_lic='Titulación', lic_none='Sin titulación: uso privado, de día y a no más de 2 millas de la salida, mayor de 18 años',
  lic_ln='Licencia de Navegación o superior',
  sum_quote='Te presupuesto aparte', q_motor='motor de {cv} CV', q_trailer='remolque', q_reg='matriculación y papeles', q_ship='transporte desde fábrica',
  b_form='Pedir este presupuesto', b_wa='Enviarlo por WhatsApp',
  wa='Hola Juan, he configurado un SeaStorm en la web: {cfg}. ¿Me preparas presupuesto?',
  msg='Configuración: {cfg}',
  note='Precio del barco según la tarifa oficial de SeaStorm para la versión Advantage, sin motor. Motor, remolque, transporte y matriculación se presupuestan aparte y por escrito antes de pedir nada. Los colores en pantalla son orientativos. Información orientativa y no vinculante: podemos equivocarnos.'),
 'ca': dict(
  nav='Configurar', k='Configurador', h='Configura el teu SeaStorm',
  sub="Tria model, color, motor i extres. Veuràs el preu del barco al moment, la titulació que necessites i el que et pressuposto a part.",
  s1='1. Model', s2='2. Color del casc', s3='3. Motor', s4='4. Extres',
  colors={'white': 'Blanc', 'lgrey': 'Gris clar', 'dgrey': 'Gris fosc', 'green': 'Verd', 'lime': 'Verd llima', 'red': 'Vermell', 'yellow': 'Groc', 'blue': 'Blau', 'orange': 'Taronja'},
  m_none='Sense motor', m_none_d="Ja en tinc un o el poso jo",
  m_15='15 CV', m_15_d='Es pot portar sense titulació',
  m_rec='{cv} CV', m_rec_d='El recomanat pel fabricant',
  m_max='{cv} CV', m_max_d='La potència màxima homologada',
  x_trailer='Remolc adequat al seu pes', x_reg='Matriculació i papers', x_ship='Transport des de fàbrica',
  x_ship_d='sempre a part',
  sum_h='El teu SeaStorm', sum_boat='Barco (versió Advantage)', sum_vat='amb IVA', sum_color='Color', sum_motor='Motor',
  sum_lic='Titulació', lic_none='Sense titulació: ús privat, de dia i a no més de 2 milles de la sortida, major de 18 anys',
  lic_ln='Llicència de Navegació o superior',
  sum_quote='Et pressuposto a part', q_motor='motor de {cv} CV', q_trailer='remolc', q_reg='matriculació i papers', q_ship='transport des de fàbrica',
  b_form='Demanar aquest pressupost', b_wa='Enviar-ho per WhatsApp',
  wa='Hola Juan, he configurat un SeaStorm a la web: {cfg}. Em prepares pressupost?',
  msg='Configuració: {cfg}',
  note="Preu del barco segons la tarifa oficial de SeaStorm per a la versió Advantage, sense motor. Motor, remolc, transport i matriculació es pressuposten a part i per escrit abans de demanar res. Els colors en pantalla són orientatius. Informació orientativa i no vinculant: ens podem equivocar."),
 'en': dict(
  nav='Configure', k='Configurator', h='Build your SeaStorm',
  sub='Choose model, colour, engine and extras. You will see the boat price straight away, the licence you need and what I quote separately.',
  s1='1. Model', s2='2. Hull colour', s3='3. Engine', s4='4. Extras',
  colors={'white': 'White', 'lgrey': 'Light grey', 'dgrey': 'Dark grey', 'green': 'Green', 'lime': 'Lime green', 'red': 'Red', 'yellow': 'Yellow', 'blue': 'Blue', 'orange': 'Orange'},
  m_none='No engine', m_none_d='I already have one or will fit my own',
  m_15='15 hp', m_15_d='No licence needed in Spain',
  m_rec='{cv} hp', m_rec_d="The manufacturer's recommendation",
  m_max='{cv} hp', m_max_d='Maximum rated power',
  x_trailer='Trailer suited to its weight', x_reg='Registration and paperwork', x_ship='Transport from the factory',
  x_ship_d='always separate',
  sum_h='Your SeaStorm', sum_boat='Boat (Advantage version)', sum_vat='incl. VAT', sum_color='Colour', sum_motor='Engine',
  sum_lic='Licence (Spain)', lic_none='No licence: private use, daytime, no more than 2 miles from departure, over 18',
  lic_ln='Licencia de Navegación or higher',
  sum_quote='Quoted separately', q_motor='{cv} hp engine', q_trailer='trailer', q_reg='registration and paperwork', q_ship='transport from the factory',
  b_form='Request this quote', b_wa='Send it on WhatsApp',
  wa='Hi Juan, I have built a SeaStorm on your website: {cfg}. Could you prepare a quote?',
  msg='Configuration: {cfg}',
  note="Boat price from SeaStorm's official price list for the Advantage version, without engine. Engine, trailer, transport and registration are quoted separately and in writing before anything is ordered. On-screen colours are approximate. Guidance only, not binding: we may make mistakes."),
 'fr': dict(
  nav='Configurer', k='Configurateur', h='Configurez votre SeaStorm',
  sub='Choisissez le modèle, la couleur, le moteur et les options. Vous verrez tout de suite le prix du bateau, le permis nécessaire et ce que je chiffre à part.',
  s1='1. Modèle', s2='2. Couleur de coque', s3='3. Moteur', s4='4. Options',
  colors={'white': 'Blanc', 'lgrey': 'Gris clair', 'dgrey': 'Gris foncé', 'green': 'Vert', 'lime': 'Vert citron', 'red': 'Rouge', 'yellow': 'Jaune', 'blue': 'Bleu', 'orange': 'Orange'},
  m_none='Sans moteur', m_none_d="J'en ai déjà un ou je le monte moi-même",
  m_15='15 CV', m_15_d='Sans permis en Espagne',
  m_rec='{cv} CV', m_rec_d='Le moteur conseillé par le fabricant',
  m_max='{cv} CV', m_max_d='La puissance maximale homologuée',
  x_trailer='Remorque adaptée à son poids', x_reg='Immatriculation et papiers', x_ship="Transport depuis l'usine",
  x_ship_d='toujours à part',
  sum_h='Votre SeaStorm', sum_boat='Bateau (version Advantage)', sum_vat='TTC', sum_color='Couleur', sum_motor='Moteur',
  sum_lic='Permis (Espagne)', lic_none="Sans permis : usage privé, de jour, à 2 milles maximum du départ, plus de 18 ans",
  lic_ln='Licencia de Navegación ou supérieur',
  sum_quote='Chiffré à part', q_motor='moteur de {cv} CV', q_trailer='remorque', q_reg='immatriculation et papiers', q_ship="transport depuis l'usine",
  b_form='Demander ce devis', b_wa="L'envoyer sur WhatsApp",
  wa="Bonjour Juan, j'ai configuré un SeaStorm sur le site : {cfg}. Pouvez-vous me préparer un devis ?",
  msg='Configuration : {cfg}',
  note="Prix du bateau selon le tarif officiel SeaStorm pour la version Advantage, sans moteur. Moteur, remorque, transport et immatriculation sont chiffrés à part et par écrit avant toute commande. Les couleurs à l'écran sont indicatives. Information indicative et non contractuelle : nous pouvons nous tromper."),
}

CSS = """<style id="ss-cfg-css">
.ss-cfg{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:28px;align-items:start;margin-top:26px}
.ss-cfg fieldset{border:0;margin:0 0 22px;padding:0;min-width:0}
.ss-cfg legend{font-family:var(--display);font-size:12.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--sea);margin-bottom:10px;padding:0}
.ss-cfg-m{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
.ss-cfg-m label,.ss-cfg-e label{position:relative;display:flex;cursor:pointer}
.ss-cfg input{position:absolute;opacity:0;width:1px;height:1px}
.ss-cfg-m label>span{display:flex;flex-direction:column;width:100%;border:1.5px solid var(--line);border-radius:12px;overflow:hidden;background:#fff;transition:border-color .15s,box-shadow .15s}
.ss-cfg-m img,.ss-cfg-m i{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;background:var(--soft)}
.ss-cfg-m i{display:flex;align-items:center;justify-content:center;font-style:normal;font-family:var(--display);font-weight:800;font-size:1.3rem;color:var(--ink)}
.ss-cfg-m b{font-family:var(--display);font-size:.95rem;padding:8px 10px 2px}
.ss-cfg-m small{font-size:.85rem;color:var(--ink-2,#46606e);padding:0 10px 9px}
.ss-cfg-m input:checked+span{border-color:var(--sea);box-shadow:0 0 0 3px rgba(11,118,107,.18)}
.ss-cfg input:focus-visible+span{outline:2px solid var(--ink);outline-offset:2px}
.ss-cfg-c{display:flex;flex-wrap:wrap;gap:10px}
.ss-cfg-c label{cursor:pointer;position:relative}
.ss-cfg-c span{display:block;width:44px;height:44px;border-radius:50%;border:2px solid rgba(14,48,66,.18);transition:box-shadow .15s}
.ss-cfg-c input:checked+span{box-shadow:0 0 0 3px #fff,0 0 0 5px var(--sea)}
.ss-cfg-c input:focus-visible+span{outline:2px solid var(--ink);outline-offset:4px}
.ss-cfg-cn{font-size:.92rem;color:var(--ink-2,#46606e);margin-top:8px}
.ss-cfg-e{display:grid;gap:8px}
.ss-cfg-e label>span{display:flex;justify-content:space-between;gap:12px;width:100%;border:1.5px solid var(--line);border-radius:12px;padding:12px 14px;background:#fff;font-size:.97rem}
.ss-cfg-e label>span em{font-style:normal;color:var(--ink-2,#46606e);font-size:.88rem;text-align:right}
.ss-cfg-e input:checked+span{border-color:var(--sea);box-shadow:0 0 0 3px rgba(11,118,107,.18)}
.ss-cfg-e input:focus-visible+span{outline:2px solid var(--ink);outline-offset:2px}
.ss-cfg-e .fixed span{background:var(--soft);cursor:default}
.ss-cfg-sum{position:sticky;top:84px;background:var(--soft);border-radius:16px;padding:20px 20px 22px}
.ss-cfg-sum svg{display:block;width:100%;height:auto;margin:-4px 0 6px}
.ss-cfg-sum h3{font-size:1.3rem;font-weight:800;margin:0 0 4px}
.ss-cfg-pr{font-family:var(--display);font-size:1.9rem;font-weight:800;line-height:1.1}
.ss-cfg-pr .vat{font-size:.55em}
.ss-cfg-vi{font-size:.9rem;color:var(--ink-2,#46606e);margin:2px 0 12px}
.ss-cfg-sum dl{margin:0;display:grid;gap:8px;font-size:.95rem}
.ss-cfg-sum dl div{display:grid;grid-template-columns:110px 1fr;gap:10px;border-top:1px solid var(--line);padding-top:8px}
.ss-cfg-sum dt{color:var(--ink-2,#46606e)}
.ss-cfg-sum dd{margin:0;font-weight:600}
.ss-cfg-btns{display:grid;gap:10px;margin-top:16px}
.ss-cfg-btns .ss-btn{width:100%}
.ss-cfg-note{font-size:.8rem;line-height:1.5;color:var(--ink-2,#46606e);margin-top:14px}
@media (max-width:900px){.ss-cfg{grid-template-columns:1fr}.ss-cfg-sum{position:static}}
@media (max-width:640px){.ss-cfg-m{grid-template-columns:repeat(2,minmax(0,1fr))}.ss-cfg-sum dl div{grid-template-columns:96px 1fr}}
</style>"""

# Silueta propia de una lancha pequeña de consola (dibujo genérico). El casco toma el color elegido.
SVG = ('<svg viewBox="0 0 400 150" role="img" aria-hidden="true">'
       '<path d="M20 112 Q200 126 380 104" fill="none" stroke="#9fb6c0" stroke-width="2" stroke-dasharray="6 6"/>'
       '<path id="ssCfgHull" d="M28 70 L364 70 Q378 70 382 76 L340 108 Q330 114 312 114 L70 114 Q50 114 40 104 L28 92 Z" fill="#F4F5F2" stroke="#0E3042" stroke-width="2.5" stroke-linejoin="round"/>'
       '<path d="M30 80 L372 80" stroke="#0E3042" stroke-opacity=".25" stroke-width="2"/>'
       '<rect x="150" y="44" width="34" height="26" rx="4" fill="#fff" stroke="#0E3042" stroke-width="2.5"/>'
       '<path d="M156 44 L170 26 L186 26" fill="none" stroke="#0E3042" stroke-width="2.5" stroke-linecap="round"/>'
       '<path d="M70 70 L70 54 L110 54" fill="none" stroke="#0E3042" stroke-width="2.5" stroke-linecap="round"/>'
       '<path d="M250 70 L250 58 L330 58 L352 70" fill="none" stroke="#0E3042" stroke-width="2.5" stroke-linejoin="round"/>'
       '<g id="ssCfgEng"><rect x="6" y="56" width="22" height="30" rx="5" fill="#0E3042"/><rect x="13" y="86" width="8" height="30" fill="#0E3042"/></g>'
       '</svg>')


def eur(n, lang):
    s = f'{n:,}'
    if lang == 'en':
        return '€' + s
    if lang == 'fr':
        return s.replace(',', ' ') + ' €'
    return s.replace(',', '.') + ' €'


def section(lang):
    t = T[lang]
    e = html.escape
    models = ''.join(
        f'<label><input type="radio" name="cfg_m" value="{s}"{" checked" if s == "14" else ""}>'
        f'<span>{f"<img src={chr(34)}{ph}{chr(34)} alt={chr(34)}{chr(34)} width={chr(34)}800{chr(34)} height={chr(34)}600{chr(34)} loading={chr(34)}lazy{chr(34)} decoding={chr(34)}async{chr(34)}>" if ph else "<i>" + n.split()[-2] + " " + n.split()[-1] + "</i>"}'
        f'<b>{e(n)}</b><small>{eur(p, lang)}<span class="vat">{VAT[lang]}</span></small></span></label>'
        for s, n, _l, _mx, _r, _rv, p, ph in M)
    colors = ''.join(
        f'<label><input type="radio" name="cfg_c" value="{k}"{" checked" if k == "white" else ""} aria-label="{e(t["colors"][k])}"><span style="background:{hx}"></span></label>'
        for hx, k in COLORS)
    data = {
        'lang': lang, 'iva': IVA,
        'vat': VAT[lang], 'm': {s: {'n': n, 'loa': l, 'max': mx, 'rec': rv, 'p': p} for s, n, l, mx, _r, rv, p, _ph in M},
        'c': {k: {'hex': hx, 'n': t['colors'][k]} for hx, k in COLORS},
        't': {k: t[k] for k in ('m_none', 'm_none_d', 'm_15', 'm_15_d', 'm_rec', 'm_rec_d', 'm_max', 'm_max_d', 'lic_none', 'lic_ln',
                                'q_motor', 'q_trailer', 'q_reg', 'q_ship', 'wa', 'msg', 'sum_vat')},
    }
    return f'''<!--ss-cfg-->
<section class="ss-sec" id="configurar" style="padding-top:0">
  <div class="wrap"><p class="ss-kick">{t['k']}</p><h2>{t['h']}</h2><p class="ss-sub">{t['sub']}</p>
  <div class="ss-cfg" id="ssCfg">
    <div>
      <fieldset><legend>{t['s1']}</legend><div class="ss-cfg-m">{models}</div></fieldset>
      <fieldset><legend>{t['s2']}</legend><div class="ss-cfg-c">{colors}</div><p class="ss-cfg-cn" id="ssCfgCn"></p></fieldset>
      <fieldset><legend>{t['s3']}</legend><div class="ss-cfg-e" id="ssCfgMot"></div></fieldset>
      <fieldset><legend>{t['s4']}</legend><div class="ss-cfg-e">
        <label><input type="checkbox" name="cfg_x" value="trailer"><span>{t['x_trailer']}</span></label>
        <label><input type="checkbox" name="cfg_x" value="reg"><span>{t['x_reg']}</span></label>
        <div class="fixed"><label><span>{t['x_ship']}<em>{t['x_ship_d']}</em></span></label></div>
      </div></fieldset>
    </div>
    <aside class="ss-cfg-sum" aria-live="polite">
      {SVG}
      <h3 id="ssCfgName"></h3>
      <p class="ss-cfg-pr" id="ssCfgPr"></p><p class="ss-cfg-vi" id="ssCfgVi"></p>
      <dl>
        <div><dt>{t['sum_color']}</dt><dd id="ssCfgCol"></dd></div>
        <div><dt>{t['sum_motor']}</dt><dd id="ssCfgMo"></dd></div>
        <div><dt>{t['sum_lic']}</dt><dd id="ssCfgLic"></dd></div>
        <div><dt>{t['sum_quote']}</dt><dd id="ssCfgQ"></dd></div>
      </dl>
      <div class="ss-cfg-btns"><a class="ss-btn pri" href="#presupuesto" id="ssCfgGo">{t['b_form']}</a><a class="ss-btn wa" href="https://wa.me/34633742973" id="ssCfgWa" target="_blank" rel="noopener">{t['b_wa']}</a></div>
      <p class="ss-cfg-note">{t['note']}</p>
    </aside>
  </div>
  <script type="application/json" id="ssCfgData">{json.dumps(data, ensure_ascii=False)}</script>
  </div>
</section>
<!--/ss-cfg-->'''


def run():
    for lang, pre in LANGS.items():
        p = f'{ROOT}{pre}/seastorm/index.html'
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'\n?<!--ss-cfg-->.*?<!--/ss-cfg-->', '', s, flags=re.S)
        s = re.sub(r'<style id="ss-cfg-css">.*?</style>', '', s, flags=re.S)
        s = s.replace('</head>', CSS + '\n</head>', 1)
        i = s.find('id="comparar"')
        j = s.find('</section>', i) + len('</section>')
        s = s[:j] + '\n' + section(lang) + s[j:]
        # menú interno de la página: "Configurar" detrás de "Comparar"
        nav = T[lang]['nav']
        if 'href="#configurar"' not in s.split('<!--ss-cfg-->')[0]:
            s = re.sub(r'(<a href="#comparar"[^>]*>[^<]*</a>)', r'\1' + f'<a href="#configurar">{nav}</a>', s, count=1)
        if '/seastorm/config.js' not in s:
            s = s.replace('</body>', '<script src="/seastorm/config.js" defer></script>\n</body>', 1)
        open(p, 'w', encoding='utf-8').write(s)
        print('ok', p)


if __name__ == '__main__':
    run()
