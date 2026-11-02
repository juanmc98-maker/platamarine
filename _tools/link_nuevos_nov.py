#!/usr/bin/env python3
"""Enlaces contextuales a barcos nuevos (nov 2026) en páginas con tráfico: semirrígidas de ocasión -> Mar.Co;
barcos para Licencia/PNB -> SeaStorm y Squama; guía del primer barco -> SeaStorm. Sin SKIPPER (no junto a barcos baratos).
Idempotente (bloque entre <!--pm-nuevos--> y <!--/pm-nuevos-->), antes de <h2 id="faq">. Uso: python3 _tools/link_nuevos_nov.py"""
import re
L = {'es': '', 'ca': 'ca/', 'en': 'en/', 'fr': 'fr/'}
B = {
 'comprar/semirrigidas-neumaticas-segunda-mano.html': {
  'es': ('¿Y si la prefieres nueva?', 'Si prefieres estrenar, trabajo bajo pedido con <a href="{p}/marco/">Mar.Co</a>: semirrígidas de 7,40 a 13,50 m, open y con camarote, con la tarifa oficial y un configurador con el precio de cada motorización. También tienes <a href="{p}/barcos-nuevos/">todos los barcos nuevos</a> con los que trabajo.'),
  'ca': ('I si la prefereixes nova?', 'Si prefereixes estrenar, treballo sota comanda amb <a href="{p}/marco/">Mar.Co</a>: semirígides de 7,40 a 13,50 m, open i amb camarot, amb la tarifa oficial i un configurador amb el preu de cada motorització. També tens <a href="{p}/barcos-nuevos/">tots els vaixells nous</a> amb què treballo.'),
  'en': ('Would you rather have a new one?', 'If you prefer a new boat, I work to order with <a href="{p}/marco/">Mar.Co</a>: RIBs from 7.40 to 13.50 m, open and with a cabin, with the official price list and a configurator showing the price of each engine option. You can also see <a href="{p}/barcos-nuevos/">all the new boats</a> I work with.'),
  'fr': ('Et si vous le préférez neuf ?', 'Si vous préférez du neuf, je travaille sur commande avec <a href="{p}/marco/">Mar.Co</a> : semi-rigides de 7,40 à 13,50 m, open et avec cabine, avec le tarif officiel et un configurateur indiquant le prix de chaque motorisation. Voir aussi <a href="{p}/barcos-nuevos/">tous les bateaux neufs</a> avec lesquels je travaille.')},
 'comprar/barcos-licencia-navegacion-pnb.html': {
  'es': ('Barcos nuevos que puedes llevar con la Licencia', 'Si buscas uno nuevo: los <a href="{p}/seastorm/">SeaStorm</a> de polietileno, de 3,66 a 5,17 m, se llevan con la Licencia de Navegación (y los de menos de 5 m, sin título con un motor de hasta 15 CV, para uso privado, de día y a 2 millas como máximo). La <a href="{p}/squama/">Squama 21</a>, con 5,86 m de eslora de casco, también se gobierna con la Licencia, de día y hasta 2 millas de un puerto o abrigo.'),
  'ca': ('Vaixells nous que pots portar amb la Llicència', 'Si en busques un de nou: els <a href="{p}/seastorm/">SeaStorm</a> de polietilè, de 3,66 a 5,17 m, es porten amb la Llicència de Navegació (i els de menys de 5 m, sense títol amb un motor de fins a 15 CV, per a ús privat, de dia i a 2 milles com a màxim). La <a href="{p}/squama/">Squama 21</a>, amb 5,86 m d’eslora de buc, també es governa amb la Llicència, de dia i fins a 2 milles d’un port o abric.'),
  'en': ('New boats you can take out with the Licencia', 'If you are after a new one: the polyethylene <a href="{p}/seastorm/">SeaStorm</a> boats, from 3.66 to 5.17 m, can be used with the Licencia de Navegación (and those under 5 m without a licence, with an engine of up to 15 hp, for private use, by day and within 2 miles). The <a href="{p}/squama/">Squama 21</a>, with a 5.86 m hull length, can also be skippered with the Licencia, by day and up to 2 miles from a port or shelter.'),
  'fr': ('Bateaux neufs accessibles avec la Licencia', 'Si vous cherchez du neuf : les <a href="{p}/seastorm/">SeaStorm</a> en polyéthylène, de 3,66 à 5,17 m, se pilotent avec la Licencia de Navegación (et ceux de moins de 5 m sans permis avec un moteur jusqu’à 15 ch, pour un usage privé, de jour et à 2 milles maximum). Le <a href="{p}/squama/">Squama 21</a>, avec 5,86 m de longueur de coque, se pilote aussi avec la Licencia, de jour et jusqu’à 2 milles d’un port ou abri.')},
 'guias/primer-barco-guia-para-empezar.html': {
  'es': ('¿Y un primer barco nuevo y sencillo?', 'Si prefieres empezar con uno nuevo y sin complicaciones, los <a href="{p}/seastorm/">SeaStorm</a> son de polietileno, de una sola pieza y sin gelcoat que pulir, de 3,66 a 5,17 m y desde 4.454 € + impuestos sin motor. Los de menos de 5 m se pueden llevar sin título con un motor de hasta 15 CV, para uso privado, de día y a 2 millas como máximo.'),
  'ca': ('I un primer vaixell nou i senzill?', 'Si prefereixes començar amb un de nou i sense complicacions, els <a href="{p}/seastorm/">SeaStorm</a> són de polietilè, d’una sola peça i sense gelcoat per polir, de 3,66 a 5,17 m i des de 4.454 € + impostos sense motor. Els de menys de 5 m es poden portar sense títol amb un motor de fins a 15 CV, per a ús privat, de dia i a 2 milles com a màxim.'),
  'en': ('What about a simple new first boat?', 'If you would rather start with a new, no-fuss boat, <a href="{p}/seastorm/">SeaStorm</a> boats are one-piece polyethylene with no gelcoat to polish, from 3.66 to 5.17 m and from €4,454 + taxes without engine. In Spain, those under 5 m can be used without a licence with an engine of up to 15 hp, for private use, by day and within 2 miles.'),
  'fr': ('Et un premier bateau neuf et simple ?', 'Si vous préférez commencer avec un bateau neuf et sans souci, les <a href="{p}/seastorm/">SeaStorm</a> sont en polyéthylène d’une seule pièce, sans gelcoat à polir, de 3,66 à 5,17 m et dès 4 454 € + taxes sans moteur. En Espagne, ceux de moins de 5 m se pilotent sans permis avec un moteur jusqu’à 15 ch, pour un usage privé, de jour et à 2 milles maximum.')},
}
n = 0
for rel, d in B.items():
    for l, p in L.items():
        f = p + rel
        h = open(f, encoding='utf-8').read()
        h2 = re.sub(r'<!--pm-nuevos-->.*?<!--/pm-nuevos-->\n?', '', h, flags=re.S)
        t, txt = d[l]
        blk = f'<!--pm-nuevos--><h2 id="nuevos">{t}</h2><p>{txt.format(p="/" + p.rstrip("/") if p else "")}</p><!--/pm-nuevos-->\n'
        i = h2.find('<h2 id="faq">')
        assert i > 0, f
        h2 = h2[:i] + blk + h2[i:]
        if h2 != h:
            open(f, 'w', encoding='utf-8').write(h2); n += 1
print(n)
