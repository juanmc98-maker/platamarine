#!/usr/bin/env python3
"""SEO de las marcas de barcos nuevos (nov 2026): títulos/descripciones, preguntas frecuentes (con FAQPage)
en Mar.Co (marca + 10 modelos), Catharsis y Squama; títulos de SeaStorm y SKIPPER EN/FR.
Idempotente: el bloque de preguntas va entre <!--pm-faq--> ... <!--/pm-faq--> y se reemplaza si ya existe.
Uso (desde la raíz del repo): python3 _tools/seo_marcas_nov.py"""
import re, json, html, glob, os

LANGS = {'es': '', 'ca': 'ca/', 'en': 'en/', 'fr': 'fr/'}

def eur(n, l):
    s = f'{n:,}'
    return '€' + s if l == 'en' else (s.replace(',', ' ') + ' €' if l == 'fr' else s.replace(',', '.') + ' €')

TAX = {'es': '+ impuestos', 'ca': '+ impostos', 'en': '+ taxes', 'fr': '+ taxes'}
FAQ_H = {'es': ('Preguntas frecuentes', 'Preguntas'), 'ca': ('Preguntes freqüents', 'Preguntes'),
         'en': ('Frequently asked questions', 'FAQ'), 'fr': ('Questions fréquentes', 'Questions')}

CSS = ('<style>.pm-faq details{border-bottom:1px solid rgba(14,48,66,.16);scroll-margin-top:70px}'
       '.pm-faq summary{cursor:pointer;font-weight:700;font-size:16.5px;line-height:1.35;padding:18px 34px 18px 0;list-style:none;position:relative}'
       '.pm-faq summary::-webkit-details-marker{display:none}'
       '.pm-faq summary:after{content:"+";position:absolute;right:4px;top:13px;font-size:24px;opacity:.7}'
       '.pm-faq details[open] summary:after{content:"\\2013"}'
       '.pm-faq details p{margin:0 0 18px;line-height:1.6;max-width:760px}'
       '.pm-faq h2{margin-bottom:14px}</style>')

def guide(l, path):
    return '/' + LANGS[l] + path

# ---------------------------------------------------------------- Mar.Co
def marco_cfg(path):
    h = open(path, encoding='utf-8').read()
    return json.loads(re.search(r'MC_CFG\s*=\s*(\{[^<]*\});</script>', h).group(1))

