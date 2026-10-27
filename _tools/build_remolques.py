#!/usr/bin/env python3
"""Página /remolques/ (ES/CA/EN/FR): remolques Goliath (Océane y Satellite) bajo pedido.
Cabecera, estilos de menú y pie se copian de /squama/ de cada idioma. Uso: python3 _tools/build_remolques.py"""
import os, re, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.platamarine.com'
LANGS = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}
E = html.escape

# modelo, MMA kg, carga útil kg, longitud remolque, precio sin IVA (tarifa Plata Marine)
OCE = [('Océane O101', 1000, 730, '5,50', 3390), ('Océane O131', 1300, 990, '6,00', 3890),
       ('Océane O151', 1500, 1170, '6,00', 3990), ('Océane O181', 1800, 1420, '6,50', 4790)]
SAT = [('Satellite MX101', 1000, 730, 3790), ('Satellite MX131', 1300, 990, 4090),
       ('Satellite MX151', 1500, 1170, 4290), ('Satellite MX181', 1800, 1420, 4990)]


def eur(n, lg):
    s = f'{n:,}'
    if lg == 'en':
        return '€' + s
    if lg == 'fr':
        return s.replace(',', '&nbsp;') + '&nbsp;€'
    return s.replace(',', '.') + '&nbsp;€'


def num(n, lg):
    s = f'{n:,}'
    return s if lg == 'en' else s.replace(',', '&nbsp;' if lg == 'fr' else '.')


def m(v, lg):
    return (v.replace(',', '.') if lg == 'en' else v) + ' m'


