#!/usr/bin/env bash
# Build the Brave Kitty theme from src/css.tmpl into dist/, and with --install
# copy it into T3 Code's themes folder. Reload T3 (or re-pick the theme) after installing.
set -euo pipefail
cd "$(dirname "$0")"
id=bk-navy-silver label="Blade Silver" hex="#d4dcec" surf="#1f2840" fg="#eef2fa"
tmp=$(mktemp); trap 'rm -f "$tmp"' EXIT
sed "s/__HEX__/$hex/" src/css.tmpl > "$tmp"
jq --arg n "Brave Kitty · Navy · $label" --arg a "$hex" --arg s "$surf" --arg f "$fg" --rawfile css "$tmp" \
  '.name=$n | .accent=$a | .css=$css | .colors += {accent:$a,focus:$a,accentSurface:$s,accentSurfaceForeground:$f,searchMatchActiveBackground:$a,terminalCursor:$a,sidebarRowSelected:$s}' \
  src/navy_base.json > "dist/$id.json"
cp assets/navy_flop.webp "dist/$id.webp"
echo "built dist/$id.json"
if [[ ${1:-} == --install ]]; then
  td="$HOME/.t3/userdata/themes"
  cp "dist/$id.json" "dist/$id.webp" "$td/"
  echo "installed to $td"
fi
