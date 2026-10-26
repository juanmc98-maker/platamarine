# Datos del configurador Kattum: tarifas 2026 del astillero (sin IVA). None = pendiente de cotizar (a consultar).
# Cada texto: (es, ca, en, fr)
ENG_K30 = [
 (('Sin motores', 'Sense motors', 'Without engines', 'Sans moteurs'), 0),
 (('2 × Suzuki 200 cv', '2 × Suzuki 200 CV', '2 × Suzuki 200 hp', '2 × Suzuki 200 ch'), 40000),
 (('2 × Suzuki 250 cv', '2 × Suzuki 250 CV', '2 × Suzuki 250 hp', '2 × Suzuki 250 ch'), 49490),
 (('2 × Suzuki 300 cv, hélices contrarrotantes', '2 × Suzuki 300 CV, hèlixs contrarotatives', '2 × Suzuki 300 hp, counter-rotating propellers', '2 × Suzuki 300 ch, hélices contrarotatives'), 63000),
 (('2 × Mercury 200 cv', '2 × Mercury 200 CV', '2 × Mercury 200 hp', '2 × Mercury 200 ch'), 43000),
 (('2 × Mercury 250 cv', '2 × Mercury 250 CV', '2 × Mercury 250 hp', '2 × Mercury 250 ch'), 56200),
 (('2 × Mercury 300 cv', '2 × Mercury 300 CV', '2 × Mercury 300 hp', '2 × Mercury 300 ch'), 61800),
]
ENG_K40 = [
 (('2 × Mercury 400 cv (de serie)', '2 × Mercury 400 CV (de sèrie)', '2 × Mercury 400 hp (standard)', '2 × Mercury 400 ch (de série)'), 0),
 (('2 × 600 cv', '2 × 600 CV', '2 × 600 hp', '2 × 600 ch'), 76000),
]
_T = {
 'teca': ('Cubierta de teca', 'Coberta de teca', 'Teak deck', 'Pont en teck'),
 'jaima': ('Jaima para popa y proa', 'Haima per a popa i proa', 'Stern and bow bimini', 'Bimini arrière et avant'),
 'jaima_p': ('Jaima para popa', 'Haima per a popa', 'Stern bimini', 'Bimini arrière'),
 'jaima_b': ('Jaima para proa', 'Haima per a proa', 'Bow bimini', 'Bimini avant'),
 'tapi': ('Tapicería premium (espumas antiabsorbentes)', 'Tapisseria prèmium (escumes antiabsorbents)', 'Premium upholstery (quick-dry foam)', 'Sellerie premium (mousses anti-absorption)'),
 'sol': ('Solárium de proa', 'Solàrium de proa', 'Bow sunbed', 'Bain de soleil avant'),
 'puertas': ('Puertas de popa en inox', 'Portes de popa d’inox', 'Stainless stern gates', 'Portes arrière en inox'),
 'fundas': ('Fundas para asientos y consola', 'Fundes per a seients i consola', 'Seat and console covers', 'Housses sièges et console'),
 'toldo': ('Toldo eléctrico', 'Tendal elèctric', 'Electric awning', 'Taud électrique'),
 'carg': ('Cargador de baterías, separador de carga, toma de puerto y cable', 'Carregador de bateries, separador de càrrega, presa de port i cable', 'Battery charger, charge splitter, shore power socket and cable', 'Chargeur de batteries, répartiteur, prise de quai et câble'),
 'nev49': ('Nevera adicional de 49 l', 'Nevera addicional de 49 l', 'Extra 49 l fridge', 'Réfrigérateur supplémentaire 49 l'),
 'nev75': ('Nevera de cajón de 75 l (frigorífico o congelador)', 'Nevera de calaix de 75 l (frigorífic o congelador)', '75 l drawer fridge (fridge or freezer)', 'Réfrigérateur tiroir 75 l (frigo ou congélateur)'),
 'luces': ('Luces subacuáticas', 'Llums subaquàtics', 'Underwater lights', 'Éclairage sous-marin'),
 'preos': ('Preósmosis y antiincrustante', 'Preosmosi i antiincrustant', 'Osmosis protection and antifouling', 'Traitement anti-osmose et antifouling'),
 'color': ('Casco y cubierta en color', 'Buc i coberta en color', 'Coloured hull and deck', 'Coque et pont en couleur'),
 'vhf': ('Radio VHF y antena', 'Ràdio VHF i antena', 'VHF radio and antenna', 'VHF et antenne'),
 'piloto': ('Piloto automático', 'Pilot automàtic', 'Autopilot', 'Pilote automatique'),
 'joy': ('Joystick (con dirección electrohidráulica)', 'Joystick (amb direcció electrohidràulica)', 'Joystick (with electro-hydraulic steering)', 'Joystick (avec direction électro-hydraulique)'),
 'dir': ('Dirección electrohidráulica', 'Direcció electrohidràulica', 'Electro-hydraulic steering', 'Direction électro-hydraulique'),
 'musica': ('Equipo de música premium', 'Equip de música prèmium', 'Premium sound system', 'Système audio premium'),
 'ray12': ('Raymarine de 12", carta y transductor', 'Raymarine de 12", carta i transductor', '12" Raymarine, chart and transducer', 'Raymarine 12", carte et sonde'),
 'pant2': ('2.ª pantalla para los motores', '2a pantalla per als motors', 'Second engine display', '2e écran moteurs'),
 'helice': ('Hélice de proa', 'Hèlix de proa', 'Bow thruster', 'Propulseur d’étrave'),
 'plast': ('Plastificado para transporte', 'Plastificat per al transport', 'Shrink-wrap for transport', 'Film de protection pour le transport'),
 'movil': ('Cargador de móvil inalámbrico', 'Carregador de mòbil sense fil', 'Wireless phone charger', 'Chargeur de téléphone sans fil'),
 'solar': ('Placas solares', 'Plaques solars', 'Solar panels', 'Panneaux solaires'),
 'wc': ('WC eléctrico, tanque de aguas negras y aseo completo', 'WC elèctric, dipòsit d’aigües negres i lavabo complet', 'Electric toilet, holding tank and full head', 'WC électrique, cuve à eaux noires et toilettes complètes'),
 'escal': ('Escalera sobre la plataforma', 'Escala sobre la plataforma', 'Ladder on the platform', 'Échelle sur la plateforme'),
 'seadeck': ('Seadeck en regalas y proa', 'Seadeck a les regales i proa', 'Seadeck on gunwales and bow', 'Seadeck sur les plats-bords et l’avant'),
 'banana': ('Tirador para banana reforzado', 'Tirador reforçat per a banana', 'Reinforced towing point', 'Point de remorquage renforcé'),
 'inverter': ('Inverter', 'Inverter', 'Inverter', 'Onduleur'),
 'bat': ('Batería extra de servicio', 'Bateria extra de servei', 'Extra service battery', 'Batterie de service supplémentaire'),
 'tender': ('Auxiliar de 2 m con motor eléctrico', 'Auxiliar de 2 m amb motor elèctric', '2 m tender with electric motor', 'Annexe de 2 m avec moteur électrique'),
 'cadena': ('Contador de cadena', 'Comptador de cadena', 'Chain counter', 'Compteur de chaîne'),
 'plat': ('Plataforma de baño hidráulica', 'Plataforma de bany hidràulica', 'Hydraulic swim platform', 'Plateforme de bain hydraulique'),
 'cama': ('Cuna para transporte marítimo', 'Bressol per al transport marítim', 'Cradle for sea freight', 'Ber pour le transport maritime'),
 'ac12': ('Aire acondicionado de 12.000 BTU', 'Aire condicionat de 12.000 BTU', '12,000 BTU air conditioning', 'Climatisation 12 000 BTU'),
 'ac16': ('Aire acondicionado de 16.000 BTU', 'Aire condicionat de 16.000 BTU', '16,000 BTU air conditioning', 'Climatisation 16 000 BTU'),
 'gen': ('Generador de 4 kW', 'Generador de 4 kW', '4 kW generator', 'Groupe électrogène 4 kW'),
 'inv3': ('Inversor de 3 kW con 3 baterías de 240 Ah', 'Inversor de 3 kW amb 3 bateries de 240 Ah', '3 kW inverter with 3 × 240 Ah batteries', 'Onduleur 3 kW avec 3 batteries 240 Ah'),
 'hielo': ('Máquina de hielo', 'Màquina de gel', 'Ice maker', 'Machine à glaçons'),
 'tv': ('Televisión interior', 'Televisió interior', 'Interior TV', 'Télévision intérieure'),
}
_K30 = [('teca', None), ('jaima', 1580), ('tapi', 3456), ('sol', 800), ('puertas', None), ('fundas', 650), ('toldo', 2150), ('carg', 1670), ('nev49', 2200), ('nev75', 2750),
        ('luces', 600), ('preos', 2880), ('color', 5184), ('vhf', 1040), ('piloto', None), ('joy', 35712), ('dir', 11520), ('musica', 2300), ('ray12', 3200), ('pant2', None),
        ('helice', None), ('movil', 350), ('solar', 2100), ('wc', 3400), ('escal', 1670), ('seadeck', 1498), ('banana', 300), ('inverter', 350), ('bat', 270)]
