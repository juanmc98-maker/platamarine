# Genera /vender/guia-fotos-barco.html en ES, CA y EN a partir de la cabecera y pie
# de /vender/broker-nautico-barcelona-maresme.html de cada idioma.
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'vender/guia-fotos-barco.html'
BASE = 'https://www.platamarine.com'
TPL = 'vender/broker-nautico-barcelona-maresme.html'
TYPES = ['semirrigida', 'lancha', 'cabinado', 'fly', 'velero']

T = {
'es': dict(
  pre='', title='Cómo hacer las fotos de tu barco para venderlo · guía por tipo',
  desc='Guía sencilla para hacer con el móvil las fotos de tu barco para el anuncio: cómo prepararlo, la luz, el encuadre y las 6 fotos que necesito según sea semirrígida, lancha, cabinado, flybridge o velero.',
  eyebrow='Vender barco · Fotos', h1='Cómo hacer las fotos de tu barco',
  lead='Las fotos son lo primero que ve un comprador. Con el móvil y unos 20 minutos se pueden hacer muy bien. Elige tu tipo de barco y mira las fotos que necesito.',
  choose='¿Qué barco tienes?',
  names={'semirrigida':'Semirrígida','lancha':'Lancha','cabinado':'Motor cabinado','fly':'Flybridge','velero':'Velero'},
  caps={'semirrigida':['Costado entero en 3/4','Popa con el motor','Desde popa hacia proa','Consola de cerca','Motor de lado','En el remolque (si lo tiene)'],
        'lancha':['Costado entero en 3/4','Popa de frente','Bañera desde popa','Puesto de mando','Solárium de proa','Cabina (si la tiene)'],
        'cabinado':['Costado entero en 3/4','Popa de frente','Bañera desde popa','Puesto de mando','Salón interior','Camarote'],
        'fly':['Costado entero en 3/4','Popa de frente','Flybridge','Mando del flybridge','Salón interior','Camarote principal'],
        'velero':['Costado entero, mástil incluido','Popa de frente','Bañera y timón','Cubierta de proa y jarcia','Salón y mesa de cartas','Camarote']},
  six='Las 6 fotos que necesito', pdf='Descargar esta guía en PDF',
  tips_h='Antes de hacer las fotos',
  tips=[('Barco limpio','Por fuera y por dentro.'),('Sin lona ni fundas','Que se vea el barco tal como es.'),('Sin objetos personales','Cubos, bolsas, toallas, cabos sueltos.'),('Día de sol','Con el sol a tu espalda, nunca de frente.')],
  how_h='Cómo hacerlas',
  how=[('Móvil en horizontal','Las fotos en vertical no sirven para el anuncio.'),('Sin zoom ni filtros','Para encuadrar, acércate o aléjate andando.'),('Barco entero','Sin cortar la proa ni la popa.')],
  send_h='Envíamelas por WhatsApp', send='Mejor que sobren a que falten: yo elijo las mejores y las edito para dejarlas listas para el anuncio.',
  wa_btn='Enviar fotos por WhatsApp', wa_text='Hola Juan, te mando las fotos de mi barco.',
  alt='Ejemplo de foto para el anuncio: {t}, {c}', also='También te puede interesar',
  rel=[('/herramientas/valora-tu-barco.html','¿Cuánto vale mi barco?'),('/guias/que-hace-un-broker-nautico.html','Qué hace un broker náutico'),('/papeles-fiscalidad/','Papeles e impuestos')],
  card_e='¿Hablamos?', card_h='¿Dudas con las fotos?', card_p='Escríbeme y te digo qué falta o cómo mejorarlas.', card_btn='Hablar con Juan por WhatsApp',
  updated='Actualizado en octubre de 2026', by='Por Juan Morante'),
'ca': dict(
  pre='/ca', title='Com fer les fotos del teu vaixell per vendre’l · guia per tipus',
  desc='Guia senzilla per fer amb el mòbil les fotos del teu vaixell per a l’anunci: com preparar-lo, la llum, l’enquadrament i les 6 fotos que necessito segons sigui semirígida, llanxa, cabinat, flybridge o veler.',
  eyebrow='Vendre vaixell · Fotos', h1='Com fer les fotos del teu vaixell',
  lead='Les fotos són el primer que veu un comprador. Amb el mòbil i uns 20 minuts es poden fer molt bé. Tria el teu tipus de vaixell i mira les fotos que necessito.',
  choose='Quin vaixell tens?',
  names={'semirrigida':'Semirígida','lancha':'Llanxa','cabinado':'Motor cabinat','fly':'Flybridge','velero':'Veler'},
  caps={'semirrigida':['Costat sencer en 3/4','Popa amb el motor','Des de popa cap a proa','Consola de prop','Motor de costat','Al remolc (si en té)'],
        'lancha':['Costat sencer en 3/4','Popa de cara','Banyera des de popa','Lloc de comandament','Solàrium de proa','Cabina (si en té)'],
        'cabinado':['Costat sencer en 3/4','Popa de cara','Banyera des de popa','Lloc de comandament','Saló interior','Cabina'],
        'fly':['Costat sencer en 3/4','Popa de cara','Flybridge','Comandament del flybridge','Saló interior','Cabina principal'],
        'velero':['Costat sencer, amb el pal','Popa de cara','Banyera i timó','Coberta de proa i eixàrcia','Saló i taula de cartes','Cabina']},
  six='Les 6 fotos que necessito', pdf='Descarregar la guia en PDF (castellà)',
  tips_h='Abans de fer les fotos',
  tips=[('Vaixell net','Per fora i per dins.'),('Sense lona ni fundes','Que es vegi el vaixell tal com és.'),('Sense objectes personals','Galledes, bosses, tovalloles, caps solts.'),('Dia de sol','Amb el sol a l’esquena, mai de cara.')],
  how_h='Com fer-les',
  how=[('Mòbil en horitzontal','Les fotos en vertical no serveixen per a l’anunci.'),('Sense zoom ni filtres','Per enquadrar, apropa’t o allunya’t caminant.'),('Vaixell sencer','Sense tallar la proa ni la popa.')],
  send_h='Envia-me-les per WhatsApp', send='Millor que en sobrin que no pas que en faltin: jo trio les millors i les edito perquè quedin a punt per a l’anunci.',
  wa_btn='Enviar fotos per WhatsApp', wa_text='Hola Juan, t’envio les fotos del meu vaixell.',
  alt='Exemple de foto per a l’anunci: {t}, {c}', also='També et pot interessar',
  rel=[('/herramientas/valora-tu-barco.html','Quant val el meu vaixell?'),('/guias/que-hace-un-broker-nautico.html','Què fa un bròquer nàutic'),('/papeles-fiscalidad/','Papers i impostos')],
  card_e='En parlem?', card_h='Dubtes amb les fotos?', card_p='Escriu-me i et dic què falta o com millorar-les.', card_btn='Parlar amb el Juan per WhatsApp',
  updated='Actualitzat a l’octubre de 2026', by='Per Juan Morante'),
'en': dict(
  pre='/en', title='How to photograph your boat to sell it · guide by boat type',
  desc='A simple guide to taking the photos of your boat for the listing with your phone: how to prepare it, light, framing and the 6 photos I need for a RIB, open boat, cabin cruiser, flybridge or sailboat.',
  eyebrow='Sell your boat · Photos', h1='How to photograph your boat',
  lead='Photos are the first thing a buyer sees. With your phone and about 20 minutes you can do a great job. Choose your type of boat and see the photos I need.',
  choose='What boat do you have?',
  names={'semirrigida':'RIB','lancha':'Open boat','cabinado':'Cabin cruiser','fly':'Flybridge','velero':'Sailboat'},
  caps={'semirrigida':['Full side view at 3/4','Stern with the engine','From stern to bow','Console close-up','Engine from the side','On the trailer (if any)'],
        'lancha':['Full side view at 3/4','Stern head-on','Cockpit from the stern','Helm station','Bow sunpad','Cabin (if any)'],
        'cabinado':['Full side view at 3/4','Stern head-on','Cockpit from the stern','Helm station','Saloon','Cabin'],
        'fly':['Full side view at 3/4','Stern head-on','Flybridge','Flybridge helm','Saloon','Master cabin'],
        'velero':['Full side view, mast included','Stern head-on','Cockpit and wheel','Foredeck and rigging','Saloon and chart table','Cabin']},
  six='The 6 photos I need', pdf='Download this guide as PDF (Spanish)',
  tips_h='Before taking the photos',
  tips=[('Clean boat','Inside and out.'),('No covers','Show the boat as it really is.'),('No personal items','Buckets, bags, towels, loose lines.'),('Sunny day','With the sun behind you, never facing it.')],
  how_h='How to take them',
  how=[('Phone in landscape','Portrait photos don’t work for the listing.'),('No zoom, no filters','To frame, walk closer or further away.'),('Whole boat','Don’t cut off the bow or the stern.')],
  send_h='Send them to me on WhatsApp', send='Better too many than too few: I pick the best ones and edit them so they are ready for the listing.',
  wa_btn='Send photos on WhatsApp', wa_text='Hi Juan, here are the photos of my boat.',
  alt='Example listing photo: {t}, {c}', also='You may also like',
  rel=[('/herramientas/valora-tu-barco.html','What is my boat worth?'),('/guias/que-hace-un-broker-nautico.html','What a yacht broker does'),('/papeles-fiscalidad/','Paperwork and taxes')],
  card_e='Let’s talk', card_h='Questions about the photos?', card_p='Message me and I’ll tell you what’s missing or how to improve them.', card_btn='Talk to Juan on WhatsApp',
  updated='Updated October 2026', by='By Juan Morante'),
}

