"""
Bitdefender GravityZone - Push Events API Event Generator
API Endpoint: /v1.0/jsonrpc/push
Methods: setPushEventSettings, getPushEventSettings, sendTestPushEvent,
         getPushEventStats, resetPushEventStats

Also generates all documented push event types:
  av, fw, aph, hd, dp, avc, antiexploit, network-sandboxing,
  uc, registration, modules, exchange-malware,
  exchange-user-credentials, endpoint-moved-in, endpoint-moved-out,
  sva, sva-load, network-monitor
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

def _rand_hash32() -> str:
    return f"{random.randint(0, 0xffffffffffffffffffffffffffffffff):032x}"


# ── Domain constants ──────────────────────────────────────────────────────────

_MALWARE_NAMES = [
    "Trojan.GenericKD.123456", "Ransomware.WannaCry", "Adware.BrowseFox",
    "Exploit.CVE-2021-44228", "Backdoor.Cobalt.Strike", "PUA.CoinMiner",
    "Worm.Conficker", "Spyware.AgentTesla", "Rootkit.NecursDropper",
]
_FW_PROTOCOLS = ["TCP", "UDP", "ICMP"]


# ── Push event payload builders ───────────────────────────────────────────────

def _payload_av() -> tuple[str, dict]:
    return "av", {
        "module": "av",
        "computerName": _rand_hostname(),
        "computerFQDN": f"{_rand_hostname().lower()}.corp.example.com",
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "malwareName": random.choice(_MALWARE_NAMES),
        "malwareType": random.choice(["virus", "trojan", "ransomware", "adware", "spyware"]),
        "filePath": random.choice([
            "C:\\Users\\user\\Downloads\\malware.exe",
            "C:\\Windows\\Temp\\payload.dll",
            "/tmp/malicious_script.sh",
        ]),
        "hash": _rand_hash32(),
        "detectionType": random.randint(1, 10),
        "action": random.choice(["quarantine", "block", "remove", "ignore"]),
        "status": random.choice(["resolved", "pending", "failed"]),
        "timestamp": _now_iso(),
        "username": f"DOMAIN\\user{random.randint(1, 100)}",
    }


def _payload_fw() -> tuple[str, dict]:
    return "fw", {
        "module": "fw",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "localAddress": _rand_ip(),
        "localPort": random.randint(1024, 65535),
        "remoteAddress": _rand_ip(),
        "remotePort": random.randint(1, 65535),
        "protocol": random.choice(_FW_PROTOCOLS),
        "direction": random.choice(["in", "out"]),
        "action": random.choice(["blocked", "allowed"]),
        "applicationPath": random.choice([
            "C:\\Program Files\\App\\app.exe",
            "/usr/bin/python3",
            "C:\\Windows\\System32\\svchost.exe",
        ]),
        "timestamp": _now_iso(),
    }


def _payload_aph() -> tuple[str, dict]:
    return "aph", {
        "module": "aph",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "processName": random.choice(["chrome.exe", "iexplore.exe", "winword.exe", "excel.exe"]),
        "processPath": "C:\\Program Files\\...",
        "exploitTechnique": random.choice([
            "ROP Chain", "Heap Spray", "Stack Pivot", "VBScript God Mode", "NULL Dereference",
        ]),
        "action": random.choice(["block", "report"]),
        "timestamp": _now_iso(),
    }


def _payload_hd() -> tuple[str, dict]:
    return "hd", {
        "module": "hd",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "threatName": random.choice(_MALWARE_NAMES),
        "threatType": random.choice(["fileless", "script", "powershell", "wmi", "macro"]),
        "filePath": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "commandLine": "powershell.exe -encodedcommand " + "A" * random.randint(50, 150),
        "detectionLevel": random.choice(["permissive", "normal", "aggressive"]),
        "action": random.choice(["block", "quarantine", "report"]),
        "timestamp": _now_iso(),
    }


def _payload_dp() -> tuple[str, dict]:
    return "dp", {
        "module": "dp",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "dataType": random.choice(["credit-card", "ssn", "iban", "custom"]),
        "applicationName": random.choice(["chrome.exe", "outlook.exe", "filezilla.exe"]),
        "action": random.choice(["block", "report"]),
        "ruleId": _rand_id(),
        "ruleName": random.choice(["PCI Data Rule", "PII Protection Rule", "Custom DLP Rule"]),
        "timestamp": _now_iso(),
    }


def _payload_avc() -> tuple[str, dict]:
    return "avc", {
        "module": "avc",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "processPath": random.choice([
            "C:\\Windows\\Temp\\loader.exe",
            "C:\\Users\\Public\\Documents\\updater.exe",
        ]),
        "processHash": _rand_hash32(),
        "detectionName": random.choice(_MALWARE_NAMES),
        "action": random.choice(["block", "report", "allow"]),
        "parentProcess": "explorer.exe",
        "commandLine": "cmd.exe /c whoami & ipconfig /all",
        "timestamp": _now_iso(),
    }


def _payload_antiexploit() -> tuple[str, dict]:
    return "antiexploit", {
        "module": "antiexploit",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "exploitedProcess": random.choice(["acrobat.exe", "flash.exe", "java.exe", "office.exe"]),
        "exploitType": random.choice(["CVE-2021-40444", "CVE-2022-30190", "Log4Shell"]),
        "action": random.choice(["block", "disinfect"]),
        "timestamp": _now_iso(),
    }


def _payload_network_sandboxing() -> tuple[str, dict]:
    return "network-sandboxing", {
        "module": "network-sandboxing",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "filePath": "C:\\Downloads\\suspicious.pdf",
        "fileHash": _rand_hash32(),
        "threatName": random.choice(_MALWARE_NAMES),
        "sandboxVerdict": random.choice(["malicious", "suspicious", "clean"]),
        "action": random.choice(["block", "quarantine"]),
        "timestamp": _now_iso(),
    }


def _payload_uc() -> tuple[str, dict]:
    return "uc", {
        "module": "uc",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "username": f"DOMAIN\\user{random.randint(1, 100)}",
        "url": random.choice([
            "http://malware-domain.ru/payload.exe",
            "https://phishing-bank.com/login",
            "http://gambling-site.com",
        ]),
        "category": random.choice(["malware", "phishing", "gambling", "social-networking"]),
        "action": random.choice(["block", "allow"]),
        "timestamp": _now_iso(),
    }


def _payload_registration() -> tuple[str, dict]:
    return "registration", {
        "module": "registration",
        "computerName": _rand_hostname(),
        "computerFQDN": f"{_rand_hostname().lower()}.corp.example.com",
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "action": random.choice(["new-endpoint", "re-registered", "unregistered"]),
        "operatingSystem": random.choice(["Windows 10", "Windows 11", "Ubuntu 22.04"]),
        "agentVersion": (
            f"7.{random.randint(5, 9)}.{random.randint(0, 5)}.{random.randint(100, 200)}"
        ),
        "timestamp": _now_iso(),
    }


def _payload_modules() -> tuple[str, dict]:
    return "modules", {
        "module": "modules",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "moduleStatuses": {
            "antimalware": random.choice(["running", "stopped", "error"]),
            "firewall": random.choice(["running", "stopped", "not-installed"]),
            "advancedThreatControl": random.choice(["running", "stopped"]),
            "contentControl": random.choice(["running", "stopped", "not-installed"]),
            "deviceControl": random.choice(["running", "not-installed"]),
            "patchManagement": random.choice(["running", "stopped", "not-installed"]),
        },
        "timestamp": _now_iso(),
    }


def _payload_exchange_malware() -> tuple[str, dict]:
    return "exchange-malware", {
        "module": "exchange-malware",
        "serverName": f"EXCH-{random.randint(1, 5)}",
        "serverIp": _rand_ip(),
        "senderEmail": f"attacker{random.randint(1, 100)}@evil.com",
        "recipientEmail": f"user{random.randint(1, 100)}@example.com",
        "subject": random.choice(["Invoice #12345", "Urgent: Your account", "RE: Meeting"]),
        "malwareName": random.choice(_MALWARE_NAMES),
        "attachmentName": random.choice(["invoice.pdf.exe", "document.docm", "report.zip"]),
        "action": random.choice(["deleted", "quarantine", "blocked"]),
        "timestamp": _now_iso(),
    }


def _payload_exchange_user_credentials() -> tuple[str, dict]:
    return "exchange-user-credentials", {
        "module": "exchange-user-credentials",
        "serverName": f"EXCH-{random.randint(1, 5)}",
        "serverIp": _rand_ip(),
        "username": f"DOMAIN\\user{random.randint(1, 100)}",
        "action": random.choice(["suspicious-login", "brute-force", "credential-stuffing"]),
        "sourceIp": _rand_ip(),
        "timestamp": _now_iso(),
    }


def _payload_endpoint_moved_in() -> tuple[str, dict]:
    return "endpoint-moved-in", {
        "module": "endpoint-moved-in",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "sourceGroupId": _rand_id(),
        "destinationGroupId": _rand_id(),
        "timestamp": _now_iso(),
    }


def _payload_endpoint_moved_out() -> tuple[str, dict]:
    return "endpoint-moved-out", {
        "module": "endpoint-moved-out",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "sourceGroupId": _rand_id(),
        "destinationGroupId": _rand_id(),
        "timestamp": _now_iso(),
    }


def _payload_sva() -> tuple[str, dict]:
    return "sva", {
        "module": "sva",
        "svaName": f"SVA-{random.randint(1, 5)}",
        "svaIp": _rand_ip(),
        "status": random.choice(["online", "offline", "degraded"]),
        "version": (
            f"6.{random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(100, 500)}"
        ),
        "protectedEndpoints": random.randint(10, 200),
        "timestamp": _now_iso(),
    }


def _payload_sva_load() -> tuple[str, dict]:
    return "sva-load", {
        "module": "sva-load",
        "svaName": f"SVA-{random.randint(1, 5)}",
        "svaIp": _rand_ip(),
        "cpuUsage": round(random.uniform(10.0, 95.0), 1),
        "memoryUsage": round(random.uniform(20.0, 90.0), 1),
        "loadLevel": random.choice(["low", "medium", "high", "critical"]),
        "timestamp": _now_iso(),
    }


def _payload_network_monitor() -> tuple[str, dict]:
    return "network-monitor", {
        "module": "network-monitor",
        "computerName": _rand_hostname(),
        "computerIp": _rand_ip(),
        "endpointId": _rand_id(),
        "remoteIp": _rand_ip(),
        "remotePort": random.randint(1, 65535),
        "protocol": random.choice(_FW_PROTOCOLS),
        "attackType": random.choice([
            "PortScan", "BruteForce", "ARP Poisoning", "DNS Spoofing", "SYN Flood",
        ]),
        "action": random.choice(["block", "report"]),
        "timestamp": _now_iso(),
    }


# Push API management method builders

def _build_setPushEventSettings() -> dict:
    return {"method": "setPushEventSettings", "result": {"result": True}}


def _build_getPushEventSettings() -> dict:
    return {
        "method": "getPushEventSettings",
        "result": {
            "status": 1,
            "serviceType": "json",
            "serviceSettings": {
                "url": "https://siem.example.com:8080/gz/events",
                "requireValidSslCertificate": True,
            },
            "subscribeToEventTypes": {
                "av": True, "fw": True, "aph": True, "hd": True, "dp": True,
                "avc": True, "antiexploit": True, "network-sandboxing": True,
                "uc": True, "registration": True, "modules": True,
                "exchange-malware": True, "exchange-user-credentials": True,
                "endpoint-moved-in": True, "endpoint-moved-out": True,
                "sva": True, "sva-load": True, "network-monitor": True,
            },
        },
    }


def _build_getPushEventStats() -> dict:
    return {
        "method": "getPushEventStats",
        "result": {
            "totalSent": random.randint(1000, 100000),
            "totalFailed": random.randint(0, 50),
            "lastSuccessfulDelivery": _now_iso(),
        },
    }


def _build_resetPushEventStats() -> dict:
    return {"method": "resetPushEventStats", "result": {"result": True}}


def _build_sendTestPushEvent() -> dict:
    return {"method": "sendTestPushEvent", "result": {"result": True}}


# ── Scenario pool ─────────────────────────────────────────────────────────────

_PUSH_EVENT_PAYLOADS = [
    _payload_av, _payload_fw, _payload_aph, _payload_hd,
    _payload_dp, _payload_avc, _payload_antiexploit,
    _payload_network_sandboxing, _payload_uc, _payload_registration,
    _payload_modules, _payload_exchange_malware,
    _payload_exchange_user_credentials, _payload_endpoint_moved_in,
    _payload_endpoint_moved_out, _payload_sva, _payload_sva_load,
    _payload_network_monitor,
]

_MANAGEMENT_SCENARIOS = [
    _build_setPushEventSettings,
    _build_getPushEventSettings,
    _build_getPushEventStats,
    _build_resetPushEventStats,
    _build_sendTestPushEvent,
]


# ── Public generator ──────────────────────────────────────────────────────────

def bitdefender_gravityzone_push_events_log(overrides: dict | None = None) -> dict:
    """Return one simulated GravityZone push event or push API management call."""
    # Weight toward push events (80%) vs management API calls (20%)
    if random.random() < 0.8:
        event_type, data = random.choice(_PUSH_EVENT_PAYLOADS)()
        event = {
            "timestamp": _now_iso(),
            "vendor": "bitdefender",
            "product": "gravityzone",
            "api": "push",
            "jsonrpc": "2.0",
            "method": "push",
            "eventType": event_type,
            "id": _rand_id(),
            "params": {"events": [data]},
        }
    else:
        scenario = random.choice(_MANAGEMENT_SCENARIOS)()
        event = {
            "timestamp": _now_iso(),
            "vendor": "bitdefender",
            "product": "gravityzone",
            "api": "push",
            "jsonrpc": "2.0",
            "method": scenario["method"],
            "id": _rand_id(),
            "result": scenario["result"],
        }
    if overrides:
        event.update(overrides)
    return event


if __name__ == "__main__":
    print(json.dumps(bitdefender_gravityzone_push_events_log(), indent=2))