_K40 = [('teca', None), ('jaima_p', 3300), ('jaima_b', 3300), ('toldo', 10500), ('fundas', 2900), ('puertas', None), ('tender', 4700), ('carg', 1100), ('nev49', 1900), ('nev75', 2200),
        ('preos', 4000), ('color', 10100), ('vhf', 600), ('piloto', 6500), ('cadena', 1350), ('plat', None), ('musica', 3900), ('ray12', 4100), ('helice', 6900),
        ('movil', 350), ('solar', 2100), ('wc', 2880), ('escal', 1100), ('seadeck', 3100), ('banana', 300), ('inverter', 350), ('bat', 270),
        ('ac12', 10300), ('ac16', 15800), ('gen', 19000), ('inv3', 7900), ('hielo', 2900), ('tv', 1600)]
INC = {'no': ('sin motores', 'sense motors', 'without engines', 'sans moteurs'), 'yes': ('con 2 × Mercury 400 cv', 'amb 2 × Mercury 400 CV', 'with 2 × Mercury 400 hp', 'avec 2 × Mercury 400 ch')}


def cfg(li):
    def opts(lst):
        return [[_T[k][li], p] for k, p in lst]
    def eng(lst):
        return [[t[li], p] for t, p in lst]
    k30_cr = [x for x in _K30 if x[0] != 'sol']
    return {'brand': 'Kattum', 'src': 'kattum', 'models': [
        {'id': 'k30-open', 'name': 'Kattum K30 Open', 'base': 175000, 'inc': INC['no'][li], 'eng': eng(ENG_K30), 'opt': opts(_K30)},
        {'id': 'k30-cruiser', 'name': 'Kattum K30 Cruiser', 'base': 215000, 'inc': INC['no'][li], 'eng': eng(ENG_K30), 'opt': opts(k30_cr)},
        {'id': 'k40', 'name': 'Kattum K40 Open', 'base': 500000, 'inc': INC['yes'][li], 'eng': eng(ENG_K40), 'opt': opts(_K40)},
    ]}