ICONS = {
 'sparkle':'<path d="M10 30 Q24 36 38 30 L35 38 H13 Z"/><path d="M20 12 l2 5 5 2 -5 2 -2 5 -2 -5 -5 -2 5 -2z"/>',
 'cover':'<path d="M8 32 Q24 38 40 32 L37 40 H11 Z"/><path d="M12 26 Q24 14 36 26" stroke-dasharray="3 4"/><path d="M30 10 l6 6 M36 10 l-6 6"/>',
 'box':'<rect x="12" y="16" width="24" height="24" rx="3"/><path d="M18 16 v-4 h12 v4"/><path d="M8 8 L40 40"/>',
 'sun':'<circle cx="24" cy="24" r="7"/><path d="M24 6v5M24 37v5M6 24h5M37 24h5M11 11l3.5 3.5M33.5 33.5L37 37M11 37l3.5-3.5M33.5 14.5L37 11"/>',
 'phone':'<rect x="6" y="14" width="36" height="20" rx="4"/><circle cx="37" cy="24" r="1.5"/>',
 'zoom':'<circle cx="21" cy="21" r="11"/><path d="M29 29l10 10M16 21h10"/><path d="M8 8L40 40"/>',
 'frame':'<path d="M6 30 Q24 36 42 30 L38 38 H10 Z"/><path d="M4 12v-6h6M44 12v-6h-6M4 36v6h6M44 36v6h-6"/>',
}
def icon(k):
    return f'<svg viewBox="0 0 48 48" width="40" height="40" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[k]}</svg>'

