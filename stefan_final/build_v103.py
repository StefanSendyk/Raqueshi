# v103 = v102 + varied layout (suggestions 2-5): chapter bands / slim headings, full-width pieces, crew ID cards,
# genre film strip, treatment on script paper, chapter colours from the moodboard. Patches v102's output.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
s = open(os.path.join(ROOT, 'Media_Studies_portfolio102.html'), encoding='utf-8').read()
rd = lambda f: open(os.path.join(HERE, f), encoding='utf-8').read()
IMG = 'https://cdn.jsdelivr.net/gh/StefanSendyk/Raqueshi@MediaStudies/media_photos_hq/'
def img(path, alt, cls=''):
    return f'<img{cls} src="{IMG}{path}" onerror="this.onerror=null;this.src=\'media_photos_hq/{path}\'" alt="{alt}" loading="lazy">'
def band(path, alt, credit):
    return f'\n      <figure class="ch-band" aria-hidden="true">{img(path, alt)}<figcaption>{credit}</figcaption></figure>'

def page(pid):
    a = s.index('<script type="text/plain" id="mm-page-%s">' % pid); e = s.index('</html>\n</script>', a); return a, e

def patch(pid, big, slim, wide, extra_css='', fn=None):
    global s
    a, e = page(pid); p = s[a:e]
    for sid, (path, alt, credit) in big.items():
        o = f'<section class="chapter" id="{sid}">'; assert p.count(o) == 1, o
        p = p.replace(o, f'<section class="chapter ch-big" id="{sid}">' + band(path, alt, credit))
    for sid in slim:
        o = f'<section class="chapter" id="{sid}">'; assert p.count(o) == 1, o
        n = re.search(r'Chapter (\d+)', p[p.index(o):p.index(o) + 300]).group(1)
        p = p.replace(o, f'<section class="chapter ch-slim" id="{sid}">\n      <span class="ch-num" aria-hidden="true">{n}</span>')
    for o, c in wide:
        assert o in p, o; p = p.replace(o, o.replace('class="', 'class="fullw ', 1), c)
    if fn: p = fn(p)
    i = p.index('</style>'); p = p[:i] + rd('layout_v103.css') + extra_css + p[i:]
    i = p.rindex('</body>'); p = p[:i] + rd('layout_v103.js') + p[i:]
    assert '</script>' not in p.split('id="mm-page-%s">' % pid, 1)[1]
    s = s[:a] + p + s[e:]

def final_fn(p):
    # crew ID cards
    for name, ini, no in (('Stefan', 'S', '01'), ('Anna Van Der Lip', 'A', '02')):
        o = re.search(r'<article class="fp-card( rv[^"]*)">\s*<h3>' + name + '</h3>', p); assert o, name
        p = p.replace(o.group(0), f'<article class="fp-card id-card{o.group(1)}" data-no="Still House Productions · Crew ID · {no}">\n          <span class="id-photo" aria-hidden="true">{ini}</span>\n          <h3>{name}</h3>')
    # genre history film strip with a still per era
    o = '<ol class="fp-time rv">\n        <li><b>1940s–60s</b>'; assert p.count(o) == 1
    p = p.replace(o, '<ol class="fp-time fp-strip rv" tabindex="0" aria-label="Action film history, scroll sideways">\n        <li><b>1940s–60s</b>')
    for era, path, alt in (('1940s–60s', 'v103/hist_drno.jpg', 'Still from Dr. No (1962)'), ('1970s–80s', 'v103/hist_diehard.jpg', 'Still from Die Hard (1988)'),
                           ('1990s–2000s', 'v103/hist_matrix.jpg', 'Still from The Matrix (1999)'), ('Today', 'v103/hist_johnwick.jpg', 'Still from John Wick: Chapter 2 (2017)')):
        o = f'<li><b>{era}</b>'; assert p.count(o) == 1, era
        p = p.replace(o, f'<li>{img(path, alt)}<b>{era}</b>')
    o = '</ol>\n\n      <div class="plan-head rv"><h3>Genre icons</h3>'; assert o in p
    p = p.replace(o, '</ol>\n      <p class="fp-strip-hint" aria-hidden="true">Scroll sideways →</p>\n\n      <div class="plan-head rv"><h3>Genre icons</h3>')
    i = p.index('</head>'); p = p[:i] + '<link href="https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">\n' + p[i:]
    return p

patch('final',
      big={'research': ('v103/band_heat.jpg', 'Still from Heat', 'Heat (1995)'),
           'planning': ('v103/band_inception.jpg', 'Still from Inception', 'Inception (2010)'),
           'preproduction': ('v103/band_collateral.jpg', 'Still from Collateral', 'Collateral (2004)')},
      slim=['brief', 'team', 'studio', 'genre', 'audience', 'ideas', 'theory', 'production', 'final-cut', 'evaluation'],
      wide=[('<div class="fp-mind2 rv">', 3), ('<div class="fp-moods">', 1), ('<ol class="fp-time rv"><li><b>0:00 · Ident</b>', 1)],
      extra_css=rd('final_v103.css'), fn=final_fn)
patch('prelim',
      big={'research': ('prelim_final_poster.jpg', 'Frame from The Meeting', 'The Meeting · my film'),
           'planning': ('prelim_hero_bench_sunset.jpg', 'Frame from The Meeting', 'The Meeting · my film')},
      slim=['brief', 'final-cut', 'evaluation'],
      wide=[('<div class="mindmap rv" id="pl-mindmap">', 1)])
out = os.path.join(ROOT, 'Media_Studies_portfolio103.html'); open(out, 'w', encoding='utf-8').write(s); print(out, round(os.path.getsize(out) / 1e6, 2), 'MB')
