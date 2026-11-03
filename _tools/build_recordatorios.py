#!/usr/bin/env python3
"""Avisos gratis de vencimientos del barco (ES/CA/EN/FR): /recordatorios-barco/.

Uso: python3 _tools/build_recordatorios.py
Molde: /servicios/cambio-titularidad-barco.html de cada idioma (cabecera, menú, pie, estilos de formulario).
El formulario envía a la hoja de leads con source 'recordatorio'; los avisos los manda el script diario
de la hoja (avisos a 60, 30 y 7 días y el mismo día). Dos casillas separadas: avisos (obligatoria) y
novedades (opcional, sin marcar). No toca menús, sitemap ni el índice de búsqueda.
"""
import json, re, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SLUG = 'recordatorios-barco'
SRC = 'cambio-titularidad-barco'
BASE = 'https://www.platamarine.com'
PRE = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
WA = 'https://wa.me/34633742973?text='
JS = f'/{SLUG}/recordatorios-forms.js?v=20261103'
TIPOS = ['itb', 'seguro', 'navegabilidad', 'permiso', 'titulo', 'balsa', 'extintores', 'bengalas', 'radiobaliza', 'otro']

T = {
 'es': dict(
  title='Avisos gratis de la ITB y el seguro del barco',
  desc='Apunta cuándo te vence la ITB, el seguro, el certificado de navegabilidad o las bengalas y te aviso por correo antes de que caduquen. Gratis.',
  crumb='Avisos de vencimientos', eyebrow='Herramientas · Papeles del barco',
  h1='Te aviso antes de que caduquen los papeles de tu barco',
  meta='<span>Por Juan Morante</span><span>Comprobado el 3 de noviembre de 2026</span>',
  lead='La ITB, el seguro o las bengalas caducan cuando menos te lo esperas, y casi siempre te enteras en el peor momento: en la gasolinera, en un control o al ir a vender el barco. Déjame la fecha y te escribo un correo antes de que venza. Es gratis y te das de baja cuando quieras.',
  toc=[('como', 'Cómo funciona'), ('apunta', 'Apunta tus fechas'), ('que', 'Qué vence en un barco'), ('datos', 'Tus datos')],
  como=['Eliges qué te vence y pones la fecha (puedes apuntar hasta cuatro cosas a la vez).',
        'Te escribo un correo unos 60 días antes, otro a los 30, otro a los 7 y otro el mismo día.',
        'Si cambias de barco o ya lo has renovado, me contestas al correo y lo actualizo o lo borro.'],
  aviso='Los avisos son orientativos: la fecha que cuenta es la de tu documentación. Si tienes dudas sobre si a tu barco le toca la ITB, mira la <a href="/guias/itb-inspeccion-tecnica-barcos-recreo">guía de la ITB</a>.',
  que_intro='Lo que más se olvida, con su plazo habitual. Confírmalo siempre con tu documentación:',
  que=[('ITB', 'cada 5 años como máximo en barcos de lista 7ª de 6 a 24 m, y según la lista y la eslora en el resto.'),
       ('Seguro de responsabilidad civil', 'cuando acaba la póliza, normalmente cada año.'),
       ('Certificado de navegabilidad', 'la validez que figure en el propio certificado.'),
       ('Bengalas, cohetes y botes de humo', 'la fecha de caducidad de cada unidad.'),
       ('Extintores, balsa salvavidas y chalecos inflables', 'las revisiones que marquen el fabricante y la normativa.'),
       ('Titulación náutica', 'la tarjeta se renueva cada 10 años, y cada 5 a partir de los 70.')],
  f=dict(n='Nombre', e='Email', boat='Nombre o modelo del barco', opt='(opcional)', boatp='Jeanneau Cap Camarat 7.5, "Tramuntana"…',
         rows='Qué te vence y cuándo', add='Añadir otra fecha', tipo='Qué vence', fecha='Fecha',
         tipos=['ITB', 'Seguro', 'Certificado de navegabilidad', 'Permiso de navegación', 'Titulación (tarjeta)', 'Balsa salvavidas', 'Extintores', 'Bengalas / pirotecnia', 'Radiobaliza', 'Otro'],
         ck1='Quiero recibir por correo los avisos de estas fechas. He leído la información de privacidad.',
         ck2='Además, puedes enviarme de vez en cuando novedades de Plata Marine (guías y barcos). Es opcional.',
         send='Activar mis avisos',
         legal='Responsable: Juan Morante (Plata Marine), juan@platamarine.com. Finalidad: enviarte los avisos de las fechas que apuntes y, solo si marcas la segunda casilla, novedades de Plata Marine. Base legal: tu consentimiento, que puedes retirar cuando quieras contestando a cualquier aviso o escribiendo a juan@platamarine.com. No cedo tus datos a terceros. Conservación: hasta que pase la última fecha que hayas apuntado o te des de baja. Derechos: acceso, rectificación, supresión, oposición y los demás que reconoce el RGPD; también puedes reclamar ante la AEPD. Más información en la <a href="/privacidad">política de privacidad</a>.',
         req='Los campos con * son obligatorios.'),
  datos='Solo te pido lo necesario para avisarte: un correo y las fechas. El nombre del barco es opcional. No uso estos datos para nada más salvo que marques la casilla de novedades, y en cada aviso tienes cómo darte de baja.',
  wa_msg='Hola Juan, tengo una duda sobre los papeles de mi barco.',
  aside_e='¿Dudas con los papeles?', aside_h='Te lo miro sin compromiso.', aside_p='ITB, cambio de nombre, bandera: dime qué tienes y te digo qué toca.', aside_b='Hablar con Juan por WhatsApp',
  toc_e='En esta página', rel_e='También te puede interesar',
  rel=[('/herramientas/libro-mantenimiento-barco', 'Libro de mantenimiento (PDF)'), ('/navegante/preparar-barco-fin-de-temporada', 'Invernaje del barco'), ('/guias/itb-inspeccion-tecnica-barcos-recreo', 'La ITB explicada'), ('/servicios/', 'Servicios náuticos')],
 ),
 'ca': dict(
  title="Avisos gratis de l'ITB i l'assegurança del vaixell",
  desc="Apunta quan et venç l'ITB, l'assegurança, el certificat de navegabilitat o les bengales i t'aviso per correu abans que caduquin. Gratis.",
  crumb='Avisos de venciments', eyebrow='Eines · Papers del vaixell',
  h1="T'aviso abans que caduquin els papers del teu vaixell",
  meta='<span>Per Juan Morante</span><span>Comprovat el 3 de novembre de 2026</span>',
  lead="L'ITB, l'assegurança o les bengales caduquen quan menys t'ho esperes, i gairebé sempre te n'assabentes en el pitjor moment: a la benzinera, en un control o quan vas a vendre el vaixell. Deixa'm la data i t'escric un correu abans que venci. És gratis i et dones de baixa quan vulguis.",
  toc=[('como', 'Com funciona'), ('apunta', 'Apunta les teves dates'), ('que', 'Què venç en un vaixell'), ('datos', 'Les teves dades')],
  como=["Tries què et venç i poses la data (pots apuntar fins a quatre coses alhora).",
        "T'escric un correu uns 60 dies abans, un altre als 30, un altre als 7 i un altre el mateix dia.",
        "Si canvies de vaixell o ja l'has renovat, em contestes el correu i ho actualitzo o ho esborro."],
  aviso="Els avisos són orientatius: la data que compta és la de la teva documentació. Si dubtes si al teu vaixell li toca l'ITB, mira la <a href=\"/ca/guias/itb-inspeccion-tecnica-barcos-recreo\">guia de l'ITB</a>.",
  que_intro="El que més s'oblida, amb el termini habitual. Confirma-ho sempre amb la teva documentació:",
  que=[('ITB', 'cada 5 anys com a màxim en vaixells de llista 7a de 6 a 24 m, i segons la llista i l’eslora en la resta.'),
       ('Assegurança de responsabilitat civil', 'quan acaba la pòlissa, normalment cada any.'),
       ('Certificat de navegabilitat', 'la validesa que figuri al mateix certificat.'),
       ('Bengales, coets i pots de fum', 'la data de caducitat de cada unitat.'),
       ('Extintors, bassa salvavides i armilles inflables', 'les revisions que marquin el fabricant i la normativa.'),
       ('Titulació nàutica', 'la targeta es renova cada 10 anys, i cada 5 a partir dels 70.')],
  f=dict(n='Nom', e='Correu', boat='Nom o model del vaixell', opt='(opcional)', boatp='Jeanneau Cap Camarat 7.5, "Tramuntana"…',
         rows='Què et venç i quan', add='Afegir una altra data', tipo='Què venç', fecha='Data',
         tipos=['ITB', 'Assegurança', 'Certificat de navegabilitat', 'Permís de navegació', 'Titulació (targeta)', 'Bassa salvavides', 'Extintors', 'Bengales / pirotècnia', 'Radiobalisa', 'Altres'],
         ck1="Vull rebre per correu els avisos d'aquestes dates. He llegit la informació de privacitat.",
         ck2="A més, em pots enviar de tant en tant novetats de Plata Marine (guies i vaixells). És opcional.",
         send='Activar els meus avisos',
         legal="Responsable: Juan Morante (Plata Marine), juan@platamarine.com. Finalitat: enviar-te els avisos de les dates que apuntis i, només si marques la segona casella, novetats de Plata Marine. Base legal: el teu consentiment, que pots retirar quan vulguis contestant qualsevol avís o escrivint a juan@platamarine.com. No cedeixo les teves dades a tercers. Conservació: fins que passi l'última data que hagis apuntat o et donis de baixa. Drets: accés, rectificació, supressió, oposició i els altres que reconeix el RGPD; també pots reclamar davant l'AEPD. Més informació a la <a href=\"/ca/privacidad\">política de privacitat</a>.",
         req='Els camps amb * són obligatoris.'),
  datos="Només et demano el necessari per avisar-te: un correu i les dates. El nom del vaixell és opcional. No faig servir aquestes dades per a res més si no marques la casella de novetats, i a cada avís tens com donar-te de baixa.",
  wa_msg='Hola Juan, tinc un dubte sobre els papers del meu vaixell.',
  aside_e='Dubtes amb els papers?', aside_h="T'ho miro sense compromís.", aside_p="ITB, canvi de nom, bandera: digues-me què tens i et dic què toca.", aside_b='Parlar amb Juan per WhatsApp',
  toc_e='En aquesta pàgina', rel_e='També et pot interessar',
  rel=[('/ca/herramientas/libro-mantenimiento-barco', 'Llibre de manteniment (PDF)'), ('/ca/navegante/preparar-barco-fin-de-temporada', 'Hivernatge del vaixell'), ('/ca/guias/itb-inspeccion-tecnica-barcos-recreo', "L'ITB explicada"), ('/ca/servicios/', 'Serveis nàutics')],
 ),
 'en': dict(
  title='Free reminders for your boat inspection and insurance',
  desc='Tell me when your boat inspection (ITB), insurance, seaworthiness certificate or flares expire and I will email you before they do. Free.',
  crumb='Expiry reminders', eyebrow='Tools · Boat paperwork',
  h1="I'll remind you before your boat's papers expire",
  meta='<span>By Juan Morante</span><span>Checked on 3 November 2026</span>',
  lead="The inspection, the insurance or the flares always seem to expire at the worst moment: at the fuel dock, during a check or just as you go to sell the boat. Leave me the date and I will send you an email before it runs out. It is free and you can unsubscribe whenever you like.",
  toc=[('como', 'How it works'), ('apunta', 'Add your dates'), ('que', 'What expires on a boat'), ('datos', 'Your data')],
  como=['Choose what expires and enter the date (up to four items at once).',
        'I email you about 60 days before, again at 30, at 7 and on the day itself.',
        'If you change boat or have already renewed, just reply to the email and I will update or delete it.'],
  aviso='Reminders are a guide: the date that counts is the one in your documents. If you are not sure whether your boat needs the ITB, see the <a href="/en/guias/itb-inspeccion-tecnica-barcos-recreo">ITB guide</a>.',
  que_intro='What people forget most, with the usual interval. Always check against your own documents:',
  que=[('ITB (Spanish boat inspection)', 'every 5 years at most for list 7 boats from 6 to 24 m; for others it depends on the list and length.'),
       ('Third-party liability insurance', 'when the policy ends, usually every year.'),
       ('Seaworthiness certificate', 'the validity shown on the certificate itself.'),
       ('Flares, rockets and smoke signals', 'the expiry date of each unit.'),
       ('Extinguishers, life raft and inflatable lifejackets', 'the servicing set by the manufacturer and the rules.'),
       ('Boating licence (Spanish card)', 'renewed every 10 years, and every 5 from age 70.')],
  f=dict(n='Name', e='Email', boat='Boat name or model', opt='(optional)', boatp='Jeanneau Cap Camarat 7.5, "Tramuntana"…',
         rows='What expires and when', add='Add another date', tipo='What expires', fecha='Date',
         tipos=['ITB (inspection)', 'Insurance', 'Seaworthiness certificate', 'Navigation permit', 'Licence (card)', 'Life raft', 'Extinguishers', 'Flares / pyrotechnics', 'EPIRB', 'Other'],
         ck1='I want to receive email reminders for these dates. I have read the privacy information.',
         ck2='You may also occasionally send me Plata Marine news (guides and boats). Optional.',
         send='Turn on my reminders',
         legal='Data controller: Juan Morante (Plata Marine), juan@platamarine.com. Purpose: sending you reminders for the dates you enter and, only if you tick the second box, Plata Marine news. Legal basis: your consent, which you can withdraw at any time by replying to any reminder or writing to juan@platamarine.com. Your data is not shared with third parties. Retention: until the last date you entered has passed or you unsubscribe. Rights: access, rectification, erasure, objection and the other GDPR rights; you can also complain to the Spanish Data Protection Agency (AEPD). More in the <a href="/en/privacidad">privacy policy</a>.',
         req='Fields marked * are required.'),
  datos='I only ask for what I need to remind you: an email and the dates. The boat name is optional. I do not use this data for anything else unless you tick the news box, and every reminder tells you how to unsubscribe.',
  wa_msg='Hi Juan, I have a question about my boat paperwork.',
  aside_e='Questions about paperwork?', aside_h='Happy to take a look.', aside_p='Inspection, change of ownership, flag: tell me what you have and I will tell you what is due.', aside_b='Message Juan on WhatsApp',
  toc_e='On this page', rel_e='You may also like',
  rel=[('/en/herramientas/libro-mantenimiento-barco', 'Maintenance log (PDF)'), ('/en/navegante/preparar-barco-fin-de-temporada', 'Laying up the boat'), ('/en/guias/itb-inspeccion-tecnica-barcos-recreo', 'The ITB explained'), ('/en/servicios/', 'Boat services')],
 ),
 'fr': dict(
  title='Rappels gratuits pour l’ITB et l’assurance du bateau',
  desc='Indiquez quand expirent l’ITB, l’assurance, le certificat de navigabilité ou les fusées de votre bateau et je vous préviens par e-mail. Gratuit.',
  crumb='Rappels d’échéances', eyebrow='Outils · Papiers du bateau',
  h1='Je vous préviens avant que les papiers de votre bateau expirent',
  meta='<span>Par Juan Morante</span><span>Vérifié le 3 novembre 2026</span>',
  lead='L’inspection, l’assurance ou les fusées expirent toujours au mauvais moment : à la station-service, lors d’un contrôle ou au moment de vendre le bateau. Laissez-moi la date et je vous écris un e-mail avant l’échéance. C’est gratuit et vous pouvez vous désinscrire quand vous voulez.',
  toc=[('como', 'Comment ça marche'), ('apunta', 'Indiquez vos dates'), ('que', 'Ce qui expire sur un bateau'), ('datos', 'Vos données')],
  como=['Choisissez ce qui expire et indiquez la date (jusqu’à quatre éléments à la fois).',
        'Je vous écris environ 60 jours avant, puis à 30, à 7 et le jour même.',
        'Si vous changez de bateau ou avez déjà renouvelé, répondez à l’e-mail et je mets à jour ou je supprime.'],
  aviso='Les rappels sont indicatifs : la date qui compte est celle de vos documents. Si vous ne savez pas si votre bateau doit passer l’ITB, voyez le <a href="/fr/guias/itb-inspeccion-tecnica-barcos-recreo">guide de l’ITB</a>.',
  que_intro='Ce que l’on oublie le plus, avec le délai habituel. Vérifiez toujours avec vos documents :',
  que=[('ITB (inspection espagnole)', 'tous les 5 ans maximum pour les bateaux de liste 7 de 6 à 24 m ; pour les autres, selon la liste et la longueur.'),
       ('Assurance responsabilité civile', 'à la fin de la police, en général chaque année.'),
       ('Certificat de navigabilité', 'la validité indiquée sur le certificat.'),
       ('Fusées, feux et fumigènes', 'la date de péremption de chaque unité.'),
       ('Extincteurs, radeau de survie et gilets gonflables', 'les révisions fixées par le fabricant et la réglementation.'),
       ('Permis bateau (carte espagnole)', 'renouvelé tous les 10 ans, et tous les 5 ans à partir de 70 ans.')],
  f=dict(n='Nom', e='E-mail', boat='Nom ou modèle du bateau', opt='(facultatif)', boatp='Jeanneau Cap Camarat 7.5, « Tramuntana »…',
         rows='Ce qui expire et quand', add='Ajouter une autre date', tipo='Ce qui expire', fecha='Date',
         tipos=['ITB (inspection)', 'Assurance', 'Certificat de navigabilité', 'Permis de navigation', 'Permis bateau (carte)', 'Radeau de survie', 'Extincteurs', 'Fusées / pyrotechnie', 'Balise de détresse', 'Autre'],
         ck1='Je veux recevoir par e-mail les rappels de ces dates. J’ai lu les informations sur la confidentialité.',
         ck2='Vous pouvez aussi m’envoyer de temps en temps des nouveautés de Plata Marine (guides et bateaux). Facultatif.',
         send='Activer mes rappels',
         legal='Responsable du traitement : Juan Morante (Plata Marine), juan@platamarine.com. Finalité : vous envoyer les rappels des dates indiquées et, uniquement si vous cochez la seconde case, des nouveautés de Plata Marine. Base juridique : votre consentement, que vous pouvez retirer à tout moment en répondant à un rappel ou en écrivant à juan@platamarine.com. Vos données ne sont pas cédées à des tiers. Conservation : jusqu’au passage de la dernière date indiquée ou jusqu’à votre désinscription. Droits : accès, rectification, effacement, opposition et les autres droits du RGPD ; vous pouvez aussi saisir l’autorité espagnole de protection des données (AEPD). Plus d’informations dans la <a href="/fr/privacidad">politique de confidentialité</a>.',
         req='Les champs marqués * sont obligatoires.'),
  datos='Je ne vous demande que le nécessaire pour vous prévenir : un e-mail et les dates. Le nom du bateau est facultatif. Je n’utilise pas ces données pour autre chose, sauf si vous cochez la case des nouveautés, et chaque rappel indique comment vous désinscrire.',
  wa_msg='Bonjour Juan, j’ai une question sur les papiers de mon bateau.',
  aside_e='Une question sur les papiers ?', aside_h='Je regarde sans engagement.', aside_p='ITB, changement de propriétaire, pavillon : dites-moi ce que vous avez et je vous dis ce qui s’applique.', aside_b='Écrire à Juan sur WhatsApp',
  toc_e='Sur cette page', rel_e='À lire aussi',
  rel=[('/fr/herramientas/libro-mantenimiento-barco', 'Carnet d’entretien (PDF)'), ('/fr/navegante/preparar-barco-fin-de-temporada', 'Hivernage du bateau'), ('/fr/guias/itb-inspeccion-tecnica-barcos-recreo', 'L’ITB expliquée'), ('/fr/servicios/', 'Services nautiques')],
 ),
}


