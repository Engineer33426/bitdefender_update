"""
Bitdefender GravityZone - Licensing API Event Generator
API Endpoint: /v1.0/jsonrpc/licensing
Methods: getLicenseInfo, setLicenseKey, getMonthlyUsage
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


# ── Private builders ──────────────────────────────────────────────────────────

def _build_getLicenseInfo() -> dict:
    return {
        "method": "getLicenseInfo",
        "result": {
            "licenseKey": f"GZ-{random.randint(100000, 999999)}-{random.randint(1000, 9999)}",
            "type": random.choice(
                ["BusinessSecurity", "BusinessSecurityPremium", "Enterprise"]
            ),
            "status": random.choice(["active", "expired", "trial"]),
            "startDate": "2024-01-01",
            "endDate": "2025-12-31",
            "seats": random.randint(50, 500),
            "usedSeats": random.randint(10, 49),
            "modules": {
                "advancedThreatControl": True,
                "patchManagement": random.choice([True, False]),
                "fullDiskEncryption": random.choice([True, False]),
                "edr": random.choice([True, False]),
                "networkSandboxAnalyzer": random.choice([True, False]),
            },
        },
    }


def _build_setLicenseKey() -> dict:
    return {
        "method": "setLicenseKey",
        "result": {"result": True},
    }


def _build_getMonthlyUsage() -> dict:
    months = [
        {"month": f"2024-{m:02d}", "slots": random.randint(40, 500)}
        for m in range(1, 13)
    ]
    return {
        "method": "getMonthlyUsage",
        "result": {"usageData": months},
    }


_SCENARIOS = [_build_getLicenseInfo, _build_setLicenseKey, _build_getMonthlyUsage]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_licensing_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone Licensing API event."""
    scenario = random.choice(_SCENARIOS)()
    event = {
        "timestamp": _now_iso(),
        "vendor": "bitdefender",
        "product": "gravityzone",
        "api": "licensing",
        "jsonrpc": "2.0",
        "method": scenario["method"],
        "id": _rand_id(),
        "result": scenario["result"],
    }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_licensing_log(), indent=2))