T = {
 'es': dict(
  title='Remolques Goliath para barcos: precios en Barcelona',
  desc='Remolques Goliath Océane y Satellite para barcos de hasta 1.800 kg, bajo pedido. Desde 3.390 € + IVA, con COC y ficha técnica en español para matricularlo.',
  crumb=('Inicio', 'Barcos nuevos', 'Remolques'), k='Remolques para barcos',
  h1='Remolques Goliath para tu barco',
  lead='Remolques galvanizados de rodillos para llevar tu barco de casa a la rampa. Los pido a fábrica ajustados a tu barco y te acompaño hasta que lo tienes matriculado.',
  cta='Pedir precio para mi barco', wa='Hola Juan, quiero información sobre un remolque Goliath para mi barco.',
  vat='+ IVA', from_='Desde',
  oce_h='Océane', oce_p='La gama más vendida de Goliath: robusta, con rodillos de 90 mm, cabrestante Goliath, luces retráctiles y guardabarros negros. Una longitud fija por cada modelo.',
  sat_h='Satellite', sat_p='Un escalón por encima: rodillos de 110 mm, luces LED retráctiles, sistema de amarre QuickFlex y garantía ampliada en las piezas de freno. Cada modelo se fabrica en tres longitudes, sin coste extra, para que se ajuste a tu casco.',
  th=('Modelo', 'MMA', 'Carga útil', 'Longitud', 'Precio'), sat_len='a elegir',
  inc_h='Qué incluye conmigo', inc=[
   ('Te ayudo a elegir', 'Calculamos el peso real de tu barco con motor, combustible y equipo, y elegimos el remolque con margen de carga.'),
   ('Hecho a medida de tu barco', 'Paso a fábrica las medidas de tu casco para ajustar la longitud, la altura del soporte del cabrestante y los rodillos.'),
   ('Papeles para matricularlo', 'Cada remolque viene con COC y ficha técnica en español. Te acompaño en la ITV y la matriculación.'),
   ('Entrega en Barcelona', 'Lo recibes en la zona de Barcelona y te lo enseño antes de enganchar.')],
  how_h='Cómo se pide', how=[('Me cuentas tu barco', 'Modelo, eslora, peso y motor. Si tienes la documentación a mano, mejor.'),
   ('Te paso el presupuesto', 'Por escrito, con el remolque elegido, sus opciones y el plazo de entrega.'),
   ('Pedido a fábrica', 'Con tu señal, hago el pedido a Goliath ajustado a tu barco.'),
   ('Entrega', 'Te lo entrego con sus papeles listos para matricular.')],
  faq_h='Preguntas frecuentes', faq=[
   ('¿Hay que matricular el remolque?', 'Sí. En España, los remolques de más de 750 kg de MMA llevan matrícula propia y pasan ITV. Todos los de esta página superan ese peso, por eso vienen con COC y ficha técnica en español.'),
   ('¿Qué carné necesito para llevarlo?', 'Con el carné B puedes llevar un remolque de más de 750 kg si la suma de la MMA del coche y la del remolque no pasa de 3.500 kg. Si la supera, necesitas el B96 (hasta 4.250 kg) o el BE.'),
   ('¿Cuánto tarda?', 'El plazo depende de fábrica y te lo confirmo por escrito al hacer el pedido.'),
   ('¿Tenéis remolques para motos de agua o barcos más grandes?', 'Sí, Goliath fabrica remolques para motos de agua y para barcos de hasta 3.500 kg. Cuéntame qué necesitas y te paso opciones.')],
  small='Precios sin IVA, por unidad, con entrega en la zona de Barcelona. No incluyen matriculación, ITV ni gestoría. Información orientativa: puede cambiar y no es vinculante; el precio final es el del presupuesto por escrito. Las normas de matriculación y carné son un resumen: confírmalas con tu gestoría o la DGT.',
  alt_o='Remolque Goliath Océane de un eje', alt_s='Remolque Goliath Satellite de un eje',
 ),
 'ca': dict(
  title='Remolcs Goliath per a vaixells: preus a Barcelona',
  desc='Remolcs Goliath Océane i Satellite per a vaixells de fins a 1.800 kg, per encàrrec. Des de 3.390 € + IVA, amb COC i fitxa tècnica en castellà per matricular-lo.',
  crumb=('Inici', 'Vaixells nous', 'Remolcs'), k='Remolcs per a vaixells',
  h1='Remolcs Goliath per al teu vaixell',
  lead='Remolcs galvanitzats de corrons per portar el teu vaixell de casa a la rampa. Els demano a fàbrica ajustats al teu vaixell i t’acompanyo fins que el tens matriculat.',
  cta='Demanar preu per al meu vaixell', wa='Hola Juan, vull informació sobre un remolc Goliath per al meu vaixell.',
  vat='+ IVA', from_='Des de',
  oce_h='Océane', oce_p='La gamma més venuda de Goliath: robusta, amb corrons de 90 mm, cabrestant Goliath, llums retràctils i parafangs negres. Una longitud fixa per a cada model.',
  sat_h='Satellite', sat_p='Un graó per sobre: corrons de 110 mm, llums LED retràctils, sistema d’amarratge QuickFlex i garantia ampliada a les peces de fre. Cada model es fabrica en tres longituds, sense cost extra, perquè s’ajusti al teu buc.',
  th=('Model', 'MMA', 'Càrrega útil', 'Longitud', 'Preu'), sat_len='a triar',
  inc_h='Què inclou amb mi', inc=[
   ('T’ajudo a triar', 'Calculem el pes real del teu vaixell amb motor, combustible i equip, i triem el remolc amb marge de càrrega.'),
   ('Fet a mida del teu vaixell', 'Passo a fàbrica les mides del teu buc per ajustar la longitud, l’alçada del suport del cabrestant i els corrons.'),
   ('Papers per matricular-lo', 'Cada remolc ve amb COC i fitxa tècnica en castellà. T’acompanyo a la ITV i la matriculació.'),
   ('Lliurament a Barcelona', 'El reps a la zona de Barcelona i te l’ensenyo abans d’enganxar.')],
  how_h='Com es demana', how=[('M’expliques el teu vaixell', 'Model, eslora, pes i motor. Si tens la documentació a mà, millor.'),
   ('Et passo el pressupost', 'Per escrit, amb el remolc triat, les seves opcions i el termini de lliurament.'),
   ('Comanda a fàbrica', 'Amb la teva paga i senyal, faig la comanda a Goliath ajustada al teu vaixell.'),
   ('Lliurament', 'Te’l lliuro amb els papers a punt per matricular.')],
  faq_h='Preguntes freqüents', faq=[
   ('Cal matricular el remolc?', 'Sí. A Espanya, els remolcs de més de 750 kg de MMA porten matrícula pròpia i passen ITV. Tots els d’aquesta pàgina superen aquest pes, per això vénen amb COC i fitxa tècnica en castellà.'),
   ('Quin carnet necessito per portar-lo?', 'Amb el carnet B pots portar un remolc de més de 750 kg si la suma de la MMA del cotxe i la del remolc no passa de 3.500 kg. Si la supera, necessites el B96 (fins a 4.250 kg) o el BE.'),
   ('Quant triga?', 'El termini depèn de fàbrica i te’l confirmo per escrit en fer la comanda.'),
   ('Teniu remolcs per a motos d’aigua o vaixells més grans?', 'Sí, Goliath fabrica remolcs per a motos d’aigua i per a vaixells de fins a 3.500 kg. Explica’m què necessites i et passo opcions.')],
  small='Preus sense IVA, per unitat, amb lliurament a la zona de Barcelona. No inclouen matriculació, ITV ni gestoria. Informació orientativa: pot canviar i no és vinculant; el preu final és el del pressupost per escrit. Les normes de matriculació i carnet són un resum: confirma-les amb la teva gestoria o la DGT.',
  alt_o='Remolc Goliath Océane d’un eix', alt_s='Remolc Goliath Satellite d’un eix',
 ),
 'en': dict(
  title='Goliath boat trailers: prices in Barcelona',
  desc='Goliath Océane and Satellite trailers for boats up to 1,800 kg, built to order. From €3,390 + VAT, with Spanish COC and technical sheet for registration.',
  crumb=('Home', 'New boats', 'Trailers'), k='Boat trailers',
  h1='Goliath trailers for your boat',
  lead='Galvanised roller trailers to take your boat from home to the slipway. I order them from the factory adjusted to your boat and help you until it is registered.',
  cta='Get a price for my boat', wa='Hi Juan, I would like information about a Goliath trailer for my boat.',
  vat='+ VAT', from_='From',
  oce_h='Océane', oce_p='Goliath’s best-selling range: sturdy, with 90 mm rollers, Goliath winch, retractable lights and black mudguards. One fixed length per model.',
  sat_h='Satellite', sat_p='One step up: 110 mm rollers, retractable LED lights, QuickFlex tie-down system and extended warranty on brake parts. Each model is built in three lengths, at no extra cost, to fit your hull.',
  th=('Model', 'GVW', 'Payload', 'Length', 'Price'), sat_len='your choice',
  inc_h='What you get with me', inc=[
   ('Help choosing', 'We work out the real weight of your boat with engine, fuel and gear, and choose a trailer with load margin.'),
   ('Made to fit your boat', 'I send your hull measurements to the factory to adjust the length, winch post height and rollers.'),
   ('Papers for registration', 'Every trailer comes with a Spanish COC and technical sheet. I help you with the ITV inspection and registration.'),
   ('Delivery in Barcelona', 'You receive it in the Barcelona area and I show it to you before you hitch it.')],
  how_h='How to order', how=[('Tell me about your boat', 'Model, length, weight and engine. If you have the papers to hand, even better.'),
   ('I send you a quote', 'In writing, with the chosen trailer, its options and the delivery time.'),
   ('Factory order', 'With your deposit, I place the order with Goliath, adjusted to your boat.'),
   ('Delivery', 'I hand it over with its papers ready for registration.')],
  faq_h='Frequently asked questions', faq=[
   ('Does the trailer need registering?', 'Yes. In Spain, trailers over 750 kg GVW have their own number plate and pass the ITV inspection. All the trailers on this page are above that weight, so they come with a Spanish COC and technical sheet.'),
   ('Which driving licence do I need?', 'With a B licence you can tow a trailer over 750 kg if the GVW of car and trailer together does not exceed 3,500 kg. Above that you need B96 (up to 4,250 kg) or BE.'),
   ('How long does it take?', 'Lead time depends on the factory; I confirm it in writing when placing the order.'),
   ('Do you have trailers for jet skis or bigger boats?', 'Yes, Goliath builds trailers for jet skis and for boats up to 3,500 kg. Tell me what you need and I will send you options.')],
  small='Prices excluding VAT, per unit, delivered in the Barcelona area. Registration, ITV inspection and paperwork fees are not included. Indicative information: it may change and is not binding; the final price is the one in the written quote. Registration and licence rules are a summary: check them with your agent or the DGT.',
  alt_o='Goliath Océane single-axle trailer', alt_s='Goliath Satellite single-axle trailer',
 ),
 'fr': dict(
  title='Remorques Goliath pour bateaux : prix à Barcelone',
  desc='Remorques Goliath Océane et Satellite pour bateaux jusqu’à 1 800 kg, sur commande. À partir de 3 390 € HT, avec COC et fiche technique espagnols.',
  crumb=('Accueil', 'Bateaux neufs', 'Remorques'), k='Remorques pour bateaux',
  h1='Remorques Goliath pour votre bateau',
  lead='Remorques galvanisées à rouleaux pour emmener votre bateau de chez vous à la cale. Je les commande à l’usine ajustées à votre bateau et je vous accompagne jusqu’à l’immatriculation.',
  cta='Demander un prix pour mon bateau', wa='Bonjour Juan, je souhaite des informations sur une remorque Goliath pour mon bateau.',
  vat='HT', from_='À partir de',
  oce_h='Océane', oce_p='La gamme la plus vendue de Goliath : robuste, rouleaux de 90 mm, treuil Goliath, feux rétractables et garde-boue noirs. Une longueur fixe par modèle.',
  sat_h='Satellite', sat_p='Un cran au-dessus : rouleaux de 110 mm, feux LED rétractables, système d’arrimage QuickFlex et garantie étendue sur les pièces de freinage. Chaque modèle existe en trois longueurs, sans surcoût, pour s’adapter à votre coque.',
  th=('Modèle', 'PTAC', 'Charge utile', 'Longueur', 'Prix'), sat_len='au choix',
  inc_h='Ce qui est inclus avec moi', inc=[
   ('Aide au choix', 'Nous calculons le poids réel de votre bateau avec moteur, carburant et équipement, et choisissons une remorque avec de la marge.'),
   ('Ajustée à votre bateau', 'Je transmets à l’usine les mesures de votre coque pour ajuster la longueur, la hauteur du support de treuil et les rouleaux.'),
   ('Papiers pour l’immatriculation', 'Chaque remorque est livrée avec COC et fiche technique espagnols. Je vous accompagne pour l’ITV et l’immatriculation.'),
   ('Livraison à Barcelone', 'Vous la recevez dans la région de Barcelone et je vous la présente avant d’atteler.')],
  how_h='Comment commander', how=[('Parlez-moi de votre bateau', 'Modèle, longueur, poids et moteur. Si vous avez les papiers sous la main, c’est encore mieux.'),
   ('Je vous envoie un devis', 'Par écrit, avec la remorque choisie, ses options et le délai de livraison.'),
   ('Commande à l’usine', 'Avec votre acompte, je passe la commande à Goliath, ajustée à votre bateau.'),
   ('Livraison', 'Je vous la remets avec ses papiers prêts pour l’immatriculation.')],
  faq_h='Questions fréquentes', faq=[
   ('Faut-il immatriculer la remorque ?', 'Oui. En Espagne, les remorques de plus de 750 kg de PTAC ont leur propre immatriculation et passent l’ITV. Toutes celles de cette page dépassent ce poids, elles sont donc livrées avec COC et fiche technique espagnols.'),
   ('Quel permis faut-il ?', 'Avec le permis B, vous pouvez tracter une remorque de plus de 750 kg si le PTAC cumulé de la voiture et de la remorque ne dépasse pas 3 500 kg. Au-delà, il faut le B96 (jusqu’à 4 250 kg) ou le BE.'),
   ('Quel est le délai ?', 'Le délai dépend de l’usine ; je vous le confirme par écrit lors de la commande.'),
   ('Avez-vous des remorques pour jet-skis ou plus grands bateaux ?', 'Oui, Goliath fabrique des remorques pour jet-skis et pour bateaux jusqu’à 3 500 kg. Dites-moi ce dont vous avez besoin et je vous envoie des options.')],
  small='Prix hors TVA, à l’unité, livrés dans la région de Barcelone. Immatriculation, ITV et frais de gestion non inclus. Information indicative : elle peut changer et n’est pas contractuelle ; le prix final est celui du devis écrit. Les règles d’immatriculation et de permis sont un résumé : vérifiez-les auprès de votre gestionnaire ou de la DGT. Nous ne parlons pas français : nous utilisons un traducteur.',
  alt_o='Remorque Goliath Océane à un essieu', alt_s='Remorque Goliath Satellite à un essieu',
 ),
}

