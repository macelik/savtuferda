#!/usr/bin/env python3
"""Compose a promo video timeline from a storyboard.

Usage:
    python3 compose.py <storyboard.json> <out_dir>

Writes:
    <out_dir>/full.html    the long cut   (render with render.js)
    <out_dir>/short.html   the short cut  (scenes that have "short")
    <out_dir>/seslendirme.md   Turkish voice-over sheet with timestamps for both cuts
    <out_dir>/timeline.json    scene start/end times (for stills and checks)

See ../SKILL.md and ../references/scene-types.md for the storyboard format.
"""
import json, re, sys, pathlib, html

HERE = pathlib.Path(__file__).resolve().parent
KIT = HERE.parent / 'assets' / 'scene-kit.html'

# Minimum length of each scene type (s): the time its built-in choreography needs.
MIN_DUR = {'hook': 4.6, 'motto': 6.0, 'verse': 6.4, 'zoom': 4.4, 'root': 6.2, 'harf': 4.2,
           'syn': 4.0, 'context': 4.8, 'press': 4.2, 'ayah': 4.8, 'literary': 5.4,
           'punch': 3.0, 'quiz': 6.0, 'statement': 4.6, 'cta': 6.4}
STEP_TYPES = ('root', 'harf', 'syn', 'context', 'press', 'ayah')
WORDS_PER_SEC = 2.6
UNSAFE = re.compile(r'<\s*(script|iframe|object|embed|foreignObject|image)|\son\w+\s*=|javascript:|(href|src)\s*=\s*["\']?\s*(https?:|//)', re.I)

# ---------------------------------------------------------------- helpers
DIAC = 'ً-ٰٟـ'
HAMZA, WEAK = 'ءأإآؤئا', 'اوىيئ'


def same(r, ch):
    return r == ch or (r in HAMZA and ch in HAMZA) or (r in 'وي' and ch in WEAK)


def hl(word, root):
    """Wrap the root letters inside a vowelled word in <span class="rl"> (same rule as the lesson page)."""
    clusters = re.findall(f'[^{DIAC}][{DIAC}]*|[{DIAC}]+', word)
    out, ri, run = '', 0, ''
    for k in clusters:
        b = k[0]
        if ri < len(root) and same(root[ri], b):
            ri += 1
            if 'ّ' in k and ri < len(root) and same(root[ri], b):
                ri += 1
            run += k
        else:
            if run:
                out += f'<span class="rl">{run}</span>'; run = ''
            out += k
    if run:
        out += f'<span class="rl">{run}</span>'
    return out


def root_of(card):
    m = re.search(r'Kök:</b>\s*([^\s·<]+)', card.get('sarfNote', '')) or re.search(r'<b>([^<\s]+-[^<\s]+)</b>', card.get('sarfNote', ''))
    return m.group(1).split('-') if m else []


def plain(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h or '')).strip()


def words(text):
    return len(re.findall(r'\S+', plain(text)))


def lit(text):
    """Teacher-facing text may contain simple markup (<b>, <mark>, <span class="rl">, <br>)."""
    return text or ''


def ar(text):
    return f'lang="ar"'


# ---------------------------------------------------------------- scene renderers
# Each returns inner HTML of one <section>. Element entrances use --r (seconds after scene start);
# the short cut compresses them with --k. Markup mirrors the original hand-made Reel.

def r_hook(s, ctx):
    return f'''  <div class="rays spin" style="top:860px">{RAYS}</div>
  <div class="center" style="top:560px"><p class="eyebrow a up" style="--r:.2s">{lit(s.get('eyebrow',''))}</p></div>
  <div class="center" style="top:700px">
    <p class="h1 a up" style="--r:.5s">{lit(s['line1'])}</p>
    <p class="h1 a up" style="--r:.8s;color:var(--gold)">{lit(s.get('line2',''))}</p>
  </div>
  <p class="ar a blur" lang="ar" style="--r:1.3s;position:absolute;left:0;right:0;top:1060px;text-align:center;font-size:260px;line-height:1;color:var(--gold);opacity:.9">{lit(s.get('glyph','؟'))}</p>'''


