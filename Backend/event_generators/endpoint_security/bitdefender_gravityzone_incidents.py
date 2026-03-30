"""
Bitdefender GravityZone - Incidents API Event Generator
API Endpoint: /v1.0/jsonrpc/incidents
Methods: addToBlocklist, getBlocklistItems, removeFromBlocklist,
         createIsolateEndpointTask, createRestoreEndpointFromIsolationTask
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

def _random_hash(hash_type: str = "sha256") -> str:
    length = 64 if hash_type == "sha256" else 32
    return f"{random.randint(0, 16 ** length - 1):0{length}x}"


# ── Domain constants ──────────────────────────────────────────────────────────

_HASH_TYPES = ["md5", "sha256"]
_BLOCKLIST_REASONS = ["malware", "suspicious-activity", "policy-violation", "user-request"]
_ISOLATION_REASONS = [
    "ransomware-detected",
    "lateral-movement-suspected",
    "active-incident",
    "threat-investigation",
]


# ── Private builders ──────────────────────────────────────────────────────────

def _build_addToBlocklist() -> dict:
    hash_type = random.choice(_HASH_TYPES)
    return {
        "method": "addToBlocklist",
        "result": {
            "hashType": hash_type,
            "hashList": [_random_hash(hash_type) for _ in range(random.randint(1, 5))],
            "sourceInfo": {
                "type": random.choice(["file", "process"]),
                "computerName": _rand_hostname(),
                "filePath": "C:\\Windows\\Temp\\malware.exe",
            },
            "reason": random.choice(_BLOCKLIST_REASONS),
            "result": True,
        },
    }


def _build_getBlocklistItems() -> dict:
    items = [
        {
            "id": _rand_id(),
            "hash": _random_hash(),
            "hashType": "sha256",
            "addedAt": _now_iso(),
            "addedBy": f"user{random.randint(1, 10)}@example.com",
            "reason": random.choice(_BLOCKLIST_REASONS),
            "status": random.choice(["active", "pending"]),
        }
        for _ in range(random.randint(2, 10))
    ]
    return {
        "method": "getBlocklistItems",
        "result": {"total": len(items), "items": items},
    }


def _build_removeFromBlocklist() -> dict:
    return {
        "method": "removeFromBlocklist",
        "result": {"result": True},
    }


def _build_createIsolateEndpointTask() -> dict:
    return {
        "method": "createIsolateEndpointTask",
        "result": {
            "taskId": _rand_id(),
            "endpointId": _rand_id(),
            "computerName": _rand_hostname(),
            "isolationReason": random.choice(_ISOLATION_REASONS),
            "status": "pending",
            "createdAt": _now_iso(),
        },
    }


def _build_createRestoreEndpointFromIsolationTask() -> dict:
    return {
        "method": "createRestoreEndpointFromIsolationTask",
        "result": {
            "taskId": _rand_id(),
            "endpointId": _rand_id(),
            "computerName": _rand_hostname(),
            "status": "pending",
            "createdAt": _now_iso(),
        },
    }


_SCENARIOS = [
    _build_addToBlocklist,
    _build_getBlocklistItems,
    _build_removeFromBlocklist,
    _build_createIsolateEndpointTask,
    _build_createRestoreEndpointFromIsolationTask,
]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_incidents_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone Incidents API event."""
    scenario = random.choice(_SCENARIOS)()
    event = {
        "timestamp": _now_iso(),
        "vendor": "bitdefender",
        "product": "gravityzone",
        "api": "incidents",
        "jsonrpc": "2.0",
        "method": scenario["method"],
        "id": _rand_id(),
        "result": scenario["result"],
    }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_incidents_log(), indent=2))
