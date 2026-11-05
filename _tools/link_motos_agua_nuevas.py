#!/usr/bin/env python3
"""Añade el bloque de motos de agua nuevas tras Goliath en /barcos-nuevos/ ×4 y las URLs al sitemap (idempotente)."""
import os
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TX={'':('Sea-Doo y Kawasaki, gama 2027','Motos de agua nuevas','Toda la gama de motos de agua Sea-Doo y Kawasaki, de la Spark a la Ultra. Me dices cuál te interesa y te paso el precio por escrito.','Precio a consultar','Ver motos de agua nuevas'),
 'ca':('Sea-Doo i Kawasaki, gamma 2027',"Motos d'aigua noves","Tota la gamma de motos d'aigua Sea-Doo i Kawasaki, de la Spark a la Ultra. Em dius quina t'interessa i et passo el preu per escrit.",'Preu a consultar',"Veure motos d'aigua noves"),
 'en':('Sea-Doo and Kawasaki, 2027 range','New jet skis',"The full Sea-Doo and Kawasaki jet ski range, from the Spark to the Ultra. Tell me which one you like and I'll send you the price in writing.",'Price on request','See new jet skis'),
 'fr':('Sea-Doo et Kawasaki, gamme 2027','Jet-skis neufs',"Toute la gamme de jet-skis Sea-Doo et Kawasaki, du Spark à l'Ultra. Dites-moi lequel vous intéresse et je vous envoie le prix par écrit.",'Prix sur demande','Voir les jet-skis neufs')}
for l,(k,h,d,pr,b) in TX.items():
    p=('/'+l) if l else ''
    f=os.path.join(R,l,'barcos-nuevos','index.html'); s=open(f,encoding='utf-8').read()
    if 'id="marca-motos-agua"' in s: continue
    i=s.index('id="marca-goliath"'); e=s.index('</section>',i)+10
    blk=f'''
    <section class="nv-brand" id="marca-motos-agua" aria-labelledby="nv-motos"><style>#marca-motos-agua .nv-ph{{background:#fff}}#marca-motos-agua .nv-ph::after{{display:none}}#marca-motos-agua .nv-ph img.ph{{object-fit:contain;max-height:380px}}#marca-motos-agua .mj-l{{display:flex;gap:16px;align-items:center;margin:0 0 8px}}#marca-motos-agua .mj-l img{{height:22px;width:auto}}#marca-motos-agua .mj-l img+img{{height:30px}}</style>
      <a class="nv-ph" href="{p}/motos-de-agua-nuevas/" tabindex="-1" aria-hidden="true"><img class="ph" loading="lazy" src="/motos-de-agua-nuevas/fotos/sd-gtx-limited.jpg" alt="Sea-Doo GTX Limited 350" width="900" height="636" decoding="async" style="object-fit:contain;background:#fff"></a>
      <div class="nv-body">
        <div class="mj-l"><img src="/barcos-nuevos/logos/sea-doo.png" alt="Sea-Doo" width="900" height="97" data-nolb><img src="/barcos-nuevos/logos/kawasaki.png" alt="Kawasaki" width="319" height="88" data-nolb></div>
        <p class="nv-kick">{k}</p>
        <h2 id="nv-motos">{h}</h2>
        <p class="d">{d}</p>
        <p class="nv-pr">{pr}</p>
        <div class="nv-cta"><a class="btn btn-pri" href="{p}/motos-de-agua-nuevas/">{b}</a></div>
      </div>
    </section>'''
    open(f,'w',encoding='utf-8').write(s[:e]+blk+s[e:])
sm=os.path.join(R,'sitemap.xml'); s=open(sm,encoding='utf-8').read()
if 'motos-de-agua-nuevas' not in s:
    add=''.join(f'    <url><loc>https://www.platamarine.com{("/"+l) if l else ""}/motos-de-agua-nuevas/</loc><lastmod>2026-11-05</lastmod><priority>0.6</priority></url>\n' for l in TX)
    s=s.replace('</urlset>',add+'</urlset>'); open(sm,'w',encoding='utf-8').write(s)
print('ok')