def marco_model_faq(slug, l):
    d = marco_cfg(f'{LANGS[l]}marco/{slug}/index.html')
    es = marco_cfg(f'marco/{slug}/index.html')
    n = d['name']
    sp = dict(es['specs'])
    tit = sp.get('Titulación', 'PER o superior')
    cat = sp.get('Categoría de diseño CE')
    pmax = dict(d['specs']).get({'es': 'Potencia máxima', 'ca': 'Potència màxima', 'en': 'Maximum power', 'fr': 'Puissance maximale'}[l]) or sp['Potencia máxima']
    base, inf = es['base'], es['inf']
    mer = es['mer'][0]
    total = base + mer[1]
    iedmt = slug != 'twentythree'
    pnb = tit.startswith('PNB')
    t = TAX[l]
    tg = guide(l, 'titulaciones/')
    ig = guide(l, 'guias/impuesto-matriculacion-barcos')
    if l == 'es':
        q = [(f'¿Cuánto cuesta la {n} en España?',
              f'Según la tarifa oficial de Mar.Co, desde {eur(base,l)} {t} sin motores' + (f' (la versión por infusión, desde {eur(inf,l)} {t})' if inf else '') +
              f'. Con {mer[0]} sale por {eur(total,l)} {t}, con el equipamiento de serie. El IVA, ' + ('el impuesto de matriculación, ' if iedmt else '') +
              'el transporte y la matriculación van aparte: te lo detallo todo en el presupuesto por escrito.'),
             ('¿Paga impuesto de matriculación?',
              (f'Sí. Su eslora documentada supera los 8 m, y los barcos de recreo de más de 8 m pagan, con carácter general, el impuesto especial de matriculación (IEDMT) al matricularse por primera vez en España, salvo exenciones. Te lo calculo en el presupuesto. <a href="{ig}">Cómo funciona este impuesto</a>.' if iedmt else
               f'No. Su eslora documentada está por debajo de 8 m, y el impuesto especial de matriculación (IEDMT) solo se aplica, con carácter general, a los barcos de recreo de más de 8 m. Sí hay tasas de matriculación, que van en el presupuesto. <a href="{ig}">Cómo funciona este impuesto</a>.')),
             ('¿Qué titulación necesito?',
              (f'El {"PNB" if pnb else "PER"} o un título superior.' + (f' Es de categoría de diseño CE {cat}.' if cat else '') + f' <a href="{tg}">Ver titulaciones</a>.'))]
        if inf:
            q.append(('¿Estándar o con laminado por infusión?',
                      f'La versión por infusión cuesta {eur(inf-base,l)} más ({t}). En las dos el casco es de fibra; en la de infusión la resina entra con vacío, con lo que se controla mejor la cantidad de resina y el laminado sale más uniforme y, normalmente, más ligero. Lo tienes explicado en el configurador.'))
        q += [('¿Puedo montar otros motores?',
               f'Sí. En el configurador tienes el precio de cada motorización Mercury; si prefieres otra marca, te la presupuesto aparte. Siempre sin pasar de la potencia máxima de su placa CE: {pmax}.'),
              ('¿Cuánto tarda la entrega?',
               'Se fabrica bajo pedido. El plazo depende de la producción del astillero y se confirma siempre por escrito antes de hacer el pedido. El transporte hasta Barcelona se presupuesta aparte.')]
    elif l == 'ca':
        q = [(f'Quant costa la {n} a Espanya?',
              f'Segons la tarifa oficial de Mar.Co, des de {eur(base,l)} {t} sense motors' + (f' (la versió per infusió, des de {eur(inf,l)} {t})' if inf else '') +
              f'. Amb {mer[0]} surt per {eur(total,l)} {t}, amb l’equipament de sèrie. L’IVA, ' + ('l’impost de matriculació, ' if iedmt else '') +
              'el transport i la matriculació van a part: t’ho detallo tot al pressupost per escrit.'),
             ('Paga impost de matriculació?',
              (f'Sí. La seva eslora documentada supera els 8 m, i les embarcacions d’esbarjo de més de 8 m paguen, amb caràcter general, l’impost especial de matriculació (IEDMT) en matricular-se per primer cop a Espanya, llevat d’exempcions. T’ho calculo al pressupost. <a href="{ig}">Com funciona aquest impost</a>.' if iedmt else
               f'No. La seva eslora documentada és inferior a 8 m, i l’impost especial de matriculació (IEDMT) només s’aplica, amb caràcter general, a les embarcacions d’esbarjo de més de 8 m. Sí que hi ha taxes de matriculació, que van al pressupost. <a href="{ig}">Com funciona aquest impost</a>.')),
             ('Quina titulació necessito?',
              (f'El {"PNB" if pnb else "PER"} o un títol superior.' + (f' És de categoria de disseny CE {cat}.' if cat else '') + f' <a href="{tg}">Veure titulacions</a>.'))]
        if inf:
            q.append(('Estàndard o amb laminat per infusió?',
                      f'La versió per infusió costa {eur(inf-base,l)} més ({t}). A les dues el buc és de fibra; a la d’infusió la resina entra amb buit, amb la qual cosa es controla millor la quantitat de resina i el laminat surt més uniforme i, normalment, més lleuger. Ho tens explicat al configurador.'))
        q += [('Hi puc posar altres motors?',
               f'Sí. Al configurador tens el preu de cada motorització Mercury; si prefereixes una altra marca, te la pressuposto a part. Sempre sense passar de la potència màxima de la placa CE: {pmax}.'),
              ('Quant triga l’entrega?',
               'Es fabrica sota comanda. El termini depèn de la producció de la drassana i es confirma sempre per escrit abans de fer la comanda. El transport fins a Barcelona es pressuposta a part.')]
    elif l == 'en':
        tit_en = 'the PNB licence' if pnb else 'the PER licence'
        q = [(f'How much does the {n} cost in Spain?',
              f'On Mar.Co’s official price list, from {eur(base,l)} {t} without engines' + (f' (the infusion version from {eur(inf,l)} {t})' if inf else '') +
              f'. With {mer[0]} it comes to {eur(total,l)} {t}, with the standard equipment. VAT, ' + ('the Spanish registration tax, ' if iedmt else '') +
              'transport and registration are extra: I list everything in the written quote.'),
             ('Does it pay the Spanish registration tax?',
              (f'Yes. Its documented length is over 8 m, and leisure boats over 8 m generally pay the special registration tax (IEDMT) on first registration in Spain, unless an exemption applies. I work it out in the quote. <a href="{ig}">How this tax works</a>.' if iedmt else
               f'No. Its documented length is under 8 m, and the special registration tax (IEDMT) generally only applies to leisure boats over 8 m. There are registration fees, which are in the quote. <a href="{ig}">How this tax works</a>.')),
             ('What licence do I need?',
              (f'In Spain, {tit_en} or higher.' + (f' It is CE design category {cat}.' if cat else '') + f' <a href="{tg}">Licences explained</a>.'))]
        if inf:
            q.append(('Standard or infusion-laminated?',
                      f'The infusion version costs {eur(inf-base,l)} more ({t}). Both hulls are fibreglass; with infusion the resin is drawn in under vacuum, which gives better control of the resin content and a more even, usually lighter, laminate. It is explained in the configurator.'))
        q += [('Can I fit other engines?',
               f'Yes. The configurator shows the price of each Mercury option; if you prefer another brand, I quote it separately. Never above the maximum power on its CE plate: {pmax}.'),
              ('How long is delivery?',
               'It is built to order. Lead time depends on the yard’s production and is always confirmed in writing before the order. Transport to Barcelona is quoted separately.')]
    else:
        tit_fr = 'le PNB' if pnb else 'le PER'
        q = [(f'Combien coûte le {n} en Espagne ?',
              f'Selon le tarif officiel Mar.Co, à partir de {eur(base,l)} {t} sans moteurs' + (f' (la version infusion, à partir de {eur(inf,l)} {t})' if inf else '') +
              f'. Avec {mer[0]}, il revient à {eur(total,l)} {t}, avec l’équipement de série. La TVA, ' + ('la taxe d’immatriculation espagnole, ' if iedmt else '') +
              'le transport et l’immatriculation sont en sus : je détaille tout dans le devis écrit.'),
             ('Paie-t-il la taxe d’immatriculation espagnole ?',
              (f'Oui. Sa longueur documentée dépasse 8 m, et les bateaux de plaisance de plus de 8 m paient en règle générale la taxe spéciale d’immatriculation (IEDMT) lors de leur première immatriculation en Espagne, sauf exonération. Je la calcule dans le devis. <a href="{ig}">Comment fonctionne cette taxe</a>.' if iedmt else
               f'Non. Sa longueur documentée est inférieure à 8 m, et la taxe spéciale d’immatriculation (IEDMT) ne s’applique en règle générale qu’aux bateaux de plaisance de plus de 8 m. Il y a des frais d’immatriculation, inclus dans le devis. <a href="{ig}">Comment fonctionne cette taxe</a>.')),
             ('Quel permis faut-il ?',
              (f'En Espagne, {tit_fr} ou supérieur.' + (f' Il est de catégorie de conception CE {cat}.' if cat else '') + f' <a href="{tg}">Voir les permis</a>.'))]
        if inf:
            q.append(('Standard ou stratifié par infusion ?',
                      f'La version infusion coûte {eur(inf-base,l)} de plus ({t}). Les deux coques sont en fibre ; avec l’infusion, la résine est aspirée sous vide, ce qui permet de mieux maîtriser la quantité de résine et donne un stratifié plus homogène et, en général, plus léger. C’est expliqué dans le configurateur.'))
        q += [('Puis-je monter d’autres moteurs ?',
               f'Oui. Le configurateur indique le prix de chaque motorisation Mercury ; pour une autre marque, je fais un devis à part. Toujours sans dépasser la puissance maximale de sa plaque CE : {pmax}.'),
              ('Quel est le délai de livraison ?',
               'Il est construit sur commande. Le délai dépend de la production du chantier et il est toujours confirmé par écrit avant la commande. Le transport jusqu’à Barcelone est chiffré à part.')]
    return q

