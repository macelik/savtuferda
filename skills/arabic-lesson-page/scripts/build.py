#!/usr/bin/env python3
"""Build a lesson page: python3 <skill>/scripts/build.py lessons/<slug>/<slug>.json lessons/<slug>/<Name>-Ders.html"""
import json, sys, html, pathlib, re

MG_KEYS = {'point','aim','rise','deflate','slope','thought','diverge','dim','flame','eye',
           'radiate','grow','shart','birds','shout','break','embrace','vanish'}  # keep in sync with MG in assets/template.html
REQUIRED_CARD = ['word','translit','levels','verse','verseTr','sarf','sarfNote','def','defTr',
                 'syn','meanings','extras','qs','gist','mg']

UNSAFE = re.compile(r'<\s*(script|foreignObject|image|iframe|object|embed)|\son\w+\s*=|javascript:|(href|src)\s*=\s*["\']?\s*(https?:|//)|url\(\s*["\']?\s*(https?:|//)', re.I)
HARAKA = re.compile('[\u064B-\u0652]')
ROOT = re.compile(r'Kök:</b>\s*\S+-\S+|<b>[^<\s]+-[^<\s]+</b>')

def strip_tags(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h)).strip()

def bare(h):
    # same normalisation as the page uses to link text marks to cards
    return re.sub('[أإآ]', 'ا', re.sub('[\u064B-\u065F\u0670\u0640]', '', strip_tags(h)))

def find_todo(x, path='$'):
    if isinstance(x, str):
        if 'TODO' in x: yield path, x
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from find_todo(v, f'{path}[{i}]')
    elif isinstance(x, dict):
        for k, v in x.items(): yield from find_todo(v, f'{path}.{k}')

def main(src, dst):
    here = pathlib.Path(__file__).parent
    d = json.load(open(src, encoding='utf-8'))
    m, cards = d['meta'], d['cards']
    errs, warns = [], []
    poem_marks = {bare(x) for u in d['poem'] for x in re.findall(r'<mark>(.*?)</mark>', u)}
    if len(d['poem']) != len(d['rows']):
        errs.append(f"poem has {len(d['poem'])} units but rows has {len(d['rows'])}")
    for i, c in enumerate(cards, 1):
        for k in REQUIRED_CARD:
            if k not in c: errs.append(f'card {i}: missing "{k}"')
        if c.get('mg') == 'custom':
            svg = c.get('mgSvg', '')
            if not svg.strip(): errs.append(f'card {i}: mg "custom" needs "mgSvg" (inner SVG markup, viewBox 0 0 240 180)')
            if UNSAFE.search(svg): errs.append(f'card {i}: mgSvg may not contain <script>, <foreignObject>, <image>, event handlers, external URLs or javascript:')
            if len(svg) > 6000: errs.append(f'card {i}: mgSvg is {len(svg)} chars; keep custom animations simple (< 6000)')
        elif c.get('mg') not in MG_KEYS: errs.append(f'card {i}: unknown mg "{c.get("mg")}" (allowed: {", ".join(sorted(MG_KEYS))})')
        v = c.get('verse', '')
        if v.count('<mark>') != 1: errs.append(f'card {i}: verse must contain exactly one <mark>')
        elif bare(re.search(r'<mark>(.*?)</mark>', v).group(1)) not in poem_marks:
            errs.append(f'card {i}: the <mark> in "verse" is not one of the <mark>s in "poem" (they must be the same text)')
        if not HARAKA.search(c.get('word', '')): errs.append(f'card {i}: word has no harakat')
        for row in c.get('sarf', []):
            if len(row) != 3: errs.append(f'card {i}: each sarf row needs [mazi, muzari, masdar]')
        if not ROOT.search(c.get('sarfNote', '')): errs.append(f'card {i}: sarfNote must contain "<b>Kök:</b> x-y-z" (or <b>x-y-z</b>)')
        if not set(c.get('levels', [])) <= {'A2', 'B1', 'B2'} or not c.get('levels'):
            errs.append(f'card {i}: levels must be a non-empty subset of A2, B1, B2')
    css = m.get('css', '')
    if UNSAFE.search(css) or '</style' in css.lower() or '@import' in css.lower():
        errs.append('meta.css may only hold plain CSS (no </style>, @import, url(http…), script)')
    todo = sorted({p for p, _ in find_todo(d)})
    if todo:
        errs.append('unfilled TODO at: ' + ', '.join(todo[:25]) + (' …' if len(todo) > 25 else ''))
    for w in warns: print('warning:', w)
    if errs:
        sys.exit('Data errors:\n  ' + '\n  '.join(errs))
    t = (here.parent / 'assets' / 'template.html').read_text(encoding='utf-8')
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
