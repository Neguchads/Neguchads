<p align="center">
  <img src="assets/banner.svg" alt="Neguchads — Game engineering, AI and automation" width="100%" />
</p>

<p align="center">
  <a href="https://recompstore.com/dev/neguchads"><img src="https://recompstore.com/assets/press/verified-dark.svg" alt="Verified developer on RecompStore" height="48"></a>
</p>

<p align="center"><strong>Game engineering · Artificial intelligence · Developer tooling</strong></p>
<p align="center">
  <a href="#navi-os--command-center">NAVI-OS</a> · <a href="#navi-engineering-universe">Universe</a> · <a href="#featured-projects">Projects</a> · <a href="#technology">Technology</a> · <a href="#github-analytics">Analytics</a> · <a href="https://github.com/Neguchads?tab=repositories">Repositories</a>
</p>
<p align="center"><a href="README.pt-BR.md"><img src="assets/language-pt.svg" alt="Leia em português brasileiro" height="32" /></a></p>


I develop tools, applications and experimental static game recompilation projects. My focus is on turning technical problems into reproducible solutions through clear documentation, automation and verifiable tests.

## NAVI-OS / Command Center

A public control surface for an independent engineering ecosystem. NAVI-OS is the umbrella identity; the executable engineering foundation lives in NAVI Core. This is a development preview, not an operating-system distribution or a production certification.

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/navi-command.en.light.svg" />
  <source media="(prefers-color-scheme: dark)" srcset="assets/navi-command.en.svg" />
  <img src="assets/navi-command.en.svg" width="100%" alt="NAVI-OS architecture: Core, NEF, Agent Interface, Graphify, Homepage, Abyss" />
</picture>

