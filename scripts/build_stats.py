"""Aggregate commit counts by year across every repo the user owns, public and private.

Only totals are written out: no repo names or other details from private repos.

Usage: GITHUB_TOKEN=... python3 scripts/build_stats.py <user> <out.json>
The token needs read access to private repos (a fine-grained token with Metadata + Contents read).
"""
import collections, datetime, json, os, sys, urllib.error, urllib.request

API = "https://api.github.com"
TOKEN = os.environ["GITHUB_TOKEN"]


def get(path):
    req = urllib.request.Request(API + path, headers={"Authorization": f"Bearer {TOKEN}",
                                                      "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 409:  # empty repo
            return []
        raise


def paged(path):
    page = 1
    while True:
        batch = get(f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}")
        yield from batch
        if len(batch) < 100:
            return
        page += 1


def main(user, out):
    years = collections.defaultdict(lambda: {"commits": 0, "repos": set()})
    counted = {"public": 0, "private": 0}
    for r in paged("/user/repos?affiliation=owner&visibility=all"):
        if r["fork"]:
            continue
        # Commits on the default branch authored by the user, dated by when they were written.
        commits = list(paged(f"/repos/{r['full_name']}/commits?author={user}"))
        if not commits:
            continue
        counted["private" if r["private"] else "public"] += 1
        for c in commits:
            y = years[int(c["commit"]["author"]["date"][:4])]
            y["commits"] += 1
            y["repos"].add(r["id"])
    by_year = {str(y): {"commits": d["commits"], "repos": len(d["repos"])} for y, d in sorted(years.items())}
    result = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "repos": counted,
        "totals": {"commits": sum(d["commits"] for d in by_year.values())},
        "by_year": by_year,
    }
    with open(out, "w") as f:
        json.dump(result, f, indent=1)
    print(result["totals"], result["repos"], file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
