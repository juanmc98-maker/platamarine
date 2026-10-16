#!/usr/bin/env python3
"""Genera /skipper/ (ES) y /en/skipper/ (EN): página de marca SKIPPER Powerboats.
Datos: configurador oficial SKIPPER (precios, oct 2026) y fichas de skipper-bsk.com (especificaciones)."""
import os, re, json, urllib.parse

NOINDEX = os.environ.get("SK_NOINDEX","1") == "1"  # quitar al aprobar SKIPPER
ROOT = os.environ.get("PM_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = "/skipper/fotos/"
WA_NUM = "34633742973"

MODELS = [
 {"id": "ace360", "name": "ACE 360", "img": "ace-run", "gal": ["ace-proa", "hero"],
  "tag": {"es": "La nueva. Presentada en mayo de 2026.", "en": "The new one. Unveiled in May 2026."},
  "spec": {"loa": "10,85 m", "beam": "3,10 m", "pax": "14", "vmax": "70 nudos", "fuel": "700 L", "cat": "B", "weight": "3.700 kg", "dr": "24°"},
  "spec_en": {"loa": "10.85 m", "beam": "3.10 m", "pax": "14", "vmax": "70 knots", "fuel": "700 L", "cat": "B", "weight": "3,700 kg", "dr": "24°"},
  "engines": [("2× Mercury Verado 300 V8", 329000), ("2× Yamaha 300 V6", 331000), ("2× Mercury 300 V8 Racing AMS", 340000),
              ("2× Mercury Verado 350 V10", 345000), ("2× Mercury Verado 400 V10", 358000), ("2× Mercury 400 Racing V10", 370000)]},
 {"id": "38nc", "name": "38 NC+", "img": "38-sunset", "gal": ["38-perfil", "38-34"],
  "tag": {"es": "La renovada: hardtop de carbono y parabrisas cerrado.", "en": "Refreshed: carbon hardtop and closed windscreen."},
  "spec": {"loa": "12,00 m", "beam": "3,35 m", "pax": "12", "vmax": "70 nudos", "fuel": "2 × 340 L", "cat": "B", "weight": "5.200 kg", "dr": "24°"},
  "spec_en": {"loa": "12.00 m", "beam": "3.35 m", "pax": "12", "vmax": "70 knots", "fuel": "2 × 340 L", "cat": "B", "weight": "5,200 kg", "dr": "24°"},
  "engines": [("2× Mercury Verado 400 V10", 423000), ("2× Mercury Verado 425 V10", 426000),
              ("2× Mercury 400 Racing V10", 438000), ("2× Mercury 500 Racing V8", 479000)]},
 {"id": "42nc", "name": "42 NC", "img": "42-aerea", "gal": ["42-proa"],
  "tag": {"es": "La insignia: cama doble y baño en la consola.", "en": "The flagship: double bed and head in the console."},
  "spec": {"loa": "12,40 m", "beam": "3,60 m", "pax": "12", "vmax": "80 nudos", "fuel": "880–1.000 L", "cat": "B", "weight": "6.200 kg", "dr": "24°"},
  "spec_en": {"loa": "12.40 m", "beam": "3.60 m", "pax": "12", "vmax": "80 knots", "fuel": "880–1,000 L", "cat": "B", "weight": "6,200 kg", "dr": "24°"},
  "engines": [("3× Mercury Verado V10 400", 588000), ("3× Mercury Verado V10 425", 592000), ("3× Mercury 400 Racing V10", 612000),
              ("2× Mercury Verado V12 600", 639000), ("3× Mercury 500 Racing V8", 671000), ("4× Mercury 500 Racing V8", 751000)]},
]

T = {
 "es": {
  "path": "/skipper/", "home": "/", "tpl": "astilleros/index.html",
  "title": "SKIPPER Powerboats en Cataluña y Baleares: modelos y precios · Plata Marine",
  "desc": "Semirrígidas SKIPPER ACE 360, 38 NC+ y 42 NC en Cataluña y Baleares. Precios por motorización desde 329.000 € +IVA, fichas técnicas y cómo se compra bajo pedido.",
  "eyebrow": "Contacto oficial en Cataluña y Baleares",
  "h1": "Semirrígidas que se construyen para ir rápido. Y para ti.",
  "lead": "SKIPPER fabrica en Grecia semirrígidas de alto rendimiento de 11 a 12,4 metros. Te ayudo a elegir modelo y motores, y estoy contigo hasta el día de la entrega.",
  "cta": "Hablar con Juan", "cta2": "Ver modelos y precios",
  "stats": [("70–80", "nudos de velocidad máxima"), ("24°", "de astilla muerta"), ("Cat. B", "navegación en altura"), ("2015", "año de fundación")],
  "models_h": "Elige tu SKIPPER", "models_p": "Toca un modelo, elige motores y verás el precio al momento.",
  "labels": {"loa": "Eslora", "beam": "Manga", "pax": "Personas", "vmax": "Velocidad máx.", "fuel": "Combustible", "cat": "Categoría", "weight": "Peso sin motores", "dr": "Astilla muerta"},
  "pick": "Elige motorización", "price": "Precio con esta motorización", "vat": "+IVA", "licence": "Titulación: PER o superior",
  "ask": "Pedir presupuesto oficial", "from": "desde",
  "wa_cfg": "Hola Juan, me interesa el SKIPPER {m} con {e}. ¿Me preparas el presupuesto oficial?",
  "wa_gen": "Hola Juan, me interesa un SKIPPER. ¿Me ayudas a elegir modelo?",
  "cmp_h": "Los tres, cara a cara", "cmp_model": "Modelo", "cmp_price": "Desde",
  "tech_h": "Por qué navegan así", "tech_p": "Lo que el astillero ha puesto en el casco y en la cubierta de los tres modelos.",
  "tech": [("Casco AeroQuad™ de 4 escalones", "Patente de SKIPPER: los escalones meten aire bajo el casco, reducen la fricción y hacen que el barco planee antes y gaste menos."),
           ("V profunda de 24°", "Corta la ola en lugar de saltar sobre ella. Más seco y más cómodo cuando el mar se pone serio."),
           ("Cubierta InfinityDeck™", "La manga se mantiene de popa a proa: pasillos anchos para moverte y más espacio útil en el mismo metro de eslora."),
           ("Construcción en composite", "Estructura rígida pensada para mar abierto, con acabados de barco grande.")],
  "tech_note": "Descripción del astillero, según sus fichas técnicas.",
  "std_h": "Lo que no tendrás que pagar aparte", "std_p": "Equipamiento de serie común en los tres modelos:",
  "std": ["Hardtop", "Hélice de proa", "Ancla con mando a distancia", "Pantalla Raymarine", "VHF y cartografía", "Sonido JL Audio",
          "Wetbar con nevera", "Baldeo de agua dulce", "Luces LED de cubierta y subacuáticas", "Cargador de baterías y toma de tierra"],
  "std_more": "En el 38 NC+ y el 42 NC, además, hardtop de carbono y salpicadero de carbono real (según configuración).",
  "how_h": "Cómo se compra un SKIPPER",
  "steps": [("Lo hablamos", "Me cuentas cómo vas a usar el barco y elegimos modelo, motores y colores."),
            ("Presupuesto oficial", "SKIPPER emite el presupuesto con tu configuración exacta."),
            ("Contrato con el astillero", "Firmas con SKIPPER y la señal se paga directamente al astillero, nunca a mí."),
            ("Fabricación y entrega", "Sigo la fabricación contigo y coordino transporte, matriculación y puesta en marcha.")],
  "about_h": "Quién hay detrás",
  "about_sk": "SKIPPER es la marca de BSK Marine, astillero fundado en 2015 en Koropi, a las afueras de Atenas. En pocos años ha llevado sus semirrígidas por todo el Mediterráneo.",
  "about_me": "Yo soy Juan Morante, de Plata Marine. Soy el contacto de SKIPPER en Cataluña y Baleares: te asesoro, te acompaño a ver el barco y me ocupo de que todo llegue bien hasta el amarre.",
  "end_h": "¿Te imaginas en uno?", "end_p": "Escríbeme y lo vemos con calma. Sin compromiso.",
  "small": "Precios orientativos del configurador oficial de SKIPPER (octubre de 2026), sin transporte, matriculación ni impuestos. Especificaciones según las fichas del astillero. Pueden cambiar y no son vinculantes: el precio final es siempre el del presupuesto oficial de SKIPPER. Podemos equivocarnos; si ves un error, avísanos.",
  "crumb": "SKIPPER Powerboats",
 },
 "en": {
  "path": "/en/skipper/", "home": "/en/", "tpl": "en/astilleros/index.html",
  "title": "SKIPPER Powerboats in Catalonia and the Balearics: models and prices · Plata Marine",
  "desc": "SKIPPER ACE 360, 38 NC+ and 42 NC RIBs in Catalonia and the Balearic Islands. Prices by engine package from €329,000 +VAT, specs and how to order one.",
  "eyebrow": "Official contact in Catalonia and the Balearics",
  "h1": "RIBs built to go fast. And built for you.",
  "lead": "SKIPPER builds high-performance RIBs from 11 to 12.4 metres in Greece. I help you choose model and engines, and I'm with you until delivery day.",
  "cta": "Talk to Juan", "cta2": "See models and prices",
  "stats": [("70–80", "knots top speed"), ("24°", "deadrise"), ("Cat. B", "offshore design category"), ("2015", "year founded")],
  "models_h": "Choose your SKIPPER", "models_p": "Tap a model, pick the engines and see the price instantly.",
  "labels": {"loa": "Length", "beam": "Beam", "pax": "Persons", "vmax": "Top speed", "fuel": "Fuel", "cat": "Category", "weight": "Dry weight", "dr": "Deadrise"},
  "pick": "Choose engines", "price": "Price with these engines", "vat": "+VAT", "licence": "Licence: Spanish PER or higher",
  "ask": "Ask for the official quote", "from": "from",
  "wa_cfg": "Hi Juan, I'm interested in the SKIPPER {m} with {e}. Can you prepare the official quote?",
  "wa_gen": "Hi Juan, I'm interested in a SKIPPER. Can you help me choose a model?",
  "cmp_h": "All three, side by side", "cmp_model": "Model", "cmp_price": "From",
  "tech_h": "Why they run like this", "tech_p": "What the shipyard has built into the hull and deck of all three models.",
  "tech": [("AeroQuad™ 4-step hull", "SKIPPER's patent: the steps feed air under the hull, cut drag and get the boat on the plane sooner and more efficiently."),
           ("24° deep V", "Cuts through the waves instead of slamming on them. Drier and more comfortable when the sea gets serious."),
           ("InfinityDeck™ layout", "The beam stays constant from stern to bow: wide side decks and more usable space for the same length."),
           ("Composite construction", "A rigid structure designed for open water, with big-boat finishes.")],
  "tech_note": "Shipyard's description, from its technical sheets.",
  "std_h": "What you won't pay extra for", "std_p": "Standard equipment shared by all three models:",
  "std": ["Hardtop", "Bow thruster", "Remote-controlled anchor", "Raymarine screen", "VHF and charts", "JL Audio sound",
          "Wet bar with fridge", "Fresh water washdown", "LED deck and underwater lights", "Battery charger and shore power"],
  "std_more": "On the 38 NC+ and 42 NC you also get a carbon hardtop and real carbon dashboard (depending on configuration).",
  "how_h": "How to buy a SKIPPER",
  "steps": [("We talk", "You tell me how you'll use the boat and we choose model, engines and colours."),
            ("Official quote", "SKIPPER issues the quote for your exact configuration."),
            ("Contract with the shipyard", "You sign with SKIPPER and the deposit is paid directly to the shipyard, never to me."),
            ("Build and delivery", "I follow the build with you and coordinate transport, registration and commissioning.")],
  "about_h": "Who's behind it",
  "about_sk": "SKIPPER is the brand of BSK Marine, a shipyard founded in 2015 in Koropi, just outside Athens. In a few years its RIBs have spread across the Mediterranean.",
  "about_me": "I'm Juan Morante, from Plata Marine. I'm SKIPPER's contact in Catalonia and the Balearics: I advise you, come with you to see the boat and make sure everything reaches your berth properly.",
  "end_h": "Can you picture yourself in one?", "end_p": "Message me and we'll go through it calmly. No commitment.",
  "small": "Indicative prices from SKIPPER's official configurator (October 2026), excluding transport, registration and taxes. Specs from the shipyard's technical sheets. They may change and are not binding: the final price is always SKIPPER's official quote. We may be wrong; if you spot a mistake, let us know.",
  "crumb": "SKIPPER Powerboats",
 },
}

def eur(n, lang):
    s = f"{n:,}"
    return (s.replace(",", ".") + " €") if lang == "es" else ("€" + s)

def wa(text):
    return f"https://wa.me/{WA_NUM}?text=" + urllib.parse.quote(text)

def pic(name, alt, sizes="100vw", cls="", lazy=True, w=1920, h=1080):
    return (f'<img{(" class=%s" % chr(34) + cls + chr(34)) if cls else ""} src="{F}{name}.jpg" srcset="{F}{name}-m.jpg 900w, {F}{name}.jpg 1920w" '
            f'sizes="{sizes}" alt="{alt}" width="{w}" height="{h}"{" loading=" + chr(34) + "lazy" + chr(34) if lazy else ""} decoding="async">')

CSS = r"""
.sk{--ink:#0E3042;--sea:#0B766B;--sea2:#2BB3A3;--night:#06080b;--line:rgba(14,48,66,.12);--hk:"Hanken Grotesk",system-ui,sans-serif;background:#fff}
.sk *{box-sizing:border-box}
.sk h1,.sk h2,.sk h3{font-family:var(--hk);letter-spacing:-.01em}
.sk-hero{position:relative;min-height:min(92vh,860px);display:flex;align-items:flex-end;color:#fff;background:var(--night);overflow:hidden}
.sk-hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 50%;transform:scale(1.04);animation:skz 14s ease-out forwards}
@keyframes skz{to{transform:scale(1)}}
.sk-hero:after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(6,8,11,.92) 0,rgba(6,8,11,.45) 45%,rgba(6,8,11,.1) 75%),linear-gradient(90deg,rgba(6,8,11,.55),transparent 60%)}
.sk-hero .wrap{position:relative;z-index:1;width:100%;max-width:1180px;padding:0 24px 72px}
.sk-logo{height:34px;width:auto;margin:0 0 26px;display:block}
.sk-eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;margin:0 0 16px;padding:7px 12px;border:1px solid rgba(255,255,255,.3);border-radius:999px;backdrop-filter:blur(6px)}
.sk-eyebrow:before{content:"";width:7px;height:7px;border-radius:50%;background:var(--sea2)}
.sk-hero h1{color:#fff!important;font-size:clamp(36px,6vw,72px);line-height:1.02;font-weight:800;margin:0 0 18px;max-width:900px}
.sk-hero .lead{font-size:clamp(17px,2vw,20px);line-height:1.55;max-width:600px;margin:0 0 30px;color:rgba(255,255,255,.88)}
.sk-btns{display:flex;gap:12px;flex-wrap:wrap}
.sk-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;font-weight:700;border-radius:999px;padding:15px 26px;text-decoration:none;font-size:16px;transition:transform .15s,background .15s;border:0;cursor:pointer;font-family:inherit}
.sk-btn:hover{transform:translateY(-1px)}
.sk-btn.pri{background:var(--sea);color:#fff}.sk-btn.pri:hover{background:#085C53}
.sk-btn.ghost{border:1px solid rgba(255,255,255,.5);color:#fff}.sk-btn.ghost:hover{background:rgba(255,255,255,.1)}
.sk-btn svg{width:19px;height:19px;fill:currentColor}
.sk-stats{background:var(--night);color:#fff;border-top:1px solid rgba(255,255,255,.08)}
.sk-stats .wrap{display:grid;grid-template-columns:repeat(4,1fr);max-width:1180px;padding:0 24px}
.sk-stats div{padding:26px 10px;border-right:1px solid rgba(255,255,255,.08)}.sk-stats div:last-child{border-right:0}
.sk-stats b{display:block;font-family:var(--hk);font-size:clamp(26px,3.4vw,38px);font-weight:800;line-height:1}
.sk-stats span{font-size:13.5px;opacity:.65}
.sk-sec{padding:96px 0}.sk-sec>.wrap{max-width:1180px;padding:0 24px}
.sk-kick{font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--sea);font-weight:700;margin:0 0 10px}
.sk-sec h2{font-size:clamp(30px,4.4vw,48px);line-height:1.05;margin:0 0 12px;color:var(--ink)}
.sk-sub{font-size:18px;opacity:.75;margin:0 0 40px;max-width:640px}
.sk-tabs{display:flex;gap:6px;background:#EEF2F4;border-radius:999px;padding:6px;width:max-content;max-width:100%;overflow-x:auto;margin:0 0 30px}
.sk-tabs button{font:inherit;font-weight:700;font-size:15px;border:0;background:transparent;color:var(--ink);padding:11px 22px;border-radius:999px;cursor:pointer;white-space:nowrap}
.sk-tabs button[aria-selected=true]{background:var(--ink);color:#fff}
.sk-panel{display:grid;grid-template-columns:1.25fr 1fr;gap:0;border:1px solid var(--line);border-radius:22px;overflow:hidden;background:#fff;box-shadow:0 30px 60px -40px rgba(14,48,66,.45)}
.sk-panel[hidden]{display:none}
.sk-media{background:var(--night);position:relative;min-height:420px}
.sk-media>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .35s}
.sk-thumbs{position:absolute;left:16px;bottom:16px;display:flex;gap:8px;z-index:2}
.sk-thumbs button{width:66px;height:44px;border-radius:8px;border:2px solid rgba(255,255,255,.5);padding:0;overflow:hidden;cursor:pointer;background:#000}
.sk-thumbs button[aria-pressed=true]{border-color:#fff}
.sk-thumbs img{width:100%;height:100%;object-fit:cover;display:block}
.sk-info{padding:30px 30px 28px;display:flex;flex-direction:column}
.sk-info h3{font-size:34px;margin:0 0 4px;color:var(--ink)}
.sk-tag{margin:0 0 20px;opacity:.7;font-size:15.5px}
.sk-spec{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border:1px solid var(--line);border-radius:12px;margin:0 0 22px}
.sk-spec div{padding:11px 10px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.sk-spec div:nth-child(4n){border-right:0}.sk-spec div:nth-last-child(-n+4){border-bottom:0}
.sk-spec dt{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;opacity:.55;margin:0 0 3px}
.sk-spec dd{margin:0;font-weight:700;color:var(--ink);font-size:15px}
.sk-pick{font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;opacity:.6;margin:0 0 8px;font-weight:700}
.sk-eng{display:grid;gap:7px;margin:0 0 20px}
.sk-eng label{display:flex;align-items:center;justify-content:space-between;gap:12px;border:1px solid var(--line);border-radius:10px;padding:11px 13px;cursor:pointer;font-size:14.5px;transition:border-color .15s,background .15s}
.sk-eng label:hover{border-color:rgba(14,48,66,.35)}
.sk-eng input{accent-color:var(--sea);margin:0 10px 0 0}
.sk-eng label>span:first-child{display:flex;align-items:center}
.sk-eng label b{white-space:nowrap;color:var(--ink)}
.sk-eng label:has(input:checked){border-color:var(--sea);background:#F0F8F7}
.sk-total{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:18px;margin-top:auto}
.sk-total small{display:block;font-size:12.5px;opacity:.6;margin-bottom:2px}
.sk-total strong{font-family:var(--hk);font-size:34px;color:var(--ink);line-height:1}
.vat{color:#C62828;font-weight:800;font-size:15px;margin-left:6px}
.sk-lic{font-size:13px;opacity:.6;margin:6px 0 0}
.sk-cmp{overflow-x:auto;border:1px solid var(--line);border-radius:16px}
.sk-cmp table{width:100%;border-collapse:collapse;min-width:620px;font-size:15px}
.sk-cmp th,.sk-cmp td{padding:14px 18px;text-align:left;border-bottom:1px solid var(--line)}
.sk-cmp thead th{background:var(--ink);color:#fff;font-family:var(--hk);font-size:17px}
.sk-cmp tbody th{font-weight:600;opacity:.7;font-size:13.5px;text-transform:uppercase;letter-spacing:.05em;width:24%}
.sk-cmp tr:last-child td,.sk-cmp tr:last-child th{border-bottom:0}
.sk-cmp td b{color:var(--ink)}
.sk-dark{background:var(--night);color:#fff}.sk-dark h2{color:#fff!important}.sk-dark .sk-sub{color:rgba(255,255,255,.75);opacity:1}.sk-dark .sk-kick{color:var(--sea2)}
.sk-tech{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.sk-tech img{width:100%;height:auto;border-radius:18px;display:block}
.sk-tech ol{list-style:none;margin:0;padding:0;counter-reset:t}
.sk-tech li{counter-increment:t;padding:18px 0 18px 54px;position:relative;border-top:1px solid rgba(255,255,255,.12)}
.sk-tech li:before{content:"0" counter(t);position:absolute;left:0;top:18px;font-family:var(--hk);font-weight:800;font-size:22px;color:var(--sea2)}
.sk-tech b{display:block;font-size:18px;margin-bottom:5px}.sk-tech span{color:rgba(255,255,255,.72);line-height:1.55;font-size:15.5px}
.sk-note{font-size:12.5px;opacity:.5;margin:14px 0 0}
.sk-std{display:grid;grid-template-columns:1fr 1.1fr;gap:56px;align-items:center}
.sk-std img{width:100%;height:auto;border-radius:18px;background:var(--night);display:block}
.sk-chips{display:flex;flex-wrap:wrap;gap:9px;margin:0 0 18px;padding:0;list-style:none}
.sk-chips li{border:1px solid var(--line);border-radius:999px;padding:9px 15px;font-size:14.5px;font-weight:600;color:var(--ink);background:#F7FAFB}
.sk-chips li:before{content:"✓";color:var(--sea);margin-right:7px;font-weight:800}
.sk-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:26px;counter-reset:s;list-style:none;margin:0;padding:0}
.sk-steps li{counter-increment:s;border-top:3px solid var(--ink);padding-top:18px}
.sk-steps li:before{content:"0" counter(s);font-family:var(--hk);font-weight:800;font-size:30px;color:var(--sea);display:block;margin-bottom:10px}
.sk-steps b{display:block;font-size:18px;color:var(--ink);margin-bottom:6px}.sk-steps span{font-size:15.5px;opacity:.75;line-height:1.55}
.sk-about{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.sk-about div{border-radius:18px;padding:30px;background:#F3F6F7}
.sk-about div:first-child{background:var(--ink);color:#fff}
.sk-about img{height:22px;width:auto;margin-bottom:16px;display:block}
.sk-about p{margin:0;font-size:16.5px;line-height:1.6}
.sk-about b{font-family:var(--hk);display:block;font-size:20px;margin-bottom:14px;color:var(--ink)}
.sk-end{position:relative;color:#fff;text-align:center;overflow:hidden;background:var(--night)}
.sk-end>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.45}
.sk-end .wrap{position:relative}
.sk-end h2{color:#fff!important}.sk-end .sk-sub{color:rgba(255,255,255,.85);opacity:1;margin:0 auto 28px}
.sk-end .sk-btns{justify-content:center}
.sk-small{font-size:12.5px;color:rgba(255,255,255,.6);max-width:780px;margin:36px auto 0;line-height:1.55}
.sk-float{position:fixed;right:16px;bottom:16px;z-index:50;display:none}
@media (max-width:980px){.sk-panel{grid-template-columns:1fr}.sk-media{min-height:0;aspect-ratio:16/10}.sk-tech,.sk-std{grid-template-columns:1fr;gap:34px}.sk-steps{grid-template-columns:1fr 1fr}}
@media (max-width:640px){.sk-hero{min-height:88vh}.sk-hero .wrap{padding:0 18px 46px}.sk-logo{height:26px}
.sk-stats .wrap{grid-template-columns:1fr 1fr;padding:0 8px}.sk-stats div:nth-child(2){border-right:0}.sk-stats div:nth-child(-n+2){border-bottom:1px solid rgba(255,255,255,.08)}
.sk-sec{padding:64px 0}.sk-sec>.wrap{padding:0 18px}.sk-info{padding:22px 18px}.sk-spec{grid-template-columns:repeat(2,1fr)}
.sk-spec div:nth-child(4n){border-right:1px solid var(--line)}.sk-spec div:nth-child(2n){border-right:0}.sk-spec div:nth-last-child(-n+4){border-bottom:1px solid var(--line)}.sk-spec div:nth-last-child(-n+2){border-bottom:0}
.sk-steps,.sk-about{grid-template-columns:1fr}.sk-btn{width:100%}.sk-total .sk-btn{width:100%}}
@media (prefers-reduced-motion:reduce){.sk-hero>img{animation:none;transform:none}}
"""

JS = r"""
(function(){
 var tabs=document.querySelectorAll('.sk-tabs button');
 tabs.forEach(function(b){b.addEventListener('click',function(){
  tabs.forEach(function(x){x.setAttribute('aria-selected',x===b?'true':'false')});
  document.querySelectorAll('.sk-panel').forEach(function(p){p.hidden=p.id!==b.getAttribute('aria-controls')});
 })});
 document.querySelectorAll('.sk-panel').forEach(function(p){
  var out=p.querySelector('[data-total]'),a=p.querySelector('[data-wa]');
  function upd(){var r=p.querySelector('input:checked');if(!r)return;out.textContent=r.dataset.fmt;
   a.href=a.dataset.base+encodeURIComponent(a.dataset.tpl.replace('{e}',r.value));}
  p.querySelectorAll('input').forEach(function(i){i.addEventListener('change',upd)});upd();
  var main=p.querySelector('.sk-media>img');
  p.querySelectorAll('.sk-thumbs button').forEach(function(t){t.addEventListener('click',function(){
   main.src=t.dataset.src;main.srcset=t.dataset.srcset;
   p.querySelectorAll('.sk-thumbs button').forEach(function(x){x.setAttribute('aria-pressed',x===t?'true':'false')});})});
 });
})();
"""

WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2z"/></svg>'

def header_from(tpl, lang, t):
    s = open(tpl, encoding="utf-8").read()
    h = s[s.find("<body>") + 6:s.find("<main")]
    sw = ('<div class="langsw" aria-label="%s">' % ("Idioma" if lang == "es" else "Language") +
          '<a href="https://www.platamarine.com/skipper/"%s><span class="flag flag-es" aria-hidden="true"></span><span class="sr-only">ES</span></a>' % (' aria-current="page"' if lang == "es" else "") +
          '<a href="https://www.platamarine.com/en/skipper/"%s><span class="flag flag-en" aria-hidden="true"></span><span class="sr-only">EN</span></a></div>' % (' aria-current="page"' if lang == "en" else ""))
    h = re.sub(r'<div class="langsw".*?</div>', sw, h, count=1, flags=re.S)
    h = re.sub(r'(<a class="btn btn-wa" href=")[^"]*(")', lambda m: m.group(1) + wa(t["wa_gen"]) + m.group(2), h, count=1)
    return h

def footer_from(tpl):
    s = open(tpl, encoding="utf-8").read()
    return s[s.find('<footer class="foot">'):s.find("</footer>") + 9]

def build(lang):
    t = T[lang]; L = t["labels"]
    tpl = os.path.join(ROOT, t["tpl"])
    url = "https://www.platamarine.com" + t["path"]
    base = f"https://wa.me/{WA_NUM}?text="

    tabs, panels = [], []
    for i, m in enumerate(MODELS):
        sp = m["spec"] if lang == "es" else m["spec_en"]
        tabs.append(f'<button type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" aria-controls="p-{m["id"]}">{m["name"]}</button>')
        spec = "".join(f'<div><dt>{L[k]}</dt><dd>{sp[k]}</dd></div>' for k in ("loa", "beam", "pax", "vmax", "fuel", "weight", "dr", "cat"))
        eng = "".join(
            f'<label><span><input type="radio" name="e-{m["id"]}" value="{n}" data-fmt="{eur(p, lang)}"{" checked" if j == 0 else ""}>{n}</span><b>{eur(p, lang)}</b></label>'
            for j, (n, p) in enumerate(m["engines"]))
        imgs = [m["img"]] + m["gal"]
        thumbs = "".join(
            f'<button type="button" aria-pressed="{"true" if k == 0 else "false"}" aria-label="{k + 1}" data-src="{F}{g}.jpg" data-srcset="{F}{g}-m.jpg 900w, {F}{g}.jpg 1920w">'
            f'<img src="{F}{g}-m.jpg" alt="" loading="lazy" width="900" height="506"></button>' for k, g in enumerate(imgs))
        tplmsg = t["wa_cfg"].replace("{m}", m["name"])
        panels.append(f'''<div class="sk-panel" id="p-{m["id"]}" role="tabpanel"{"" if i == 0 else " hidden"}>
  <div class="sk-media">{pic(m["img"], "SKIPPER " + m["name"], "(max-width:980px) 100vw, 60vw", lazy=i != 0)}<div class="sk-thumbs">{thumbs}</div></div>
  <div class="sk-info">
    <h3>SKIPPER {m["name"]}</h3><p class="sk-tag">{m["tag"][lang]}</p>
    <dl class="sk-spec">{spec}</dl>
    <p class="sk-pick">{t["pick"]}</p>
    <div class="sk-eng">{eng}</div>
    <div class="sk-total"><div><small>{t["price"]}</small><strong data-total>{eur(m["engines"][0][1], lang)}</strong><span class="vat">{t["vat"]}</span><p class="sk-lic">{t["licence"]}</p></div>
    <a class="sk-btn pri" data-wa data-base="{base}" data-tpl="{tplmsg}" href="{wa(tplmsg.replace("{e}", m["engines"][0][0]))}" target="_blank" rel="noopener">{WA_SVG}{t["ask"]}</a></div>
  </div>
</div>''')

    rows = [(t["cmp_price"], [f'<b>{eur(min(p for _, p in m["engines"]), lang)}</b> <span class="vat">{t["vat"]}</span>' for m in MODELS])]
    for k in ("loa", "beam", "pax", "vmax", "fuel", "weight"):
        rows.append((L[k], [(m["spec"] if lang == "es" else m["spec_en"])[k] for m in MODELS]))
    rows.append((t["pick"], [str(len(m["engines"])) + (" opciones" if lang == "es" else " options") for m in MODELS]))
    cmp = ('<table><thead><tr><th>' + t["cmp_model"] + '</th>' + "".join(f'<th>{m["name"]}</th>' for m in MODELS) + '</tr></thead><tbody>' +
           "".join('<tr><th>' + a + '</th>' + "".join(f'<td>{v}</td>' for v in vals) + '</tr>' for a, vals in rows) + '</tbody></table>')

    offers = [{"@type": "Product", "name": "SKIPPER " + m["name"], "brand": {"@type": "Brand", "name": "SKIPPER Powerboats"},
               "image": "https://www.platamarine.com" + F + m["img"] + ".jpg",
               "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": min(p for _, p in m["engines"]),
                          "highPrice": max(p for _, p in m["engines"]), "offerCount": len(m["engines"])}} for m in MODELS]
    ld = {"@context": "https://schema.org", "@graph": [{"@type": "WebPage", "name": t["title"], "description": t["desc"], "inLanguage": lang, "url": url,
           "publisher": {"@type": "Organization", "name": "Plata Marine"}}, *offers]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Plata Marine", "item": "https://www.platamarine.com" + t["home"]},
        {"@type": "ListItem", "position": 2, "name": t["crumb"], "item": url}]}
    stats = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in t["stats"])
    tech = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in t["tech"])
    std = "".join(f"<li>{x}</li>" for x in t["std"])
    steps = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in t["steps"])

    html = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t["title"]}</title>
