# Squarespace "long version": the whole v104 page for pasting into one Code Block, with the ident video and poster
# loaded from jsDelivr instead of being written into the file (2.4 MB -> ~0.6 MB). Usage: python3 make_paste_v104.py
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = 'https://cdn.jsdelivr.net/gh/StefanSendyk/Raqueshi@3d6560e29457310520884b7038e5f15ea0e26c5b/media_photos_hq/v104/'
s = open(os.path.join(ROOT, 'Media_Studies_portfolio104.html'), encoding='utf-8').read()
s, a = re.subn(r'data:video/mp4;base64,[A-Za-z0-9+/=]+', B + 'stillhouse_logo_web.mp4', s)
s, b = re.subn(r'data:image/jpeg;base64,[A-Za-z0-9+/=]{50000,}', B + 'stillhouse_logo_poster.jpg', s); assert (a, b) == (1, 1), (a, b)
s = s.replace('Paste into ONE Squarespace Code Block', 'v104 (Final Project: blog checklist, case-file theme; Preliminary: sunset theme). Paste into ONE Squarespace Code Block', 1)
out = os.path.join(ROOT, 'squarespace', 'portfolio104_paste.html'); open(out, 'w', encoding='utf-8').write(s); print(out, round(len(s.encode()) / 1024), 'KB')
