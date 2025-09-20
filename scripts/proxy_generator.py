#!/usr/bin/env python3
"""
Proxy Configuration Generator.

Generates secure proxy configurations for various protocols.
"""

import base64
import json
import random
import string
import uuid
from typing import Dict, List
from urllib.parse import quote


class ProxyGenerator:
    """Generates various proxy configurations."""

    def __init__(self):
        """Initializes the ProxyGenerator."""
        self.servers: List[Dict] = []

    def update_servers(self, new_servers: List[Dict]):
        """Update the server list with new servers."""
        self.servers = new_servers

    def _generate_password(self, length: int = 16) -> str:
        """Generate a random password."""
        return ''.join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )

    def generate_shadowsocks_config(self, server: Dict) -> Dict:
        """Generate Shadowsocks configuration."""
        password = self._generate_password()
        return {
            "server": server["host"],
            "server_port": server["ports"].get("shadowsocks", 8388),
            "password": password,
            "method": "chacha20-ietf-poly1305",
            "remarks": f"SS-{server['country']}-{server['city']}",
        }

    def generate_vmess_config(self, server: Dict) -> Dict:
        """Generate VMess configuration."""
        user_id = str(uuid.uuid4())
        return {
            "v": "2",
            "ps": f"VMess-{server['country']}-{server['city']}",
            "add": server["host"],
            "port": str(server["ports"].get("vmess", 10086)),
            "id": user_id,
            "aid": "0",
            "scy": "auto",
            "net": "ws",
            "type": "none",
            "host": server["host"],
            "path": "/vmess",
            "tls": "tls",
            "sni": server["host"],
        }

    def generate_trojan_config(self, server: Dict) -> Dict:
        """Generate Trojan configuration."""
        password = self._generate_password(32)
        return {
            "password": password,
            "remote_addr": server["host"],
            "remote_port": server["ports"].get("trojan", 443),
            "ssl": {
                "sni": server["host"],
            },
        }

    def export_shadowsocks_subscription(self) -> str:
        """Export Shadowsocks subscription."""
        configs = []
        for server in self.servers:
            ss_config = self.generate_shadowsocks_config(server)
            auth_str = f"{ss_config['method']}:{ss_config['password']}"
            auth_b64 = base64.b64encode(auth_str.encode()).decode()
            ss_url = (
                f"ss://{auth_b64}@{server['host']}:"
                f"{ss_config['server_port']}#{quote(ss_config['remarks'])}"
            )
            configs.append(ss_url)
        return '\n'.join(configs)

    def export_vmess_subscription(self) -> str:
        """Export VMess subscription."""
        configs = []
        for server in self.servers:
            vmess_config = self.generate_vmess_config(server)
            vmess_json = json.dumps(vmess_config, separators=(',', ':'))
            vmess_b64 = base64.b64encode(vmess_json.encode()).decode()
            configs.append(f"vmess://{vmess_b64}")
        return '\n'.join(configs)

    def export_trojan_subscription(self) -> str:
        """Export Trojan subscription."""
        configs = []
        for server in self.servers:
            trojan_config = self.generate_trojan_config(server)
            trojan_url = (
                f"trojan://{trojan_config['password']}@"
                f"{server['host']}:{trojan_config['remote_port']}"
                f"?sni={server['host']}#"
                f"{quote(f'Trojan-{server['country']}-{server['city']}')}"
            )
            configs.append(trojan_url)
        return '\n'.join(configs)

    def export_universal_subscription(self) -> str:
        """Export universal subscription in plain text."""
        all_configs = (
            self.export_shadowsocks_subscription().split('\n')
            + self.export_vmess_subscription().split('\n')
            + self.export_trojan_subscription().split('\n')
        )
        return '\n'.join(filter(None, all_configs))

    def export_universal_subscription_base64(self) -> str:
        """Export universal subscription in base64 format."""
        content = self.export_universal_subscription()
        return base64.b64encode(content.encode()).decode()

    def generate_all_configs(self):
        """Generate all configuration files."""
        config_dir = Path(__file__).parent.parent / "configs"
        config_dir.mkdir(exist_ok=True)

        with open(config_dir / "shadowsocks.txt", "w") as f:
            f.write(self.export_shadowsocks_subscription())
        with open(config_dir / "v2ray.txt", "w") as f:
            f.write(self.export_vmess_subscription())
        with open(config_dir / "universal.txt", "w") as f:
            f.write(self.export_universal_subscription())
        with open(config_dir / "universal-base64.txt", "w") as f:
            f.write(self.export_universal_subscription_base64())


if __name__ == "__main__":
    generator = ProxyGenerator()
    # Add dummy data for standalone execution
    generator.update_servers([
        {
            "host": "example.com",
            "country": "US",
            "city": "Test",
            "ports": {"shadowsocks": 8388, "vmess": 10086, "trojan": 443},
        }
    ])
    generator.generate_all_configs()
    print("✅ All proxy configurations generated successfully!")

