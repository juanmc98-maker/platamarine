#!/usr/bin/env python3
"""Libro de mantenimiento del barco (PDF A4 para imprimir y rellenar a mano) y su página de descarga.

Uso:  PM_ROOT=<repo> python3 _tools/build_libro_mantenimiento.py [pdf] [pages]
      (sin argumentos hace las dos cosas)
Salida:
  herramientas/libro-mantenimiento-barco.pdf  (ES) y -ca / -en / -fr .pdf
  herramientas/libro-mantenimiento-barco.html (ES) y ca/ en/ fr/herramientas/...
Las páginas copian cabecera, menú y pie de herramientas/coste-mantener-barco.html de cada idioma.
"""
import asyncio, base64, html, io, json, os, re, sys

ROOT = os.environ.get('PM_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'libro-mantenimiento-barco'
SITE = 'https://www.platamarine.com'
PHONE = '+34 633 742 973'
PRE = {'es': '', 'ca': 'ca/', 'en': 'en/', 'fr': 'fr/'}
PDFNAME = {'es': SLUG + '.pdf', 'ca': SLUG + '-ca.pdf', 'en': SLUG + '-en.pdf', 'fr': SLUG + '-fr.pdf'}

# ---------------------------------------------------------------- textos del PDF
T = {
'es': dict(
  title='Libro de mantenimiento del barco', h1='Libro de mantenimiento', sub='del barco',
  intro='Para apuntar todo lo que se le hace al barco: revisiones, reparaciones, varadas y documentos. Con fecha, horas de motor y número de factura.',
  fields=[('Nombre del barco', 2), ('Marca y modelo', 2), ('Año', 1), ('Matrícula', 1), ('Eslora', 1), ('Puerto base', 1),
          ('Motor 1 · marca y modelo', 1), ('Nº de serie', 1), ('Motor 2 · marca y modelo', 1), ('Nº de serie', 1),
          ('Horas de motor al empezar este libro', 2)],
  howh='Cómo usarlo',
  how=['Apunta cada trabajo el mismo día, aunque lo hagas tú.',
       'Numera las facturas y guárdalas en una carpeta con el mismo número que pones aquí.',
       'Haz una foto de cada página cuando la llenes: si el libro se moja o se pierde, no pierdes el historial.'],
  docs='Datos y documentos', docs_cols=['Documento o equipo', 'Fecha', 'Caduca', 'Notas'],
  docs_rows=[('Permiso de navegación', ''), ('Certificado de navegabilidad', ''),
             ('ITB', 'Fecha: última inspección · Caduca: próxima'),
             ('Seguro', 'Compañía: ______________  Póliza nº: ______________'),
             ('Balsa salvavidas', 'Revisión'), ('Extintores', 'Revisión'), ('Bengalas y señales pirotécnicas', ''),
             ('Radiobaliza (EPIRB)', 'Batería y zafa hidrostática'), ('Licencia de radio (MMSI)', ''), ('', ''), ('', '')],
  contacts='Contactos útiles', contacts_cols=['', 'Nombre', 'Teléfono'],
  contacts_rows=['Mecánico', 'Varadero', 'Marina / amarre', 'Asistencia del seguro', 'Otro'],
  eng='Registro de motor', eng_note='Marca lo que se ha hecho. Los intervalos de cada trabajo los indica el manual de tu motor.',
  eng_cols=['Fecha', 'Horas', 'Motor', 'Trabajo hecho', 'Taller', 'Coste', 'Factura nº'],
  eng_items=['Aceite y filtro', 'Filtro gasoil / decantador', 'Rodete', 'Ánodos', 'Aceite de cola', 'Correas', 'Bujías'],
  other='Otro', cont='(continuación)',
  hull='Casco y equipos', hull_ref='Datos de referencia',
  hull_refs=['Antifouling (marca y color)', 'Baterías (tipo, Ah y fecha de compra)', 'Hélice (diámetro × paso)', 'Ánodos (cantidad y tipo)'],
  hull_cols=['Fecha', 'Elemento', 'Detalle de lo hecho', 'Taller', 'Coste', 'Factura nº'],
  hull_items=['Antifouling', 'Ánodos', 'Pasacascos', 'Hélice', 'Baterías', 'Bombas de achique', 'Electrónica', 'Jarcia (velero)', 'Winches (velero)'],
  win='Invernaje y botadura', win_note='Cada vez que el barco sale o vuelve al agua, o se prepara para pasar el invierno.',
  win_cols=['Fecha', 'Situación', 'Dónde', 'Lo hecho', 'Notas'], win_state=['En agua', 'En seco'],
  win_items=['Motor invernado', 'Circuito con agua dulce / anticongelante', 'Depósito lleno con aditivo', 'Baterías cargadas o desconectadas',
             'Velas, lonas y cojines fuera', 'Sentina limpia y seca', 'Limpieza de casco / antifouling'],
  win_guide='Lista completa para el fin de temporada: ',
  sell='Cuando vendas el barco',
  sell_intro='Lo primero que pide un comprador serio es ver los papeles y saber qué se le ha hecho al barco. Tenerlo todo junto y en orden ahorra muchas preguntas.',
  sell_items=['Hoja de asiento actualizada, sin cargas', 'Permiso de navegación', 'Certificado de navegabilidad y última ITB',
              'Recibo del seguro en vigor', 'Facturas de compra y de reparaciones, ordenadas por fecha', 'Este libro de mantenimiento',
              'Manuales del barco, del motor y de la electrónica', 'Declaración de conformidad CE, si la tiene',
              'Revisiones de la balsa, los extintores y la radiobaliza', 'Justificante del impuesto pagado al comprarlo (ITP o IVA)',
              'Llaves, duplicados y códigos (contacto, candados, electrónica)'],
  sell_quote='Un historial claro da confianza al comprador: ve qué se ha hecho, cuándo y quién lo hizo, y llega a la visita con menos dudas.',
  sell_juan='Si algún día lo vendes y te puedo echar una mano, escríbeme. — Juan Morante',
  notes='Notas'),
'ca': dict(
  title='Llibre de manteniment del vaixell', h1='Llibre de manteniment', sub='del vaixell',
  intro='Per apuntar tot el que es fa al vaixell: revisions, reparacions, varades i documents. Amb data, hores de motor i número de factura.',
  fields=[('Nom del vaixell', 2), ('Marca i model', 2), ('Any', 1), ('Matrícula', 1), ('Eslora', 1), ('Port base', 1),
          ('Motor 1 · marca i model', 1), ('Núm. de sèrie', 1), ('Motor 2 · marca i model', 1), ('Núm. de sèrie', 1),
          ("Hores de motor en començar aquest llibre", 2)],
  howh='Com fer-lo servir',
  how=["Apunta cada feina el mateix dia, encara que la facis tu.",
       "Numera les factures i guarda-les en una carpeta amb el mateix número que poses aquí.",
       "Fes una foto de cada pàgina quan l'omplis: si el llibre es mulla o es perd, no perds l'historial."],
  docs='Dades i documents', docs_cols=['Document o equip', 'Data', 'Caduca', 'Notes'],
  docs_rows=[('Permís de navegació', ''), ('Certificat de navegabilitat', ''),
             ('ITB', 'Data: última inspecció · Caduca: propera'),
             ('Assegurança', 'Companyia: ______________  Pòlissa núm.: ____________'),
             ('Balsa salvavides', 'Revisió'), ('Extintors', 'Revisió'), ('Bengales i senyals pirotècnics', ''),
             ('Radiobalisa (EPIRB)', 'Bateria i alliberament hidrostàtic'), ('Llicència de ràdio (MMSI)', ''), ('', ''), ('', '')],
  contacts='Contactes útils', contacts_cols=['', 'Nom', 'Telèfon'],
  contacts_rows=['Mecànic', 'Varador', 'Port / amarratge', "Assistència de l'assegurança", 'Altres'],
  eng='Registre de motor', eng_note="Marca el que s'ha fet. Els intervals de cada feina els indica el manual del teu motor.",
  eng_cols=['Data', 'Hores', 'Motor', 'Feina feta', 'Taller', 'Cost', 'Factura núm.'],
  eng_items=['Oli i filtre', 'Filtre gasoil / decantador', 'Rodet', 'Ànodes', 'Oli de cua', 'Corretges', 'Bugies'],
  other='Altres', cont='(continuació)',
  hull='Casc i equips', hull_ref='Dades de referència',
  hull_refs=['Antifouling (marca i color)', 'Bateries (tipus, Ah i data de compra)', 'Hèlix (diàmetre × pas)', 'Ànodes (quantitat i tipus)'],
  hull_cols=['Data', 'Element', 'Detall del que s’ha fet', 'Taller', 'Cost', 'Factura núm.'],
  hull_items=['Antifouling', 'Ànodes', 'Passacascs', 'Hèlix', 'Bateries', 'Bombes de sentina', 'Electrònica', 'Eixàrcia (velers)', 'Winches (velers)'],
  win='Hivernada i botada', win_note="Cada cop que el vaixell surt de l'aigua o hi torna, o es prepara per passar l'hivern.",
  win_cols=['Data', 'Situació', 'On', 'El que s’ha fet', 'Notes'], win_state=["A l'aigua", 'En sec'],
  win_items=['Motor hivernat', "Circuit amb aigua dolça / anticongelant", 'Dipòsit ple amb additiu', 'Bateries carregades o desconnectades',
             'Veles, lones i coixins fora', 'Sentina neta i seca', 'Neteja de casc / antifouling'],
  win_guide='Llista completa per al final de temporada: ',
  sell='Quan venguis el vaixell',
  sell_intro="El primer que demana un comprador seriós és veure els papers i saber què s'ha fet al vaixell. Tenir-ho tot junt i en ordre estalvia moltes preguntes.",
  sell_items=["Full d'assentament actualitzat, sense càrregues", 'Permís de navegació', 'Certificat de navegabilitat i última ITB',
              "Rebut de l'assegurança en vigor", 'Factures de compra i de reparacions, ordenades per data', 'Aquest llibre de manteniment',
              "Manuals del vaixell, del motor i de l'electrònica", 'Declaració de conformitat CE, si en té',
              'Revisions de la balsa, els extintors i la radiobalisa', "Justificant de l'impost pagat en comprar-lo (ITP o IVA)",
              'Claus, duplicats i codis (contacte, cadenats, electrònica)'],
  sell_quote="Un historial clar dona confiança al comprador: veu què s'ha fet, quan i qui ho va fer, i arriba a la visita amb menys dubtes.",
  sell_juan="Si algun dia el vens i et puc donar un cop de mà, escriu-me. — Juan Morante",
  notes='Notes'),
'en': dict(
  title='Boat maintenance log', h1='Maintenance log', sub='for your boat',
  intro='A place to write down everything done to the boat: services, repairs, haul-outs and documents. With the date, engine hours and invoice number.',
  fields=[('Boat name', 2), ('Make and model', 2), ('Year', 1), ('Registration', 1), ('Length', 1), ('Home port', 1),
          ('Engine 1 · make and model', 1), ('Serial no.', 1), ('Engine 2 · make and model', 1), ('Serial no.', 1),
          ('Engine hours when this log was started', 2)],
  howh='How to use it',
  how=['Write each job down on the day it is done, even if you did it yourself.',
       'Number your invoices and keep them in a folder with the same number you write here.',
       'Take a photo of each page once it is full: if the log gets wet or lost, you keep the history.'],
  docs='Details and documents', docs_cols=['Document or equipment', 'Date', 'Expires', 'Notes'],
  docs_rows=[('Navigation permit', ''), ('Certificate of seaworthiness', ''),
             ('ITB (technical inspection)', 'Date: last inspection · Expires: next one'),
             ('Insurance', 'Company: ______________  Policy no.: ______________'),
             ('Liferaft', 'Service'), ('Fire extinguishers', 'Service'), ('Flares and pyrotechnics', ''),
             ('EPIRB', 'Battery and hydrostatic release'), ('Radio licence (MMSI)', ''), ('', ''), ('', '')],
  contacts='Useful contacts', contacts_cols=['', 'Name', 'Phone'],
  contacts_rows=['Mechanic', 'Boatyard', 'Marina / berth', 'Insurance assistance', 'Other'],
  eng='Engine log', eng_note='Tick what was done. Your engine manual gives the service interval for each job.',
  eng_cols=['Date', 'Hours', 'Engine', 'Work done', 'Workshop', 'Cost', 'Invoice no.'],
  eng_items=['Oil and filter', 'Fuel filter / water separator', 'Impeller', 'Anodes', 'Gear oil (leg / drive)', 'Belts', 'Spark plugs'],
  other='Other', cont='(continued)',
  hull='Hull and equipment', hull_ref='Reference details',
  hull_refs=['Antifouling (brand and colour)', 'Batteries (type, Ah and purchase date)', 'Propeller (diameter × pitch)', 'Anodes (number and type)'],
  hull_cols=['Date', 'Item', 'Details of the work', 'Workshop', 'Cost', 'Invoice no.'],
  hull_items=['Antifouling', 'Anodes', 'Through-hulls', 'Propeller', 'Batteries', 'Bilge pumps', 'Electronics', 'Rigging (sailboat)', 'Winches (sailboat)'],
  win='Laying up and launching', win_note='Every time the boat comes out of the water or goes back in, or is prepared for the winter.',
  win_cols=['Date', 'Status', 'Where', 'Work done', 'Notes'], win_state=['Afloat', 'Ashore'],
  win_items=['Engine winterised', 'Cooling circuit flushed / antifreeze', 'Tank filled with additive', 'Batteries charged or disconnected',
             'Sails, covers and cushions removed', 'Bilge clean and dry', 'Hull cleaned / antifouling'],
  win_guide='Full end-of-season checklist: ',
  sell='When you sell the boat',
  sell_intro='The first thing a serious buyer asks for is the paperwork and what has been done to the boat. Having it all together and in order saves a lot of questions.',
  sell_items=['Up-to-date registry sheet (hoja de asiento), free of charges', 'Navigation permit', 'Certificate of seaworthiness and last ITB',
              'Current insurance receipt', 'Purchase and repair invoices, in date order', 'This maintenance log',
              'Manuals for the boat, engine and electronics', 'CE declaration of conformity, if it has one',
              'Liferaft, fire extinguisher and EPIRB service records', 'Proof of the tax paid when you bought it (ITP or VAT)',
              'Keys, spares and codes (ignition, padlocks, electronics)'],
  sell_quote='A clear history gives the buyer confidence: they can see what was done, when and by whom, and they come to the viewing with fewer doubts.',
  sell_juan='If you ever sell it and I can help, just get in touch. — Juan Morante',
  notes='Notes'),
'fr': dict(
  title="Carnet d'entretien du bateau", h1="Carnet d'entretien", sub='du bateau',
  intro="Pour noter tout ce qui est fait sur le bateau : révisions, réparations, carénages et documents. Avec la date, les heures moteur et le numéro de facture.",
  fields=[('Nom du bateau', 2), ('Marque et modèle', 2), ('Année', 1), ('Immatriculation', 1), ('Longueur', 1), ("Port d'attache", 1),
          ('Moteur 1 · marque et modèle', 1), ('N° de série', 1), ('Moteur 2 · marque et modèle', 1), ('N° de série', 1),
          ('Heures moteur au début de ce carnet', 2)],
  howh='Comment l’utiliser',
  how=['Notez chaque intervention le jour même, même si vous la faites vous-même.',
       'Numérotez les factures et rangez-les dans un classeur avec le même numéro que celui noté ici.',
       'Prenez chaque page en photo une fois remplie : si le carnet est mouillé ou perdu, vous gardez l’historique.'],
  docs='Données et documents', docs_cols=['Document ou équipement', 'Date', 'Expire le', 'Notes'],
  docs_rows=[('Titre / permis de navigation', ''), ('Certificat de navigabilité', ''),
             ('ITB (inspection technique)', 'Date : dernière inspection · Expire : prochaine'),
             ('Assurance', 'Compagnie : ____________  Police n° : ____________'),
             ('Radeau de survie', 'Révision'), ('Extincteurs', 'Révision'), ('Feux à main et fusées', ''),
             ('Balise de détresse (EPIRB)', 'Batterie et largueur hydrostatique'), ('Licence radio (MMSI)', ''), ('', ''), ('', '')],
  contacts='Contacts utiles', contacts_cols=['', 'Nom', 'Téléphone'],
  contacts_rows=['Mécanicien', 'Chantier / port à sec', 'Port / place', "Assistance de l'assurance", 'Autre'],
  eng='Suivi moteur', eng_note="Cochez ce qui a été fait. Les intervalles de chaque opération figurent dans le manuel de votre moteur.",
  eng_cols=['Date', 'Heures', 'Moteur', 'Travaux effectués', 'Atelier', 'Coût', 'Facture n°'],
  eng_items=['Huile et filtre', 'Filtre à gasoil / décanteur', 'Rouet de pompe à eau', 'Anodes', "Huile d'embase", 'Courroies', 'Bougies'],
  other='Autre', cont='(suite)',
  hull='Coque et équipements', hull_ref='Données de référence',
  hull_refs=['Antifouling (marque et couleur)', "Batteries (type, Ah et date d'achat)", 'Hélice (diamètre × pas)', 'Anodes (nombre et type)'],
  hull_cols=['Date', 'Élément', 'Détail des travaux', 'Atelier', 'Coût', 'Facture n°'],
  hull_items=['Antifouling', 'Anodes', 'Passe-coques', 'Hélice', 'Batteries', 'Pompes de cale', 'Électronique', 'Gréement (voilier)', 'Winchs (voilier)'],
  win='Hivernage et mise à l’eau', win_note="Chaque fois que le bateau sort de l'eau ou y retourne, ou qu'il est préparé pour l'hiver.",
  win_cols=['Date', 'Situation', 'Où', 'Travaux effectués', 'Notes'], win_state=["À l'eau", 'À terre'],
  win_items=['Moteur hiverné', 'Circuit rincé à l’eau douce / antigel', 'Réservoir plein avec additif', 'Batteries chargées ou débranchées',
             'Voiles, bâches et coussins retirés', 'Cale propre et sèche', 'Nettoyage de coque / antifouling'],
  win_guide='Liste complète pour la fin de saison : ',
  sell='Quand vous vendrez le bateau',
  sell_intro="La première chose que demande un acheteur sérieux, ce sont les papiers et ce qui a été fait sur le bateau. Avoir tout réuni et en ordre évite beaucoup de questions.",
  sell_items=['Feuille du registre à jour (hoja de asiento), sans charges', 'Titre / permis de navigation', 'Certificat de navigabilité et dernière ITB',
              "Attestation d'assurance en cours", "Factures d'achat et de réparations, classées par date", "Ce carnet d'entretien",
              "Manuels du bateau, du moteur et de l'électronique", 'Déclaration de conformité CE, si elle existe',
              'Révisions du radeau, des extincteurs et de la balise', "Justificatif de la taxe payée à l'achat (ITP ou TVA)",
              'Clés, doubles et codes (contact, cadenas, électronique)'],
  sell_quote="Un historique clair donne confiance à l'acheteur : il voit ce qui a été fait, quand et par qui, et il arrive à la visite avec moins de doutes.",
  sell_juan="Si un jour vous le vendez et que je peux vous aider, écrivez-moi. — Juan Morante",
  notes='Notes'),
}

CSS = r'''@font-face{font-family:A;src:url(%(fa)s) format("woff2");font-weight:100 900;font-stretch:62%% 125%%}
@font-face{font-family:S;src:url(%(fs)s) format("woff2");font-weight:200 900}
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:A,Arial,sans-serif;color:#0D1C27;font-size:8.6pt;line-height:1.3;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;width:210mm;height:297mm;padding:14mm 14mm 20mm;overflow:hidden;page-break-after:always}
.page:last-child{page-break-after:auto}
.ph{display:flex;align-items:flex-end;justify-content:space-between;border-bottom:1.4pt solid #0E3042;padding-bottom:2.5mm;margin-bottom:4mm}
.ph h2{font-size:16pt;font-weight:650;margin:0;color:#0E3042;letter-spacing:-.01em}
.ph h2 small{font-size:9pt;font-weight:400;color:#7F929E;margin-left:2mm}
.ph img{height:9mm}
.note{color:#44545F;font-size:8.2pt;margin:0 0 3.5mm}
table{width:100%%;border-collapse:collapse;table-layout:fixed}
th{background:#0E3042;color:#fff;font-weight:600;font-size:7.6pt;text-align:left;padding:1.6mm 1.8mm;border:.5pt solid #0E3042}
td{border:.5pt solid #B7C3CB;padding:1.2mm 1.8mm;vertical-align:top}
tr.z td{background:#F6F8F9}
.lbl{font-weight:600;font-size:8.4pt}
.lbl small{display:block;font-weight:400;font-size:7pt;color:#5A6B76;margin-top:.6mm}
.cb{display:grid;grid-template-columns:1fr 1fr;gap:.9mm 2.5mm;font-size:7pt;color:#33434E;line-height:1.15}
.cb span{display:flex;align-items:flex-start;gap:1.3mm}
.cb span::before{content:"";flex:none;width:2.5mm;height:2.5mm;border:.6pt solid #0B766B;border-radius:.4mm;background:#fff}
.cb .o{grid-column:1/-1}
.cb .o::after{content:"";flex:1;border-bottom:.5pt solid #B7C3CB;height:2.2mm}
.cb1{grid-template-columns:1fr}
.mot{font-size:7.4pt;color:#33434E;display:flex;flex-direction:column;gap:1.4mm}
.mot span{display:flex;align-items:center;gap:1.3mm}
.mot span::before{content:"";width:2.5mm;height:2.5mm;border:.6pt solid #0B766B;border-radius:.4mm}
.foot{position:absolute;left:14mm;right:14mm;bottom:8mm;display:flex;justify-content:space-between;font-size:7pt;color:#7F929E;border-top:.5pt solid #D5DDE2;padding-top:2mm}
/* portada */
.cover{display:flex;flex-direction:column;padding-top:22mm}
.cover .logo{width:118mm;margin:0 auto 10mm;display:block}
.cover .band{background:#0E3042;color:#fff;margin:0 -14mm;padding:9mm 14mm 8mm}
.cover .band h1{font-size:30pt;margin:0;font-weight:650;letter-spacing:-.015em;line-height:1.05}
.cover .band h1 span{display:block;font-size:15pt;font-weight:400;color:#9FD6CF;margin-top:1.5mm;letter-spacing:0}
.cover .band p{font-family:S,Georgia,serif;font-size:10pt;margin:4mm 0 0;color:#D5DDE2;max-width:150mm}
.fields{display:grid;grid-template-columns:1fr 1fr;gap:0 8mm;margin-top:9mm}
.fields div{border-bottom:.6pt solid #7F929E;height:12.5mm;padding-top:1.5mm;font-size:7.6pt;color:#44545F;text-transform:uppercase;letter-spacing:.06em;font-weight:600}
.fields .w2{grid-column:1/-1}
.how{margin-top:9mm;border-left:2pt solid #0B766B;padding:1mm 0 1mm 5mm}
.how h3{margin:0 0 2mm;font-size:9.5pt;color:#0B766B}
.how ol{margin:0;padding-left:4.5mm;font-family:S,Georgia,serif;font-size:9pt;color:#33434E}
.how li{margin-bottom:1.2mm}
/* bloques */
.refs{display:grid;grid-template-columns:1fr 1fr;gap:0 8mm;margin:0 0 5mm;border:.5pt solid #B7C3CB;padding:1mm 4mm 3mm;background:#F6F8F9}
.refs div{border-bottom:.5pt solid #9AAAB4;height:10.5mm;padding-top:1.5mm;font-size:7.4pt;color:#44545F;font-weight:600}
h3.sub{font-size:10pt;color:#0E3042;margin:6mm 0 2mm}
.sell p{font-family:S,Georgia,serif;font-size:10.5pt;line-height:1.5;margin:0 0 4mm;color:#1D2D38}
.check{list-style:none;margin:0 0 6mm;padding:0;columns:1}
.check li{display:flex;gap:3mm;align-items:flex-start;padding:2.3mm 0;border-bottom:.5pt solid #E1E7EA;font-size:9.6pt}
.check li::before{content:"";flex:none;width:3.6mm;height:3.6mm;border:.7pt solid #0B766B;border-radius:.6mm;margin-top:.3mm}
.quote{background:#E7F2F0;border-left:2.2pt solid #0B766B;padding:4mm 5mm;font-family:S,Georgia,serif;font-size:10.5pt;color:#0D1C27;margin:0 0 5mm}
.juan{font-size:9pt;color:#44545F}
.lines div{border-bottom:.5pt solid #B7C3CB;height:8.6mm}
.guide{margin-top:4mm;font-size:8pt;color:#44545F}
.guide b{color:#0E3042;font-weight:600}
'''


def b64file(path, mime):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(path, 'rb').read()).decode())


