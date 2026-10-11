# -*- coding: utf-8 -*-
"""Actualiza la sección #temporal de la guía de lista 6ª/7ª (ES/CA/EN/FR) al RD 1188/2025 y enlaza la guía de alquiler."""
import os, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NEW = {
'es': '''<h2 id="temporal">El cambio temporal de uso privado a comercial (actualizado 2026)</h2>
        <p>Desde el 31 de diciembre de 2025, el Real Decreto 1188/2025 regula de forma definitiva lo que en julio de 2025 se abrió de manera provisional: un barco de lista 7ª puede pasar temporalmente a uso comercial, como máximo 3 meses consecutivos por año natural, sin cambiar de lista. Tiene que gestionarlo una empresa de arrendamiento náutico, lleva "CT" delante de la matrícula, pasa los reconocimientos de la lista 6ª y, durante ese periodo, el propietario no puede usarlo ni trabajar a bordo. En Baleares, el Decreto 44/2025 prohíbe esta vía.</p>
        <p>Para un comprador que piense en amortizar el barco alquilándolo algunas semanas, te lo explico con todos los requisitos e impuestos en la guía <a href="alquilar-mi-barco-charter.html">¿Puedo alquilar mi barco para pagar los gastos?</a>. Antes de contar con ello, contrástalo siempre con tu gestoría.</p>

        ''',
'ca': '''<h2 id="temporal">El canvi temporal d'ús privat a comercial (actualitzat 2026)</h2>
        <p>Des del 31 de desembre de 2025, el Reial decret 1188/2025 regula de manera definitiva el que el juliol de 2025 es va obrir de forma provisional: un vaixell de la llista 7a pot passar temporalment a ús comercial, com a màxim 3 mesos consecutius per any natural, sense canviar de llista. L'ha de gestionar una empresa d'arrendament nàutic, porta "CT" davant de la matrícula, passa els reconeixements de la llista 6a i, durant aquest període, el propietari no el pot fer servir ni treballar-hi a bord. A Balears, el Decret 44/2025 prohibeix aquesta via.</p>
        <p>Si ets comprador i penses amortitzar el vaixell llogant-lo algunes setmanes, t'ho explico amb tots els requisits i impostos a la guia <a href="alquilar-mi-barco-charter.html">Puc llogar el meu vaixell per pagar les despeses?</a>. Abans de comptar-hi, contrasta-ho sempre amb la teva gestoria.</p>

        ''',
'en': '''<h2 id="temporal">The temporary switch from private to commercial use (updated 2026)</h2>
        <p>Since 31 December 2025, Royal Decree 1188/2025 has permanently regulated what was opened provisionally in July 2025: a list 7 boat can temporarily switch to commercial use, for a maximum of 3 consecutive months per calendar year, without changing list. It must be managed by a charter company, carries "CT" before the registration number, follows list 6 inspections and, during that period, the owner may not use it or work on board. In the Balearic Islands, Decree 44/2025 bans this route.</p>
        <p>If you’re a buyer thinking of offsetting costs by chartering the boat for a few weeks, I explain all the requirements and taxes in the guide <a href="alquilar-mi-barco-charter.html">Can I charter out my boat to cover the costs?</a>. Before counting on it, always check with your gestoría.</p>

        ''',
'fr': '''<h2 id="temporal">Le passage temporaire de l’usage privé à l’usage commercial (mis à jour en 2026)</h2>
        <p>Depuis le 31 décembre 2025, le décret royal 1188/2025 encadre de façon définitive ce qui avait été ouvert à titre provisoire en juillet 2025 : un bateau en liste 7 peut passer temporairement à l’usage commercial, 3 mois consécutifs maximum par année civile, sans changer de liste. Il doit être géré par une société de location nautique, porte « CT » devant l’immatriculation, suit les inspections de la liste 6 et, pendant cette période, le propriétaire ne peut ni l’utiliser ni travailler à bord. Aux Baléares, le décret 44/2025 interdit cette voie.</p>
        <p>Si vous êtes acheteur et pensez amortir le bateau en le louant quelques semaines, j’explique toutes les exigences et la fiscalité dans le guide <a href="alquilar-mi-barco-charter.html">Puis-je louer mon bateau pour couvrir les frais ?</a>. Avant de compter dessus, vérifiez toujours auprès de votre gestoría.</p>

        ''',
}
TOC = {'es': ('Novedad 2025', 'Cambio temporal (2026)'), 'ca': None, 'en': None, 'fr': None}
for lang, new in NEW.items():
    p = os.path.join(ROOT, ('' if lang == 'es' else lang + '/') + 'guias/lista-6-y-lista-7.html')
    s = open(p, encoding='utf-8').read()
    a = s.index('<h2 id="temporal">'); b = s.index('<h2 id="resumen">', a)
    s = s[:a] + new + s[b:]
    if lang == 'es':
        s = s.replace('<a href="#temporal">Novedad 2025</a>', '<a href="#temporal">Cambio temporal (2026)</a>')
    s = re.sub(r'"dateModified": "[0-9-]+"', '"dateModified": "2026-10-11"', s)
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', p, re.findall(r'<a href="#temporal">([^<]*)</a>', s))
