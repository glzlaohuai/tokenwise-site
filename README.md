# Tokenly — Website

Marketing landing page, Privacy Policy, and Support pages for **Tokenly**, a local
token-usage tracker for AI coding tools (Claude Code / Codex / OpenCode / Gemini)
that lives in the macOS menu bar.

- **Live:** https://glzlaohuai.github.io/tokenwise-site/
- Privacy Policy — [`privacy.html`](privacy.html)
- Support / FAQ — [`support.html`](support.html)

## Structure

- `index.html` — landing page (hero, feature sections, privacy, footer)
- `privacy.html`, `support.html` — content pages
- `assets/styles.css`, `assets/app.js` — shared design system + language toggle
- `assets/{en,zh}/*.webp` — product screenshots per language
- `assets/og.png`, `assets/icon.png`, `assets/favicon.png` — share card & icons

Static HTML/CSS/JS with a client-side **EN / 中文** language toggle (defaults to
English, remembers your choice, never shows both languages at once). No framework,
no tracking, no runtime dependencies.

## Rebuilding image assets

Screenshots under `assets/` are generated from the app's raw screenshots:

```
python tools/build_assets.py --src /path/to/appstore/screenshots/raw
```

## Deploy

Hosted on GitHub Pages from `main`. Pushing to `main` redeploys automatically.

> After the app ships, replace the `idXXXXXXXXXX` placeholder in the “Download on the
> Mac App Store” links (search `apps.apple.com` in `index.html`) with the real URL.

Contact: 494763134@qq.com
