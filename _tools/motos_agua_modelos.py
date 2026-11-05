"""Datos del resto de modelos 2027 (fichas oficiales Sea-Doo y Kawasaki) para build_motos_agua_fichas.py."""

LB = {  # etiquetas de fila
 'es': dict(eng='Motor', pw='Potencia', fu='Depósito', st='Almacenamiento', se='Plazas', hu='Casco', ln='Eslora', wd='Manga', ht='Altura', cw='Peso en orden de marcha', dw='Peso en seco (aprox.)'),
 'ca': dict(eng='Motor', pw='Potència', fu='Dipòsit', st='Emmagatzematge', se='Places', hu='Buc', ln='Eslora', wd='Mànega', ht='Alçada', cw='Pes en ordre de marxa', dw='Pes en sec (aprox.)'),
 'en': dict(eng='Engine', pw='Power', fu='Fuel tank', st='Storage', se='Seats', hu='Hull', ln='Length', wd='Width', ht='Height', cw='Curb weight', dw='Dry weight (approx.)'),
 'fr': dict(eng='Moteur', pw='Puissance', fu='Réservoir', st='Rangement', se='Places', hu='Coque', ln='Longueur', wd='Largeur', ht='Hauteur', cw='Poids en ordre de marche', dw='Poids à sec (env.)')}

HP = {'es': 'cv', 'ca': 'cv', 'en': 'hp', 'fr': 'ch'}
PS = {'es': 'CV', 'ca': 'CV', 'en': 'PS', 'fr': 'ch'}
CC = {'es': 'cc', 'ca': 'cc', 'en': 'cc', 'fr': 'cm³'}
HULL = {'poly': {'es': 'Polytec', 'ca': 'Polytec', 'en': 'Polytec', 'fr': 'Polytec'},
        'fib': {'es': 'Fibra de vidrio', 'ca': 'Fibra de vidre', 'en': 'Fibreglass', 'fr': 'Fibre de verre'},
        'dv': {'es': 'Deep-V', 'ca': 'Deep-V', 'en': 'Deep-V', 'fr': 'Deep-V'}}
NOTE = {'linq_bag': {'es': ' (con bolsa LinQ)', 'ca': ' (amb bossa LinQ)', 'en': ' (incl. LinQ bag)', 'fr': ' (avec sac LinQ)'},
        'linq_cool': {'es': ' (con nevera LinQ)', 'ca': ' (amb nevera LinQ)', 'en': ' (incl. LinQ cooler)', 'fr': ' (avec glacière LinQ)'}}
SEAT2 = {'es': '1 (2 con asiento de pasajero opcional)', 'ca': '1 (2 amb seient de passatger opcional)', 'en': '1 (2 with optional passenger seat)', 'fr': '1 (2 avec selle passager en option)'}
STAND = {'es': '1 (de pie)', 'ca': '1 (dret)', 'en': '1 (stand-up)', 'fr': '1 (à bras)'}
SCENG = {'es': '4 cilindros, 1.498 cc, con compresor e intercooler', 'ca': '4 cilindres, 1.498 cc, amb compressor i intercooler',
         'en': '4-cylinder, 1,498 cc, supercharged with intercooler', 'fr': '4 cylindres, 1 498 cm³, compresseur et intercooler'}
NAENG = {'es': '4 cilindros, 1.498 cc, atmosférico', 'ca': '4 cilindres, 1.498 cc, atmosfèric', 'en': '4-cylinder, 1,498 cc, naturally aspirated', 'fr': '4 cylindres, 1 498 cm³, atmosphérique'}


def n(x, lang, dec=None):
    """número con formato local: 1.498 / 1,498 / 1 498 y decimales con coma o punto"""
    s = f'{x:,.{dec}f}' if dec is not None else (f'{x:,}' if isinstance(x, int) else f'{x:,}')
    if lang == 'en':
        return s
    s = s.replace(',', 'X').replace('.', ',')
    return s.replace('X', ' ' if lang == 'fr' else '.')


def m_(mm, lang):
    return n(mm / 1000, lang, 2 if mm % 10 == 0 else 3) + ' m'


