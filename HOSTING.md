# Hosting this site

Upload this directory to Netlify, Cloudflare Pages, or GitHub Pages. It is a static site with no build step.

- Netlify publish directory: `website`
- Cloudflare Pages output directory: `website`
- GitHub Pages: use the repository workflow in `.github/workflows/pages.yml`

For local preview: `python3 -m http.server 8000 --directory website`.
