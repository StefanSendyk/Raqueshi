# Builds Media_Studies_portfolio102.html from v101 (keeps v101's later hand edits): swaps the Final Project page body
# for final_body.html (blog-checklist sections), adds final_extra_v102.css, updates the contents panel.
import base64, html, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
s = open(os.path.join(ROOT, 'Media_Studies_portfolio101.html'), encoding='utf-8').read()
b64 = lambda f: base64.b64encode(open(os.path.join(HERE, f), 'rb').read()).decode()
body = open(os.path.join(HERE, 'final_body.html'), encoding='utf-8').read()
body = body.replace('{vid:logo}', 'data:video/mp4;base64,' + b64('stillhouse_logo_web.mp4')).replace('{img:poster}', 'data:image/jpeg;base64,' + b64('stillhouse_logo_poster.jpg'))
k = body.index('<div class="body">'); body = body[k:body.index('</main>\n</div>', k) + len('</main>\n</div>')]

a = s.index('<script type="text/plain" id="mm-page-final">'); e = s.index('</html>\n</script>', a)
page = s[a:e]
i = page.index('<div class="body">'); j = page.index('</main>\n</div>', i) + len('</main>\n</div>')
page = page[:i] + body + page[j:]
i = page.index('</style>'); page = page[:i] + open(os.path.join(HERE, 'final_extra_v102.css'), encoding='utf-8').read() + page[i:]
assert '</script>' not in page.split('id="mm-page-final">', 1)[1]
s = s[:a] + page + s[e:]

# sidebar scroll + clapstick fix, both case-study pages
css2 = open(os.path.join(HERE, 'side_v102.css'), encoding='utf-8').read()
for pid in ('prelim', 'final'):
    a = s.index('<script type="text/plain" id="mm-page-%s">' % pid); i = s.index('</style>', a)
    s = s[:i] + css2 + s[i:]

old = re.search(r'"page": "final", "part": "Case study 02", "title": "Final project", "sub": "[^"]*", "items": \[.*?\]\]', s).group(0)
ch = [("01", "Brief", "what was asked", "brief"), ("02", "Team", "Stefan & Anna Van Der Lip · roles", "team"),
      ("03", "Studio", "Still House Productions · logo & mission", "studio"), ("04", "Genre", "sub-genre · conventions · history", "genre"),
      ("05", "Research", "USPs, gaps & title sequences", "research"), ("06", "Audience", "profile · survey · findings", "audience"),
      ("07", "Ideas", "first ideas · moodboard", "ideas"), ("08", "Theory", "Barthes · Todorov · Propp · Lévi-Strauss", "theory"),
      ("09", "Planning", "treatment · script · storyboard", "planning"), ("10", "Pre-production", "locations · schedule · cast · risks", "preproduction"),
      ("11", "Production", "diary from the set", "production"), ("12", "The film", "rough cut · final cut", "final-cut"),
      ("13", "Evaluation", "looking back", "evaluation")]
new = old[:old.index('"items": [')] + '"items": [' + ', '.join('[%s]' % ', '.join('"%s"' % x for x in c) for c in ch) + ']'
n = s.count(old); s = s.replace(old, new)
eo, en = html.escape(old, quote=True), html.escape(new, quote=True); n2 = s.count(eo); s = s.replace(eo, en)
print('contents panels updated:', n, 'escaped:', n2); assert n
out = os.path.join(ROOT, 'Media_Studies_portfolio102.html')
open(out, 'w', encoding='utf-8').write(s); print(out, round(os.path.getsize(out) / 1e6, 2), 'MB')