| Module | Responsibility |
| :--- | :--- |
| **[NAVI Core](https://github.com/Neguchads/navi-core)** | Project contracts, CLI and reusable verification gates. |
| **[NEF](https://github.com/Neguchads/navi-core/blob/main/docs/NEF.md)** | Architecture profiles, reference policies, roadmap, handoff and reviewed learning. |
| **[Universal Agent Interface](https://github.com/Neguchads/navi-core/blob/main/docs/UNIVERSAL_AGENT_INTERFACE.md)** | Portable context and structured handoff; optional MCP. |
| **[NAVI Graphify](https://github.com/Neguchads/navi-graphify)** | Versioned public project catalog and knowledge graph tooling. |
| **[NAVI GitHomepage](https://github.com/Neguchads/navi-githomepage)** | Brand, cards and interactive explorer renderer. |
| **[NAVI Abyss](https://github.com/Neguchads/navi-abyss)** | Cosmic ocean and repository-star navigation. |

**Engineering workflow:** Clarify → Plan → Build → Verify → Record evidence → Handoff.

[Architecture](docs/ARCHITECTURE.md) · [Roadmap](docs/ROADMAP.md) · [Handoff](docs/HANDOFF.md) · [Verification policy](docs/NAVI_PILOT.md) · [Core CI runs](https://github.com/Neguchads/navi-core/actions/workflows/ci.yml)

<sub>The diagram describes component roles, not live health or compliance. The public snapshot below contains dated metrics; private agent memory is never part of the public catalog.</sub>

## NAVI Engineering Universe

<a href="docs/UNIVERSE.md"><img src="assets/universe.en.svg" width="100%" alt="NAVI Universe — unified public projects and metrics" /></a>

[Hosted 3D dashboard (when Pages is enabled)](https://neguchads.github.io/Neguchads/) · [Offline bundle after the first run](https://github.com/Neguchads/Neguchads/tree/main/docs/universe) · [Architecture and daily refresh](docs/UNIVERSE.md)

## Featured projects

**Engineering tools and frameworks** — development infrastructure, verification and knowledge.

<p align="center">
<a href="https://github.com/Neguchads/navi-core"><img src="assets/projects/navi-core.svg" width="48%" alt="NAVI Engineering Core" /></a>
<a href="https://github.com/Neguchads/spec-to-proof"><img src="assets/projects/spec-to-proof.svg" width="48%" alt="Spec-to-Proof" /></a>
<a href="https://github.com/Neguchads/codex-config-universal"><img src="assets/projects/codex-config-universal.svg" width="48%" alt="Codex Universal Config" /></a>
<a href="https://github.com/Neguchads/navi-graphify"><img src="assets/projects/navi-graphify.svg" width="48%" alt="NAVI Graphify (integrated fork)" /></a>
<a href="https://github.com/Neguchads/chad-recomp"><img src="assets/projects/chad-recomp.svg" width="48%" alt="Chad Standard Recomp — engineering framework" /></a>
</p>

**Featured game recompilation**

<p align="center">
<a href="https://github.com/Neguchads/ccod-xbox-recomp"><img src="assets/projects/ccod-xbox-recomp.svg" width="48%" alt="Curse of Darkness Recomp" /></a>
</p>

<sub>Chad Standard Recomp is a framework, not a game. NAVI Graphify is an integrated fork. Other games remain in the full directory.</sub>

<details>
<summary><strong>Full project directory</strong></summary>

### Game engineering and preservation

| Project | Description |
| :--- | :--- |
| **[Chad Standard Recomp](https://github.com/Neguchads/chad-recomp)** | Universal engineering standard for ports, recompilers and games. Draft specification, schema and manifest validator. |
| **[Dawn of Sorrow Recompiled](https://github.com/Neguchads/cdos-nintendods-recomp)** | Nintendo DS · AOT recompilation, Direct3D 12, Vulkan and RecompLauncher integration. [Releases](https://github.com/Neguchads/cdos-nintendods-recomp/releases) |
| **[Curse of Darkness Recomp](https://github.com/Neguchads/ccod-xbox-recomp)** | Xbox · Experimental Windows port through static recompilation. |
| **[Symphony of the Night Recomp](https://github.com/Neguchads/csotn-saturn-recomp)** | Sega Saturn · Native runtime, engine, recompilation tools and tests. |

### Applications and artificial intelligence

| Project | Description |
| :--- | :--- |
| **[Starlight BI](https://github.com/Neguchads/starlight-bi)** | Interactive dashboards and visual data editing. |
| **[ScriptForge](https://github.com/Neguchads/ScriptForge)** | Web studio for AI-assisted content and music creation. |
| **[Favorite Manager](https://github.com/Neguchads/favorite-manager)** | Chromium bookmark manager with local AI organization. |
| **[PoseClone / ComfyUI](https://github.com/Neguchads/comfyui)** | Python tools and workflows for visual references and character consistency. |

### Developer tooling

**[Spec-to-Proof](https://github.com/Neguchads/spec-to-proof)** — Requirements, acceptance criteria and evidence-based verification.  
**[Codex Universal Config](https://github.com/Neguchads/codex-config-universal)** — Portable configuration, privacy and reusable CI infrastructure.

</details>

## Engineering ecosystem

<a href="https://github.com/Neguchads/navi-githomepage/tree/main/docs/explore"><img src="assets/ecosystem.en.svg" width="100%" alt="Neguchads public project map" /></a>

[NAVI Graphify](https://github.com/Neguchads/navi-graphify) provides the versioned public catalog. [NAVI GitHomepage](https://github.com/Neguchads/navi-githomepage) generates the map and offline explorer. Private graphs and agent memory remain local.

[Explore and download offline HTML](https://github.com/Neguchads/navi-githomepage/tree/main/docs/explore) · [Architecture and privacy](docs/ECOSYSTEM.md)

## Technology

<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/stack.en.light.svg" />
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack.en.svg" />
  <img src="assets/stack.en.svg" width="100%" alt="Technology stack: native engineering, web applications, games, AI, automation, quality and delivery" />
</picture>

<details>
<summary>Technology list (text)</summary>

| Area | Stack |
| :--- | :--- |
| Native engineering | C · C++ · Python · CMake · Ninja · LLVM/Clang |
| Web applications | TypeScript · JavaScript · React · Node.js |
| Games and graphics | SDL3 · Dear ImGui · Direct3D 12 · Vulkan |
| AI and automation | Codex · Ollama · ComfyUI · PowerShell |
| Quality and delivery | Git · GitHub Actions · CodeQL · Playwright · Vitest · Hypothesis |

</details>

## GitHub Analytics

The NAVI Universe above provides the daily public snapshot. The card below is a separate historical aggregate, not refreshed by this pipeline.


<picture>
  <source media="(prefers-color-scheme: light)" srcset="assets/github-stats.en.light.svg" />
  <source media="(prefers-color-scheme: dark)" srcset="assets/github-stats.en.svg" />
  <img src="assets/github-stats.en.svg" width="100%" alt="Aggregate GitHub statistics and top languages of public and private projects" />
</picture>

<sub>Cards show a dated snapshot; see the refresh documentation. Aggregated active original projects, including accessible public and private repositories; third-party forks, archived repositories and this profile repository are excluded from project and language totals. Authored PRs and issues in account-owned repositories reflect accessible GitHub search results. Stars and received forks are from public original projects only. No private repository names or links are published.</sub>

[Methodology & refresh](docs/PROFILE_ANALYTICS.md)

## Engineering principles

- **Reproducibility:** incremental builds, traceable dependencies and technical documentation.
- **Quality:** regression and property tests, fuzzing and benchmarks where applicable.
- **Security:** static analysis, integrity checks and distribution evidence where available.
- **Open source:** project-specific licensing, dependency attribution and respect for third-party rights.

Game ports are experimental and require your own compatible game copy. Consult each project's README and licensing terms before redistribution or reuse.

---

<p align="center">
  <strong>Explore. Build. Verify.</strong><br />
  <a href="https://github.com/Neguchads?tab=repositories">All public repositories</a>
</p>