def marco_hub_faq(l):
    t = TAX[l]; tg = guide(l, 'titulaciones/'); ig = guide(l, 'guias/impuesto-matriculacion-barcos')
    lo, hi = eur(66000, l), eur(980000, l)
    return {
     'es': [('¿Cuánto cuesta una semirrígida Mar.Co?', f'Con la tarifa oficial, desde {lo} {t} la TwentyThree (7,40 m) hasta {hi} {t} la E-Motion 44 (13,50 m), siempre sin motores. En la página de cada modelo tienes el configurador con el precio de las motorizaciones Mercury y de los opcionales.'),
            ('¿Open o cabinada?', 'Las R-Evolution, la TwentySix y la TwentyThree son open: más bañera y solárium, para salir en el día. Las E-Motion llevan camarote con baño bajo la consola, para dormir a bordo o alargar la temporada.'),
            ('¿Qué modelos pagan impuesto de matriculación?', f'Todos menos la TwentyThree, cuya eslora documentada está por debajo de 8 m. El impuesto especial de matriculación (IEDMT) se aplica, con carácter general, a los barcos de recreo de más de 8 m; te lo calculo en el presupuesto. <a href="{ig}">Cómo funciona este impuesto</a>.'),
            ('¿Qué titulación necesito?', f'Para la TwentyThree, el PNB o un título superior; para el resto de modelos, el PER o superior. <a href="{tg}">Ver titulaciones</a>.'),
            ('¿Cómo se compra una Mar.Co?', 'Configuras el modelo, te paso el presupuesto por escrito con todo (barco, motores, opcionales, transporte e impuestos) y se hace el pedido con la señal que marque el contrato. Se fabrica bajo pedido y el plazo se confirma por escrito antes de pedirla.')],
     'ca': [('Quant costa una semirígida Mar.Co?', f'Amb la tarifa oficial, des de {lo} {t} la TwentyThree (7,40 m) fins a {hi} {t} la E-Motion 44 (13,50 m), sempre sense motors. A la pàgina de cada model tens el configurador amb el preu de les motoritzacions Mercury i dels opcionals.'),
            ('Open o amb cabina?', 'Les R-Evolution, la TwentySix i la TwentyThree són open: més banyera i solàrium, per sortir durant el dia. Les E-Motion porten camarot amb bany sota la consola, per dormir a bord o allargar la temporada.'),
            ('Quins models paguen impost de matriculació?', f'Tots menys la TwentyThree, que té una eslora documentada inferior a 8 m. L’impost especial de matriculació (IEDMT) s’aplica a les embarcacions d’esbarjo de més de 8 m; t’ho calculo al pressupost. <a href="{ig}">Com funciona aquest impost</a>.'),
            ('Quina titulació necessito?', f'Per a la TwentyThree, el PNB o un títol superior; per a la resta de models, el PER o superior. <a href="{tg}">Veure titulacions</a>.'),
            ('Com es compra una Mar.Co?', 'Configures el model, et passo el pressupost per escrit amb tot (vaixell, motors, opcionals, transport i impostos) i es fa la comanda amb el senyal que marqui el contracte. Es fabrica sota comanda i el termini es confirma per escrit abans de demanar-la.')],
     'en': [('How much does a Mar.Co RIB cost?', f'On the official price list, from {lo} {t} for the TwentyThree (7.40 m) to {hi} {t} for the E-Motion 44 (13.50 m), always without engines. Each model page has a configurator with the price of the Mercury engine options and extras.'),
            ('Open or cabin?', 'The R-Evolution range, the TwentySix and the TwentyThree are open boats: more cockpit and sunbathing space, for day trips. The E-Motion models have a cabin with a toilet under the console, to sleep on board or stretch the season.'),
            ('Which models pay the Spanish registration tax?', f'All except the TwentyThree, whose documented length is under 8 m. The special registration tax (IEDMT) applies to leisure boats over 8 m; I work it out in the quote. <a href="{ig}">How this tax works</a>.'),
            ('What licence do I need?', f'In Spain, the PNB licence or higher for the TwentyThree, and the PER or higher for the other models. <a href="{tg}">Licences explained</a>.'),
            ('How do I buy a Mar.Co?', 'You configure the model, I send you a written quote with everything (boat, engines, extras, transport and taxes) and the order is placed with the deposit set in the contract. Boats are built to order and the lead time is confirmed in writing before ordering.')],
     'fr': [('Combien coûte un semi-rigide Mar.Co ?', f'Selon le tarif officiel, de {lo} {t} pour le TwentyThree (7,40 m) à {hi} {t} pour l’E-Motion 44 (13,50 m), toujours sans moteurs. Chaque page de modèle a un configurateur avec le prix des motorisations Mercury et des options.'),
            ('Open ou cabine ?', 'Les R-Evolution, le TwentySix et le TwentyThree sont des open : plus de cockpit et de bain de soleil, pour la journée. Les E-Motion ont une cabine avec WC sous la console, pour dormir à bord ou prolonger la saison.'),
            ('Quels modèles paient la taxe d’immatriculation espagnole ?', f'Tous sauf le TwentyThree, dont la longueur documentée est inférieure à 8 m. La taxe spéciale d’immatriculation (IEDMT) s’applique aux bateaux de plaisance de plus de 8 m ; je la calcule dans le devis. <a href="{ig}">Comment fonctionne cette taxe</a>.'),
            ('Quel permis faut-il ?', f'En Espagne, le PNB ou supérieur pour le TwentyThree, et le PER ou supérieur pour les autres modèles. <a href="{tg}">Voir les permis</a>.'),
            ('Comment acheter un Mar.Co ?', 'Vous configurez le modèle, je vous envoie un devis écrit complet (bateau, moteurs, options, transport et taxes) et la commande se fait avec l’acompte prévu au contrat. Construit sur commande ; le délai est confirmé par écrit avant la commande.')],
    }[l]

