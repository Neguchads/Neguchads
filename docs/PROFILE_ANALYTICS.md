# Profile analytics

The profile publishes only aggregate statistics from accessible repositories owned by Neguchads. The initial snapshot uses the primary language reported by GitHub for each original, non-archived repository, excluding the profile repository itself. Repositories with no detected language are excluded from the percentage denominator. Public stars and received forks are summed only across public original active repositories. PRs and issues are authored by Neguchads in account-owned repositories, according to accessible search results.

## Refresh securely

Run locally from a checkout of this repository with Python 3.10+ and an up-to-date GitHub CLI:

```powershell
gh auth login
gh auth status
python scripts/refresh_profile.py --by-bytes
git diff -- assets/github-stats*.svg
git add -- assets/github-stats.en.svg assets/github-stats.en.light.svg assets/github-stats.pt-BR.svg assets/github-stats.pt-BR.light.svg
git commit -m "docs: refresh aggregate profile analytics"
git push
```

Without `--by-bytes`, percentages count the primary language of each repository, matching the initial snapshot. With it, percentages count GitHub Linguist code bytes across accessible original public and private repositories. Neither measure is a proficiency score or the share of code authored by the account owner. Vendored or generated files that GitHub Linguist counts can affect the result.

The script requests metadata and language totals, not file contents. It uses GitHub CLI's local credential storage; no token, repository-level list, private names, links or raw API responses are committed. Review the generated aggregates before publishing. Access depends on the authenticated account and token scope; missing access may exclude projects. The script refuses to overwrite combined statistics with a public-only snapshot. Do not paste a personal access token into this public repository or use it as an external stats service URL. Do not expose private repository names, even in error logs.

All four aggregate SVG variants are hosted directly in the profile repository. The initial metrics are a dated snapshot, not a live service. No contribution streak is claimed without an authenticated contribution calendar.

## Showcase cards and themes

Six public project cards link directly to the corresponding repositories. A weekly GitHub Actions workflow refreshes only their public star and fork counts, with a repository-scoped GitHub token; it never enumerates private repositories. It can also be dispatched manually. Aggregated statistics remain a local authenticated refresh; merged PR totals refer to the same account-owned search scope as authored PRs. The light and dark variants of the aggregate and stack cards are selected with GitHub's picture element. The showcase cards use SVG color-scheme media queries with a dark fallback.

Design inspiration: [Beautiful GitHub Homepage](https://github.com/ishandutta2007/beautiful-github-homepage), MIT. The profile cards, rendering code and theme are independently implemented, not a deployment of that service. WakaTime, gist pins, arbitrary developer ranks and private-data external endpoints are not enabled.
