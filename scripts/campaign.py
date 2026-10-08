#!/usr/bin/env python3
"""Shared reading of the campaign's declarations.

`record_run.py`, `validate_run.py` and `report_run.py` all have to agree on what
a suite declares and on which provider an engine name belongs to. That
agreement is exactly what a schema cannot express, so it lives here rather than
being restated in each script, where the copies would drift.
"""
from __future__ import annotations

import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent

# What provides each engine name the harness emits. An arm whose provider cannot
# be identified refuses the run: a page that says "LAPACK (unknown vendor)" is
# exactly the opacity the result pages exist to remove.
PROVIDER_OF_ENGINE = {
    "faer-1lane": "tlinalg",
    "faer-pool": "tlinalg",
    "lapack-openblas": "openblas",
}

# The faer crates the `tlinalg` provider links, read out of the measured
# checkout's `Cargo.lock` and recorded under their own package names (`faer` or
# the fork's `t4a-faer`). They are dependencies, not engines: the provider that
# computes is `tlinalg`, which is what `PROVIDER_OF_ENGINE` maps to, so a
# dependency entry can never be confused with the engine's provider.
FAER_PACKAGES = ("faer", "faer-traits", "t4a-faer", "t4a-faer-traits")


def load(path) -> dict:
    return yaml.safe_load(pathlib.Path(path).read_text())


def find_suite(suite_id: str):
    """The declaration file and body whose `id` is `suite_id`."""
    for f in sorted((ROOT / "benchmarks/suites").glob("*.yaml")):
        data = load(f)
        if data["id"] == suite_id:
            return f, data
    return None, None


def run_spec(suite: dict) -> dict:
    """The suite's declared measurements. One spec per suite, as the model says."""
    return suite["runs"][0]


def populations(suite: dict) -> list[dict]:
    """The declared populations with their family groups expanded.

    The expansion is the definition of what the suite covers, so every script
    expands it the same way instead of trusting a manifest's own account.
    """
    groups = suite["family_groups"]
    out = []
    for spec in run_spec(suite)["populations"]:
        families = [f for group in spec["groups"] for f in groups[group]]
        out.append({"regime": spec["regime"], "families": families,
                    "n": [str(n) for n in spec["n"]], "batch": [int(b) for b in spec["batch"]]})
    return out


def same_populations(covered: list[dict], declared: list[dict]) -> bool:
    def key(p):
        return (p["regime"], tuple(p["families"]), tuple(p["n"]), tuple(p["batch"]))
    return sorted(key(p) for p in covered) == sorted(key(p) for p in declared)


def vendors_declared(engines) -> bool:
    """Whether any declared engine is backed by a vendor library."""
    return "openblas" in {PROVIDER_OF_ENGINE.get(e) for e in engines}
