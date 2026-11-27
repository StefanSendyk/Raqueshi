# v104 = v103 + a look of its own per page (suggestion 1): Dirty Deeds as a case file, The Meeting warm and quiet.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
s = open(os.path.join(ROOT, 'Media_Studies_portfolio103.html'), encoding='utf-8').read()
rd = lambda f: open(os.path.join(HERE, f), encoding='utf-8').read()
FONT = '<link href="https://fonts.googleapis.com/css2?family=Special+Elite&display=swap" rel="stylesheet">\n'
for pid, css, word in (('final', 'theme_final_v104.css', 'File'), ('prelim', 'theme_prelim_v104.css', 'Scene')):
    a = s.index('<script type="text/plain" id="mm-page-%s">' % pid); e = s.index('</html>\n</script>', a); p = s[a:e]
    p, n = re.subn(r'(<span class="idx ctag rv">)Chapter ', r'\g<1>' + word + ' ', p); assert n >= 5, (pid, n)
    i = p.index('</head>'); p = p[:i] + (FONT if pid == 'final' else '') + '<style>' + rd(css) + rd('nobreak_v104.css') + '</style>\n' + p[i:]
    s = s[:a] + p + s[e:]

# 104b: no full-width pieces (the sidebar still steps aside for the chapter film stills)
s = s.replace('class="fullw ', 'class="')
# 104b: final page — no reds (yellow / cold grey instead), Pulp Fiction hero in 4K
a = s.index('<script type="text/plain" id="mm-page-final">'); e = s.index('</html>\n</script>', a); p = s[a:e]
SW = '--c:#a3171f'; p = p.replace(SW, '@@SW@@')  # the moodboard swatch is the lipstick colour in the film: kept
for old, new in (('#c4373e', '#d6a85a'), ('#dc4a50', '#e2b866'), ('rgba(196,55,62', 'rgba(214,168,90'), ('#a3171f', '#8a96a6'), ('#e0453a', '#e2b866'),
                 ('#140a0b', '#0e1115'), ('#110d0d', '#0e1115'), ('#cf4a2a', '#8a96a6'), ('#d9583f', '#e2b866')):
    p = p.replace(old, new)
p = p.replace('@@SW@@', SW)
old = 'https://cdn.jsdelivr.net/gh/StefanSendyk/Raqueshi@7bcb14332dff8f0021751a2cea4ec1d68a442ab3/media_photos_hq/v86/prelim_lalaland.jpg" alt="Still from La La Land: Sebastian and Mia watching a film in the cinema"'
assert p.count(old) == 1
p = p.replace(old, 'https://cdn.jsdelivr.net/gh/StefanSendyk/Raqueshi@MediaStudies/media_photos_hq/v104/hero_pulpfiction_vincent_jules.jpg" onerror="this.onerror=null;this.src=\'media_photos_hq/v104/hero_pulpfiction_vincent_jules.jpg\'" alt="Pulp Fiction: Vincent and Jules aiming their guns"')
assert p.count('Still: La La Land (2016) · © Lionsgate') == 1
p = p.replace('Still: La La Land (2016) · © Lionsgate', 'Still: Pulp Fiction (1994) · © Miramax')
s = s[:a] + p + s[e:]

# 104e: chapter heading block = number | (tag + title); big chapters get a number too
for pid in ('final', 'prelim'):
    a = s.index('<script type="text/plain" id="mm-page-%s">' % pid); e = s.index('</html>\n</script>', a); p = s[a:e]
    p = re.sub(r'\n      <span class="ch-num" aria-hidden="true">\d+</span>', '', p)
    def head(m):
        n = re.search(r'(\d+)', m.group(1)).group(1)
        return ('<div class="ch-head"><span class="ch-num" aria-hidden="true">%s</span><div class="ch-titles">\n      ' % n) + m.group(1) + '\n      ' + m.group(2) + '</div></div>'
    p, k = re.subn(r'(<span class="idx ctag rv">[^<]*<i>/</i>[^<]*</span>)\s*(<h2 class="rv d1">.*?</h2>)', head, p, flags=re.S); assert k >= 5, (pid, k)
    for o, n_ in (('.chapter > h2::after', '.chapter .ch-titles > h2::after'), ('.ch-big > h2 {', '.ch-big h2 {'), ('.ch-big > h2 em', '.ch-big h2 em'),
                  ('.ch-slim > h2 {', '.ch-slim h2 {'), ('.ch-big > .ch-band + .ctag { margin-top: -210px !important; }', '')):
        p = p.replace(o, n_)
    if pid == 'final':
        i = p.index('<script>\n  /* mind maps: curved wires'); j = p.index('<\\/script>', i) + len('<\\/script>')
        p = p[:i] + rd('mindmap_v104.js').strip() + p[j:]
    s = s[:a] + p + s[e:]

# 104f: a longer genre-history film strip: nine eras, a still for each
a = s.index('<script type="text/plain" id="mm-page-final">'); e = s.index('</html>\n</script>', a); p = s[a:e]
i = p.index('<ol class="fp-time fp-strip rv"'); i = p.index('>', i) + 1; j = p.index('</ol>', i)
IMG = 'https://cdn.jsdelivr.net/gh/StefanSendyk/Raqueshi@MediaStudies/media_photos_hq/'
li = re.sub(r'\{img:([^|]+)\|([^}]+)\}', lambda m: '<img src="%s%s" onerror="this.onerror=null;this.src=\'media_photos_hq/%s\'" alt="%s" loading="lazy">' % (IMG, m.group(1), m.group(1), m.group(2)), rd('history_v104.html'))
p = p[:i] + '\n' + li + '      ' + p[j:]
s = s[:a] + p + s[e:]

# pin every image link to the commit that holds the images (jsDelivr caches branch links for days)
PIN = os.environ.get('PIN')
if PIN: s = s.replace('StefanSendyk/Raqueshi@MediaStudies/', 'StefanSendyk/Raqueshi@%s/' % PIN)
out = os.path.join(ROOT, 'Media_Studies_portfolio104.html'); open(out, 'w', encoding='utf-8').write(s); print(out, round(os.path.getsize(out) / 1e6, 2), 'MB')
