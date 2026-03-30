"""
Bitdefender GravityZone - Policies API Event Generator
API Endpoint: /v1.0/jsonrpc/policies
Methods: getPoliciesList, getPolicyDetails
"""
import json
import random
import uuid
from datetime import datetime, timezone


# ── Helpers ───────────────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _rand_id() -> str:
    return str(uuid.uuid4())


# ── Domain constants ──────────────────────────────────────────────────────────

_POLICY_NAMES = [
    "Default Policy",
    "Strict Endpoint Policy",
    "Server Policy",
    "Developer Workstation Policy",
    "Finance Workstation Policy",
    "Executive Device Policy",
    "PCI-DSS Compliance Policy",
]


# ── Private builders ──────────────────────────────────────────────────────────

def _fake_policy() -> dict:
    return {
        "id": _rand_id(),
        "name": random.choice(_POLICY_NAMES),
        "isDefault": random.choice([True, False]),
        "assignedEndpoints": random.randint(0, 100),
        "updatedAt": _now_iso(),
        "modules": {
            "antimalware": {
                "enabled": True,
                "onAccess": True,
                "onDemand": True,
                "quarantine": True,
            },
            "firewall": {
                "enabled": random.choice([True, False]),
                "blockAllExceptAllowed": False,
            },
            "contentControl": {
                "enabled": random.choice([True, False]),
                "webCategories": ["malware", "phishing"],
            },
            "deviceControl": {"enabled": random.choice([True, False])},
            "advancedThreatControl": {
                "enabled": True,
                "level": random.choice(["permissive", "normal", "aggressive"]),
            },
            "hvi": {"enabled": random.choice([True, False])},
        },
    }


def _build_getPoliciesList() -> dict:
    policies = [_fake_policy() for _ in range(random.randint(2, 7))]
    return {
        "method": "getPoliciesList",
        "result": {
            "total": len(policies),
            "page": 1,
            "perPage": 30,
            "pagesCount": 1,
            "items": policies,
        },
    }


def _build_getPolicyDetails() -> dict:
    return {
        "method": "getPolicyDetails",
        "result": _fake_policy(),
    }


_SCENARIOS = [_build_getPoliciesList, _build_getPolicyDetails]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_policies_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone Policies API event."""
    scenario = random.choice(_SCENARIOS)()
    event = {
        "timestamp": _now_iso(),
        "vendor": "bitdefender",
        "product": "gravityzone",
        "api": "policies",
        "jsonrpc": "2.0",
        "method": scenario["method"],
        "id": _rand_id(),
        "result": scenario["result"],
    }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_policies_log(), indent=2))
