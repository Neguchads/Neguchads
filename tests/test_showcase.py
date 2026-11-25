import copy
import unittest
from scripts.showcase import ADDITIONS, apply, load

def metadata(slug):
    return {"private": False, "visibility": "public", "full_name": "Neguchads/"+slug,
            "fork": ADDITIONS[slug][1], "archived": False, "stargazers_count": 2,
            "forks_count": 1, "open_issues_count": 0, "language": "Python", "pushed_at": None}

def fixture():
    return {"scope":"public-only","owner":"Neguchads","totals":{"stars":42},"history":[],
            "sectors":[{"id":"tools","projects":[{"slug":s,"archived":False}
                for s in ("github-homepage","navyv-abyss","spec-to-proof","codex-config-universal","navi-graphify","Neguchads")]},
                {"id":"games","projects":[{"slug":s,"archived":False} for s in ("chad-recomp","ccod-xbox-recomp","cdos-nintendods-recomp")]}],
            "integrations":[{"source":"github-homepage","target":"Neguchads","kind":"visualization-provider"}],
            "featured":["cdos-nintendods-recomp"]}

class ShowcaseTests(unittest.TestCase):
    def test_sync_and_idempotence(self):
        data=apply(fixture(),metadata)
        self.assertEqual(data["featured"],list(load()))
        self.assertEqual(data["totals"],{"stars":42})
        slugs=[p["slug"] for s in data["sectors"] for p in s["projects"]]
        self.assertIn("navi-githomepage",slugs)
        self.assertIn("navi-abyss",slugs)
        self.assertIn("cdos-nintendods-recomp",slugs)
        self.assertNotIn("github-homepage",slugs)
        self.assertNotIn("navyv-abyss",slugs)
        self.assertEqual(apply(copy.deepcopy(data),metadata),data)
    def test_reject_private_or_wrong_identity(self):
        for override in ({"private":True},{"visibility":"private"},{"full_name":"Other/navi-core"},{"archived":True}):
            with self.subTest(override=override), self.assertRaises(ValueError):
                apply(fixture(),lambda slug:{**metadata(slug),**override})
