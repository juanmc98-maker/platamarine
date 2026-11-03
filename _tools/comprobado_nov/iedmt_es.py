# -*- coding: utf-8 -*-
"""Guía impuesto de matriculación (ES): correcciones del 3 nov 2026 + fecha y fuentes."""
import re
f='guias/impuesto-matriculacion-barcos.html'
h=open(f,encoding='utf-8').read()
R=[
 ('No es casualidad: a partir de 8 metros de eslora, la primera matriculación en España paga un 12 % de impuesto.',
  'No es casualidad: por encima de 8 metros de eslora, la primera matriculación en España paga un 12 % de impuesto.'),
 ('Las motos de agua lo pagan siempre, tengan la eslora que tengan.</p>',
  'Las motos de agua lo pagan siempre, tengan la eslora que tengan, y a un tipo distinto: el 14,75 %.</p>'),
 ('la base es el valor de mercado, y Hacienda lo calcula con sus tablas oficiales de valoración de embarcaciones (una orden que se publica cada año) o con el precio real si es superior.</p>',
  'la base es el valor de mercado; puedes usar las tablas oficiales de valoración de embarcaciones (una orden que se publica cada año) y Hacienda puede comprobar ese valor.</p>'),
 ('y si el precio real es mayor que la tabla, manda el precio real.',
  'y Hacienda puede comprobar el valor que declares.'),
 ('<td>Barco de más de 8 m comprado en otro país de la UE</td><td>Sí, 12 % sobre valor de tablas</td>',
  '<td>Barco de más de 8 m comprado en otro país de la UE</td><td>Sí, 12 %: si es usado, sobre su valor de mercado (tablas); si es nuevo, sobre el precio sin IVA</td>'),
 ('solo se presenta una declaración de exención (modelo 06).','solo se presenta una declaración de no sujeción (modelo 06).'),
 ('<p>No pagan, pero la exención no es automática: hay que presentar el modelo 06','<p>No pagan, pero no es automático: hay que presentar la declaración de no sujeción (modelo 06)'),
 ('sobre el valor que tenga el barco entonces.','sobre el valor que tenga el barco entonces, con el modelo 576 y en un plazo de 15 días naturales desde el cambio. La exención también se pierde si el barco se cede más de 3 meses en un año a la misma persona, o si el dueño o alguien vinculado a él se reserva su uso.'),
 ('La eslora que cuenta es la que figura en la documentación del barco (la eslora de casco de la declaración de conformidad CE), no la eslora total con plataforma de baño o púlpitos.',
  'La eslora que cuenta es la que figura en la documentación del barco, no la eslora total con plataforma de baño o púlpitos; si tienes dudas, que la gestoría la confirme con el certificado del barco.'),
 ('<span>Actualizado septiembre 2026</span>','<span>Comprobado el 3 de noviembre de 2026</span>'),
 ('Información fiscal orientativa, revisada en septiembre de 2026 según','Información fiscal orientativa, comprobada el 3 de noviembre de 2026 según'),
]
for a,b in R:
    c=h.count(a); assert c==1,(a[:60],c); h=h.replace(a,b)
h=re.sub(r'"dateModified":\s*"[0-9-]+"','"dateModified": "2026-11-03"',h)
FU=('<div class="fuentes" style="font-size:.82em;opacity:.9;margin:14px 0 0"><p style="margin:0 0 6px"><strong>Fuentes oficiales</strong> (comprobadas el 3 de noviembre de 2026):</p><ul style="margin:0;padding-left:18px">'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-1992-28741" target="_blank" rel="noopener">BOE: Ley 38/1992 de Impuestos Especiales (arts. 65 a 70)</a></li>'
 '<li><a href="https://www3.agenciatributaria.gob.es/static_files/Sede/Procedimiento_ayuda/G502/instr_mod576.pdf" target="_blank" rel="noopener">Agencia Tributaria: instrucciones del modelo 576 (tipos y base)</a></li>'
 '<li><a href="https://sede.agenciatributaria.gob.es/Sede/vehiculos-embarcaciones/primera-matriculacion-medios-transporte/que-supuestos-puedo-estar-exento-transporte.html" target="_blank" rel="noopener">Agencia Tributaria: exenciones (alquiler, modelo 05)</a></li>'
 '<li><a href="https://www.boe.es/buscar/act.php?id=BOE-A-2025-26357" target="_blank" rel="noopener">BOE: Orden HAC/1501/2025, precios medios de embarcaciones 2026</a></li>'
 '</ul></div>')
a='Confírmalo con tu gestoría o con la Administración antes de comprar.</p>'
assert h.count(a)==1
if 'class="fuentes"' not in h: h=h.replace(a,a+'\n    '+FU)
open(f,'w',encoding='utf-8').write(h); print('ok',f)
