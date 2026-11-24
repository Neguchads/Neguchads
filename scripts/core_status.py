"""Allowlisted public GitHub CI metadata, never private inventory or logs."""
import json
import re
import urllib.request

REPO="Neguchads/navi-core"
URL="https://api.github.com/repos/Neguchads/navi-core/actions/runs?branch=main&per_page=20"
STATES={"success","failure","cancelled","skipped","timed_out","action_required","neutral","stale","in_progress","queued","unknown"}

def select(payload):
    rows=payload.get("workflow_runs",[])
    if not isinstance(rows,list):return None
    for run in rows:
        if not isinstance(run,dict):continue
        if run.get("head_branch")!="main" or run.get("event") not in ("push","workflow_dispatch") or run.get("path")!=".github/workflows/ci.yml":continue
        if run.get("repository",{}).get("full_name")!=REPO or run.get("repository",{}).get("private") is not False:continue
        sha=run.get("head_sha");run_id=run.get("id")
        if not isinstance(sha,str) or not re.fullmatch("[a-f0-9]{40}",sha) or type(run_id) is not int or not 0<run_id<=9007199254740991:continue
        state=run.get("conclusion") if run.get("status")=="completed" else run.get("status")
        if state not in STATES:state="unknown"
        return {"scope":"public-core-ci","repository":REPO,"commit":sha,"run_id":run_id,"state":state}
    return None

def fetch_core_status():
    try:
        # No token and no user-controlled URLs or query parameters.
        req=urllib.request.Request(URL,headers={"User-Agent":"NAVI-Universe","Accept":"application/vnd.github+json"})
        with urllib.request.urlopen(req,timeout=15) as response:
            raw=response.read(2*1024*1024+1)
            if len(raw)>2*1024*1024:return None
            return select(json.loads(raw))
    except (OSError,ValueError,TypeError,AttributeError):
        return None