# ---------------------------------------------------------------- Catharsis
def catharsis_faq(l):
    t = TAX[l]; tg = guide(l, 'titulaciones/'); ig = guide(l, 'guias/impuesto-matriculacion-barcos')
    return {
     'es': [('¿Cuánto cuesta el Catharsis 930?', f'Desde {eur(103990,l)} {t} sin motores. Con dos fuerabordas de 250 cv ya montados son {eur(49490,l)} {t} más, y con un Mercury de 400 cv, {eur(45990,l)} {t} más. El IVA, el impuesto de matriculación, el transporte, los trámites de importación y la matriculación van aparte y te los detallo en el presupuesto.'),
            ('¿Quién fabrica el Catharsis 930?', 'Lo fabrica el astillero Avila Marin, que lo vende con la marca Catharsis. Se hace bajo pedido, con el casco laminado por infusión al vacío.'),
            ('¿Qué titulación necesito?', f'El PER o un título superior. Según el astillero, es de categoría de diseño CE C y está homologado para 8 personas. <a href="{tg}">Ver titulaciones</a>.'),
            ('¿Paga impuesto de matriculación?', f'Sí. Su eslora de casco es de 9,10 m, y los barcos de recreo de más de 8 m pagan, con carácter general, el impuesto especial de matriculación (IEDMT) al matricularse por primera vez en España, salvo exenciones. Te lo calculo en el presupuesto. <a href="{ig}">Cómo funciona este impuesto</a>.'),
            ('¿Se puede dormir a bordo?', 'Sí. Tiene dos camarotes (principal y de invitados) con 4 plazas, un baño y la timonera cerrada, que alarga la temporada.'),
            ('¿Cuánto tarda la entrega?', 'Se fabrica bajo pedido. El plazo depende de la producción del astillero y se confirma siempre por escrito antes del pedido.')],
     'ca': [('Quant costa el Catharsis 930?', f'Des de {eur(103990,l)} {t} sense motors. Amb dos foraborda de 250 cv ja muntats són {eur(49490,l)} {t} més, i amb un Mercury de 400 cv, {eur(45990,l)} {t} més. L’IVA, l’impost de matriculació, el transport, els tràmits d’importació i la matriculació van a part i te’ls detallo al pressupost.'),
            ('Qui fabrica el Catharsis 930?', 'El fabrica la drassana Avila Marin, que el ven amb la marca Catharsis. Es fa sota comanda, amb el buc laminat per infusió al buit.'),
            ('Quina titulació necessito?', f'El PER o un títol superior. Segons la drassana, és de categoria de disseny CE C i està homologat per a 8 persones. <a href="{tg}">Veure titulacions</a>.'),
            ('Paga impost de matriculació?', f'Sí. La seva eslora de buc és de 9,10 m, i les embarcacions d’esbarjo de més de 8 m paguen, amb caràcter general, l’impost especial de matriculació (IEDMT) en matricular-se per primer cop a Espanya, llevat d’exempcions. T’ho calculo al pressupost. <a href="{ig}">Com funciona aquest impost</a>.'),
            ('Es pot dormir a bord?', 'Sí. Té dos camarots (principal i de convidats) amb 4 places, un bany i la timonera tancada, que allarga la temporada.'),
            ('Quant triga l’entrega?', 'Es fabrica sota comanda. El termini depèn de la producció de la drassana i es confirma sempre per escrit abans de la comanda.')],
     'en': [('How much does the Catharsis 930 cost?', f'From {eur(103990,l)} {t} without engines. Twin 250 hp outboards fitted at the yard add {eur(49490,l)} {t}, and a single 400 hp Mercury adds {eur(45990,l)} {t}. VAT, the Spanish registration tax, transport, import formalities and registration are extra and listed in the quote.'),
            ('Who builds the Catharsis 930?', 'It is built by the Avila Marin yard, which sells it under the Catharsis brand. It is built to order, with a vacuum-infused hull.'),
            ('What licence do I need?', f'In Spain, the PER licence or higher. According to the yard, it is CE design category C and rated for 8 people. <a href="{tg}">Licences explained</a>.'),
            ('Does it pay the Spanish registration tax?', f'Yes. Its hull length is 9.10 m, and leisure boats over 8 m generally pay the special registration tax (IEDMT) on first registration in Spain, unless an exemption applies. I work it out in the quote. <a href="{ig}">How this tax works</a>.'),
            ('Can you sleep on board?', 'Yes. It has two cabins (master and guest) with 4 berths, a toilet and a closed wheelhouse that stretches the season.'),
            ('How long is delivery?', 'It is built to order. Lead time depends on the yard’s production and is always confirmed in writing before the order.')],
     'fr': [('Combien coûte le Catharsis 930 ?', f'À partir de {eur(103990,l)} {t} sans moteurs. Deux hors-bord de 250 ch montés au chantier ajoutent {eur(49490,l)} {t}, et un seul Mercury de 400 ch ajoute {eur(45990,l)} {t}. La TVA, la taxe d’immatriculation espagnole, le transport, les formalités d’importation et l’immatriculation sont en sus et détaillés dans le devis.'),
            ('Qui construit le Catharsis 930 ?', 'Il est construit par le chantier Avila Marin, qui le vend sous la marque Catharsis. Il est fabriqué sur commande, avec une coque stratifiée par infusion sous vide.'),
            ('Quel permis faut-il ?', f'En Espagne, le PER ou supérieur. Selon le chantier, il est de catégorie de conception CE C et homologué pour 8 personnes. <a href="{tg}">Voir les permis</a>.'),
            ('Paie-t-il la taxe d’immatriculation espagnole ?', f'Oui. Sa longueur de coque est de 9,10 m, et les bateaux de plaisance de plus de 8 m paient en règle générale la taxe spéciale d’immatriculation (IEDMT) lors de leur première immatriculation en Espagne, sauf exonération. Je la calcule dans le devis. <a href="{ig}">Comment fonctionne cette taxe</a>.'),
            ('Peut-on dormir à bord ?', 'Oui. Il a deux cabines (propriétaire et invités) avec 4 couchages, un WC et une timonerie fermée qui prolonge la saison.'),
            ('Quel est le délai de livraison ?', 'Il est construit sur commande. Le délai dépend de la production du chantier et il est toujours confirmé par écrit avant la commande.')],
    }[l]