def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')


def url(lang):
    return f'{BASE}{PRE[lang]}/{SLUG}/'


def main_html(L, t):
    f = t['f']
    wa = WA + urllib.parse.quote(t['wa_msg'])
    opts = ''.join(f'<option value="{k}">{n}</option>' for k, n in zip(TIPOS, f['tipos']))
    row = lambda i: (f'<div class="rc-row"{" hidden" if i else ""} data-row="{i}"><select name="tipo{i}" aria-label="{esc(f["tipo"])}"><option value="">{f["tipo"]}…</option>{opts}</select>'
                     f'<input type="date" name="fecha{i}" aria-label="{esc(f["fecha"])}"></div>')
    rows = ''.join(row(i) for i in range(4))
    form = (f'<style>.rc-row{{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:8px;margin:0 0 8px}}.rc-row select,.rc-row input{{width:100%;min-height:44px}}'
            f'.rc-add{{background:none;border:1px dashed var(--plata,#B7C3CB);border-radius:8px;padding:10px 14px;font:inherit;font-weight:600;color:var(--sea,#17465F);cursor:pointer;min-height:44px}}'
            f'@media (max-width:420px){{.rc-row{{grid-template-columns:minmax(0,1fr)}}}}.rc-row[hidden],.rc-add[hidden]{{display:none}}</style>'
            f'<div class="pm-amf" id="activar"><form id="pmRecordatorio" novalidate>'
            f'<div class="s2"><label>{f["rows"]} <i>*</i></label>{rows}<button type="button" class="rc-add">{f["add"]}</button></div>'
            f'<div><label for="rc_e">{f["e"]} <i>*</i></label><input id="rc_e" name="email" type="email" required autocomplete="email" maxlength="100"></div>'
            f'<div><label for="rc_n">{f["n"]} <small>{f["opt"]}</small></label><input id="rc_n" name="su_nombre" type="text" autocomplete="name" maxlength="60"></div>'
            f'<div class="s2"><label for="rc_b">{f["boat"]} <small>{f["opt"]}</small></label><input id="rc_b" name="barco" type="text" maxlength="100" placeholder="{esc(f["boatp"])}"></div>'
            f'<p class="help s2">{f["legal"]}</p>'
            f'<div class="s2"><label class="ck" for="rc_ok"><input id="rc_ok" name="privacidad" type="checkbox" required><span>{f["ck1"]}&nbsp;<i>*</i></span></label></div>'
            f'<div class="s2"><label class="ck" for="rc_nl"><input id="rc_nl" name="novedades" type="checkbox"><span>{f["ck2"]}</span></label></div>'
            f'<div class="s2"><button type="submit">{f["send"]}</button></div><p class="help s2">{f["req"]}</p>'
            f'<p class="pm-amst s2" role="status" aria-live="polite" hidden></p></form></div>')
    como = ''.join(f'<li>{x}</li>' for x in t['como'])
    que = ''.join(f'<li><b>{a}:</b> {b}</li>' for a, b in t['que'])
    toc = ''.join(f'<li><a href="#{i}">{n}</a></li>' for i, n in t['toc'])
    rel = ''.join(f'<a href="{u}">{n}</a>' for u, n in t['rel'])
    h = dict(t['toc'])
    return f'''<main class="art">
  <div class="wrap">
    <article>
      <header>
        <p class="eyebrow">{t["eyebrow"]}</p>
        <h1>{t["h1"]}</h1>
        <div class="meta">{t["meta"]}</div>
        <p class="lead">{t["lead"]}</p>
      </header>
      <div class="prose">
        <h2 id="como">{h["como"]}</h2>
        <ol>{como}</ol>
        <p class="muted" style="font-size:.9rem">{t["aviso"]}</p>
        <h2 id="apunta">{h["apunta"]}</h2>
        {form}
        <h2 id="que">{h["que"]}</h2>
        <p>{t["que_intro"]}</p>
        <ul>{que}</ul>
        <h2 id="datos">{h["datos"]}</h2>
        <p>{t["datos"]}</p>
      </div>
    </article>

    <aside class="aside" aria-label="{esc(t["aside_e"])}">
      <div class="card">
        <p class="eyebrow">{t["aside_e"]}</p>
        <h3>{t["aside_h"]}</h3>
        <p>{t["aside_p"]}</p>
        <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{t["aside_b"]}</a>
      </div>
      <nav class="toc" aria-label="{t["toc_e"]}">
        <p class="eyebrow">{t["toc_e"]}</p>
        <ol>{toc}</ol>
      </nav>
      <div class="rel">
        <p class="eyebrow">{t["rel_e"]}</p>{rel}
      </div>
    </aside>

  </div>
</main>'''