CSS = """<style>
.rm{color:var(--ink,#0E3042)}
.rm .wrap{max-width:1120px;margin:0 auto;padding:0 20px}
.rm-crumb{font-size:.85rem;color:#5b6b75;margin:18px 0 0}.rm-crumb a{color:inherit}
.rm-hero{display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center;padding:28px 0 36px}
.rm-hero .k{font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:#5b6b75;margin:0 0 8px}
.rm-hero h1{font-size:clamp(1.8rem,4vw,2.6rem);line-height:1.12;margin:6px 0 14px}
.rm-hero .lead{font-size:1.06rem;line-height:1.6;color:#33474f;margin:0 0 18px}
.rm-hero .from{font-size:1.25rem;font-weight:700;margin:0 0 20px}.rm .vat{color:#C0392B;font-weight:700;font-size:.85em;margin-left:4px}
.rm-logo{height:64px;width:auto;display:block;margin:0 0 6px}
.rm-hero img.ph{width:100%;height:auto;border-radius:14px;background:#fff}
.rm-sec{padding:40px 0;border-top:1px solid #e3e9ec}.rm-sec h2{font-size:1.6rem;margin:0 0 10px}.rm-sec>.wrap>p{line-height:1.6;color:#33474f;max-width:760px}
.rm-range{display:grid;grid-template-columns:320px 1fr;gap:28px;align-items:start;margin-top:18px}
.rm-range img{width:100%;height:auto;border-radius:12px;border:1px solid #e3e9ec;background:#fff}
.rm-tw{overflow-x:auto}.rm table{width:100%;border-collapse:collapse;font-size:.95rem;min-width:460px}
.rm th,.rm td{padding:11px 10px;border-bottom:1px solid #e3e9ec;text-align:left;white-space:nowrap}.rm th{font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:#5b6b75}
.rm td.p{font-weight:700}
.rm-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:18px}
.rm-grid>div{border:1px solid #e3e9ec;border-radius:14px;padding:18px;background:#fff}.rm-grid h3{font-size:1.02rem;margin:0 0 8px}.rm-grid p{margin:0;line-height:1.55;color:#33474f;font-size:.95rem}
.rm-grid .n{display:inline-block;width:28px;height:28px;border-radius:50%;background:#0E3042;color:#fff;text-align:center;line-height:28px;font-weight:700;margin-bottom:10px}
.rm-faq details{border-bottom:1px solid #e3e9ec;padding:14px 0}.rm-faq summary{font-weight:700;cursor:pointer}.rm-faq p{line-height:1.6;color:#33474f;margin:10px 0 0}
.rm-end{background:#0E3042;color:#fff;border-radius:16px;padding:30px;margin:40px 0;text-align:center}.rm-end h2{margin:0 0 14px;color:#fff}
.rm-small{font-size:.8rem;color:#5b6b75;line-height:1.5;margin:0 0 36px}
@media(max-width:860px){.rm-hero,.rm-range{grid-template-columns:1fr}.rm-grid{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.rm-grid{grid-template-columns:1fr}}
</style>"""


