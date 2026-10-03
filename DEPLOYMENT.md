# DT lll external hosting

The site is a static, zero-dependency website. The deployable directory is `website/`; it contains HTML, CSS, JavaScript, Markdown docs, the route manifest, and no server-side code.

## Netlify

Create a new site from this project repository and use:

- Build command: leave empty
- Publish directory: `website`

The included `netlify.toml` already declares these settings. You can also drag the `website/` directory into Netlify Drop for a quick deployment.

## GitHub Pages

Push the project to a GitHub repository. The included workflow at `.github/workflows/pages.yml` publishes the `website/` directory whenever the `main` branch changes.

In the repository settings, open **Pages** and select **GitHub Actions** as the source. GitHub will then provide the permanent `github.io` URL. A custom domain can be added later in the Pages settings.

## Cloudflare Pages

Create a Pages project connected to the repository and use:

- Framework preset: None
- Build command: leave empty
- Output directory: `website`

The site needs no Node.js build step. Cloudflare Pages can supply a permanent `pages.dev` URL and can connect a custom domain.

## Local preview

```bash
python3 -m http.server 8000 --directory website
```

The demo chat is intentionally labeled simulated. It does not call the trained checkpoint. To make it live, add a backend endpoint that invokes `model/infer.py` or a separately hosted inference service; do not put model execution secrets in browser JavaScript.