def r_motto(s, ctx):
    items = s['items'][:3]
    rs = ['.5s', '1.8s', '3.1s']
    rows = []
    for i, it in enumerate(items):
        gold = ';color:var(--gold)' if i == len(items) - 1 else ''
        rows.append(f'''    <div class="a pop" style="--r:{rs[i]}"><p class="ar" lang="ar" style="font-size:118px;line-height:1.35;font-weight:700{gold}">{it['ar']}</p><p class="tr">{lit(it.get('tr',''))}</p></div>''')
    return f'''  <div class="ring" style="left:290px;top:560px;width:500px;height:500px;--r:.4s"></div>
  <div class="ring" style="left:290px;top:560px;width:500px;height:500px;--r:1.6s"></div>
  <div class="center" style="top:470px"><p class="eyebrow a up" style="--r:.1s">{lit(s.get('eyebrow','Mottomuz'))}</p></div>
  <div class="center" style="top:600px;display:grid;gap:34px">
{chr(10).join(rows)}
  </div>'''


def r_verse(s, ctx):
    def ctxline(t, r):
        return f'''    <p class="ar a up" lang="ar" style="--r:{r}s;font-size:56px;line-height:1.6;opacity:.5"><span class="a dim" style="--r:2.6s;display:block">{t}</span></p>'''
    before = [ctxline(t, round(.3 + .3 * i, 2)) for i, t in enumerate(s.get('before', [])[:2])]
    after = [ctxline(t, .9) for t in s.get('after', [])[:1]]
    line = re.sub(r'<mark>', '<mark style="color:var(--gold2)">', s['line'])
    cap = f'''\n  <p class="cap a up" style="--r:3.9s;top:1420px">{lit(s['caption'])}</p>''' if s.get('caption') else ''
    return f'''  <div class="center" style="top:440px"><p class="eyebrow a up" style="--r:.1s">{lit(s.get('eyebrow',''))}</p></div>
  <div class="center" style="top:580px;display:grid;gap:26px">
{chr(10).join(before)}
    <div class="card a pop" style="--r:2.4s;margin:24px -20px;transform-origin:center">
      <p class="ar" lang="ar" style="font-size:82px;line-height:1.6;font-weight:700">{line}</p>
      <p class="tr a fade" style="--r:3.4s">{lit(s.get('tr',''))}</p>
    </div>
{chr(10).join(after)}
  </div>{cap}'''


def r_zoom(s, ctx):
    size = 250 if len(plain(s['word'])) <= 8 else 170
    cap = f'''\n  <p class="cap a up" style="--r:2.8s;top:1420px">{lit(s['caption'])}</p>''' if s.get('caption') else ''
    return f'''  <div class="ring" style="left:240px;top:560px;width:600px;height:600px;--r:.2s"></div>
  <p class="ar a blur" lang="ar" style="--r:.1s;position:absolute;left:0;right:0;top:600px;text-align:center;font-size:{size}px;line-height:1.5;font-weight:700">{s['word']}</p>
  <svg class="a up" style="--r:.7s;position:absolute;left:640px;top:520px" width="300" height="300" viewBox="0 0 300 300"><circle cx="120" cy="120" r="95" fill="rgba(226,184,90,.08)" stroke="#e2b85a" stroke-width="14"/><path d="M190 190 L270 270" stroke="#e2b85a" stroke-width="26" stroke-linecap="round"/></svg>
  <div class="center" style="top:1060px">
    <p class="h2 a up" style="--r:1.2s">{lit(s.get('q1',''))}</p>
    <p class="h2 a up" style="--r:2s;color:var(--gold)">{lit(s.get('q2',''))}</p>
  </div>{cap}'''


