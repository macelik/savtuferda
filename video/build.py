#!/usr/bin/env python3
"""Expand video/src/scene.html into renderable timelines.

    python3 video/build.py            -> video/build/full.html (75 s) and video/build/short.html (30 s)

scene.html holds every scene as <section class="sc" data-s="START" data-e="END">.
Inside a scene, each element's entrance is at  scene start + --r * --k  (seconds).
The short cut keeps a subset of scenes, gives each a new start/end, and sets --k to
compress the inner choreography. Placeholders __RAYS__ / __DOTSn__ are expanded here.
"""
import re, pathlib
HERE = pathlib.Path(__file__).parent

FULL_SECONDS = 75
SHORT_SECONDS = 30
# scene number (1-based, order in scene.html) -> (start, end, k)
SHORT_PLAN = {1: (0, 2.8, .6), 2: (2.8, 6.6, .5), 3: (6.6, 10.6, .5), 4: (10.6, 13.2, .55),
              5: (13.2, 16.2, .55), 6: (16.2, 18.2, .5), 7: (18.2, 20.2, .5), 8: (20.2, 22.4, .5),
              9: (22.4, 24.2, .5), 10: (24.2, 26.6, .5), 15: (26.6, 40, .6)}

def expand(s):
    s = s.replace('__RAYS__', ''.join(f'<i style="transform:rotate({i*22.5}deg)"></i>' for i in range(16)))
    for k in range(1, 7):
        s = s.replace(f'__DOTS{k}__', ''.join(f'<i class="{"on" if j == k else ""}"></i>' for j in range(1, 7)))
    return s

def main():
    src = expand((HERE / 'src' / 'scene.html').read_text(encoding='utf-8'))
    out = HERE / 'build'; out.mkdir(exist_ok=True)
    # last scene must not fade out before the video ends
    full = re.sub(r'(<section class="sc" data-s="[^"]*" data-e=")[^"]*("[^>]*>)(?![\s\S]*<section class="sc")', r'\g<1>999\g<2>', src)
    (out / 'full.html').write_text(full, encoding='utf-8')
    parts = re.split(r'(<section class="sc"[^>]*>.*?</section>)', src, flags=re.S)
    res, n = [], 0
    for p in parts:
        if p.startswith('<section class="sc"'):
            n += 1
            if n not in SHORT_PLAN: continue
            a, e, k = SHORT_PLAN[n]
            p = re.sub(r'<section class="sc" data-s="[^"]*" data-e="[^"]*"',
                       f'<section class="sc" data-s="{a}" data-e="{e}" style="--k:{k}"', p, count=1)
        res.append(p)
    (out / 'short.html').write_text(''.join(res), encoding='utf-8')
    print(f'{n} scenes -> video/build/full.html ({FULL_SECONDS}s), video/build/short.html ({SHORT_SECONDS}s)')

if __name__ == '__main__':
    main()
