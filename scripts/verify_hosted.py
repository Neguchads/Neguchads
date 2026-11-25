"""Anonymous hosted byte verification; no credentials, no private data."""
import argparse
import hashlib
import pathlib
import time
import urllib.error
import urllib.request

BASE = "https://neguchads.github.io/Neguchads/"
FILES = ("index.html", "snapshot.json", "abyss.html", "cosmic.html")
MAX_BYTES = 16 * 1024 * 1024

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def read_public(name, expected):
    if name not in FILES:
        raise ValueError("Unapproved public file")
    url = BASE + name + "?navi=" + expected
    req = urllib.request.Request(url, headers={"User-Agent": "NAVI-hosted-check", "Accept-Encoding": "identity"})
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(req, timeout=20) as response:
        if response.status != 200 or response.geturl() != url:
            raise ValueError("Unexpected hosted response")
        return response.read(MAX_BYTES + 1)

def verify(root, fetch=read_public, attempts=12, sleep=time.sleep):
    expected = {}
    for name in FILES:
        path = pathlib.Path(root) / name
        if not path.is_file() or path.stat().st_size > MAX_BYTES:
            raise ValueError("Invalid deployment artifact")
        expected[name] = digest(path.read_bytes())
    pending = dict(expected)
    for attempt in range(attempts):
        for name, sha in list(pending.items()):
            try:
                raw = fetch(name, sha)
                if len(raw) <= MAX_BYTES and digest(raw) == sha:
                    del pending[name]
                    print("Verified hosted bytes:", name, sha)
            except (OSError, ValueError, urllib.error.URLError):
                pass
        if not pending:
            return expected
        if attempt + 1 < attempts:
            sleep(5)
    raise RuntimeError("Hosted artifact mismatch or unavailable: " + ", ".join(pending))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=pathlib.Path)
    verify(parser.parse_args().artifact)