def step_head(s, ctx):
    n = ctx['step_no']
    dots = ''.join(f'<i class="{"on" if j == n else ""}"></i>' for j in range(1, ctx['step_total'] + 1))
    return f'''  <div class="step">{dots}</div>
  <div class="stitle a up" style="--r:.1s"><div class="n">{n}</div><h2>{lit(s['title'])}</h2></div>'''


def r_root(s, ctx):
    letters = s['letters']
    tiles = ''.join(f'''
    <span class="a drop ar" lang="ar" style="--r:{round(.6 + .25 * i, 2)}s;width:170px;height:190px;border-radius:32px;background:var(--gold);color:#1b1608;font-size:120px;font-weight:700;display:grid;place-items:center;line-height:1">{l}</span>''' for i, l in enumerate(letters))
    labels = [('الماضي', 'mazi'), ('المضارع', 'muzari'), ('المصدر', 'masdar')]
    forms = ''.join(f'''
    <div class="card a up" style="--r:{round(1.8 + .4 * i, 2)}s;padding:26px 10px;text-align:center"><p class="ar" lang="ar" style="font-size:34px;color:#66736b;line-height:1.3;margin-bottom:22px">{labels[i][0]}</p><p class="ar" lang="ar" style="font-size:{96 if len(plain(w)) <= 6 else 72}px;line-height:1.45;font-weight:700">{hl(w, letters)}</p><p style="font-size:32px;color:#66736b">{labels[i][1]}</p></div>''' for i, w in enumerate(s['forms'][:3]))
    cap = f'''\n  <p class="cap a up" style="--r:3.2s;top:1360px">{lit(s['caption'])}</p>''' if s.get('caption') else ''
    return step_head(s, ctx) + f'''
  <div style="position:absolute;top:700px;left:0;right:0;display:flex;justify-content:center;gap:30px;direction:rtl">{tiles}
  </div>
  <div style="position:absolute;top:960px;left:70px;right:70px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px;direction:rtl">{forms}
  </div>{cap}'''


def r_harf(s, ctx):
    chips = ''.join(f'''
    <span class="a pop ar" lang="ar" style="--r:{round(.5 + .3 * i, 2)}s;font-size:130px;font-weight:700;line-height:1.3;padding:10px 60px;border-radius:40px;border:5px solid var(--gold);color:var(--gold)">{c}</span>''' for i, c in enumerate(s['chips'][:3]))
    ex = s.get('example') or {}
    exh = re.sub(r'<b>(.*?)</b>', r'<span class="rl">\1</span>', ex.get('ar', ''))
    return step_head(s, ctx) + f'''
  <div style="position:absolute;top:700px;left:0;right:0;display:flex;justify-content:center;gap:40px;direction:rtl">{chips}
  </div>
  <div class="center card a up" style="--r:1.4s;top:1000px">
    <p class="ar" lang="ar" style="font-size:76px;line-height:1.5;font-weight:700">{exh}</p>
    <p class="tr" style="margin-top:14px">{lit(ex.get('tr',''))}</p>
  </div>'''


def r_syn(s, ctx):
    def col(label, ar_label, colour, items, r):
        return f'''<div class="card a up" style="--r:{r}s;text-align:center;padding:36px 20px"><p style="font-size:34px;font-weight:800;letter-spacing:.12em;color:{colour}">{label}</p><p class="ar" lang="ar" style="font-size:40px;color:{colour};line-height:1.4;margin-bottom:10px">{ar_label}</p><p class="ar" lang="ar" style="font-size:72px;line-height:1.6;font-weight:700">{'<br>'.join(items[:2])}</p></div>'''
    cap = f'''\n  <p class="cap a up" style="--r:1.5s;top:1240px">{lit(s['caption'])}</p>''' if s.get('caption') else ''
    return step_head(s, ctx) + f'''
  <div style="position:absolute;top:720px;left:70px;right:70px;display:grid;grid-template-columns:1fr 1fr;gap:26px">
    {col('EŞ ANLAMLI', 'مرادف', 'var(--green)', s['syn'], .5)}
    {col('ZIT ANLAMLI', 'ضد', '#9c4536', s['ant'], .9)}
  </div>{cap}'''


