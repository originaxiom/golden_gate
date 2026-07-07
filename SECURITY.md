# Security policy

`golden_gate` is a pure-Python computational library. It has **no network client, no server, no
authentication, no credential handling, no database, and no deserialization of untrusted input**. The
one `subprocess` call runs a fixed `git ls-files` in the internal hygiene gate. So the traditional
web/app attack surface does not apply.

The one thing worth knowing: the braid **compiler** and `evaluate_braid` perform bounded search /
matrix products. They already reject explosive inputs (`compiler._MAX_LENGTH`, a `max_nodes` budget,
`braiding._MAX_ABS_POWER`). **If you ever expose these through a web API or hosted notebook**, enforce
request/resource limits at that boundary — an unbounded compile request is a denial-of-service risk.

## Reporting a vulnerability

If you find a security issue, please **open a GitHub issue** (or contact the maintainer via the repo).
There is no bug-bounty; this is a research project. We'll respond as availability allows.

## Supported versions

Pre-1.0, only the latest `main` is supported. From v1.0.0, security fixes target the latest release.
