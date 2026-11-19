# M&M Productions: polished logo still + 5 s animated ident (1920x1080, 24 fps, with sound)
#   ~/animation-tools/bin/python make_mm_logo.py            -> mm_logo.png, mm_logo_ident.mp4, mm_logo_ident_web.mp4
# Based on Max Matuzani's design: classic serif "M&M", spaced "PRODUCTIONS", thin rule, a red blood line and drop.
import os, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', 'Cinzel.ttf')
W, H, FPS, DUR = 1920, 1080, 24, 5.0
SS = 2                                  # layers are drawn at 2x and scaled down per frame
rng = np.random.default_rng(13)

def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([weight])
    return f

def smooth(a, b, t):
    x = min(max((t - a) / (b - a), 0.0), 1.0)
    return x * x * (3 - 2 * x)

def ease_out(a, b, t):
    x = min(max((t - a) / (b - a), 0.0), 1.0)
    return 1 - (1 - x) ** 3

# ------------------------------------------------------------------ layers (2x)
CW, CH = W * SS, H * SS
CX = CW // 2

def text_mask(text, f, spacing=0.0):
    """Grey mask of text with extra letter spacing (in px), centred at x=0; returns (img, width, ascent offset)."""
    widths = [f.getlength(ch) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    asc, desc = f.getmetrics()
    m = Image.new('L', (int(total) + 40, asc + desc + 40), 0)
    d = ImageDraw.Draw(m)
    x = 20
    for ch, w in zip(text, widths):
        d.text((x, 20), ch, font=f, fill=255)
        x += w + spacing
    return m

def fractal(w, h, octaves=6, base=6, persist=0.55, seed=0):
    r = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32); amp = 1.0; tot = 0.0
    for o in range(octaves):
        res = base * 2 ** o
        g = r.random((res + 1, int(res * w / h) + 2)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        acc += amp * np.asarray(im, np.float32) / 255; tot += amp; amp *= persist
    return acc / tot

# "M&M"
f_mm = font(300 * SS, 640)
mm_mask = text_mask('M&M', f_mm, spacing=-6 * SS)
bbox = mm_mask.getbbox(); mm_mask = mm_mask.crop(bbox)
MM_Y = int(330 * SS)                                        # top of the letters (2x)
mm_w, mm_h = mm_mask.size
mm_x = CX - mm_w // 2

# weathered stone / pewter surface for the letters
tex = fractal(mm_w, mm_h, 7, 5, seed=3)
pits = np.clip((fractal(mm_w, mm_h, 5, 40, 0.6, seed=9) - 0.66) * 5, 0, 1)     # small worn spots
grad = np.linspace(1.08, 0.72, mm_h, dtype=np.float32)[:, None]                  # lit from above
base = np.array([0.80, 0.76, 0.70], np.float32)                                 # warm silver-stone
shade = grad * (0.74 + 0.30 * tex) * (1 - 0.14 * pits)
mm_rgb = np.clip(base[None, None, :] * shade[..., None], 0, 1)
# soft inner edge darkening so the letters read as carved
m = np.asarray(mm_mask, np.float32) / 255
edge = np.asarray(mm_mask.filter(ImageFilter.GaussianBlur(3 * SS)), np.float32) / 255
mm_rgb *= (0.75 + 0.25 * np.clip(edge * 1.4 - 0.2, 0, 1))[..., None]
mm_alpha = m

# "PRODUCTIONS" + rule
f_pr = font(46 * SS, 430)
PR_TOP = MM_Y + mm_h + int(58 * SS)
letters = list('PRODUCTIONS')
pr_masks = []
for ch in letters:
    lm = Image.new('L', (int(f_pr.getlength(ch)) + 20, 46 * SS * 2), 0)
    ImageDraw.Draw(lm).text((10, 10), ch, font=f_pr, fill=255)
    pr_masks.append(lm)
pr_adv = [f_pr.getlength(ch) for ch in letters]
RULE_Y = PR_TOP + int(84 * SS)
RULE_HALF = int(370 * SS)
PR_COL = np.array([0.80, 0.77, 0.72], np.float32)

# blood line + drop
LINE_TOP = int(120 * SS)
LINE_BOT = RULE_Y + int(14 * SS)
RED_DARK = np.array([0.30, 0.012, 0.018], np.float32)
RED = np.array([0.66, 0.035, 0.045], np.float32)

# ------------------------------------------------------------------ frame
grain_bank = [rng.normal(0, 1, (H, W)).astype(np.float32) for _ in range(8)]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
vignette = 1 - 0.55 * np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.70)) ** 2, 0, 1)

def paste(canvas, rgb, alpha, x, y):
    h, w = alpha.shape
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, canvas.shape[1]), min(y + h, canvas.shape[0])
    if x1 <= x0 or y1 <= y0:
        return
    a = alpha[y0 - y:y1 - y, x0 - x:x1 - x][..., None]
    src = rgb[y0 - y:y1 - y, x0 - x:x1 - x] if rgb.ndim == 3 else rgb
    canvas[y0:y1, x0:x1] = canvas[y0:y1, x0:x1] * (1 - a) + src * a

