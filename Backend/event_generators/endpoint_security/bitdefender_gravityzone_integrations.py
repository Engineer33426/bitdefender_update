"""
Bitdefender GravityZone - Integrations API Event Generator
API Endpoint: /v1.0/jsonrpc/integrations
Methods: getHourlyUsageForAmazonEC2Instances,
         configureAmazonEC2IntegrationUsingCrossAccountRole,
         generateAmazonEC2ExternalIdForCrossAccountRole,
         getAmazonEC2ExternalIdForCrossAccountRole,
         disableAmazonEC2Integration
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

_AWS_REGIONS = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1", "ca-central-1"]
_INSTANCE_TYPES = ["t3.micro", "t3.small", "t3.medium", "m5.large", "c5.xlarge"]


# ── Private builders ──────────────────────────────────────────────────────────

def _build_getHourlyUsageForAmazonEC2Instances() -> dict:
    instances = [
        {
            "instanceId": f"i-{random.randint(0x100000000000, 0xffffffffffff):012x}",
            "instanceType": random.choice(_INSTANCE_TYPES),
            "region": random.choice(_AWS_REGIONS),
            "usageHours": random.randint(1, 744),
            "startDate": _now_iso(),
            "endDate": _now_iso(),
            "licenseConsumed": random.choice([True, False]),
        }
        for _ in range(random.randint(2, 8))
    ]
    return {
        "method": "getHourlyUsageForAmazonEC2Instances",
        "result": {"total": len(instances), "items": instances},
    }


def _build_configureAmazonEC2IntegrationUsingCrossAccountRole() -> dict:
    return {
        "method": "configureAmazonEC2IntegrationUsingCrossAccountRole",
        "result": {
            "result": True,
            "roleArn": (
                f"arn:aws:iam::{random.randint(100000000000, 999999999999)}:"
                "role/BitdefenderGZRole"
            ),
            "regions": random.sample(_AWS_REGIONS, random.randint(1, 3)),
        },
    }


def _build_generateAmazonEC2ExternalIdForCrossAccountRole() -> dict:
    return {
        "method": "generateAmazonEC2ExternalIdForCrossAccountRole",
        "result": {"externalId": str(uuid.uuid4()).replace("-", "")},
    }


def _build_getAmazonEC2ExternalIdForCrossAccountRole() -> dict:
    return {
        "method": "getAmazonEC2ExternalIdForCrossAccountRole",
        "result": {"externalId": str(uuid.uuid4()).replace("-", "")},
    }


def _build_disableAmazonEC2Integration() -> dict:
    return {
        "method": "disableAmazonEC2Integration",
        "result": {"result": True},
    }


_SCENARIOS = [
    _build_getHourlyUsageForAmazonEC2Instances,
    _build_configureAmazonEC2IntegrationUsingCrossAccountRole,
    _build_generateAmazonEC2ExternalIdForCrossAccountRole,
    _build_getAmazonEC2ExternalIdForCrossAccountRole,
    _build_disableAmazonEC2Integration,
]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_integrations_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone Integrations API event."""
    scenario = random.choice(_SCENARIOS)()
    event = {
        "timestamp": _now_iso(),
        "vendor": "bitdefender",
        "product": "gravityzone",
        "api": "integrations",
        "jsonrpc": "2.0",
        "method": scenario["method"],
        "id": _rand_id(),
        "result": scenario["result"],
    }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_integrations_log(), indent=2))
