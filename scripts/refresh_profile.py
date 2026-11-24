#!/usr/bin/env python3
"""Refresh only anonymized profile SVGs using your local authenticated GitHub CLI.

No repository names, private URLs, source files, tokens or raw API responses
are written to disk by this program. Review the aggregate changes before push.
"""
import argparse
import collections
import datetime as dt
import json
import pathlib
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ET

OWNER = "Neguchads"
ROOT = pathlib.Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def api(endpoint, paginate=False):
    args = ["gh", "api", "--hostname", "github.com"]
    if paginate:
        args += ["--paginate", "--slurp"]
    try:
        result = subprocess.run(args + [endpoint], check=True, capture_output=True, text=True, encoding="utf-8")
        return json.loads(result.stdout)
    except (OSError, subprocess.CalledProcessError, ValueError):
        raise RuntimeError("GitHub API request failed. Check your local authentication and read access.") from None


def count_items(kind):
    q = urllib.parse.urlencode({"q": f"is:{kind} author:{OWNER} user:{OWNER}", "per_page": 1})
    data = api("/search/issues?" + q)
    if data.get("incomplete_results") or not isinstance(data.get("total_count"), int):
        raise RuntimeError("Incomplete activity query; existing cards preserved.")
    return data["total_count"]


def collect(by_bytes):
    if api("/user").get("login", "").lower() != OWNER.lower():
        raise RuntimeError("Authenticate GitHub CLI as the profile owner.")
    pages = api("/user/repos?affiliation=owner&visibility=all&per_page=100", paginate=True)
    repos = [r for page in pages for r in page if r["owner"]["login"].lower() == OWNER.lower()
             and not r["fork"] and not r["archived"] and r["name"].lower() != OWNER.lower()]
    if not any(r["private"] for r in repos):
        raise RuntimeError("No private original repositories visible. Refusing to replace combined statistics with public-only data.")
    public = [r for r in repos if not r["private"]]
    langs = collections.Counter()
    detected = 0
    for r in repos:
        if by_bytes:
            name = urllib.parse.quote(r["name"], safe="")
            values = api(f"/repos/{OWNER}/{name}/languages")
            if not isinstance(values, dict) or any(not isinstance(v, int) or v < 0 for v in values.values()):
                raise RuntimeError("Invalid language response.")
            if sum(values.values()) > 0:
                detected += 1
                langs.update({k: v for k, v in values.items() if v > 0})
        elif r.get("language"):
            detected += 1
            langs[r["language"]] += 1
    if not langs:
        raise RuntimeError("No detected languages; existing cards preserved.")
    metrics = [len(repos), sum(r["stargazers_count"] for r in public),
               count_items("pr"), count_items("issue"), sum(r["forks_count"] for r in public)]
    return metrics, langs, detected


def render(path, metrics, langs, detected, by_bytes, pt):
    tree = ET.parse(path)
    root = tree.getroot()
    nodes = {e.attrib["id"]: e for e in root.iter() if "id" in e.attrib}
    for i, value in enumerate(metrics):
        nodes[f"metric{i}"].text = str(value)
    ranked = sorted(langs.items(), key=lambda item: (-item[1], item[0].casefold()))
    if len(ranked) > 8:
        ranked = ranked[:7] + [("Outras" if pt else "Other", sum(v for _, v in ranked[7:]))]
    total = sum(langs.values())
    for i in range(8):
        visible = i < len(ranked)
        name, n = ranked[i] if visible else ("", 0)
        nodes[f"row{i}"].set("visibility", "visible" if visible else "hidden")
        nodes[f"lang{i}"].text = name if len(name) <= 17 else name[:16] + "…"
        nodes[f"bar{i}"].set("width", f"{223*n/total:.2f}")
        nodes[f"pct{i}"].text = f"{100*n/total:.1f}%"
    nodes["method"].text = (
        ("Por bytes de código" if by_bytes else "Por projeto próprio") + " · públicos + privados"
        if pt else ("By code bytes" if by_bytes else "By original repository") + " · public + private"
    )
    nodes["coverage"].text = (
        f"{detected} projetos com linguagem identificada" if pt else f"{detected} projects with a detected language"
    )
    nodes["updated"].text = ("Atualizado: " if pt else "Updated: ") + dt.datetime.now(dt.timezone.utc).date().isoformat()
    return ET.tostring(root, encoding="unicode") + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--by-bytes", action="store_true", help="Use GitHub Linguist byte counts instead of primary language per repository.")
    args = parser.parse_args()
    metrics, langs, detected = collect(args.by_bytes)
    files = [(ROOT / "assets" / f"github-stats.{locale}.svg", locale == "pt-BR") for locale in ("en", "pt-BR")]
    rendered = [(p, render(p, metrics, langs, detected, args.by_bytes, pt)) for p, pt in files]
    for p, content in rendered:
        temp = p.with_suffix(".tmp")
        temp.write_text(content, encoding="utf-8")
        temp.replace(p)
    print("Updated both aggregate cards. Review git diff before committing. No private repository details exported.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, KeyError, TypeError, ValueError, ET.ParseError):
        print("Refresh failed; check GitHub CLI authentication, repository visibility and API access.", file=sys.stderr)
        sys.exit(1)
