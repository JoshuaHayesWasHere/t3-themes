# Emits a CSS fragment: 16 moon-phase frames + 3 twinkle star maps (lowres, scaled 5x in CSS), and phase rules.
import sys, io, base64, numpy as np
from PIL import Image
OUT_CSS, PREVIEW = sys.argv[1], sys.argv[2]
rng = np.random.default_rng(11)
B4 = np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]) / 16 + 1/32
SILV = [(70,86,128),(150,166,200),(212,220,236),(244,247,252)]
EARTH = (16,28,64); HALO = (63,99,189)
def tile(h,w): return np.tile(B4,(h//4+1,w//4+1))[:h,:w]
def noise(n, scale):
    g = rng.random((n//scale+2, n//scale+2)); im = Image.fromarray((g*255).astype(np.uint8)).resize((n+scale, n+scale), Image.BICUBIC)
    return np.asarray(im, float)[:n,:n]/255
R, r = 60, 17; N = 2*R+1
y, x = np.mgrid[-R:R+1, -R:R+1]; d = np.hypot(x, y)
disc = d <= r
crater = 0.78 + 0.35*noise(N, 6)
shade = np.clip(0.62 + 0.38*(x/(1.4*r)), 0, 1)*crater          # light from the right (waxing)
for cx, cy, cr in [(-6,-4,4),(5,3,5),(-2,8,3),(8,-7,2.5)]: shade -= 0.22*np.exp(-((x-cx)**2+(y-cy)**2)/cr**2)
T = tile(N, N)
def b64png(rgba):
    buf = io.BytesIO(); Image.fromarray(rgba,'RGBA').save(buf,'PNG',optimize=True); return base64.b64encode(buf.getvalue()).decode()
frames = []
PH = 16
for k in range(PH):
    f = k/(PH-1)
    rgba = np.zeros((N,N,4), np.uint8)
    hv = np.clip((R-d)/(R-r),0,1)**2.2*(0.08+0.40*f); hv[disc] = 0
    hm = hv > T; rgba[hm,:3] = HALO; rgba[hm,3] = 200
    kk = 1-2*f; lit = disc & (x >= kk*np.sqrt(np.clip(r*r - y*y, 0, None)))
    rgba[disc,:3] = EARTH; rgba[disc,3] = 255                     # earthshine disc, occludes stars
    e = disc & ~lit & (0.10 > T); rgba[e,:3] = (28,44,92)
    q = np.clip(np.floor(np.clip(shade,.05,1)*len(SILV) + T - 1), -1, len(SILV)-1).astype(int)
    for i,c in enumerate(SILV): m = lit & (q==i); rgba[m,:3] = c
    frames.append(rgba)
# stars: 320x120 lowres map, density fading downward; 3 variants for twinkle
H, W = 120, 320
base = np.zeros((H,W), int); fall = np.linspace(1,.1,H)[:,None]
base[rng.random((H,W)) < .0045*fall] = 1
ys, xs = np.nonzero(base); tw = rng.choice(len(ys), size=max(6,len(ys)//5), replace=False)
bright = [(rng.integers(3,50), rng.integers(3,W-3)) for _ in range(5)]
def starmap(v):
    rgba = np.zeros((H,W,4),np.uint8)
    for i,(yy,xx) in enumerate(zip(ys,xs)):
        on = not (i in tw and (i+v) % 3 == 0); dim = i in tw and (i+v) % 3 == 1
        if on: rgba[yy,xx] = (*(SILV[0] if dim else SILV[1]),255)
    for j,(yy,xx) in enumerate(bright):
        big = (j+v) % 3 != 0
        rgba[yy,xx] = (*SILV[3],255)
        if big:
            for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]: rgba[yy+dy,xx+dx] = (*SILV[1],255)
    return rgba
stars = [starmap(v) for v in range(3)]
css = [":root{" + "".join(f"--bk-m{k}:url(data:image/png;base64,{b64png(fr)});" for k,fr in enumerate(frames))
       + "".join(f"--bk-s{v}:url(data:image/png;base64,{b64png(s)});" for v,s in enumerate(stars)) + "}"]
TICK = 30
for k in range(PH-1):
    us = [u for u in range(TICK) if round(u/TICK*(PH-1)) == k]
    if us: css.append("html:has(" + ",".join(f'[aria-label="Context: {u}% used"]' for u in us) + "){--bk-moon:var(--bk-m%d)}" % k)
open(OUT_CSS,'w').write("\n".join(css)+"\n")
# preview strip of all phases
strip = Image.new('RGBA', (N*8, N*2), (2,5,15,255))
for k,fr in enumerate(frames): strip.alpha_composite(Image.fromarray(fr,'RGBA'), ((k%8)*N, (k//8)*N))
strip.resize((strip.width*2, strip.height*2), Image.NEAREST).convert('RGB').save(PREVIEW)
print(len("\n".join(css)), "chars")
