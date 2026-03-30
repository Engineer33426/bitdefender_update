"""
Bitdefender GravityZone - Companies API Event Generator
API Endpoint: /v1.0/jsonrpc/companies
Methods: getCompanyDetails, updateCompanyDetails
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

_COUNTRIES = ["US", "GB", "DE", "FR", "CA", "AU"]
_COMPANY_NAMES = ["Acme Corp", "Globex Inc", "Initech", "Umbrella LLC"]
_CITIES = ["New York", "London", "Berlin", "Toronto"]


# ── Private builders ──────────────────────────────────────────────────────────

def _build_getCompanyDetails() -> dict:
    return {
        "method": "getCompanyDetails",
        "result": {
            "id": _rand_id(),
            "name": random.choice(_COMPANY_NAMES),
            "address": f"{random.randint(1, 999)} Main St",
            "city": random.choice(_CITIES),
            "country": random.choice(_COUNTRIES),
            "phone": (
                f"+1-{random.randint(200, 999)}-"
                f"{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            ),
            "licenseType": random.choice(["business", "enterprise"]),
            "parentId": None,
        },
    }


def _build_updateCompanyDetails() -> dict:
    return {
        "method": "updateCompanyDetails",
        "result": {"result": True},
    }


_SCENARIOS = [_build_getCompanyDetails, _build_updateCompanyDetails]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_companies_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone Companies API event."""
    scenario = random.choice(_SCENARIOS)()
    event = {
        "timestamp": _now_iso(),
        "vendor": "bitdefender",
        "product": "gravityzone",
        "api": "companies",
        "jsonrpc": "2.0",
        "method": scenario["method"],
        "id": _rand_id(),
        "result": scenario["result"],
    }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_companies_log(), indent=2))
