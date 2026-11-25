# Neguchads engineering ecosystem

- [NAVI Graphify](https://github.com/Neguchads/navi-graphify/tree/v8/integrations/portfolio): canonical versioned public catalog, local Graphify AST exporter and numeric summary.
- [NAVI GitHomepage](https://github.com/Neguchads/navi-githomepage/tree/main/docs/explore): consumes a pinned catalog, generates offline interactive HTML and bilingual SVGs.
- This profile: copies the generated SVGs from the renderer and links to both repositories.

## Data boundary

The initial map is curated public membership, not extracted dependencies. Optional code-only metrics require a fresh verified public checkout and real Graphify scan. No raw graphs, private code, paths, prompts, tokens or agent memory are published. Existing aggregated profile analytics remain independent.

## Reviewed update

After the canonical catalog changes, update the pinned snapshot in Homepage, run `node scripts/build-portfolio.mjs`, and review the generated files. Then copy the two SVGs here and update `assets/ecosystem-source.json` to the exact reviewed source commit. No browser-side API call or private credential is needed. GitHub Pages is optional; the explorer is downloadable and offline.

Initial renderer source: [pinned commit](https://github.com/Neguchads/navi-githomepage/tree/a8e231893eeee43d1376e03f53f5d3505d4618e8/docs/explore).
