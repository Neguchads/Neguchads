"""Regression checks for the public NAVI-OS profile surface."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class CommandCenterTests(unittest.TestCase):
    def test_language_parity_and_navigation(self):
        en = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(en, (ROOT / "README.en.md").read_text(encoding="utf-8"))
        for file, locale in (("README.md", "en"), ("README.pt-BR.md", "pt-BR")):
            body = (ROOT / file).read_text(encoding="utf-8")
            for item in ("NAVI-OS / Command Center", "#navi-os--command-center", "docs/ARCHITECTURE.md", "docs/ROADMAP.md", "docs/HANDOFF.md", "assets/universe.", "assets/banner.svg", "docs/NEF.md", "docs/UNIVERSAL_AGENT_INTERFACE.md"):
                self.assertIn(item, body)
            for path in re.findall(r'(?:src|srcset)="(assets/navi-command\.[^"]+)"', body):
                self.assertTrue((ROOT / path).is_file(), path)
            self.assertIn(f"assets/navi-command.{locale}.light.svg", body)
            self.assertIn(f"assets/navi-command.{locale}.svg", body)
    def test_safe_static_artwork(self):
        ns = "{http://www.w3.org/2000/svg}"
        for locale in ("en", "pt-BR"):
            for theme in ("", ".light"):
                root = ET.parse(ROOT / "assets" / f"navi-command.{locale}{theme}.svg").getroot()
                self.assertEqual(root.tag, ns + "svg")
                self.assertTrue(root.find(ns + "title").text)
                self.assertTrue(root.find(ns + "desc").text)
                for element in root.iter():
                    self.assertNotIn(element.tag.rsplit("}", 1)[-1], ("script", "foreignObject", "image", "a"))
                    self.assertFalse(any(key.lower().startswith("on") or key.endswith("href") for key in element.attrib))
                text = " ".join(root.itertext())
                for name in ("NAVI CORE", "NEF", "AGENT INTERFACE", "NAVI GRAPHIFY", "HOMEPAGE", "NAVI ABYSS"):
                    self.assertIn(name, text)
    def test_reference_docs(self):
        for name in ("ARCHITECTURE.md", "ROADMAP.md", "HANDOFF.md"):
            self.assertTrue((ROOT / "docs" / name).is_file())

if __name__ == "__main__":
    unittest.main()