# ---------------------------------------------------------------- Squama
def squama_faq(l):
    t = TAX[l]; tg = guide(l, 'titulaciones/')
    p = [eur(x, l) for x in (56000, 59000, 62400, 64500)]
    return {
     'es': [('¿Cuánto cuesta la Squama 21?', f'Con el motor Mercury ya montado y el equipamiento de serie: {p[0]} con el FourStroke 115 CT, {p[1]} con el 150, {p[2]} con el 175 V6 y {p[3]} con el 200 V6, siempre {t}. El IVA, los opcionales, el transporte y la matriculación van aparte.'),
            ('¿Qué titulación necesito?', f'Su eslora de casco (la que consta en los papeles) es de 5,86 m: se puede gobernar con la Licencia de Navegación, de día y hasta 2 millas de un puerto o abrigo. Para navegar más allá de lo que permite la Licencia, el PNB o un título superior, con sus límites. <a href="{tg}">Ver titulaciones</a>.'),
            ('¿Paga impuesto de matriculación?', 'No. El impuesto especial de matriculación (IEDMT) solo se aplica a los barcos de recreo de más de 8 m, y la Squama 21 mide 6,40 m en total.'),
            ('¿Open o Sundeck?', 'Es el mismo casco con dos proas. La Open tiene la proa libre para tomar el sol y moverse; la Sundeck, una proa cerrada con un hueco a cubierto para guardar cosas o echarse un rato.'),
            ('¿Me vale el carnet B para el remolque?', 'Con el carnet B puedes llevar un remolque de hasta 750 kg de masa máxima autorizada, o uno más pesado si el coche y el remolque juntos no pasan de 3.500 kg. La Squama pesa 820 kg sin motor, así que con motor y remolque normalmente se pasa de 750 kg. Si el conjunto pasa de 3.500 kg, hace falta el B96 (hasta 4.250 kg) o el BE, y siempre hay que respetar la masa remolcable de tu coche. Te digo qué remolque encaja con tu barco y con tu coche.'),
            ('¿Cuánto tarda la entrega?', 'Se fabrica bajo pedido. El plazo depende de la producción del astillero y se confirma por escrito en cada pedido; si la quieres para el verano, conviene pedirla con tiempo.')],
     'ca': [('Quant costa la Squama 21?', f'Amb el motor Mercury ja muntat i l’equipament de sèrie: {p[0]} amb el FourStroke 115 CT, {p[1]} amb el 150, {p[2]} amb el 175 V6 i {p[3]} amb el 200 V6, sempre {t}. L’IVA, els opcionals, el transport i la matriculació van a part.'),
            ('Quina titulació necessito?', f'La seva eslora de buc (la que consta als papers) és de 5,86 m: es pot governar amb la Llicència de Navegació, de dia i fins a 2 milles d’un port o abric. Per navegar més enllà del que permet la Llicència, el PNB o un títol superior, amb els seus límits. <a href="{tg}">Veure titulacions</a>.'),
            ('Paga impost de matriculació?', 'No. L’impost especial de matriculació (IEDMT) només s’aplica a les embarcacions d’esbarjo de més de 8 m, i la Squama 21 fa 6,40 m en total.'),
            ('Open o Sundeck?', 'És el mateix buc amb dues proes. L’Open té la proa lliure per prendre el sol i moure’s; la Sundeck, una proa tancada amb un espai cobert per guardar coses o estirar-se una estona.'),
            ('Em serveix el carnet B per al remolc?', 'Amb el carnet B pots portar un remolc de fins a 750 kg de massa màxima autoritzada, o un de més pesat si el cotxe i el remolc junts no passen de 3.500 kg. La Squama pesa 820 kg sense motor, així que amb motor i remolc normalment passa de 750 kg. Si el conjunt passa de 3.500 kg, cal el B96 (fins a 4.250 kg) o el BE, i sempre s\u2019ha de respectar la massa remolcable del cotxe. Et dic quin remolc encaixa amb el teu vaixell i el teu cotxe.'),
            ('Quant triga l’entrega?', 'Es fabrica sota comanda. El termini depèn de la producció de la drassana i es confirma per escrit a cada comanda; si la vols per a l’estiu, convé demanar-la amb temps.')],
     'en': [('How much does the Squama 21 cost?', f'With the Mercury engine fitted and standard equipment: {p[0]} with the FourStroke 115 CT, {p[1]} with the 150, {p[2]} with the 175 V6 and {p[3]} with the 200 V6, always {t}. VAT, extras, transport and registration are extra.'),
            ('What licence do I need?', f'Its hull length (the one in the papers) is 5.86 m, so in Spain it can be skippered with the Licencia de Navegación, by day and up to 2 miles from a port or shelter. Beyond what the Licencia allows, the PNB licence or higher, within its limits. <a href="{tg}">Licences explained</a>.'),
            ('Does it pay the Spanish registration tax?', 'No. The special registration tax (IEDMT) only applies to leisure boats over 8 m, and the Squama 21 is 6.40 m overall.'),
            ('Open or Sundeck?', 'Same hull, two bows. The Open has a free bow to sunbathe and move around; the Sundeck has a closed bow with a covered space to store things or have a rest.'),
            ('Can I tow it with a standard car licence?', 'In Spain a B licence lets you tow a trailer of up to 750 kg gross weight, or a heavier one if car and trailer together are no more than 3,500 kg. The Squama weighs 820 kg without engine, so with engine and trailer it is usually over 750 kg. If the combination exceeds 3,500 kg you need a B96 (up to 4,250 kg) or BE licence, and you must always respect your car\u2019s towing capacity. I tell you which trailer suits your boat and your car.'),
            ('How long is delivery?', 'It is built to order. Lead time depends on the yard’s production and is confirmed in writing for each order; if you want it for the summer, order early.')],
     'fr': [('Combien coûte le Squama 21 ?', f'Avec le moteur Mercury monté et l’équipement de série : {p[0]} avec le FourStroke 115 CT, {p[1]} avec le 150, {p[2]} avec le 175 V6 et {p[3]} avec le 200 V6, toujours {t}. La TVA, les options, le transport et l’immatriculation sont en sus.'),
            ('Quel permis faut-il ?', f'Sa longueur de coque (celle des papiers) est de 5,86 m : en Espagne, il peut être piloté avec la Licencia de Navegación, de jour et jusqu’à 2 milles d’un port ou abri. Au-delà de ce que permet la Licencia, le PNB ou supérieur, dans ses limites. <a href="{tg}">Voir les permis</a>.'),
            ('Paie-t-il la taxe d’immatriculation espagnole ?', 'Non. La taxe spéciale d’immatriculation (IEDMT) ne s’applique qu’aux bateaux de plaisance de plus de 8 m, et le Squama 21 mesure 6,40 m hors tout.'),
            ('Open ou Sundeck ?', 'Même coque, deux proues. L’Open a une proue dégagée pour bronzer et circuler ; le Sundeck, une proue fermée avec un espace couvert pour ranger ou se reposer.'),
            ('Le permis B suffit-il pour la remorque ?', 'En Espagne, le permis B permet de tracter une remorque jusqu’à 750 kg de PTAC, ou plus lourde si voiture et remorque ensemble ne dépassent pas 3 500 kg. Le Squama pèse 820 kg sans moteur : avec moteur et remorque il dépasse en général 750 kg. Si l\u2019ensemble dépasse 3\u202f500 kg, il faut le B96 (jusqu\u2019à 4\u202f250 kg) ou le BE, et toujours respecter la masse remorquable de la voiture. Je vous dis quelle remorque convient à votre bateau et à votre voiture.'),
            ('Quel est le délai de livraison ?', 'Il est construit sur commande. Le délai dépend de la production du chantier et il est confirmé par écrit pour chaque commande ; pour l’été, mieux vaut commander tôt.')],
    }[l]