CSS = '''<style>
.gf-types{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 18px}
.gf-types button{font:inherit;font-family:var(--display);font-weight:600;font-size:15px;padding:10px 16px;border-radius:999px;border:1.5px solid var(--sea);background:#fff;color:var(--sea);cursor:pointer}
.gf-types button[aria-selected="true"]{background:var(--sea-deep);border-color:var(--sea-deep);color:#fff}
.gf-panel[hidden]{display:none}
.gf-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin:0 0 12px;padding:0;list-style:none}
.gf-grid li{margin:0;padding:0}.gf-grid li::before{content:none}
.gf-grid img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:8px;display:block}
.gf-grid span{display:flex;gap:8px;align-items:center;font-family:var(--display);font-weight:600;font-size:14px;margin-top:6px}
.gf-grid b{display:inline-flex;width:22px;height:22px;border-radius:50%;background:var(--sea-deep);color:#fff;font-size:12px;align-items:center;justify-content:center;flex:none}
.gf-chips{display:grid;grid-template-columns:repeat(auto-fit,minmax(125px,1fr));gap:10px;margin:0 0 8px}
.gf-chip{background:#F3F5F6;border-radius:8px;padding:14px 12px;text-align:center;color:var(--sea-deep)}
.gf-chip svg{display:block;margin:0 auto 6px}.gf-chip strong{display:block;font-family:var(--display);font-size:15px}
.gf-chip small{display:block;color:var(--ink-2);font-size:13px;margin-top:3px}
.gf-pdf{display:inline-block;font-size:14px;margin:0 0 6px}
.cta2{background:var(--sea-deep);color:#D5DDE2;padding:20px 22px;border-radius:6px;margin:18px 0 22px}
.cta2 h3{color:#fff;font-family:var(--display);font-size:1.05rem;margin:0 0 6px}.cta2 p{margin:0 0 12px}
</style>'''

JS = '''<script>
(function(){var b=document.querySelectorAll('.gf-types button'),p=document.querySelectorAll('.gf-panel');
function show(id,push){var ok=false;for(var i=0;i<b.length;i++){var on=b[i].getAttribute('data-t')===id;b[i].setAttribute('aria-selected',on);if(on)ok=true;}
for(var j=0;j<p.length;j++)p[j].hidden=p[j].id!=='t-'+id;if(push&&history.replaceState)history.replaceState(null,'','#'+id);return ok;}
for(var i=0;i<b.length;i++)b[i].addEventListener('click',function(){show(this.getAttribute('data-t'),true);});
var h=(location.hash||'').slice(1);if(!h||!show(h,false))show('lancha',false);})();
</script>'''

