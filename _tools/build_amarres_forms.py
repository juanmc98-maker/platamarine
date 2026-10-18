"""Inserta en la guía de amarres (ES/CA/EN/FR) el enlace de arriba, el bloque de descarga de la tabla en PDF y el formulario
"¿Tienes un amarre que alquilar o traspasar?", y el mismo formulario en /servicios/amarres. Idempotente (marcas pm-am).
Uso: python3 _tools/build_amarres_forms.py   (desde la raíz del repo). Después: _tools/clean_urls.py si se usa y build_search_index.py no hace falta.
"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIA = 'amarres-cataluna-tipos-precios-alquiler-compra.html'

CSS = ('<style id="pm-am-css">.pm-amtop{font-family:var(--display);font-size:15px;margin:18px 0 0;display:flex;flex-wrap:wrap;gap:6px 18px}'
       '.pm-amtop a{font-weight:600}.pm-amf{background:#fff;border:1px solid var(--paper-2);border-top:3px solid var(--brass);border-radius:6px;padding:20px 20px 16px;margin:22px 0 28px}'
       '.pm-amf h3{font-size:20px;margin:0 0 6px}.pm-amf>p{margin:0 0 14px}.pm-amf form{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}'
       '.pm-amf .s2{grid-column:1/-1}.pm-amf label{display:block;font-family:var(--display);font-weight:600;font-size:13.5px;margin:0 0 4px}'
       '.pm-amf input[type=text],.pm-amf input[type=email],.pm-amf input[type=tel],.pm-amf select,.pm-amf textarea{width:100%;font:16px var(--serif);padding:11px 12px;border:1px solid var(--plata-2);border-radius:6px;background:#fff;color:var(--ink)}'
       '.pm-amf textarea{min-height:84px}.pm-amf .ck{display:flex;gap:10px;align-items:flex-start;font-family:var(--serif);font-weight:400;font-size:14.5px;line-height:1.45;margin:0;cursor:pointer}'
       '.pm-amf .ck input{width:20px;height:20px;min-width:20px;margin:1px 0 0;accent-color:#0B766B}.pm-amf button[type=submit]{font-family:var(--display);font-weight:600;font-size:15px;padding:14px 22px;border:0;border-radius:4px;background:var(--wa);color:#fff;cursor:pointer}'
       '.pm-amf button[type=submit]:hover{background:var(--wa-hover)}.pm-amf .help{font-size:13px;color:var(--ink-2);margin:0}.pm-amst{font-size:15px;margin:4px 0 0;display:flex;flex-wrap:wrap;gap:10px;align-items:center}'
       '.pm-amf i{color:#b42318;font-style:normal}@media (max-width:640px){.pm-amf form{grid-template-columns:1fr}.pm-amf{padding:18px 16px 14px}.pm-amf button[type=submit]{width:100%}}</style>')

T = {
 'es': dict(
  top='<a href="#descarga">Descarga la tabla de los 19 puertos en PDF</a><a href="#tengo-amarre">¿Tienes un amarre que alquilar o traspasar?</a>',
  dl_h='Llévate la tabla en PDF', dl_p='Las tarifas de los 19 puertos en una sola hoja, para tenerla a mano o compararlas con calma. Te la dejo aquí mismo en cuanto envíes el formulario.',
  name='Nombre', email='Email', tel='Teléfono', ph_name='Tu nombre', ph_email='nombre@gmail.com', ph_tel='600 000 000',
  priv_dl='Responsable: Juan Morante (Plata Marine). Uso tus datos para darte la tabla y, si me lo pides, ayudarte con el amarre o el barco. No los cedo a nadie. Puedes ejercer tus derechos en juan@platamarine.com. <a href="/privacidad.html">Política de privacidad</a>.',
  ck_priv='He leído la información de privacidad y acepto que uses estos datos para esto.', ck_nl='Quiero recibir de vez en cuando guías y novedades de Plata Marine (opcional).',
  dl_btn='Descargar la tabla', req='Los campos con * son obligatorios.',
  pub_h='¿Tienes un amarre que alquilar o traspasar?', pub_p='Si tienes un amarre en Cataluña o Baleares y quieres alquilarlo o traspasar el derecho de uso, puedo publicarlo en <a href="/servicios/amarres.html">la página de amarres</a> sin coste por adelantado. Cuéntame lo básico y te escribo.',
  pub_p2='Si tienes un amarre en Cataluña o Baleares y quieres alquilarlo o traspasar el derecho de uso, puedo publicarlo aquí sin coste por adelantado. Cuéntame lo básico y te escribo.',
  puerto='Puerto o club', ph_puerto='Port de Roses', medidas='Medidas (eslora × manga)', ph_medidas='10 × 3,5 m', modo='Qué quieres hacer',
  modos=['Alquilarlo', 'Traspasar el derecho de uso', 'Cualquiera de las dos'], conc='Concesión hasta', ph_conc='2040', precio='Precio que tienes en mente', ph_precio='Lo que tengas pensado',
  msg='Algo más', ph_msg='Agua y luz, parking, disponibilidad…', opt='(opcional)',
  priv_pub='Responsable: Juan Morante (Plata Marine). Uso tus datos solo para contestarte y, si lo acordamos, publicar tu amarre. No los cedo a nadie. Puedes ejercer tus derechos en juan@platamarine.com. <a href="/privacidad.html">Política de privacidad</a>.',
  ck_pub='He leído la información de privacidad y acepto que uses estos datos para contestarme.', pub_btn='Enviar',
  pub_note='Antes de publicar nada lo hablamos y lo dejamos por escrito. El traspaso suele necesitar la autorización del puerto o del club.',
  wa_alt='¿Prefieres WhatsApp?'),
 'ca': dict(
  top='<a href="#descarga">Descarrega la taula dels 19 ports en PDF</a><a href="#tengo-amarre">Tens un amarratge per llogar o traspassar?</a>',
  dl_h='Emporta’t la taula en PDF', dl_p='Les tarifes dels 19 ports en un sol full, per tenir-la a mà o comparar-les amb calma. Te la deixo aquí mateix tan bon punt enviïs el formulari.',
  name='Nom', email='Correu', tel='Telèfon', ph_name='El teu nom', ph_email='nom@gmail.com', ph_tel='600 000 000',
  priv_dl='Responsable: Juan Morante (Plata Marine). Faig servir les teves dades per donar-te la taula i, si m’ho demanes, ajudar-te amb l’amarratge o el vaixell. No les cedeixo a ningú. Pots exercir els teus drets a juan@platamarine.com. <a href="/ca/privacidad.html">Política de privacitat</a>.',
  ck_priv='He llegit la informació de privacitat i accepto que facis servir aquestes dades per a això.', ck_nl='Vull rebre de tant en tant guies i novetats de Plata Marine (opcional).',
  dl_btn='Descarregar la taula', req='Els camps amb * són obligatoris.',
  pub_h='Tens un amarratge per llogar o traspassar?', pub_p='Si tens un amarratge a Catalunya o a les Balears i el vols llogar o traspassar-ne el dret d’ús, el puc publicar a <a href="/ca/servicios/amarres.html">la pàgina d’amarratges</a> sense cap cost per avançat. Explica’m el bàsic i t’escric.',
  pub_p2='Si tens un amarrador a Catalunya o a les Balears i el vols llogar o traspassar-ne el dret d’ús, el puc publicar aquí sense cap cost per avançat. Explica’m el bàsic i t’escric.',
  puerto='Port o club', ph_puerto='Port de Roses', medidas='Mides (eslora × mànega)', ph_medidas='10 × 3,5 m', modo='Què vols fer',
  modos=['Llogar-lo', 'Traspassar el dret d’ús', 'Qualsevol de les dues'], conc='Concessió fins a', ph_conc='2040', precio='Preu que tens al cap', ph_precio='El que tinguis pensat',
  msg='Alguna cosa més', ph_msg='Aigua i llum, pàrquing, disponibilitat…', opt='(opcional)',
  priv_pub='Responsable: Juan Morante (Plata Marine). Faig servir les teves dades només per contestar-te i, si ho acordem, publicar el teu amarratge. No les cedeixo a ningú. Pots exercir els teus drets a juan@platamarine.com. <a href="/ca/privacidad.html">Política de privacitat</a>.',
  ck_pub='He llegit la informació de privacitat i accepto que facis servir aquestes dades per contestar-me.', pub_btn='Enviar',
  pub_note='Abans de publicar res ho parlem i ho deixem per escrit. El traspàs sol necessitar l’autorització del port o del club.',
  wa_alt='Prefereixes WhatsApp?'),
 'en': dict(
  top='<a href="#descarga">Download the 19-marina price table (PDF)</a><a href="#tengo-amarre">Do you have a berth to rent out or transfer?</a>',
  dl_h='Take the table with you as a PDF', dl_p='The rates for all 19 marinas on a single sheet, to keep handy or compare at your own pace. It appears right here as soon as you send the form.',
  name='Name', email='Email', tel='Phone', ph_name='Your name', ph_email='name@gmail.com', ph_tel='+44 7700 900000',
  priv_dl='Controller: Juan Morante (Plata Marine). I use your details to give you the table and, if you ask me, to help you with the berth or the boat. I do not share them with anyone. You can exercise your rights at juan@platamarine.com. <a href="/en/privacidad.html">Privacy policy</a>.',
  ck_priv='I have read the privacy information and agree to you using these details for this.', ck_nl='I would like to receive guides and news from Plata Marine now and then (optional).',
  dl_btn='Download the table', req='Fields marked * are required.',
  pub_h='Do you have a berth to rent out or transfer?', pub_p='If you have a berth in Catalonia or the Balearics and want to rent it out or transfer the right of use, I can list it on <a href="/en/servicios/amarres.html">the moorings page</a> with no upfront cost. Tell me the basics and I will get back to you.',
  pub_p2='If you have a berth in Catalonia or the Balearics and want to rent it out or transfer the right of use, I can list it here with no upfront cost. Tell me the basics and I will get back to you.',
  puerto='Marina or club', ph_puerto='Port de Roses', medidas='Size (length × beam)', ph_medidas='10 × 3.5 m', modo='What would you like to do',
  modos=['Rent it out', 'Transfer the right of use', 'Either'], conc='Concession until', ph_conc='2040', precio='Price you have in mind', ph_precio='Whatever you have in mind',
  msg='Anything else', ph_msg='Water and power, parking, availability…', opt='(optional)',
  priv_pub='Controller: Juan Morante (Plata Marine). I use your details only to reply to you and, if we agree, to list your berth. I do not share them with anyone. You can exercise your rights at juan@platamarine.com. <a href="/en/privacidad.html">Privacy policy</a>.',
  ck_pub='I have read the privacy information and agree to you using these details to reply to me.', pub_btn='Send',
  pub_note='Before anything is published we talk it through and put it in writing. A transfer usually needs the approval of the marina or club.',
  wa_alt='Prefer WhatsApp?'),
 'fr': dict(
  top='<a href="#descarga">Téléchargez le tableau des 19 ports en PDF</a><a href="#tengo-amarre">Vous avez une place de port à louer ou à céder ?</a>',
  dl_h='Emportez le tableau en PDF', dl_p='Les tarifs des 19 ports sur une seule feuille, à garder sous la main ou à comparer tranquillement. Il s’affiche ici dès que vous envoyez le formulaire.',
  name='Nom', email='E-mail', tel='Téléphone', ph_name='Votre nom', ph_email='nom@gmail.com', ph_tel='+33 6 12 34 56 78',
  priv_dl='Responsable : Juan Morante (Plata Marine). J’utilise vos données pour vous donner le tableau et, si vous me le demandez, vous aider pour la place de port ou le bateau. Je ne les cède à personne. Vous pouvez exercer vos droits à juan@platamarine.com. <a href="/fr/privacidad.html">Politique de confidentialité</a>.',
  ck_priv='J’ai lu les informations sur la confidentialité et j’accepte que vous utilisiez ces données à cette fin.', ck_nl='Je souhaite recevoir de temps en temps des guides et des nouveautés de Plata Marine (facultatif).',
  dl_btn='Télécharger le tableau', req='Les champs marqués * sont obligatoires.',
  pub_h='Vous avez une place de port à louer ou à céder ?', pub_p='Si vous avez une place de port en Catalogne ou aux Baléares et souhaitez la louer ou céder le droit d’usage, je peux la publier sur <a href="/fr/servicios/amarres.html">la page des places de port</a> sans frais à l’avance. Donnez-moi l’essentiel et je vous écris.',
  pub_p2='Si vous avez une place de port en Catalogne ou aux Baléares et souhaitez la louer ou céder le droit d’usage, je peux la publier ici sans frais à l’avance. Donnez-moi l’essentiel et je vous écris.',
  puerto='Port ou club', ph_puerto='Port de Roses', medidas='Dimensions (longueur × largeur)', ph_medidas='10 × 3,5 m', modo='Que souhaitez-vous faire',
  modos=['La louer', 'Céder le droit d’usage', 'L’un ou l’autre'], conc='Concession jusqu’en', ph_conc='2040', precio='Prix envisagé', ph_precio='Ce que vous avez en tête',
  msg='Autre chose', ph_msg='Eau et électricité, parking, disponibilité…', opt='(facultatif)',
  priv_pub='Responsable : Juan Morante (Plata Marine). J’utilise vos données uniquement pour vous répondre et, si nous en convenons, publier votre place. Je ne les cède à personne. Vous pouvez exercer vos droits à juan@platamarine.com. <a href="/fr/privacidad.html">Politique de confidentialité</a>.',
  ck_pub='J’ai lu les informations sur la confidentialité et j’accepte que vous utilisiez ces données pour me répondre.', pub_btn='Envoyer',
  pub_note='Avant toute publication, nous en parlons et le mettons par écrit. Une cession nécessite en général l’accord du port ou du club.',
  wa_alt='Vous préférez WhatsApp ?'),
}

def field(id_, name, label, typ, ph, req, auto='', opt='', cls=''):
    star = ' <i>*</i>' if req else ' <small>%s</small>' % opt
    return '<div class="%s"><label for="%s">%s%s</label><input id="%s" name="%s" type="%s" placeholder="%s"%s%s maxlength="%d"></div>' % (
        cls, id_, label, star, id_, name, typ, ph, ' required' if req else '', ' autocomplete="%s"' % auto if auto else '', 100 if typ == 'email' else 80)

def contact(t, p):
    return (field(p + 'n', 'nombre', t['name'], 'text', t['ph_name'], True, 'name') +
            field(p + 't', 'telefono', t['tel'], 'tel', t['ph_tel'], True, 'tel') +
            field(p + 'e', 'email', t['email'], 'email', t['ph_email'], True, 'email', cls='s2'))

def ck(id_, name, text, req):
    return '<div class="s2"><label class="ck" for="%s"><input id="%s" name="%s" type="checkbox"%s><span>%s%s</span></label></div>' % (
        id_, id_, name, ' required' if req else '', text, '&nbsp;<i>*</i>' if req else '')

def dl_box(t):
    return ('<!-- pm-am-dl --><div class="pm-amf" id="descarga"><h3>%s</h3><p>%s</p><form id="pmAmDl" novalidate>%s<p class="help s2">%s</p>%s%s'
            '<div class="s2"><button type="submit">%s</button></div><p class="help s2">%s</p><p class="pm-amst s2" role="status" aria-live="polite" hidden></p></form></div><!-- /pm-am-dl -->') % (
        t['dl_h'], t['dl_p'], contact(t, 'amd_'), t['priv_dl'], ck('amd_c', 'privacidad', t['ck_priv'], True), ck('amd_nl', 'novedades', t['ck_nl'], False), t['dl_btn'], t['req'])

def pub_form(t, intro):
    sel = '<div><label for="amp_m">%s <i>*</i></label><select id="amp_m" name="modalidad" required><option value=""></option>%s</select></div>' % (
        t['modo'], ''.join('<option>%s</option>' % o for o in t['modos']))
    return ('<!-- pm-am-pub --><div class="pm-amf" id="tengo-amarre"><h3>%s</h3><p>%s</p><form id="pmAmPub" novalidate>%s%s%s%s%s%s'
            '<div class="s2"><label for="amp_x">%s <small>%s</small></label><textarea id="amp_x" name="mensaje" maxlength="1000" placeholder="%s"></textarea></div>'
            '<p class="help s2">%s</p>%s<div class="s2"><button type="submit">%s</button></div><p class="help s2">%s %s</p><p class="pm-amst s2" role="status" aria-live="polite" hidden></p></form></div><!-- /pm-am-pub -->') % (
        t['pub_h'], intro, contact(t, 'amp_'),
        field('amp_p', 'puerto', t['puerto'], 'text', t['ph_puerto'], True), field('amp_d', 'medidas', t['medidas'], 'text', t['ph_medidas'], True),
        sel, field('amp_c', 'concesion', t['conc'], 'text', t['ph_conc'], False, opt=t['opt']), field('amp_r', 'precio', t['precio'], 'text', t['ph_precio'], False, opt=t['opt'], cls='s2'),
        t['msg'], t['opt'], t['ph_msg'], t['priv_pub'], ck('amp_ok', 'privacidad', t['ck_pub'], True), t['pub_btn'], t['req'], t['pub_note'])

def strip_old(s):
    s = re.sub(r'<!-- pm-am-(dl|pub|top) -->.*?<!-- /pm-am-\1 -->', '', s, flags=re.S)
    s = re.sub(r'<style id="pm-am-css">.*?</style>', '', s, flags=re.S)
    return s.replace('<script src="/guias/amarres-forms.js?v=20261018" defer></script>\n', '')

def add_common(s):
    s = s.replace('</head>', CSS + '\n</head>', 1)
    return s.replace('<script src="/analytics.js', '<script src="/guias/amarres-forms.js?v=20261018" defer></script>\n<script src="/analytics.js', 1)

def must(cond, msg):
    if not cond: raise SystemExit('No encuentro: ' + msg)

for lang, pre in [('es', ''), ('ca', 'ca/'), ('en', 'en/'), ('fr', 'fr/')]:
    t = T[lang]
    # Guía
    p = os.path.join(ROOT, pre + 'guias', GUIA); s = strip_old(open(p, encoding='utf-8').read())
    a = s.find('<p class="lead">'); b = s.find('</header>', a); must(a > 0 and b > 0, 'lead ' + p)
    s = s[:b] + '<!-- pm-am-top --><p class="pm-amtop">%s</p><!-- /pm-am-top -->\n      ' % t['top'] + s[b:]
    k = s.find('</table>'); k2 = s.find('</div>', k); must(k > 0 and k2 > 0, 'tabla ' + p); k2 += len('</div>')
    s = s[:k2] + '\n        ' + dl_box(t) + s[k2:]
    k = s.find('<p class="aviso">', s.find('id="buscas-amarre"')); must(k > 0, 'aviso ' + p)
    s = s[:k] + pub_form(t, t['pub_p']) + '\n        ' + s[k:]
    s = add_common(s)
    open(p, 'w', encoding='utf-8').write(s)
    # Servicios / amarres: el formulario sustituye al párrafo de texto + WhatsApp de #publicar (el WhatsApp queda debajo)
    p = os.path.join(ROOT, pre + 'servicios', 'amarres.html'); s = strip_old(open(p, encoding='utf-8').read())
    h = s.find('<h2 id="publicar">'); must(h > 0, 'publicar ' + p)
    e = s.find('</h2>', h) + 5
    p1 = s.find('<p>', e); p1e = s.find('</p>', p1) + 4          # párrafo explicativo
    w = s.find('<p><a class="btn btn-wa"', p1e); we = s.find('</p>', w) + 4
    must(p1 > 0 and w > 0 and w - p1e < 20, 'bloque publicar ' + p)
    wa = s[w:we].replace('<p><a class="btn btn-wa"', '<p class="help">%s <a' % t['wa_alt']).replace('" target="_blank" rel="noopener">', '" target="_blank" rel="noopener">', 1)
    wa = re.sub(r'(<p class="help">[^<]*<a [^>]*>)[^<]*(</a></p>)', r'\1WhatsApp\2', wa)
    form = pub_form(t, t['pub_p2']).replace('<div class="pm-amf" id="tengo-amarre"><h3>%s</h3>' % t['pub_h'], '<div class="pm-amf" id="tengo-amarre">')
    s = s[:e] + '\n        ' + form + '\n        ' + wa + s[we:]
    s = add_common(s)
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', lang)
