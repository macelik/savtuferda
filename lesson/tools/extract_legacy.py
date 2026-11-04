#!/usr/bin/env python3
"""Import content from the legacy long-scroll lesson HTML into the JSON shape.
Usage: python3 -I lesson/tools/extract_legacy.py <old.html> <out.json>  (needs beautifulsoup4)
Afterwards add meta + per-card gist/mg by hand (see docs/lesson-page-instructions.md)."""
import json,sys,re
from bs4 import BeautifulSoup
src=sys.argv[1]
s=BeautifulSoup(open(src,encoding='utf-8').read(),'html.parser')
def T(e): return re.sub(r'\s+',' ',e.get_text(' ',strip=True)) if e else ''
def H(e): return re.sub(r'\s+',' ',e.decode_contents()).strip() if e else ''
def pairs(block):
  out=[];ps=block.find_all('p',recursive=False);i=0
  while i<len(ps):
    p=ps[i]
    if 'ar' in (p.get('class') or []):
      tr=''
      if i+1<len(ps) and 'tr-trans' in (ps[i+1].get('class') or []): tr=H(ps[i+1]); i+=1
      out.append({'ar':H(p),'tr':tr})
    i+=1
  return out
cards=[]
for a in s.select('article.card'):
  c={'id':a['id'],'num':T(a.select_one('.num')),'accent':re.search(r'--accent:([^;]+)',a.get('style','')).group(1),
     'word':T(a.select_one('h3.word')),'translit':H(a.select_one('.translit')),
     'levels':[T(x) for x in a.select('.card-head .levels .lvl, .shart-head .levels .lvl')],
     'verse':H(a.select_one('.verse')),'verseTr':T(a.select_one('.verse-tr'))}
  sb=a.select('.sarf-block .sarf')
  c['sarf']=[[T(d.select_one('.ar')) for d in x.find_all('div',recursive=False)] for x in sb]
  c['sarfNote']=H(a.select_one('.sarf-note'))
  mb=a.select('.meaning-block')
  c['def']=H(mb[0].select_one('.def')) if mb else ''
  c['defTr']=H(mb[0].select_one('.tr-trans')) if mb else ''
  hb=a.select_one('.harf-block')
  if hb: c['harf']={'chips':[T(x) for x in hb.select('.chip')],'ex':pairs(hb)}
  c['syn']=[]
  for r in a.select('.sa-row'):
    c['syn'].append({'k':'syn' if r.select_one('.tag-syn') else 'ant','ar':T(r.select_one('.ar'))})
  nb=a.select_one('.note-block')
  if nb: c['noteH']=T(nb.find('h4').contents[0]); c['note']=H(nb.select_one('.note'))
  c['meanings']=[]
  for li in a.select('ol.meanings > li'):
    m={'t':H(li.select_one('.meaning')),'ex':[]}
    m['t']=re.sub(r'<span class="mnum">\d+</span>\s*','',m['t'])
    for e in li.select('ul.examples > li'):
      m['ex'].append({'lvl':T(e.select_one('.lvl')),'ar':H(e.select_one('p.ar')),'tr':H(e.select_one('.tr-trans'))})
    c['meanings'].append(m)
  c['extras']=[]
  for e in a.select('.extra-use'):
    c['extras'].append({'tag':T(e.select_one('.tag')),'ar':H(e.select_one('p.ar')),'tr':H(e.select_one('.tr-trans')),'src':T(e.select_one('.src'))})
  c['qs']=[{'lvl':T(q.select_one('.lvl')),'ar':H(q.select_one('p.ar'))} for q in a.select('.questions-block .q')]
  if len(mb)>1: c['commonAr']=pairs(mb[1])
  rw=a.select_one('.root-wrap')
  if rw:
    c['rootGrid']=[{'ar':T(d.select_one('.ar')),'tr':T(d.find_all('p')[1])} for d in rw.select('.root-grid > div')]
    cb=rw.select_one('.common-box'); ps=cb.find_all('p')
    c['commonBoxAr']=T(ps[0]); c['commonBoxTr']=H(ps[1])
  c['ayat']=[{'ar':H(x.select_one('p.ar')),'tr':H(x.select_one('.tr-trans')),'src':T(x.select_one('.src'))} for x in a.select('.ayetler-block .ayah')]
  cards.append(c)
rows=[[T(td) for td in tr.find_all('td')] for tr in s.select('.tr-table tbody tr')]
poem=[H(p) for p in s.select('.poem-body p')]
out=sys.argv[2] if len(sys.argv)>2 else 'data.json'
json.dump({'meta':{},'cards':cards,'rows':rows,'poem':poem},open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(cards),len(rows),len(poem))
for c in cards: print(c['num'],c['word'],len(c['sarf']),len(c['meanings']),len(c['extras']),len(c['qs']),'harf' in c,'note' in c)
