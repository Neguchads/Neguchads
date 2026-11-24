import collections
import pathlib
import tempfile
import unittest
import xml.etree.ElementTree as ET
from scripts import refresh_profile as aggregate
from scripts import refresh_public_cards as public

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ProfileTests(unittest.TestCase):
    def test_aggregate_variants(self):
        for locale in ("en", "pt-BR"):
            for theme in ("", ".light"):
                path = ROOT / "assets" / f"github-stats.{locale}{theme}.svg"
                counts = collections.Counter({f"Language{i}": i+1 for i in range(12)})
                content = aggregate.render(path, [25, 34, 401, 2, 1, 351], counts, 22, True, locale == "pt-BR")
                root = ET.fromstring(content)
                nodes = {e.get("id"): e for e in root.iter() if e.get("id")}
                self.assertEqual(nodes["metric5"].text, "351")
                self.assertEqual(nodes["donut-total"].text, "22")
                self.assertAlmostEqual(sum(float(nodes[f"arc{i}"].get("stroke-dasharray").split()[0]) for i in range(8)), 100, places=3)
                self.assertEqual(nodes["lang7"].text, "Outras" if locale == "pt-BR" else "Other")
                self.assertIn("bytes", nodes["method"].text)

    def test_public_cards_reject_private_or_fork(self):
        d = {"private": False, "visibility": "public", "fork": False, "archived": False,
             "full_name": "Neguchads/chad-recomp", "stargazers_count": 2, "forks_count": 1}
        self.assertEqual(public.validate(d, "chad-recomp"), (2, 1))
        for change in ({"private": True}, {"fork": True}, {"archived": True},
                       {"visibility": "private"}, {"full_name": "another/repo"}, {"stargazers_count": -1}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                public.validate({**d, **change}, "chad-recomp")

    def test_public_render_keeps_layout(self):
        for name in public.NAMES:
            path = ROOT / "assets" / "projects" / (name + ".svg")
            content = public.render(path, 987, 12)
            root = ET.fromstring(content)
            nodes = {e.get("id"): e for e in root.iter() if e.get("id")}
            self.assertEqual(nodes["stars"].text, "987")
            self.assertEqual(nodes["forks"].text, "12")
            self.assertIn("987 GitHub stars, 12 forks.", nodes["desc"].text)
            with tempfile.TemporaryDirectory() as d:
                p = pathlib.Path(d) / "card.svg"
                p.write_text(content, encoding="utf-8")
                self.assertIsNone(public.render(p, 987, 12))

    def test_readme_local_assets(self):
        import re
        for name in ("README.md", "README.en.md", "README.pt-BR.md"):
            s = (ROOT / name).read_text(encoding="utf-8")
            for asset in re.findall(r'(?:src|srcset)="(assets/[^"]+)"', s):
                self.assertTrue((ROOT / asset).is_file(), asset)
                ET.parse(ROOT / asset)
            self.assertEqual(s.count("<details>"), s.count("</details>"))


if __name__ == "__main__":
    unittest.main()
