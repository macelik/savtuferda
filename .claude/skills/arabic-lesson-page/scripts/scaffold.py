#!/usr/bin/env python3
"""Turn a lesson request into a JSON skeleton for lesson/build.py.

Usage:
    python3 scaffold.py <request.md | draft.html> <out.json>

Input A: a request in the format of templates/lesson-request.md
         (front matter, "## Metin" with [[marked]] targets, optional "## Çeviri", "## Notlar").
Input B: a teacher's HTML draft in which target words are wrapped in <mark>
         (needs beautifulsoup4). Units = <p> elements of .poem-body if present,
         otherwise every <p>/<li>/<blockquote> that contains a <mark>.

The skeleton has every mechanical field filled (text units, rows, verse with exactly
one <mark>, card order) and every content field set to a "TODO: ..." string.
lesson/build.py refuses to build while any "TODO" remains.
"""
import json, re, sys, pathlib

DEFAULT_SOURCES = [
    '<span lang="ar">المعجم الوسيط — مجمع اللغة العربية بالقاهرة</span>',
    '<span lang="ar">معجم اللغة العربية المعاصرة — د. أحمد مختار عمر</span>',
    '<span lang="ar">لسان العرب — ابن منظور</span>',
    '<span lang="ar">معجم الغني — عبد الغني أبو العزم</span>',
]
TAB = {'poem': ('Şiir', 'Önce şiiri dinleyelim'), 'prose': ('Metin', 'Önce metni okuyalım'),
       'dialogue': ('Diyalog', 'Önce sahneyi izleyelim'), 'song': ('Şarkı', 'Önce şarkıyı dinleyelim')}


def parse_request(text):
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    meta = {}
    m = re.match(r'\s*---\n(.*?)\n---\n', text, flags=re.S)
    if m:
        for line in m.group(1).splitlines():
            line = re.sub(r'\s+#.*$', '', line).strip()
            if not line or line.startswith('#') or ':' not in line:
                continue
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()
        text = text[m.end():]
    sections, cur = {}, None
    for line in text.splitlines():
        h = re.match(r'##\s+(.+)', line)
        if h:
            cur = h.group(1).strip().lower(); sections[cur] = []; continue
        if cur is not None and line.strip():
            sections[cur].append(line.strip())
    units = sections.get('metin', [])
    trs = sections.get('çeviri', sections.get('ceviri', []))
    notes = sections.get('notlar', [])
    marked = [re.sub(r'\[\[(.+?)\]\]', r'<mark>\1</mark>', u) for u in units]
    return meta, marked, trs, notes


def parse_html(text):
    from bs4 import BeautifulSoup
    s = BeautifulSoup(text, 'html.parser')
    meta = {'title': s.title.get_text(strip=True) if s.title else ''}
    body = s.select('.poem-body p')
    if not body:
        body = [e for e in s.find_all(['p', 'li', 'blockquote']) if e.find('mark')
                and not e.find_parent(['p', 'li', 'blockquote'])]
    units = []
    for e in body:
        for x in e.find_all(True):
            if x.name != 'mark':
                x.unwrap()
        units.append(re.sub(r'\s+', ' ', e.decode_contents()).strip())
    return meta, units, [], []


def card_for(unit, mark_text, idx_in_unit):
    # verse = the unit with only this occurrence marked
    n = -1
    def keep(m):
        nonlocal n
        n += 1
        return f'<mark>{m.group(1)}</mark>' if n == idx_in_unit else m.group(1)
    verse = re.sub(r'<mark>(.*?)</mark>', keep, unit)
    return {
        "word": mark_text,
        "translit": "TODO: transliteration <span class=\"sep\">·</span> TODO: grammar label in Turkish",
        "levels": ["A2", "B1"],
        "gist": "TODO: 1-3 Turkish words",
        "mg": "TODO: motion graphic key",
        "verse": verse,
        "verseTr": "TODO: Turkish translation of this unit, in “quotes”",
        "sarf": [["TODO: mazi", "TODO: muzari", "TODO: masdar"]],
        "sarfNote": "<b>Kök:</b> TODO: x-y-z · TODO: short Turkish note",
        "def": "TODO: simple Arabic definition (A2-B1)",
        "defTr": "Türkçe: “TODO”",
        "syn": [{"k": "syn", "ar": "TODO"}, {"k": "ant", "ar": "TODO"}],
        "noteH": "Kullanım notu",
        "note": "TODO: one short usage note in Turkish",
        "harf": {"chips": ["TODO"], "ex": [{"ar": "TODO", "tr": "TODO"}]},
        "meanings": [
            {"t": "TODO: meaning 1 in Arabic (Turkish gloss)", "ex": [
                {"lvl": "A2", "ar": "TODO", "tr": "TODO"}, {"lvl": "B1", "ar": "TODO", "tr": "TODO"}]},
            {"t": "TODO: meaning 2", "ex": [
                {"lvl": "B1", "ar": "TODO", "tr": "TODO"}, {"lvl": "B2", "ar": "TODO", "tr": "TODO"}]}],
        "extras": [{"tag": "mecaz", "ar": "TODO", "tr": "TODO", "src": ""},
                   {"tag": "basın", "ar": "TODO", "tr": "TODO", "src": ""}],
        "qs": [{"lvl": "A2", "ar": "TODO"}, {"lvl": "B1", "ar": "TODO"}],
    }


def main(src, dst):
    text = pathlib.Path(src).read_text(encoding='utf-8')
    if src.lower().endswith(('.html', '.htm')):
        meta, units, trs, notes = parse_html(text)
    else:
        meta, units, trs, notes = parse_request(text)
    if not units:
        sys.exit('No text units found. Request: put lines under "## Metin". HTML: wrap targets in <mark>.')
    stype = meta.get('source_type', 'poem')
    tab, heading = TAB.get(stype, TAB['prose'])
    plain = [re.sub(r'</?mark>', '', u) for u in units]
    rows = [[str(i + 1), plain[i], trs[i] if i < len(trs) else 'TODO: Turkish translation']
            for i in range(len(units))]
    cards = []
    for u in units:
        for j, m in enumerate(re.findall(r'<mark>(.*?)</mark>', u)):
            cards.append(card_for(u, m, j))
    out = {
        "meta": {
            "title": meta.get('title') or 'TODO: short page name',
            "brandAr": meta.get('brand_ar') or 'TODO',
            "brandTr": meta.get('brand_tr') or 'TODO',
            "textTab": tab, "textHeading": heading,
            "sources": DEFAULT_SOURCES + ["TODO: Quran/hadith references used, or delete this line"],
            "notes": ["TODO: one sentence on the text and its VERIFIED author/source",
                      "Tanımlar A2–B1 seviyesine sadeleştirilmiştir; örnek cümleler özgün olarak hazırlanmıştır."],
        },
        "request": {k: meta.get(k, '') for k in ('author', 'source', 'level', 'source_type')} | {"notes": notes},
        "poem": units, "rows": rows, "cards": cards,
    }
    pathlib.Path(dst).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(dst).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{len(units)} units, {len(cards)} cards -> {dst}')
    for i, c in enumerate(cards, 1):
        print(f'  card {i}: {re.sub("<[^>]+>", "", c["word"])}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
