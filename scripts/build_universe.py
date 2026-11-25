#!/usr/bin/env python3
"""Build the public NAVI bundle with reviewed, pinned upstream revisions."""
import argparse,json,pathlib,re,subprocess,tempfile,os
from core_status import fetch_core_status
from showcase import apply as apply_showcase
from refresh_public_cards import fetch as fetch_public_repo
ROOT=pathlib.Path(__file__).resolve().parents[1]
def run(*args,**kw): subprocess.run(args,check=True,**kw)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=pathlib.Path)
    p.add_argument("--scan",action="store_true")
    a=p.parse_args()
    out=a.out.resolve()
    pins=json.loads((ROOT/"docs/universe-pins.json").read_text())
    if set(pins)!={"navi-graphify","navi-githomepage","navi-abyss"} or not all(re.fullmatch(r"[a-f0-9]{40}",s) for s in pins.values()): raise ValueError("Invalid pins")
    with tempfile.TemporaryDirectory(prefix="navi-build-") as tmp:
        t=pathlib.Path(tmp)
        for repo,sha in pins.items():
            dest=t/repo
            run("git","init","-q",str(dest))
            run("git","-C",str(dest),"-c","credential.helper=","fetch","--depth=1","https://github.com/Neguchads/"+repo+".git",sha)
            run("git","-C",str(dest),"checkout","--detach","FETCH_HEAD")
            assert subprocess.check_output(["git","-C",str(dest),"rev-parse","HEAD"],text=True).strip()==sha
        graph=t/"navi-graphify"
        sources=t/"sources.json"
        sources.write_text(json.dumps({**pins,"Neguchads":subprocess.check_output(["git","-C",str(ROOT),"rev-parse","HEAD"],text=True).strip()}))
        snapshot=t/"snapshot.json"
        cmd=["python3",str(graph/"integrations/portfolio/universe_snapshot.py"),"--out",str(snapshot),"--sources",str(sources),"--previous",str(ROOT/"docs/universe/snapshot.json")]
        if a.scan:
            summary=t/"summary.json"
            try:
                run("uv","sync","--frozen","--no-dev",cwd=graph,timeout=300)
                run("uv","run","--frozen","--no-dev","python","integrations/portfolio/export_public.py","Neguchads","--out",str(summary),cwd=graph,timeout=1000)
                if json.loads(summary.read_text())["nodes"]>0: cmd.extend(["--summary",str(summary)])
                else: print("::warning::Graphify returned an empty graph; AST metrics unavailable.")
            except (subprocess.SubprocessError,OSError,ValueError,KeyError):
                print("::warning::Graphify scan unavailable; no AST metrics fabricated.")
        run(*cmd)
        public_data=json.loads(snapshot.read_text(encoding="utf-8"))
        apply_showcase(public_data, fetch_public_repo)
        public_data["core_status"]=fetch_core_status()
        snapshot.write_text(json.dumps(public_data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        run("node",str(t/"navi-githomepage/scripts/build-universe.mjs"),str(snapshot),str(t/"navi-abyss"),str(ROOT),str(out))
        run("node","--check",str(t/"navi-githomepage/docs/universe/universe.js"))
        import xml.etree.ElementTree as ET
        for f in out.glob("*.svg"): ET.parse(f)
        assert (out/"index.html").is_file() and (out/"snapshot.json").is_file() and (out/"cosmic.html").is_file() and (out/"abyss.html").is_file()
if __name__=="__main__": main()
