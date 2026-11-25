#!/usr/bin/env python3
"""Publish reviewed generated public assets on the latest main; never force push."""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
try:
    from .showcase import load
except ImportError:  # direct CLI execution
    from showcase import load
FEATURED = load()
LEGACY_FEATURED = ("cdos-nintendods-recomp", "csotn-saturn-recomp", "starlight-bi")
FILES = ("index.html", "abyss.html", "ABYSS-LICENSE.txt", "snapshot.json",
         "universe.en.svg", "universe.pt-BR.svg", "assets/banner.svg")
INPUTS = ("scripts", "docs/universe-pins.json", "docs/showcase.json", "docs/universe/snapshot.json",
          "assets/banner.svg", "assets/projects", ".github/workflows/navi-universe.yml")

def git(root, *args, check=True, capture=False):
    return subprocess.run(["git", "-C", str(root), *args], check=check,
                          text=True, capture_output=capture)

def validate(bundle):
    data = json.loads((bundle / "snapshot.json").read_text(encoding="utf-8"))
    if data.get("owner") != "Neguchads" or data.get("scope") != "public-only" or data.get("schema_version") != 1:
        raise ValueError("Invalid public snapshot")
    source = data["sources"]["Neguchads"]
    if not re.fullmatch(r"[0-9a-f]{40}", source):
        raise ValueError("Invalid snapshot source")
    featured = data["featured"]
    if not isinstance(featured, list) or len(featured) != len(set(featured)) or not set(featured) <= set(FEATURED) or featured != [s for s in FEATURED if s in featured]:
        raise ValueError("Invalid featured catalog")
    paths = [*FILES, *("assets/projects/"+s+".svg" for s in featured)]
    for path in paths:
        item = bundle / path
        if not item.is_file() or item.is_symlink() or not item.resolve().is_relative_to(bundle):
            raise ValueError("Missing or unsafe artifact path: "+path)
    return source, paths, featured

def check_fresh(root, source, bundle):
    git(root, "merge-base", "--is-ancestor", source, "HEAD")
    previous = root / "docs/universe/snapshot.json"
    same_snapshot = previous.is_file() and previous.read_bytes() == (bundle / "snapshot.json").read_bytes()
    if same_snapshot:
        # An already-published artifact must never overwrite a newer manual edit.
        return False
    result = git(root, "diff", "--quiet", source, "HEAD", "--", *INPUTS, check=False)
    if result.returncode != 0:
        raise RuntimeError("Build inputs or published snapshot changed; start a new workflow on main.")
    return True

def apply(root, bundle, paths, featured):
    for rel in paths:
        dest = root / "docs/universe" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(bundle / rel, dest)
    # Remove only obsolete generated project images from the published bundle.
    directory = root / "docs/universe/assets/projects"
    if directory.is_dir():
        for slug in (set(FEATURED) | set(LEGACY_FEATURED)) - set(featured):
            (directory / (slug+".svg")).unlink(missing_ok=True)
    for rel in ("universe.en.svg", "universe.pt-BR.svg", *("assets/projects/"+s+".svg" for s in featured)):
        dest = root / "assets" / (rel.removeprefix("assets/"))
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(bundle / rel, dest)
    git(root, "add", "--", "docs/universe", "assets/universe.en.svg", "assets/universe.pt-BR.svg", "assets/projects")

def publish(root, bundle, attempts=4):
    root, bundle = root.resolve(), bundle.resolve()
    source, paths, featured = validate(bundle)
    if git(root, "status", "--porcelain", capture=True).stdout:
        raise RuntimeError("Publication requires a clean checkout")
    git(root, "config", "user.name", "github-actions[bot]")
    git(root, "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    for attempt in range(attempts):
        git(root, "fetch", "origin", "refs/heads/main:refs/remotes/origin/main")
        git(root, "checkout", "--detach", "refs/remotes/origin/main")
        if not check_fresh(root, source, bundle):
            print("This snapshot is already published; no changes required.")
            return
        apply(root, bundle, paths, featured)
        if git(root, "diff", "--cached", "--quiet", check=False).returncode == 0:
            print("No generated changes.")
            return
        git(root, "commit", "-m", "docs: publish daily NAVI Universe snapshot")
        if git(root, "push", "origin", "HEAD:refs/heads/main", check=False).returncode == 0:
            return
        if attempt+1 < attempts:
            print("Push failed; fetching latest main and retrying without force.")
            time.sleep(2*(attempt+1))
    raise RuntimeError("Could not publish after bounded retries; no force push attempted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=pathlib.Path)
    args = parser.parse_args()
    publish(ROOT, args.bundle)
