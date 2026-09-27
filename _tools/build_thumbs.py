"""Genera versiones ligeras de las fotos de barcos: <nombre>-t.jpg (480 px, miniaturas)
y <nombre>-m.jpg (1000 px, tarjetas y móvil). Ejecutar tras añadir o cambiar fotos:
python3 _tools/build_thumbs.py   (solo rehace las que falten o estén desfasadas)"""
import glob, os, re, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for f in sorted(glob.glob(os.path.join(ROOT, '*.jpg'))):
    b = os.path.basename(f)
    if not re.fullmatch(r'[a-z0-9-]+-\d+\.jpg', b):
        continue
    im = None
    for suf, w, q in (('-t', 480, 76), ('-m', 1000, 80)):
        out = f[:-4] + suf + '.jpg'
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(f) and '--force' not in sys.argv:
            continue
        im = im or Image.open(f).convert('RGB')
        r = im.copy(); r.thumbnail((w, 10000), Image.LANCZOS)
        r.save(out, 'JPEG', quality=q, optimize=True, progressive=True)
        print(os.path.basename(out), os.path.getsize(out) // 1024, 'KB')
