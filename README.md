# pravin.github.io

My projects page, live at https://pravin.github.io. Two browser games (Hollowmoon and EBB) sit side by side at the top, then a few hand-picked projects, then every other public repo.

- `index.html`: the whole site. The featured and selected projects are written by hand; "Everything else" is filled from `repos.json`.
- `assets/hollowmoon-art.svg`, `assets/ebb-art.svg`: artwork for the two game cards.
- `scripts/build_data.py`: fetches my public repos into `repos.json`.
- `scripts/build_stats.py`: counts my commits per year across all repos I own, public and private, into `stats.json` (totals only, no repo names).
- `.github/workflows/deploy.yml`: builds the data and deploys to GitHub Pages on every push and once a day. Private-repo stats refresh only if a `STATS_TOKEN` secret is set; otherwise the committed `stats.json` is used.

Local preview: `python3 -m http.server` and open http://localhost:8000. To refresh the commit stats by hand: `GITHUB_TOKEN=$(gh auth token) python3 scripts/build_stats.py pravin stats.json`.