def build(lg):
    t = T[lg]; P = LANGS[lg]
    src = open(os.path.join(ROOT, P.lstrip('/'), 'squama', 'index.html') if P else os.path.join(ROOT, 'squama', 'index.html'), encoding='utf-8').read()
    h_end = src.find('</head>')
    st = src.find('<style>'); style = src[st:src.find('</style>', st) + 8]
    keep = [l for l in src[:h_end].split('\n') if re.search(r'rel="icon"|barcos\.css|consent\.js|analytics\.js|nav\.css', l)]
    body0 = src.find('<body'); header = src[body0:src.find('</header>') + 9]
    for p2 in LANGS.values():
        header = header.replace(f'{SITE}{p2}/squama/', f'{SITE}{p2}/remolques/')
    foot = src[src.find('<footer'):]
    url = f'{SITE}{P}/remolques/'
    img_o = '/remolques/fotos/remolque-goliath-oceane.jpg'; img_s = '/remolques/fotos/remolque-goliath-satellite.jpg'
    wa = 'https://wa.me/34633742973?text=' + re.sub(r'%20', '%20', __import__('urllib.parse').parse.quote(t['wa']))
    alts = ''.join(f'<link rel="alternate" hreflang="{l2}" href="{SITE}{p2}/remolques/">\n' for l2, p2 in LANGS.items()) + f'<link rel="alternate" hreflang="x-default" href="{SITE}/remolques/">\n'
    offers = [{'@type': 'Offer', 'name': n, 'price': str(p), 'priceCurrency': 'EUR', 'availability': 'https://schema.org/PreOrder',
               'priceSpecification': {'@type': 'UnitPriceSpecification', 'price': str(p), 'priceCurrency': 'EUR', 'valueAddedTaxIncluded': False}}
              for n, *_, p in [(o[0], o[4]) for o in OCE] + [(s[0], s[3]) for s in SAT]]
    ld = {'@context': 'https://schema.org', '@type': 'Product', 'name': t['h1'], 'brand': {'@type': 'Brand', 'name': 'Goliath'},
          'image': [SITE + img_o, SITE + img_s], 'description': t['desc'],
          'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'EUR', 'lowPrice': str(min(o[4] for o in OCE)), 'highPrice': str(max(s[3] for s in SAT)), 'offerCount': str(len(offers)), 'offers': offers}}
    bc = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Plata Marine', 'item': f'{SITE}{P}/'},
        {'@type': 'ListItem', 'position': 2, 'name': t['crumb'][1], 'item': f'{SITE}{P}/barcos-nuevos/'},
        {'@type': 'ListItem', 'position': 3, 'name': t['crumb'][2], 'item': url}]}
    faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}
    head = (f'<!doctype html>\n<html lang="{lg}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{E(t["title"])}</title>\n<meta name="description" content="{E(t["desc"])}">\n<link rel="canonical" href="{url}">\n{alts}'
            f'<meta property="og:title" content="{E(t["title"])}">\n<meta property="og:description" content="{E(t["desc"])}">\n<meta property="og:type" content="website">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{SITE}{img_o}">\n<meta name="twitter:card" content="summary_large_image">\n'
            + '\n'.join(keep) + '\n'
            + ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (bc, ld, faq))
            + style + '\n' + CSS + '\n</head>\n')
    th = ''.join(f'<th scope="col">{h}</th>' for h in t['th'])
    rows_o = ''.join(f'<tr><th scope="row">{n}</th><td>{num(a, lg)} kg</td><td>{num(b, lg)} kg</td><td>{m(c, lg)}</td><td class="p">{eur(p, lg)}<span class="vat">{t["vat"]}</span></td></tr>' for n, a, b, c, p in OCE)
    rows_s = ''.join(f'<tr><th scope="row">{n}</th><td>{num(a, lg)} kg</td><td>{num(b, lg)} kg</td><td>{t["sat_len"]}</td><td class="p">{eur(p, lg)}<span class="vat">{t["vat"]}</span></td></tr>' for n, a, b, p in SAT)
    inc = ''.join(f'<div><h3>{E(h)}</h3><p>{E(p)}</p></div>' for h, p in t['inc'])
    how = ''.join(f'<div><span class="n">{i + 1}</span><h3>{E(h)}</h3><p>{E(p)}</p></div>' for i, (h, p) in enumerate(t['how']))
    faqh = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in t['faq'])
    main = f'''<main class="rm">
<div class="wrap"><p class="rm-crumb"><a href="{P}/">{t["crumb"][0]}</a> · <a href="{P}/barcos-nuevos/">{t["crumb"][1]}</a> · {t["crumb"][2]}</p></div>
<section class="wrap rm-hero"><div><img class="rm-logo" src="/barcos-nuevos/logos/goliath.png" alt="Goliath" width="216" height="216"><p class="k">{t["k"]}</p><h1>{E(t["h1"])}</h1><p class="lead">{E(t["lead"])}</p>
<p class="from">{t["from_"]} {eur(OCE[0][4], lg)}<span class="vat">{t["vat"]}</span></p>
<a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener" data-wa-context="remolques_goliath">{E(t["cta"])}</a></div>
<div><img class="ph" src="{img_o}" alt="{E(t["alt_o"])}" width="880" height="750"></div></section>
<section class="rm-sec" id="oceane"><div class="wrap"><h2>{t["oce_h"]}</h2><p>{E(t["oce_p"])}</p>
<div class="rm-range"><img src="/remolques/fotos/remolque-goliath-oceane-m.jpg" alt="{E(t["alt_o"])}" width="440" height="375" loading="lazy"><div class="rm-tw"><table><thead><tr>{th}</tr></thead><tbody>{rows_o}</tbody></table></div></div></div></section>
<section class="rm-sec" id="satellite"><div class="wrap"><h2>{t["sat_h"]}</h2><p>{E(t["sat_p"])}</p>
<div class="rm-range"><img src="/remolques/fotos/remolque-goliath-satellite-m.jpg" alt="{E(t["alt_s"])}" width="440" height="375" loading="lazy"><div class="rm-tw"><table><thead><tr>{th}</tr></thead><tbody>{rows_s}</tbody></table></div></div></div></section>
<section class="rm-sec"><div class="wrap"><h2>{t["inc_h"]}</h2><div class="rm-grid">{inc}</div></div></section>
<section class="rm-sec"><div class="wrap"><h2>{t["how_h"]}</h2><div class="rm-grid">{how}</div></div></section>
<section class="rm-sec rm-faq"><div class="wrap"><h2>{t["faq_h"]}</h2>{faqh}</div></section>
<div class="wrap"><div class="rm-end"><h2>{E(t["cta"])}</h2><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener" data-wa-context="remolques_goliath">{E(t["cta"])}</a></div>
<p class="rm-small">{E(t["small"])}</p></div>
</main>
'''
    out = head + header + '\n\n' + main + foot
    d = os.path.join(ROOT, P.lstrip('/'), 'remolques') if P else os.path.join(ROOT, 'remolques')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(out)


for lg in LANGS:
    build(lg)
print('ok 4 páginas')
