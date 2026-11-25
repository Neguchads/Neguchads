# NAVI Engineering Universe

Four versioned components: [Graphify](https://github.com/Neguchads/navi-graphify), [Homepage](https://github.com/Neguchads/navi-githomepage), [Abyss](https://github.com/Neguchads/navi-abyss), [Profile](https://github.com/Neguchads/Neguchads). The profile orchestrates a daily public-only snapshot at 09:23 UTC (06:23 Brasília); scheduled Actions are best effort. Upstream code is pinned by commit; daily data are fresh. Review pin changes via PR. No cross-repo write token, personal PAT, commercial Graphify Cloud or browser API credentials required.

The 3D dashboard projects XYZ coordinates onto Canvas; the new NAVI Abyss cosmic ocean is published as `cosmic.html`; the original WebGPU scene remains a separate legacy `abyss.html`. The cosmic scene uses its own pinned public catalog, not live analytics. GitHub README supports static SVG, not interactive JS. After the first successful main-branch run of this revision, the bundle is in docs/universe; download the folder to use offline. For hosted interactive access, enable Settings > Pages > Source: GitHub Actions, and set repository Actions variable NAVI_ENABLE_PAGES=true. Expected URL: https://neguchads.github.io/Neguchads/. The Pages job is optional and does not gate snapshot commits.

Metrics cover publicly visible owned repositories; aggregate originals exclude forks, archived repos and profile. Daily history begins at first successful run; no backfilled numbers. Structural Graphify scan is attempted for the public profile; failures are explicitly unavailable and do not prevent analytics publication. Raw graphs and private data are never published. Existing private-inclusive aggregate cards are historical, separate from this public dataset.

Publication uses a separate write-permission job; the build job has read permission only. A failed build leaves the previous snapshot intact. Check the Actions run for evidence. The original six featured cards are refreshed in the same build.

## Recovery and publication safety

NAVI Universe daily is the single writer for public cards and generated dashboard files. Profile cards remains a validation-only workflow. Main builds use the current main checkout, and publication fetches main before each bounded non-force push. A stale snapshot or changed build input causes a clear failure rather than overwriting newer data. For recovery, launch a fresh Run workflow on main; do not rerun executions created before the workflow fix. Pages artifacts have per-attempt names to avoid immutable-artifact collisions. GitHub Pages service errors may still need a fresh deployment.

## Rename and coordinated rollout
Canonical slugs: `navi-graphify`, `navi-githomepage`, `navi-abyss`, `Neguchads`, and `navi-core`. The three producer pins are reviewed PR commit candidates; merge the upstream PRs before merging this profile PR. The historical generated snapshot and its source SHAs are not rewritten; the next successful daily publication regenerates the bundle with canonical slugs. No Pages settings are changed.
