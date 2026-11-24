# Profile analytics

The profile publishes only aggregate statistics from accessible repositories owned by Neguchads. The initial snapshot uses the primary language reported by GitHub for each original, non-archived repository, excluding the profile repository itself. Repositories with no detected language are excluded from the percentage denominator. Public stars and received forks are summed only across public original active repositories. PRs and issues are authored by Neguchads in account-owned repositories, according to accessible search results.

## Refresh securely

Run locally from a checkout of this repository with Python 3.10+ and an up-to-date GitHub CLI:

```powershell
gh auth login
gh auth status
python scripts/refresh_profile.py --by-bytes
git diff -- assets/github-stats.en.svg assets/github-stats.pt-BR.svg
git add assets/github-stats.en.svg assets/github-stats.pt-BR.svg
git commit -m "docs: refresh aggregate profile analytics"
git push
```

Without `--by-bytes`, percentages count the primary language of each repository, matching the initial snapshot. With it, percentages count GitHub Linguist code bytes across accessible original public and private repositories. Neither measure is a proficiency score or the share of code authored by the account owner. Vendored or generated files that GitHub Linguist counts can affect the result.

The script requests metadata and language totals, not file contents. It uses GitHub CLI's local credential storage; no token, repository-level list, private names, links or raw API responses are committed. Review the generated aggregates before publishing. Access depends on the authenticated account and token scope; missing access may exclude projects. The script refuses to overwrite combined statistics with a public-only snapshot. Do not paste a personal access token into this public repository or use it as an external stats service URL. Do not expose private repository names, even in error logs.

Both SVGs are hosted directly in the profile repository. The initial metrics are a dated snapshot, not a live service. No contribution streak is claimed without an authenticated contribution calendar.