def r_context(s, ctx):
    rows = ''.join(f'''
    <div class="card a up" style="--r:{round(.5 + .4 * i, 2)}s;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:30px 44px"><span style="font-size:46px;font-weight:700">{lit(r['tr'])}</span><span class="ar" lang="ar" style="font-size:66px;font-weight:700;line-height:1.4">{r['ar']}</span></div>''' for i, r in enumerate(s['rows'][:2]))
    m = s.get('mecaz')
    mec = f'''
    <div class="card a pop" style="--r:1.8s;padding:30px 44px;text-align:center;background:var(--gold)"><p style="font-size:34px;font-weight:800;letter-spacing:.14em;margin-bottom:16px">MECAZ</p><p class="ar" lang="ar" style="font-size:72px;font-weight:700;line-height:1.5">{m['ar']}</p><p class="tr" style="color:#3b2f12">{lit(m.get('tr',''))}</p></div>''' if m else ''
    return step_head(s, ctx) + f'''
  <div style="position:absolute;top:700px;left:70px;right:70px;display:grid;gap:26px">{rows}{mec}
  </div>'''


def r_press(s, ctx):
    return step_head(s, ctx) + f'''
  <div class="center a up" style="--r:.5s;top:720px;background:var(--stone);color:var(--stone-ink);border-radius:30px;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.35);text-align:right">
    <div style="background:#9c4536;color:#fff;display:flex;justify-content:space-between;align-items:center;padding:16px 34px;font-weight:800;font-size:34px;letter-spacing:.12em"><span>HABER</span><span class="ar" lang="ar" style="font-size:44px;letter-spacing:0;line-height:1.2">أخبار</span></div>
    <div style="padding:34px 44px">
      <p class="ar" lang="ar" style="font-size:70px;line-height:1.55;font-weight:700">{s['ar']}</p>
      <p class="tr" style="text-align:left;margin-top:18px">{lit(s.get('tr',''))}</p>
    </div>
  </div>'''


def r_ayah(s, ctx):
    size = 92 if len(plain(s['ar'])) < 60 else 72
    return step_head(s, ctx) + f'''
  <div class="rays spin" style="top:960px">{RAYS}</div>
  <div class="center a blur" style="--r:.6s;top:720px">
    <p class="ar" lang="ar" style="font-size:{size}px;line-height:1.75;font-weight:700">{s['ar']}</p>
    <p class="tr a fade" style="--r:1.8s;margin-top:20px">{lit(s.get('tr',''))}</p>
    <p class="a fade" style="--r:2.2s;margin-top:18px;font-size:36px;font-weight:800;color:var(--gold);letter-spacing:.1em">{html.escape(s.get('src','').upper())}</p>
  </div>'''


DEFAULT_ART = '''<path d="M60 150 L52 108 L80 74 L150 70 L188 100 L184 150 Z" class="s"/><g class="flick"><circle cx="120" cy="40" r="7" class="f"/><path d="M120 40 L94 25 M120 40 L107 12 M120 40 L120 8 M120 40 L133 12 M120 40 L146 25" class="s" style="stroke-width:2.5"/></g>'''


def r_literary(s, ctx):
    cap = f'''\n  <p class="cap a up" style="--r:2.6s;top:1400px">{lit(s['caption'])}</p>''' if s.get('caption') else ''
    return f'''  <div class="center" style="top:450px"><p class="eyebrow a up" style="--r:.1s">{lit(s.get('eyebrow',''))}</p><p class="h2 a up" style="--r:.3s;margin-top:14px">{lit(s.get('title',''))}</p></div>
  <svg class="art" style="position:absolute;left:290px;top:690px" width="500" height="380" viewBox="0 0 240 180">{s.get('art') or DEFAULT_ART}</svg>
  <div class="center" style="top:1100px">
    <p class="a up" style="--r:1s;font-size:50px;line-height:1.35">{lit(s.get('line',''))}</p>
    <p class="a up h2" style="--r:1.6s;color:var(--gold);margin-top:10px">{lit(s.get('big',''))}</p>
  </div>{cap}'''


