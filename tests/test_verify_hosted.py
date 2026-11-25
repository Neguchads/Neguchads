import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
import verify_hosted as hosted

class HostedTests(unittest.TestCase):
    def test_exact_bytes_and_delayed_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            for name in hosted.FILES:
                (root / name).write_bytes(name.encode())
            calls = {}
            def fetch(name, sha):
                calls[name] = calls.get(name, 0) + 1
                return b"stale" if calls[name] == 1 else name.encode()
            self.assertEqual(len(hosted.verify(root, fetch, 2, lambda _: None)), 4)
            self.assertEqual(set(calls.values()), {2})

    def test_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            for name in hosted.FILES:
                (root / name).write_bytes(name.encode())
            with self.assertRaisesRegex(RuntimeError, "Hosted artifact mismatch"):
                hosted.verify(root, lambda *_: b"wrong", 1)
