#!/usr/bin/env python3
"""Añade a la política de privacidad (ES/CA/EN/FR) el párrafo de solicitudes de visita y Google Calendar."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = {
 '': ('<p><strong>Barcos en colaboración con otros intermediarios.</strong>',
      '<p><strong>Solicitudes de visita.</strong> Si pides ver un barco desde la página de visitas, guardo tu nombre, teléfono, correo, el barco, el día y la hora y, si los escribes, tu titulación y tus notas, para organizar la visita. La solicitud se anota en mi hoja de visitas y en mi calendario de Google, y me llega un aviso por correo. Para cuadrarla le digo al propietario, o al intermediario que tenga el encargo, tu nombre y el día; nada más. Base legal: tu propia solicitud, como paso previo a una posible compra. Conservo estos datos hasta doce meses después de la visita, salvo que me pidas antes que los borre.</p>\n',
      ('Google Apps Script y Sheets para recibir y organizar las consultas', 'Google Apps Script, Sheets y Calendar para recibir y organizar las consultas y las visitas')),
 'ca/': ('<p><strong>Vaixells en col·laboració amb altres intermediaris.</strong>',
      '<p><strong>Sol·licituds de visita.</strong> Si demanes veure un vaixell des de la pàgina de visites, guardo el teu nom, telèfon, correu, el vaixell, el dia i l’hora i, si els escrius, la teva titulació i les teves notes, per organitzar la visita. La sol·licitud s’anota al meu full de visites i al meu calendari de Google, i m’arriba un avís per correu. Per quadrar-la li dic al propietari, o a l’intermediari que tingui l’encàrrec, el teu nom i el dia; res més. Base legal: la teva pròpia sol·licitud, com a pas previ a una possible compra. Conservo aquestes dades fins a dotze mesos després de la visita, tret que em demanis abans que les esborri.</p>\n',
      ('Google Apps Script i Sheets per rebre i organitzar les consultes', 'Google Apps Script, Sheets i Calendar per rebre i organitzar les consultes i les visites')),
 'en/': ('<p><strong>Boats offered together with other intermediaries.</strong>',
      '<p><strong>Viewing requests.</strong> If you ask to see a boat from the viewings page, I keep your name, phone number, email, the boat, the day and time and, if you provide them, your licence and notes, in order to arrange the viewing. The request is recorded in my viewings sheet and in my Google calendar, and I receive an email notice. To arrange it I tell the owner, or the intermediary holding the sale mandate, your name and the day; nothing else. Legal basis: your own request, as a step prior to a possible purchase. I keep this data for up to twelve months after the viewing, unless you ask me to delete it earlier.</p>\n',
      ('Google Apps Script and Sheets to receive and organise enquiries', 'Google Apps Script, Sheets and Calendar to receive and organise enquiries and viewings')),
 'fr/': ('<p><strong>Bateaux proposés en collaboration avec d’autres intermédiaires.</strong>',
      '<p><strong>Demandes de visite.</strong> Si vous demandez à voir un bateau depuis la page des visites, je conserve votre nom, votre téléphone, votre e-mail, le bateau, le jour et l’heure et, si vous les indiquez, votre permis et vos remarques, afin d’organiser la visite. La demande est enregistrée dans mon tableau des visites et dans mon agenda Google, et je reçois un avis par e-mail. Pour l’organiser, je communique au propriétaire, ou à l’intermédiaire qui a le mandat de vente, votre nom et le jour ; rien d’autre. Base juridique : votre propre demande, comme démarche préalable à un éventuel achat. Je conserve ces données jusqu’à douze mois après la visite, sauf si vous me demandez de les effacer avant.</p>\n',
      ('Google Apps Script et Sheets pour recevoir et organiser les demandes', 'Google Apps Script, Sheets et Calendar pour recevoir et organiser les demandes et les visites')),
}
for pre, (anchor, para, (old, new)) in P.items():
    f = os.path.join(ROOT, pre + 'privacidad.html'); s = open(f, encoding='utf-8').read()
    if para.split('</strong>')[0] in s: print('ya estaba', f); continue
    assert s.count(anchor) == 1 and s.count(old) == 1, f
    s = s.replace(anchor, para + anchor).replace(old, new)
    open(f, 'w', encoding='utf-8').write(s); print('ok', f)

# Presupuestos de traslado (10 oct 2026)
TR = {
 '': ('<p><strong>Solicitudes de visita.</strong>', '<p><strong>Presupuestos de traslado.</strong> Si desde la ficha de un barco me pides presupuesto para llevarlo por carretera o por mar, guardo tu nombre, teléfono, correo y el destino para pedir el presupuesto y enviártelo. A la empresa de transporte o al patrón solo le doy el barco y el destino; tus datos no, salvo que después me des permiso para poneros en contacto. Base legal: tu propia solicitud. Conservo estos datos hasta doce meses, salvo que me pidas antes que los borre.</p>\n'),
 'ca/': ('<p><strong>Sol·licituds de visita.</strong>', '<p><strong>Pressupostos de trasllat.</strong> Si des de la fitxa d’un vaixell em demanes pressupost per portar-lo per carretera o per mar, guardo el teu nom, telèfon, correu i la destinació per demanar el pressupost i enviar-te’l. A l’empresa de transport o al patró només li dono el vaixell i la destinació; les teves dades no, tret que després em donis permís per posar-vos en contacte. Base legal: la teva pròpia sol·licitud. Conservo aquestes dades fins a dotze mesos, tret que em demanis abans que les esborri.</p>\n'),
 'en/': ('<p><strong>Viewing requests.</strong>', '<p><strong>Delivery quotes.</strong> If you ask me from a boat page for a quote to move it by road or by sea, I keep your name, phone number, email and the destination in order to request the quote and send it to you. I only give the transport company or skipper the boat and the destination; not your details, unless you later allow me to put you in touch. Legal basis: your own request. I keep this data for up to twelve months, unless you ask me to delete it earlier.</p>\n'),
 'fr/': ('<p><strong>Demandes de visite.</strong>', '<p><strong>Devis de transport.</strong> Si, depuis la fiche d’un bateau, vous me demandez un devis pour l’acheminer par la route ou par la mer, je conserve votre nom, votre téléphone, votre e-mail et la destination afin de demander le devis et de vous l’envoyer. À l’entreprise de transport ou au skipper, je ne communique que le bateau et la destination ; pas vos données, sauf si vous m’autorisez ensuite à vous mettre en contact. Base juridique : votre propre demande. Je conserve ces données jusqu’à douze mois, sauf si vous me demandez de les effacer avant.</p>\n'),
}
for pre, (anchor, para) in TR.items():
    f = os.path.join(ROOT, pre + 'privacidad.html'); s = open(f, encoding='utf-8').read()
    if para.split('</strong>')[0] in s: print('ya estaba', f); continue
    assert s.count(anchor) == 1, f
    i = s.index(anchor); j = s.index('</p>', i) + len('</p>\n')
    s = s[:j] + para + s[j:]
    open(f, 'w', encoding='utf-8').write(s); print('ok traslado', f)