# Sea-Doo: clave, slug, nombre, motor, cv, depósito, almacenamiento, nota, plazas, casco
SD = [
 ('sd-spark-x', 'sea-doo-spark-x-110', 'Spark X 110', 'Rotax 1000 ACE', 110, 30, 44.7, None, 2, 'poly'),
 ('sd-trixx-for3-blue-mist', 'sea-doo-spark-trixx-110', 'Spark Trixx 110', 'Rotax 1000 ACE', 110, 30, 44.7, None, 3, 'poly'),
 ('sd-gti', 'sea-doo-gti-130', 'GTI 130', 'Rotax 1630 ACE', 130, 70, 152.8, None, 3, 'poly'),
 ('sd-gti-se-teal-blue', 'sea-doo-gti-se-170', 'GTI SE 170', 'Rotax 1630 ACE', 170, 70, 152.8, None, 3, 'poly'),
 ('sd-gtx-230', 'sea-doo-gtx-230', 'GTX 230', 'Rotax 1630 ACE', 230, 70, 98.9, None, 3, 'fib'),
 ('sd-gtx-limited', 'sea-doo-gtx-limited-350', 'GTX Limited 350', 'Rotax 1630 ACE', 350, 70, 98.9, None, 3, 'fib'),
 ('sd-explorer-pro', 'sea-doo-explorer-pro-230', 'Explorer Pro 230', 'Rotax 1630 ACE', 230, 70, 198.9, 'linq_bag', 3, 'fib'),
 ('sd-rxp-x-350-solar-orange', 'sea-doo-rxp-x-350', 'RXP-X 350', 'Rotax 1630 ACE', 350, 70, 153.7, None, 'x2', 'fib'),
 ('sd-rxp-x-senna', 'sea-doo-rxp-x-350-senna', 'RXP-X 350 Senna', 'Rotax 1630 ACE', 350, 70, 153.7, None, 'x2', 'fib'),
 ('sd-rxt-x-350-solar-orange', 'sea-doo-rxt-x-350', 'RXT-X 350', 'Rotax 1630 ACE', 350, 70, 98.9, None, 3, 'fib'),
 ('sd-wake-170', 'sea-doo-wake-170', 'Wake 170', 'Rotax 1630 ACE', 170, 70, 152.8, None, 3, 'poly'),
 ('sd-wake-pro-230', 'sea-doo-wake-pro-230', 'Wake Pro 230', 'Rotax 1630 ACE', 230, 70, 98.9, None, 3, 'fib'),
 ('sd-fishpro-trophy', 'sea-doo-fish-pro-trophy-170', 'Fish Pro Trophy 170', 'Rotax 1630 ACE', 170, 70, 153.9, 'linq_cool', 3, 'fib'),
]

# Kawasaki: clave, slug, nombre, compresor, PS, (eslora, manga, altura) mm, depósito, peso orden de marcha, peso seco, plazas
KW = [
 ('kw-ultra-310lx-s-2027', 'kawasaki-ultra-310lx-s', 'Ultra 310LX-S', True, 300, None, 80, None, None, 3),
 ('kw-ultra-160lx-2027', 'kawasaki-ultra-160lx', 'Ultra 160LX', False, 152, (3580, 1195, 1195), 80, 467, 403, 3),
 ('kw-ultra-160lx-s-2027', 'kawasaki-ultra-160lx-s', 'Ultra 160LX-S', False, 152, (3580, 1195, 1175), 80, 456, 392, 3),
 ('kw-ultra-160lx-s-wakesport', 'kawasaki-ultra-160lx-s-wakesport', 'Ultra 160LX-S Wakesport', False, 152, (3580, 1195, 1175), 80, 464, 400, 3),
 ('kw-stx-310rx', 'kawasaki-stx-310rx', 'STX 310RX', True, 300, (3310, None, 1145), 78, 477, 414, 3),
 ('kw-stx-310r', 'kawasaki-stx-310r', 'STX 310R', True, 300, (3310, None, 1120), 78, 472, 409, 3),
 ('kw-stx-160lx-2027', 'kawasaki-stx-160lx', 'STX 160LX', False, 152, (3420, 1185, 1145), 78, 443, 380, 3),
 ('kw-stx-160lx-s-2027', 'kawasaki-stx-160lx-s', 'STX 160LX-S', False, 152, (3420, 1185, 1145), 78, 438, 375, 3),
 ('kw-stx-160r-2027', 'kawasaki-stx-160r', 'STX 160R', False, 152, (3310, 1180, 1120), 78, 423, 360, 3),
 ('kw-stx-160x-2027', 'kawasaki-stx-160x', 'STX 160X', False, 152, (3310, 1180, 1145), 78, 425, 362, 3),
 ('kw-sx-r-160', 'kawasaki-sx-r-160', 'SX-R 160', False, 152, (2655, 765, 840), 23, 250, None, 'stand'),
 ('kw-sx-x-160', 'kawasaki-sx-x-160', 'SX-X 160', False, None, None, None, None, None, None),
]