def r_punch(s, ctx):
    return f'''  <div class="center" style="top:700px">
    <p class="h1 a up" style="--r:.1s">{lit(s['q'])}</p>
    <p class="h1 a pop" style="--r:1.1s;color:var(--gold);font-size:150px;margin-top:40px">{lit(s['a'])}</p>
  </div>'''


def r_quiz(s, ctx):
    opts = s['options'][:4]
    ans = s['answer']
    idx = opts.index(ans)
    cells = []
    for i, o in enumerate(opts):
        if i == idx:
            cells.append(f'''    <div class="opt ok a up" lang="ar" style="--r:{round(1 + .15 * i, 2)}s"><span>{o}</span></div>''')
        else:
            cells.append(f'''    <div class="opt a up" lang="ar" style="--r:{round(1 + .15 * i, 2)}s">{o}</div>''')
    # RTL grid: index 0 = right column, 1 = left column, 2 = right, 3 = left
    left = 245 if idx % 2 == 1 else 725
    top = 1270 if idx < 2 else 1413
    cap = f'''\n  <p class="cap a up" style="--r:3.6s;top:1390px">{lit(s['caption'])}</p>''' if s.get('caption') else ''
    return f'''  <div class="center" style="top:440px"><p class="eyebrow a up" style="--r:.1s">{lit(s.get('eyebrow',''))}</p><p class="h2 a up" style="--r:.3s;margin-top:10px">{lit(s.get('title',''))}</p></div>
  <div class="center card a up" style="--r:.6s;top:700px">
    <p class="ar" lang="ar" style="font-size:74px;line-height:1.7;font-weight:700">{s.get('before','')} <span style="display:inline-block;min-width:240px;border-bottom:6px solid var(--gold2);position:relative"><span class="a pop" style="--r:3.3s;color:var(--gold2)">{ans}</span></span> {s.get('after','')}</p>
  </div>
  <div style="position:absolute;top:1010px;left:70px;right:70px;display:grid;grid-template-columns:1fr 1fr;gap:22px;direction:rtl">
{chr(10).join(cells)}
  </div>
  <div class="tap" style="--r:2.6s;left:{left}px;top:{top}px"></div>{cap}'''


def r_statement(s, ctx):
    strike = f'''<p class="a up" style="--r:.1s;font-size:56px;color:var(--muted);text-decoration:line-through;text-decoration-color:var(--red);text-decoration-thickness:5px">{lit(s['strike'])}</p>''' if s.get('strike') else ''
    cap = f'''\n  <p class="cap a up" style="--r:2.5s;top:1330px">{lit(s['caption'])}</p>''' if s.get('caption') else ''
    return f'''  <div class="center" style="top:600px">
    {strike}
    <p class="h2 a up" style="--r:.8s;margin-top:50px">{lit(s['line1'])}</p>
    <p class="h2 a up" style="--r:1.6s;margin-top:30px;color:var(--gold)">{lit(s.get('line2',''))}</p>
  </div>{cap}'''


def r_cta(s, ctx):
    return f'''  <div class="rays spin" style="top:960px">{RAYS}</div>
  <div class="center" style="top:470px">
    <p class="ar a blur" lang="ar" style="--r:.1s;font-size:78px;line-height:1.5;font-weight:700;color:var(--gold)">{s.get('motto','')}</p>
  </div>
  <div class="center" style="top:760px">
    <p class="h1 a up" style="--r:.7s;font-size:100px">{lit(s['title'])}</p>
    <p class="tr a up" style="--r:1.3s;margin-top:30px">{lit(s.get('sub',''))}</p>
  </div>
  <div class="a pop" style="--r:1.9s;position:absolute;left:190px;right:190px;top:1180px">
    <div class="dm">{lit(s.get('button','Detaylar için DM’den yazın'))}</div>
  </div>
  <p class="a up" style="--r:2.5s;position:absolute;left:0;right:0;top:1340px;text-align:center;font-family:var(--display);font-weight:800;font-size:64px;color:var(--ink)">{html.escape(ctx['handle'])}</p>'''


