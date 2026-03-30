"""
Bitdefender GravityZone - Packages API Event Generator
API Endpoint: /v1.0/jsonrpc/packages
Methods: getInstallationLinks, createPackage, getPackagesList,
         deletePackage, getPackageDetails
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

_OS_PLATFORMS = ["windows", "linux", "mac"]


# ── Private builders ──────────────────────────────────────────────────────────

def _fake_package() -> dict:
    return {
        "id": _rand_id(),
        "name": f"BEST-Package-{random.randint(1, 20)}",
        "description": "Auto-generated deployment package",
        "language": "en_US",
        "modules": {
            "antimalware": True,
            "advancedThreatControl": True,
            "firewall": random.choice([True, False]),
            "contentControl": random.choice([True, False]),
            "deviceControl": random.choice([True, False]),
            "patchManagement": random.choice([True, False]),
            "fullDiskEncryption": random.choice([True, False]),
        },
        "scanMode": random.choice([1, 2, 3]),
        "deploymentOptions": {
            "downloadFromCloud": True,
            "uninstallPassword": random.choice([True, False]),
        },
        "platform": random.choice(_OS_PLATFORMS),
        "version": (
            f"7.{random.randint(5, 9)}.{random.randint(0, 9)}.{random.randint(100, 200)}"
        ),
    }


def _build_getInstallationLinks() -> dict:
    links = [
        {
            "id": _rand_id(),
            "packageName": f"BEST-Package-{random.randint(1, 10)}",
            "installLink": (
                f"https://cloud.gravityzone.bitdefender.com/Packages/STD/0/"
                f"{_rand_id()}/gravityzone_business_security.exe"
            ),
            "osType": random.choice(_OS_PLATFORMS),
        }
        for _ in range(random.randint(1, 3))
    ]
    return {
        "method": "getInstallationLinks",
        "result": {"installationLinks": links},
    }


def _build_createPackage() -> dict:
    return {
        "method": "createPackage",
        "result": {"id": _rand_id()},
    }


def _build_getPackagesList() -> dict:
    pkgs = [_fake_package() for _ in range(random.randint(2, 6))]
    return {
        "method": "getPackagesList",
        "result": {"total": len(pkgs), "items": pkgs},
    }


def _build_deletePackage() -> dict:
    return {"method": "deletePackage", "result": {"result": True}}


def _build_getPackageDetails() -> dict:
    return {
        "method": "getPackageDetails",
        "result": _fake_package(),
    }


_SCENARIOS = [
    _build_getInstallationLinks,
    _build_createPackage,
    _build_getPackagesList,
    _build_deletePackage,
    _build_getPackageDetails,
]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_packages_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone Packages API event."""
    scenario = random.choice(_SCENARIOS)()
    event = {
        "timestamp": _now_iso(),
        "vendor": "bitdefender",
        "product": "gravityzone",
        "api": "packages",
        "jsonrpc": "2.0",
        "method": scenario["method"],
        "id": _rand_id(),
        "result": scenario["result"],
    }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_packages_log(), indent=2))