# Para quién es (es, ca, en, fr) y con qué compararla
WHO = {
 'sd-spark-x': ("La Spark X 110 es la Spark con más genio: 110 cv con el motor Rotax 1000 ACE, el mismo casco ligero de Polytec y audio portátil. Para quien quiere una moto de agua ligera y fácil de remolcar, pero con un punto más de diversión que la Spark básica.",
                "La Spark X 110 és la Spark amb més geni: 110 cv amb el motor Rotax 1000 ACE, el mateix buc lleuger de Polytec i àudio portàtil. Per a qui vol una moto d'aigua lleugera i fàcil de remolcar, però amb un punt més de diversió que la Spark bàsica.",
                "The Spark X 110 is the livelier Spark: 110 hp from the Rotax 1000 ACE, the same light Polytec hull and portable audio. For riders who want a light jet ski that is easy to tow, with more fun than the base Spark.",
                "Le Spark X 110 est le Spark le plus vif : 110 ch avec le moteur Rotax 1000 ACE, la même coque légère en Polytec et l’audio portable. Pour ceux qui veulent un jet-ski léger et facile à remorquer, avec plus de plaisir que le Spark de base.",
                ['sd-spark', 'sd-trixx-for3-blue-mist']),
 'sd-trixx-for3-blue-mist': ("La Spark Trixx 110 es la Spark pensada para jugar: manillar elevado, trim extendido y modo para hacer trucos sobre el agua. Para quien busca diversión y una moto ligera, sin necesidad de grandes potencias.",
                "La Spark Trixx 110 és la Spark pensada per jugar: manillar elevat, trim estès i mode per fer trucs sobre l'aigua. Per a qui busca diversió i una moto lleugera, sense necessitat de grans potències.",
                "The Spark Trixx 110 is the Spark built to play: raised handlebar, extended trim and a mode for tricks on the water. For riders after fun and a light jet ski, without needing big power.",
                "Le Spark Trixx 110 est le Spark fait pour jouer : guidon relevé, trim étendu et un mode pour les figures sur l’eau. Pour ceux qui cherchent le plaisir et un jet-ski léger, sans grosse puissance.",
                ['sd-spark-x', 'sd-spark']),
 'sd-gti': ("La GTI 130 es la Sea-Doo para iniciarse con tres plazas de verdad: estable, con 70 litros de depósito y mucho espacio para guardar cosas. Para familias o grupos que quieren salir tranquilos sin ir a por la máxima potencia.",
            "La GTI 130 és la Sea-Doo per iniciar-se amb tres places de veritat: estable, amb 70 litres de dipòsit i molt espai per guardar coses. Per a famílies o grups que volen sortir tranquils sense anar a buscar la màxima potència.",
            "The GTI 130 is the Sea-Doo to start with three real seats: stable, with a 70-litre tank and plenty of storage. For families or groups who want relaxed rides without chasing top power.",
            "Le GTI 130 est le Sea-Doo pour débuter avec trois vraies places : stable, réservoir de 70 litres et beaucoup de rangement. Pour les familles ou les groupes qui veulent sortir tranquillement sans viser la puissance maximale.",
            ['sd-gti-se-teal-blue', 'kw-stx-160x-2027']),
 'sd-gti-se-teal-blue': ("La GTI SE 170 es la GTI con más motor y mejor equipada: 170 cv, tres plazas y el mismo casco estable de la gama. Para quien sale en familia y quiere margen para tirar de un hinchable o ir cargado.",
            "La GTI SE 170 és la GTI amb més motor i més ben equipada: 170 cv, tres places i el mateix buc estable de la gamma. Per a qui surt en família i vol marge per arrossegar un inflable o anar carregat.",
            "The GTI SE 170 is the better-equipped GTI with more engine: 170 hp, three seats and the same stable hull. For families who want headroom to tow an inflatable or ride loaded.",
            "Le GTI SE 170 est le GTI le mieux équipé et le plus puissant : 170 ch, trois places et la même coque stable. Pour les familles qui veulent de la marge pour tracter une bouée ou rouler chargé.",
            ['sd-gti', 'sd-gtx']),
 'sd-gtx-230': ("La GTX 230 es la Touring de Sea-Doo con un salto de potencia: 230 cv, casco ST3 estable y 70 litros de depósito. Para salir en pareja o en familia, tirar de esquí o hinchable y hacer millas cómodo.",
            "La GTX 230 és la Touring de Sea-Doo amb un salt de potència: 230 cv, buc ST3 estable i 70 litres de dipòsit. Per sortir en parella o en família, arrossegar esquí o inflable i fer milles còmode.",
            "The GTX 230 is Sea-Doo's touring model with a step up in power: 230 hp, a stable ST3 hull and a 70-litre tank. For couples or families who want to tow skis or inflatables and cover miles in comfort.",
            "Le GTX 230 est le modèle de randonnée Sea-Doo avec plus de puissance : 230 ch, coque ST3 stable et réservoir de 70 litres. Pour sortir à deux ou en famille, tracter un ski ou une bouée et faire des milles confortablement.",
            ['sd-gtx', 'kw-ultra-160lx-2027']),
 'sd-gtx-limited': ("La GTX Limited 350 es la Touring más completa de Sea-Doo: 350 cv, casco ST3 y el equipamiento más alto de la gama para viajar cómodo. Para quien sale a menudo, lejos y acompañado, y quiere lo mejor de la marca.",
            "La GTX Limited 350 és la Touring més completa de Sea-Doo: 350 cv, buc ST3 i l'equipament més alt de la gamma per viatjar còmode. Per a qui surt sovint, lluny i acompanyat, i vol el millor de la marca.",
            "The GTX Limited 350 is Sea-Doo's most complete touring model: 350 hp, ST3 hull and the highest equipment level in the range. For riders who go out often, far and with company, and want the brand's best.",
            "Le GTX Limited 350 est le modèle de randonnée le plus complet de Sea-Doo : 350 ch, coque ST3 et le plus haut niveau d’équipement. Pour ceux qui sortent souvent, loin et accompagnés, et veulent le meilleur de la marque.",
            ['kw-ultra-310lx-2027', 'sd-gtx-230']),
 'sd-explorer-pro': ("La Explorer Pro 230 está pensada para travesías: 230 cv, casco ST3, mucho almacenamiento y preparación para llevar equipaje. Para quien quiere hacer rutas largas por la costa con todo lo necesario a bordo.",
            "L'Explorer Pro 230 està pensada per a travessies: 230 cv, buc ST3, molt d'emmagatzematge i preparació per portar equipatge. Per a qui vol fer rutes llargues per la costa amb tot el necessari a bord.",
            "The Explorer Pro 230 is built for long trips: 230 hp, ST3 hull, lots of storage and ready to carry luggage. For riders who want long coastal routes with everything they need on board.",
            "L’Explorer Pro 230 est pensé pour les longues sorties : 230 ch, coque ST3, beaucoup de rangement et prêt à embarquer des bagages. Pour ceux qui veulent de longues balades côtières avec tout le nécessaire à bord.",
            ['sd-gtx-230', 'kw-ultra-310lx-2027']),
 'sd-rxp-x-350-solar-orange': ("La RXP-X 350 es la moto de agua más deportiva de Sea-Doo: 350 cv, casco T3-R pensado para girar fuerte y posición de pilotaje agresiva. Para quien busca prestaciones y sale sobre todo a pilotar.",
            "La RXP-X 350 és la moto d'aigua més esportiva de Sea-Doo: 350 cv, buc T3-R pensat per girar fort i posició de pilotatge agressiva. Per a qui busca prestacions i surt sobretot a pilotar.",
            "The RXP-X 350 is Sea-Doo's sportiest jet ski: 350 hp, a T3-R hull built for hard turns and an aggressive riding position. For riders after performance who go out mainly to ride.",
            "Le RXP-X 350 est le jet-ski le plus sportif de Sea-Doo : 350 ch, coque T3-R faite pour virer fort et position de pilotage agressive. Pour ceux qui cherchent la performance et sortent surtout pour piloter.",
            ['sd-rxt-x-350-solar-orange', 'kw-stx-310r']),
 'sd-rxp-x-senna': ("La RXP-X 350 Senna es la edición especial de la RXP-X con la decoración en homenaje a Ayrton Senna: la misma base deportiva de 350 cv y casco T3-R. Para quien quiere la RXP-X y una unidad diferente.",
            "La RXP-X 350 Senna és l'edició especial de la RXP-X amb la decoració en homenatge a Ayrton Senna: la mateixa base esportiva de 350 cv i buc T3-R. Per a qui vol la RXP-X i una unitat diferent.",
            "The RXP-X 350 Senna is the special edition of the RXP-X with livery honouring Ayrton Senna: the same 350 hp sporty base and T3-R hull. For riders who want an RXP-X that stands apart.",
            "Le RXP-X 350 Senna est l’édition spéciale du RXP-X avec une décoration en hommage à Ayrton Senna : la même base sportive de 350 ch et la coque T3-R. Pour ceux qui veulent un RXP-X différent.",
            ['sd-rxp-x-350-solar-orange', 'sd-rxt-x-350-solar-orange']),
 'sd-rxt-x-350-solar-orange': ("La RXT-X 350 es la deportiva de Sea-Doo para ir con mar: 350 cv, casco ST3 y tres plazas. Para quien quiere prestaciones altas pero también salir acompañado y con estabilidad cuando hay ola.",
            "La RXT-X 350 és l'esportiva de Sea-Doo per anar amb mar: 350 cv, buc ST3 i tres places. Per a qui vol prestacions altes però també sortir acompanyat i amb estabilitat quan hi ha onada.",
            "The RXT-X 350 is Sea-Doo's performance model for rough water: 350 hp, ST3 hull and three seats. For riders who want high performance but also ride with company and stability in waves.",
            "Le RXT-X 350 est le sportif de Sea-Doo pour la mer formée : 350 ch, coque ST3 et trois places. Pour ceux qui veulent de hautes performances tout en sortant accompagnés et stables dans les vagues.",
            ['sd-rxp-x-350-solar-orange', 'kw-ultra-310lx-2027']),
 'sd-wake-170': ("La Wake 170 está preparada para deportes de arrastre: 170 cv, modo esquí, torre o mástil de arrastre y soporte para tabla. Para quien sale a hacer wakeboard, esquí o hinchable con la familia o los amigos.",
            "La Wake 170 està preparada per a esports d'arrossegament: 170 cv, mode esquí, torre o pal d'arrossegament i suport per a taula. Per a qui surt a fer wakeboard, esquí o inflable amb la família o els amics.",
            "The Wake 170 is ready for tow sports: 170 hp, ski mode, tow pylon and board rack. For riders who go wakeboarding, skiing or tubing with family or friends.",
            "Le Wake 170 est prêt pour les sports tractés : 170 ch, mode ski, mât de traction et support de planche. Pour ceux qui font du wakeboard, du ski ou de la bouée en famille ou entre amis.",
            ['sd-wake-pro-230', 'kw-ultra-160lx-s-wakesport']),
 'sd-wake-pro-230': ("La Wake Pro 230 es la versión más completa para arrastre: 230 cv, casco ST3 y equipamiento específico para wakeboard y esquí. Para quien hace deportes de arrastre a menudo y quiere más potencia y estabilidad.",
            "La Wake Pro 230 és la versió més completa per a arrossegament: 230 cv, buc ST3 i equipament específic per a wakeboard i esquí. Per a qui fa esports d'arrossegament sovint i vol més potència i estabilitat.",
            "The Wake Pro 230 is the most complete tow-sports model: 230 hp, ST3 hull and dedicated wakeboard and ski equipment. For riders who tow often and want more power and stability.",
            "Le Wake Pro 230 est la version la plus complète pour les sports tractés : 230 ch, coque ST3 et équipement dédié wakeboard et ski. Pour ceux qui tractent souvent et veulent plus de puissance et de stabilité.",
            ['sd-wake-170', 'kw-ultra-160lx-s-wakesport']),
 'sd-fishpro-trophy': ("La Fish Pro Trophy 170 es la moto de agua de pesca de Sea-Doo: 170 cv, casco estable, sonda y nevera LinQ. Para quien quiere salir a pescar con una embarcación pequeña, ágil y fácil de remolcar.",
            "La Fish Pro Trophy 170 és la moto d'aigua de pesca de Sea-Doo: 170 cv, buc estable, sonda i nevera LinQ. Per a qui vol sortir a pescar amb una embarcació petita, àgil i fàcil de remolcar.",
            "The Fish Pro Trophy 170 is Sea-Doo's fishing jet ski: 170 hp, a stable hull, fish finder and LinQ cooler. For anglers who want a small, agile craft that is easy to tow.",
            "Le Fish Pro Trophy 170 est le jet-ski de pêche de Sea-Doo : 170 ch, coque stable, sondeur et glacière LinQ. Pour les pêcheurs qui veulent une embarcation petite, agile et facile à remorquer.",
            ['sd-explorer-pro', 'sd-gti-se-teal-blue']),
 'kw-ultra-310lx-s-2027': ("La Ultra 310LX-S es la Ultra con compresor y un enfoque más deportivo: 300 CV, casco Deep-V y 80 litros de depósito. Para quien quiere la potencia y la autonomía de la Ultra con un acabado diferente.",
            "La Ultra 310LX-S és la Ultra amb compressor i un enfocament més esportiu: 300 CV, buc Deep-V i 80 litres de dipòsit. Per a qui vol la potència i l'autonomia de la Ultra amb un acabat diferent.",
            "The Ultra 310LX-S is the supercharged Ultra with a sportier focus: 300 PS, Deep-V hull and an 80-litre tank. For riders who want the Ultra's power and range with a different finish.",
            "L’Ultra 310LX-S est l’Ultra à compresseur à l’orientation plus sportive : 300 ch, coque Deep-V et réservoir de 80 litres. Pour ceux qui veulent la puissance et l’autonomie de l’Ultra avec une finition différente.",
            ['kw-ultra-310lx-2027', 'sd-gtx-limited']),
 'kw-ultra-160lx-2027': ("La Ultra 160LX es la Ultra sin compresor: motor de 1.498 cc y 152 CV, el casco grande de la familia y 80 litros de depósito. Para quien quiere estabilidad y autonomía para hacer millas sin ir al tope de potencia.",
            "La Ultra 160LX és la Ultra sense compressor: motor de 1.498 cc i 152 CV, el buc gran de la família i 80 litres de dipòsit. Per a qui vol estabilitat i autonomia per fer milles sense anar al màxim de potència.",
            "The Ultra 160LX is the non-supercharged Ultra: 1,498 cc and 152 PS, the family's large hull and an 80-litre tank. For riders who want stability and range for long rides without top power.",
            "L’Ultra 160LX est l’Ultra sans compresseur : 1 498 cm³ et 152 ch, la grande coque de la famille et un réservoir de 80 litres. Pour ceux qui veulent stabilité et autonomie pour faire des milles sans la puissance maximale.",
            ['sd-gtx', 'kw-ultra-160lx-s-2027']),
 'kw-ultra-160lx-s-2027': ("La Ultra 160LX-S comparte motor de 152 CV y casco con la 160LX, con un acabado y un equipamiento diferentes. Para quien busca una Ultra para hacer millas con un punto más de estilo.",
            "La Ultra 160LX-S comparteix motor de 152 CV i buc amb la 160LX, amb un acabat i un equipament diferents. Per a qui busca una Ultra per fer milles amb un punt més d'estil.",
            "The Ultra 160LX-S shares the 152 PS engine and hull with the 160LX, with a different finish and equipment. For riders who want an Ultra for long rides with a bit more style.",
            "L’Ultra 160LX-S partage le moteur de 152 ch et la coque de la 160LX, avec une finition et un équipement différents. Pour ceux qui veulent une Ultra pour faire des milles avec un peu plus de style.",
            ['kw-ultra-160lx-2027', 'sd-gtx-230']),
 'kw-ultra-160lx-s-wakesport': ("La Ultra 160LX-S Wakesport es la Ultra preparada para deportes de arrastre: 152 CV, casco grande y estable, y equipamiento para wakeboard y esquí. Para quien quiere hacer arrastre con una moto de agua de gran tamaño.",
            "La Ultra 160LX-S Wakesport és la Ultra preparada per a esports d'arrossegament: 152 CV, buc gran i estable, i equipament per a wakeboard i esquí. Per a qui vol fer arrossegament amb una moto d'aigua de gran mida.",
            "The Ultra 160LX-S Wakesport is the Ultra set up for tow sports: 152 PS, a large stable hull and wakeboard and ski equipment. For riders who want to tow with a full-size jet ski.",
            "L’Ultra 160LX-S Wakesport est l’Ultra préparée pour les sports tractés : 152 ch, grande coque stable et équipement wakeboard et ski. Pour ceux qui veulent tracter avec un jet-ski de grande taille.",
            ['sd-wake-pro-230', 'sd-wake-170']),
 'kw-stx-310rx': ("La STX 310RX es la STX más equipada con el motor de compresor: 300 CV en el casco ágil de la STX. Para quien busca prestaciones altas en una moto de agua más compacta que la Ultra.",
            "La STX 310RX és la STX més equipada amb el motor de compressor: 300 CV al buc àgil de la STX. Per a qui busca prestacions altes en una moto d'aigua més compacta que la Ultra.",
            "The STX 310RX is the best-equipped STX with the supercharged engine: 300 PS in the agile STX hull. For riders after high performance in a more compact jet ski than the Ultra.",
            "Le STX 310RX est le STX le mieux équipé avec le moteur à compresseur : 300 ch dans la coque agile du STX. Pour ceux qui cherchent de hautes performances dans un jet-ski plus compact que l’Ultra.",
            ['kw-stx-310r', 'sd-rxt-x-350-solar-orange']),
 'kw-stx-310r': ("La STX 310R lleva el motor de compresor de 300 CV en el casco de la STX, con un planteamiento deportivo. Para quien quiere mucha potencia y agilidad para pilotar.",
            "La STX 310R porta el motor de compressor de 300 CV al buc de la STX, amb un plantejament esportiu. Per a qui vol molta potència i agilitat per pilotar.",
            "The STX 310R puts the 300 PS supercharged engine in the STX hull with a sporty focus. For riders who want lots of power and agility.",
            "Le STX 310R associe le moteur à compresseur de 300 ch à la coque du STX, dans une optique sportive. Pour ceux qui veulent beaucoup de puissance et d’agilité.",
            ['kw-stx-310rx', 'sd-rxp-x-350-solar-orange']),
 'kw-stx-160lx-2027': ("La STX 160LX es la STX más cómoda: motor de 1.498 cc y 152 CV, tres plazas y equipamiento de confort. Para quien quiere una moto de agua versátil para salir en familia y hacer millas.",
            "La STX 160LX és la STX més còmoda: motor de 1.498 cc i 152 CV, tres places i equipament de confort. Per a qui vol una moto d'aigua versàtil per sortir en família i fer milles.",
            "The STX 160LX is the most comfortable STX: 1,498 cc, 152 PS, three seats and comfort equipment. For riders who want a versatile jet ski for family outings and longer rides.",
            "Le STX 160LX est le STX le plus confortable : 1 498 cm³, 152 ch, trois places et équipement de confort. Pour ceux qui veulent un jet-ski polyvalent pour sortir en famille et faire des milles.",
            ['kw-stx-160lx-s-2027', 'sd-gti-se-teal-blue']),
 'kw-stx-160lx-s-2027': ("La STX 160LX-S comparte base con la 160LX (152 CV y tres plazas) con un acabado y un equipamiento diferentes. Para quien quiere una STX versátil con un punto más de estilo.",
            "La STX 160LX-S comparteix base amb la 160LX (152 CV i tres places) amb un acabat i un equipament diferents. Per a qui vol una STX versàtil amb un punt més d'estil.",
            "The STX 160LX-S shares its base with the 160LX (152 PS and three seats) with a different finish and equipment. For riders who want a versatile STX with a bit more style.",
            "Le STX 160LX-S partage sa base avec le 160LX (152 ch et trois places) avec une finition et un équipement différents. Pour ceux qui veulent un STX polyvalent avec un peu plus de style.",
            ['kw-stx-160lx-2027', 'sd-gti-se-teal-blue']),
 'kw-stx-160r-2027': ("La STX 160R es la STX de enfoque deportivo con motor atmosférico: 152 CV, tres plazas y un casco ágil. Para quien quiere una moto de agua divertida y manejable sin ir al compresor.",
            "La STX 160R és la STX d'enfocament esportiu amb motor atmosfèric: 152 CV, tres places i un buc àgil. Per a qui vol una moto d'aigua divertida i manejable sense anar al compressor.",
            "The STX 160R is the sporty STX with a naturally aspirated engine: 152 PS, three seats and an agile hull. For riders who want a fun, easy-to-handle jet ski without the supercharger.",
            "Le STX 160R est le STX à l’orientation sportive avec moteur atmosphérique : 152 ch, trois places et une coque agile. Pour ceux qui veulent un jet-ski amusant et maniable sans compresseur.",
            ['kw-stx-160x-2027', 'sd-gti-se-teal-blue']),
 'kw-stx-160x-2027': ("La STX 160X es la puerta de entrada a la gama STX: 152 CV, tres plazas y el casco ágil de la familia. Para quien quiere una Kawasaki para salir con la familia o los amigos con un presupuesto más contenido.",
            "La STX 160X és la porta d'entrada a la gamma STX: 152 CV, tres places i el buc àgil de la família. Per a qui vol una Kawasaki per sortir amb la família o els amics amb un pressupost més contingut.",
            "The STX 160X is the entry point to the STX range: 152 PS, three seats and the family's agile hull. For riders who want a Kawasaki for outings with family or friends on a tighter budget.",
            "Le STX 160X est l’entrée de gamme STX : 152 ch, trois places et la coque agile de la famille. Pour ceux qui veulent un Kawasaki pour sortir en famille ou entre amis avec un budget plus serré.",
            ['sd-gti', 'kw-stx-160r-2027']),
 'kw-sx-r-160': ("La SX-R 160 es una moto de agua de pie: se pilota de pie, con 152 CV y un casco pensado para saltar y girar. Para pilotos que buscan la sensación más pura y deportiva, no para pasear acompañado.",
            "La SX-R 160 és una moto d'aigua dreta: es pilota dret, amb 152 CV i un buc pensat per saltar i girar. Per a pilots que busquen la sensació més pura i esportiva, no per passejar acompanyat.",
            "The SX-R 160 is a stand-up jet ski: ridden standing, with 152 PS and a hull built to jump and turn. For riders after the purest, sportiest feel, not for cruising with a passenger.",
            "Le SX-R 160 est un jet-ski à bras : on le pilote debout, avec 152 ch et une coque faite pour sauter et virer. Pour les pilotes qui cherchent les sensations les plus pures, pas pour se balader à deux.",
            ['kw-sx-x-160', 'sd-rxp-x-350-solar-orange']),
 'kw-sx-x-160': ("La SX-X 160 es la moto de agua de Kawasaki que combina pilotaje de pie y sentado, con el motor de 4 cilindros y 1.498 cc. Para quien busca una moto deportiva y diferente, con más versatilidad que una moto de pie pura.",
            "La SX-X 160 és la moto d'aigua de Kawasaki que combina pilotatge dret i assegut, amb el motor de 4 cilindres i 1.498 cc. Per a qui busca una moto esportiva i diferent, amb més versatilitat que una moto dreta pura.",
            "The SX-X 160 is Kawasaki's jet ski that combines stand-up and seated riding, with the 4-cylinder 1,498 cc engine. For riders who want something sporty and different, more versatile than a pure stand-up.",
            "Le SX-X 160 est le jet-ski Kawasaki qui combine pilotage debout et assis, avec le moteur 4 cylindres de 1 498 cm³. Pour ceux qui cherchent un jet-ski sportif et différent, plus polyvalent qu’un pur jet à bras.",
            ['kw-sx-r-160', 'sd-rxp-x-350-solar-orange']),
}