RENDER = {k[2:]: v for k, v in globals().items() if k.startswith('r_')}
RAYS = ''.join(f'<i style="transform:rotate({i * 22.5}deg)"></i>' for i in range(16))

# What the teacher sees on screen, for the voice-over sheet.
SCREEN = {
    'hook': lambda s: f"“{plain(s['line1'])} {plain(s.get('line2',''))}” yazısı",
    'motto': lambda s: 'Arapça motto kelime kelime beliriyor',
    'verse': lambda s: 'metnin satırları; hedef satır kart olarak öne çıkıyor',
    'zoom': lambda s: f"büyük “{plain(s['word'])}” ve mercek",
    'root': lambda s: f"{s['_n']}. adım: kök harfleri ({' '.join(s['letters'])}) düşüyor, sonra mazi, muzari, masdar",
    'harf': lambda s: f"{s['_n']}. adım: harf-i cerler ({' / '.join(s['chips'])}) ve bir örnek",
    'syn': lambda s: f"{s['_n']}. adım: eş ve zıt anlamlılar",
    'context': lambda s: f"{s['_n']}. adım: bağlama göre anlamlar" + (' ve mecaz kartı' if s.get('mecaz') else ''),
    'press': lambda s: f"{s['_n']}. adım: haber kartı",
    'ayah': lambda s: f"{s['_n']}. adım: ayet ({s.get('src','')})",
    'literary': lambda s: f"edebî tahlil: {plain(s.get('big',''))}",
    'punch': lambda s: f"“{plain(s['q'])}” ve ardından büyük “{plain(s['a'])}”",
    'quiz': lambda s: 'boşluk doldurma sorusu; doğru cevap seçilip yeşile dönüyor',
    'statement': lambda s: f"“{plain(s['line1'])}” " + (f"(üstü çizili “{plain(s['strike'])}”)" if s.get('strike') else ''),
    'cta': lambda s: 'davet, DM butonu ve hesap adı',
}
# Moments inside a scene worth cueing (offset in s from scene start, Turkish label).
CUES = {
    'motto': lambda s: [(r, f"“{plain(i['ar'])}” belirir") for r, i in zip((.5, 1.8, 3.1), s['items'][:3])],
    'verse': lambda s: [(2.4, 'hedef satır öne çıkar; o anda okuyun')],
    'punch': lambda s: [(1.1, f"“{plain(s['a'])}” ekrana gelir")],
    'quiz': lambda s: [(3.0, 'doğru cevap yeşile döner')],
    'cta': lambda s: [(2.5, 'hesap adı belirir')],
}


# ---------------------------------------------------------------- lesson data fill-in
def fill_from_card(s, cards):
    n = s.get('from_card')
    if not n:
        return s
    c = cards[n - 1]
    t = s['type']
    out = dict(s)
    if t == 'root':
        out.setdefault('letters', root_of(c))
        out.setdefault('forms', c['sarf'][0])
    elif t == 'harf' and c.get('harf'):
        out.setdefault('chips', c['harf']['chips'])
        out.setdefault('example', c['harf']['ex'][0])
    elif t == 'syn':
        sy = next((x['ar'] for x in c['syn'] if x['k'] == 'syn'), '')
        an = next((x['ar'] for x in c['syn'] if x['k'] == 'ant'), '')
        out.setdefault('syn', [w.strip() for w in sy.split('،')][:2])
        out.setdefault('ant', [w.strip() for w in an.split('،')][:2])
    elif t == 'context':
        m = next((e for e in c.get('extras', []) if e['tag'] == 'mecaz'), None)
        if m:
            out.setdefault('mecaz', {'ar': m['ar'], 'tr': m['tr']})
    elif t == 'press':
        p = next((e for e in c.get('extras', []) if e['tag'] == 'basın'), None)
        if p:
            out.setdefault('ar', p['ar']); out.setdefault('tr', p['tr'])
    elif t == 'ayah':
        a = next((e for e in c.get('extras', []) if e['tag'] == 'ayet'), None) or (c.get('ayat') or [None])[0]
        if a:
            out.setdefault('ar', a['ar']); out.setdefault('tr', a['tr']); out.setdefault('src', a.get('src', ''))
    elif t == 'zoom':
        out.setdefault('word', re.sub('[ً-ٰٟ]$', '', c['word']))
    elif t == 'verse':
        out.setdefault('line', c['verse']); out.setdefault('tr', c['verseTr'])
    return out


