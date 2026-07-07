# Releasing golden_gate

The release machinery is wired; cutting a release is a short, mostly-automated sequence. A few steps
are **owner-only** because this environment cannot push tags (the git proxy returns HTTP 403 on tag
refs) and PyPI/Pages need one-time account setup.

## One-time owner setup

1. **PyPI distribution name.** `golden-gate` / `golden-gates` are taken on PyPI. Keep the *import* name
   `golden_gate`, but set a distinct `[project].name` in `pyproject.toml` (e.g. `golden-gate-anyons`)
   before the first upload.
2. **PyPI trusted publishing.** Create the PyPI project and add this repo + `publish.yml` + a `pypi`
   environment as a trusted publisher (<https://docs.pypi.org/trusted-publishers/>). No token needed.
3. **GitHub Pages.** Settings → Pages → Source = **GitHub Actions** (so `docs.yml` can deploy).
4. **Repo topics** (cosmetic, discoverability): `quantum-computing`, `topological-quantum-computation`,
   `fibonacci-anyons`, `knot-theory`, `braid-group`.

## Cutting a release (vX.Y.Z)

1. Decide the version per SemVer (see the policy in `docs/API.md`). **Note on maturity:** the trove
   classifier is `Development Status :: 4 - Beta` and the README frames this as a `v0.1` prototype —
   a `1.0.0` cut is a deliberate API-stability commitment, so make it consciously (or stay on the 0.x
   line until there's adoption/feedback).
2. Bump the version in **`pyproject.toml`** and **`CITATION.cff`**; if cutting 1.0.0, change the
   classifier to `Development Status :: 5 - Production/Stable`.
3. Move the `## [Unreleased]` items in **`CHANGELOG.md`** under a new `## [X.Y.Z] — YYYY-MM-DD` heading.
4. Commit; ensure CI (lint + types + tests + gates) is green on `main`.
5. **(owner)** Tag and push:
   ```bash
   git tag -a vX.Y.Z -m "golden_gate vX.Y.Z"
   git push origin vX.Y.Z
   ```
   The tag push triggers **`publish.yml`** (build → `twine check` → PyPI trusted publishing) and the
   push to `main` keeps **`docs.yml`** deploying the site + explorer to Pages.
6. **(owner)** Create the GitHub Release from the tag (paste the CHANGELOG section as notes). Optionally
   mint a **Zenodo DOI** for the release and add it to `CITATION.cff` + the README badge.

## Verifying a build locally (no upload)

```bash
python -m build              # sdist + wheel in dist/
twine check dist/*           # metadata (needs current `packaging`)
pip install dist/*.whl       # in a fresh venv
golden-gate-verify           # the banked math identities reproduce -> exit 0
```