def build(lang):
    L = T[lang]; pre = L['pre']
    tpl = open(os.path.join(ROOT, pre.strip('/'), TPL) if pre else os.path.join(ROOT, TPL)).read()
    url = f'{BASE}{pre}/{SLUG}'
    head, rest = tpl.split('<main', 1)
    foot = rest[rest.index('</main>')+len('</main>'):]
    old = f'{BASE}{pre}/{TPL}'
    head = head.replace('broker-nautico-barcelona-maresme.html', 'guia-fotos-barco.html')
    head = re.sub(r'<title>.*?</title>', f'<title>{L["title"]}</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1)+L['desc'], head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1)+L['title'], head)
    head = re.sub(r'<style>.*?</style>\s*', '', head, flags=re.S)
    ld = {"@context":"https://schema.org","@type":"WebPage","name":L['title'],"inLanguage":lang,"url":url,"description":L['desc'],"publisher":{"@type":"Organization","name":"Plata Marine"}}
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">\n'+json.dumps(ld, ensure_ascii=False)+'\n</script>', head, flags=re.S)
    head = head.replace('<link rel="stylesheet" href="/nav.css', CSS+'\n<link rel="stylesheet" href="/nav.css', 1)
    wa = 'https://wa.me/34633742973?text=' + __import__('urllib.parse').parse.quote(L['wa_text'])
    head = re.sub(r'(<a class="btn btn-wa" href=")https://wa\.me/[^"]*(" target="_blank" rel="noopener">)', lambda m: m.group(1)+wa+m.group(2), head, count=1)
    btns = ''.join(f'<button type="button" role="tab" data-t="{t}" aria-selected="false">{L["names"][t]}</button>' for t in TYPES)
    panels = ''
    for t in TYPES:
        items = ''.join(f'<li><img src="/vender/fotos-guia/{t}-{i}.jpg" width="1000" height="750" loading="lazy" alt="{L["alt"].format(t=L["names"][t].lower(), c=c.lower())}"><span><b>{i}</b>{c}</span></li>' for i, c in enumerate(L['caps'][t], 1))
        pdf = f'<a class="gf-pdf" href="/vender/fotos-guia/guia-fotos-{t}.pdf" target="_blank" rel="noopener">{L["pdf"]} ↓</a>'
        panels += f'<section class="gf-panel" id="t-{t}" role="tabpanel" hidden><h2>{L["six"]} · {L["names"][t]}</h2><ul class="gf-grid">{items}</ul>{pdf}</section>'
    chip = lambda ic, a, b: f'<div class="gf-chip">{icon(ic)}<strong>{a}</strong><small>{b}</small></div>'
    tips = ''.join(chip(ic, a, b) for ic, (a, b) in zip(['sparkle','cover','box','sun'], L['tips']))
    how = ''.join(chip(ic, a, b) for ic, (a, b) in zip(['phone','zoom','frame'], L['how']))
    rel = ''.join(f'<a href="{pre}{h}">{t}</a>' for h, t in L['rel'])
    main = f'''<main class="art">
  <div class="wrap">
    <article>
      <header>
        <p class="eyebrow">{L['eyebrow']}</p>
        <h1>{L['h1']}</h1>
        <div class="meta"><span>{L['by']}</span><span>{L['updated']}</span></div>
        <p class="lead">{L['lead']}</p>
      </header>
      <div class="prose">
        <h2 id="tipo">{L['choose']}</h2>
        <div class="gf-types" role="tablist">{btns}</div>
        {panels}
        <h2 id="antes">{L['tips_h']}</h2>
        <div class="gf-chips">{tips}</div>
        <h2 id="como">{L['how_h']}</h2>
        <div class="gf-chips">{how}</div>
        <div class="cta2"><h3>{L['send_h']}</h3><p>{L['send']}</p><a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{L['wa_btn']}</a></div>
      </div>
    </article>
    <aside class="aside">
      <div class="card">
        <p class="eyebrow">{L['card_e']}</p>
        <h3>{L['card_h']}</h3>
        <p>{L['card_p']}</p>
        <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{L['card_btn']}</a>
      </div>
      <div class="rel"><p class="eyebrow">{L['also']}</p>{rel}</div>
    </aside>
  </div>
</main>'''
    out = head + main + foot.replace('</body>', JS + '\n</body>', 1)
    path = os.path.join(ROOT, pre.strip('/'), SLUG) if pre else os.path.join(ROOT, SLUG)
    open(path, 'w').write(out)
    print('ok', path)

for l in ('es', 'ca', 'en'):
    build(l)
