import json
import pathlib
import subprocess
import tempfile
import unittest
from scripts import publish_universe as pub

class PublishTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.work = self.root / "work"
        self.bundle = self.root / "bundle"
        subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(self.remote)], check=True, capture_output=True)
        subprocess.run(["git", "clone", str(self.remote), str(self.work)], check=True, capture_output=True)
        pub.git(self.work, "config", "user.name", "test")
        pub.git(self.work, "config", "user.email", "test@example.invalid")
        (self.work/"README.md").write_text("base")
        pub.git(self.work,"add",".")
        pub.git(self.work,"commit","-m","base")
        pub.git(self.work,"push","origin","main")
        self.source=pub.git(self.work,"rev-parse","HEAD",capture=True).stdout.strip()
        for rel in (*pub.FILES, "assets/projects/chad-recomp.svg"):
            p=self.bundle/rel
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text("test")
        (self.bundle/"snapshot.json").write_text(json.dumps({"owner":"Neguchads","scope":"public-only","schema_version":1,"sources":{"Neguchads":self.source},"featured":["chad-recomp"]}))
    def advance(self, rel):
        other=self.root/"other"
        subprocess.run(["git","clone",str(self.remote),str(other)],check=True,capture_output=True)
        pub.git(other,"config","user.name","test")
        pub.git(other,"config","user.email","test@example.invalid")
        p=other/rel
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text("new remote change")
        pub.git(other,"add",".")
        pub.git(other,"commit","-m","remote advance")
        pub.git(other,"push","origin","main")
    def test_preserves_remote_advance_and_idempotent(self):
        self.advance("README.md")
        pub.publish(self.work,self.bundle)
        self.assertEqual((self.work/"README.md").read_text(),"new remote change")
        self.assertTrue((self.work/"docs/universe/index.html").exists())
        self.assertTrue((self.work/"docs/universe/cosmic.html").exists())
        head=pub.git(self.work,"rev-parse","HEAD",capture=True).stdout
        pub.publish(self.work,self.bundle)
        self.assertEqual(pub.git(self.work,"rev-parse","HEAD",capture=True).stdout,head)
    def test_refuses_stale_inputs(self):
        self.advance("docs/universe-pins.json")
        with self.assertRaisesRegex(RuntimeError,"changed"):
            pub.publish(self.work,self.bundle)
        self.assertFalse((self.work/"docs/universe/index.html").exists())

    def test_refuses_untracked_non_generated_content(self):
        (self.work/"unreviewed.txt").write_text("do not overwrite")
        with self.assertRaisesRegex(RuntimeError,"clean checkout"):
            pub.publish(self.work,self.bundle)
        self.assertTrue((self.work/"unreviewed.txt").is_file())
        self.assertFalse((self.work/"docs/universe/index.html").exists())

    def test_direct_publisher_import_does_not_dirty_checkout(self):
        import shutil
        import sys
        source = pathlib.Path(pub.__file__).resolve().parent
        scripts = self.work/"scripts"
        scripts.mkdir()
        for name in ("publish_universe.py","showcase.py"):
            shutil.copyfile(source/name,scripts/name)
        docs=self.work/"docs"
        docs.mkdir()
        shutil.copyfile(source.parent/"docs/showcase.json",docs/"showcase.json")
        pub.git(self.work,"add",".")
        pub.git(self.work,"commit","-m","publisher fixture")
        subprocess.run([sys.executable,str(scripts/"publish_universe.py"),"--help"],check=True,capture_output=True)
        self.assertEqual(pub.git(self.work,"status","--porcelain",capture=True).stdout,"")
