# Static-position star field as SVG; a subset fades smoothly via SMIL. Same 5px grid as the pixel art.
import sys, base64, numpy as np
OUT = sys.argv[1]
rng = np.random.default_rng(11)
H, W, PX = 120, 320, 5
fall = np.linspace(1, .1, H)[:, None]
m = rng.random((H, W)) < .0045*fall
ys, xs = np.nonzero(m)
parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W*PX}' height='{H*PX}' shape-rendering='crispEdges'>"]
DIM, MID, BRIGHT = '#96a6c8', '#d4dcec', '#f4f7fc'
for i, (y, x) in enumerate(zip(ys, xs)):
    r = f"<rect x='{x*PX}' y='{y*PX}' width='{PX}' height='{PX}' fill='{DIM}'"
    if rng.random() < .3:  # this star twinkles: smooth fade, own period and phase
        dur = rng.uniform(4.5, 9); lo = rng.uniform(.2, .45); beg = rng.uniform(0, dur)
        r += f"><animate attributeName='opacity' values='1;{lo:.2f};1' keyTimes='0;.5;1' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1' dur='{dur:.1f}s' begin='-{beg:.1f}s' repeatCount='indefinite'/></rect>"
    else: r += "/>"
    parts.append(r)
for _ in range(5):  # bright cross stars: fixed shape, only the core glow breathes
    y, x = int(rng.integers(3, 50)), int(rng.integers(3, W-3))
    for dy, dx in [(1,0),(-1,0),(0,1),(0,-1)]:
        parts.append(f"<rect x='{(x+dx)*PX}' y='{(y+dy)*PX}' width='{PX}' height='{PX}' fill='{DIM}' opacity='.8'/>")
    dur = rng.uniform(6, 10)
    parts.append(f"<rect x='{x*PX}' y='{y*PX}' width='{PX}' height='{PX}' fill='{BRIGHT}'><animate attributeName='opacity' values='1;.55;1' keyTimes='0;.5;1' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1' dur='{dur:.1f}s' begin='-{rng.uniform(0,dur):.1f}s' repeatCount='indefinite'/></rect>")
parts.append("</svg>")
svg = "".join(parts)
open(OUT + ".svg", "w").write(svg)
open(OUT + ".css", "w").write(":root{--bk-stars:url(data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode() + ")}\n")
print(len(svg), "svg bytes")
