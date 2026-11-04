#!/usr/bin/env python3
"""Build a lesson page: python3 lesson/build.py lesson/data/<name>.json lesson/output/<Name>-Ders.html"""
import json, sys, html, pathlib

MG_KEYS = {'point','aim','rise','deflate','slope','thought','diverge','dim','flame','eye',
           'radiate','grow','shart','birds','shout'}  # keep in sync with MG in src/template.html
REQUIRED_CARD = ['word','translit','levels','verse','verseTr','sarf','sarfNote','def','defTr',
                 'syn','meanings','extras','qs','gist','mg']

def main(src, dst):
    here = pathlib.Path(__file__).parent
    d = json.load(open(src, encoding='utf-8'))
    m, cards = d['meta'], d['cards']
    errs = []
    if len(d['poem']) != len(d['rows']):
        errs.append(f"poem has {len(d['poem'])} units but rows has {len(d['rows'])}")
    for i, c in enumerate(cards, 1):
        for k in REQUIRED_CARD:
            if k not in c: errs.append(f'card {i}: missing "{k}"')
        if c.get('mg') not in MG_KEYS: errs.append(f'card {i}: unknown mg "{c.get("mg")}"')
        if '<mark>' not in c.get('verse', ''): errs.append(f'card {i}: verse has no <mark>')
    if errs:
        sys.exit('Data errors:\n  ' + '\n  '.join(errs))
    t = (here / 'src' / 'template.html').read_text(encoding='utf-8')
    rep = {
        '__TITLE__': html.escape(m['title']),
        '__BRAND_AR__': m['brandAr'], '__BRAND_TR__': m['brandTr'],
        '__TEXT_TAB__': m.get('textTab', 'Metin'), '__TEXT_HEADING__': m.get('textHeading', 'Önce metni okuyalım'),
        '__N__': str(len(cards)),
        '__SOURCES__': ''.join(f'<li>{s}</li>' for s in m.get('sources', [])),
        '__NOTES__': ''.join(f'<p>{s}</p>' for s in m.get('notes', [])),
        '__DATA__': json.dumps(d, ensure_ascii=False).replace('</', '<\\/'),
    }
    for k, v in rep.items():
        t = t.replace(k, v)
    pathlib.Path(dst).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(dst).write_text(t, encoding='utf-8')
    print(f'wrote {dst} ({len(cards)} cards)')

if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
