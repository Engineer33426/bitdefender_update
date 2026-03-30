"""
Bitdefender GravityZone - Quarantine API Event Generator
API Endpoint: /v1.0/jsonrpc/quarantine
Methods: getQuarantineItemsList, createRemoveQuarantineItemTask,
         createRestoreQuarantineItemTask, createRemoveQuarantineExchangeItemTask,
         createRestoreQuarantineExchangeItemTask
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


# ── Domain constants ──────────────────────────────────────────────────────────

_QUARANTINE_REASONS = [
    "on-access-scan", "on-demand-scan", "real-time-scan",
    "manual", "exchange-scan", "policy-action",
]
_MALWARE_NAMES = [
    "Trojan.GenericKD.123456", "Ransomware.WannaCry", "Adware.BrowseFox",
    "Exploit.CVE-2021-44228", "Backdoor.Cobalt.Strike", "PUA.CoinMiner",
]
_FILE_PATHS = [
    "C:\\Users\\user\\Downloads\\infected.exe",
    "C:\\Windows\\Temp\\payload.dll",
    "/tmp/.malware",
]
_EMAIL_SUBJECTS = ["Invoice", "Urgent Notice", "Account Suspended"]


# ── Private builders ──────────────────────────────────────────────────────────

def _fake_quarantine_item(exchange: bool = False) -> dict:
    item: dict = {
        "id": _rand_id(),
        "endpointId": _rand_id(),
        "computerName": _rand_hostname(),
        "malwareName": random.choice(_MALWARE_NAMES),
        "malwareType": random.choice(["virus", "trojan", "ransomware", "adware"]),
        "hash": f"{random.randint(0, 16 ** 64 - 1):064x}",
        "quarantineDate": _now_iso(),
        "reason": random.choice(_QUARANTINE_REASONS),
        "status": random.choice(["quarantined", "pending-delete", "pending-restore"]),
    }
    if exchange:
        item["senderEmail"] = f"attacker{random.randint(1, 99)}@malicious.com"
        item["recipientEmail"] = f"user{random.randint(1, 100)}@example.com"
        item["subject"] = random.choice(_EMAIL_SUBJECTS)
    else:
        item["filePath"] = random.choice(_FILE_PATHS)
        item["fileSize"] = random.randint(1024, 10485760)
    return item


def _build_getQuarantineItemsList() -> dict:
    items = [
        _fake_quarantine_item(exchange=random.choice([True, False]))
        for _ in range(random.randint(2, 8))
    ]
    return {
        "method": "getQuarantineItemsList",
        "result": {
            "total": len(items),
            "page": 1,
            "perPage": 30,
            "pagesCount": 1,
            "items": items,
        },
    }


def _build_createRemoveQuarantineItemTask() -> dict:
    return {
        "method": "createRemoveQuarantineItemTask",
        "result": {
            "taskId": _rand_id(),
            "status": "pending",
            "targetItems": [_rand_id() for _ in range(random.randint(1, 3))],
            "createdAt": _now_iso(),
        },
    }


def _build_createRestoreQuarantineItemTask() -> dict:
    return {
        "method": "createRestoreQuarantineItemTask",
        "result": {
            "taskId": _rand_id(),
            "status": "pending",
            "targetItems": [_rand_id() for _ in range(random.randint(1, 3))],
            "restorePath": "C:\\Users\\user\\Desktop\\restored\\",
            "createdAt": _now_iso(),
        },
    }


def _build_createRemoveQuarantineExchangeItemTask() -> dict:
    return {
        "method": "createRemoveQuarantineExchangeItemTask",
        "result": {
            "taskId": _rand_id(),
            "status": "pending",
            "targetItems": [_rand_id() for _ in range(random.randint(1, 3))],
            "createdAt": _now_iso(),
        },
    }


def _build_createRestoreQuarantineExchangeItemTask() -> dict:
    return {
        "method": "createRestoreQuarantineExchangeItemTask",
        "result": {
            "taskId": _rand_id(),
            "status": "pending",
            "targetItems": [_rand_id() for _ in range(random.randint(1, 2))],
            "createdAt": _now_iso(),
        },
    }


_SCENARIOS = [
    _build_getQuarantineItemsList,
    _build_createRemoveQuarantineItemTask,
    _build_createRestoreQuarantineItemTask,
    _build_createRemoveQuarantineExchangeItemTask,
    _build_createRestoreQuarantineExchangeItemTask,
]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_quarantine_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone Quarantine API event."""
    scenario = random.choice(_SCENARIOS)()
    event = {
        "timestamp": _now_iso(),
        "vendor": "bitdefender",
        "product": "gravityzone",
        "api": "quarantine",
        "jsonrpc": "2.0",
        "method": scenario["method"],
        "id": _rand_id(),
        "result": scenario["result"],
    }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_quarantine_log(), indent=2))
