"""
Bitdefender GravityZone - Accounts API Event Generator
API Endpoint: /v1.0/jsonrpc/accounts
Methods: getAccountsList, deleteAccount, createAccount, updateAccount,
         configureNotificationsSettings, getNotificationsSettings
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

_ROLES = [1, 2, 3, 4, 5]  # 1=company admin, 2=network admin, 3=reporter, etc.
_LANGUAGES = ["en_US", "en_GB", "de_DE", "fr_FR", "es_ES"]
_NAMES = ["alice", "bob", "carol", "dave", "eve", "frank"]


# ── Private builders ──────────────────────────────────────────────────────────

def _fake_account() -> dict:
    name = random.choice(_NAMES)
    return {
        "id": _rand_id(),
        "email": f"{name}.{random.randint(10, 99)}@example.com",
        "profile": {
            "fullName": name.capitalize() + " Smith",
            "timezone": "UTC",
            "preferredLanguage": random.choice(_LANGUAGES),
        },
        "role": random.choice(_ROLES),
        "isActive": random.choice([True, True, True, False]),
        "twoFactorAuthEnabled": random.choice([True, False]),
        "lastLogin": _now_iso(),
    }


def _build_getAccountsList() -> dict:
    accounts = [_fake_account() for _ in range(random.randint(2, 6))]
    return {
        "method": "getAccountsList",
        "result": {
            "total": len(accounts),
            "page": 1,
            "perPage": 30,
            "pagesCount": 1,
            "items": accounts,
        },
    }


def _build_createAccount() -> dict:
    return {
        "method": "createAccount",
        "result": {"id": _rand_id()},
    }


def _build_updateAccount() -> dict:
    return {
        "method": "updateAccount",
        "result": {"result": True},
    }


def _build_deleteAccount() -> dict:
    return {
        "method": "deleteAccount",
        "result": {"result": True},
    }


def _build_configureNotificationsSettings() -> dict:
    return {
        "method": "configureNotificationsSettings",
        "result": {"result": True},
    }


def _build_getNotificationsSettings() -> dict:
    return {
        "method": "getNotificationsSettings",
        "result": {
            "notifications": {
                "malwareDetectionAlert": {
                    "sendEmail": True,
                    "emailAddresses": ["soc@example.com"],
                },
                "blocklistThreats": {"sendEmail": False, "emailAddresses": []},
                "productRegistration": {
                    "sendEmail": True,
                    "emailAddresses": ["admin@example.com"],
                },
                "licenseExpiration": {
                    "sendEmail": True,
                    "emailAddresses": ["admin@example.com"],
                },
            }
        },
    }


_SCENARIOS = [
    _build_getAccountsList,
    _build_createAccount,
    _build_updateAccount,
    _build_deleteAccount,
    _build_configureNotificationsSettings,
    _build_getNotificationsSettings,
]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_accounts_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone Accounts API event."""
    scenario = random.choice(_SCENARIOS)()
    event = {
        "timestamp": _now_iso(),
        "vendor": "bitdefender",
        "product": "gravityzone",
        "api": "accounts",
        "jsonrpc": "2.0",
        "method": scenario["method"],
        "id": _rand_id(),
        "result": scenario["result"],
    }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_accounts_log(), indent=2))