def build(L):
    t = T[L]
    root = ROOT / (PRE[L].lstrip('/') + '/' if PRE[L] else '')
    h = (root / 'servicios' / f'{SRC}.html').read_text(encoding='utf-8')
    full_title = f'{t["title"]} | Plata Marine' if len(t['title']) <= 46 else t['title']
    assert len(full_title) <= 60 and len(t['desc']) <= 155, (L, len(full_title), len(t['desc']))
    h = re.sub(r'<title>.*?</title>', f'<title>{full_title}</title>', h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(t["desc"])}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(full_title)}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(t["desc"])}">', h, count=1)
    for l2 in PRE:
        h = h.replace(f'{BASE}{PRE[l2]}/servicios/{SRC}"', f'{url(l2)}"')
    h = re.sub(r'<style>(?:\.dir[^\n]*\n)+', '<style>', h, count=1)
    wp = {"@context": "https://schema.org", "@type": "WebPage", "@id": url(L) + '#webpage', "url": url(L),
          "name": full_title, "description": t['desc'], "inLanguage": L, "dateModified": "2026-11-03",
          "isPartOf": {"@type": "WebSite", "name": "Plata Marine", "url": f'{BASE}/'},
          "publisher": {"@type": "Organization", "name": "Plata Marine", "url": f'{BASE}/', "logo": f'{BASE}/logo-plata-marine-1200.png', "email": "juan@platamarine.com"},
          "breadcrumb": {"@id": url(L) + '#breadcrumb'}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "@id": url(L) + '#breadcrumb', "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": f'{BASE}{PRE[L]}/'},
        {"@type": "ListItem", "position": 2, "name": t['crumb'], "item": url(L)}]}
    ld = ('<script type="application/ld+json">' + json.dumps(wp, ensure_ascii=False) + '</script>\n'
          '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + '</script>')
    h, n = re.subn(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>\s*<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>',
                   lambda m: ld, h, count=1, flags=re.S)
    assert n == 1
    h = re.sub(r'<main class="art">.*?</main>', lambda m: main_html(L, t), h, count=1, flags=re.S)
    h = re.sub(r'<script src="/servicios/tramites-forms\.js[^"]*" defer></script>', f'<script src="{JS}" defer></script>', h, count=1)
    h = re.sub(r'(<a class="btn btn-wa" href=")https://wa\.me/[^"]*(" target="_blank" rel="noopener">)', lambda m: m.group(1) + WA + urllib.parse.quote(t['wa_msg']) + m.group(2), h, count=1)
    assert SRC not in h and 'tramites-forms' not in h and 'FAQPage' not in h and JS in h
    out = root / SLUG / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(h, encoding='utf-8')
    return out


if __name__ == '__main__':
    for L in T:
        print(build(L))
