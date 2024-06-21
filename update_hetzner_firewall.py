import os
import requests
from dotenv import load_dotenv

load_dotenv()


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


API_KEY = os.getenv("HETZNER_API_KEY")
FIREWALL_ID = os.getenv("HETZNER_FIREWALL_ID")
NAT_INSTANCE_IP = os.getenv("NAT_INSTANCE_IP")

if not API_KEY:
    raise ValueError("HETZNER_API_KEY not set")

if not FIREWALL_ID:
    raise ValueError("HETZNER_FIREWALL_ID not set")

if not NAT_INSTANCE_IP:
    raise ValueError("NAT_INSTANCE_IP not set")


github_response = requests.get("https://api.github.com/meta")
data = github_response.json()
github_ips = data["hooks"] + data["web"] + data["api"] + data["git"]

rules = [
    {
        "description": "Github action",
        "direction": "in",
        "port": "443",
        "protocol": "tcp",
        "source_ips": ips,
    }
    for ips in chunks(github_ips, 100)
]
rules += [
    {
        "description": "NAT instance",
        "direction": "in",
        "port": "3310",
        "protocol": "tcp",
        "source_ips": [f"{NAT_INSTANCE_IP}/32"],
    },
    {
        "description": "Tailscale",
        "direction": "in",
        "port": "41641",
        "protocol": "udp",
        "source_ips": ["0.0.0.0/0", "::/0"],
    },
]

response = requests.post(
    f"https://api.hetzner.cloud/v1/firewalls/{FIREWALL_ID}/actions/set_rules",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "rules": rules,
    },
)
response.raise_for_status()
print("Done")
