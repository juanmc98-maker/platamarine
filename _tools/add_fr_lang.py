"""Añade el francés (/fr/) al selector de idioma y a los hreflang de todas las páginas. Idempotente."""
import re,pathlib,os
B='https://www.platamarine.com'
root=pathlib.Path('.')
def rel_of(p):
    s=str(p)
    for L in ('ca/','en/','fr/'):
        if s.startswith(L): return L[:2],s[3:]
    return 'es',s
n=0
for p in root.rglob('*.html'):
    if '.git' in p.parts or p.parts[0]=='_tools': continue
    lang,rel=rel_of(p)
    s=p.read_text(encoding='utf-8'); o=s
    # hreflang fr
    m=re.search(r'<link rel="alternate" hreflang="en" href="'+re.escape(B)+r'/en/([^"]*)">',s)
    if m and 'hreflang="fr"' not in s:
        target=m.group(1)
        if (root/'fr'/(target or 'index.html')).exists() or (root/'fr'/target/'index.html').exists():
            s=s.replace(m.group(0),m.group(0)+'\n<link rel="alternate" hreflang="fr" href="'+B+'/fr/'+target+'">')
    # langsw
    def fix(mm):
        blk=mm.group(0)
        if 'flag-fr' in blk: return blk
        a=re.search(r'<a href="([^"]*)"([^>]*)><span class="flag flag-en" aria-hidden="true"></span><span class="sr-only">EN</span></a>',blk)
        if not a: return blk
        href=a.group(1)
        if lang=='fr':
            frhref=href
            enhref=href.replace(B+'/fr/',B+'/en/')
            new='<a href="'+enhref+'"><span class="flag flag-en" aria-hidden="true"></span><span class="sr-only">EN</span></a><a href="'+frhref+'" aria-current="page"><span class="flag flag-fr" aria-hidden="true"></span><span class="sr-only">FR</span></a>'
        else:
            frhref=href.replace(B+'/en/',B+'/fr/')
            new=a.group(0)+'<a href="'+frhref+'"><span class="flag flag-fr" aria-hidden="true"></span><span class="sr-only">FR</span></a>'
        return blk.replace(a.group(0),new)
    s=re.sub(r'<div class="langsw".*?</div>',fix,s,flags=re.S)
    if s!=o: p.write_text(s,encoding='utf-8'); n+=1
print('cambiados',n)
