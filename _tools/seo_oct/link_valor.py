# -*- coding: utf-8 -*-
"""Enlaza /cuanto-vale-mi-barco/ y las guías de valor fiscal y tasación desde herramientas, guías y papeles (4 idiomas). Idempotente."""
import re, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
IMG_VF = 'https://images.unsplash.com/photo-1625225233840-695456021cde?auto=format&fit=crop&w=800&q=70'
IMG_TS = 'https://images.unsplash.com/photo-1708023987502-476c3db22373?auto=format&fit=crop&w=800&q=70'
D = {
 'es': dict(old=('¿Cuánto vale mi barco?', '¿Qué influye en el precio de mi barco?'), new=('Vender', '¿Cuánto vale mi barco?', 'Precio orientativo por modelo, año y estado, con datos de mercado', 'Abrir'),
   g=[('valor-fiscal-barco-tablas-hacienda.html', IMG_VF, 'Fiscalidad', 'Valor fiscal de un barco: las tablas de Hacienda y cómo se calcula', 'Casco, motor y años de uso: cómo valora Hacienda un barco para el ITP y por qué no es lo que vale en el mercado.', 'Leer la guía →'),
      ('tasacion-barco.html', IMG_TS, 'Comprar y vender', 'Tasación de un barco: valoración, peritaje y cuándo necesitas cada uno', 'Qué diferencia hay entre valorar, peritar y tasar un barco usado, quién lo hace y qué revisa un perito.', 'Leer la guía →')]),
 'ca': dict(old=('Quant val el meu vaixell?', 'Què influeix en el preu del meu vaixell?'), new=('Vendre', 'Quant val el meu vaixell?', 'Preu orientatiu per model, any i estat, amb dades de mercat', 'Obrir'),
   g=[('valor-fiscal-barco-tablas-hacienda.html', IMG_VF, 'Fiscalitat', "Valor fiscal d'un vaixell: les taules d'Hisenda i com es calcula", "Buc, motor i anys d'ús: com valora Hisenda un vaixell per a l'ITP i per què no és el que val al mercat.", 'Llegir la guia →'),
      ('tasacion-barco.html', IMG_TS, 'Comprar i vendre', "Taxació d'un vaixell: valoració, peritatge i quan necessites cadascun", "Quina diferència hi ha entre valorar, peritar i taxar un vaixell usat, qui ho fa i què revisa un perit.", 'Llegir la guia →')]),
 'en': dict(old=('How much is my boat worth?', 'What affects my boat’s price?'), new=('Sell', 'How much is my boat worth?', 'Guide price by model, year and condition, from market data', 'Open'),
   g=[('valor-fiscal-barco-tablas-hacienda.html', IMG_VF, 'Tax', 'Tax value of a boat in Spain: the official tables and how it is calculated', 'Hull, engine and years of use: how the Spanish tax office values a boat for transfer tax, and why it is not market value.', 'Read the guide →'),
      ('tasacion-barco.html', IMG_TS, 'Buying and selling', 'Boat valuation and survey: what each one is and when you need it', 'The difference between a valuation, a survey and a formal valuation, who does them and what a surveyor checks.', 'Read the guide →')]),
 'fr': dict(old=('Combien vaut mon bateau ?', 'Qu’est-ce qui influe sur le prix de mon bateau ?'), new=('Vendre', 'Combien vaut mon bateau ?', 'Prix indicatif par modèle, année et état, à partir de données de marché', 'Ouvrir'),
   g=[('valor-fiscal-barco-tablas-hacienda.html', IMG_VF, 'Fiscalité', "Valeur fiscale d'un bateau en Espagne : les barèmes officiels et leur calcul", "Coque, moteur et années d'utilisation : comment le fisc espagnol évalue un bateau pour l'ITP, et pourquoi ce n'est pas sa valeur de marché.", 'Lire le guide →'),
      ('tasacion-barco.html', IMG_TS, 'Achat et vente', "Expertise d'un bateau : estimation, inspection et quand il vous faut chacune", "La différence entre estimer, inspecter et expertiser un bateau d'occasion, qui s'en charge et ce que vérifie un expert.", 'Lire le guide →')]),
}
for l, d in D.items():
    P = '' if l == 'es' else '/' + l
    pth = lambda r: os.path.join(ROOT, (l + '/' if l != 'es' else '') + r)
    # herramientas
    f = pth('herramientas/index.html'); s = open(f, encoding='utf-8').read()
    if '/cuanto-vale-mi-barco/' not in s:
        m = re.search(r'<a class="tl" href="%s/herramientas/valora-tu-barco.html">.*?</a>' % P, s, re.S)
        card = m.group(0).replace('<strong class="tl-h">%s</strong>' % d['old'][0], '<strong class="tl-h">%s</strong>' % d['old'][1])
        new = m.group(0)
        new = re.sub(r'href="[^"]*"', 'href="%s/cuanto-vale-mi-barco/"' % P, new, 1)
        new = re.sub(r'<span class="tl-tag">[^<]*</span><strong class="tl-h">[^<]*</strong><span class="tl-d">[^<]*</span><span class="tl-go">[^<]*</span>',
                     '<span class="tl-tag">%s</span><strong class="tl-h">%s</strong><span class="tl-d">%s</span><span class="tl-go">%s</span>' % d['new'], new)
        s = s.replace(m.group(0), new + card, 1); open(f, 'w', encoding='utf-8').write(s); print('tools', l)
    # guías y papeles
    for idx, pref in (('guias/index.html', ''), ('papeles-fiscalidad/index.html', '../guias/' if l == 'es' else P + '/guias/')):
        f = pth(idx); s = open(f, encoding='utf-8').read()
        anchor = re.search(r'<li><a href="%sitp-comprar-barco-usado-por-comunidad.html">.*?</li>' % re.escape(pref), s, re.S)
        if not anchor: print('NO ANCHOR', f); continue
        add = ''
        for slug, img, tag, h2, p, more in d['g']:
            if (pref + slug) in s: continue
            add += '<li><a href="%s%s"><img src="%s" alt="" loading="lazy"><span class="g-body"><span class="tag">%s</span><h2>%s</h2><p>%s</p><span class="g-more">%s</span></span></a></li>' % (pref, slug, img, tag, h2, p, more)
        if add:
            s = s.replace(anchor.group(0), anchor.group(0) + add, 1); open(f, 'w', encoding='utf-8').write(s); print('idx', f)
