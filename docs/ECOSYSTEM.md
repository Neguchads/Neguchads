# Neguchads engineering ecosystem

## Responsibilities

| Repository | Responsibility | Integration |
| --- | --- | --- |
| [NAVI Core](https://github.com/Neguchads/navi-core) | Provider-independent engineering contracts, NEF, portable agent interface, local knowledge and governance | Pinned read-only reusable CI; public CI metadata only |
| [NAVI Graphify](https://github.com/Neguchads/navi-graphify/tree/v8/integrations/portfolio) | Canonical public catalog, daily snapshot and optional numeric AST summary | Versioned public Universe contract |
| [NAVI GitHomepage](https://github.com/Neguchads/navi-githomepage) | Offline HTML/SVG and Universe renderer | Consumes reviewed snapshot and Abyss assets |
| [NAVI Abyss](https://github.com/Neguchads/navi-abyss) | Cosmic reference and separate legacy underwater renderer | Public catalog, local assets and shared visual identity |
| [Neguchads](https://github.com/Neguchads/Neguchads) | Profile, public bundle orchestration and deployment | Pinned sources, artifacts, GitHub Pages and hosted verification |

Nexus is a separate candidate, not a required dependency. Core runs without an AI provider; adoption of a single compatible host (Codex, Claude Code, Gemini CLI or Copilot) does not depend on the others. Real host acceptance is separate from CI.

## Public integration lifecycle

1. Review producer/renderer changes and native CI on their own repositories.
2. Update [universe-pins.json](universe-pins.json) to exact reviewed commits in a profile PR. The pinned source set is deliberately independent of the Core pilot pin.
3. The [Universe workflow](../.github/workflows/navi-universe.yml) builds the public bundle from detached, exact revisions, optionally scans public code for numeric aggregate metrics, renders the portal and runs profile tests.
4. Main-only publication writes generated public assets. When Pages is enabled, deploy the artifact and compare hosted HTTPS files against the expected artifact without credentials.
5. If validation fails, keep or restore the previously reviewed source pins. Never silently follow a floating upstream branch.

The [Core pilot](../.github/workflows/navi-pilot.yml) must pin the same reviewed full SHA in both the reusable workflow reference and the `core_sha` input. Update each consumer via PR and verify its own native and reusable CI before merging. Passing the Core's own CI is not sufficient for consumer acceptance.

## Data boundary

Membership and integration edges are curated public metadata, not extracted dependency claims. Optional code-only metrics require a verified public checkout and actual Graphify scan. Unavailable measurements must not be represented as zero. No raw graphs, private code, paths, prompts, tokens or agent memory are published. Core status is allowlisted public GitHub CI metadata, not runtime health or production certification. No private credentials are required in the browser.

## Current evidence and remaining acceptance

- The [Universe run 45684548882](https://github.com/Neguchads/Neguchads/actions/runs/45684548882) passed build, publication, Pages deployment and hosted HTTPS artifact verification.
- Future runs must supply fresh evidence; previous success does not certify a later revision.
- Remaining work includes real single-host acceptance, security/license/recovery gates, production rollout approval and visual/accessibility acceptance across browsers. Nexus evaluation remains independent.

Historical initial renderer source: [pinned commit](https://github.com/Neguchads/navi-githomepage/tree/a8e231893eeee43d1376e03f53f5d3505d4618e8/docs/explore).
