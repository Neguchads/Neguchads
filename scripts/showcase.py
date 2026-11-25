"""Profile-owned showcase contract and public-only compatibility bridge."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALIASES = {"github-homepage": "navi-githomepage", "navyv-abyss": "navi-abyss"}
ADDITIONS = {
    "navi-core": ("NAVI Engineering Core", False),
    "navi-githomepage": ("NAVI GitHomepage", True),
    "navi-abyss": ("NAVI Abyss", True),
}
RELATIONSHIPS = (
    ("navi-graphify", "navi-githomepage", "catalog-provider"),
    ("navi-githomepage", "Neguchads", "visualization-provider"),
    ("Neguchads", "navi-graphify", "project-discovery"),
    ("navi-abyss", "navi-githomepage", "immersive-theme-provider"),
    ("Neguchads", "navi-abyss", "public-experience-publisher"),
)

def load(root=ROOT):
    data = json.loads((root / "docs/showcase.json").read_text(encoding="utf-8"))
    if set(data) != {"schema_version", "featured", "static_role_cards"} or data["schema_version"] != 1:
        raise ValueError("Invalid showcase contract")
    featured = data["featured"]
    import re
    if not isinstance(featured, list) or not featured or any(not isinstance(s, str) or not re.fullmatch(r"[a-z0-9-]{1,100}", s) for s in featured) or len(set(featured)) != len(featured):
        raise ValueError("Invalid showcase slugs")
    roles = data["static_role_cards"]
    if not isinstance(roles, list) or any(not isinstance(s, str) or s not in featured for s in roles) or len(set(roles)) != len(roles):
        raise ValueError("Invalid static roles")
    return tuple(featured)

def public_node(data, slug, title, fork):
    if (data.get("private") is not False or data.get("visibility") != "public"
            or data.get("full_name") != "Neguchads/" + slug
            or data.get("fork") is not fork or data.get("archived") is not False):
        raise ValueError("Unverified public catalog entry: " + slug)
    counts = [data.get(k) for k in ("stargazers_count", "forks_count", "open_issues_count")]
    if any(type(n) is not int or n < 0 for n in counts):
        raise ValueError("Invalid public counts")
    return {"slug": slug, "title": title, "stars": counts[0], "forks": counts[1],
            "open_items": counts[2], "language": data.get("language"),
            "pushed_at": data.get("pushed_at"), "fork": fork, "archived": False}

def apply(data, fetch, featured=None):
    """Keep upstream metrics/history; adapt only explicitly reviewed public nodes."""
    if data.get("scope") != "public-only" or data.get("owner") != "Neguchads":
        raise ValueError("Invalid public snapshot")
    featured = load() if featured is None else featured
    tools = next(s for s in data["sectors"] if s["id"] == "tools")
    for sector in data["sectors"]:
        sector["projects"] = [p for p in sector["projects"] if p["slug"] not in ALIASES and p["slug"] not in ADDITIONS]
    for slug, (title, fork) in ADDITIONS.items():
        tools["projects"].append(public_node(fetch(slug), slug, title, fork))
    nodes = {p["slug"]: p for s in data["sectors"] for p in s["projects"]}
    edges = {}
    for edge in data["integrations"]:
        source = ALIASES.get(edge["source"], edge["source"])
        target = ALIASES.get(edge["target"], edge["target"])
        if source in nodes and target in nodes:
            edges[(source, target, edge["kind"])] = {"source": source, "target": target, "kind": edge["kind"]}
    for source, target, kind in RELATIONSHIPS:
        if source in nodes and target in nodes:
            edges[(source, target, kind)] = {"source": source, "target": target, "kind": kind}
    data["integrations"] = list(edges.values())
    # No fabricated status: absent or archived upstream entries are not featured.
    data["featured"] = [s for s in featured if s in nodes and nodes[s]["archived"] is False]
    return data
