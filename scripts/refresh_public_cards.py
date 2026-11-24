#!/usr/bin/env python3
"""Update only the six explicit public showcase cards. No private repo enumeration."""
import datetime as dt
import json
import os
import pathlib
import urllib.request
import xml.etree.ElementTree as ET

OWNER = "Neguchads"
ROOT = pathlib.Path(__file__).resolve().parents[1]
NAMES = ("chad-recomp", "cdos-nintendods-recomp", "ccod-xbox-recomp",
         "csotn-saturn-recomp", "starlight-bi", "spec-to-proof")
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def fetch(name):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Neguchads-profile-refresh",
               "X-GitHub-Api-Version": "2022-11-28"}
    # The workflow's repository-scoped token is optional; never persist it.
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    req = urllib.request.Request(f"https://api.github.com/repos/{OWNER}/{name}", headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)


def validate(data, name):
    if (data.get("private") is not False or data.get("visibility") != "public"
            or data.get("fork") is not False or data.get("archived") is not False
            or data.get("full_name", "").casefold() != f"{OWNER}/{name}".casefold()):
        raise ValueError("Showcase repository no longer meets public original eligibility.")
    values = tuple(data.get(key) for key in ("stargazers_count", "forks_count"))
    if any(type(n) is not int or n < 0 for n in values):
        raise ValueError("Invalid public counts.")
    return values


def render(path, stars, forks):
    root = ET.parse(path).getroot()
    nodes = {e.get("id"): e for e in root.iter() if e.get("id")}
    if nodes["stars"].text == str(stars) and nodes["forks"].text == str(forks):
        return None
    nodes["stars"].text = str(stars)
    nodes["forks"].text = str(forks)
    desc = nodes["desc"]
    prefix = (desc.text or "").split(". Snapshot ")[0]
    # Keep only the authored public description, not metadata from arbitrary API strings.
    prefix = prefix.rsplit(". ", 1)[0]
    desc.text = f"{prefix}. {stars} GitHub stars, {forks} forks. Snapshot {dt.datetime.now(dt.timezone.utc).date().isoformat()}."
    return ET.tostring(root, encoding="unicode") + "\n"


def main():
    updated = []
    for name in NAMES:
        stars, forks = validate(fetch(name), name)
        p = ROOT / "assets" / "projects" / (name + ".svg")
        content = render(p, stars, forks)
        if content is not None:
            updated.append((p, content))
    # If any query fails, no cards are replaced.
    for p, content in updated:
        p.write_text(content, encoding="utf-8")
    print(f"Updated {len(updated)} public cards.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError):
        raise SystemExit("Public showcase refresh failed; previous cards preserved.")
