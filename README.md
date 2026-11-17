# Brave Kitty theme

A T3 Code theme built from `assets/braveKitty.gif`: a deep navy night with a dithered pixel cat, faint pixel rain, twinkling stars and a moon that fills with the thread's context window (full at the 30% mark). The message column sits on soft glass; the accent is Blade Silver.

- `src/css.tmpl`: the theme CSS. `__HEX__` is the accent colour.
- `src/navy_base.json`: the theme's colour roles.
- `assets/navy_flop.webp`: the background cat (becomes `<id>.webp` next to the theme).
- `tools/moon.py`, `tools/stars_svg.py`: generators for the moon-phase and star CSS already inlined in the template.
- `dist/`: the built theme as T3 loads it.

Build: `./build.sh`. Build and install: `./build.sh --install`, then pick "Brave Kitty · Navy · Blade Silver" in T3 settings (or reload if it is already active).

Regenerate decorations: `uv run --no-project --with numpy --with pillow python -I tools/moon.py moon.css moon.png` and `... tools/stars_svg.py stars`, then paste the output over the matching `:root{--bk-m…}` / `--bk-stars` rules in the template.
