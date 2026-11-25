# Handoff / Transferência de contexto

PR #9 is merged (05a83c8); Profile cards and NAVI pilot passed. Visual browser review remains pending.

Current scope: canonical profile showcase and repository rename compatibility. README references use navi-githomepage and navi-abyss; the pinned upstream provenance keys are retained until schema migration. Build bridge verifies public identity and fork status for the two renamed repositories and NAVI Core. No private data or new credentials. Dashboard publication requires successful CI and a fresh main run.

Dependencies: [GitHomepage #7](https://github.com/Neguchads/navi-githomepage/pull/7), [Abyss #4](https://github.com/Neguchads/navi-abyss/pull/4), [Graphify #6](https://github.com/Neguchads/navi-graphify/pull/6). Open at the time of this update; do not pin unmerged heads.

Next: verify PR tests and rendered output; merge if approved, verify main build/publish/Pages and review upstream pins separately. Rollback: revert this change and rebuild with the earlier compatible pins; generated snapshot may need regeneration. Do not force push.

References: [architecture](ARCHITECTURE.md), [roadmap](ROADMAP.md), [showcase](showcase.json), [pilot](NAVI_PILOT.md).