<meta name="description" content="{t["desc"]}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="es" href="https://www.platamarine.com/skipper/">
<link rel="alternate" hreflang="en" href="https://www.platamarine.com/en/skipper/">
<link rel="alternate" hreflang="x-default" href="https://www.platamarine.com/skipper/">
<link rel="icon" type="image/png" href="/logo-plata-marine.png">
<meta property="og:title" content="{t["title"]}">
<meta property="og:description" content="{t["desc"]}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://www.platamarine.com{F}hero.jpg">
<meta name="theme-color" content="#06080b">{"<meta name=\"robots\" content=\"noindex\">" if NOINDEX else ""}
<link rel="preload" as="image" href="{F}hero.jpg" imagesrcset="{F}hero-m.jpg 900w, {F}hero.jpg 1920w" imagesizes="100vw">
<link rel="stylesheet" href="/guias/guias.css">
<link rel="stylesheet" href="/nav.css?v=20261006m">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(crumbs, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
{header_from(tpl, lang, t)}<main class="sk">
<section class="sk-hero">
  {pic("hero", "SKIPPER ACE 360", lazy=False)}
  <div class="wrap">
    <img class="sk-logo" src="{F}skipper-logo-blanco.png" alt="SKIPPER" width="900" height="103">
    <p class="sk-eyebrow">{t["eyebrow"]}</p>
    <h1>{t["h1"]}</h1>
    <p class="lead">{t["lead"]}</p>
    <div class="sk-btns"><a class="sk-btn pri" href="{wa(t["wa_gen"])}" target="_blank" rel="noopener">{WA_SVG}{t["cta"]}</a><a class="sk-btn ghost" href="#modelos">{t["cta2"]}</a></div>
  </div>
</section>
<div class="sk-stats"><div class="wrap">{stats}</div></div>
<section class="sk-sec" id="modelos">
  <div class="wrap">
    <p class="sk-kick">SKIPPER Powerboats</p><h2>{t["models_h"]}</h2><p class="sk-sub">{t["models_p"]}</p>
    <div class="sk-tabs" role="tablist">{"".join(tabs)}</div>
    {"".join(panels)}
  </div>
</section>
<section class="sk-sec" style="padding-top:0">
  <div class="wrap"><h2>{t["cmp_h"]}</h2><div class="sk-cmp specs" style="margin-top:26px">{cmp}</div></div>
</section>
<section class="sk-sec sk-dark">
  <div class="wrap sk-tech">
    <div><p class="sk-kick">AeroQuad™ · InfinityDeck™</p><h2>{t["tech_h"]}</h2><p class="sk-sub">{t["tech_p"]}</p><ol>{tech}</ol><p class="sk-note">{t["tech_note"]}</p></div>
    {pic("ace-proa", "SKIPPER ACE 360", "(max-width:980px) 100vw, 50vw")}
  </div>
</section>
<section class="sk-sec">
  <div class="wrap sk-std">
    {pic("38-planta", "SKIPPER 38 NC+", "(max-width:980px) 100vw, 45vw")}
    <div><h2>{t["std_h"]}</h2><p class="sk-sub" style="margin-bottom:22px">{t["std_p"]}</p><ul class="sk-chips">{std}</ul><p class="sk-note" style="opacity:.65">{t["std_more"]}</p></div>
  </div>
</section>
<section class="sk-sec" style="padding-top:0">
  <div class="wrap"><h2 style="margin-bottom:34px">{t["how_h"]}</h2><ol class="sk-steps">{steps}</ol></div>
</section>
<section class="sk-sec" style="padding-top:0">
  <div class="wrap"><h2 style="margin-bottom:28px">{t["about_h"]}</h2>
    <div class="sk-about"><div><img src="{F}skipper-logo-blanco.png" alt="SKIPPER" width="900" height="103" loading="lazy"><p>{t["about_sk"]}</p></div>
    <div><b>Plata Marine</b><p>{t["about_me"]}</p></div></div>
  </div>
</section>
<section class="sk-sec sk-end">
  {pic("42-aerea", "SKIPPER 42 NC")}
  <div class="wrap">
    <h2>{t["end_h"]}</h2><p class="sk-sub">{t["end_p"]}</p>
    <div class="sk-btns"><a class="sk-btn pri" href="{wa(t["wa_gen"])}" target="_blank" rel="noopener">{WA_SVG}{t["cta"]}</a></div>
    <p class="sk-small">{t["small"]}</p>
  </div>
</section>
</main>
{footer_from(tpl)}
<script>{JS}</script>
<script src="/nav.js?v=20261006m" defer></script>
<script src="/consent.js?v=20261006" defer></script>
<script src="/analytics.js?v=20261006" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, t["path"].strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    print("ok", out, len(html))

for L_ in ("es", "en"):
    build(L_)