def esc(s):
    return html.escape(s, quote=False)


def cbs(items, other=None, one=False):
    s = ''.join('<span>%s</span>' % esc(i) for i in items)
    if other:
        s += '<span class="o">%s:</span>' % esc(other)
    return '<div class="cb%s">%s</div>' % (' cb1' if one else '', s)


def build_pdf_html(lang, logo, fa, fs):
    c = T[lang]
    pages = []

    def head(title, cont=False):
        return '<div class="ph"><h2>%s%s</h2><img src="%s" alt="Plata Marine"></div>' % (
            esc(title), ' <small>%s</small>' % esc(c['cont']) if cont else '', logo)

    # 1 portada
    fields = ''.join('<div class="%s">%s</div>' % ('w2' if w == 2 else '', esc(n)) for n, w in c['fields'])
    pages.append('<section class="page cover"><img class="logo" src="%s" alt="Plata Marine"><div class="band"><h1>%s<span>%s</span></h1><p>%s</p></div>'
                 '<div class="fields">%s</div><div class="how"><h3>%s</h3><ol>%s</ol></div></section>' % (
                     logo, esc(c['h1']), esc(c['sub']), esc(c['intro']), fields, esc(c['howh']),
                     ''.join('<li>%s</li>' % esc(x) for x in c['how'])))
    # 2 documentos
    cols = c['docs_cols']
    rows = ''.join('<tr style="height:12.6mm"><td class="lbl">%s%s</td><td></td><td></td><td></td></tr>' % (
        esc(a), '<small>%s</small>' % esc(b) if b else '') for a, b in c['docs_rows'])
    ct = ''.join('<tr style="height:9.4mm"><td class="lbl">%s</td><td></td><td></td></tr>' % esc(r) for r in c['contacts_rows'])
    pages.append('<section class="page">%s<table><colgroup><col style="width:36%%"><col style="width:15%%"><col style="width:15%%"><col></colgroup>'
                 '<thead><tr>%s</tr></thead><tbody>%s</tbody></table><h3 class="sub">%s</h3>'
                 '<table><colgroup><col style="width:30%%"><col><col style="width:28%%"></colgroup><thead><tr>%s</tr></thead><tbody>%s</tbody></table></section>' % (
                     head(c['docs']), ''.join('<th>%s</th>' % esc(x) for x in cols), rows, esc(c['contacts']),
                     ''.join('<th>%s</th>' % esc(x) for x in c['contacts_cols']), ct))
    # 3-5 motor
    erow = '<tr style="height:19.2mm"><td></td><td></td><td><div class="mot"><span>1</span><span>2</span></div></td><td>%s</td><td></td><td></td><td></td></tr>' % cbs(c['eng_items'], c['other'])
    ecols = '<colgroup><col style="width:11%"><col style="width:8.5%"><col style="width:7.5%"><col style="width:41%"><col><col style="width:9%"><col style="width:10.5%"></colgroup>'
    for k in range(3):
        pages.append('<section class="page">%s%s<table>%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table></section>' % (
            head(c['eng'], k > 0), '<p class="note">%s</p>' % esc(c['eng_note']) if k == 0 else '', ecols,
            ''.join('<th>%s</th>' % esc(x) for x in c['eng_cols']), erow * (10 if k == 0 else 11)))
    # 6-7 casco y equipos
    hrow = '<tr style="height:21.5mm"><td></td><td>%s</td><td></td><td></td><td></td><td></td></tr>' % cbs(c['hull_items'], c['other'])
    hcols = '<colgroup><col style="width:11%"><col style="width:34%"><col><col style="width:13%"><col style="width:9%"><col style="width:10.5%"></colgroup>'
    refs = '<div class="refs">%s</div>' % ''.join('<div>%s</div>' % esc(r) for r in c['hull_refs'])
    for k in range(2):
        pages.append('<section class="page">%s%s<table>%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table></section>' % (
            head(c['hull'], k > 0), refs if k == 0 else '', hcols, ''.join('<th>%s</th>' % esc(x) for x in c['hull_cols']),
            hrow * (7 if k == 0 else 9)))
    # 8 invernaje y botadura
    wrow = '<tr style="height:26.5mm"><td></td><td><div class="mot"><span>%s</span><span>%s</span></div></td><td></td><td>%s</td><td></td></tr>' % (
        esc(c['win_state'][0]), esc(c['win_state'][1]), cbs(c['win_items'], c['other'], one=True))
    wcols = '<colgroup><col style="width:11%"><col style="width:12%"><col style="width:16%"><col style="width:36%"><col></colgroup>'
    gurl = 'www.platamarine.com/%snavegante/preparar-barco-fin-de-temporada' % PRE[lang]
    pages.append('<section class="page">%s<p class="note">%s</p><table>%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table><p class="guide">%s<b>%s</b></p></section>' % (
        head(c['win']), esc(c['win_note']), wcols, ''.join('<th>%s</th>' % esc(x) for x in c['win_cols']), wrow * 6,
        esc(c['win_guide']), gurl))
    # 9 venta
    pages.append('<section class="page sell">%s<p>%s</p><ul class="check">%s</ul><div class="quote">%s</div><p class="juan">%s</p></section>' % (
        head(c['sell']), esc(c['sell_intro']), ''.join('<li>%s</li>' % esc(x) for x in c['sell_items']), esc(c['sell_quote']), esc(c['sell_juan'])))
    # 10 notas
    pages.append('<section class="page">%s<div class="lines">%s</div></section>' % (head(c['notes']), '<div></div>' * 28))

    n = len(pages)
    out = []
    for i, p in enumerate(pages, 1):
        foot = '<div class="foot"><span>www.platamarine.com · %s</span><span>%d / %d</span></div>' % (PHONE, i, n)
        out.append(p.replace('</section>', foot + '</section>'))
    return '<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>%s</body></html>' % (
        lang, esc(c['title']), CSS % {'fa': fa, 'fs': fs}, ''.join(out))


