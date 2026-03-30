"""
Bitdefender GravityZone - Network API Event Generator
API Endpoint: /v1.0/jsonrpc/network
Methods: getEndpointsList, getManagedEndpointDetails, createCustomGroup,
         deleteCustomGroup, getCustomGroupsList, moveEndpoints, deleteEndpoint,
         moveCustomGroup, getNetworkInventoryItems, createScanTask,
         getScanTasksList, setEndpointLabel
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

def _rand_hostname() -> str:
    return f"{random.choice(['DESKTOP', 'LAPTOP', 'WKS', 'SRV', 'WIN10'])}-{random.randint(1000, 9999)}"

def _rand_ip() -> str:
    return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def _rand_mac() -> str:
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))


# ── Domain constants ──────────────────────────────────────────────────────────

_OS_TYPES = ["Windows 10", "Windows 11", "Windows Server 2019", "Ubuntu 22.04", "macOS 13"]
_AGENT_VERSIONS = ["7.9.5.177", "7.8.4.160", "7.7.3.140"]
_SCAN_TYPES = [1, 2, 3]  # 1=quick, 2=full, 3=custom
_POLICY_NAMES = ["Default Policy", "Strict Policy", "Server Policy"]
_LABELS = ["", "critical-server", "dev-machine", "finance"]


# ── Private builders ──────────────────────────────────────────────────────────

def _fake_endpoint() -> dict:
    return {
        "id": _rand_id(),
        "name": _rand_hostname(),
        "fqdn": f"{_rand_hostname().lower()}.corp.example.com",
        "groupId": _rand_id(),
        "isManaged": True,
        "operatingSystemVersion": random.choice(_OS_TYPES),
        "ip": _rand_ip(),
        "macs": [_rand_mac()],
        "agentVersion": random.choice(_AGENT_VERSIONS),
        "state": random.choice([1, 2, 3]),
        "lastSeen": _now_iso(),
        "policy": {
            "id": _rand_id(),
            "name": random.choice(_POLICY_NAMES),
        },
        "modules": {
            "antimalware": {"installed": True, "running": True},
            "firewall": {"installed": random.choice([True, False]), "running": True},
            "advancedThreatControl": {"installed": True, "running": True},
            "contentControl": {"installed": random.choice([True, False]), "running": True},
        },
        "riskScore": round(random.uniform(0.0, 10.0), 2),
        "label": random.choice(_LABELS),
    }


def _build_getEndpointsList() -> dict:
    endpoints = [_fake_endpoint() for _ in range(random.randint(3, 10))]
    return {
        "method": "getEndpointsList",
        "result": {
            "total": len(endpoints),
            "page": 1,
            "perPage": 30,
            "pagesCount": 1,
            "items": endpoints,
        },
    }


def _build_getManagedEndpointDetails() -> dict:
    return {
        "method": "getManagedEndpointDetails",
        "result": _fake_endpoint(),
    }


def _build_createCustomGroup() -> dict:
    return {
        "method": "createCustomGroup",
        "result": {"id": _rand_id()},
    }


def _build_deleteCustomGroup() -> dict:
    return {
        "method": "deleteCustomGroup",
        "result": {"result": True},
    }


def _build_getCustomGroupsList() -> dict:
    groups = [
        {"id": _rand_id(), "name": f"Group-{random.randint(1, 50)}", "parentId": None}
        for _ in range(random.randint(2, 6))
    ]
    return {
        "method": "getCustomGroupsList",
        "result": {"items": groups},
    }


def _build_moveEndpoints() -> dict:
    return {"method": "moveEndpoints", "result": {"result": True}}


def _build_deleteEndpoint() -> dict:
    return {"method": "deleteEndpoint", "result": {"result": True}}


def _build_moveCustomGroup() -> dict:
    return {"method": "moveCustomGroup", "result": {"result": True}}


def _build_getNetworkInventoryItems() -> dict:
    items = [
        {
            "id": _rand_id(),
            "name": _rand_hostname(),
            "type": random.choice(["computer", "virtualMachine", "mobileDevice"]),
            "ip": _rand_ip(),
            "operatingSystem": random.choice(_OS_TYPES),
            "lastSeen": _now_iso(),
        }
        for _ in range(random.randint(3, 10))
    ]
    return {
        "method": "getNetworkInventoryItems",
        "result": {"total": len(items), "items": items},
    }


def _build_createScanTask() -> dict:
    return {
        "method": "createScanTask",
        "result": {"id": _rand_id()},
    }


def _build_getScanTasksList() -> dict:
    tasks = [
        {
            "id": _rand_id(),
            "name": f"ScanTask-{random.randint(100, 999)}",
            "status": random.choice([1, 2, 3]),
            "scanType": random.choice(_SCAN_TYPES),
            "startDate": _now_iso(),
            "endDate": _now_iso() if random.choice([True, False]) else None,
            "targetEndpoints": [_rand_id() for _ in range(random.randint(1, 5))],
        }
        for _ in range(random.randint(1, 5))
    ]
    return {
        "method": "getScanTasksList",
        "result": {"total": len(tasks), "items": tasks},
    }


def _build_setEndpointLabel() -> dict:
    return {"method": "setEndpointLabel", "result": {"result": True}}


_SCENARIOS = [
    _build_getEndpointsList,
    _build_getManagedEndpointDetails,
    _build_createCustomGroup,
    _build_deleteCustomGroup,
    _build_getCustomGroupsList,
    _build_moveEndpoints,
    _build_deleteEndpoint,
    _build_moveCustomGroup,
    _build_getNetworkInventoryItems,
    _build_createScanTask,
    _build_getScanTasksList,
    _build_setEndpointLabel,
]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_network_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone Network API event."""
    scenario = random.choice(_SCENARIOS)()
    event = {
        "timestamp": _now_iso(),
        "vendor": "bitdefender",
        "product": "gravityzone",
        "api": "network",
        "jsonrpc": "2.0",
        "method": scenario["method"],
        "id": _rand_id(),
        "result": scenario["result"],
    }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_network_log(), indent=2))
