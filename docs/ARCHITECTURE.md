# Profile architecture / Arquitetura do perfil

NAVI-OS is the umbrella identity; NAVI Core contains the executable CLI and NEF reference framework. The profile is a public, read-only presentation of the ecosystem.

## Boundaries
- Profile README and local SVGs: static, bilingual, no executable browser code.
- Graphify: reviewed public catalog and optional structural summary.
- Homepage: renders the public catalog and snapshot.
- Abyss: optional interactive world in the separately generated Pages/offline bundle.
- NAVI Core: existing pinned read-only Python verification gate. NEF guides documentation and agent handoff; the profile does not execute a hosted agent.
- Universe daily: existing single writer of generated assets. Command-center artwork is a separate reviewed static asset, not generated metrics.

See [Universe](UNIVERSE.md), [ecosystem](ECOSYSTEM.md), [analytics](PROFILE_ANALYTICS.md), [pilot](NAVI_PILOT.md) and [NEF](https://github.com/Neguchads/navi-core/blob/main/docs/NEF.md).

## Decisions and privacy
Preserve the original logo, graphite/cyan palette, existing card assets, manifest, CI pin and folder layout. Keep the diagram conceptual; no inferred compliance scores or invented runtime status. Do not export raw prompts, private repository names, private graphs, credentials or agent memory. Existing historical aggregates keep their documented scope. No new network calls or tokens. The README showcase is curated separately from the generated Universe dashboard. Original metrics cards and their refresh allowlist remain available to the pinned renderer; new role cards are static and the integrated Graphify fork is explicitly identified.

## Verification
Run `python -m unittest discover -s tests -v` from the repository root. Check both languages, both GitHub themes, accessible image descriptions, and the profile preview before publication. CI is complementary; a pass is not proof of visual quality or production certification.