# ---------------------------------------------------------------- Títulos y descripciones
MARCO_MODELS = ['twentythree', 'twentysix', 'r-evolution-26', 'r-evolution-x27', 'r-evolution-35', 'r-evolution-x36',
                'e-motion-29', 'e-motion-32', 'e-motion-36', 'e-motion-44']
TITLE_MODEL = {'es': '{n} nueva: precio en España y configurador', 'ca': '{n} nova: preu a Espanya i configurador',
               'en': 'New {n}: price in Spain and configurator', 'fr': '{n} neuf : prix en Espagne et configurateur'}
META = {
 'marco/index.html': {
   'es': ('Semirrígidas Mar.Co nuevas: precios en España y modelos', 'Las 10 semirrígidas Mar.Co (Marco), open y cabinadas de 7,40 a 13,50 m, con la tarifa oficial y configurador. Desde 66.000 € + impuestos sin motores.'),
   'ca': ('Semirígides Mar.Co noves: preus a Espanya i models', 'Les 10 semirígides Mar.Co (Marco), open i amb cabina de 7,40 a 13,50 m, amb la tarifa oficial i configurador. Des de 66.000 € + impostos sense motors.'),
   'en': ('New Mar.Co RIBs: prices in Spain and all models', 'All 10 Mar.Co (Marco) RIBs, open and cabin, from 7.40 to 13.50 m, with the official price list and a configurator. From €66,000 + taxes without engines.'),
   'fr': ('Semi-rigides Mar.Co neufs : prix en Espagne et modèles', 'Les 10 semi-rigides Mar.Co (Marco), open et cabine de 7,40 à 13,50 m, avec le tarif officiel et un configurateur. Dès 66 000 € + taxes sans moteurs.')},
 'catharsis/index.html': {
   'es': ('Catharsis 930 de Avila Marin nuevo: precio y ficha', None),
   'ca': ('Catharsis 930 d’Avila Marin nou: preu i fitxa', None),
   'en': ('New Avila Marin Catharsis 930: price and specs', None),
   'fr': ('Catharsis 930 d’Avila Marin neuf : prix et fiche', None)},
 'squama/index.html': {
   'es': ('Squama 21 nueva en España: precio, ficha y fotos', None),
   'ca': ('Squama 21 nova a Espanya: preu, fitxa i fotos', None),
   'en': ('New Squama 21 in Spain: price, specs and photos', None),
   'fr': ('Squama 21 neuf en Espagne : prix, fiche et photos', None)},
 'seastorm/index.html': {
   'es': ('Barcos SeaStorm de polietileno: precios y modelos', None),
   'ca': ('Vaixells SeaStorm de polietilè: preus i models', None),
   'en': ('SeaStorm polyethylene boats: prices and models', None),
   'fr': ('Bateaux SeaStorm en polyéthylène : prix et modèles', None)},
 'skipper/index.html': {
   'en': ('SKIPPER RIBs in Spain: luxury performance RIBs and prices', 'SKIPPER-BSK luxury performance RIBs from 10.85 to 13.40 m for sale in Spain: ACE 360, 38 NC+, 42 NC and ZYARA 440. Photos, specs and prices from €329,000 + taxes.'),
   'fr': ('Semi-rigides SKIPPER en Espagne : RIB de luxe et prix', 'Semi-rigides de luxe SKIPPER-BSK de 10,85 à 13,40 m en vente en Espagne : ACE 360, 38 NC+, 42 NC et ZYARA 440. Photos, fiches et prix dès 329 000 € + taxes.')},
}
SEASTORM_H1 = {'es': ('Barcos de polietileno con 20 años de garantía de casco', 'Barcos SeaStorm de polietileno, con 20 años de garantía de casco'),
               'ca': ('Vaixells de polietilè amb 20 anys de garantia de buc', 'Vaixells SeaStorm de polietilè, amb 20 anys de garantia de buc'),
               'en': ('Polyethylene boats with a 20-year hull warranty', 'SeaStorm polyethylene boats with a 20-year hull warranty'),
               'fr': ('Bateaux en polyéthylène, coque garantie 20 ans', 'Bateaux SeaStorm en polyéthylène, coque garantie 20 ans')}