def logo_data():
    """Logo reducido a 900 px de ancho para no inflar el PDF."""
    src = os.path.join(ROOT, 'logo-plata-marine.png')
    try:
        from PIL import Image
        im = Image.open(src).convert('RGBA')
        im.thumbnail((900, 300))
        buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
        return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
    except ImportError:
        return b64file(src, 'image/png')


async def build_pdfs():
    from playwright.async_api import async_playwright
    logo = logo_data()
    fa = b64file(os.path.join(ROOT, 'archivo.woff2'), 'font/woff2')
    fs = b64file(os.path.join(ROOT, 'source-serif-4.woff2'), 'font/woff2')
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page()
        for lang in T:
            await pg.set_content(build_pdf_html(lang, logo, fa, fs), wait_until='load')
            await pg.evaluate('document.fonts.ready')
            await pg.emulate_media(media='print')
            bad = await pg.evaluate('''[...document.querySelectorAll('section')].map((s,i)=>{const f=s.querySelector('.foot').getBoundingClientRect().top;
                const last=[...s.children].filter(e=>!e.classList.contains('foot')).pop().getBoundingClientRect().bottom;return last>f-4?i+1:0}).filter(Boolean)''')
            if bad:
                print('AVISO %s: contenido encima del pie en las páginas %s' % (lang, bad))
            out = os.path.join(ROOT, 'herramientas', PDFNAME[lang])
            await pg.pdf(path=out, print_background=True, prefer_css_page_size=True)
            import pikepdf
            with pikepdf.open(out, allow_overwriting_input=True) as pdf:
                if '/Metadata' in pdf.Root:  # sin flujo XMP: solo Title y Author en el diccionario Info
                    del pdf.Root.Metadata
                for k in list(pdf.docinfo.keys()):
                    del pdf.docinfo[k]
                pdf.docinfo['/Title'] = T[lang]['title']
                pdf.docinfo['/Author'] = 'Plata Marine'
                pdf.save(out)
            print(out, os.path.getsize(out))
        await br.close()


