import sys
import pathlib
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"scripts"))
from core_status import select

class CoreStatusTests(unittest.TestCase):
    def fixture(self,**kw):
        d={"head_branch":"main","event":"push","path":".github/workflows/ci.yml","repository":{"full_name":"Neguchads/navi-core","private":False},"head_sha":"a"*40,"id":123,"status":"completed","conclusion":"success"}
        d.update(kw);return d
    def test_allowlist(self):
        d=select({"workflow_runs":[self.fixture(log="private",name="untrusted")]})
        self.assertEqual(d,{"scope":"public-core-ci","repository":"Neguchads/navi-core","commit":"a"*40,"run_id":123,"state":"success"})
    def test_excludes_private_and_pr(self):
        self.assertIsNone(select({"workflow_runs":[self.fixture(repository={"full_name":"Neguchads/navi-core","private":True}),self.fixture(event="pull_request")]}))
    def test_unknown_not_success(self):
        self.assertEqual(select({"workflow_runs":[self.fixture(status="completed",conclusion=None)]})["state"],"unknown")
    def test_rejects_bad_sha(self):
        self.assertIsNone(select({"workflow_runs":[self.fixture(head_sha="main")]}))