REQUIRED = {'hook': ['line1'], 'motto': ['items'], 'verse': ['line'], 'zoom': ['word'],
            'root': ['title', 'letters', 'forms'], 'harf': ['title', 'chips'], 'syn': ['title', 'syn', 'ant'],
            'context': ['title', 'rows'], 'press': ['title', 'ar'], 'ayah': ['title', 'ar', 'src'],
            'literary': ['big'], 'punch': ['q', 'a'], 'quiz': ['options', 'answer'],
            'statement': ['line1'], 'cta': ['title']}


def mmss(t):
    t = int(round(t))
    return f'{t // 60}:{t % 60:02d}'


def build(sb, scenes, cut, kit, handle, title):
    """scenes: list of (scene, start, end, k). Returns html."""
    total_steps = sum(1 for s, *_ in scenes if s['type'] in STEP_TYPES)
    parts, n = [], 0
    for idx, (s, a, e, k) in enumerate(scenes):
        ctx = {'handle': handle, 'step_total': total_steps}
        if s['type'] in STEP_TYPES:
            n += 1; ctx['step_no'] = n
        end = 999 if idx == len(scenes) - 1 else e
        kk = f' style="--k:{k}"' if k != 1 else ''
        parts.append(f'<!-- {idx + 1} {s["type"].upper()} {a:.1f}–{e:.1f} -->\n<section class="sc" data-s="{a:g}" data-e="{end:g}"{kk}>\n{RENDER[s["type"]](s, ctx)}\n</section>')
    total = scenes[-1][2]
    return (kit.replace('__SCENES__', '\n\n'.join(parts)).replace('__HANDLE__', html.escape(handle))
            .replace('__TOTAL__', f'{total:g}').replace('__CSS__', sb.get('css', '').replace('</', '')).replace('__TITLE__', html.escape(f'{title} · {cut}')))