# ---------------------------------------------------------------- páginas web
P = {
'es': dict(
  title='Libro de mantenimiento del barco: plantilla PDF gratis',
  desc='Descarga gratis un libro de mantenimiento para tu barco: motor, casco, documentos, invernaje y lo que pide un comprador. PDF A4 para imprimir.',
  h1='Libro de mantenimiento del barco', crumb='Herramientas', eyebrow='Herramientas · Plantilla para imprimir',
  by='Por Juan Morante', date='Noviembre de 2026',
  lead='Una libreta sencilla para apuntar todo lo que le haces al barco: cambios de aceite, ánodos, varadas, la revisión de la balsa, el seguro… La he preparado en PDF para que la imprimas y la tengas a bordo. Es gratis y no te pido el correo.',
  dl='Descargar el libro en PDF', dlmeta='A4 · {n} páginas · para imprimir y rellenar a mano',
  h_why='Para qué sirve',
  why=['Con los años nadie se acuerda de cuándo se cambió el rodete o de qué antifouling se le dio. Tenerlo apuntado ayuda a no saltarse revisiones, a saber qué pedir en el taller y a no pagar dos veces el mismo trabajo.',
       'Y si algún día vendes el barco, es de lo primero que te piden. Un historial claro da confianza al comprador: ve qué se ha hecho, cuándo y quién lo hizo.'],
  h_inc='Qué incluye',
  inc=['<strong>Portada con los datos del barco:</strong> modelo, año, matrícula, eslora y los motores con su número de serie.',
       '<strong>Documentos y equipos de seguridad:</strong> permiso de navegación, certificado de navegabilidad, ITB, seguro, balsa, extintores, bengalas y radiobaliza, con fecha y caducidad.',
       '<strong>Registro de motor:</strong> tres páginas con fecha, horas, trabajo hecho (aceite y filtro, filtro de gasoil, rodete, ánodos, aceite de cola, correas, bujías), taller, coste y número de factura.',
       '<strong>Casco y equipos:</strong> antifouling, ánodos, pasacascos, hélice, baterías, bombas de achique, electrónica y, si es velero, jarcia y winches.',
       '<strong>Invernaje y botadura:</strong> cuándo sale y cuándo vuelve al agua, y qué se ha hecho cada vez.',
       '<strong>Cuando vendas el barco:</strong> la lista de papeles que pide un comprador, para tenerlo todo a mano.'],
  h_tips='Para que te sirva de verdad',
  tips=['Apunta cada trabajo el mismo día, aunque lo hagas tú.',
        'Numera las facturas y guárdalas en una carpeta con el mismo número que escribes en el libro.',
        'Cuando llenes una página, hazle una foto. Si el libro se moja o se pierde, el historial sigue ahí.'],
  h_more='Para no olvidarte de las fechas',
  more='El libro te dice cuándo caduca cada cosa, pero hay que acordarse de mirarlo. Si prefieres que te llegue un aviso antes de que venza la ITB, el seguro o la revisión de la balsa, tienes los avisos gratis. Y si estás cerrando la temporada, en la guía de invernaje está todo lo que conviene hacer antes de dejar el barco parado.',
  b_rem='Avisos de vencimientos gratis', b_win='Guía para preparar el barco en invierno',
  aviso='Es una plantilla orientativa. Los intervalos de cada mantenimiento los marca el fabricante de tu motor y de tus equipos: consulta siempre su manual.',
  card_k='¿Piensas venderlo?', card_h='Lo miramos juntos.',
  card_p='Si un día quieres vender el barco, te ayudo a ver qué papeles tienes, qué falta y cómo presentarlo.',
  card_b='Hablar con Juan por WhatsApp',
  wa='Hola Juan, he descargado el libro de mantenimiento y quería preguntarte una cosa.',
  rel_k='Más herramientas',
  rel=[('herramientas/coste-mantener-barco', 'Cuánto cuesta mantener un barco'), ('navegante/preparar-barco-fin-de-temporada', 'Preparar el barco para el invierno'),
       ('herramientas/valora-tu-barco', '¿Qué influye en el precio de mi barco?'), ('herramientas/', 'Todas las herramientas')]),
'ca': dict(
  title='Llibre de manteniment del vaixell: plantilla PDF gratis',
  desc="Descarrega gratis un llibre de manteniment per al teu vaixell: motor, casc, documents, hivernada i el que demana un comprador. PDF A4 per imprimir.",
  h1='Llibre de manteniment del vaixell', crumb='Eines', eyebrow='Eines · Plantilla per imprimir',
  by='Per Juan Morante', date='Novembre de 2026',
  lead="Una llibreta senzilla per apuntar tot el que fas al vaixell: canvis d'oli, ànodes, varades, la revisió de la balsa, l'assegurança… L'he preparada en PDF perquè la imprimeixis i la tinguis a bord. És gratis i no et demano el correu.",
  dl='Descarregar el llibre en PDF', dlmeta='A4 · {n} pàgines · per imprimir i omplir a mà',
  h_why='Per a què serveix',
  why=["Amb els anys ningú no recorda quan es va canviar el rodet o quin antifouling s'hi va donar. Tenir-ho apuntat ajuda a no saltar-se revisions, a saber què demanar al taller i a no pagar dues vegades la mateixa feina.",
       "I si algun dia vens el vaixell, és de les primeres coses que et demanen. Un historial clar dona confiança al comprador: veu què s'ha fet, quan i qui ho va fer."],
  h_inc='Què inclou',
  inc=['<strong>Portada amb les dades del vaixell:</strong> model, any, matrícula, eslora i els motors amb el número de sèrie.',
       "<strong>Documents i equips de seguretat:</strong> permís de navegació, certificat de navegabilitat, ITB, assegurança, balsa, extintors, bengales i radiobalisa, amb data i caducitat.",
       "<strong>Registre de motor:</strong> tres pàgines amb data, hores, feina feta (oli i filtre, filtre de gasoil, rodet, ànodes, oli de cua, corretges, bugies), taller, cost i número de factura.",
       '<strong>Casc i equips:</strong> antifouling, ànodes, passacascs, hèlix, bateries, bombes de sentina, electrònica i, si és un veler, eixàrcia i winches.',
       "<strong>Hivernada i botada:</strong> quan surt i quan torna a l'aigua, i què s'hi ha fet cada vegada.",
       '<strong>Quan venguis el vaixell:</strong> la llista de papers que demana un comprador, per tenir-ho tot a mà.'],
  h_tips='Perquè et serveixi de debò',
  tips=['Apunta cada feina el mateix dia, encara que la facis tu.',
        'Numera les factures i guarda-les en una carpeta amb el mateix número que escrius al llibre.',
        "Quan omplis una pàgina, fes-li una foto. Si el llibre es mulla o es perd, l'historial continua allà."],
  h_more='Per no oblidar-te de les dates',
  more="El llibre et diu quan caduca cada cosa, però cal recordar-se de mirar-lo. Si prefereixes rebre un avís abans que venci l'ITB, l'assegurança o la revisió de la balsa, tens els avisos gratis. I si estàs tancant la temporada, a la guia d'hivernada hi ha tot el que convé fer abans de deixar el vaixell aturat.",
  b_rem='Avisos de venciments gratis', b_win="Guia per preparar el vaixell a l'hivern",
  aviso="És una plantilla orientativa. Els intervals de cada manteniment els marca el fabricant del teu motor i dels teus equips: consulta sempre el manual.",
  card_k="Penses vendre'l?", card_h="Ho mirem junts.",
  card_p="Si un dia vols vendre el vaixell, t'ajudo a veure quins papers tens, què hi falta i com presentar-lo.",
  card_b='Parlar amb el Juan per WhatsApp',
  wa="Hola Juan, he descarregat el llibre de manteniment i et volia preguntar una cosa.",
  rel_k='Més eines',
  rel=[('herramientas/coste-mantener-barco', 'Quant costa mantenir un vaixell'), ('navegante/preparar-barco-fin-de-temporada', "Preparar el vaixell per a l'hivern"),
       ('herramientas/valora-tu-barco', 'Què influeix en el preu del meu vaixell?'), ('herramientas/', 'Totes les eines')]),
'en': dict(
  title='Boat maintenance log PDF: free printable template',
  desc='Download a free boat maintenance log: engine, hull, documents, laying up and the paperwork a buyer asks for. A4 PDF to print and fill in by hand.',
  h1='Boat maintenance log', crumb='Tools', eyebrow='Tools · Printable template',
  by='By Juan Morante', date='November 2026',
  lead='A simple log to write down everything you do to the boat: oil changes, anodes, haul-outs, the liferaft service, the insurance… I have put it together as a PDF so you can print it and keep it on board. It is free and I do not ask for your email.',
  dl='Download the log as a PDF', dlmeta='A4 · {n} pages · to print and fill in by hand',
  h_why='What it is for',
  why=['After a few years nobody remembers when the impeller was changed or which antifouling went on. Writing it down helps you not to skip services, to know what to ask for at the yard and not to pay twice for the same job.',
       'And if you ever sell the boat, it is one of the first things you will be asked for. A clear history gives the buyer confidence: they can see what was done, when and by whom.'],
  h_inc='What is inside',
  inc=['<strong>Cover page with the boat details:</strong> model, year, registration, length and the engines with their serial numbers.',
       '<strong>Documents and safety equipment:</strong> navigation permit, certificate of seaworthiness, ITB, insurance, liferaft, fire extinguishers, flares and EPIRB, with dates and expiry.',
       '<strong>Engine log:</strong> three pages with date, hours, work done (oil and filter, fuel filter, impeller, anodes, gear oil, belts, spark plugs), workshop, cost and invoice number.',
       '<strong>Hull and equipment:</strong> antifouling, anodes, through-hulls, propeller, batteries, bilge pumps, electronics and, on a sailboat, rigging and winches.',
       '<strong>Laying up and launching:</strong> when the boat comes out and goes back in, and what was done each time.',
       '<strong>When you sell the boat:</strong> the list of papers a buyer asks for, so you have everything to hand.'],
  h_tips='To get real use out of it',
  tips=['Write each job down on the day, even if you did it yourself.',
        'Number your invoices and keep them in a folder with the same number you write in the log.',
        'When a page is full, take a photo of it. If the log gets wet or lost, the history is still there.'],
  h_more='So you do not miss a date',
  more='The log tells you when each thing expires, but you have to remember to look at it. If you would rather get a reminder before the ITB, the insurance or the liferaft service runs out, there are free reminders. And if you are closing the season, the laying-up guide covers what is worth doing before the boat sits still.',
  b_rem='Free expiry reminders', b_win='Guide to laying up the boat for winter',
  aviso='This is a general template. Service intervals are set by the manufacturer of your engine and equipment: always check their manual.',
  card_k='Thinking of selling?', card_h='We can look at it together.',
  card_p='If you ever want to sell the boat, I can help you see which papers you have, what is missing and how to present it.',
  card_b='Talk to Juan on WhatsApp',
  wa='Hi Juan, I downloaded the maintenance log and had a question.',
  rel_k='More tools',
  rel=[('herramientas/coste-mantener-barco', 'How much it costs to keep a boat'), ('navegante/preparar-barco-fin-de-temporada', 'Laying up the boat for winter'),
       ('herramientas/valora-tu-barco', 'What affects my boat’s price?'), ('herramientas/', 'All tools')]),
'fr': dict(
  title="Carnet d'entretien du bateau PDF : modèle gratuit",
  desc="Téléchargez un carnet d'entretien gratuit pour votre bateau : moteur, coque, documents, hivernage et papiers demandés par l'acheteur. PDF A4 à imprimer.",
  h1="Carnet d'entretien du bateau", crumb='Outils', eyebrow='Outils · Modèle à imprimer',
  by='Par Juan Morante', date='Novembre 2026',
  lead="Un carnet simple pour noter tout ce que vous faites sur le bateau : vidanges, anodes, carénages, révision du radeau, assurance… Je l'ai préparé en PDF pour que vous puissiez l'imprimer et le garder à bord. C'est gratuit et je ne vous demande pas votre e-mail.",
  dl='Télécharger le carnet en PDF', dlmeta='A4 · {n} pages · à imprimer et remplir à la main',
  h_why='À quoi il sert',
  why=["Au bout de quelques années, personne ne se souvient de la date du changement de rouet ni de l'antifouling utilisé. Tout noter aide à ne pas sauter de révision, à savoir quoi demander au chantier et à ne pas payer deux fois le même travail.",
       "Et si un jour vous vendez le bateau, c'est l'une des premières choses qu'on vous demandera. Un historique clair donne confiance à l'acheteur : il voit ce qui a été fait, quand et par qui."],
  h_inc='Ce qu’il contient',
  inc=["<strong>Couverture avec les données du bateau :</strong> modèle, année, immatriculation, longueur et moteurs avec leur numéro de série.",
       "<strong>Documents et matériel de sécurité :</strong> titre de navigation, certificat de navigabilité, ITB, assurance, radeau, extincteurs, feux à main et balise, avec date et expiration.",
       "<strong>Suivi moteur :</strong> trois pages avec date, heures, travaux effectués (huile et filtre, filtre à gasoil, rouet, anodes, huile d'embase, courroies, bougies), atelier, coût et numéro de facture.",
       "<strong>Coque et équipements :</strong> antifouling, anodes, passe-coques, hélice, batteries, pompes de cale, électronique et, pour un voilier, gréement et winchs.",
       "<strong>Hivernage et mise à l'eau :</strong> quand le bateau sort et retourne à l'eau, et ce qui a été fait à chaque fois.",
       "<strong>Quand vous vendrez le bateau :</strong> la liste des papiers demandés par un acheteur, pour tout avoir sous la main."],
  h_tips='Pour qu’il serve vraiment',
  tips=["Notez chaque intervention le jour même, même si vous la faites vous-même.",
        "Numérotez les factures et rangez-les dans un classeur avec le même numéro que dans le carnet.",
        "Quand une page est pleine, prenez-la en photo. Si le carnet est mouillé ou perdu, l'historique reste."],
  h_more='Pour ne pas oublier les échéances',
  more="Le carnet indique quand chaque chose expire, mais il faut penser à le regarder. Si vous préférez recevoir un rappel avant l'échéance de l'ITB, de l'assurance ou de la révision du radeau, il existe des rappels gratuits. Et si vous terminez la saison, le guide d'hivernage reprend tout ce qu'il vaut mieux faire avant de laisser le bateau à l'arrêt.",
  b_rem="Rappels d'échéances gratuits", b_win="Guide pour préparer le bateau pour l'hiver",
  aviso="Ce modèle est indicatif. Les intervalles d'entretien sont fixés par le fabricant de votre moteur et de vos équipements : consultez toujours leur manuel.",
  card_k='Vous pensez vendre ?', card_h='Regardons-le ensemble.',
  card_p="Si un jour vous voulez vendre le bateau, je vous aide à voir quels papiers vous avez, ce qui manque et comment le présenter.",
  card_b='Parler à Juan sur WhatsApp',
  wa="Bonjour Juan, j'ai téléchargé le carnet d'entretien et j'avais une question.",
  rel_k='Plus d’outils',
  rel=[('herramientas/coste-mantener-barco', 'Combien coûte l’entretien d’un bateau'), ('navegante/preparar-barco-fin-de-temporada', "Préparer le bateau pour l'hiver"),
       ('herramientas/valora-tu-barco', 'Qu’est-ce qui influe sur le prix de mon bateau ?'), ('herramientas/', 'Tous les outils')]),
}