AND = {'es': ' y ', 'ca': ' i ', 'en': ' and ', 'fr': ' et '}
TITLE = {'es': '{n} 2027: precio desde {p} y ficha técnica', 'ca': '{n} 2027: preu des de {p} i fitxa tècnica',
         'en': '{n} 2027: price from {p} and specs', 'fr': '{n} 2027 : prix dès {p} et fiche technique'}
DESC = {'es': '{n} 2027 desde {p}{x}. Ficha técnica oficial, fotos y presupuesto por WhatsApp.',
        'ca': "{n} 2027 des de {p}{x}. Fitxa tècnica oficial, fotos i pressupost per WhatsApp.",
        'en': '{n} 2027 from {p}{x}. Official specs, photos and quote on WhatsApp.',
        'fr': '{n} 2027 à partir de {p}{x}. Fiche technique officielle, photos et devis par WhatsApp.'}
SEATS_W = {'es': '{s} plazas', 'ca': '{s} places', 'en': '{s} seats', 'fr': '{s} places'}


SLUGS = {r[0]: r[1] for r in SD + KW}
OLD = {'sd-spark', 'sd-gtx', 'kw-ultra-310lx-2027'}
SLUGS.update({'sd-spark': 'sea-doo-spark', 'sd-gtx': 'sea-doo-gtx-170', 'kw-ultra-310lx-2027': 'kawasaki-ultra-310lx'})