def main(sb_path, out_dir):
    sb_path = pathlib.Path(sb_path)
    sb = json.load(open(sb_path, encoding='utf-8'))
    cards = []
    if sb.get('lesson'):
        lp = (sb_path.parent / sb['lesson']).resolve()
        if lp.suffix.lower() in ('.html', '.htm'):
            m = re.search(r'<script type="application/json" id="data">(.*?)</script>', lp.read_text(encoding='utf-8'), re.S)
            cards = json.loads(m.group(1).replace('<\\/', '</'))['cards']
        else:
            cards = json.load(open(lp, encoding='utf-8'))['cards']
    handle = sb.get('handle', '')
    errs = []
    scenes = []
    for i, s in enumerate(sb['scenes'], 1):
        if s.get('type') not in RENDER:
            errs.append(f'scene {i}: unknown type "{s.get("type")}" (allowed: {", ".join(RENDER)})'); continue
        if s.get('from_card') and not cards:
            errs.append(f'scene {i}: "from_card" needs "lesson" (path to the lesson .html or .json)'); continue
        s = fill_from_card(s, cards)
        for f in REQUIRED[s['type']]:
            if not s.get(f): errs.append(f'scene {i} ({s["type"]}): missing "{f}"')
        if s['type'] == 'quiz' and s.get('answer') not in s.get('options', []):
            errs.append(f'scene {i} (quiz): "answer" must be one of "options"')
        if UNSAFE.search(json.dumps(s, ensure_ascii=False)):
            errs.append(f'scene {i}: scripts, event handlers and external URLs are not allowed')
        scenes.append(s)
    if UNSAFE.search(sb.get('css', '')) or '@import' in sb.get('css', '').lower():
        errs.append('"css" may only hold plain @keyframes / CSS')
    if errs:
        sys.exit('Storyboard errors:\n  ' + '\n  '.join(errs))

    # ---- timing: long cut
    full, t = [], 0.0
    for s in scenes:
        need = words(s.get('say', '')) / WORDS_PER_SEC + 0.9
        d = round(max(MIN_DUR[s['type']], s.get('dur', 0), need) * 10) / 10
        full.append((s, round(t, 2), round(t + d, 2), 1)); t += d
    # ---- short cut: scenes with "short" seconds
    short, t = [], 0.0
    for s in scenes:
        d = s.get('short')
        if not d:
            continue
        k = s.get('k') or max(.45, min(1, round(d / MIN_DUR[s['type']], 2)))
        short.append((s, round(t, 2), round(t + d, 2), k)); t += d

    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    kit = KIT.read_text(encoding='utf-8')
    title = sb.get('title', 'Promo')
    (out / 'full.html').write_text(build(sb, full, 'uzun', kit, handle, title), encoding='utf-8')
    if short:
        (out / 'short.html').write_text(build(sb, short, 'kısa', kit, handle, title), encoding='utf-8')
    (out / 'timeline.json').write_text(json.dumps({
        'full': [{'type': s['type'], 'start': a, 'end': e} for s, a, e, _ in full],
        'short': [{'type': s['type'], 'start': a, 'end': e} for s, a, e, _ in short]}, indent=1), encoding='utf-8')

    # ---- Turkish voice-over sheet
    def sheet(cut, rows, key):
        L = []
        for s, a, e, k in rows:
            L.append(f"**{mmss(a)} – {mmss(e)}**")
            cue = SCREEN[s['type']]({**s, '_n': s.get('_n', '')})
            L.append(f"[[Ekranda: {cue}.]]")
            for off, label in CUES.get(s['type'], lambda s: [])(s):
                L.append(f"[[{mmss(a + off * k)} · {label}.]]")
            if s.get('note'):
                L.append(f"[[{s['note']}]]")
            text = s.get(key) if key == 'say' else s.get('say_short')
            L.append(text if text else '[[Bu bölümde konuşma yok; müzik ve ekrandaki yazılar yeterli.]]')
            L.append('')
        return f"## {cut}\n\n" + '\n'.join(L)
    # number the step scenes for the sheet
    n = 0
    for s in scenes:
        if s['type'] in STEP_TYPES:
            n += 1; s['_n'] = n
    md = [f"# Seslendirme metni · {title}\n",
          "Düz yazı okunacak metindir. `[[…]]` içindekiler okunmaz: o anda ekranda ne olduğunu ve nasıl söyleneceğini anlatır. Zamanlar dakika:saniye.\n",
          sheet(f'Uzun versiyon ({mmss(full[-1][2])})', full, 'say')]
    if short:
        md.append(sheet(f'Kısa versiyon ({mmss(short[-1][2])})', short, 'say_short'))
    (out / 'seslendirme.md').write_text('\n'.join(md), encoding='utf-8')
    print(f'full: {len(full)} scenes, {full[-1][2]:.1f} s -> {out / "full.html"}')
    if short:
        print(f'short: {len(short)} scenes, {short[-1][2]:.1f} s -> {out / "short.html"}')
    print(f'voice-over sheet -> {out / "seslendirme.md"}')
    for s, a, e, _ in full:
        need = words(s.get('say', '')) / WORDS_PER_SEC
        if need > e - a - 0.5:
            print(f'note: {s["type"]} at {mmss(a)}: narration ({words(s.get("say",""))} words) is tight for {e - a:.1f} s')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