PAGE_CSS = '''<style>.dl{background:#fff;border:1px solid var(--plata);border-radius:8px;padding:18px 20px;margin:0 0 26px;font-family:var(--display);display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px}
.dl .btn{flex:none}.dl p{margin:0;font-size:13.5px;color:var(--ink-2);min-width:0}
.cta2{background:#F3F5F6;padding:18px 20px;border-radius:6px;margin:0 0 22px}.cta2 h3{font-family:var(--display);font-size:1.05rem;margin:0 0 6px}.cta2 p{margin:0 0 12px}.cta2 .btn{margin-right:8px;margin-bottom:8px}
@media (max-width:480px){.dl .btn,.cta2 .btn{width:100%;margin-right:0}}
</style>'''


def url(lang, path=''):
    return '%s/%s%s' % (SITE, PRE[lang], path)


def build_page(lang, npages):
    c = P[lang]
    tpl = open(os.path.join(ROOT, PRE[lang] + 'herramientas', 'coste-mantener-barco.html'), encoding='utf-8').read()
    hdr = tpl[tpl.index('<header class="top">'):tpl.index('</header>') + len('</header>')]
    hdr = hdr.replace('herramientas/coste-mantener-barco', 'herramientas/' + SLUG)
    # botón de WhatsApp de la cabecera: el genérico del menú móvil, no el de la calculadora
    generic = re.search(r'<div class="pmx-wide"><a class="btn btn-wa" href="([^"]+)"', hdr).group(1)
    hdr = re.sub(r'(</nav>\s*<a class="btn btn-wa" href=")[^"]+(")', lambda m: m.group(1) + generic + m.group(2), hdr, count=1)
    ftr = tpl[tpl.index('<footer class="foot">'):tpl.index('</footer>') + len('</footer>')]
    if lang == 'es':  # la plantilla ES usa rutas relativas; aquí todo absoluto
        ftr = ftr.replace('href="../', 'href="/')
        hdr = hdr.replace('href="../"', 'href="/"').replace('src="../', 'src="/')
    scripts = '\n'.join(l for l in tpl.splitlines() if re.match(r'<script src="/(nav|consent|submit-confirmed|analytics)\.js', l))
    p = PRE[lang]
    canon = url(lang, 'herramientas/' + SLUG)
    alts = '\n'.join('<link rel="alternate" hreflang="%s" href="%s">' % (l, url(l, 'herramientas/' + SLUG)) for l in PRE)
    alts += '\n<link rel="alternate" hreflang="x-default" href="%s">' % url('es', 'herramientas/' + SLUG)
    og = 'og-image.jpg' if lang == 'es' else 'og-image-%s.jpg' % lang
    pdf = '/herramientas/' + PDFNAME[lang]  # los cuatro PDF viven en /herramientas/
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": canon + "#page", "url": canon, "name": c['h1'], "description": c['desc'], "inLanguage": lang,
         "isPartOf": {"@type": "WebSite", "name": "Plata Marine", "url": SITE + "/"},
         "author": {"@type": "Person", "name": "Juan Morante"}, "publisher": {"@type": "Organization", "name": "Plata Marine", "url": SITE + "/"},
         "primaryImageOfPage": SITE + "/" + og,
         "mainEntity": {"@type": "DigitalDocument", "name": T[lang]['title'], "encodingFormat": "application/pdf", "url": SITE + pdf, "inLanguage": lang,
                        "isAccessibleForFree": True}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": url(lang)},
            {"@type": "ListItem", "position": 2, "name": c['crumb'], "item": url(lang, 'herramientas/')},
            {"@type": "ListItem", "position": 3, "name": c['h1'], "item": canon}]}]}
    a = lambda s: html.escape(s, quote=True)
    wa = 'https://wa.me/34633742973?text=' + __import__('urllib.parse').parse.quote(c['wa'])
    dlmeta = c['dlmeta'].format(n=npages)
    count = "try{window.pmCount&&window.pmCount({t:'descarga_libro',m:'%s'})}catch(e){}" % lang
    body = '''<main class="art">
  <div class="wrap">
    <article>
      <header>
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
        <div class="meta"><span>{by}</span><span>{date}</span></div>
        <p class="lead">{lead}</p>
      </header>
      <div class="prose">
        <div class="dl"><a class="btn btn-wa" href="{pdf}" download onclick="{count}">{dl}</a><p>{dlmeta}</p></div>
        <h2 id="para-que">{h_why}</h2>
        {why}
        <h2 id="que-incluye">{h_inc}</h2>
        <ul>{inc}</ul>
        <h2 id="consejos">{h_tips}</h2>
        <ul>{tips}</ul>
        <div class="cta2"><h3>{h_more}</h3><p>{more}</p><a class="btn btn-wa" href="/{p}recordatorios-barco/">{b_rem}</a><a class="btn btn-ghost" href="/{p}navegante/preparar-barco-fin-de-temporada">{b_win}</a></div>
        <p class="aviso">{aviso}</p>
      </div>
    </article>
    <aside class="aside">
      <div class="card">
        <p class="eyebrow">{card_k}</p>
        <h3>{card_h}</h3>
        <p>{card_p}</p>
        <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{card_b}</a>
      </div>
      <div class="rel">
        <p class="eyebrow">{rel_k}</p>
        {rel}
      </div>
    </aside>
  </div>
</main>'''.format(
        eyebrow=esc(c['eyebrow']), h1=esc(c['h1']), by=esc(c['by']), date=esc(c['date']), lead=esc(c['lead']),
        pdf=pdf, count=count, dl=esc(c['dl']), dlmeta=esc(dlmeta), h_why=esc(c['h_why']),
        why='\n        '.join('<p>%s</p>' % esc(x) for x in c['why']), h_inc=esc(c['h_inc']),
        inc=''.join('<li>%s</li>' % x for x in c['inc']), h_tips=esc(c['h_tips']),
        tips=''.join('<li>%s</li>' % esc(x) for x in c['tips']), h_more=esc(c['h_more']), more=esc(c['more']), p=p,
        b_rem=esc(c['b_rem']), b_win=esc(c['b_win']), aviso=esc(c['aviso']), card_k=esc(c['card_k']), card_h=esc(c['card_h']),
        card_p=esc(c['card_p']), wa=a(wa), card_b=esc(c['card_b']), rel_k=esc(c['rel_k']),
        rel=''.join('<a href="/%s%s">%s</a>' % (p, h, esc(t)) for h, t in c['rel']))
    doc = '''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
{alts}
<link rel="icon" type="image/png" href="/logo-plata-marine.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{site}/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<link rel="stylesheet" href="/guias/guias.css">
{css}
<link rel="stylesheet" href="/nav.css?v=20261006m">
<script type="application/ld+json">{ld}</script>
</head>
<body>

{hdr}

{body}

{ftr}
{scripts}
</body>
</html>
'''.format(lang=lang, title=a(c['title']), desc=a(c['desc']), canon=canon, alts=alts, site=SITE, og=og, css=PAGE_CSS,
           ld=json.dumps(ld, ensure_ascii=False), hdr=hdr, body=body, ftr=ftr, scripts=scripts)
    out = os.path.join(ROOT, p + 'herramientas', SLUG + '.html')
    open(out, 'w', encoding='utf-8').write(doc)
    print(out, len(doc))


def pdf_pages():
    try:
        import pikepdf
        with pikepdf.open(os.path.join(ROOT, 'herramientas', PDFNAME['es'])) as pdf:
            return len(pdf.pages)
    except Exception:
        return 10


if __name__ == '__main__':
    what = set(sys.argv[1:]) or {'pdf', 'pages'}
    if 'pdf' in what:
        asyncio.run(build_pdfs())
    if 'pages' in what:
        n = pdf_pages()
        for lang in P:
            build_page(lang, n)
