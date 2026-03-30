"""
Bitdefender GravityZone - Reports API Event Generator
API Endpoint: /v1.0/jsonrpc/reports
Methods: createReport, getReportsList, getDownloadLinks, deleteReport
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

_REPORT_TYPES = [
    "malwareStatus", "networkStatus", "policyCompliance",
    "updateStatus", "licenseUsage", "executiveSummary",
    "topMalware", "topTargetedEndpoints", "deviceControl",
    "webCategoryTraffic", "firewallActivity", "scanTaskStatus",
]
_REPORT_FORMATS = ["pdf", "csv", "xlsx"]
_REPORT_FREQUENCIES = ["once", "daily", "weekly", "monthly"]
_REPORT_STATUSES = ["pending", "running", "finished", "error"]


# ── Private builders ──────────────────────────────────────────────────────────

def _build_createReport() -> dict:
    return {
        "method": "createReport",
        "result": {"id": _rand_id()},
    }


def _build_getReportsList() -> dict:
    report_type = random.choice(_REPORT_TYPES)
    reports = [
        {
            "id": _rand_id(),
            "name": f"{report_type}-{random.randint(1, 100)}",
            "type": random.choice(_REPORT_TYPES),
            "format": random.choice(_REPORT_FORMATS),
            "frequency": random.choice(_REPORT_FREQUENCIES),
            "status": random.choice(_REPORT_STATUSES),
            "scheduledDate": _now_iso(),
            "createdAt": _now_iso(),
            "size": random.randint(50000, 5000000),
        }
        for _ in range(random.randint(2, 8))
    ]
    return {
        "method": "getReportsList",
        "result": {
            "total": len(reports),
            "page": 1,
            "perPage": 30,
            "pagesCount": 1,
            "items": reports,
        },
    }


def _build_getDownloadLinks() -> dict:
    base = "https://cloud.gravityzone.bitdefender.com/reports"
    links = [
        {
            "id": _rand_id(),
            "link": f"{base}/{_rand_id()}/download",
            "expiresAt": _now_iso(),
        }
        for _ in range(random.randint(1, 3))
    ]
    return {
        "method": "getDownloadLinks",
        "result": {"downloadLinks": links},
    }


def _build_deleteReport() -> dict:
    return {"method": "deleteReport", "result": {"result": True}}


_SCENARIOS = [
    _build_createReport,
    _build_getReportsList,
    _build_getDownloadLinks,
    _build_deleteReport,
]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_reports_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone Reports API event."""
    scenario = random.choice(_SCENARIOS)()
    event = {
        "timestamp": _now_iso(),
        "vendor": "bitdefender",
        "product": "gravityzone",
        "api": "reports",
        "jsonrpc": "2.0",
        "method": scenario["method"],
        "id": _rand_id(),
        "result": scenario["result"],
    }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_reports_log(), indent=2))