def build(PRICE, money, FROM):
    names = {k: ('Sea-Doo ' + nm) for k, _, nm, *_ in SD}
    names.update({k: ('Kawasaki ' + nm) for k, _, nm, *_ in KW})
    names.update({'sd-spark': 'Sea-Doo Spark', 'sd-gtx': 'Sea-Doo GTX 170', 'kw-ultra-310lx-2027': 'Kawasaki Ultra 310LX'})
    out = []
    for k, slug, nm, eng, hp, fu, stv, note, seats, hull in SD:
        rows, key4, x = {}, {}, {}
        for lg in ('es', 'ca', 'en', 'fr'):
            lb = LB[lg]
            se = SEAT2[lg] if seats == 'x2' else str(seats)
            r = [(lb['eng'], eng), (lb['pw'], f'{hp} {HP[lg]}'), (lb['fu'], f'{fu} l'), (lb['st'], f'{n(stv, lg)} l' + (NOTE[note][lg] if note else '')),
                 (lb['se'], se), (lb['hu'], HULL[hull][lg])]
            rows[lg] = r
            key4[lg] = [(lb['pw'], f'{hp} {HP[lg]}'), (lb['se'], '1-2' if seats == 'x2' else str(seats)), (lb['fu'], f'{fu} l'), (lb['st'], f'{n(stv, lg)} l')]
            x[lg] = f': {hp} {HP[lg]}, ' + SEATS_W[lg].format(s='1-2' if seats == 'x2' else seats)
        out.append((k, slug, 'Sea-Doo', 'Sea-Doo ' + nm, rows, key4, x))
    for k, slug, nm, sc, ps, dims, fu, cw, dw, seats in KW:
        rows, key4, x = {}, {}, {}
        for lg in ('es', 'ca', 'en', 'fr'):
            lb = LB[lg]
            r = [(lb['eng'], SCENG[lg] if sc else NAENG[lg])]
            if ps: r.append((lb['pw'], f'{ps} {PS[lg]}'))
            if dims:
                for lab, v in zip(('ln', 'wd', 'ht'), dims):
                    if v: r.append((lb[lab], m_(v, lg)))
            if fu: r.append((lb['fu'], f'{fu} l'))
            if cw: r.append((lb['cw'], f'{cw} kg'))
            if dw: r.append((lb['dw'], f'{dw} kg'))
            se = STAND[lg] if seats == 'stand' else (str(seats) if seats else None)
            if se: r.append((lb['se'], se))
            if not sc and ps is None: pass
            rows[lg] = r
            k4 = [z for z in r if z[0] in (lb['pw'], lb['se'], lb['fu'], lb['ln'])]
            key4[lg] = k4[:4]
            x[lg] = (f': {ps} {PS[lg]}' if ps else '') + (', ' + SEATS_W[lg].format(s=seats) if isinstance(seats, int) else '')
        out.append((k, slug, 'Kawasaki', 'Kawasaki ' + nm, rows, key4, x))
    M2 = []
    for k, slug, brand, name, rows, key4, x in out:
        who = WHO[k]
        txt = {}
        for i, lg in enumerate(('es', 'ca', 'en', 'fr')):
            p = money(PRICE[k], lg)
            pf = {'es': '', 'ca': '/ca', 'en': '/en', 'fr': '/fr'}[lg]
            alt = AND[lg].join(f'<a href="{pf}/motos-de-agua-nuevas/{SLUGS[a]}{"/" if a in OLD else ""}">{names[a]}</a>' for a in who[4])
            txt[lg] = (TITLE[lg].format(n=name, p=p), DESC[lg].format(n=name, p=p, x=x[lg]), who[i], [], alt)
        M2.append(dict(flat=True, slug=slug, key=k, brand=brand, name=name, price=PRICE[k], rows=rows, key4=key4, txt=txt, alts=who[4]))
    return M2