def set_meta(h, title, desc):
    et = html.escape(title, quote=True)
    h = re.sub(r'<title>.*?</title>', f'<title>{et}</title>', h, count=1, flags=re.S)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + et, h, count=1)
    h = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + et, h, count=1)
    if desc:
        ed = html.escape(desc, quote=True)
        for k in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            h = re.sub(r'(<meta ' + re.escape(k) + r' content=")[^"]*', lambda m: m.group(1) + ed, h, count=1)
    return h

def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))

def faq_block(qs, l, cls):
    t, _ = FAQ_H[l]
    items = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{a}</p></details>' for q, a in qs)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qs]}
    return (f'<!--pm-faq--><section class="{cls} pm-faq" id="preguntas"><div class="wrap">{CSS}<h2>{t}</h2>{items}</div>'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></section><!--/pm-faq-->')

def put_faq(h, qs, l, kind):
    h = re.sub(r'<!--pm-faq-->.*?<!--/pm-faq-->', '', h, flags=re.S)
    cls = 'mm-sec' if kind == 'mm' else 'v2-sec'
    blk = faq_block(qs, l, cls)
    i = h.find('<section class="mm-sec alt" id="presupuesto"') if kind == 'mm' else h.find('<section class="v2-end" id="presupuesto"')
    assert i > 0
    h = h[:i] + blk + h[i:]
    lab = FAQ_H[l][1]
    if kind == 'mm':
        if 'href="#preguntas"' not in h:
            h = h.replace('<a href="#presupuesto" class=q>', f'<a href="#preguntas">{lab}</a><a href="#presupuesto" class=q>', 1)
    else:
        if 'href="#preguntas"' not in h:
            h = re.sub(r'(<nav class="v2-side".*?)(<a href="#presupuesto">)', lambda m: m.group(1) + f'<a href="#preguntas"><span>{lab}</span><i></i></a>' + m.group(2), h, count=1, flags=re.S)
    return h

def rw(path, fn):
    h = open(path, encoding='utf-8').read()
    n = fn(h)
    if n != h:
        open(path, 'w', encoding='utf-8').write(n)
        return True
    return False

changed = []
for l, p in LANGS.items():
    for rel, m in META.items():
        if l in m:
            ti, de = m[l]
            def f(h, ti=ti, de=de, rel=rel, l=l):
                h = set_meta(h, ti, de)
                if rel == 'marco/index.html':
                    h = put_faq(h, marco_hub_faq(l), l, 'v2')
                elif rel == 'catharsis/index.html':
                    h = put_faq(h, catharsis_faq(l), l, 'v2')
                elif rel == 'squama/index.html':
                    h = put_faq(h, squama_faq(l), l, 'v2')
                elif rel == 'seastorm/index.html':
                    a, b = SEASTORM_H1[l]
                    h = h.replace(f'<h1>{a}</h1>', f'<h1>{b}</h1>', 1)
                return h
            if rw(p + rel, f): changed.append(p + rel)
    for s in MARCO_MODELS:
        path = f'{p}marco/{s}/index.html'
        n = marco_cfg(path)['name']
        def f(h, n=n, s=s, l=l):
            h = set_meta(h, TITLE_MODEL[l].format(n=n), None)
            return put_faq(h, marco_model_faq(s, l), l, 'mm')
        if rw(path, f): changed.append(path)
print(len(changed)); print('\n'.join(changed))
