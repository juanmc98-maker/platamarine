#!/usr/bin/env python3
"""Genera /visita/ (ES/CA/EN/FR) a partir de la cabecera y el pie de /alertas/ de cada idioma.
La página no se indexa (noindex) y no va al sitemap: es un paso del embudo, no contenido.
Uso: python3 _tools/build_visita.py"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """<style>.pmf{background:#fff;border:1px solid var(--plata);border-radius:8px;padding:22px 22px 18px;margin:0 0 22px}
.pmf h2{margin-top:0;font-size:1.15rem}
.pmf .row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.pmf .f{margin:0 0 12px}
.pmf label.l{display:block;font-family:var(--display);font-size:13px;font-weight:600;color:var(--ink-2);margin:0 0 5px}
.pmf input[type=text],.pmf input[type=email],.pmf input[type=tel],.pmf select,.pmf textarea{width:100%;font:16px var(--serif);padding:10px 12px;border:1px solid var(--plata-2);border-radius:6px;box-sizing:border-box;background:#fff;color:var(--ink)}
.pmf textarea{min-height:80px;resize:vertical}
.pmf label.chk{display:flex;gap:8px;align-items:flex-start;font-family:var(--display);font-size:13px;color:var(--ink-2);margin:0 0 8px;line-height:1.4}
.pmf .btn{cursor:pointer}
.pmf .msg{font-family:var(--display);font-size:13.5px;color:#c0392b;margin:8px 0 0}
.pmf .msg.ok{color:#2e8b57}
.pmf .legal{font-family:var(--display);font-size:11.5px;color:var(--ink-3,#7F929E);line-height:1.45;margin:12px 0 0}
.pmf .step{font-family:var(--display);font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-2);margin:18px 0 8px}
.pmf .step:first-child{margin-top:0}
.v-boat{font-family:var(--display);font-size:14.5px;margin:0 0 6px}
.v-link{background:none;border:0;padding:0;font:inherit;color:var(--ink-2);text-decoration:underline;cursor:pointer}
.v-sched{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:18px;align-items:start}
.v-cal-head{display:flex;align-items:center;justify-content:space-between;font-family:var(--display);font-size:15px;margin:0 0 8px}
.v-nav{width:34px;height:34px;border:1px solid var(--plata-2);border-radius:6px;background:#fff;font-size:18px;line-height:1;cursor:pointer;color:var(--ink)}
.v-nav:disabled{opacity:.3;cursor:default}
.v-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
.v-wd{font-family:var(--display);font-size:11.5px;font-weight:600;color:var(--ink-3,#7F929E);text-align:center;padding:2px 0}
.v-day{position:relative;aspect-ratio:1;min-height:36px;border:1px solid var(--plata-2);border-radius:6px;background:#fff;font-family:var(--display);font-size:14px;color:var(--ink);cursor:pointer}
.v-day.off{border-color:transparent;color:var(--ink-3,#9AA8B1);cursor:default;opacity:.45}
.v-day.req::after,.v-dot{content:"";display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--brass,#B58A2C)}
.v-day.req::after{position:absolute;left:50%;bottom:4px;margin-left:-2.5px}
.v-day.sel,.v-hour.sel{background:var(--ink);border-color:var(--ink);color:#fff}
.v-day:not(.off):hover,.v-hour:hover{border-color:var(--ink)}
.v-legend{font-family:var(--display);font-size:12px;color:var(--ink-2);margin:8px 0 0}
.v-hours{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.v-hour{padding:10px 0;border:1px solid var(--plata-2);border-radius:6px;background:#fff;font-family:var(--display);font-size:14.5px;color:var(--ink);cursor:pointer}
.v-hint{font-family:var(--display);font-size:13.5px;color:var(--ink-2);margin:0 0 10px}
.v-sum{font-family:var(--display);font-size:14px;font-weight:600;background:rgba(11,118,107,.08);border-radius:6px;padding:10px 12px;margin:14px 0 0}
.pmf button:focus-visible,.pmf select:focus-visible,.pmf input:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.steps{padding-left:20px}.steps li{margin:0 0 8px}
@media (max-width:640px){.pmf .row,.v-sched{grid-template-columns:1fr}}
"""

L = {
    'es': {
        'mailPh': 'tu@correo.com',
        'title': 'Solicitar visita · Plata Marine',
        'desc': 'Elige día y hora para ver el barco que te interesa. Lo cuadro con el propietario y te confirmo la visita por WhatsApp.',
        'eyebrow': 'Comprar · Visita',
        'h1': 'Solicita una visita para ver el barco',
        'meta': ['Gratis y sin compromiso', 'Te la confirmo por WhatsApp'],
        'lead': 'Elige el día y la hora que mejor te vengan. Antes de confirmártela la cuadro con el propietario, y te escribo por WhatsApp con el día, la hora y el punto de encuentro.',
        's1': '1. Barco', 'boatLabel': 'Barco que quieres ver', 's2': '2. Día y hora', 's3': '3. Tus datos',
        'name': 'Nombre *', 'namePh': 'Cómo te llamo', 'tel': 'Teléfono (WhatsApp) *', 'telPh': 'Con prefijo si no es de España',
        'mail': 'Correo *', 'tit': 'Titulación náutica <small>(opcional)</small>',
        'titOpts': ['Prefiero no decirlo', 'Aún no tengo', 'Licencia de Navegación', 'PNB', 'PER', 'Patrón de Yate', 'Capitán de Yate'],
        'notes': 'Algo que deba saber <small>(opcional)</small>', 'notesPh': 'Si vienes acompañado, si quieres probarlo en el agua, si financias…',
        'consent': '* Acepto que Plata Marine use estos datos para organizar la visita, según la <a href="{priv}" target="_blank" rel="noopener">política de privacidad</a>.',
        'news': 'Avísame también, de vez en cuando, de guías, novedades y alguna oferta de barcos en cartera de Plata Marine (nada de spam, baja cuando quieras).',
        'req': 'Los campos con * son obligatorios.', 'btn': 'Solicitar visita',
        'legal': 'Responsable: Juan Morante (Plata Marine), juan@platamarine.com. Finalidad: organizar la visita que pides y, solo si lo marcas, enviarte novedades de la web. Base legal: tu propia solicitud (pasos previos a una posible compra) y, para las novedades, tu consentimiento, que puedes retirar cuando quieras. Para organizar la visita le digo al propietario, o al intermediario que tenga el encargo, tu nombre y el día; nada más. Conservación: hasta doce meses después de la visita, salvo que me pidas antes que los borre. Derechos: acceso, rectificación, supresión, oposición y los demás que reconoce el RGPD, escribiendo a juan@platamarine.com; también puedes reclamar ante la AEPD. Más información en la <a href="{priv}" target="_blank" rel="noopener">política de privacidad</a>.',
        'alt': 'También puedes <a href="mailto:juan@platamarine.com">escribir a juan@platamarine.com</a>. Si no aparece una confirmación, consulta antes de volver a enviar.',
        'h2a': 'Cómo funciona',
        'steps': ['Eliges el barco, el día y la hora. Los domingos son bajo solicitud: me dices la franja y te propongo hora.',
                  'Lo cuadro con el propietario. Hasta entonces la visita queda pendiente.',
                  'Te escribo por WhatsApp para confirmarte día, hora y punto de encuentro. El puerto exacto te lo doy en ese momento, por la privacidad del propietario.'],
        'h2b': 'Antes de venir',
        'pb': 'Si es tu primer barco o dudas entre varios, te ayudará la guía de <a href="{pre}/guias/que-mirar-comprar-barco-segunda-mano.html">qué mirar al comprar de segunda mano</a>. Y si te surge algo, avísame por WhatsApp y movemos la visita sin problema.',
        'asideEy': '¿Prefieres escribirme?', 'asideH': 'Pídeme la visita por WhatsApp.', 'asideP': 'Dime qué barco quieres ver y qué días te van bien.',
        'asideBtn': 'Escribir a Juan por WhatsApp', 'asideWa': 'Hola Juan, me gustaría ver un barco. Barco:  | Días que me van bien: ',
        'rel': 'También te puede interesar', 'relLinks': [('/barcos/', 'Barcos en venta ahora'), ('/guias/que-mirar-comprar-barco-segunda-mano.html', 'Qué mirar al comprar de segunda mano'), ('/titulaciones/', 'Titulaciones náuticas')],
        'topWa': 'Hola Juan, me gustaría ver un barco.',
        'aside': 'Contacto y navegación', 'frNote': '',
    },
    'ca': {
        'mailPh': 'el.teu@correu.com',
        'title': 'Sol·licitar visita · Plata Marine',
        'desc': 'Tria dia i hora per veure el vaixell que t’interessa. Ho quadro amb el propietari i et confirmo la visita per WhatsApp.',
        'eyebrow': 'Comprar · Visita',
        'h1': 'Sol·licita una visita per veure el vaixell',
        'meta': ['Gratuït i sense compromís', 'Te la confirmo per WhatsApp'],
        'lead': 'Tria el dia i l’hora que et vagin millor. Abans de confirmar-te-la la quadro amb el propietari, i t’escric per WhatsApp amb el dia, l’hora i el punt de trobada.',
        's1': '1. Vaixell', 'boatLabel': 'Vaixell que vols veure', 's2': '2. Dia i hora', 's3': '3. Les teves dades',
        'name': 'Nom *', 'namePh': 'Com et dic', 'tel': 'Telèfon (WhatsApp) *', 'telPh': 'Amb prefix si no és d’Espanya',
        'mail': 'Correu *', 'tit': 'Titulació nàutica <small>(opcional)</small>',
        'titOpts': ['Prefereixo no dir-ho', 'Encara no en tinc', 'Llicència de Navegació', 'PNB', 'PER', 'Patró de Iot', 'Capità de Iot'],
        'notes': 'Alguna cosa que hagi de saber <small>(opcional)</small>', 'notesPh': 'Si vens acompanyat, si el vols provar a l’aigua, si finances…',
        'consent': '* Accepto que Plata Marine faci servir aquestes dades per organitzar la visita, segons la <a href="{priv}" target="_blank" rel="noopener">política de privacitat</a>.',
        'news': 'Avisa’m també, de tant en tant, de guies, novetats i alguna oferta de vaixells en cartera de Plata Marine (res de correu brossa, baixa quan vulguis).',
        'req': 'Els camps amb * són obligatoris.', 'btn': 'Sol·licitar visita',
        'legal': 'Responsable: Juan Morante (Plata Marine), juan@platamarine.com. Finalitat: organitzar la visita que demanes i, només si ho marques, enviar-te novetats del web. Base legal: la teva pròpia sol·licitud (passos previs a una possible compra) i, per a les novetats, el teu consentiment, que pots retirar quan vulguis. Per organitzar la visita li dic al propietari, o a l’intermediari que tingui l’encàrrec, el teu nom i el dia; res més. Conservació: fins a dotze mesos després de la visita, tret que em demanis abans que les esborri. Drets: accés, rectificació, supressió, oposició i els altres que reconeix el RGPD, escrivint a juan@platamarine.com; també pots reclamar davant l’AEPD. Més informació a la <a href="{priv}" target="_blank" rel="noopener">política de privacitat</a>.',
        'alt': 'També pots <a href="mailto:juan@platamarine.com">escriure a juan@platamarine.com</a>. Si no apareix una confirmació, consulta abans de tornar a enviar.',
        'h2a': 'Com funciona',
        'steps': ['Tries el vaixell, el dia i l’hora. Els diumenges són sota petició: em dius la franja i et proposo hora.',
                  'Ho quadro amb el propietari. Fins aleshores la visita queda pendent.',
                  'T’escric per WhatsApp per confirmar-te dia, hora i punt de trobada. El port exacte te’l dono en aquell moment, per la privacitat del propietari.'],
        'h2b': 'Abans de venir',
        'pb': 'Si és el teu primer vaixell o dubtes entre diversos, t’ajudarà la guia de <a href="{pre}/guias/que-mirar-comprar-barco-segunda-mano.html">què mirar en comprar de segona mà</a>. I si et sorgeix alguna cosa, avisa’m per WhatsApp i movem la visita sense problema.',
        'asideEy': 'Prefereixes escriure’m?', 'asideH': 'Demana’m la visita per WhatsApp.', 'asideP': 'Digues-me quin vaixell vols veure i quins dies et van bé.',
        'asideBtn': 'Escriure a Juan per WhatsApp', 'asideWa': 'Hola Juan, m’agradaria veure un vaixell. Vaixell:  | Dies que em van bé: ',
        'rel': 'També et pot interessar', 'relLinks': [('/barcos/', 'Vaixells en venda ara'), ('/guias/que-mirar-comprar-barco-segunda-mano.html', 'Què mirar en comprar de segona mà'), ('/titulaciones/', 'Titulacions nàutiques')],
        'topWa': 'Hola Juan, m’agradaria veure un vaixell.',
        'aside': 'Contacte i navegació', 'frNote': '',
    },
    'en': {
        'mailPh': 'you@email.com',
        'title': 'Book a viewing · Plata Marine',
        'desc': 'Choose a day and time to see the boat you are interested in. I arrange it with the owner and confirm the viewing on WhatsApp.',
        'eyebrow': 'Buy · Viewing',
        'h1': 'Request a viewing of the boat',
        'meta': ['Free, no obligation', 'Confirmed on WhatsApp'],
        'lead': 'Choose the day and time that suit you best. Before confirming, I arrange it with the owner, then I message you on WhatsApp with the day, time and meeting point.',
        's1': '1. Boat', 'boatLabel': 'Boat you want to see', 's2': '2. Day and time', 's3': '3. Your details',
        'name': 'Name *', 'namePh': 'Your name', 'tel': 'Phone (WhatsApp) *', 'telPh': 'With country code if not Spanish',
        'mail': 'Email *', 'tit': 'Boating licence <small>(optional)</small>',
        'titOpts': ['Prefer not to say', 'None yet', 'Licencia de Navegación (Spanish basic licence)', 'PNB', 'PER', 'Patrón de Yate', 'Capitán de Yate', 'ICC or licence from another country'],
        'notes': 'Anything I should know <small>(optional)</small>', 'notesPh': 'If someone is coming with you, if you would like a sea trial, if you need financing…',
        'consent': '* I agree that Plata Marine may use these details to arrange the viewing, as set out in the <a href="{priv}" target="_blank" rel="noopener">privacy policy</a>.',
        'news': 'Also let me know, from time to time, about guides, news and boats for sale at Plata Marine (no spam, unsubscribe any time).',
        'req': 'Fields marked * are required.', 'btn': 'Request viewing',
        'legal': 'Controller: Juan Morante (Plata Marine), juan@platamarine.com. Purpose: arranging the viewing you request and, only if you tick the box, sending you news from the website. Legal basis: your own request (steps prior to a possible purchase) and, for news, your consent, which you can withdraw at any time. To arrange the viewing I tell the owner, or the intermediary holding the sale mandate, your name and the day; nothing else. Retention: up to twelve months after the viewing, unless you ask me to delete it earlier. Rights: access, rectification, erasure, objection and the other rights under the GDPR, by writing to juan@platamarine.com; you may also complain to the Spanish Data Protection Agency (AEPD). More information in the <a href="{priv}" target="_blank" rel="noopener">privacy policy</a>.',
        'alt': 'You can also <a href="mailto:juan@platamarine.com">write to juan@platamarine.com</a>. If no confirmation appears, please check before sending again.',
        'h2a': 'How it works',
        'steps': ['You choose the boat, the day and the time. Sundays are on request: tell me the time of day and I will suggest a time.',
                  'I arrange it with the owner. Until then, the viewing stays pending.',
                  'I message you on WhatsApp to confirm the day, time and meeting point. I give you the exact marina at that point, to protect the owner’s privacy.'],
        'h2b': 'Before you come',
        'pb': 'If it is your first boat or you are deciding between several, the guide on <a href="{pre}/guias/que-mirar-comprar-barco-segunda-mano.html">what to check when buying second-hand</a> will help. And if something comes up, just tell me on WhatsApp and we will move the viewing.',
        'asideEy': 'Prefer to message me?', 'asideH': 'Ask for the viewing on WhatsApp.', 'asideP': 'Tell me which boat you want to see and which days suit you.',
        'asideBtn': 'Message Juan on WhatsApp', 'asideWa': "Hi Juan, I'd like to see a boat. Boat:  | Days that suit me: ",
        'rel': 'You may also like', 'relLinks': [('/barcos/', 'Boats for sale now'), ('/guias/que-mirar-comprar-barco-segunda-mano.html', 'What to check when buying second-hand'), ('/titulaciones/', 'Boating licences')],
        'topWa': "Hi Juan, I'd like to see a boat.",
        'aside': 'Contact and navigation', 'frNote': '',
    },
    'fr': {
        'mailPh': 'vous@email.fr',
        'title': 'Demander une visite · Plata Marine',
        'desc': 'Choisissez le jour et l’heure pour voir le bateau qui vous intéresse. Je l’organise avec le propriétaire et je vous confirme la visite sur WhatsApp.',
        'eyebrow': 'Acheter · Visite',
        'h1': 'Demandez une visite du bateau',
        'meta': ['Gratuit et sans engagement', 'Confirmée sur WhatsApp'],
        'lead': 'Choisissez le jour et l’heure qui vous conviennent. Avant de vous la confirmer, je l’organise avec le propriétaire, puis je vous écris sur WhatsApp avec le jour, l’heure et le point de rendez-vous.',
        's1': '1. Bateau', 'boatLabel': 'Bateau que vous voulez voir', 's2': '2. Jour et heure', 's3': '3. Vos coordonnées',
        'name': 'Nom *', 'namePh': 'Votre nom', 'tel': 'Téléphone (WhatsApp) *', 'telPh': 'Avec l’indicatif, par exemple +33',
        'mail': 'E-mail *', 'tit': 'Permis bateau <small>(facultatif)</small>',
        'titOpts': ['Je préfère ne pas le dire', 'Pas encore', 'Permis côtier', 'Permis hauturier', 'Licence espagnole (Licencia de Navegación, PNB, PER…)', 'Autre permis'],
        'notes': 'Quelque chose à savoir <small>(facultatif)</small>', 'notesPh': 'Si vous venez accompagné, si vous voulez un essai en mer, si vous financez…',
        'consent': '* J’accepte que Plata Marine utilise ces données pour organiser la visite, conformément à la <a href="{priv}" target="_blank" rel="noopener">politique de confidentialité</a>.',
        'news': 'Prévenez-moi aussi, de temps en temps, des guides, nouveautés et bateaux en vente chez Plata Marine (pas de spam, désinscription à tout moment).',
        'req': 'Les champs marqués * sont obligatoires.', 'btn': 'Demander la visite',
        'legal': 'Responsable : Juan Morante (Plata Marine), juan@platamarine.com. Finalité : organiser la visite que vous demandez et, seulement si vous cochez la case, vous envoyer les nouveautés du site. Base juridique : votre propre demande (démarches préalables à un éventuel achat) et, pour les nouveautés, votre consentement, que vous pouvez retirer à tout moment. Pour organiser la visite, je communique au propriétaire, ou à l’intermédiaire qui a le mandat de vente, votre nom et le jour ; rien d’autre. Conservation : jusqu’à douze mois après la visite, sauf si vous me demandez de les effacer avant. Droits : accès, rectification, effacement, opposition et les autres droits prévus par le RGPD, en écrivant à juan@platamarine.com ; vous pouvez aussi saisir l’autorité espagnole de protection des données (AEPD). Plus d’informations dans la <a href="{priv}" target="_blank" rel="noopener">politique de confidentialité</a>.',
        'alt': 'Vous pouvez aussi <a href="mailto:juan@platamarine.com">écrire à juan@platamarine.com</a>. Si aucune confirmation n’apparaît, vérifiez avant de renvoyer.',
        'h2a': 'Comment ça marche',
        'steps': ['Vous choisissez le bateau, le jour et l’heure. Le dimanche, c’est sur demande : indiquez-moi le moment et je vous propose une heure.',
                  'Je l’organise avec le propriétaire. En attendant, la visite reste en attente.',
                  'Je vous écris sur WhatsApp pour confirmer le jour, l’heure et le point de rendez-vous. Le port exact, je vous le donne à ce moment-là, par respect pour la vie privée du propriétaire.'],
        'h2b': 'Avant de venir',
        'pb': 'Si c’est votre premier bateau ou si vous hésitez entre plusieurs, le guide <a href="{pre}/guias/que-mirar-comprar-barco-segunda-mano.html">que vérifier avant d’acheter d’occasion</a> vous aidera. Et en cas d’imprévu, prévenez-moi sur WhatsApp et nous déplacerons la visite.',
        'asideEy': 'Vous préférez m’écrire ?', 'asideH': 'Demandez la visite sur WhatsApp.', 'asideP': 'Dites-moi quel bateau vous voulez voir et quels jours vous conviennent.',
        'asideBtn': 'Écrire à Juan sur WhatsApp', 'asideWa': 'Bonjour Juan, j’aimerais voir un bateau. Bateau :  | Jours qui me conviennent : ',
        'rel': 'À voir aussi', 'relLinks': [('/barcos/', 'Bateaux à vendre'), ('/guias/que-mirar-comprar-barco-segunda-mano.html', 'Que vérifier avant d’acheter d’occasion'), ('/titulaciones/', 'Permis bateau')],
        'topWa': 'Bonjour Juan, j’aimerais voir un bateau.',
        'aside': 'Contact et navigation',
        'frNote': '<p class="legal">Je ne parle pas français : je vous répondrai avec l’aide d’un traducteur.</p>',
    },
}


def wa(text):
    from urllib.parse import quote
    return 'https://wa.me/34633742973?text=' + quote(text, safe='')


def main_html(lang, t):
    pre = '' if lang == 'es' else '/' + lang
    priv = pre + '/privacidad.html'
    tit = ''.join('<option value="%s">%s</option>' % ('' if i == 0 else o, o) for i, o in enumerate(t['titOpts']))
    steps = ''.join('<li>%s</li>' % s for s in t['steps'])
    rel = ''.join('<a href="%s%s">%s</a>' % (pre, h, n) for h, n in t['relLinks'])
    return f'''<main class="art">
  <div class="wrap">
    <article>
      <header>
        <p class="eyebrow">{t['eyebrow']}</p>
        <h1>{t['h1']}</h1>
        <div class="meta"><span>{t['meta'][0]}</span><span>{t['meta'][1]}</span></div>
        <p class="lead">{t['lead']}</p>
      </header>

      <div class="prose">
        <div class="pmf">
          <form id="visitaForm" novalidate>
            <p class="step">{t['s1']}</p>
            <div class="f" id="v-barco-box" data-label="{t['boatLabel']}"></div>
            <p class="step">{t['s2']}</p>
            <div class="v-sched">
              <div id="v-cal"></div>
              <div id="v-horas"></div>
            </div>
            <p class="v-sum" id="v-resumen" hidden></p>
            <p class="step">{t['s3']}</p>
            <div class="row">
              <div class="f"><label class="l" for="v-nombre">{t['name']}</label><input type="text" name="nombre" id="v-nombre" autocomplete="name" placeholder="{t['namePh']}" required maxlength="80"></div>
              <div class="f"><label class="l" for="v-tel">{t['tel']}</label><input type="tel" name="telefono" id="v-tel" autocomplete="tel" placeholder="{t['telPh']}" required inputmode="tel" maxlength="20"></div>
            </div>
            <div class="row">
              <div class="f"><label class="l" for="v-email">{t['mail']}</label><input type="email" name="email" id="v-email" autocomplete="email" placeholder="{t['mailPh']}" maxlength="120" required></div>
              <div class="f"><label class="l" for="v-tit">{t['tit']}</label><select name="titulacion" id="v-tit">{tit}</select></div>
            </div>
            <div class="f"><label class="l" for="v-notas">{t['notes']}</label><textarea name="notas" id="v-notas" maxlength="600" placeholder="{t['notesPh']}"></textarea></div>
            <label class="chk"><input type="checkbox" name="consent" required> <span>{t['consent'].format(priv=priv)}</span></label>
            <label class="chk"><input type="checkbox" name="newsletter"> <span>{t['news']}</span></label>
            <p class="legal req-note">{t['req']}</p>
            <button type="submit" class="btn btn-wa">{t['btn']}</button>
            <p class="msg" role="status" aria-live="polite"></p>
            <p class="legal">{t['legal'].format(priv=priv)}</p>
            <p class="legal">{t['alt']}</p>{t['frNote']}
          </form>
        </div>

        <h2 id="como">{t['h2a']}</h2>
        <ol class="steps">{steps}</ol>
        <h2 id="antes">{t['h2b']}</h2>
        <p>{t['pb'].format(pre=pre)}</p>
      </div>
    </article>

    <aside class="aside" aria-label="{t['aside']}">
      <div class="card">
        <p class="eyebrow">{t['asideEy']}</p>
        <h3>{t['asideH']}</h3>
        <p>{t['asideP']}</p>
        <a class="btn btn-wa" href="{wa(t['asideWa'])}" target="_blank" rel="noopener">{t['asideBtn']}</a>
      </div>
      <div class="rel">
        <p class="eyebrow">{t['rel']}</p>
        {rel}
      </div>
    </aside>

  </div>
</main>
'''


def build(lang):
    pre = '' if lang == 'es' else lang + '/'
    src = open(os.path.join(ROOT, pre + 'alertas/index.html'), encoding='utf-8').read()
    t = L[lang]
    s = src
    # cabecera <head>
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % t['title'], s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">\n<meta name="robots" content="noindex, follow">' % t['desc'], s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % t['title'].split(' · ')[0], s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % t['desc'], s, count=1)
    s = s.replace('platamarine.com/alertas/', 'platamarine.com/visita/')
    for l2 in ('ca', 'en', 'fr'):
        s = s.replace('platamarine.com/%s/alertas/' % l2, 'platamarine.com/%s/visita/' % l2)
    # estilos propios de la página
    s = re.sub(r'<style>\.pmf\{.*?\.disc p\{margin:0\}\n@media \(max-width:640px\)\{\.pmf \.row\{grid-template-columns:1fr\}\}\n', CSS, s, count=1, flags=re.S)
    assert '.v-grid' in s, lang + ': no se encontró el bloque de estilos'
    # menú: la página de alertas ya no es la actual
    s = re.sub(r'(<a href="[^"]*/alertas/") aria-current="page"', r'\1', s)
    s = s.replace('pmx-dd pmx-res cur"', 'pmx-dd pmx-res"')
    # botón de WhatsApp de la cabecera
    s = re.sub(r'(<a class="btn btn-wa" href=")https://wa\.me/34633742973\?text=[^"]*(" target="_blank" rel="noopener">)',
               lambda m: m.group(1) + wa(t['topWa']) + m.group(2), s, count=1)
    # contenido
    a, b = s.index('<main class="art">'), s.index('<footer class="foot">')
    s = s[:a] + main_html(lang, t) + '\n' + s[b:]
    s = s.replace('<script src="/alertas-contexto.js?v=20261006"></script>', '<script src="/visita/visita.js?v=20261010" defer></script>')
    s = s.replace('<script src="/inventario.js?v=20261006"></script>', '<script src="/inventario.js?v=20261006" defer></script>')
    assert 'visita.js' in s and 'alertas' not in s.split('<main')[0].split('<header class="top">')[0], lang
    out = os.path.join(ROOT, pre + 'visita/index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(s)
    print('ok', out)


if __name__ == '__main__':
    for lang in ('es', 'ca', 'en', 'fr'):
        build(lang)
