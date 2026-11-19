# Builds Max_Media_Studies_portfolio5.html from v4: new Final Project page with Max's pre-production research.
#   python3 build_max_v5.py
import base64, io, os, re, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'Max_Media_Studies_portfolio4.html')
OUT = os.path.join(ROOT, 'Max_Media_Studies_portfolio5.html')
MEDIA = os.path.join(ROOT, 'max_final_media')

def jpeg_uri(path, width=1100, q=84):
    im = Image.open(path).convert('RGB')
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

imgs = {os.path.splitext(f)[0]: os.path.join(MEDIA, f) for f in os.listdir(MEDIA) if f.endswith('.png')}
imgs['mm_logo_polished'] = os.path.join(HERE, 'mm_logo.png')

body = open(os.path.join(HERE, 'final_page_body.html'), encoding='utf-8').read()
def img_sub(m):
    name = m.group(1)
    return jpeg_uri(imgs[name], 1600 if name == 'mm_logo_polished' else 1100)
body = re.sub(r'\{img:(\w+)\}', img_sub, body)
vid = 'data:video/mp4;base64,' + base64.b64encode(open(os.path.join(HERE, 'mm_logo_ident_web.mp4'), 'rb').read()).decode()
body = body.replace('{vid:ident}', vid)
assert '{img:' not in body and '{vid:' not in body

css = open(os.path.join(HERE, 'final_page_extra.css'), encoding='utf-8').read()
js = """
<script>
  // the logo ident is stored inside the page: turn it into a playable file, click toggles sound
  document.querySelectorAll('video[data-inline]').forEach(function (v) {
    fetch(v.getAttribute('data-inline')).then(function (r) { return r.blob(); }).then(function (b) {
      v.src = URL.createObjectURL(b); v.play().catch(function () {});
    });
    v.addEventListener('click', function () { v.muted = !v.muted; if (!v.muted) { v.currentTime = 0; v.play(); } });
  });
<\\/script>
"""

s = open(SRC, encoding='utf-8').read()
start = s.index('<script type="text/plain" id="mm-page-final">')
end = s.index('</html>\n</script>', start)
page = s[start:end]

# 1) extra styles at the end of the page's <style>
i = page.rindex('</style>')
page = page[:i] + css + page[i:]
# 2) replace hero ... end of .body with the new content
a = page.index('<header class="hero">')
b = page.index('</main>\n</div>', a) + len('</main>\n</div>')
page = page[:a] + body.strip() + js + page[b:]
assert '</script>' not in page.replace('<\\/script>', ''), 'unescaped </script> inside the page block'

s = s[:start] + page + s[end:]
s = s.replace('<title>Final Project — Maximilian Matuzani</title>', '<title>Spectrophobia — Final Project — Maximilian Matuzani</title>')
open(OUT, 'w', encoding='utf-8').write(s)
print(OUT, round(os.path.getsize(OUT) / 1e6, 2), 'MB')
