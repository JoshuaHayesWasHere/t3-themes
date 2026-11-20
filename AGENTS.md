# brave-kitty-theme

The Brave Kitty theme for T3 Code (navy night, pixel cat, stars, a moon that fills with context usage, Blade Silver accent). `build.sh` turns `src/css.tmpl` and `src/navy_base.json` into `dist/bk-navy-silver.json` plus its `.webp` background. `README.md` says what each source file is.

## Commands

| What | Command |
|---|---|
| Build, and confirm the committed `dist/` matches | `./build.sh && git diff --exit-code dist/` |
| Check T3 accepts the theme, without touching live T3 | `d=$(mktemp -d) && mkdir -p "$d/userdata/themes" && cp dist/* "$d/userdata/themes/" && (cd ~/repos/t3-fork/apps/server && node src/bin.ts theme show --base-dir "$d")` (it must list `bk-navy-silver` under Published themes; an invalid file is only a warning and the command still exits 0) |
| Regenerate the moon frames | `out=$(mktemp -d) && uv run --no-project --with numpy --with pillow python -I tools/moon.py "$out/moon.css" "$out/moon.png"` |
| Regenerate the stars | `out=$(mktemp -d) && uv run --no-project --with numpy --with pillow python -I tools/stars_svg.py "$out/stars"` |
| Install into live T3 | `./build.sh --install` (copies into `~/.t3/userdata/themes`; only when the owner asks) |

Generated CSS is pasted by hand over the matching `:root{--bk-m...}` or `--bk-stars` rules in `src/css.tmpl`. Write generator output outside the repo.

## How T3 picks it up

- The T3 fork (`~/repos/t3-fork`) carries this repo as the `themes/brave-kitty` submodule. Its `t3-fork sync` moves the submodule to this repo's `main` and pushes the bump; `t3-fork build` (and so `apply`) copies the committed `dist/*.json` and `dist/*.webp` into `~/.t3/userdata/themes`. They never run `build.sh`, so every change to `src/` ships with a rebuilt, committed `dist/`.
- `~/.t3/userdata/themes` is the owner's live T3 Code. Do not install, select or delete themes there unless asked. It also holds `bk-navy-periwinkle`, which this repo does not build; leave it alone.
- The CSS keys off T3's own markup (`[data-chat-canvas]` lane insets, `[data-draft-hero]`, `[data-workspace-area]`, the context bar's `aria-valuenow`). T3 changes its markup without notice; that is how the moon once stopped following context usage. When something stops matching, read the current markup in `~/repos/t3-fork/apps/web` and fix the selector here; it is a theme change, not a fork change, unless the fork exposes nothing to key off.

## Proving a visual change

Check it in a headless T3 web dev server from a t3-fork worktree, with the built theme copied into that worktree's `.t3/userdata/themes` (the fork's `AGENTS.md`, "Dev servers", covers starting and stopping it). Screenshot the affected screens before and after: a thread with messages, a new thread, the new-tab launcher, and home. Attach the shots to the reply and stop the dev server when done.

## Commits and PRs

Conventional subjects with no scope, saying what the user now sees, for example `fix: glass column follows the chat lane when panels push it off-centre`. A body explains the T3 markup the change relies on. PRs are rebase-merged into `main`. There is no CI.

## Done means

End every task by saying: committed, pushed, merged, whether `dist/` was rebuilt, and whether the fork's submodule was bumped or the theme installed into live T3. Remove worktrees, branches and dev servers you created once their work has merged.
