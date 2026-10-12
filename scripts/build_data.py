"""Fetch public repos for a GitHub user for the site.

Usage: GITHUB_TOKEN=... python3 scripts/build_data.py <user> <out.json>
"""
import json, os, sys, urllib.error, urllib.request

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN")

# Projects that predate GitHub: when work actually started (approximate).
STARTED = {"Yammy": "2003-01-01T00:00:00Z", "win32": "2003-01-01T00:00:00Z"}


def get(path):
    req = urllib.request.Request(API + path, headers={"Accept": "application/vnd.github+json"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise



def main(user, out):
    repos, page = [], 1
    while True:
        batch = get(f"/users/{user}/repos?type=owner&per_page=100&page={page}")
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    result = []
    for r in repos:
        if r["private"] or r["name"].lower() == f"{user}.github.io".lower():
            continue
        item = {k: r[k] for k in ("name", "html_url", "description", "homepage", "language", "topics", "fork",
                                  "archived", "stargazers_count", "forks_count", "created_at", "pushed_at", "license")}
        item["license"] = (r.get("license") or {}).get("spdx_id")
        if r["name"] in STARTED:
            item["started_at"] = STARTED[r["name"]]
        result.append(item)
        print(f"  {r['name']}", file=sys.stderr)
    with open(out, "w") as f:
        json.dump(result, f, separators=(",", ":"))
    print(f"Wrote {len(result)} repos to {out}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
