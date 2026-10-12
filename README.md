# pravin.github.io

A single-page showcase of my public GitHub repositories, live at https://pravin.github.io.

- `index.html` — the whole site (three switchable looks: Paper, Terminal, Blueprint).
- `.github/workflows/deploy.yml` — fetches the repo list into `repos.json` and deploys to GitHub Pages on every push and once a day.

Local preview: `python3 -m http.server` and open http://localhost:8000 (falls back to the live GitHub API when `repos.json` is absent).