def render(t, still=False):
    big = np.zeros((CH, CW, 3), np.float32)

    # --- M&M: rises out of the dark, unblurs, with a slow light sweep
    a_mm = 1.0 if still else smooth(0.30, 1.7, t)
    blur = 0 if still else 16 * (1 - ease_out(0.30, 1.9, t))
    rgb = mm_rgb.copy()
    if not still:
        sweep_x = -0.3 + 1.6 * smooth(1.0, 3.2, t)                # band travels left to right
        u = np.linspace(0, 1, mm_w, dtype=np.float32)[None, :] + np.linspace(0, 0.25, mm_h, dtype=np.float32)[:, None]
        band = np.exp(-((u - sweep_x) / 0.07) ** 2) * 0.55
        rgb = np.clip(rgb * (1 + band[..., None]), 0, 1.2)
    alpha = mm_alpha
    if blur > 0.3:
        am = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur * SS))
        alpha = np.asarray(am, np.float32) / 255
        rgb = np.stack([np.asarray(Image.fromarray((np.clip(rgb[..., k], 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur * SS)), np.float32) / 255 for k in range(3)], -1)
    paste(big, rgb, alpha * a_mm, mm_x, MM_Y)

    # --- PRODUCTIONS: letters come in from the centre outwards, tracking settles
    track = (0.62 if still else 0.62 + 0.30 * (1 - ease_out(2.2, 3.6, t))) * 46 * SS
    total = sum(pr_adv) + track * (len(letters) - 1)
    x = CX - total / 2
    for i, (ch, lm, adv) in enumerate(zip(letters, pr_masks, pr_adv)):
        dist = abs(i - (len(letters) - 1) / 2)
        a = 1.0 if still else smooth(2.25 + 0.06 * dist, 2.85 + 0.06 * dist, t)
        if a > 0:
            la = np.asarray(lm, np.float32) / 255 * a
            paste(big, PR_COL, la, int(x) - 10, PR_TOP - 10)
        x += adv + track

    # --- rule under PRODUCTIONS, drawn outwards from the centre, gap for the blood line
    k = 1.0 if still else ease_out(2.5, 3.5, t)
    if k > 0:
        half = int(RULE_HALF * k)
        rule = np.zeros((4 * SS, 2 * half + 1), np.float32)
        rule[SS:3 * SS, :] = 1
        fade = np.minimum(1, (half - np.abs(np.arange(-half, half + 1))) / (90 * SS) + 0.02)[None, :]
        gap = np.abs(np.arange(-half, half + 1))[None, :] > 16 * SS
        paste(big, PR_COL * 0.85, rule * fade * gap * 0.85, CX - half, RULE_Y)

    # --- blood line: runs down from the top, then a drop gathers and hangs at the bottom
    p = 1.0 if still else smooth(1.25, 2.35, t)
    if p > 0:
        y_end = int(LINE_TOP + (LINE_BOT - LINE_TOP) * p)
        n = y_end - LINE_TOP
        ys = np.arange(n, dtype=np.float32)
        width = (1.6 + 0.9 * (ys / max(n, 1)) ** 2) * SS                     # thickens as it runs
        col = RED_DARK + (RED - RED_DARK) * (0.4 + 0.6 * (ys / max(n, 1)))[:, None]
        top_fade = np.clip(ys / (140 * SS), 0, 1)[:, None]
        wmax = int(width.max()) + 3
        xs = np.arange(-wmax, wmax + 1, dtype=np.float32)[None, :]
        a = np.clip(width[:, None] / 2 + 0.5 - np.abs(xs), 0, 1) * top_fade
        paste(big, np.repeat(col[:, None, :], a.shape[1], 1), a, CX - wmax, LINE_TOP)
        d = 1.0 if still else ease_out(2.30, 3.0, t)                         # the drop swells at the tip
        if d > 0:
            r = 8.5 * SS * d
            sag = (6 * SS * smooth(3.0, 4.4, t)) if not still else 3 * SS     # slowly stretches downwards
            cy = y_end + r * 0.9 + sag
            R = int(r * 2 + sag + 8)
            gy, gx = np.mgrid[-R:R + 1, -R:R + 1].astype(np.float32)
            # teardrop: circle plus a cone towards the line above it
            circ = np.clip(r + 0.6 - np.hypot(gx, gy), 0, 1)
            cone_w = r * np.clip((gy + r * 2.2 + sag) / (r * 2.2 + sag), 0, 1)
            cone = np.clip(cone_w + 0.6 - np.abs(gx), 0, 1) * (gy < 0) * (gy > -(r * 2.2 + sag))
            da = np.maximum(circ, cone)
            shine = np.exp(-(((gx + r * 0.35) / (r * 0.28 + 1e-3)) ** 2 + ((gy + r * 0.35) / (r * 0.22 + 1e-3)) ** 2)) * 0.45
            drgb = np.clip(RED[None, None, :] * (0.85 + 0.3 * (gy / (r + 1e-3)))[..., None] + shine[..., None], 0, 1)
            paste(big, drgb, da, CX - R, int(cy) - R)

    # --- down to 1080p, slow push-in, grain, vignette, fade out
    scale = 1.0 if still else 1.065 - 0.065 * ease_out(0.0, 5.0, t)
    img = Image.fromarray((np.clip(big, 0, 1) * 255).astype(np.uint8))
    sw, sh = int(W * scale), int(H * scale)
    img = img.resize((sw, sh), Image.LANCZOS).crop(((sw - W) // 2, (sh - H) // 2, (sw - W) // 2 + W, (sh - H) // 2 + H))
    out = np.asarray(img, np.float32) / 255
    glow = np.asarray(img.filter(ImageFilter.GaussianBlur(18)), np.float32) / 255
    out = out + 0.18 * glow                                                  # gentle halation
    out *= vignette[..., None]
    if not still:
        out *= 1 - smooth(4.45, 5.0, t)
        out += grain_bank[int(t * FPS) % len(grain_bank)][..., None] * 0.010
        out *= 1 - 0.025 * (math.sin(t * 37.0) * math.sin(t * 11.0) > 0.7)   # faint projector flicker
    return np.clip(out, 0, 1)

# ------------------------------------------------------------------ sound
def make_sound(path, sr=48000):
    n = int(sr * DUR); t = np.arange(n) / sr
    env = lambda a, b: np.clip((t - a) / (b - a), 0, 1)
    out = np.zeros((n, 2), np.float32)
    # low drone that swells into the blood line and then dies away
    drone = (np.sin(2 * np.pi * 41 * t) + 0.6 * np.sin(2 * np.pi * 61.7 * t + 0.4) + 0.3 * np.sin(2 * np.pi * 82.3 * t))
    noise = np.convolve(rng.normal(0, 1, n), np.ones(220) / 220, 'same')
    dr = (0.16 * drone + 0.5 * noise) * (env(0.0, 1.6) ** 2) * (1 - env(3.4, 5.0)) ** 1.5
    out += dr[:, None]
    # rising breath into the hit
    rise = np.convolve(rng.normal(0, 1, n), np.ones(30) / 30, 'same') * env(0.6, 1.55) ** 3 * (t < 1.55)
    out[:, 0] += 0.22 * rise; out[:, 1] += 0.22 * np.roll(rise, 90)
    # low impact when the line starts to run
    th = np.clip(t - 1.55, 0, None)
    hit = (np.sin(2 * np.pi * (48 * th - 20 * th ** 2)) * np.exp(-th * 2.6) + 0.4 * rng.normal(0, 1, n) * np.exp(-th * 30)) * (t >= 1.55)
    out += 0.55 * hit[:, None]
    # the drip, with a short room echo
    for k, (delay, g) in enumerate([(0, 1.0), (0.11, 0.35), (0.23, 0.16), (0.37, 0.08)]):
        td = np.clip(t - 2.62 - delay, 0, None)
        f = 1450 - 700 * (1 - np.exp(-td * 40))
        drip = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-td * 32) * (t >= 2.62 + delay) * g
        out[:, k % 2] += 0.28 * drip; out[:, 1 - k % 2] += 0.18 * drip
    out *= (1 - env(4.5, 5.0))[:, None]
    out /= max(1e-6, np.abs(out).max()) / 0.85
    pcm = (out * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

if __name__ == '__main__':
    import sys
    os.makedirs(os.path.join(HERE, 'frames'), exist_ok=True)
    Image.fromarray((render(0, still=True) * 255).astype(np.uint8)).save(os.path.join(HERE, 'mm_logo.png'))
    print('still done')
    if '--still' in sys.argv:
        raise SystemExit
    for i in range(0 if '--sound-only' in sys.argv else int(DUR * FPS)):
        Image.fromarray((render(i / FPS) * 255).astype(np.uint8)).save(os.path.join(HERE, 'frames', f'f{i:04d}.png'))
    make_sound(os.path.join(HERE, 'mm_logo_sound.wav'))
    fr = os.path.join(HERE, 'frames', 'f%04d.png')
    snd = os.path.join(HERE, 'mm_logo_sound.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', fr, '-i', snd,
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k',
                    '-movflags', '+faststart', os.path.join(HERE, 'mm_logo_ident.mp4')], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', fr, '-i', snd,
                    '-vf', 'scale=1280:720:flags=lanczos', '-c:v', 'libx264', '-preset', 'slow', '-crf', '24', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', os.path.join(HERE, 'mm_logo_ident_web.mp4')], check=True)
    print('video done')
