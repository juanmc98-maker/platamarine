#!/usr/bin/env python3
"""Guía de invernaje del barco (navegante/preparar-barco-fin-de-temporada) en ES/CA/EN/FR.

Reescribe solo el contenido de <main>, el título, la descripción y los datos
estructurados de las cuatro versiones. Cabecera, menú y pie se dejan como están.
Se puede ejecutar varias veces: el resultado es el mismo.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "navegante/preparar-barco-fin-de-temporada"
BASE = "https://www.platamarine.com"
MODIFIED = "2026-11-03"
STORE_KEY = "pm-invernaje-v1"

BOE_339 = "https://www.boe.es/buscar/act.php?id=BOE-A-2021-8268"
BOE_1434 = "https://www.boe.es/eli/es/rd/1999/09/10/1434/con"

CSS = """<style id="pm-inv-css">
.pm-steps{counter-reset:st;list-style:none;padding-left:0!important}
.pm-steps li{counter-increment:st;position:relative;padding-left:40px;margin-bottom:12px}
.pm-steps li::before{content:counter(st);position:absolute;left:0;top:1px;width:26px;height:26px;border-radius:50%;background:var(--sea);color:#fff;font-family:var(--display);font-size:13px;font-weight:600;display:flex;align-items:center;justify-content:center}
.pm-check{background:#fff;border:1px solid rgba(127,146,158,.35);border-radius:10px;padding:20px 18px 8px;margin:8px 0 26px}
.pm-tools{display:flex;flex-wrap:wrap;align-items:center;gap:10px 14px;margin:0 0 6px}
.pm-count{font-family:var(--display);font-weight:600;font-size:15px;color:var(--ink);margin-right:auto}
.pm-bar{height:6px;border-radius:3px;background:var(--paper-2);overflow:hidden;margin:4px 0 14px}
.pm-bar span{display:block;height:100%;width:0;background:var(--wa);transition:width .2s}
.pm-tools button{font-family:var(--display);font-size:14px;font-weight:600;padding:9px 14px;border-radius:4px;cursor:pointer;border:1px solid var(--plata-2);background:transparent;color:var(--ink)}
.pm-tools button.pm-print{background:var(--sea);border-color:var(--sea);color:#fff}
.pm-tools button:hover{border-color:var(--ink)}
.pm-check h3{font-size:1rem;margin:18px 0 6px;color:var(--sea)}
.pm-check ul{list-style:none;padding-left:0!important;margin:0 0 6px}
.pm-check li{margin:0;border-top:1px solid var(--paper-2)}
.pm-check label{display:flex;gap:12px;align-items:flex-start;padding:10px 2px;cursor:pointer;font-size:16px;line-height:1.45}
.pm-check input{flex:0 0 auto;width:20px;height:20px;margin:2px 0 0;accent-color:var(--sea);cursor:pointer}
.pm-check input:checked+span{color:var(--ink-2);text-decoration:line-through;text-decoration-color:var(--plata-2)}
.pm-note{font-size:.9em;color:var(--ink-2);margin:10px 0 12px!important}
.pm-links{display:grid;gap:14px;margin:30px 0 0}
@media (min-width:640px){.pm-links{grid-template-columns:1fr 1fr}}
.pm-links a{display:block;background:#fff;border:1px solid rgba(127,146,158,.35);border-left:3px solid var(--brass);border-radius:6px;padding:16px 18px;text-decoration:none;color:var(--ink)}
.pm-links a:hover{border-color:var(--sea)}
.pm-links strong{display:block;font-family:var(--display);font-size:1rem;margin-bottom:4px}
.pm-links span{display:block;font-size:.92em;color:var(--ink-2)}
.prose .fuentes{font-size:.85em;color:var(--ink-2);margin:28px 0 0;padding-top:16px;border-top:1px solid var(--plata);overflow-wrap:anywhere}
.prose .fuentes ul{margin:6px 0 0}
@media print{
body{background:#fff;font-size:12pt}
body>*:not(main){display:none!important}
.aside,.pm-tools,.pm-links,.pm-bar{display:none!important}
.art{padding:0}
.art .wrap{display:block;padding:0;max-width:none}
.prose{max-width:none}
.pm-check{border:0;padding:0;margin:0}
.pm-check li{break-inside:avoid}
.pm-check h3{break-after:avoid;color:#000}
.pm-check input:checked+span{text-decoration:none;color:#000}
a{color:#000;text-decoration:none}
body.pm-printlist .art header,body.pm-printlist .prose>*:not(#lista-wrap){display:none!important}
body.pm-printlist #lista-wrap .pm-note{display:none}
}
</style>"""

JS = """<script id="pm-inv-js">
(function(){
var KEY='%(key)s',box=document.getElementById('lista-wrap');if(!box)return;
var boxes=box.querySelectorAll('input[type=checkbox][data-k]'),out=box.querySelector('[data-count]'),bar=box.querySelector('.pm-bar span'),tpl=out.getAttribute('data-tpl');
function load(){try{return JSON.parse(localStorage.getItem(KEY)||'{}')||{}}catch(e){return {}}}
function save(){var s={};for(var i=0;i<boxes.length;i++){if(boxes[i].checked)s[boxes[i].getAttribute('data-k')]=1}try{localStorage.setItem(KEY,JSON.stringify(s))}catch(e){}}
function count(){var n=0;for(var i=0;i<boxes.length;i++){if(boxes[i].checked)n++}out.textContent=tpl.replace('{x}',n).replace('{n}',boxes.length);if(bar)bar.style.width=(boxes.length?n/boxes.length*100:0)+'%%'}
var st=load();for(var i=0;i<boxes.length;i++){boxes[i].checked=!!st[boxes[i].getAttribute('data-k')];boxes[i].addEventListener('change',function(){save();count()})}
count();
var p=box.querySelector('[data-print]');if(p)p.addEventListener('click',function(){document.body.classList.add('pm-printlist');window.print()});
window.addEventListener('afterprint',function(){document.body.classList.remove('pm-printlist')});
var r=box.querySelector('[data-reset]');if(r)r.addEventListener('click',function(){if(!window.confirm(r.getAttribute('data-confirm')))return;for(var i=0;i<boxes.length;i++)boxes[i].checked=false;save();count()});
})();
</script>""" % {"key": STORE_KEY}

# Claves estables de la lista (iguales en los cuatro idiomas para que el progreso se comparta)
GROUPS = [
    ("motor", ["aceite", "filtros-comb", "agua-salada", "rodete", "refrigerante", "cola", "combustible", "tapones", "fueraborda"]),
    ("agua", ["agua-dulce", "wc", "sentina"]),
    ("bat", ["bat-carga", "bat-general", "bat-mantenedor"]),
    ("casco", ["anodos", "grifos", "desagues", "amarras", "lona", "obra-viva"]),
    ("vela", ["velas", "jarcia", "winches"]),
    ("interior", ["cojines", "humedad", "nevera", "gas", "electronica", "seguridad", "itb-seguro", "comida"]),
    ("venta", ["carpeta"]),
]
N_ITEMS = sum(len(k) for _, k in GROUPS)

L = {}

# ---------------------------------------------------------------- ES
L["es"] = dict(
    prefix="",
    title="Invernaje del barco: lista para dejarlo listo en invierno",
    desc="Invernaje del barco en el Mediterráneo: motor diésel, gasolina o fueraborda, agua, baterías, casco y lonas. Lista para marcar e imprimir.",
    h1="Invernaje del barco: cómo lo dejo listo para el invierno",
    eyebrow="Guía del navegante · Mantenimiento",
    meta=["Por Juan Morante", "Comprobado el 3 de noviembre de 2026", "12 min de lectura"],
    lead="En otoño se estropean muchos barcos sin salir del amarre. Lo que se hace en estas semanas decide cómo arranca en primavera y, si el barco está en venta, qué impresión da en la visita. Esta es la lista que sigo con el mío, pensada para el Mediterráneo: aquí hiela poco, pero la humedad y los temporales no perdonan.",
    steps_h="La respuesta corta: el invernaje en 5 pasos",
    steps_intro="Si solo tienes cinco minutos, esto es lo que no me salto nunca. El detalle está más abajo y, al final, la <a href=\"#lista\">lista para ir marcando</a>.",
    steps=[
        ("Motor", "Aceite y filtros cambiados, circuito de agua salada enjuagado con agua dulce y el combustible preparado para estar parado, siempre según el manual de tu motor."),
        ("Agua fuera", "Depósitos, calentador, WC y sentina vacíos, limpios y secos."),
        ("Baterías cargadas", "Desconecta todo menos la bomba de achique automática si el barco se queda en el agua."),
        ("Casco y amarre", "Ánodos, grifos de fondo, amarras y defensas revisados. Lona bien sujeta y con ventilación."),
        ("Interior seco", "Ventilación o deshumidificador, gas cerrado y las fechas del equipo de seguridad apuntadas."),
    ],
    howto_name="Invernaje del barco en 5 pasos",
    list_h="Lista de comprobación de invernaje",
    list_note="Marca lo que vayas haciendo. Se queda guardado en este navegador, así que puedes volver otro día y seguir donde lo dejaste. Lo que no aplique a tu barco, sáltatelo.",
    count_tpl="{x} de {n} hechas",
    print_btn="Imprimir lista",
    reset_btn="Desmarcar todo",
    reset_confirm="¿Desmarcar todas las tareas?",
    groups={
        "motor": ("Motor", [
            "Aceite y filtro cambiados con el motor caliente (según el manual)",
            "Filtros de combustible y vaso decantador purgados o cambiados",
            "Circuito de agua salada enjuagado con agua dulce",
            "Rodete de la bomba de agua revisado (o sacado, si el manual lo indica)",
            "Refrigerante del circuito cerrado comprobado",
            "Aceite de la cola, pie o saildrive cambiado y sin rastro lechoso",
            "Combustible: depósito casi lleno y estabilizador si el fabricante lo recomienda",
            "Admisión y escape tapados, con una nota en el contacto",
            "Fueraborda: enjuagado, engrasado y guardado en vertical",
        ]),
        "agua": ("Agua dulce, WC y sentina", [
            "Depósito de agua dulce, tuberías y calentador vaciados",
            "Aguas negras vaciadas en la estación de bombeo y WC aclarado",
            "Sentina limpia y seca; bomba de achique y flotador probados",
        ]),
        "bat": ("Baterías", [
            "Baterías cargadas (litio, al nivel que diga el fabricante) y bornes limpios",
            "Interruptor general desconectado; achique automático alimentado si queda en el agua",
            "Mantenedor con el perfil correcto, o visita cada pocas semanas",
        ]),
        "casco": ("Casco y amarre", [
            "Ánodos revisados y cambiados si están gastados",
            "Grifos de fondo accionados; mangueras y abrazaderas revisadas",
            "Desagües de la bañera e imbornales libres",
            "Amarras dobladas, con protección donde rozan, y defensas puestas",
            "Lona bien sujeta, sin bolsas de agua y con ventilación",
            "En seco: obra viva lavada y revisada (ósmosis, antifouling, hélice)",
        ]),
        "vela": ("Veleros", [
            "Génova fuera del enrollador; velas lavadas, secas y guardadas",
            "Jarcia firme revisada (terminales, crucetas, tensores)",
            "Winches limpios y engrasados según el fabricante",
        ]),
        "interior": ("Interior y seguridad", [
            "Colchonetas de canto o en casa, armarios abiertos",
            "Deshumidificador o absorbentes de humedad colocados",
            "Nevera vacía, limpia y con la puerta entreabierta",
            "Botella de gas cerrada y desconectada; fecha del tubo mirada",
            "Electrónica portátil a casa",
            "Fechas apuntadas: bengalas, extintores, balsa, chalecos, botiquín",
            "Caducidad de la ITB y del seguro apuntadas",
            "Ni comida ni basura a bordo",
        ]),
        "venta": ("Si lo vas a vender", [
            "Carpeta con la documentación y las facturas de mantenimiento",
        ]),
    },
    links=[
        ("/herramientas/libro-mantenimiento-barco", "Libro de mantenimiento del barco (PDF gratis)", "Para apuntar lo que haces cada invierno. Te sirve a ti y, el día que vendas, al comprador."),
        ("/recordatorios-barco/", "Avisos de vencimientos gratis (ITB, seguro…)", "Apunta las fechas una vez y recibe un aviso antes de que caduquen."),
    ],
    sources_h="Fuentes",
    sources=[
        (BOE_339, "BOE: Real Decreto 339/2021, equipo de seguridad y de prevención de la contaminación de las embarcaciones de recreo"),
        (BOE_1434, "BOE: Real Decreto 1434/1999, reconocimientos e inspecciones de las embarcaciones de recreo (ITB)"),
    ],
    sources_tail="Y, por encima de todo, el manual del propietario de tu motor y de cada equipo: manda sobre cualquier lista, también sobre esta.",
    toc_label="Contenido", toc_h="En esta página",
    toc=[("corta", "La respuesta corta"), ("agua-o-seco", "¿En el agua o en seco?"), ("motor", "Motor"), ("agua", "Agua dulce, WC y sentina"),
         ("baterias", "Baterías"), ("casco", "Casco, amarras y lonas"), ("veleros", "Veleros"), ("interior", "Interior y seguridad"),
         ("errores", "Errores que salen caros"), ("lista", "Lista para marcar"), ("venta", "Si está en venta"), ("fuentes", "Fuentes")],
)
L["es"]["body1"] = """
        <h2 id="agua-o-seco">¿En el agua o en seco?</h2>
        <p>En el Mediterráneo muchos barcos pasan el invierno en el agua y no pasa nada, siempre que alguien se pase a mirarlos. En la costa catalana, a pie de mar, hiela poco. Lo que sí hay es humedad, lluvia y temporales de levante que ponen a prueba las amarras.</p>
        <ul>
          <li><strong>En el agua.</strong> Más cómodo y normalmente más barato. El mar hace de colchón térmico y el motor sigue a mano para arrancarlo de vez en cuando. A cambio, necesitas la bomba de achique alimentada, amarras en buen estado y una visita después de cada temporal.</li>
          <li><strong>En seco.</strong> Sin riesgo de hundimiento ni de rozaduras contra el pantalán, y aprovechas para mirar y pintar la obra viva. A cambio, hay que vaciar bien todos los circuitos de agua, dejar el barco bien calzado y pagar la varada y la estancia.</li>
        </ul>
        <div class="ejemplo">
          <p class="eyebrow">Si tu puerto puede helar</p>
          <p>Un pantano, un puerto de interior o un barco guardado en seco tierra adentro sí pueden ver noches bajo cero. Ahí, cualquier circuito con agua que no se pueda vaciar del todo necesita anticongelante, y del tipo que diga el manual. En un amarre a pie de mar suele bastar con vaciar y enjuagar, pero mira las previsiones y no lo des por hecho.</p>
        </div>

        <h2 id="motor">Motor</h2>
        <p>Es lo primero y lo que más cuesta si se descuida. Cada motor tiene su manual de invernaje y manda sobre todo lo que leas aquí. Lo que sigue es el orden que sigo yo.</p>

        <h3 id="diesel">Intraborda diésel</h3>
        <ul>
          <li>Cambio de aceite y filtro con el motor caliente. El aceite usado lleva ácidos que no conviene dejar dentro todo el invierno.</li>
          <li>Filtros de combustible y vaso decantador: purga el agua y cambia los filtros si toca.</li>
          <li>Depósito casi lleno, para que no condense agua dentro. Si has tenido problemas de bacterias en el gasoil, pregunta por un biocida y úsalo como indique el fabricante.</li>
          <li>Circuito de agua salada: enjuágalo con agua dulce. Si el barco puede helar, el manual te dirá si toca pasar anticongelante y cuál.</li>
          <li>Circuito cerrado: comprueba nivel y estado del refrigerante. Si toca cambiarlo por horas o por años, mejor ahora que en mayo.</li>
          <li>Rodete de la bomba de agua: revísalo. Algunos fabricantes recomiendan sacarlo durante el invierno para que no se deforme; si lo haces, deja una nota bien visible.</li>
          <li>Correas, manguitos y abrazaderas: un vistazo buscando grietas u óxido.</li>
          <li>Si lleva saildrive o cola, cambia el aceite y mira que no salga lechoso.</li>
          <li>Tapa la toma de aire y la salida de escape para que no entre humedad, y deja una nota en el contacto para acordarte de quitarlo.</li>
        </ul>
        <p>Un motor con el mantenimiento hecho y anotado en un cuaderno o en las facturas es de los argumentos de venta más baratos que hay. Cuando valoro un barco, un historial claro de mantenimiento pesa más que la mayoría de extras.</p>

        <h3 id="gasolina">Intraborda y dentro-fueraborda de gasolina</h3>
        <ul>
          <li>Aceite y filtro con el motor caliente, igual que en un diésel.</li>
          <li>La gasolina envejece rápido si se queda parada. Añade estabilizador y haz funcionar el motor unos minutos para que llegue a todo el sistema, como indique el fabricante.</li>
          <li>Algunos manuales piden aceite de nebulizar (<em>fogging</em>) en los cilindros, sobre todo en motores de carburación. En los de inyección no siempre se hace así: sigue el tuyo.</li>
          <li>Aceite de la cola: si sale lechoso, hay agua dentro y toca revisar retenes antes de guardar.</li>
          <li>Fuelles de la cola: mira que no tengan grietas. Un fuelle roto puede meter agua en el barco.</li>
          <li>Si el barco puede helar, el bloque y los colectores se vacían por sus tapones o se protegen con anticongelante, según el manual. Un bloque rajado por el hielo es de las averías más caras que hay.</li>
          <li>En primavera, ventila la sala de máquinas antes de arrancar. Con gasolina, siempre.</li>
        </ul>

        <h3 id="fueraborda">Fueraborda</h3>
        <ul>
          <li>Enjuágalo con agua dulce con orejeras o con la toma de lavado que traen muchos modelos. Nunca lo arranques sin agua: el rodete se quema en segundos.</li>
          <li>Combustible: estabilizador y unos minutos en marcha para que llegue a la inyección o al carburador. Algunos fabricantes piden vaciar la cuba del carburador; mira el tuyo.</li>
          <li>Aceite del motor (en los de cuatro tiempos) y aceite de la cola. Si sale lechoso, al taller.</li>
          <li>Engrase de los puntos que marca el manual, ánodos y un vistazo a la hélice.</li>
          <li>Si lo desmontas, guárdalo en vertical para que escurra toda el agua. Si tiene que ir tumbado, hazlo del lado que indique el fabricante; del otro, el aceite puede ir a donde no debe.</li>
          <li>Depósito portátil: cerrado, en un sitio ventilado y lejos de cualquier llama.</li>
        </ul>

        <h2 id="agua">Agua dulce, WC y sentina</h2>
        <ul>
          <li>Vacía el depósito de agua dulce y abre los grifos hasta que la bomba se quede sin agua. Apaga la bomba y deja los grifos abiertos.</li>
          <li>El calentador también se vacía. Es lo primero que se rompe si hiela.</li>
          <li>Si tu puerto puede helar y no puedes vaciarlo todo, usa solo anticongelante apto para agua potable. El del coche es tóxico: ni en el circuito de agua ni en el WC.</li>
          <li>WC: vacía las aguas negras en la estación de bombeo del puerto, aclara con agua dulce y usa el producto que recomiende el fabricante del WC.</li>
          <li>Sentina limpia y seca. Prueba la bomba de achique levantando el flotador con la mano. Si hay restos de aceite, recógelos con absorbentes: el agua con aceite no se bombea al mar.</li>
        </ul>

        <h2 id="baterias">Baterías</h2>
        <p>Una batería que pasa el invierno descargada muchas veces no llega a la primavera. Y una de plomo descargada, además, se puede congelar; cargada, es mucho más difícil.</p>
        <ul>
          <li><strong>Plomo abiertas.</strong> Cárgalas del todo, limpia los bornes y revisa el nivel del electrolito si se puede.</li>
          <li><strong>AGM y gel.</strong> También cargadas del todo, con un cargador que tenga su perfil. Un perfil equivocado las estropea poco a poco.</li>
          <li><strong>Litio (LiFePO4).</strong> Guárdalas al nivel de carga que indique el fabricante, que muchas veces no es el 100 %. No las cargues por debajo de 0 °C salvo que lleven calefacción integrada. El sistema de gestión (BMS) suele cortar la carga con frío, pero no conviene fiarlo todo a eso.</li>
          <li>Desconecta el interruptor general para que nada las vaya vaciando. Si el barco queda en el agua, deja la bomba de achique automática alimentada.</li>
          <li>Si hay corriente en el pantalán, un mantenedor con el perfil correcto las tiene a punto todo el invierno. Si no, pásate cada pocas semanas a mirarlas o llévatelas a casa.</li>
        </ul>

        <h2 id="casco">Casco, ánodos, grifos de fondo, amarras y lonas</h2>
        <h3>Casco y obra viva</h3>
        <p>Si el barco sale del agua, es el momento de mirar la obra viva con calma: ampollas de ósmosis, estado de la antifouling, ejes, cola y hélice (mellas, holgura). Un lavado a presión nada más salir ahorra horas de rascar. Si se queda en el agua, al menos limpia la línea de flotación.</p>
        <h3>Ánodos</h3>
        <p>Revísalos todos: casco, ejes, cola o saildrive y, si tiene, hélice de proa. Si están muy gastados, cámbialos antes de dejar el barco. Un ánodo agotado ya no protege nada, y el invierno es largo.</p>
        <h3>Grifos de fondo</h3>
        <p>En el agua, ábrelos y ciérralos un par de veces para que no se agarroten, y revisa mangueras y abrazaderas. Cierra los que no hagan falta, pero nunca los desagües de la bañera: tienen que poder sacar el agua de lluvia. En seco, déjalos abiertos para que escurran y engrásalos si el modelo lo pide.</p>
        <h3 id="cubierta">Amarras, defensas y lonas</h3>
        <p>Lava con agua dulce toda la cubierta, herrajes y cristales; la sal deja marcas que después cuestan de quitar. Dobla las amarras que más trabajan, pon protección donde rozan y revisa las defensas: es cuando más viento hay y más días pasan sin que nadie mire el barco. Un cabo gastado en noviembre puede acabar en un barco contra el pantalán en enero.</p>
        <p>La lona, bien tensa para que no haga bolsas de agua y con ventilación. Una lona hermética encierra la humedad y en primavera te encuentras moho. Guarda cojines y bimini en seco si puedes.</p>

        <h2 id="veleros">Velas, jarcia y winches (veleros)</h2>
        <ul>
          <li>Quita el génova del enrollador. Una vela enrollada puede abrirse con un temporal y romperse, y de paso golpea tu barco y el de al lado.</li>
          <li>Lava las velas con agua dulce, sécalas del todo y guárdalas plegadas en un sitio seco. Una vela guardada húmeda acaba con moho.</li>
          <li>La mayor, desenvergada o bien tapada con su funda.</li>
          <li>Las drizas se pueden cambiar por mensajeros finos para que no les dé el sol ni golpeen el palo.</li>
          <li>Jarcia firme: mira terminales, crucetas y tensores buscando grietas u óxido. Si tienes dudas, que la vea un aparejador.</li>
          <li>Winches: desmóntalos, límpialos y engrásalos como indique el fabricante. Los trinquetes suelen llevar aceite y no grasa; el manual del winche lo deja claro.</li>
        </ul>

        <h2 id="interior">Interior: humedad, gas, electrónica y equipo de seguridad</h2>
        <ul>
          <li>Ventilación: deshumidificador si hay corriente y el puerto lo permite, o al menos armarios abiertos, colchonetas de canto y un par de absorbentes de humedad. El olor a barco cerrado tira atrás a muchos compradores.</li>
          <li>Nevera limpia, vacía y con la puerta entreabierta.</li>
          <li>Ni comida ni basura a bordo.</li>
          <li>Gas: cierra la botella, desconéctala y mira la fecha de caducidad del tubo flexible.</li>
          <li>Electrónica: la portátil (VHF, GPS de mano) a casa. Las pantallas fijas, con su tapa.</li>
        </ul>
        <h3 id="papeles">Equipo de seguridad y papeles</h3>
        <p>Aprovecha para apuntar fechas: bengalas y demás pirotecnia, extintores, balsa salvavidas, chalecos inflables y botiquín. El Real Decreto 339/2021 remite la revisión de los extintores a la normativa de protección contra incendios, y la de balsas y chalecos inflables, a lo que indique el fabricante.</p>
        <p>Mira también la caducidad de la ITB y el recibo del seguro. Si estás pensando en vender en primavera, tener todo esto en regla en marzo te ahorra semanas: los compradores lo piden, y las gestorías van cargadas en temporada.</p>

        <h2 id="errores">Errores que salen caros</h2>
        <ul>
          <li><strong>Anticongelante de coche en el circuito de agua potable o en el WC.</strong> Es tóxico. Solo el apto para agua potable, y solo si hace falta.</li>
          <li><strong>Arrancar el fueraborda sin agua «solo un momento».</strong> El rodete se quema en segundos.</li>
          <li><strong>Lona hermética sin ventilación.</strong> Lo que te espera en primavera es moho.</li>
          <li><strong>Baterías conectadas a algo que consume poco.</strong> En tres meses, ese poco las vacía.</li>
          <li><strong>El génova enrollado durante los temporales.</strong></li>
          <li><strong>Olvidar los tapones de admisión y escape al arrancar en primavera.</strong> Por eso la nota en el contacto.</li>
          <li><strong>Desagües de la bañera tapados por la lona o llenos de hojas.</strong> El agua de lluvia tiene que poder salir.</li>
          <li><strong>Depósito de gasoil medio vacío.</strong> El aire de dentro condensa agua.</li>
        </ul>
"""
L["es"]["body2"] = """
        <h2 id="venta">Si el barco está en venta</h2>
        <p>Un barco en venta en invierno tiene que poder enseñarse en veinte minutos. Eso significa cubierta limpia, interior seco y ventilado, motor que arranca a la primera y documentación en una carpeta. No hace falta más, pero eso sí tiene que estar. Si lo tienes en seco, deja el acceso resuelto con la náutica antes de que aparezca el primer interesado, porque es de lo que más visitas hace perder.</p>
"""
L["es"]["aviso"] = "Lista orientativa. Cada motor tiene su manual y sus intervalos; en caso de duda, tu taller de confianza sabe qué toca en tu modelo."

# ---------------------------------------------------------------- CA
L["ca"] = dict(
    prefix="/ca",
    title="Hivernatge del vaixell: la llista per deixar-lo a punt",
    desc="Hivernatge del vaixell a la Mediterrània: motor dièsel, gasolina o forabord, aigua, bateries, casc i lones. Llista per marcar i imprimir.",
    h1="Hivernatge del vaixell: com el deixo a punt per a l'hivern",
    eyebrow="Guia del navegant · Manteniment",
    meta=["Per Juan Morante", "Comprovat el 3 de novembre de 2026", "12 min de lectura"],
    lead="A la tardor s'espatllen molts vaixells sense sortir de l'amarratge. El que es fa en aquestes setmanes decideix com arrenca a la primavera i, si el vaixell està en venda, quina impressió dona a la visita. Aquesta és la llista que segueixo amb el meu, pensada per a la Mediterrània: aquí glaça poc, però la humitat i els temporals no perdonen.",
    steps_h="La resposta curta: l'hivernatge en 5 passos",
    steps_intro="Si només tens cinc minuts, això és el que no em salto mai. El detall és més avall i, al final, la <a href=\"#lista\">llista per anar marcant</a>.",
    steps=[
        ("Motor", "Oli i filtres canviats, circuit d'aigua salada esbandit amb aigua dolça i el combustible preparat per estar aturat, sempre segons el manual del teu motor."),
        ("Aigua fora", "Dipòsits, escalfador, WC i sentina buits, nets i secs."),
        ("Bateries carregades", "Desconnecta-ho tot menys la bomba d'esgotament automàtica si el vaixell es queda a l'aigua."),
        ("Casc i amarratge", "Ànodes, aixetes de fons, amarres i defenses revisats. Lona ben subjecta i amb ventilació."),
        ("Interior sec", "Ventilació o deshumidificador, gas tancat i les dates de l'equip de seguretat apuntades."),
    ],
    howto_name="Hivernatge del vaixell en 5 passos",
    list_h="Llista de comprovació d'hivernatge",
    list_note="Marca el que vagis fent. Queda desat en aquest navegador, així que pots tornar un altre dia i continuar on ho vas deixar. El que no s'apliqui al teu vaixell, salta-t'ho.",
    count_tpl="{x} de {n} fetes",
    print_btn="Imprimir la llista",
    reset_btn="Desmarcar-ho tot",
    reset_confirm="Vols desmarcar totes les tasques?",
    groups={
        "motor": ("Motor", [
            "Oli i filtre canviats amb el motor calent (segons el manual)",
            "Filtres de combustible i vas decantador purgats o canviats",
            "Circuit d'aigua salada esbandit amb aigua dolça",
            "Rodet de la bomba d'aigua revisat (o tret, si el manual ho indica)",
            "Refrigerant del circuit tancat comprovat",
            "Oli de la cua, peu o saildrive canviat i sense rastre lletós",
            "Combustible: dipòsit gairebé ple i estabilitzador si el fabricant ho recomana",
            "Admissió i escapament tapats, amb una nota al contacte",
            "Forabord: esbandit, greixat i desat en vertical",
        ]),
        "agua": ("Aigua dolça, WC i sentina", [
            "Dipòsit d'aigua dolça, canonades i escalfador buidats",
            "Aigües negres buidades a l'estació de bombament i WC esbandit",
            "Sentina neta i seca; bomba d'esgotament i flotador provats",
        ]),
        "bat": ("Bateries", [
            "Bateries carregades (liti, al nivell que digui el fabricant) i borns nets",
            "Interruptor general desconnectat; esgotament automàtic alimentat si queda a l'aigua",
            "Mantenidor amb el perfil correcte, o visita cada poques setmanes",
        ]),
        "casco": ("Casc i amarratge", [
            "Ànodes revisats i canviats si estan gastats",
            "Aixetes de fons accionades; mànegues i brides revisades",
            "Desguassos de la banyera i embornals lliures",
            "Amarres doblades, amb protecció on freguen, i defenses posades",
            "Lona ben subjecta, sense bosses d'aigua i amb ventilació",
            "En sec: obra viva rentada i revisada (osmosi, antifouling, hèlix)",
        ]),
        "vela": ("Velers", [
            "Gènova fora de l'enrotllador; veles rentades, seques i desades",
            "Eixàrcia fixa revisada (terminals, creuetes, tensors)",
            "Winches nets i greixats segons el fabricant",
        ]),
        "interior": ("Interior i seguretat", [
            "Matalassos de cantell o a casa, armaris oberts",
            "Deshumidificador o absorbents d'humitat col·locats",
            "Nevera buida, neta i amb la porta entreoberta",
            "Bombona de gas tancada i desconnectada; data del tub mirada",
            "Electrònica portàtil a casa",
            "Dates apuntades: bengales, extintors, bassa, armilles, farmaciola",
            "Caducitat de l'ITB i de l'assegurança apuntades",
            "Ni menjar ni escombraries a bord",
        ]),
        "venta": ("Si el vendràs", [
            "Carpeta amb la documentació i les factures de manteniment",
        ]),
    },
    links=[
        ("/ca/herramientas/libro-mantenimiento-barco", "Llibre de manteniment del vaixell (PDF gratis)", "Per apuntar el que fas cada hivern. Et serveix a tu i, el dia que el venguis, al comprador."),
        ("/ca/recordatorios-barco/", "Avisos de venciments gratis (ITB, assegurança…)", "Apunta les dates un cop i rep un avís abans que caduquin."),
    ],
    sources_h="Fonts",
    sources=[
        (BOE_339, "BOE: Reial decret 339/2021, equip de seguretat i de prevenció de la contaminació de les embarcacions d'esbarjo (en castellà)"),
        (BOE_1434, "BOE: Reial decret 1434/1999, reconeixements i inspeccions de les embarcacions d'esbarjo, ITB (en castellà)"),
    ],
    sources_tail="I, per damunt de tot, el manual del propietari del teu motor i de cada equip: mana sobre qualsevol llista, també sobre aquesta.",
    toc_label="Contingut", toc_h="En aquesta pàgina",
    toc=[("corta", "La resposta curta"), ("agua-o-seco", "A l'aigua o en sec?"), ("motor", "Motor"), ("agua", "Aigua dolça, WC i sentina"),
         ("baterias", "Bateries"), ("casco", "Casc, amarres i lones"), ("veleros", "Velers"), ("interior", "Interior i seguretat"),
         ("errores", "Errors que surten cars"), ("lista", "Llista per marcar"), ("venta", "Si està en venda"), ("fuentes", "Fonts")],
)
L["ca"]["body1"] = """
        <h2 id="agua-o-seco">A l'aigua o en sec?</h2>
        <p>A la Mediterrània molts vaixells passen l'hivern a l'aigua i no passa res, sempre que algú s'hi passi a mirar-los. A la costa catalana, arran de mar, glaça poc. El que sí que hi ha és humitat, pluja i temporals de llevant que posen a prova les amarres.</p>
        <ul>
          <li><strong>A l'aigua.</strong> Més còmode i normalment més barat. El mar fa de coixí tèrmic i el motor continua a mà per engegar-lo de tant en tant. A canvi, necessites la bomba d'esgotament alimentada, amarres en bon estat i una visita després de cada temporal.</li>
          <li><strong>En sec.</strong> Sense risc d'enfonsament ni de fregades contra el pantalà, i aprofites per mirar i pintar l'obra viva. A canvi, cal buidar bé tots els circuits d'aigua, deixar el vaixell ben falcat i pagar la varada i l'estada.</li>
        </ul>
        <div class="ejemplo">
          <p class="eyebrow">Si al teu port hi pot glaçar</p>
          <p>Un pantà, un port d'interior o un vaixell desat en sec terra endins sí que poden veure nits sota zero. Allà, qualsevol circuit amb aigua que no es pugui buidar del tot necessita anticongelant, i del tipus que digui el manual. En un amarratge arran de mar sol n'hi ha prou amb buidar i esbandir, però mira les previsions i no ho donis per fet.</p>
        </div>

        <h2 id="motor">Motor</h2>
        <p>És el primer i el que més costa si es descuida. Cada motor té el seu manual d'hivernatge i mana sobre tot el que llegeixis aquí. El que segueix és l'ordre que segueixo jo.</p>

        <h3 id="diesel">Intrabord dièsel</h3>
        <ul>
          <li>Canvi d'oli i filtre amb el motor calent. L'oli usat porta àcids que no convé deixar dins tot l'hivern.</li>
          <li>Filtres de combustible i vas decantador: purga l'aigua i canvia els filtres si toca.</li>
          <li>Dipòsit gairebé ple, perquè no condensi aigua a dins. Si has tingut problemes de bacteris al gasoil, pregunta per un biocida i fes-lo servir com indiqui el fabricant.</li>
          <li>Circuit d'aigua salada: esbandeix-lo amb aigua dolça. Si el vaixell pot glaçar, el manual et dirà si cal passar anticongelant i quin.</li>
          <li>Circuit tancat: comprova el nivell i l'estat del refrigerant. Si toca canviar-lo per hores o per anys, millor ara que al maig.</li>
          <li>Rodet de la bomba d'aigua: revisa'l. Alguns fabricants recomanen treure'l durant l'hivern perquè no es deformi; si ho fas, deixa una nota ben visible.</li>
          <li>Corretges, mànegues i brides: una ullada buscant esquerdes o rovell.</li>
          <li>Si porta saildrive o cua, canvia l'oli i mira que no surti lletós.</li>
          <li>Tapa la presa d'aire i la sortida d'escapament perquè no hi entri humitat, i deixa una nota al contacte per recordar-te de treure-ho.</li>
        </ul>
        <p>Un motor amb el manteniment fet i anotat en un quadern o a les factures és un dels arguments de venda més barats que hi ha. Quan valoro un vaixell, un historial clar de manteniment pesa més que la majoria d'extres.</p>

        <h3 id="gasolina">Intrabord i dins-forabord de gasolina</h3>
        <ul>
          <li>Oli i filtre amb el motor calent, igual que en un dièsel.</li>
          <li>La gasolina envelleix de pressa si queda aturada. Afegeix-hi estabilitzador i fes funcionar el motor uns minuts perquè arribi a tot el sistema, com indiqui el fabricant.</li>
          <li>Alguns manuals demanen oli de nebulitzar (<em>fogging</em>) als cilindres, sobretot en motors de carburació. En els d'injecció no sempre es fa així: segueix el teu.</li>
          <li>Oli de la cua: si surt lletós, hi ha aigua a dins i toca revisar retens abans de desar-lo.</li>
          <li>Manxes de la cua: mira que no tinguin esquerdes. Una manxa trencada pot fer entrar aigua al vaixell.</li>
          <li>Si el vaixell pot glaçar, el bloc i els col·lectors es buiden pels seus taps o es protegeixen amb anticongelant, segons el manual. Un bloc esquerdat pel gel és de les avaries més cares que hi ha.</li>
          <li>A la primavera, ventila la sala de màquines abans d'engegar. Amb gasolina, sempre.</li>
        </ul>

        <h3 id="fueraborda">Forabord</h3>
        <ul>
          <li>Esbandeix-lo amb aigua dolça amb orelleres o amb la presa de rentada que porten molts models. No l'engeguis mai sense aigua: el rodet es crema en segons.</li>
          <li>Combustible: estabilitzador i uns minuts en marxa perquè arribi a la injecció o al carburador. Alguns fabricants demanen buidar la cubeta del carburador; mira el teu.</li>
          <li>Oli del motor (en els de quatre temps) i oli de la cua. Si surt lletós, al taller.</li>
          <li>Greixatge dels punts que marca el manual, ànodes i una ullada a l'hèlix.</li>
          <li>Si el desmuntes, desa'l en vertical perquè escorri tota l'aigua. Si ha d'anar estirat, fes-ho del costat que indiqui el fabricant; de l'altre, l'oli pot anar on no toca.</li>
          <li>Dipòsit portàtil: tancat, en un lloc ventilat i lluny de qualsevol flama.</li>
        </ul>

        <h2 id="agua">Aigua dolça, WC i sentina</h2>
        <ul>
          <li>Buida el dipòsit d'aigua dolça i obre les aixetes fins que la bomba es quedi sense aigua. Apaga la bomba i deixa les aixetes obertes.</li>
          <li>L'escalfador també es buida. És el primer que es trenca si glaça.</li>
          <li>Si al teu port hi pot glaçar i no ho pots buidar tot, fes servir només anticongelant apte per a aigua potable. El del cotxe és tòxic: ni al circuit d'aigua ni al WC.</li>
          <li>WC: buida les aigües negres a l'estació de bombament del port, esbandeix amb aigua dolça i fes servir el producte que recomani el fabricant del WC.</li>
          <li>Sentina neta i seca. Prova la bomba d'esgotament aixecant el flotador amb la mà. Si hi ha restes d'oli, recull-les amb absorbents: l'aigua amb oli no es bomba al mar.</li>
        </ul>

        <h2 id="baterias">Bateries</h2>
        <p>Una bateria que passa l'hivern descarregada moltes vegades no arriba a la primavera. I una de plom descarregada, a més, es pot glaçar; carregada, és molt més difícil.</p>
        <ul>
          <li><strong>Plom obertes.</strong> Carrega-les del tot, neteja els borns i revisa el nivell de l'electròlit si es pot.</li>
          <li><strong>AGM i gel.</strong> També carregades del tot, amb un carregador que tingui el seu perfil. Un perfil equivocat les espatlla a poc a poc.</li>
          <li><strong>Liti (LiFePO4).</strong> Desa-les al nivell de càrrega que indiqui el fabricant, que moltes vegades no és el 100 %. No les carreguis per sota de 0 °C si no porten calefacció integrada. El sistema de gestió (BMS) sol tallar la càrrega amb fred, però no convé refiar-se'n del tot.</li>
          <li>Desconnecta l'interruptor general perquè res no les vagi buidant. Si el vaixell queda a l'aigua, deixa la bomba d'esgotament automàtica alimentada.</li>
          <li>Si hi ha corrent al pantalà, un mantenidor amb el perfil correcte les té a punt tot l'hivern. Si no, passa-hi cada poques setmanes o emporta-te-les a casa.</li>
        </ul>

        <h2 id="casco">Casc, ànodes, aixetes de fons, amarres i lones</h2>
        <h3>Casc i obra viva</h3>
        <p>Si el vaixell surt de l'aigua, és el moment de mirar l'obra viva amb calma: butllofes d'osmosi, estat de l'antifouling, eixos, cua i hèlix (osques, joc). Una rentada a pressió tot just sortir estalvia hores de raspar. Si es queda a l'aigua, almenys neteja la línia de flotació.</p>
        <h3>Ànodes</h3>
        <p>Revisa'ls tots: casc, eixos, cua o saildrive i, si en té, hèlix de proa. Si estan molt gastats, canvia'ls abans de deixar el vaixell. Un ànode esgotat ja no protegeix res, i l'hivern és llarg.</p>
        <h3>Aixetes de fons</h3>
        <p>A l'aigua, obre-les i tanca-les un parell de vegades perquè no s'encallin, i revisa mànegues i brides. Tanca les que no facin falta, però mai els desguassos de la banyera: han de poder treure l'aigua de pluja. En sec, deixa-les obertes perquè escorrin i greixa-les si el model ho demana.</p>
        <h3 id="cubierta">Amarres, defenses i lones</h3>
        <p>Renta amb aigua dolça tota la coberta, ferramenta i vidres; la sal deixa marques que després costen de treure. Dobla les amarres que més treballen, posa protecció on freguen i revisa les defenses: és quan fa més vent i passen més dies sense que ningú miri el vaixell. Un cap gastat al novembre pot acabar amb un vaixell contra el pantalà al gener.</p>
        <p>La lona, ben tensa perquè no faci bosses d'aigua i amb ventilació. Una lona hermètica tanca la humitat a dins i a la primavera et trobes floridura. Desa coixins i bimini en sec si pots.</p>

        <h2 id="veleros">Veles, eixàrcia i winches (velers)</h2>
        <ul>
          <li>Treu el gènova de l'enrotllador. Una vela enrotllada es pot obrir amb un temporal i trencar-se, i de passada colpeja el teu vaixell i el del costat.</li>
          <li>Renta les veles amb aigua dolça, asseca-les del tot i desa-les plegades en un lloc sec. Una vela desada humida acaba amb floridura.</li>
          <li>La major, desenvergada o ben tapada amb la seva funda.</li>
          <li>Les drisses es poden canviar per missatgers fins perquè no els toqui el sol ni piquin contra el pal.</li>
          <li>Eixàrcia fixa: mira terminals, creuetes i tensors buscant esquerdes o rovell. Si tens dubtes, que la vegi un aparellador.</li>
          <li>Winches: desmunta'ls, neteja'ls i greixa'ls com indiqui el fabricant. Els trinquets solen portar oli i no greix; el manual del winch ho deixa clar.</li>
        </ul>

        <h2 id="interior">Interior: humitat, gas, electrònica i equip de seguretat</h2>
        <ul>
          <li>Ventilació: deshumidificador si hi ha corrent i el port ho permet, o almenys armaris oberts, matalassos de cantell i un parell d'absorbents d'humitat. L'olor de vaixell tancat tira enrere molts compradors.</li>
          <li>Nevera neta, buida i amb la porta entreoberta.</li>
          <li>Ni menjar ni escombraries a bord.</li>
          <li>Gas: tanca la bombona, desconnecta-la i mira la data de caducitat del tub flexible.</li>
          <li>Electrònica: la portàtil (VHF, GPS de mà) a casa. Les pantalles fixes, amb la seva tapa.</li>
        </ul>
        <h3 id="papeles">Equip de seguretat i papers</h3>
        <p>Aprofita per apuntar dates: bengales i altra pirotècnia, extintors, bassa salvavides, armilles inflables i farmaciola. El Reial decret 339/2021 remet la revisió dels extintors a la normativa de protecció contra incendis, i la de basses i armilles inflables, al que indiqui el fabricant.</p>
        <p>Mira també la caducitat de l'ITB i el rebut de l'assegurança. Si penses vendre a la primavera, tenir tot això en regla al març t'estalvia setmanes: els compradors ho demanen, i les gestories van carregades en temporada.</p>

        <h2 id="errores">Errors que surten cars</h2>
        <ul>
          <li><strong>Anticongelant de cotxe al circuit d'aigua potable o al WC.</strong> És tòxic. Només l'apte per a aigua potable, i només si cal.</li>
          <li><strong>Engegar el forabord sense aigua «només un moment».</strong> El rodet es crema en segons.</li>
          <li><strong>Lona hermètica sense ventilació.</strong> El que t'espera a la primavera és floridura.</li>
          <li><strong>Bateries connectades a alguna cosa que consumeix poc.</strong> En tres mesos, aquest poc les buida.</li>
          <li><strong>El gènova enrotllat durant els temporals.</strong></li>
          <li><strong>Oblidar els taps d'admissió i escapament en engegar a la primavera.</strong> Per això la nota al contacte.</li>
          <li><strong>Desguassos de la banyera tapats per la lona o plens de fulles.</strong> L'aigua de pluja ha de poder sortir.</li>
          <li><strong>Dipòsit de gasoil mig buit.</strong> L'aire de dins condensa aigua.</li>
        </ul>
"""
L["ca"]["body2"] = """
        <h2 id="venta">Si el vaixell està en venda</h2>
        <p>Un vaixell en venda a l'hivern ha de poder ensenyar-se en vint minuts. Això significa coberta neta, interior sec i ventilat, motor que arrenca a la primera i documentació en una carpeta. No cal més, però això sí que ha d'estar-hi. Si el tens en sec, deixa l'accés resolt amb la nàutica abans que aparegui el primer interessat, perquè és del que més visites fa perdre.</p>
"""
L["ca"]["aviso"] = "Llista orientativa. Cada motor té el seu manual i els seus intervals; en cas de dubte, el teu taller de confiança sap què toca al teu model."

# ---------------------------------------------------------------- EN
L["en"] = dict(
    prefix="/en",
    title="Laying up a boat for winter: my winterising checklist",
    desc="Winterising a boat in the Mediterranean: diesel, petrol and outboard engines, water, batteries, hull and covers. A checklist to tick off and print.",
    h1="Laying up a boat for winter: how I get mine ready",
    eyebrow="Skipper's guide · Maintenance",
    meta=["By Juan Morante", "Checked on 3 November 2026", "12 min read"],
    lead="Come autumn, plenty of boats get ruined without ever leaving the mooring. What's done in these few weeks decides how it starts up in spring and, if the boat is for sale, what impression it gives at a viewing. This is the list I follow with my own, written for the Mediterranean: frost is rare here, but damp and winter storms are not.",
    steps_h="The short answer: laying up in 5 steps",
    steps_intro="If you only have five minutes, this is what I never skip. The detail is further down and, at the end, there's a <a href=\"#lista\">checklist to tick off</a>.",
    steps=[
        ("Engine", "Oil and filters changed, raw-water circuit flushed with fresh water and the fuel ready to sit, always following your engine manual."),
        ("Water out", "Tanks, water heater, heads and bilge empty, clean and dry."),
        ("Batteries charged", "Switch everything off except the automatic bilge pump if the boat stays afloat."),
        ("Hull and mooring", "Anodes, seacocks, mooring lines and fenders checked. Cover well secured and ventilated."),
        ("Dry interior", "Ventilation or a dehumidifier, gas turned off and the dates of the safety gear written down."),
    ],
    howto_name="Laying up a boat in 5 steps",
    list_h="Winterising checklist",
    list_note="Tick things off as you go. Your progress is saved in this browser, so you can come back another day and carry on. Skip anything that doesn't apply to your boat.",
    count_tpl="{x} of {n} done",
    print_btn="Print list",
    reset_btn="Clear all",
    reset_confirm="Untick every task?",
    groups={
        "motor": ("Engine", [
            "Oil and filter changed with the engine warm (as per the manual)",
            "Fuel filters and water separator bowl drained or changed",
            "Raw-water circuit flushed with fresh water",
            "Water pump impeller checked (or removed, if the manual says so)",
            "Coolant in the closed circuit checked",
            "Sterndrive, lower unit or saildrive oil changed, with no milky traces",
            "Fuel: tank nearly full and stabiliser if the manufacturer recommends it",
            "Air intake and exhaust plugged, with a note on the ignition",
            "Outboard: flushed, greased and stored upright",
        ]),
        "agua": ("Fresh water, heads and bilge", [
            "Fresh-water tank, pipes and water heater drained",
            "Holding tank pumped out at the pump-out station and heads rinsed",
            "Bilge clean and dry; bilge pump and float switch tested",
        ]),
        "bat": ("Batteries", [
            "Batteries charged (lithium, to the level the maker states) and terminals clean",
            "Main switch off; automatic bilge pump powered if afloat",
            "Maintainer with the right profile, or a visit every few weeks",
        ]),
        "casco": ("Hull and mooring", [
            "Anodes checked and replaced if worn",
            "Seacocks worked; hoses and clamps checked",
            "Cockpit drains and scuppers clear",
            "Mooring lines doubled up, chafe protection fitted, fenders out",
            "Cover well secured, no pockets of water and ventilated",
            "Ashore: underwater hull washed and checked (osmosis, antifouling, propeller)",
        ]),
        "vela": ("Sailing boats", [
            "Genoa off the furler; sails washed, dried and stowed",
            "Standing rigging checked (terminals, spreaders, turnbuckles)",
            "Winches cleaned and greased as the maker specifies",
        ]),
        "interior": ("Interior and safety", [
            "Cushions on edge or taken home, lockers open",
            "Dehumidifier or moisture absorbers in place",
            "Fridge empty, clean and door left ajar",
            "Gas bottle closed and disconnected; hose date checked",
            "Portable electronics taken home",
            "Dates noted: flares, extinguishers, liferaft, lifejackets, first-aid kit",
            "Survey (ITB) and insurance expiry dates noted",
            "No food or rubbish left aboard",
        ]),
        "venta": ("If you're selling", [
            "Folder with the paperwork and maintenance invoices",
        ]),
    },
    links=[
        ("/en/herramientas/libro-mantenimiento-barco", "Boat maintenance log (free PDF)", "To note down what you do each winter. Useful for you and, the day you sell, for the buyer."),
        ("/en/recordatorios-barco/", "Free expiry reminders (ITB, insurance…)", "Enter the dates once and get a reminder before they run out."),
    ],
    sources_h="Sources",
    sources=[
        (BOE_339, "BOE (Spanish Official Gazette): Royal Decree 339/2021 on safety and pollution-prevention equipment for recreational craft (in Spanish)"),
        (BOE_1434, "BOE: Royal Decree 1434/1999 on surveys and inspections of recreational craft, the ITB (in Spanish)"),
    ],
    sources_tail="And above all, the owner's manual for your engine and each piece of equipment: it overrides any list, this one included.",
    toc_label="Contents", toc_h="On this page",
    toc=[("corta", "The short answer"), ("agua-o-seco", "Afloat or ashore?"), ("motor", "Engine"), ("agua", "Fresh water, heads and bilge"),
         ("baterias", "Batteries"), ("casco", "Hull, lines and covers"), ("veleros", "Sailing boats"), ("interior", "Interior and safety"),
         ("errores", "Costly mistakes"), ("lista", "Checklist"), ("venta", "If it's for sale"), ("fuentes", "Sources")],
)
L["en"]["body1"] = """
        <h2 id="agua-o-seco">Afloat or ashore?</h2>
        <p>In the Mediterranean plenty of boats spend the winter afloat without any trouble, as long as someone drops by to check on them. On the Catalan coast, right by the sea, frost is rare. What you do get is damp, rain and easterly storms that put mooring lines to the test.</p>
        <ul>
          <li><strong>Afloat.</strong> Easier and usually cheaper. The sea acts as a thermal buffer and the engine is still there to run now and then. In return, you need the bilge pump powered, mooring lines in good condition and a visit after every storm.</li>
          <li><strong>Ashore.</strong> No risk of sinking or chafing against the pontoon, and it's a chance to check and paint the underwater hull. In return, every water circuit has to be drained properly, the boat well chocked, and you pay for the lift and the stay.</li>
        </ul>
        <div class="ejemplo">
          <p class="eyebrow">If your marina can freeze</p>
          <p>A reservoir, an inland harbour or a boat stored ashore away from the coast can see nights below zero. There, any circuit holding water that can't be fully drained needs antifreeze, of the type your manual specifies. On a seafront berth draining and flushing is usually enough, but check the forecast and don't take it for granted.</p>
        </div>

        <h2 id="motor">Engine</h2>
        <p>It comes first, and it's the most expensive thing to neglect. Every engine has its own lay-up instructions and they override anything you read here. What follows is the order I work in.</p>

        <h3 id="diesel">Inboard diesel</h3>
        <ul>
          <li>Change the oil and filter with the engine warm. Used oil carries acids you don't want sitting inside all winter.</li>
          <li>Fuel filters and water separator bowl: drain off the water and change the filters if they're due.</li>
          <li>Tank nearly full, so that water doesn't condense inside. If you've had diesel bug before, ask about a biocide and use it as the maker says.</li>
          <li>Raw-water circuit: flush it with fresh water. If the boat may freeze, the manual will tell you whether to run antifreeze through and which one.</li>
          <li>Closed circuit: check the coolant level and condition. If it's due by hours or by years, better now than in May.</li>
          <li>Water pump impeller: check it. Some manufacturers recommend taking it out over winter so it doesn't take a set; if you do, leave a clearly visible note.</li>
          <li>Belts, hoses and clamps: a quick look for cracks or rust.</li>
          <li>If it has a saildrive or sterndrive, change the oil and check it doesn't come out milky.</li>
          <li>Plug the air intake and the exhaust outlet to keep damp out, and leave a note on the ignition so you remember to remove them.</li>
        </ul>
        <p>An engine with its maintenance done and written down in a log or backed by invoices is one of the cheapest selling points there is. When I value a boat, a clear maintenance history counts for more than most extras.</p>

        <h3 id="gasolina">Petrol inboard and sterndrive</h3>
        <ul>
          <li>Oil and filter with the engine warm, just like a diesel.</li>
          <li>Petrol goes stale quickly when it sits. Add stabiliser and run the engine for a few minutes so it reaches the whole system, as the maker says.</li>
          <li>Some manuals call for fogging oil in the cylinders, mainly on carburettor engines. Fuel-injected engines aren't always done that way: follow yours.</li>
          <li>Sterndrive oil: if it comes out milky, there's water inside and the seals need checking before lay-up.</li>
          <li>Sterndrive bellows: check them for cracks. A split bellows can let water into the boat.</li>
          <li>If the boat may freeze, the block and manifolds are drained through their plugs or protected with antifreeze, as per the manual. A block cracked by frost is one of the most expensive failures there is.</li>
          <li>In spring, ventilate the engine bay before starting. With petrol, always.</li>
        </ul>

        <h3 id="fueraborda">Outboard</h3>
        <ul>
          <li>Flush it with fresh water using muffs or the flushing port many models have. Never run it without water: the impeller burns out in seconds.</li>
          <li>Fuel: stabiliser and a few minutes running so it reaches the injection or the carburettor. Some makers ask you to drain the carburettor float bowl; check yours.</li>
          <li>Engine oil (on four-strokes) and gear oil. If the gear oil is milky, take it to the workshop.</li>
          <li>Grease the points the manual shows, check the anodes and take a look at the propeller.</li>
          <li>If you take it off, store it upright so all the water drains out. If it has to lie down, put it on the side the manufacturer specifies; on the other side oil can end up where it shouldn't.</li>
          <li>Portable tank: closed, somewhere ventilated and well away from any flame.</li>
        </ul>

        <h2 id="agua">Fresh water, heads and bilge</h2>
        <ul>
          <li>Empty the fresh-water tank and open the taps until the pump runs dry. Switch the pump off and leave the taps open.</li>
          <li>Drain the water heater too. It's the first thing to split if it freezes.</li>
          <li>If your marina can freeze and you can't drain everything, use only antifreeze that is safe for drinking-water systems. Car antifreeze is toxic: not in the water circuit and not in the heads.</li>
          <li>Heads: pump out the holding tank at the marina's pump-out station, rinse with fresh water and use the product the toilet maker recommends.</li>
          <li>Bilge clean and dry. Test the bilge pump by lifting the float by hand. If there's any oil, soak it up with absorbent pads: oily water is never pumped into the sea.</li>
        </ul>

        <h2 id="baterias">Batteries</h2>
        <p>A battery that spends the winter flat often doesn't make it to spring. And a flat lead-acid battery can also freeze; a charged one is much harder to freeze.</p>
        <ul>
          <li><strong>Flooded lead-acid.</strong> Charge them fully, clean the terminals and check the electrolyte level if you can.</li>
          <li><strong>AGM and gel.</strong> Also fully charged, with a charger that has the right profile. The wrong profile damages them little by little.</li>
          <li><strong>Lithium (LiFePO4).</strong> Store them at the state of charge the maker recommends, which is often not 100 %. Don't charge them below 0 °C unless they have built-in heating. The battery management system (BMS) usually cuts charging in the cold, but it's best not to rely on that alone.</li>
          <li>Turn the main switch off so nothing drains them. If the boat stays afloat, keep the automatic bilge pump powered.</li>
          <li>If there's shore power, a maintainer with the right profile keeps them topped up all winter. If not, check them every few weeks or take them home.</li>
        </ul>

        <h2 id="casco">Hull, anodes, seacocks, mooring lines and covers</h2>
        <h3>Hull and underwater surfaces</h3>
        <p>If the boat comes out of the water, this is the moment to look over the underwater hull calmly: osmosis blisters, the state of the antifouling, shafts, drive and propeller (dings, play). A pressure wash straight after lifting saves hours of scraping. If it stays afloat, at least clean the waterline.</p>
        <h3>Anodes</h3>
        <p>Check them all: hull, shafts, drive or saildrive and, if fitted, the bow thruster. If they're badly worn, replace them before you leave the boat. A spent anode protects nothing, and winter is long.</p>
        <h3>Seacocks</h3>
        <p>Afloat, open and close them a couple of times so they don't seize, and check hoses and clamps. Close the ones you don't need, but never the cockpit drains: they have to be able to clear rainwater. Ashore, leave them open so they drain, and grease them if the model calls for it.</p>
        <h3 id="cubierta">Mooring lines, fenders and covers</h3>
        <p>Wash the whole deck, fittings and windows with fresh water; salt leaves marks that are hard to remove later. Double up the lines that work hardest, fit chafe protection where they rub and check the fenders: this is when there's most wind and the most days go by without anyone looking at the boat. A worn line in November can end with a boat against the pontoon in January.</p>
        <p>The cover should be taut so it doesn't collect pools of water, and ventilated. An airtight cover traps the damp, and in spring you find mould. Store cushions and the bimini somewhere dry if you can.</p>

        <h2 id="veleros">Sails, rigging and winches (sailing boats)</h2>
        <ul>
          <li>Take the genoa off the furler. A furled sail can unroll in a storm and tear, battering your boat and the one next to it.</li>
          <li>Wash the sails with fresh water, dry them completely and store them folded somewhere dry. A sail stowed damp ends up mouldy.</li>
          <li>The mainsail, either taken off or well protected by its cover.</li>
          <li>Halyards can be swapped for thin messenger lines so they're out of the sun and don't slap the mast.</li>
          <li>Standing rigging: check terminals, spreaders and turnbuckles for cracks or rust. If in doubt, have a rigger look at it.</li>
          <li>Winches: strip, clean and grease them as the maker specifies. Pawls usually take oil rather than grease; the winch manual makes it clear.</li>
        </ul>

        <h2 id="interior">Interior: damp, gas, electronics and safety gear</h2>
        <ul>
          <li>Ventilation: a dehumidifier if there's power and the marina allows it, or at least lockers open, cushions on edge and a couple of moisture absorbers. The smell of a shut-up boat puts a lot of buyers off.</li>
          <li>Fridge clean, empty and with the door ajar.</li>
          <li>No food or rubbish aboard.</li>
          <li>Gas: close the bottle, disconnect it and check the expiry date on the flexible hose.</li>
          <li>Electronics: portable kit (handheld VHF, GPS) goes home. Fixed screens get their covers on.</li>
        </ul>
        <h3 id="papeles">Safety gear and paperwork</h3>
        <p>It's a good time to note down dates: flares and other pyrotechnics, extinguishers, liferaft, inflatable lifejackets and the first-aid kit. In Spain, Royal Decree 339/2021 refers extinguisher servicing to the fire-protection regulations, and liferaft and inflatable lifejacket servicing to the manufacturer's instructions.</p>
        <p>Check the expiry date of the survey (ITB) and the insurance renewal too. If you're thinking of selling in spring, having all this in order by March saves you weeks: buyers ask for it, and the agencies that handle paperwork are swamped in season.</p>

        <h2 id="errores">Costly mistakes</h2>
        <ul>
          <li><strong>Car antifreeze in the drinking-water system or the heads.</strong> It's toxic. Only drinking-water-safe antifreeze, and only if needed.</li>
          <li><strong>Running the outboard dry "just for a second".</strong> The impeller burns out in seconds.</li>
          <li><strong>An airtight cover with no ventilation.</strong> What's waiting for you in spring is mould.</li>
          <li><strong>Batteries left connected to something that draws a little.</strong> Over three months, that little drains them.</li>
          <li><strong>Leaving the genoa furled through the winter storms.</strong></li>
          <li><strong>Forgetting the intake and exhaust plugs when starting in spring.</strong> That's what the note on the ignition is for.</li>
          <li><strong>Cockpit drains blocked by the cover or full of leaves.</strong> Rainwater has to be able to get out.</li>
          <li><strong>A half-empty diesel tank.</strong> The air inside condenses into water.</li>
        </ul>
"""
L["en"]["body2"] = """
        <h2 id="venta">If the boat is for sale</h2>
        <p>A boat for sale in winter needs to be ready to show in twenty minutes. That means a clean deck, a dry and aired interior, an engine that starts first time, and documents in a folder. Nothing more is needed, but that much has to be there. If it's stored ashore, sort out access with the boatyard before the first interested buyer shows up, because that's what loses the most viewings.</p>
"""
L["en"]["aviso"] = "Guideline list. Every engine has its own manual and intervals; if in doubt, your trusted workshop knows what your model needs."

# ---------------------------------------------------------------- FR
L["fr"] = dict(
    prefix="/fr",
    title="Hivernage du bateau : la liste pour le préparer à l’hiver",
    desc="Hivernage du bateau en Méditerranée : moteur diesel, essence ou hors-bord, eau, batteries, coque et bâches. Une liste à cocher et à imprimer.",
    h1="Hivernage du bateau : comment je prépare le mien pour l’hiver",
    eyebrow="Guide du plaisancier · Entretien",
    meta=["Par Juan Morante", "Vérifié le 3 novembre 2026", "12 min de lecture"],
    lead="À l’automne, bien des bateaux s’abîment sans jamais quitter leur place de port. Ce que l’on fait pendant ces quelques semaines décide de la façon dont il redémarrera au printemps et, s’il est à vendre, de l’impression qu’il donnera lors d’une visite. Voici la liste que je suis avec le mien, pensée pour la Méditerranée : il gèle peu ici, mais l’humidité et les coups de vent ne pardonnent pas.",
    steps_h="La réponse courte : l’hivernage en 5 étapes",
    steps_intro="Si vous n’avez que cinq minutes, voici ce que je ne saute jamais. Le détail est plus bas et, à la fin, une <a href=\"#lista\">liste à cocher</a>.",
    steps=[
        ("Moteur", "Huile et filtres changés, circuit d’eau de mer rincé à l’eau douce et carburant préparé pour l’arrêt, toujours selon le manuel de votre moteur."),
        ("Eau dehors", "Réservoirs, chauffe-eau, WC et cale vides, propres et secs."),
        ("Batteries chargées", "Tout coupé sauf la pompe de cale automatique si le bateau reste à l’eau."),
        ("Coque et amarrage", "Anodes, vannes de coque, amarres et pare-battages vérifiés. Bâche bien tenue et ventilée."),
        ("Intérieur sec", "Ventilation ou déshumidificateur, gaz fermé et dates de l’armement de sécurité notées."),
    ],
    howto_name="Hivernage du bateau en 5 étapes",
    list_h="Liste de contrôle d’hivernage",
    list_note="Cochez au fur et à mesure. La progression reste enregistrée dans ce navigateur : vous pouvez revenir un autre jour et reprendre là où vous en étiez. Sautez ce qui ne concerne pas votre bateau.",
    count_tpl="{x} sur {n} faites",
    print_btn="Imprimer la liste",
    reset_btn="Tout décocher",
    reset_confirm="Décocher toutes les tâches ?",
    groups={
        "motor": ("Moteur", [
            "Huile et filtre changés moteur chaud (selon le manuel)",
            "Filtres à carburant et bol décanteur purgés ou changés",
            "Circuit d’eau de mer rincé à l’eau douce",
            "Rouet de pompe à eau contrôlé (ou retiré, si le manuel le prévoit)",
            "Liquide de refroidissement du circuit fermé contrôlé",
            "Huile d’embase, de pied ou de saildrive changée, sans trace laiteuse",
            "Carburant : réservoir presque plein et stabilisant si le fabricant le recommande",
            "Admission et échappement obturés, avec une note sur le contact",
            "Hors-bord : rincé, graissé et rangé à la verticale",
        ]),
        "agua": ("Eau douce, WC et cale", [
            "Réservoir d’eau douce, tuyaux et chauffe-eau vidangés",
            "Eaux noires vidées à la station de pompage et WC rincés",
            "Cale propre et sèche ; pompe de cale et flotteur testés",
        ]),
        "bat": ("Batteries", [
            "Batteries chargées (lithium : au niveau indiqué par le fabricant) et bornes propres",
            "Coupe-batterie ouvert ; pompe de cale automatique alimentée si le bateau reste à l’eau",
            "Chargeur d’entretien au bon profil, ou passage toutes les quelques semaines",
        ]),
        "casco": ("Coque et amarrage", [
            "Anodes contrôlées et remplacées si elles sont usées",
            "Vannes de coque manœuvrées ; tuyaux et colliers contrôlés",
            "Évacuations du cockpit et dalots dégagés",
            "Amarres doublées, protégées là où elles frottent, pare-battages en place",
            "Bâche bien tenue, sans poche d’eau et ventilée",
            "À terre : carène lavée et inspectée (osmose, antifouling, hélice)",
        ]),
        "vela": ("Voiliers", [
            "Génois sorti de l’enrouleur ; voiles rincées, sèches et rangées",
            "Gréement dormant contrôlé (embouts, barres de flèche, ridoirs)",
            "Winchs nettoyés et graissés selon le fabricant",
        ]),
        "interior": ("Intérieur et sécurité", [
            "Coussins sur la tranche ou à la maison, coffres ouverts",
            "Déshumidificateur ou absorbeurs d’humidité en place",
            "Frigo vide, propre et porte entrouverte",
            "Bouteille de gaz fermée et débranchée ; date du flexible vérifiée",
            "Électronique portable rapportée à la maison",
            "Dates notées : fusées, extincteurs, radeau, gilets, trousse de secours",
            "Échéances de l’ITB et de l’assurance notées",
            "Ni nourriture ni déchets à bord",
        ]),
        "venta": ("Si vous le vendez", [
            "Pochette avec les papiers et les factures d’entretien",
        ]),
    },
    links=[
        ("/fr/herramientas/libro-mantenimiento-barco", "Carnet d’entretien du bateau (PDF gratuit)", "Pour noter ce que vous faites chaque hiver. Utile pour vous et, le jour où vous vendez, pour l’acheteur."),
        ("/fr/recordatorios-barco/", "Rappels d’échéances gratuits (ITB, assurance…)", "Saisissez les dates une fois et recevez un rappel avant qu’elles n’expirent."),
    ],
    sources_h="Sources",
    sources=[
        (BOE_339, "BOE (Journal officiel espagnol) : décret royal 339/2021 sur l’équipement de sécurité et de prévention de la pollution des bateaux de plaisance (en espagnol)"),
        (BOE_1434, "BOE : décret royal 1434/1999 sur les visites et inspections des bateaux de plaisance, l’ITB (en espagnol)"),
    ],
    sources_tail="Et surtout le manuel du propriétaire de votre moteur et de chaque équipement : il prime sur toute liste, y compris celle-ci.",
    toc_label="Sommaire", toc_h="Sur cette page",
    toc=[("corta", "La réponse courte"), ("agua-o-seco", "À l’eau ou à terre ?"), ("motor", "Moteur"), ("agua", "Eau douce, WC et cale"),
         ("baterias", "Batteries"), ("casco", "Coque, amarres et bâches"), ("veleros", "Voiliers"), ("interior", "Intérieur et sécurité"),
         ("errores", "Les erreurs qui coûtent cher"), ("lista", "Liste à cocher"), ("venta", "S’il est à vendre"), ("fuentes", "Sources")],
)
L["fr"]["body1"] = """
        <h2 id="agua-o-seco">À l’eau ou à terre ?</h2>
        <p>En Méditerranée, beaucoup de bateaux passent l’hiver à l’eau sans problème, à condition que quelqu’un passe les voir. Sur la côte catalane, au bord de la mer, il gèle peu. En revanche, il y a l’humidité, la pluie et les coups de vent d’est qui mettent les amarres à l’épreuve.</p>
        <ul>
          <li><strong>À l’eau.</strong> Plus simple et en général moins cher. La mer sert de tampon thermique et le moteur reste à portée de main pour le faire tourner de temps en temps. En contrepartie, il faut une pompe de cale alimentée, des amarres en bon état et une visite après chaque coup de vent.</li>
          <li><strong>À terre.</strong> Aucun risque de coulage ni de frottement contre le ponton, et c’est l’occasion d’inspecter et de repeindre la carène. En contrepartie, il faut bien vidanger tous les circuits d’eau, caler correctement le bateau et payer la mise à terre et le séjour.</li>
        </ul>
        <div class="ejemplo">
          <p class="eyebrow">Si votre port peut geler</p>
          <p>Un lac de barrage, un port intérieur ou un bateau stocké à terre loin de la côte peuvent connaître des nuits sous zéro. Là, tout circuit contenant de l’eau qu’on ne peut pas vidanger entièrement a besoin d’antigel, du type indiqué par le manuel. Sur une place de port en bord de mer, vidanger et rincer suffit en général, mais regardez les prévisions et ne le tenez pas pour acquis.</p>
        </div>

        <h2 id="motor">Moteur</h2>
        <p>C’est la première chose, et celle qui coûte le plus cher si on la néglige. Chaque moteur a ses instructions d’hivernage et elles priment sur tout ce que vous lirez ici. Voici l’ordre que je suis.</p>

        <h3 id="diesel">Inboard diesel</h3>
        <ul>
          <li>Vidange d’huile et filtre moteur chaud. L’huile usagée contient des acides qu’il vaut mieux ne pas laisser dedans tout l’hiver.</li>
          <li>Filtres à carburant et bol décanteur : purgez l’eau et changez les filtres si c’est le moment.</li>
          <li>Réservoir presque plein, pour éviter la condensation. Si vous avez déjà eu des bactéries dans le gazole, renseignez-vous sur un biocide et utilisez-le comme l’indique le fabricant.</li>
          <li>Circuit d’eau de mer : rincez-le à l’eau douce. Si le bateau risque de geler, le manuel vous dira s’il faut passer de l’antigel et lequel.</li>
          <li>Circuit fermé : contrôlez le niveau et l’état du liquide de refroidissement. S’il doit être changé selon les heures ou les années, mieux vaut maintenant qu’en mai.</li>
          <li>Rouet de pompe à eau : contrôlez-le. Certains fabricants conseillent de le retirer pendant l’hiver pour qu’il ne se déforme pas ; si vous le faites, laissez une note bien visible.</li>
          <li>Courroies, durites et colliers : un coup d’œil pour repérer fissures ou rouille.</li>
          <li>S’il a un saildrive ou une embase, changez l’huile et vérifiez qu’elle ne ressort pas laiteuse.</li>
          <li>Obturez la prise d’air et la sortie d’échappement pour que l’humidité n’entre pas, et laissez une note sur le contact pour penser à les retirer.</li>
        </ul>
        <p>Un moteur dont l’entretien est fait et noté dans un carnet ou justifié par des factures est l’un des arguments de vente les moins chers qui soient. Quand j’estime un bateau, un historique d’entretien clair pèse plus que la plupart des options.</p>

        <h3 id="gasolina">Inboard et in-bord/hors-bord essence</h3>
        <ul>
          <li>Huile et filtre moteur chaud, comme pour un diesel.</li>
          <li>L’essence vieillit vite quand elle reste immobile. Ajoutez un stabilisant et faites tourner le moteur quelques minutes pour qu’il atteigne tout le circuit, comme l’indique le fabricant.</li>
          <li>Certains manuels demandent une huile de brumisation (<em>fogging</em>) dans les cylindres, surtout sur les moteurs à carburateur. Sur les moteurs à injection, ce n’est pas toujours le cas : suivez le vôtre.</li>
          <li>Huile d’embase : si elle ressort laiteuse, il y a de l’eau dedans et il faut contrôler les joints avant l’hivernage.</li>
          <li>Soufflets de l’embase : vérifiez qu’ils ne sont pas fissurés. Un soufflet percé peut faire entrer de l’eau dans le bateau.</li>
          <li>Si le bateau risque de geler, le bloc et les collecteurs se vidangent par leurs bouchons ou se protègent avec de l’antigel, selon le manuel. Un bloc fendu par le gel est l’une des pannes les plus chères qui soient.</li>
          <li>Au printemps, ventilez le compartiment moteur avant de démarrer. Avec de l’essence, toujours.</li>
        </ul>

        <h3 id="fueraborda">Hors-bord</h3>
        <ul>
          <li>Rincez-le à l’eau douce avec des oreilles de rinçage ou le raccord de rinçage dont beaucoup de modèles sont équipés. Ne le démarrez jamais sans eau : le rouet brûle en quelques secondes.</li>
          <li>Carburant : stabilisant et quelques minutes de fonctionnement pour qu’il atteigne l’injection ou le carburateur. Certains fabricants demandent de vider la cuve du carburateur ; vérifiez pour le vôtre.</li>
          <li>Huile moteur (sur les quatre-temps) et huile d’embase. Si elle est laiteuse, direction l’atelier.</li>
          <li>Graissage des points indiqués par le manuel, anodes et un coup d’œil à l’hélice.</li>
          <li>Si vous le démontez, rangez-le à la verticale pour que toute l’eau s’écoule. S’il doit être couché, mettez-le du côté indiqué par le fabricant ; de l’autre, l’huile peut aller là où elle ne doit pas.</li>
          <li>Réservoir portable : fermé, dans un endroit ventilé et loin de toute flamme.</li>
        </ul>

        <h2 id="agua">Eau douce, WC et cale</h2>
        <ul>
          <li>Videz le réservoir d’eau douce et ouvrez les robinets jusqu’à ce que la pompe tourne à vide. Coupez la pompe et laissez les robinets ouverts.</li>
          <li>Le chauffe-eau se vidange aussi. C’est la première chose qui casse s’il gèle.</li>
          <li>Si votre port peut geler et que vous ne pouvez pas tout vidanger, utilisez uniquement un antigel compatible eau potable. L’antigel auto est toxique : ni dans le circuit d’eau ni dans les WC.</li>
          <li>WC : videz les eaux noires à la station de pompage du port, rincez à l’eau douce et utilisez le produit recommandé par le fabricant des toilettes.</li>
          <li>Cale propre et sèche. Testez la pompe de cale en soulevant le flotteur à la main. S’il y a des traces d’huile, absorbez-les avec des feuilles absorbantes : l’eau huileuse ne se pompe jamais à la mer.</li>
        </ul>

        <h2 id="baterias">Batteries</h2>
        <p>Une batterie qui passe l’hiver déchargée n’arrive souvent pas jusqu’au printemps. Et une batterie au plomb déchargée peut en plus geler ; chargée, c’est beaucoup plus difficile.</p>
        <ul>
          <li><strong>Plomb ouvert.</strong> Chargez-les complètement, nettoyez les bornes et contrôlez le niveau d’électrolyte si possible.</li>
          <li><strong>AGM et gel.</strong> Elles aussi chargées à fond, avec un chargeur qui a leur profil. Un mauvais profil les abîme petit à petit.</li>
          <li><strong>Lithium (LiFePO4).</strong> Stockez-les au niveau de charge recommandé par le fabricant, qui n’est souvent pas 100 %. Ne les chargez pas en dessous de 0 °C, sauf si elles ont un chauffage intégré. Le système de gestion (BMS) coupe généralement la charge par temps froid, mais il vaut mieux ne pas compter uniquement là-dessus.</li>
          <li>Ouvrez le coupe-batterie pour que rien ne les vide. Si le bateau reste à l’eau, laissez la pompe de cale automatique alimentée.</li>
          <li>S’il y a du courant au ponton, un chargeur d’entretien au bon profil les maintient tout l’hiver. Sinon, passez les voir toutes les quelques semaines ou emportez-les à la maison.</li>
        </ul>

        <h2 id="casco">Coque, anodes, vannes de coque, amarres et bâches</h2>
        <h3>Coque et œuvres vives</h3>
        <p>Si le bateau sort de l’eau, c’est le moment d’examiner la carène tranquillement : cloques d’osmose, état de l’antifouling, arbres, embase et hélice (chocs, jeu). Un lavage haute pression dès la sortie fait gagner des heures de grattage. S’il reste à l’eau, nettoyez au moins la ligne de flottaison.</p>
        <h3>Anodes</h3>
        <p>Contrôlez-les toutes : coque, arbres, embase ou saildrive et, s’il y en a un, propulseur d’étrave. Si elles sont très usées, remplacez-les avant de laisser le bateau. Une anode épuisée ne protège plus rien, et l’hiver est long.</p>
        <h3>Vannes de coque</h3>
        <p>À l’eau, ouvrez-les et fermez-les deux ou trois fois pour qu’elles ne grippent pas, et contrôlez tuyaux et colliers. Fermez celles qui ne servent pas, mais jamais les évacuations du cockpit : elles doivent pouvoir évacuer l’eau de pluie. À terre, laissez-les ouvertes pour qu’elles s’égouttent et graissez-les si le modèle le demande.</p>
        <h3 id="cubierta">Amarres, pare-battages et bâches</h3>
        <p>Rincez à l’eau douce tout le pont, l’accastillage et les vitres ; le sel laisse des traces difficiles à enlever ensuite. Doublez les amarres les plus sollicitées, protégez-les là où elles frottent et vérifiez les pare-battages : c’est la saison où il y a le plus de vent et où les jours passent sans que personne ne regarde le bateau. Une amarre usée en novembre peut finir en bateau contre le ponton en janvier.</p>
        <p>La bâche doit être bien tendue pour ne pas former de poches d’eau, et ventilée. Une bâche hermétique enferme l’humidité et, au printemps, on trouve de la moisissure. Rangez coussins et bimini au sec si vous le pouvez.</p>

        <h2 id="veleros">Voiles, gréement et winchs (voiliers)</h2>
        <ul>
          <li>Sortez le génois de l’enrouleur. Une voile enroulée peut se dérouler dans un coup de vent et se déchirer, en frappant au passage votre bateau et celui d’à côté.</li>
          <li>Rincez les voiles à l’eau douce, séchez-les complètement et rangez-les pliées au sec. Une voile rangée humide finit moisie.</li>
          <li>La grand-voile, déverguée ou bien protégée par son taud.</li>
          <li>Les drisses peuvent être remplacées par des messagers fins pour qu’elles ne prennent pas le soleil et ne battent pas contre le mât.</li>
          <li>Gréement dormant : examinez embouts, barres de flèche et ridoirs à la recherche de fissures ou de rouille. En cas de doute, faites-le voir par un gréeur.</li>
          <li>Winchs : démontez-les, nettoyez-les et graissez-les comme l’indique le fabricant. Les cliquets prennent en général de l’huile et non de la graisse ; le manuel du winch le précise.</li>
        </ul>

        <h2 id="interior">Intérieur : humidité, gaz, électronique et armement de sécurité</h2>
        <ul>
          <li>Ventilation : déshumidificateur s’il y a du courant et que le port l’autorise, ou au moins coffres ouverts, coussins sur la tranche et quelques absorbeurs d’humidité. L’odeur de bateau fermé fait fuir beaucoup d’acheteurs.</li>
          <li>Frigo propre, vide et porte entrouverte.</li>
          <li>Ni nourriture ni déchets à bord.</li>
          <li>Gaz : fermez la bouteille, débranchez-la et vérifiez la date de péremption du flexible.</li>
          <li>Électronique : le matériel portable (VHF, GPS à main) rentre à la maison. Les écrans fixes, avec leur cache.</li>
        </ul>
        <h3 id="papeles">Armement de sécurité et papiers</h3>
        <p>C’est le moment de noter les dates : fusées et autres pyrotechnies, extincteurs, radeau de survie, gilets gonflables et trousse de secours. En Espagne, le décret royal 339/2021 renvoie la révision des extincteurs à la réglementation de protection incendie, et celle des radeaux et gilets gonflables aux instructions du fabricant.</p>
        <p>Vérifiez aussi l’échéance de l’ITB et l’assurance. Si vous pensez vendre au printemps, avoir tout cela en règle en mars vous fait gagner des semaines : les acheteurs le demandent, et les cabinets qui gèrent les papiers sont débordés en saison.</p>

        <h2 id="errores">Les erreurs qui coûtent cher</h2>
        <ul>
          <li><strong>De l’antigel auto dans le circuit d’eau potable ou les WC.</strong> Il est toxique. Uniquement un antigel compatible eau potable, et seulement si nécessaire.</li>
          <li><strong>Démarrer le hors-bord sans eau « juste une seconde ».</strong> Le rouet brûle en quelques secondes.</li>
          <li><strong>Une bâche hermétique sans ventilation.</strong> Ce qui vous attend au printemps, c’est la moisissure.</li>
          <li><strong>Des batteries branchées sur un appareil qui consomme peu.</strong> En trois mois, ce peu suffit à les vider.</li>
          <li><strong>Laisser le génois enroulé pendant les coups de vent.</strong></li>
          <li><strong>Oublier les obturateurs d’admission et d’échappement au redémarrage.</strong> D’où la note sur le contact.</li>
          <li><strong>Des évacuations du cockpit bouchées par la bâche ou pleines de feuilles.</strong> L’eau de pluie doit pouvoir sortir.</li>
          <li><strong>Un réservoir de gazole à moitié vide.</strong> L’air à l’intérieur se condense en eau.</li>
        </ul>
"""
L["fr"]["body2"] = """
        <h2 id="venta">Si le bateau est à vendre</h2>
        <p>Un bateau à vendre en hiver doit pouvoir être montré en vingt minutes. Cela veut dire un pont propre, un intérieur sec et aéré, un moteur qui démarre du premier coup et les documents dans une pochette. Il n’en faut pas plus, mais il faut au moins cela. S’il est à sec, réglez l’accès avec le chantier avant que le premier acheteur intéressé ne se présente, car c’est ce qui fait perdre le plus de visites.</p>
"""
L["fr"]["aviso"] = "Liste indicative. Chaque moteur a son manuel et ses intervalles ; en cas de doute, votre atelier de confiance sait ce dont votre modèle a besoin."


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_main(d):
    steps = "\n".join(f"          <li><strong>{t}.</strong> {x}</li>" for t, x in d["steps"])
    groups = []
    for gk, keys in GROUPS:
        gt, labels = d["groups"][gk]
        assert len(labels) == len(keys), (gk, len(labels), len(keys))
        items = "\n".join(
            f'            <li><label><input type="checkbox" data-k="{k}"><span>{lab}</span></label></li>'
            for k, lab in zip(keys, labels))
        groups.append(f"          <h3>{gt}</h3>\n          <ul>\n{items}\n          </ul>")
    groups = "\n".join(groups)
    links = "\n".join(f'          <a href="{h}"><strong>{t}</strong><span>{s}</span></a>' for h, t, s in d["links"])
    srcs = "\n".join(f'            <li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for u, t in d["sources"])
    toc = "\n".join(f'          <li><a href="#{a}">{t}</a></li>' for a, t in d["toc"])
    meta = "".join(f"<span>{m}</span>" for m in d["meta"])
    init_count = d["count_tpl"].replace("{x}", "0").replace("{n}", str(N_ITEMS))
    return f"""<main class="art">
  <div class="wrap">
    <article>
      <header>
        <p class="eyebrow">{d["eyebrow"]}</p>
        <h1>{d["h1"]}</h1>
        <div class="meta">{meta}</div>
        <p class="lead">{d["lead"]}</p>
      </header>
      <div class="prose">

        <h2 id="corta">{d["steps_h"]}</h2>
        <p>{d["steps_intro"]}</p>
        <ol class="pm-steps">
{steps}
        </ol>
{d["body1"]}
        <div id="lista-wrap">
        <h2 id="lista">{d["list_h"]}</h2>
        <p class="pm-note">{d["list_note"]}</p>
        <div class="pm-check">
          <div class="pm-tools">
            <span class="pm-count" data-count data-tpl="{esc(d["count_tpl"])}" aria-live="polite">{init_count}</span>
            <button type="button" class="pm-print" data-print>{d["print_btn"]}</button>
            <button type="button" data-reset data-confirm="{esc(d["reset_confirm"])}">{d["reset_btn"]}</button>
          </div>
          <div class="pm-bar" aria-hidden="true"><span></span></div>
{groups}
        </div>
        </div>
{d["body2"]}
        <div class="pm-links">
{links}
        </div>

        <p class="aviso">{d["aviso"]}</p>

        <div class="fuentes" id="fuentes">
          <p><strong>{d["sources_h"]}</strong></p>
          <ul>
{srcs}
          </ul>
          <p>{d["sources_tail"]}</p>
        </div>

      </div>
    </article>

    <aside class="aside" aria-label="{{ASIDE_LABEL}}">
{{ASIDE_CARD}}
      <nav class="toc" aria-label="{d["toc_label"]}">
        <p class="eyebrow">{d["toc_h"]}</p>
        <ol>
{toc}
        </ol>
      </nav>
{{ASIDE_REL}}
    </aside>

  </div>
</main>"""


def ld(obj):
    return json.dumps(obj, ensure_ascii=False)


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def process(lang):
    d = L[lang]
    path = ROOT / (lang + "/" if lang != "es" else "") / (SLUG + ".html")
    html = path.read_text(encoding="utf-8")
    url = f"{BASE}{d['prefix']}/{SLUG}"
    img = f"{BASE}/og-image.jpg" if lang == "es" else f"{BASE}/og-image-{lang}.jpg"

    def sub1(pattern, repl, s, flags=re.S):
        new, n = re.subn(pattern, lambda m: repl, s, count=1, flags=flags)
        assert n == 1, (lang, pattern)
        return new

    html = sub1(r"<title>.*?</title>", f"<title>{esc(d['title'])}</title>", html)
    html = sub1(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(d["desc"])}">', html)
    html = sub1(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(d["title"])}">', html)
    html = sub1(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(d["desc"])}">', html)

    article = {"@context": "https://schema.org", "@type": "Article", "headline": d["h1"], "description": d["desc"],
               "author": {"@type": "Person", "name": "Juan Morante"}, "publisher": {"@type": "Organization", "name": "Plata Marine"},
               "datePublished": "2026-09-10", "dateModified": MODIFIED, "inLanguage": lang, "mainEntityOfPage": url, "image": img}
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": d["howto_name"], "inLanguage": lang,
             "step": [{"@type": "HowToStep", "position": i + 1, "name": t, "text": strip_tags(x), "url": f"{url}#corta"}
                      for i, (t, x) in enumerate(d["steps"])]}
    # quita un HowTo previo (re-ejecución) y reescribe el Article
    html = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "HowTo".*?</script>\n', "", html, flags=re.S)
    html = sub1(r'<script type="application/ld\+json">\n\{"@context": "https://schema.org", "@type": "Article".*?</script>',
                f'<script type="application/ld+json">\n{ld(article)}\n</script>\n<script type="application/ld+json">{ld(howto)}</script>', html)
    # migas: nombre de la página
    m = re.search(r'(<script type="application/ld\+json">)(\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?)(</script>)', html, re.S)
    bc = json.loads(m.group(2))
    bc["itemListElement"][-1]["name"] = d["h1"]
    html = html[:m.start(2)] + ld(bc) + html[m.end(2):]

    html = re.sub(r'<style id="pm-inv-css">.*?</style>\n', "", html, flags=re.S)
    html = sub1(r"</head>", CSS + "\n</head>", html)

    # aside: se conservan tarjeta y enlaces relacionados de la página actual
    am = re.search(r'<aside class="aside" aria-label="([^"]*)">\s*(<div class="card">.*?</div>)\s*<nav class="toc".*?</nav>\s*(<div class="rel">.*?</div>)\s*</aside>', html, re.S)
    assert am, lang
    main = build_main(d)
    main = main.replace("{ASIDE_LABEL}", am.group(1)).replace("{ASIDE_CARD}", "      " + am.group(2)).replace("{ASIDE_REL}", "      " + am.group(3))
    html = sub1(r'<main class="art">.*?</main>', main, html)

    html = re.sub(r'<script id="pm-inv-js">.*?</script>\n', "", html, flags=re.S)
    html = sub1(r'<script src="/nav\.js', JS + '\n<script src="/nav.js', html)

    path.write_text(html, encoding="utf-8")
    return path, len(d["title"]), len(d["desc"])


if __name__ == "__main__":
    for lg in ("es", "ca", "en", "fr"):
        p, lt, ldsc = process(lg)
        print(f"{lg}: {p.relative_to(ROOT)}  title={lt}  desc={ldsc}  items={N_ITEMS}")
